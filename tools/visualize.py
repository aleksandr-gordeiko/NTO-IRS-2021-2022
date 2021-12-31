import numpy as np
from vedo import *


Z_THRESHOLDING = .5
FILENAME = '../part_4/task_2/samples/1'


def read_data(filename: str) -> tuple[np.ndarray, np.ndarray]:
    data = np.fromfile(filename, dtype=int, count=-1, sep=' ', offset=0)
    data = np.reshape(data, (-1, 6))

    min_z = np.min(data[:, 2])
    max_z = np.max(data[:, 2])
    z_threshold = min_z + (max_z - min_z) * Z_THRESHOLDING
    data = data[data[:, 2] > z_threshold, :]

    coordinates_ = data[:, :3]
    colors_ = data[:, 3:]
    colors_ = np.pad(colors_, ((0, 0), (0, 1)), constant_values=(255,))
    return coordinates_, colors_


if __name__ == '__main__':
    coordinates, colors = read_data(filename=FILENAME)
    cloud = Points(inputobj=coordinates, c=colors, r=10)
    show(cloud, __doc__, axes=True,  interactive=True)
