import numpy as np
from colorsys import rgb_to_hsv


def read_data_an_convert_to_hsv(filename: str) -> np.ndarray:
    data = []
    with open(filename, 'r') as file:
        for line in file.readlines():
            line_list: list = line[:-1].split(' ')
            line_list[0] = int(line_list[0])
            line_list[1] = int(line_list[1])
            line_list[2] = int(line_list[2])
            data.append(line_list)

    def hex2hsv(hex_color: str) -> np.ndarray:
        hex_color = int('0x' + str(hex_color), base=16)
        r = (hex_color >> 16) / 255
        g = ((hex_color >> 8) % 256) / 255
        b = (hex_color % 256) / 255
        return np.array(rgb_to_hsv(r, g, b))

    for i in range(len(data)):
        line = data[i]
        hsv = hex2hsv(line[3])
        coords = np.array(line[:3])
        data[i] = np.concatenate((coords, hsv))

    return np.array(data)


def find_points_with_max_z(data: np.ndarray) -> np.ndarray:
    z = data[:, 2]
    indexes_of_points_with_max_z = np.atleast_1d(np.argmax(z))
    return np.array([data[idx] for idx in indexes_of_points_with_max_z])


def select_point_with_max_saturation(points: np.ndarray) -> np.ndarray:
    index_of_point_with_max_saturation = np.atleast_1d(np.argmax(points[:, 4]))[0]
    return points[index_of_point_with_max_saturation]


def get_nearest_points(data: np.ndarray, point: np.ndarray, dist: int) -> np.ndarray:
    x, y, z, h, s, v = point
    filter_ = (abs(x - data[:, 0]) <= dist) &\
              (abs(y - data[:, 1]) <= dist) &\
              (abs(z - data[:, 2]) <= dist)
    return data[filter_]


def get_points_mean_hsv(points: np.ndarray) -> np.ndarray:
    colors = points[:, 3:]
    return np.mean(colors, axis=0)


def hsv2eng(hsv: np.ndarray) -> str:
    h, s, v = hsv
    if h < 1 / 3 or h > 5 / 6:
        return 'RED'
    return 'BLUE'


if __name__ == '__main__':
    raw_data = read_data_an_convert_to_hsv(filename='input.txt')
    highest_points = find_points_with_max_z(raw_data)
    highest_point = select_point_with_max_saturation(highest_points)
    points_nearest_to_highest = get_nearest_points(raw_data, highest_point, 2)
    mean_hsv = get_points_mean_hsv(points_nearest_to_highest)
    color = hsv2eng(mean_hsv)

    print('%i %s' % (abs(highest_point[2]), color))
