from time import sleep
import urx
from urx import RobotException

from constants import *
from coordinates import *


class OperateRobot:
    def __init__(self, ip: str):
        self.rob = urx.Robot(ip)
        self.rob.set_csys(CAMERA_CSYS)
        self.rob.set_tcp(GRIPPER_TCP)

    def movel(self, point: list[float]):
        if point[0] < -0.5 or point[0] > 0.5:
            raise ValueError("Point unreachable (X): {}".format(point))
        if point[1] < -0.5 or point[1] > 0.5:
            raise ValueError("Point unreachable (Y): {}".format(point))
        if point[2] > 0:
            raise ValueError("Point unreachable (Z): {}".format(point))
        if point[2] < TABLE_Z:
            point[2] = TABLE_Z
        while point[5] < MIN_RZ:
            point[5] += math.pi
        while point[5] > MAX_RZ:
            point[5] -= math.pi
        print_if_debug("Moving to point: {}".format(point))
        try:
            self.rob.movel(point, ACCELERATION, VELOCITY)
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
        sleep(OPENING_TIME)

    def close_gripper(self):
        self.rob.send_program('set_tool_digital_out(0, False)')
        self.rob.send_program('set_tool_digital_out(1, True)')
        print_if_debug("Gripper closed")
        sleep(CLOSING_TIME)

    # Higher level functions ######################################

    def move_to_camera_position(self):
        self.rob.set_tcp(CAMERA_TCP)
        self.movel(ZERO_POSITION)
        self.rob.set_tcp(GRIPPER_TCP)

    def pick_object(self, obj_xyz: list[float], obj_orientation: float):
        obj_orientation = -obj_orientation
        xyz = cloud2robot(obj_xyz)
        self.open_gripper()
        self.movel([xyz[0], xyz[1], xyz[2] + UPPER_MARGIN, 0, 0, obj_orientation])
        self.movel([xyz[0], xyz[1], xyz[2], 0, 0, obj_orientation])
        self.close_gripper()
        self.movel([xyz[0], xyz[1], xyz[2] + UPPER_MARGIN, 0, 0, obj_orientation])

    def place_object(self, place_xyz: list[float], obj_orientation: float):
        xyz = place_xyz
        self.close_gripper()
        self.movel([xyz[0], xyz[1], xyz[2] + UPPER_MARGIN, 0, 0, obj_orientation])
        self.movel([xyz[0], xyz[1], xyz[2], 0, 0, obj_orientation])
        self.open_gripper()
        self.movel([xyz[0], xyz[1], xyz[2] + UPPER_MARGIN, 0, 0, obj_orientation])

    def stack_object(self, red_stack_height: float, blue_stack_height: float, brick_height: float, stack_color: str):
        if stack_color == 'red':
            stack_top = [RED_STACK_CENTER[0], RED_STACK_CENTER[1], red_stack_height + brick_height]
            print_if_debug("Stacking red object")
        else:
            stack_top = [BLUE_STACK_CENTER[0], BLUE_STACK_CENTER[1], blue_stack_height + brick_height]
            print_if_debug("Stacking blue object")
        self.place_object(stack_top, PLACEMENT_ANGLE)
