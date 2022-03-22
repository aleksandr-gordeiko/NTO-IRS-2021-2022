import time

import urx

from math3d import Transform, Orientation, Vector
import time
from math import pi


def main():
    # Connection to the robot
    robot = urx.Robot("172.31.1.25")  # 192.168.56.101

    # Initialization
    cameratransform_base = Transform(Orientation(), Vector(-831.81 / 1000, 40.21 / 1000, 707.37 / 1000))

    camera_tcp = [-29.7 / 1000, 29.7 / 1000, 79.0 / 1000, 0.9142, 2.2072, -0.3787]
    gripper_tcp = [0, 0, 274 / 1000, 1.202, 2.902, 0]
    zeroposition = [0, 0, 0, 0, 0, 0]
    robot.set_csys(cameratransform_base)

    # Taking a photo
    robot.set_tcp(camera_tcp)
    robot.movel(zeroposition, 0.2, 0.2)



    robot.set_tcp(gripper_tcp)
    robot.movel([0/1000, 0/1000, -580/1000, 0, 0, 0], 0.2, 0.2)

    robot.close()


    pass


if __name__ == "__main__":
    main()
