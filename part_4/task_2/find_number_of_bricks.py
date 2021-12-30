import math
import random
from colorsys import rgb_to_hsv
import numpy as np

import matplotlib.pyplot as plt


# MAGIC VALUES
MIN_SATURATION = .69
MIN_NUMBER_OF_POINTS_IN_BODY = 500
MIN_VALUE_TO_BECOME_1 = .6
FILTER_SIZE = 8
RADIUS_ADDITIVE = 1
FILENAME = 'samples/2'


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


# Determines if color is red, blue or neither, based on its HSV values
# 1 = red; -1 = blue; 0 = neither
def get_color(hsv_color: tuple) -> int:
    if hsv_color[1] < MIN_SATURATION:
        return 0
    if 1 / 3 < hsv_color[0] < 5 / 6:
        return -1
    return 1


# Collapses 4th, 5th and 6th columns of a matrix (R, G and B) to a single 4th column of value 1 if red, 0 otherwise
def convert_colors(data: np.ndarray) -> np.ndarray:
    data_filtered = []
    for row in data:
        color = get_color(rgb2hsv(row[2:]))
        if color != 0:
            data_filtered.append(np.append(row[:2], color))

    return np.array(data_filtered)


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


# Converts Nx6 array of points to a HxW matrix of points with value 0, -1 or 1, representing its color
def points_to_bitmap(data: np.ndarray, boundaries_: tuple) -> np.ndarray:
    width = boundaries_[0][1] - boundaries_[0][0] + 1
    height = boundaries_[1][1] - boundaries_[1][0] + 1
    bitmap_ = np.zeros((height, width))

    def process_row(row: np.ndarray):
        x, y = coords_real2bitmap(row[0], row[1], boundaries_)
        bitmap_[y, x] = row[2]

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


# Applies a low-pass filter to a 0;1;-1 bitmap
def filter_bitmap(bitmap_: np.ndarray, kernel_size: int) -> np.ndarray:
    kernel_shape = (kernel_size, kernel_size)

    kernel = np.ones(kernel_shape)
    kernel = kernel / np.sum(kernel)

    bitmap_red = np.floor_divide(bitmap_ + 1, 2)
    bitmap_blue = np.floor_divide(bitmap_ - 1, -2)

    conv_red = convolution2d(bitmap_red, kernel)
    conv_blue = convolution2d(bitmap_blue, kernel)

    conv = np.sign(np.round(conv_red / (MIN_VALUE_TO_BECOME_1 / 0.5)) +
                   np.round(conv_blue / (MIN_VALUE_TO_BECOME_1 / 0.5)))

    return conv.astype(int)


def bitmap_to_points(bitmap_: np.ndarray) -> np.ndarray:
    points = []
    for index, value in np.ndenumerate(bitmap_):
        if value != 0:
            points.append([index[1], index[0], value])

    return np.array(points)


# Labels regions of ones on a zero-one bitmap
def label_components_of_binary_bitmap(bitmap_: np.ndarray) -> (np.ndarray, int):
    bitmap_ = np.negative(bitmap_).astype('int8')
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

    # Some variation of DFS, simplifying region equivalence graph, obtained from 1st CCL pass
    graph: list[set[int]] = [set() for _ in range(max_region_number + 1)]
    for edge in edges:
        graph[edge[0]].add(edge[1])
        graph[edge[1]].add(edge[0])
    visited = [False] * (max_region_number + 1)
    equivalences = {}
    components = 0
    for i in range(1, max_region_number + 1):
        if visited[i]:
            continue
        components += 1
        visited[i] = True
        queue = [i]
        while queue:
            v = queue.pop()
            equivalences[v] = i
            for to in graph[v]:
                if not visited[to]:
                    visited[to] = True
                    queue.append(to)

    # 2nd pass of CCL algorithm
    points_in_region = {}
    for indexes, value in np.ndenumerate(bitmap_):
        if value != 0:
            bitmap_[indexes[0], indexes[1]] = equivalences[value]
            try:
                points_in_region[equivalences[value]] += 1
            except KeyError:
                points_in_region[equivalences[value]] = 1

    # Select regions small enough to delete
    regions_to_delete = []
    for key in points_in_region:
        if points_in_region[key] < MIN_NUMBER_OF_POINTS_IN_BODY:
            regions_to_delete.append(key)

    components -= len(regions_to_delete)

    # Delete selected regions
    for index, value in np.ndenumerate(bitmap_):
        if value in regions_to_delete:
            bitmap_[index[0], index[1]] = 0

    return bitmap_, components


def make_circle(points):
    # Convert to float and randomize order
    shuffled = [(float(x), float(y)) for (x, y) in points]
    random.shuffle(shuffled)

    # Progressively add points to circle or recompute circle
    c = None
    for (i, p) in enumerate(shuffled):
        if c is None or not is_in_circle(c, p):
            c = _make_circle_one_point(shuffled[: i + 1], p)
    return c


# One boundary point known
def _make_circle_one_point(points, p):
    c = (p[0], p[1], 0.0)
    for (i, q) in enumerate(points):
        if not is_in_circle(c, q):
            if c[2] == 0.0:
                c = make_diameter(p, q)
            else:
                c = _make_circle_two_points(points[: i + 1], p, q)
    return c


# Two boundary points known
def _make_circle_two_points(points, p, q):
    circ = make_diameter(p, q)
    left = None
    right = None
    px, py = p
    qx, qy = q

    # For each point not in the two-point circle
    for r in points:
        if is_in_circle(circ, r):
            continue

        # Form a circumcircle and classify it on left or right side
        cross = _cross_product(px, py, qx, qy, r[0], r[1])
        c = make_circumcircle(p, q, r)
        if c is None:
            continue
        elif cross > 0.0 and (
                left is None or _cross_product(px, py, qx, qy, c[0], c[1]) > _cross_product(px, py, qx, qy, left[0],
                                                                                            left[1])):
            left = c
        elif cross < 0.0 and (
                right is None or _cross_product(px, py, qx, qy, c[0], c[1]) < _cross_product(px, py, qx, qy, right[0],
                                                                                             right[1])):
            right = c

    # Select which circle to return
    if left is None and right is None:
        return circ
    elif left is None:
        return right
    elif right is None:
        return left
    else:
        return left if (left[2] <= right[2]) else right


def make_diameter(a, b):
    cx = (a[0] + b[0]) / 2
    cy = (a[1] + b[1]) / 2
    r0 = math.hypot(cx - a[0], cy - a[1])
    r1 = math.hypot(cx - b[0], cy - b[1])
    return cx, cy, max(r0, r1)


def make_circumcircle(a, b, c):
    # Mathematical algorithm from Wikipedia: Circumscribed circle
    ox = (min(a[0], b[0], c[0]) + max(a[0], b[0], c[0])) / 2
    oy = (min(a[1], b[1], c[1]) + max(a[1], b[1], c[1])) / 2
    ax = a[0] - ox
    ay = a[1] - oy
    bx = b[0] - ox
    by = b[1] - oy
    cx = c[0] - ox
    cy = c[1] - oy
    d = (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by)) * 2.0
    if d == 0.0:
        return None
    x = ox + ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    y = oy + ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    ra = math.hypot(x - a[0], y - a[1])
    rb = math.hypot(x - b[0], y - b[1])
    rc = math.hypot(x - c[0], y - c[1])
    return x, y, max(ra, rb, rc)


_MULTIPLICATIVE_EPSILON = 1 + 1e-14


def is_in_circle(c, p):
    return c is not None and math.hypot(p[0] - c[0], p[1] - c[1]) <= c[2] * _MULTIPLICATIVE_EPSILON


# Returns twice the signed area of the triangle defined by (x0, y0), (x1, y1), (x2, y2).
def _cross_product(x0, y0, x1, y1, x2, y2):
    return (x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0)


def convert_labeled_bitmap_to_array_of_points_arrays(bitmap_: np.ndarray, number_of_clusters: int) -> list[list]:
    cluster = [[] for _ in range(number_of_clusters)]
    clusters_new_numbers = []
    for index, value in np.ndenumerate(bitmap_):
        if value != 0:
            if value not in clusters_new_numbers:
                clusters_new_numbers.append(value)
            cluster[clusters_new_numbers.index(value)].append(index)

    return cluster


if __name__ == '__main__':
    raw_data = read_data(filename=FILENAME)
    colored_data = convert_colors(raw_data)
    boundaries = get_image_boundaries(colored_data)

    bitmap = points_to_bitmap(colored_data, boundaries)
    filtered = filter_bitmap(bitmap, FILTER_SIZE)

    filtered_points = bitmap_to_points(filtered)
    filtered_points = np.abs(filtered_points)  # Making the bitmap of 0;1 instead of 0;1;-1

    boundaries = get_image_boundaries(filtered_points)
    binary_filtered_bitmap = points_to_bitmap(filtered_points, boundaries)
    labeled_bitmap, number_of_bodies = label_components_of_binary_bitmap(binary_filtered_bitmap)

    plt.imshow(labeled_bitmap)
    plt.show()

    if number_of_bodies < 2:
        result = number_of_bodies
    else:
        bodies = convert_labeled_bitmap_to_array_of_points_arrays(labeled_bitmap, number_of_bodies)
        circles = []
        for body in bodies:
            circles.append(make_circle(body))

        non_colliding_bodies = 0
        for i in range(number_of_bodies):
            collisions = 0
            for j in range(number_of_bodies):
                if i != j:
                    body = np.array(bodies[i])
                    circle = circles[j]
                    body_relative = body - circle[:2]
                    distances_to_center = np.sqrt(np.square(body_relative[:, 0]) + np.square(body_relative[:, 1]))
                    min_distance = np.min(distances_to_center)
                    if min_distance < (circle[2] + RADIUS_ADDITIVE):
                        collisions += 1
            if collisions == 0:
                non_colliding_bodies += 1

        result = non_colliding_bodies

    print(result)
