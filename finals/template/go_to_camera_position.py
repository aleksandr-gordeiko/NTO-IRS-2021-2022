import urx

from constants import *


def main():
    robot = urx.Robot(IP)  #
    robot.set_tcp(CAMERA_TCP)
    print('CAMERA TCP SET')
    robot.set_csys(CAMERA_CSYS)
    print('CAMERA CSYS SET')
    robot.movel(ZERO_POSITION, 0.2, 0.2)
    robot.close()


if __name__ == "__main__":
    main()
