from colorsys import rgb_to_hsv

import numpy as np
from vedo import *


MIN_POINTS_FOR_Z_THRESHOLD = 500
Z_THRESHOLD_MARGIN = 2
MIN_SATURATION = .69
FILENAME = '../part_4/task_2/samples/1'


def rgb2hsv(rgb_color: np.ndarray) -> tuple:
    rgb_color = rgb_color / 255
    return rgb_to_hsv(rgb_color[0], rgb_color[1], rgb_color[2])


def get_color(hsv_color: tuple) -> int:
    if hsv_color[1] < MIN_SATURATION:
        return 0
    if 1 / 3 < hsv_color[0] < 5 / 6:
        return -1
    return 1


def read_data(filename: str) -> tuple[np.ndarray, np.ndarray]:
    data = np.fromfile(filename, dtype=int, count=-1, sep=' ', offset=0)
    data = np.reshape(data, (-1, 6))

    min_z = np.min(data[:, 2])
    max_z = np.max(data[:, 2])
    z_distribution = np.zeros(max_z - min_z + 1)
    for row in data:
        color = get_color(rgb2hsv(row[3:]))
        if color != 0:
            z_distribution[row[2] - min_z] += 1
    z_threshold = min_z
    for i in range(len(z_distribution) - 1, -1, -1):
        if z_distribution[i] >= MIN_POINTS_FOR_Z_THRESHOLD:
            z_threshold = min_z + i - Z_THRESHOLD_MARGIN
    data = data[data[:, 2] >= z_threshold]

    coordinates_ = data[:, :3]
    colors_ = data[:, 3:]
    colors_ = np.pad(colors_, ((0, 0), (0, 1)), constant_values=(255,))
    return coordinates_, colors_


if __name__ == '__main__':
    coordinates, colors = read_data(filename=FILENAME)
    cloud = Points(inputobj=coordinates, c=colors, r=10)
    show(cloud, __doc__, axes=True,  interactive=True)
