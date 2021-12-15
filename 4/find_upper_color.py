import numpy as np
from colorsys import rgb_to_hsv
from collections import namedtuple

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


def is_red_blue_or_neither(hsv_color: tuple) -> int:
    if hsv_color[1] < 0.4 or hsv_color[2] < 0.4:
        # neutral
        return 0
    if hsv_color[0] < 1 / 3 or hsv_color[0] > 5 / 6:
        # red
        return 1
    # blue
    return 2


def convert_colors(data: list) -> list:
    for i in range(len(data)):
        data[i][3] = is_red_blue_or_neither(hex2hsv(data[i][3]))
    return data


def get_image_boundaries(data: list) -> tuple:
    maxX = -1e4
    minX = 1e4
    maxY = -1e4
    minY = 1e4
    for line in data:
        if line[0] > maxX:
            maxX = line[0]
        if line[0] < minX:
            minX = line[0]
        if line[1] > maxY:
            maxY = line[1]
        if line[1] < minY:
            minY = line[1]
    return (minX, maxX), (minY, maxY)


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
    heights_ = np.empty(shape=(height, width))
    colors_ = np.empty(shape=(height, width))
    for line in data:
        x, y = coords_real2bitmap(line[0], line[1], boundaries_)
        if heights_[y, x] == 0:
            heights_[y, x] = -1e3
        if heights_[y, x] > line[2]:
            continue
        heights_[y, x] = line[2]
        colors_[y, x] = line[3]
    return Bitmap(heights_, colors_)


def color_int2eng(color_int: int) -> str:
    if color_int == 1:
        return 'RED'
    elif color_int == 2:
        return 'BLUE'
    else:
        return 'WTF'


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
    raw_data = convert_colors(raw_data)
    boundaries = get_image_boundaries(raw_data)
    bitmap = convert_data_to_bitmap(raw_data, boundaries)
    dist, color = get_highest_point_distance_and_color(bitmap)
    print('%i %s' % (dist, color))
