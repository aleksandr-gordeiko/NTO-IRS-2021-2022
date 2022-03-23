import copy
from typing import Optional

# import math
import cv2
import numpy as np

from OperateCamera import OperateCamera
from OperateRobot import OperateRobot
from constants import *
from cv_lib import *


class Brick:
    def __init__(self, color: str, center_xy: list[float], center_z: float, orientation: float, long: bool):
        self.long = long
        self.orientation = orientation
        self.center_z = center_z
        self.center_xy = center_xy
        self.color = color

    def __repr__(self):
        return "Center: {};{};{} Orientation: {} Color: {}" \
            .format(self.center_xy[0], self.center_xy[1], self.center_z, self.orientation, self.color)

    def __str__(self):
        return self.__repr__()


def analyze_image(cam: OperateCamera, rob: OperateRobot, previous_brick: Optional[Brick]) -> (list[Brick], float):
    '''rob.move_to_camera_position()
    frame = cam.catch_frame()
    cam.save("test.ply")'''
    center_meters = [0, 0]
    brick_data = []
    dif_z = 0

    print_if_debug2("Start analyze")
    #img, img_height, borders = convert_ply2("PLY\\data_new_set2.ply")
    min_x, max_x, min_y, max_y = MIN_X, MAX_X, MIN_Y, MAX_Y
    borders = min_x, max_x, min_y, max_y
    img, img_height = convert_ply("PLY\\data_new_set2.ply", min_x, min_y, max_x, max_y)

    img = cv2.flip(img, 0)
    img_height = cv2.flip(img_height, 0)

    img = fill_gaps(img)
    create_frame(img, borders)
    # img_copy = copy.deepcopy(img)

    if DEBUG_PIC:
        cv2.imshow("MAIN_IMG", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_range = cv2.inRange(img_hsv, HSV_MIN, HSV_MAX)

    if DEBUG_PIC:
        cv2.imshow("FILT_IMG", img_range)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # _ EXPERIMENTAL _
    if EXPERIMENTAL:
        img_range = slip_obj(img, img_range)
        if DEBUG_PIC:
            cv2.imshow("frame_cut", img_range)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    # _________________

    contours_plus = find_contours(img_range)

    for cntr in contours_plus:
        obj = cv2.minAreaRect(cntr)
        # box = cv2.boxPoints(obj)
        # box = np.int0(box)

        print_if_debug2("OBJ:", str(obj))

        area = int(obj[1][0] * obj[1][1])
        if area > 100:
            # cv2.drawContours(img, [box], -1, (255, 100, 0), 1)  # cur contours
            # center = (int(obj[0][0]), int(obj[0][1]))
            color_contour = img[int(cntr[2][0][1])][int(cntr[2][0][0])]
            if check_color(color_contour[2], color_contour[1], color_contour[0]):
                color_obj = 'red'
            elif check_color(color_contour[0], color_contour[1], color_contour[2]):
                color_obj = 'blue'
            else:
                color_obj = 'none'

            center_meters[1] = (round(((obj[0][0] + min_x) / 1000), 4)) * -1  # X\Y
            center_meters[0] = (round(((obj[0][1] + min_y) / 1000), 4)) * -1  # Y\X
            center_z = img_height[round(obj[0][1])][round(obj[0][0])] / 1000  # Z

            p = 2
            while center_z == 0:
                center_z = img_height[int(cntr[p][0][1])][int(cntr[p][0][0])]
                p += 1

            long_edge = obj[1][0]
            if long_edge > 70:
                lb = True
            else:
                lb = False

            angle = obj[2] * (np.pi / 180.)  # RAD

            new_brick = Brick(color_obj, copy.deepcopy(center_meters), center_z, angle, lb)
            brick_data.append(new_brick)

            print_if_debug2("Color", str(new_brick.color), "XYZ", str(new_brick.center_xy), str(new_brick.center_z))
            print_if_debug2("Angle", str(new_brick.orientation))

            # if DEBUG_PIC:
            # cv2.circle(img_range, (int(obj[0][0]), int(obj[0][1])), 2, (0, 255, 0))
            # cv2.imshow("test", img_range)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

    if previous_brick:
        old_z = previous_brick.center_z
        brick_pos = previous_brick.center_xy
        new_z = (img_height[int(brick_pos[0] * -1000 - min_y), int(brick_pos[1] * -1000 - min_x)] / 1000)  # swap axes
        if new_z == 0:
            new_z = TABLE_Z
        dif_z = new_z - old_z
        print(new_z, old_z)
    else:
        dif_z = 0

    return brick_data, dif_z
