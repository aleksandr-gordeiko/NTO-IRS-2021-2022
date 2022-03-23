import urx

from constants import *


def main():
    robot = urx.Robot(IP)  #
    robot.set_csys(CAMERA_CSYS)
    robot.set_tcp(GRIPPER_TCP)
    print('GRIPPER TCP SET')
    robot.close()


if __name__ == "__main__":
    main()
