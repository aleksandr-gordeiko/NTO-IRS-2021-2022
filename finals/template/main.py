import socket
from operator import attrgetter

from urx.ursecmon import TimeoutException

from cv import *
from constants import *


def main():
    """while True:
        try:
            print_if_debug("Initializing hardware...")
            rob = OperateRobot(IP)
            # rob.move_to_camera_position()
            cam = OperateCamera()
            print_if_debug("Initializing hardware done")
            break
        except socket.timeout or TimeoutException:
            print_if_debug("Robot connection refused")"""

    while True:
        try:
            bricks, red_stack_height, blue_stack_height, dif_z = analyze_image(cam=None, rob=None, previous_brick=None)
            while len(bricks) != 0:
                brick = max(bricks, key=attrgetter('center_z'))
                print_if_debug("Selected brick:\n", brick)
                print_if_debug("All bricks:\n", '\n '.join(map(str, bricks)))
                rob.pick_object(
                    [brick.center_xy[0], brick.center_xy[1], brick.center_z - BLOCK_MIN_HEIGHT], brick.orientation,
                    brick.long)
                bricks, red_stack_height, blue_stack_height, dif_z = analyze_image(cam, rob, brick)
                rob.stack_object(red_stack_height, blue_stack_height, dif_z, brick.color, brick.long)
            rob.close()
            break
        except ValueError:
            print_if_debug("Restarting...")


if __name__ == "__main__":
    main()
