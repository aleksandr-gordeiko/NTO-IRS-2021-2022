#  import math
import numpy as np
from colorsys import rgb_to_hsv
from collections import namedtuple
#  import matplotlib.pyplot as plt

Bitmap = namedtuple('Bitmap', ['heights', 'colors'])


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


'''def get_saturation_threshold(data: list, boundaries_: tuple) -> float:
    filter_size = 100
    x = np.arange(1000 + filter_size)
    x0 = np.arange(1001)
    saturation_distr = np.zeros(1001)

    minZ = boundaries_[2][0] + (boundaries_[2][1] - boundaries_[2][0]) * 0.99
    for row in data:
        if row[2] > minZ:
            row_hsv = hex2hsv(row[3])
            saturation_distr[math.floor(row_hsv[1] * 1000)] += 1

    plt.figure()
    plt.plot(x0, saturation_distr)
    plt.title('Saturation')
    plt.show()

    plt.figure()
    plt.plot(x0, saturation_distr)
    plt.title('Saturation log')
    plt.yscale('log')
    plt.show()

    smoothing_filter = np.ones(filter_size)/filter_size
    saturation_distr = np.convolve(saturation_distr, smoothing_filter)

    plt.figure()
    plt.plot(x, saturation_distr)
    plt.title('Saturation log smoothed')
    plt.yscale('log')
    plt.show()

    minimums = np.argmin(saturation_distr)
    try:
        return minimums[0] / 1000
    except IndexError:
        return minimums / 1000'''


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


def coords_real2bitmap(real_x: int, real_y: int, boundaries_: tuple) -> tuple:
    bitmap_x = real_x - boundaries_[0][0]
    bitmap_y = real_y - boundaries_[1][0]
    return bitmap_x, bitmap_y


def convert_data_to_bitmap(data: list, boundaries_: tuple) -> Bitmap:
    width = boundaries_[0][1] - boundaries_[0][0] + 1
    height = boundaries_[1][1] - boundaries_[1][0] + 1
    heights_ = np.full(shape=(height, width), fill_value=-1e3)
    colors_ = np.zeros(shape=(height, width))
    for line in data:
        x, y = coords_real2bitmap(line[0], line[1], boundaries_)
        if line[2] < heights_[y, x] or line[3] == 0:
            continue
        heights_[y, x] = line[2]
        colors_[y, x] = line[3]
    return Bitmap(heights_, colors_)


def color_int2eng(color_int: int) -> str:
    if color_int == 1:
        return 'RED'
    elif color_int == 2:
        return 'BLUE'


def get_highest_point_distance_and_color(bitmap_: Bitmap) -> tuple:
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
    return abs(maxZ), color_


if __name__ == '__main__':
    raw_data = read_data(filename='input.txt')
    boundaries = get_image_boundaries(raw_data)
    #  s_threshold = get_saturation_threshold(raw_data, boundaries)
    #  print(s_threshold)
    raw_data = convert_colors(raw_data, .6)
    bitmap = convert_data_to_bitmap(raw_data, boundaries)
    dist, color = get_highest_point_distance_and_color(bitmap)
    print('%i %s' % (dist, color))
