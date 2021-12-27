from math import asin, atan2

from numpy import pi, sin, cos, radians, matmul


def rotatex(alpha):
    return [[1, 0.0, 0.0, 0.0],
            [0.0, cos(alpha), -sin(alpha), 0.0],
            [0.0, sin(alpha), cos(alpha), 0.0],
            [0.0, 0.0, 0.0, 1.0]]


def rotatey(alpha):
    return [[cos(alpha), 0.0, sin(alpha), 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [-sin(alpha), 0, cos(alpha), 0.0],
            [0.0, 0.0, 0.0, 1.0]]


def rotatez(alpha):
    return [[cos(alpha), -sin(alpha), 0.0, 0.0],
            [sin(alpha), cos(alpha), 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]]


def translate(x, y, z):
    return [[1.0, 0.0, 0.0, x],
            [0.0, 1.0, 0.0, y],
            [0.0, 0.0, 1.0, z],
            [0.0, 0.0, 0.0, 1]]


def cartesian(t):
    return [t[0, 3], t[1, 3], t[2, 3]]


def euler(r):
    if r[2, 0] != 1 and r[2, 0] != -1:
        pitch = -1 * asin(r[2, 0])
        roll = atan2(r[2, 1] / cos(pitch), r[2, 2] / cos(pitch))
        yaw = atan2(r[1, 0] / cos(pitch), r[0, 0] / cos(pitch))
    else:
        yaw = 0
        if r[2, 0] == -1:
            pitch = pi / 2
            roll = yaw + atan2(r[0, 1], r[0, 2])
        else:
            pitch = -pi / 2
            roll = -1 * yaw + atan2(-1 * r[0, 1], -1 * r[0, 2])

    return [roll, pitch, yaw]


def gettoolposition(theta):
    j = matmul(rotatez(radians(-theta[0])), matmul(translate(25.0, 0.0, 400.0), rotatex(pi)))  # 1
    j = matmul(matmul(j, rotatex(pi / 2.0)), rotatez(radians(theta[1])))  # 2
    j = matmul(
        matmul(matmul(matmul(j, translate(560.0, 0.0, 0.0)), rotatez(radians(theta[2]))), translate(117.0, -35.0, 0.0)),
        rotatey(-pi / 2.0))  # 3
    j = matmul(matmul(matmul(j, rotatez(radians(theta[3]))), translate(0.0, 0.0, -398.0)), rotatey(pi / 2.0))  # 4
    j = matmul(matmul(matmul(j, rotatez(radians(theta[4]))), translate(80.0, 0.0, 0.0)), rotatey(pi / 2.0))  # 5
    j = matmul(matmul(matmul(j, rotatez(radians(-theta[5]))), rotatex(pi / 2.0)), rotatez(pi / 2.0))  # 6

    return cartesian(j)


def inrange(min, x, max):
    return min < x < max or min > x > max


def main():
    tool_x, tool_y, tool_z = gettoolposition([int(num) for num in input().split()])
    ans = []
    for i in range(int(input())):
        n, rect_x1, rect_y1, rect_z1, rect_x2, rect_y2, rect_z2 = [float(num) for num in input().split()]
        if inrange(rect_x1, tool_x, rect_x2) and inrange(rect_y1, tool_y, rect_y2) and inrange(rect_z1, tool_z,
                                                                                               rect_z2):
            ans.append(n)
    print(len(ans))
    for n in ans:
        print(int(n))


if __name__ == '__main__':
    main()
