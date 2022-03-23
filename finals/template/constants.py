import math
import numpy as np
from math3d import Transform, Orientation, Vector


def print_if_debug(msg: str):
    if DEBUG:
        print(msg)


DEBUG = True

IP = "172.31.1.25"
BLOCK_MIN_HEIGHT = 0.02
UPPER_MARGIN = 0.1
TABLE_Z = -0.60
MIN_RZ = 0
MAX_RZ = 2 * math.pi
RED_STACK_CENTER = [0.075, 0.15]
BLUE_STACK_CENTER = [-0.090, 0.15]

CAMERA_CSYS = Transform(Orientation(), Vector(-0.8880396596672806, -0.049594297988055605, 0.7440944822385092))
CAMERA_TCP = Transform(Orientation([0.9142, 2.2072, -0.3787]), Vector(29.7, -29.7, 79.0) / 1000) \
             * Transform(Orientation(), Vector(0, 17.5, 4.2) / 1000)

GRIPPER_TCP = Transform(Orientation([1.2022, 2.9025, 0]), Vector(0, 0, 274 / 1000))
ZERO_POSITION = [0, 0, 0, 0, 0, 0]

HSV_MIN = np.array([0, 82, 0])
HSV_MAX = np.array([139, 255, 136])
MIN_Y, MAX_Y = -260, 248
MIN_X, MAX_X = -451, 443
LIM_H = -800
