from colorsys import rgb_to_hsv
import numpy as np


# Reads a Nx6 matrix from file
def read_data(filename: str) -> np.ndarray:
    data = np.fromfile(filename, dtype=int, count=-1, sep=' ', offset=0)
    data = np.reshape(data, (-1, 6))
    data = np.delete(data, 2, 1)
    return data


# converts RGB color array(1, 3) to HSV
def rgb2hsv(rgb_color: np.ndarray) -> tuple:
    rgb_color = rgb_color / 255
    return rgb_to_hsv(rgb_color[0], rgb_color[1], rgb_color[2])


# Determines if color is red based on its HSV values
def is_color_red(hsv_color: tuple) -> int:
    if hsv_color[1] < 0.3:
        return 0
    if hsv_color[2] < 0.3:
        return 0
    if 1 / 3 < hsv_color[0] < 5 / 6:
        return 0
    return 1


# Collapses 4th, 5th and 6th columns of a matrix (R, G and B) to a single 4th column of value 1 if red, 0 otherwise
def convert_colors(data: np.ndarray) -> np.ndarray:
    def transform_row(row: np.ndarray) -> np.ndarray:
        is_red = is_color_red(rgb2hsv(row[2:]))
        return np.concatenate((row[:2], np.atleast_1d(is_red)))

    return np.apply_along_axis(transform_row, 1, data)


# Calculates min and max values of X and Y coordinates in array
def get_image_boundaries(data: np.ndarray) -> tuple:
    X = data[:, 0]
    Y = data[:, 1]
    maxX = np.max(X)
    minX = np.min(X)
    maxY = np.max(Y)
    minY = np.min(Y)
    return (minX, maxX), (minY, maxY)


# Converts bitmap coordinates ((0, Xmax), (0, Ymax)) to real ones ((Xmin, Xmax), (Ymin, Ymax))
def coords_bitmap2real(bitmap_x: int, bitmap_y: int, boundaries_: tuple) -> tuple:
    real_x = bitmap_x + boundaries_[0][0]
    real_y = bitmap_y + boundaries_[1][0]
    return real_x, real_y


# Converts real coordinates ((Xmin, Xmax), (Ymin, Ymax)) to bitmap ones ((0, Xmax), (0, Ymax))
def coords_real2bitmap(real_x: int, real_y: int, boundaries_: tuple) -> tuple:
    bitmap_x = real_x - boundaries_[0][0]
    bitmap_y = real_y - boundaries_[1][0]
    return bitmap_x, bitmap_y


# Converts Nx6 array of points to a HxW matrix of points with value 0 or 1, representing its "redness"
def convert_data_to_bitmap(data: np.ndarray, boundaries_: tuple) -> np.ndarray:
    width = boundaries_[0][1] - boundaries_[0][0] + 1
    height = boundaries_[1][1] - boundaries_[1][0] + 1
    bitmap_ = np.zeros((height, width))

    def process_row(row: np.ndarray):
        x, y = coords_real2bitmap(row[0], row[1], boundaries_)
        bitmap_[y, x] = int(row[2] or bitmap_[y, x])

    np.apply_along_axis(process_row, 1, data)
    return bitmap_


# An implementation of 2d convolution numpy is lacking
def convolution2d(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    m, n = kernel.shape
    y, x = image.shape

    y = y - m + 1
    x = x - m + 1

    new_image = np.zeros((y, x))
    for i in range(y):
        for j in range(x):
            new_image[i][j] = np.sum(image[i:i + m, j:j + m] * kernel)

    return new_image


# Applies a low-pass filter to a bitmap
def filter_bitmap(bitmap_: np.ndarray) -> np.ndarray:
    kernel_shape = (15, 15)

    kernel = np.ones(kernel_shape)
    kernel = kernel / np.sum(kernel)

    conv = convolution2d(bitmap_, kernel)

    return np.round(conv).astype(int)


# Counts regions of ones on a zero-one bitmap
def count_objects_in_binary_bitmap(bitmap_: np.ndarray) -> int:
    bitmap_ = np.negative(bitmap_)
    bitmap_ = np.pad(bitmap_, ((1, 1), (1, 1)))

    max_region_number = 0
    edges = set()

    # 1st pass of CCL algorithm https://en.wikipedia.org/wiki/Connected-component_labeling
    for indexes, value in np.ndenumerate(bitmap_):
        if indexes[0] == 0 or indexes[1] == 0:
            continue

        A = bitmap_[indexes[0], indexes[1]]
        B = bitmap_[indexes[0], indexes[1] - 1]
        C = bitmap_[indexes[0] - 1, indexes[1]]

        if A == 0:
            continue
        elif B <= 0 and C <= 0:
            max_region_number += 1
            bitmap_[indexes[0], indexes[1]] = max_region_number
            edges.add((max_region_number, max_region_number))
        elif B <= 0 < C:
            bitmap_[indexes[0], indexes[1]] = C
        elif C <= 0 < B:
            bitmap_[indexes[0], indexes[1]] = B
        elif B > 0 and C > 0:
            if B != C:
                edges.add((B, C))
            bitmap_[indexes[0], indexes[1]] = B

    # Some variation of DFS, counting components of a region equivalence graph, obtained from 1st CCL pass
    graph: list[set[int]] = [set() for _ in range(max_region_number + 1)]
    for edge in edges:
        graph[edge[0]].add(edge[1])
        graph[edge[1]].add(edge[0])
    visited = [False] * (max_region_number + 1)
    components = 0
    for i in range(1, max_region_number + 1):
        if visited[i]:
            continue
        components += 1
        visited[i] = True
        queue = [i]
        while queue:
            v = queue.pop()
            for to in graph[v]:
                if not visited[to]:
                    visited[to] = True
                    queue.append(to)

    return components


if __name__ == '__main__':
    raw_data = read_data(filename='input.txt')
    colored_data = convert_colors(raw_data)
    boundaries = get_image_boundaries(colored_data)

    bitmap = convert_data_to_bitmap(colored_data, boundaries)
    filtered = filter_bitmap(bitmap)

    print(count_objects_in_binary_bitmap(filtered))
