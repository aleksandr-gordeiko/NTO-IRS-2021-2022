from colorsys import rgb_to_hsv
import numpy as np
# from matplotlib import pyplot as plt


def read_data(filename: str) -> np.ndarray:
    data = np.fromfile(filename, dtype=int, count=-1, sep=' ', offset=0)
    data = np.reshape(data, (-1, 6))
    data = np.delete(data, 2, 1)
    return data


def rgb2hsv(rgb_color: np.ndarray) -> tuple:
    rgb_color = rgb_color / 255
    return rgb_to_hsv(rgb_color[0], rgb_color[1], rgb_color[2])


def is_color_red(hsv_color: tuple) -> int:
    if hsv_color[1] < 0.3:
        return 0
    if hsv_color[2] < 0.3:
        return 0
    if 1 / 3 < hsv_color[0] < 5 / 6:
        return 0
    return 1


def convert_colors(data: np.ndarray) -> np.ndarray:
    def transform_row(row: np.ndarray) -> np.ndarray:
        is_red = is_color_red(rgb2hsv(row[2:]))
        return np.concatenate((row[:2], np.atleast_1d(is_red)))

    return np.apply_along_axis(transform_row, 1, data)


def get_image_boundaries(data: np.ndarray) -> tuple:
    X = data[:, 0]
    Y = data[:, 1]
    maxX = np.max(X)
    minX = np.min(X)
    maxY = np.max(Y)
    minY = np.min(Y)
    return (minX, maxX), (minY, maxY)


def coords_bitmap2real(bitmap_x: int, bitmap_y: int, boundaries_: tuple) -> tuple:
    real_x = bitmap_x + boundaries_[0][0]
    real_y = bitmap_y + boundaries_[1][0]
    return real_x, real_y


def coords_real2bitmap(real_x: int, real_y: int, boundaries_: tuple) -> tuple:
    bitmap_x = real_x - boundaries_[0][0]
    bitmap_y = real_y - boundaries_[1][0]
    return bitmap_x, bitmap_y


def convert_data_to_bitmap(data: np.ndarray, boundaries_: tuple) -> np.ndarray:
    width = boundaries_[0][1] - boundaries_[0][0] + 1
    height = boundaries_[1][1] - boundaries_[1][0] + 1
    bitmap_ = np.zeros((height, width))

    def process_row(row: np.ndarray):
        x, y = coords_real2bitmap(row[0], row[1], boundaries_)
        bitmap_[y, x] = int(row[2] or bitmap_[y, x])

    np.apply_along_axis(process_row, 1, data)
    return bitmap_


def convolution2d(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    new_image = np.empty((1, 1))
    m, n = kernel.shape
    if m == n:
        y, x = image.shape
        y = y - m + 1
        x = x - m + 1
        new_image = np.zeros((y, x))
        for i in range(y):
            for j in range(x):
                new_image[i][j] = np.sum(image[i:i+m, j:j+m]*kernel)
    return new_image


def filter_bitmap(bitmap_: np.ndarray) -> np.ndarray:
    kernel_shape = (15, 15)

    kernel = np.ones(kernel_shape)
    kernel = kernel / np.sum(kernel)

    conv = convolution2d(bitmap_, kernel)

    return np.round(conv)


def count_objects_in_binary_bitmap(bitmap_: np.ndarray) -> int:
    def neighbor(i, j, label_):
        # left
        left = label_[i - 1, j]
        # above
        above = label_[i, j - 1]
        neighbor_array = [left, above]
        return neighbor_array

    label = np.ones(bitmap_.shape)
    new = 0
    link = []
    idx = 0
    for indexes, value in np.ndenumerate(bitmap_):
        row = indexes[0]
        column = indexes[1]
        # no object
        if bitmap_[row, column] == [0]:
            label[row, column] = 0
        # object
        else:  # check neighbor label
            current_neighbor = neighbor(row, column, label)

            # current is new label
            if current_neighbor == [0, 0]:
                new = new + 1
                label[row, column] = new

            # neighbor got label
            else:
                # only one neighbor labeling => choose the large one (the only label)
                if np.min(current_neighbor) == 0 or current_neighbor[0] == current_neighbor[1]:
                    label[row, column] = np.max(current_neighbor)

                else:
                    label[row, column] = np.min(current_neighbor)
                    if idx == 0:
                        link.append(current_neighbor)
                        idx = idx + 1
                        # print(link)
                    else:
                        check = 0
                        for k in range(idx):
                            # 交集
                            tmp = set(link[k]).intersection(set(current_neighbor))
                            if len(tmp) != 0:
                                link[k] = set(link[k]).union(current_neighbor)
                                np.array(link)
                                check = check + 1
                                # print(link)
                        if check == 0:
                            idx = idx + 1
                            np.array(link)
                            link.append(set(current_neighbor))

    # second pass
    for indexes, value in np.ndenumerate(bitmap_):
        row = indexes[0]
        column = indexes[1]
        for x in range(idx):
            if (label[row, column] in link[x]) and label[row, column] != 0:
                label[row, column] = min(link[x])
    return idx


if __name__ == '__main__':
    raw_data = read_data(filename='input.txt')
    colored_data = convert_colors(raw_data)
    boundaries = get_image_boundaries(colored_data)

    bitmap = convert_data_to_bitmap(colored_data, boundaries)
    '''plt.imshow(bitmap, interpolation='nearest')
    plt.show()'''

    filtered = filter_bitmap(bitmap)
    '''plt.imshow(filtered, interpolation='nearest')
    plt.show()'''

    print(count_objects_in_binary_bitmap(filtered))
