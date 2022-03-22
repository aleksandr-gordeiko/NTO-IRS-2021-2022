from operator import attrgetter
from cv import *
from constants import *


def main():
    rob = OperateRobot(IP)
    cam = OperateCamera()

    bricks, previous_brick_height = analyze_image(cam, rob, None)
    while len(bricks) != 0:
        brick = max(bricks, key=attrgetter('center_z'))
        rob.pick_object([brick.center_xy[0], brick.center_xy[1], brick.center_z - BLOCK_MIN_HEIGHT],
                        brick.orientation,
                        brick.long)
        bricks, previous_brick_height = analyze_image(cam, rob, brick)
        rob.stack_object(brick.orientation, previous_brick_height, brick.color, brick.long)

    rob.close()


if __name__ == "__main__":
    main()
