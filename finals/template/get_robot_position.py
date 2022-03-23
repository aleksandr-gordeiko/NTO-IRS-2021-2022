import urx

from constants import *


def main():
    robot = urx.Robot("192.168.56.101")  #
    robot.set_csys(CAMERA_CSYS)
    robot.set_tcp(GRIPPER_TCP)
    #robot.set_tcp(CAMERA_TCP)
    print('ROBOT POSITION:')
    print(robot.getl())
    robot.close()


if __name__ == "__main__":
    main()
