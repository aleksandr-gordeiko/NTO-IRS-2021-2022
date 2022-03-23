import urx

from constants import *


def main():
    robot = urx.Robot(IP)  #
    print('ROBOT POSITION:')
    print(robot.getl())
    robot.close()


if __name__ == "__main__":
    main()
