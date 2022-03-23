import urx
import math
from urx import RobotException

from coordinates import *
from time import sleep
from constants import *


class OperateRobot:
    def __init__(self, ip: str):
        self.rob = urx.Robot(ip)
        self.red_height = 0
        self.blue_height = 0
        self.rob.set_csys(CAMERA_CSYS)
        self.rob.set_tcp(GRIPPER_TCP)

    def movel(self, point: list[float]):
        if not TABLE_Z < point[2] <= 0:
            raise ValueError("Point unreachable: {}".format(point))
        print_if_debug("Moving to point: {}".format(point))
        try:
            self.rob.movel(point, 0.2, 0.2)
        except RobotException:
            raise ValueError("Robot stopped while moving to point: {}".format(point))

    def getl(self):
        return self.rob.getl()

    def close(self):
        self.rob.close()

    def open_gripper(self):
        self.rob.send_program('set_tool_digital_out(0, True)')
        self.rob.send_program('set_tool_digital_out(1, False)')
        print_if_debug("Gripper opened")
        sleep(1)

    def close_gripper(self):
        self.rob.send_program('set_tool_digital_out(0, False)')
        self.rob.send_program('set_tool_digital_out(1, True)')
        print_if_debug("Gripper closed")
        sleep(1)

    # Higher level functions ######################################

    def move_to_camera_position(self):
        self.rob.set_tcp(CAMERA_TCP)
        self.movel(ZERO_POSITION)
        self.rob.set_tcp(GRIPPER_TCP)

    def pick_object(self, obj_xyz: list[float], obj_orientation: float):
        obj_orientation += math.pi / 2
        xyz = cloud2robot(obj_xyz)
        self.open_gripper()
        self.movel([xyz[0], xyz[1], xyz[2] + UPPER_MARGIN, 0, 0, obj_orientation])
        self.movel([xyz[0], xyz[1], xyz[2], 0, 0, obj_orientation])
        self.close_gripper()
        self.movel([xyz[0], xyz[1], xyz[2] + UPPER_MARGIN, 0, 0, obj_orientation])

    def place_object(self, place_xyz: list[float], obj_orientation: float):
        xyz = cloud2robot(place_xyz)
        self.close_gripper()
        self.movel([xyz[0], xyz[1], xyz[2] + UPPER_MARGIN, 0, 0, obj_orientation])
        self.movel([xyz[0], xyz[1], xyz[2], 0, 0, obj_orientation])
        self.open_gripper()
        self.movel([xyz[0], xyz[1], xyz[2] + UPPER_MARGIN, 0, 0, obj_orientation])

    def stack_object(self, obj_height: float, stack_color: str):
        if stack_color == 'red':
            stack_top = [RED_STACK_CENTER[0], RED_STACK_CENTER[1], TABLE_Z + self.red_height]
            self.red_height += obj_height
            print_if_debug("Stacking red object")
        else:
            stack_top = [BLUE_STACK_CENTER[0], BLUE_STACK_CENTER[1], TABLE_Z + self.blue_height]
            self.blue_height += obj_height
            print_if_debug("Stacking blue object")
        self.place_object(stack_top, math.pi / 4)
