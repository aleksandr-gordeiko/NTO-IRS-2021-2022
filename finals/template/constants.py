from math3d import Transform, Orientation, Vector

IP = "172.31.1.25"
BLOCK_MIN_HEIGHT = 0.02
UPPER_MARGIN = 0.1
TABLE_Z = -0.60
RED_STACK_CENTER = [0.075, 0.15]
BLUE_STACK_CENTER = [-0.090, 0.15]

cameratransform_base = Transform(Orientation(), Vector(-831.81 / 1000, 40.21 / 1000, 707.37 / 1000))
camera_tcp = [-29.7 / 1000, 29.7 / 1000, 79.0 / 1000, 0.9142, 2.2072, -0.3787]
gripper_tcp = [0, 0, 274 / 1000, 1.202, 2.902, 0]
zero_position = [0, 0, 0, 0, 0, 0]