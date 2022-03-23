import cv2 as cv
import numpy
import numpy as np
import cv2
import open3d as o3d
from constants import *
import copy


def fill_gaps(mat: cv.mat_wrapper, n_iterations=20) -> cv.mat_wrapper:
    res = mat.copy()
    n_channels = numpy.shape(mat)[2]
    for i in range(n_iterations):
        cv.copyTo(cv.dilate(res, cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3)), iterations=2),
                  dst=res, mask=cv.inRange(res, np.zeros(n_channels), np.ones(n_channels) * .1))
    return res


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

        if (check_color(i[0], i[1], i[2])) and (int(dots.points[cur][2] * 1000) > MAIN_LIM_H):
            img[y][x] = (int(i[2] * 255), int(i[1] * 255), int(i[0] * 255))
        elif (check_color(i[2], i[0], i[1])) and (int(dots.points[cur][2] * 1000) > MAIN_LIM_H):
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


def create_frame(src, x1=450, x2=850):
    cv2.rectangle(src, (0, 0), (x1, 1000), (0, 0, 0), -1)
    cv2.rectangle(src, (x2, 0), (1000, 1000), (0, 0, 0), -1)
