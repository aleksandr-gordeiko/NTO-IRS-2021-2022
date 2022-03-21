import urx
import math
from coordinates import *
# pip install git+https://github.com/jkur/python-urx

UPPER_MARGIN = 0.1


class OperateRobot:

    def __init__(self,
                 ip: str,
                 camera_position: list[float],
                 zone_red_position: list[list[float]],
                 zone_blue_position: list[list[float]]):
        self.rob = urx.Robot(ip)
        self.camera_position = camera_position
        self.red_height = 0
        self.blue_height = 0
        self.red_stack_center = [(zone_red_position[1][0] + zone_red_position[0][0]) / 2,
                                 (zone_red_position[1][1] + zone_red_position[0][1]) / 2]
        self.blue_stack_center = [(zone_blue_position[1][0] + zone_blue_position[0][0]) / 2,
                                 (zone_blue_position[1][1] + zone_blue_position[0][1]) / 2]

    def movel(self, point: list[float]):
        self.rob.movel(point, 0.2, 0.2)

    def getl(self):
        return self.rob.getl()

    def close(self):
        self.rob.close()

    def open_gripper(self):
        self.rob.send_program('set_tool_digital_out(0, True)')
        self.rob.send_program('set_tool_digital_out(1, False)')

    def close_gripper(self):
        self.rob.send_program('set_tool_digital_out(0, False)')
        self.rob.send_program('set_tool_digital_out(1, True)')

    # Higher level functions ######################################

    def move_to_camera_position(self):
        self.movel(self.camera_position)

    def pick_object(self, obj_xyz: list[float], obj_orientation: float, long=False):
        if long:
            obj_orientation += math.pi / 2
        xyz = cloud2robot(obj_xyz)
        self.open_gripper()
        self.movel([xyz[0], xyz[1], xyz[2] + UPPER_MARGIN, 0, 0, obj_orientation])
        self.movel([xyz[0], xyz[1], xyz[2], 0, 0, obj_orientation])
        self.close_gripper()
        self.movel([xyz[0], xyz[1], xyz[2] + UPPER_MARGIN, 0, 0, obj_orientation])

    def place_object(self, place_xyz: list[float], obj_orientation: float, long=False):
        if long:
            obj_orientation -= math.pi / 2
        xyz = cloud2robot(place_xyz)
        self.close_gripper()
        self.movel([xyz[0], xyz[1], xyz[2] + UPPER_MARGIN, 0, 0, obj_orientation])
        self.movel([xyz[0], xyz[1], xyz[2], 0, 0, obj_orientation])
        self.open_gripper()
        self.movel([xyz[0], xyz[1], xyz[2] + UPPER_MARGIN, 0, 0, obj_orientation])

    def stack_object(self, obj_orientation: float, obj_height: float, stack_color: str, long=False):
        if stack_color == 'red':
            stack_top = [self.red_stack_center[0], self.red_stack_center[1], self.red_height]
            self.red_height += obj_height
        else:
            stack_top = [self.blue_stack_center[0], self.blue_stack_center[1], self.blue_height]
            self.blue_height += obj_height
        self.place_object(stack_top, obj_orientation, long)

