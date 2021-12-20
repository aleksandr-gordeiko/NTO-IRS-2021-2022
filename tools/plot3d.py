import math
from colorsys import rgb_to_hsv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


def read_data(filename: str) -> tuple:
    with open(filename, 'r') as file:
        data = []
        min_z = 1e3
        max_z = -1e3
        lines = file.readlines()
        for line in lines:
            line_list: list = line[:-1].split(' ')
            line_list[0] = int(line_list[0])
            line_list[1] = int(line_list[1])
            line_list[2] = int(line_list[2])
            if line_list[2] > max_z:
                max_z = line_list[2]
            if line_list[2] < min_z:
                min_z = line_list[2]
            data.append(line_list)
        return data, min_z, max_z


def hex2hsv(hex_color: str) -> tuple:
    hex_color = int('0x' + hex_color, base=16)
    r = (hex_color >> 16) / 255
    g = ((hex_color >> 8) % 256) / 255
    b = (hex_color % 256) / 255
    return rgb_to_hsv(r, g, b)


if __name__ == '__main__':
    raw_data, minZ, maxZ = read_data(filename='3')
    height = maxZ - minZ + 1
    plane = np.ones((1001, height))
    x = np.linspace(0, height, height)
    y = np.linspace(0, 1001, 1001)
    X, Y = np.meshgrid(x, y)

    for row in raw_data:
        h, s, v = hex2hsv(row[3])
        s_scaled = math.floor(s * 1000)
        z = row[2] - minZ
        plane[s_scaled, z] += 1

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot_surface(X, Y, np.log10(plane))
    ax.set_title('Saturation, Z')
    plt.show()
