from OperateRobot import OperateRobot
from OperateCamera import OperateCamera
from cv import analyze_image

def main():
    '''robot = OperateRobot("172.31.1.25", [0, 0, 0, 0, 0, 0], [[0, 0], [0, 0]], [[0, 0], [0, 0]], [[0, 0], [0, 0]])
    cam = OperateCamera()

    pos = robot.getl()
    pos[0] += 1
    robot.movel(pos)'''
    analyze_image()
    '''frame = cam.catch_frame()
    print(frame.points[0])
    print(frame.colors[0])
    cam.save("test.ply")
    pcd = cam.open("test.ply")
    cam.visualization_of_points(pcd)'''

    # robot.close()


if __name__ == "__main__":
    main()