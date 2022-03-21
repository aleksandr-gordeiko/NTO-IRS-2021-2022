import time
from math import pi

from OperateCamera import OperateCamera
from OperateRobot import OperateRobot

# Connection to the robot
rob = OperateRobot("172.31.1.25")

# Taking global linear position of arm
pos = rob.getl()
pos[0] += 0.1

moving_coordinates = {"x": pos[0], "y": pos[1], "z": pos[2], "rx": pos[3], "ry": pos[4], "rz": pos[5]}

# Moving to new coordinates. X + 10 mm
rob.movel(moving_coordinates)
time.sleep(2)

# Moving to position for taking frame from camera
rob.movel({"x": -0.82, "y": -0.1723, "z": 0.68, "rx": 1.487, "ry": 3.536, "rz": -0.669})
time.sleep(4)

# Open gripper of arm
rob.open_gripper()
time.sleep(2)

# Close gripper of arm
rob.close_gripper()
time.sleep(2)

cam = OperateCamera()

# Taking data frame from camera (RGBD format)
frame = cam.catch_frame()

# Printing x y z of some point
print(frame.points[0])
# Printing r g b color of some point
print(frame.colors[0])

# Saving test data frame from camera (RGBD format)
cam.save("test.ply")

# Loading test data frame from file (RGBD format)
pcd = cam.open("test.ply")

# Visualizing test data frame
cam.visualization_of_points(pcd)
