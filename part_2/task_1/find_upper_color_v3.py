import numpy as np
from colorsys import rgb_to_hsv
from vedo import *


def read_data(filename: str) -> list:
    with open(filename, 'r') as file:
        data = []
        lines = file.readlines()
        for line in lines:
            line_list: list = line[:-1].split(' ')
            line_list[0] = int(line_list[0])
            line_list[1] = int(line_list[1])
            line_list[2] = int(line_list[2])
            data.append(line_list)
        return data


def hex2hsv(hex_color: str) -> tuple:
    hex_color = int('0x' + hex_color, base=16)
    r = (hex_color >> 16) / 255
    g = ((hex_color >> 8) % 256) / 255
    b = (hex_color % 256) / 255
    return rgb_to_hsv(r, g, b)


def is_red_blue_or_neither(hsv_color: tuple, s_threshold_: float) -> int:
    if hsv_color[1] < s_threshold_:
        # neutral
        return 0
    if hsv_color[0] < 1 / 3 or hsv_color[0] > 5 / 6:
        # red
        return 1
    # blue
    return 2


def convert_colors(data: list, s_threshold_: float) -> list:
    for i in range(len(data)):
        data[i][3] = is_red_blue_or_neither(hex2hsv(data[i][3]), s_threshold_)
    return data


def get_image_boundaries(data: list) -> tuple:
    maxX = -1e4
    minX = 1e4
    maxY = -1e4
    minY = 1e4
    maxZ = -1e4
    minZ = 1e4
    for line in data:
        if line[0] > maxX:
            maxX = line[0]
        if line[0] < minX:
            minX = line[0]
        if line[1] > maxY:
            maxY = line[1]
        if line[1] < minY:
            minY = line[1]
        if line[2] > maxZ:
            maxZ = line[2]
        if line[2] < minZ:
            minZ = line[2]
    return (minX, maxX), (minY, maxY), (minZ, maxZ)


def coords_bitmap2real(bitmap_x: int, bitmap_y: int, boundaries_: tuple) -> tuple:
    real_x = bitmap_x + boundaries_[0][0]
    real_y = bitmap_y + boundaries_[1][0]
    return real_x, real_y


def coords_real2bitmap(real_x: int, real_y: int, real_z: int, boundaries_: tuple) -> tuple:
    bitmap_x = real_x - boundaries_[0][0]
    bitmap_y = real_y - boundaries_[1][0]
    bitmap_z = real_z - boundaries_[2][0]
    return bitmap_x, bitmap_y, bitmap_z


def convert_data_to_3d_array(data: list, boundaries_: tuple) -> np.ndarray:
    width = boundaries_[0][1] - boundaries_[0][0] + 1
    height = boundaries_[1][1] - boundaries_[1][0] + 1
    depth = boundaries_[2][1] - boundaries_[2][0] + 1

    array_3d = np.zeros((depth, height, width))
    for line in data:
        x, y, z = coords_real2bitmap(line[0], line[1], line[2], boundaries_)
        if array_3d[z, y, x] == 0:
            array_3d[z, y, x] = line[3]

    return array_3d


def convolution3d(image: np.ndarray, kernel_: np.ndarray) -> np.ndarray:
    k, m, n = kernel_.shape  # k = m = n
    z, y, x = image.shape

    z = z - m + 1
    y = y - m + 1
    x = x - m + 1

    new_image = np.zeros((z, y, x))
    for i in range(z):
        for j in range(y):
            for k in range(x):
                new_image[i, j, k] = np.sum(image[i:i + m, j:j + m, k:k + m] * kernel_)

    return new_image


def visualize_3d_array(data: np.ndarray):
    number_of_points = np.count_nonzero(data)
    coordinates_ = np.empty((number_of_points, 3))
    colors_ = np.empty((number_of_points, 3))

    cnt = 0
    for index, value in np.ndenumerate(data):
        if value != 0:
            coordinates_[cnt] = np.array(index)
            if value == 1:
                colors_[cnt] = np.array([255, 0, 0, 255])
            if value == 2:
                colors_[cnt] = np.array([0, 0, 255, 255])

    cloud = Points(inputobj=coordinates_, c=colors_, r=10)
    show(cloud, __doc__, axes=True, interactive=True)


def color_int2eng(color_int: int) -> str:
    if color_int == 1:
        return 'RED'
    elif color_int == 2:
        return 'BLUE'


'''def get_highest_point_distance_and_color(bitmap_: Bitmap) -> tuple:
    maxZ = -1e4
    maxX = -1e4
    maxY = -1e4
    for indexes, z in np.ndenumerate(bitmap_.heights):
        if bitmap_.colors[indexes[0], indexes[1]] == 0:
            continue
        if z > maxZ:
            maxZ = z
            maxX = indexes[1]
            maxY = indexes[0]
    color_ = color_int2eng(bitmap_.colors[maxY, maxX])
    return abs(maxZ), color_'''


if __name__ == '__main__':
    raw_data = read_data(filename='input.txt')
    raw_data = convert_colors(raw_data, 0.6)
    boundaries = get_image_boundaries(raw_data)

    three_d = convert_data_to_3d_array(raw_data, boundaries)
    kernel_size = 30
    kernel = np.ones((kernel_size, kernel_size, kernel_size))
    three_d = convolution3d(three_d, kernel) / kernel_size ** 3
    visualize_3d_array(three_d)
    '''dist, color = get_highest_point_distance_and_color(bitmap)
    print('%i %s' % (dist, color))'''
