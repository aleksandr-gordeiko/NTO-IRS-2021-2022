from typing import Optional
from OperateCamera import OperateCamera
from OperateRobot import OperateRobot


class Brick:
    def __init__(self, color: str, center_xy: list[float], center_z: float, orientation: float, long: bool):
        self.long = long
        self.orientation = orientation
        self.center_z = center_z
        self.center_xy = center_xy
        self.color = color


def analyze_image(cam: OperateCamera, rob: OperateRobot, previous_brick: Optional[Brick]) -> (list[Brick], float):
    rob.move_to_camera_position()
    cam.catch_frame()
    cam.save("test.ply")
    pcd = cam.open("test.ply")
    # Image processing
