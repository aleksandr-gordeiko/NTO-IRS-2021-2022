import urx
# pip install git+https://github.com/jkur/python-urx


class OperateRobot:

    def __init__(self, ip):
        self.rob = urx.Robot(ip)

    def movel(self, point: dict):
        self.rob.movel((point["x"], point["y"], point["z"], point["rx"], point["ry"], point["rz"]), 0.2, 0.2)

    def getl(self):
        return self.rob.getl()

    def getj(self):
        return self.rob.getj()

    def close(self):
        self.rob.close()

    def open_gripper(self):
        self.rob.send_program('set_tool_digital_out(0, True)')
        self.rob.send_program('set_tool_digital_out(1, False)')

    def close_gripper(self):
        self.rob.send_program('set_tool_digital_out(0, False)')
        self.rob.send_program('set_tool_digital_out(1, True)')
