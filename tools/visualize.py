import numpy as np
from vedo import *


def read_data(filename: str) -> tuple[np.ndarray, np.ndarray]:
    data = np.fromfile(filename, dtype=int, count=-1, sep=' ', offset=0)
    data = np.reshape(data, (-1, 6))
    coordinates_ = data[:, :3]
    colors_ = data[:, 3:]
    colors_ = np.pad(colors_, ((0, 0), (0, 1)), constant_values=(255,))
    return coordinates_, colors_


if __name__ == '__main__':
    coordinates, colors = read_data(filename='../part_4/task_1/samples/2')
    cloud = Points(inputobj=coordinates, c=colors, r=10)
    show(cloud, __doc__, axes=True,  interactive=True)
