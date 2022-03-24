# import copy
# import math
# import cv2
# import numpy as np
from typing import Optional

from OperateCamera import OperateCamera
from OperateRobot import OperateRobot
# from constants import *
from cv_lib import *


class Brick:
    def __init__(self, color: str, center_xy: list[float], center_z: float, orientation: float, long: bool):
        self.long = long
        self.orientation = orientation
        self.center_z = center_z
        self.center_xy = center_xy
        self.color = color

    def __repr__(self):
        return "Center: {};{};{} Orientation: {} Color: {} Long: {}" \
            .format(self.center_xy[0], self.center_xy[1], self.center_z, self.orientation, self.color, self.long)

    def __str__(self):
        return self.__repr__()


def analyze_image(
    cam: OperateCamera, rob: OperateRobot, previous_brick: Optional[Brick]) -> (list[Brick], float, float):
    """rob.move_to_camera_position()
    cam.catch_frame()
    cam.save("test.ply")"""
    center_meters = [0, 0]
    brick_data = []

    print_if_debug2("Start analyze")
    img, img_height, borders = convert_ply2("PLY/data_new_set_blocks_2.ply")
    min_x, max_x, min_y, max_y, min_z, max_z = borders

    # img = cv2.flip(img, 0)
    # img_height = cv2.flip(img_height, 0)

    img = fill_gaps(img)
    red_zone_h, blue_zone_h = check_stack(img, img_height, borders)
    img = create_frame(img, borders)
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
        box = cv2.boxPoints(obj)
        box = np.int0(box)

        print_if_debug2("OBJ:", str(obj))

        area = int(obj[1][0] * obj[1][1])
        if area > 100:
            cv2.drawContours(img, [box], -1, (255, 100, 0), 1)  # draw contours
            # center = (int(obj[0][0]), int(obj[0][1]))
            color_contour = img[int(cntr[2][0][1])][int(cntr[2][0][0])]
            if check_color(color_contour[2], color_contour[1], color_contour[0]):
                color_obj = 'red'
            elif check_color(color_contour[0], color_contour[1], color_contour[2]):
                color_obj = 'blue'
            else:
                color_obj = 'none'

            center_meters[1] = (round(((obj[0][0] + min_y) / 1000), 4)) * -1  # X\Y
            center_meters[0] = (round(((obj[0][1] + min_x) / 1000), 4)) * -1  # Y\X
            center_z = img_height[round(obj[0][1])][round(obj[0][0])] / 1000  # Z
            angle = obj[2] * (np.pi / 180.)  # RAD

            edge1 = np.int0((box[1][0] - box[0][0], box[1][1] - box[0][1]))
            edge2 = np.int0((box[2][0] - box[1][0], box[2][1] - box[1][1]))
            usedEdge = edge1
            if cv.norm(edge2) > cv.norm(edge1):
                usedEdge = edge2
            reference = (1, 0)  # горизонтальный вектор, задающий горизонт
            angle = 180.0 / math.pi * math.acos(
                (reference[0] * usedEdge[0] + reference[1] * usedEdge[1]) / (cv.norm(reference) * cv.norm(usedEdge)))
            angle = angle * (np.pi / 180.)  # RAD

            p = 2
            while center_z == 0:
                center_z = img_height[int(cntr[p][0][1])][int(cntr[p][0][0])]
                p += 1

            long_edge = cv2.norm(usedEdge)
            if long_edge > 70:
                lb = True
            else:
                lb = False

            new_brick = Brick(color_obj, copy.deepcopy(center_meters), center_z, angle, lb)
            brick_data.append(new_brick)

            print_if_debug2("Color", str(new_brick.color), "XYZ", str(new_brick.center_xy), str(new_brick.center_z))
            print_if_debug2("Angle", str(obj[2]))

            '''if DEBUG_PIC:
                print((int((-0.204-min_y)*1000), int((0.09-min_x)*1000)))
                cv2.circle(img, (int((-0.204*1000-min_y)), int((0.09*1000-min_x))), 50, (0, 0, 255), -1)
                cv2.circle(img, (int((-0.204*1000-min_y)), int((-0.07*1000-min_x))), 50, (255, 0, 255), -1)
                cv2.imshow("test", img)
                print(img[int((0.09*1000-min_x))][int((-0.204*1000-min_y))])
                cv2.waitKey(0)
                cv2.destroyAllWindows()'''

    if DEBUG_PIC:
        cv2.imshow("test", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if previous_brick:
        old_z = previous_brick.center_z
        brick_pos = previous_brick.center_xy
        new_z = (img_height[int(brick_pos[0] * -1000 - min_x), int(brick_pos[1] * -1000 - min_y)] / 1000)  # swap axes
        if new_z == 0:
            new_z = TABLE_Z
        dif_z = old_z - new_z
        print_if_debug2("new, old, dif z", str(new_z), str(old_z), str(dif_z))
    else:
        dif_z = 0

    '''red_zone_h = img_height[int((0.09*1000-min_x))][int((-0.204*1000-min_y))] / 1000
    blue_zone_h = img_height[int((-0.07*1000-min_x))][int((-0.204*1000-min_y))] / 1000'''
    return brick_data, red_zone_h, blue_zone_h, dif_z
