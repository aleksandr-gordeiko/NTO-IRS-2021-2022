import numpy as np
from math3d import Transform, Orientation, Vector

IP = "172.31.1.25"
BLOCK_MIN_HEIGHT = 0.02
UPPER_MARGIN = 0.1
TABLE_Z = -0.60
RED_STACK_CENTER = [0.075, 0.15]
BLUE_STACK_CENTER = [-0.090, 0.15]

CAMERA_CSYS = Transform(Orientation(), Vector(-831.81, 40.21, 707.37) / 1000)
CAMERA_TCP = Transform(Orientation([0.9142, 2.2072, -0.3787]), Vector(29.7, -29.7, 79.0) / 1000) \
             * Transform(Orientation(), Vector(0, 17.5, 4.2) / 1000)

GRIPPER_TCP = Transform(Orientation([1.2022, 2.9025, 0]), Vector(0, 0, 274 / 1000))
zero_position = [0, 0, 0, 0, 0, 0]

HSV_MIN = np.array([0, 82, 0])
HSV_MAX = np.array([139, 255, 136])
MIN_Y, MAX_Y = -260, 248
MIN_X, MAX_X = -451, 443
LIM_H = -800
