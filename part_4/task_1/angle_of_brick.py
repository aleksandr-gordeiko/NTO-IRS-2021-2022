from colorsys import rgb_to_hsv
import numpy as np

# import matplotlib.pyplot as plt
# from vedo import *


# Reads a Nx6 matrix from file
def read_data(filename: str) -> np.ndarray:
    data = np.fromfile(filename, dtype=int, count=-1, sep=' ', offset=0)
    data = np.reshape(data, (-1, 6))
    # data = np.delete(data, 2, 1)
    return data


# converts RGB color array(1, 3) to HSV
def rgb2hsv(rgb_color: np.ndarray) -> tuple:
    rgb_color = rgb_color / 255
    return rgb_to_hsv(rgb_color[0], rgb_color[1], rgb_color[2])


# Determines if color is red based on its HSV values
def is_color_red(hsv_color: tuple) -> int:
    if hsv_color[1] < 0.69:
        return 0
    if 1 / 3 < hsv_color[0] < 5 / 6:
        return 0
    return 1


# Selects only red points from data and truncates all columns but X and Y
def select_only_red(data: np.ndarray) -> np.ndarray:
    data_filtered = []
    for row in data:
        is_red = is_color_red(rgb2hsv(row[3:]))
        if is_red:
            data_filtered.append(row[:3])

    return np.array(data_filtered)


# Returns X and Y coordinates of points' cloud center of mass
def get_center_of_mass(points: np.ndarray) -> np.ndarray:
    return np.mean(points, axis=0)


# Returns moment of inertia along axis, drawn through the given center at given angle
def calculate_moment_of_inertia(points: np.ndarray, center: np.ndarray, axis_angle: int) -> np.ndarray:
    points_relative = points - center
    k = np.tan(np.deg2rad(axis_angle))
    nominator = np.matmul(points_relative, np.array([k, 1, 0]))
    denominator = np.sqrt(np.square(k) + 1)
    distances = nominator / denominator
    return np.sum(np.square(distances))


if __name__ == '__main__':
    raw_data = read_data(filename='input.txt')
    red_points = select_only_red(raw_data)
    center_of_mass = get_center_of_mass(red_points)

    moments = []
    angles = range(0, 180)
    for angle in angles:
        moments.append(calculate_moment_of_inertia(red_points, center_of_mass, angle))

    # plt.plot(angles, moments)
    # plt.scatter(red_points[:, 0], red_points[:, 1], c='red')
    # plt.show()
    # cloud = Points(inputobj=red_points, c='red', r=10)
    # show(cloud, __doc__, axes=True, interactive=True)

    moments = np.array(moments)
    print(np.argmin(moments) - 90)
