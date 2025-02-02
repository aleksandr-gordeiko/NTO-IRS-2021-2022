import math

import numpy as np
from math3d import Transform, Orientation, Vector


def print_if_debug(*msgs: str):
    if DEBUG:
        msgs = map(str, msgs)
        print(' '.join(msgs))


def print_if_debug2(*msgs: str):
    if DEBUG_GLEB:
        msgs = map(str, msgs)
        print(' '.join(msgs))


# JUST

DEBUG = True
DEBUG_GLEB = False
DEBUG_PIC = False
EXPERIMENTAL = True

IP = "172.31.1.25"
BLOCK_MIN_HEIGHT = 0.03
UPPER_MARGIN = 0.2
TABLE_Z = -0.68
HEIGHT_STEP = 0.005
MIN_RZ = - math.pi / 2
MAX_RZ = math.pi / 2
RED_STACK_CENTER = [0.14945405457701866, 0.29544280594861944]   # 209
BLUE_STACK_CENTER = [-0.018160502716768834, 0.2956755866205111]  # 214
PLACEMENT_ANGLE = math.pi / 4

X_PICKING_OFFSET = 0.05
Y_PICKING_OFFSET = 0.1

CAMERA_CSYS = Transform(Orientation(), Vector(-0.8880396596672806, -0.049594297988055605, 0.7440944822385092))
CAMERA_TCP = Transform(Orientation([0.9142, 2.2072, -0.3787]), Vector(29.7, -29.7, 79.0) / 1000) \
             * Transform(Orientation(), Vector(0.0104, -0.0442, -0.07553909374))

GRIPPER_TCP = Transform(Orientation([1.2022, 2.9025, 0]), Vector(0, 0, 274 / 1000))
ZERO_POSITION = [0, 0, 0, 0, 0, 0]

HSV_MIN = np.array([0, 82, 0])
HSV_MAX = np.array([139, 255, 255])
'''MIN_Y, MAX_Y = -282, 269
MIN_X, MAX_X = -490, 482'''
LIM_H = -999
MAIN_LIM_H = -999
THRESHOLD_MIN = 0.37
THRESHOLD_MAX = 1.
FILTER_COLOR = 10

ACCELERATION = .2
VELOCITY = .2

OPENING_TIME = 0.26
CLOSING_TIME = 0.52
