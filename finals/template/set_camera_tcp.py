import urx

from constants import *


def main():
    robot = urx.Robot(IP)  #
    robot.set_tcp(CAMERA_TCP)
    print('CAMERA TCP SET')
    robot.close()


if __name__ == "__main__":
    main()
