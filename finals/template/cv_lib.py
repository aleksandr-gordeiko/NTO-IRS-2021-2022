import cv2 as cv
import numpy
import numpy as np
import cv2
import open3d as o3d
from constants import *
import copy

''' OALEKSANDER '''

def fill_gaps(mat: cv.mat_wrapper, n_iterations=20) -> cv.mat_wrapper:
    res = mat.copy()
    n_channels = numpy.shape(mat)[2]
    for i in range(n_iterations):
        cv.copyTo(cv.dilate(res, cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3)), iterations=2),
                  dst=res, mask=cv.inRange(res, np.zeros(n_channels), np.ones(n_channels) * .1))
    return res

def read_from_file_raw(filename) -> np.ndarray:
    pointcloud = o3d.io.read_point_cloud(filename)
    return np.concatenate((pointcloud.points, pointcloud.colors), axis=1)


def convert_units(pointcloud) -> np.ndarray:
    pointcloud[:, 0:3] *= 1000.0  # m to mm
    pointcloud[:, 3:6] *= 255  # float color to byte color
    return pointcloud


def convert_axis(pointcloud) -> np.ndarray:
    pointcloud[:, [0, 1]] = pointcloud[:, [1, 0]]
    # pointcloud[:, 0:1] = -pointcloud[:, 0:1]
    return pointcloud


def round_to_int(pointcloud) -> np.ndarray:
    return np.rint(pointcloud).astype(np.int16)


def save_to_file(pointcloud, filename):
    np.savetxt(filename, pointcloud)


def get_image_borders(pointcloud) -> tuple:
    x = pointcloud[:, 0]
    y = pointcloud[:, 1]
    z = pointcloud[:, 2]
    return np.min(x), np.max(x), np.min(y), np.max(y), np.min(z), np.max(z)


def offset_coordinates(pointcloud, x_offset, y_offset, z_offset) -> np.ndarray:
    pointcloud[:, 0] += x_offset
    pointcloud[:, 1] += y_offset
    pointcloud[:, 2] += z_offset
    return pointcloud


def to_cv2_mat(pointcloud: np.ndarray, borders: tuple) -> cv.mat_wrapper:
    min_x, max_x, min_y, max_y, min_z, max_z = borders
    x_height, y_height = max_x - min_x + 1, max_y - min_y + 1
    rgbmat = np.zeros((x_height, y_height, 3), np.uint8)
    zmat = np.zeros((x_height, y_height, 1), np.uint8)

    pointcloud[:, [3, 5]] = pointcloud[:, [5, 3]]

    def process_row(row: np.ndarray):
        rgbmat[int(row[0]), int(row[1])] = row[3:6]
        zmat[int(row[0]), int(row[1])] = min(int(row[2]), 255)

    def process_cloud(cloud: np.ndarray):
        np.apply_along_axis(process_row, 1, cloud)

    process_cloud(pointcloud)

    return rgbmat, zmat


def flip_mat(mat: cv.mat_wrapper):
    mat = cv.flip(mat, 0)
    return mat


def convert_ply2(filename):
    pcloud = read_from_file_raw(filename)
    pcloud = convert_axis(pcloud)
    pcloud = convert_units(pcloud)
    pcloud = round_to_int(pcloud)
    borders = get_image_borders(pcloud)
    pcloud = offset_coordinates(pcloud, -borders[0], -borders[2], -borders[4])
    rgb, height = to_cv2_mat(pcloud, borders)
    # rgb = fill_gaps(rgb)
    height = fill_gaps(height)
    height = height.astype(np.int16)
    height[:, :, 0] += borders[4]
    return flip_mat(rgb), flip_mat(height), borders

''' GLEB '''

def find_min_max(min_x, min_y, max_x, max_y, i, cur):
    if min_y > int(i[cur][1] * 1000):
        min_y = int(i[cur][1] * 1000)
    elif max_y < int(i[cur][1] * 1000):
        max_y = int(i[cur][1] * 1000)
    if min_x > int(i[cur][0] * 1000):
        min_x = int(i[cur][0] * 1000)
    elif max_x < int(i[cur][0] * 1000):
        max_x = int(i[cur][0] * 1000)
    print_if_debug2(min_x, min_y, max_x, max_y)
    return min_x, min_y, max_x, max_y


def check_color(main_color, color1, color2):
    if ((main_color * 255) - FILTER_COLOR > color1 * 255) and ((main_color * 255) - FILTER_COLOR > color2 * 255):
        return True
    return False


def fix_array(y, x, min_x, min_y, max_x, max_y):
    if x >= max_x - min_x:
        x = max_x - min_x - 1
    if y >= max_y - min_y:
        y = max_y - min_y - 1
    return int(y), int(x)


def convert_ply(src, min_x, min_y, max_x, max_y):
    cur = 0
    img = np.zeros((max_y - min_y + 1, max_x - min_x + 1, 3), np.uint8)
    img_height = np.zeros((max_y - min_y + 1, max_x - min_x + 1))

    dots = o3d.io.read_point_cloud(src)

    for i in dots.colors:
        p = dots.points[cur]
        y, x = fix_array(p[1] * 1000 - min_y, p[0] * 1000 - min_x, min_x, min_y, max_x, max_y)
        img[y][x] = (int(i[2] * 255), int(i[1] * 255), int(i[0] * 255))
        img_height[y][x] = p[2] * 1000
        cur += 1
    img = cv2.flip(img, 0)
    img_height = cv2.flip(img_height, 0)
    return img, img_height


def find_contours(src):
    contours, hierarchy = cv2.findContours(src, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    h = 0
    contours_plus = []
    for cntr in contours:
        if int(hierarchy[0][h][3]) == -1:
            moments = cv2.moments(cntr, 1)
            if int(moments["m00"]) > 100:
                contours_plus.append(cntr)
        h += 1

    return copy.deepcopy(contours_plus)


def slip_obj(src, bin_src):
    img_test = cv.Canny(src, 0, 255, None, 3, 0)
    dst = cv.addWeighted(bin_src, 1, img_test, -1, 0.0)
    dist = cv.distanceTransform(dst, cv.DIST_L2, 3)
    cv.normalize(dist, dist, 0, 1.0, cv.NORM_MINMAX)
    dist = dist.astype("float32")
    dst = dst.astype("float32")
    final = cv.addWeighted(dst, 0.001, dist, 1, 0.0)
    # cv.imshow("final", final)
    # cv.imshow("dst", dst)
    # cv.imshow("dist", dist)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    _, final = cv.threshold(final, 0.37, 255, cv.THRESH_BINARY)
    return copy.deepcopy(final.astype("uint8"))


def create_frame(src, borders, xy=(450, 100), xy2=(900, 470)):
    min_x, max_x, min_y, max_y, min_z, max_z = borders
    x_height, y_height = max_x - min_x + 1, max_y - min_y + 1
    mask = np.zeros((x_height, y_height), np.uint8)
    cv2.rectangle(mask, xy, xy2, 255, -1)
    final = cv2.bitwise_and(src, src, mask=mask)
    # cv2.imshow("jdd", final)
    # cv2.waitKey(0)
    # cv2.rectangle(src, (x2, 0), (1000, 1000), (0, 0, 0), -1)
    return copy.deepcopy(final)


def check_stack(src, mat_h, borders):

    max_red_z = -1.
    max_blue_z = -1.

    src = create_frame(src, borders, (70, 70), (450, 470))
    hsv_src = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    bin_src = cv2.inRange(hsv_src, HSV_MIN, HSV_MAX)
    cntrs = find_contours(bin_src)
    for cntr in cntrs:
        obj = cv2.minAreaRect(cntr)
        box = cv2.boxPoints(obj)
        box = np.int0(box)
        cv2.drawContours(src, [box], -1, (255, 255, 255))  # all contours

        color_contour = src[round(obj[0][1])][round(obj[0][0])]
        if check_color(color_contour[2], color_contour[1], color_contour[0]):
            max_red_z = max(max_red_z, mat_h[round(obj[0][1])][round(obj[0][0])] / 1000)
            mem_red = (round(obj[0][0]), round(obj[0][1]))
        elif check_color(color_contour[0], color_contour[1], color_contour[2]):
            max_blue_z = max(max_red_z, mat_h[round(obj[0][1])][round(obj[0][0])] / 1000)
            mem_blue = (round(obj[0][0]), round(obj[0][1]))
    '''if max_blue_z != TABLE_Z:
        cv2.circle(src, mem_blue, 2, (255, 255, 255), -1)
    if max_red_z != TABLE_Z:
        cv2.circle(src, mem_red, 2, (255, 0, 0), -1)
    print(len(cntrs))'''
    # print(max_red_z, max_blue_z)
    # cv2.imshow("src", src)
    # cv2.waitKey(0)
    return max_red_z, max_blue_z
