from typing import Optional
from OperateCamera import OperateCamera
from OperateRobot import OperateRobot
from constants import *
import open3d as o3d
import numpy as np
# import copy
# import math
import cv2


class Brick:
    def __init__(self, color: str, center_xy: list[float], center_z: float, orientation: float, long: bool):
        self.long = long
        self.orientation = orientation
        self.center_z = center_z
        self.center_xy = center_xy
        self.color = color


def analyze_image(cam: OperateCamera, rob: OperateRobot, previous_brick: Optional[Brick]) -> (list[Brick], float):
    rob.move_to_camera_position()
    frame = cam.catch_frame()
    cam.save("test.ply")
    dots = o3d.io.read_point_cloud("test.ply")
    red_points = []
    blue_points = []
    center_meters = [0, 0]
    brick_data = []
    cur, dif_z = 0, 0

    min_y, max_y = MIN_Y, MAX_Y
    min_x, max_x = MIN_X, MAX_X
    print("Start analyze")

    for i in dots.colors:

        if min_y > int(dots.points[cur][1] * 1000):
            min_y = int(dots.points[cur][1] * 1000)
        elif max_y < int(dots.points[cur][1] * 1000):
            max_y = int(dots.points[cur][1] * 1000)
        if min_x > int(dots.points[cur][0] * 1000):
            min_x = int(dots.points[cur][0] * 1000)
        elif max_x < int(dots.points[cur][0] * 1000):
            max_x = int(dots.points[cur][0] * 1000)

        if (int(i[0] * 255) - 5. > int(i[1] * 255)) and (int(i[0] * 255) - 10. > int(i[2] * 255)) \
                and (int(dots.points[cur][2] * 1000) > -630):
            red_points.append(
                [int(dots.points[cur][0] * 1000), int(dots.points[cur][1] * 1000), int(dots.points[cur][2] * 1000),
                 (int(i[2] * 255), int(i[1] * 255), int(i[0] * 255))])

        if (int(i[2] * 255) - 5. > int(i[0] * 255)) and (int(i[2] * 255) - 10. > int(i[1] * 255)) \
                and (int(dots.points[cur][2] * 1000) > -630):
            blue_points.append(
                [int(dots.points[cur][0] * 1000), int(dots.points[cur][1] * 1000), int(dots.points[cur][2] * 1000),
                 (int(i[2] * 255), int(i[1] * 255), int(i[0] * 255))])
        cur += 1

    print(min_x, min_y, max_x, max_y)
    img = np.zeros((max_y - min_y + 1, max_x - min_x + 1, 3), np.uint8)
    img_height = np.zeros((max_y - min_y + 1, max_x - min_x + 1))
    for i in red_points:
        if i[2] > LIM_H:
            img[i[1] - min_y][i[0] - min_x] = i[3]
        else:
            img[i[1] - min_y][i[0] - min_x] = (50, 50, 50)
        img_height[i[1] - min_y][i[0] - min_x] = i[2]
    for i in blue_points:
        if i[2] > LIM_H:
            img[i[1] - min_y][i[0] - min_x] = i[3]
        else:
            img[i[1] - min_y][i[0] - min_x] = (50, 50, 50)
        img_height[i[1] - min_y][i[0] - min_x] = i[2]
    img = cv2.flip(img, 1)
    img_height = cv2.flip(img_height, 1)
    # img_copy = copy.deepcopy(img)
    # cv2.imshow("test", img)
    # cv2.waitKey(7000)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_range = cv2.inRange(img_hsv, HSV_MIN, HSV_MAX)

    contours, hierarchy = cv2.findContours(img_range, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    h = 0
    contours_plus = []
    for cntr in contours:
        if int(hierarchy[0][h][3]) == -1:
            mom = cv2.moments(cntr, 1)
            if int(mom["m00"]) > 100:
                # cv2.drawContours(img, cntr, -1, (255, 0, 255))
                contours_plus.append(cntr)
                # obj = cv2.minAreaRect(cntr)
                # box = cv2.boxPoints(obj)
                # box = np.int0(box)
                # cv2.drawContours(img, [box], -1, (255, 255, 255))  # all contours
        h += 1

    for cntr in contours_plus:
        obj = cv2.minAreaRect(cntr)
        # box = cv2.boxPoints(obj)
        # box = np.int0(box)

        area = int(obj[1][0] * obj[1][1])
        if area > 100:
            # cv2.drawContours(img, [box], -1, (255, 100, 0), 1)  # cur contours
            # center = (int(obj[0][0]), int(obj[0][1]))
            color_contour = img[int(cntr[2][0][1])][int(cntr[2][0][0])]
            if color_contour[2] - 5 > color_contour[1] and color_contour[2] - 5 > color_contour[0]:
                color_obj = 'red'
            elif color_contour[0] - 5 > color_contour[1] and color_contour[0] - 5 > color_contour[2]:
                color_obj = 'blue'
            else:
                color_obj = 'none'
            center_meters[1] = (round(((obj[0][0] + min_x) / 1000), 4)) * -1            # X\Y
            center_meters[0] = (round(((obj[0][1] + min_y) / 1000), 4)) * -1            # Y\X
            center_z = img_height[int(obj[0][1])][int(obj[0][0])] / 1000                # Z
            long_edge = obj[1][0]
            if long_edge > 70:
                lb = True
            else:
                lb = False
            angle = obj[2] * (np.pi / 180.)                                             # RAD

            new_brick = Brick(color_obj, center_meters, center_z, angle, lb)
            brick_data.append(new_brick)
            # print(new_brick.color, new_brick.center_xy, new_brick.orientation)
    if previous_brick:
        old_z = previous_brick.center_z
        brick_pos = previous_brick.center_xy
        new_z = img_height[int(brick_pos[0] * 1000 - min_y), int(brick_pos[1] * 1000 - min_x)]  # swap axes
        dif_z = new_z - old_z
    else:
        dif_z = 0
    return brick_data, dif_z
