from math import asin, atan2

import numpy as np
from numpy import pi, sin, cos, matmul
from numpy.linalg import inv


def rotatex(alpha) -> np.ndarray:
    return np.array([[1, 0.0, 0.0, 0.0],
                     [0.0, cos(alpha), -sin(alpha), 0.0],
                     [0.0, sin(alpha), cos(alpha), 0.0],
                     [0.0, 0.0, 0.0, 1.0]])


def rotatey(alpha) -> np.ndarray:
    return np.array([[cos(alpha), 0.0, sin(alpha), 0.0],
                     [0.0, 1.0, 0.0, 0.0],
                     [-sin(alpha), 0, cos(alpha), 0.0],
                     [0.0, 0.0, 0.0, 1.0]])


def rotatez(alpha) -> np.ndarray:
    return np.array([[cos(alpha), -sin(alpha), 0.0, 0.0],
                     [sin(alpha), cos(alpha), 0.0, 0.0],
                     [0.0, 0.0, 1.0, 0.0],
                     [0.0, 0.0, 0.0, 1.0]])


def rotate3d(alpha, beta, gamma) -> np.ndarray:
    return np.matmul(np.matmul(rotatex(alpha), rotatey(beta)), rotatez(gamma))


def translate(x, y, z) -> np.ndarray:
    return np.array([[1.0, 0.0, 0.0, x],
                     [0.0, 1.0, 0.0, y],
                     [0.0, 0.0, 1.0, z],
                     [0.0, 0.0, 0.0, 1]])


def transform6dof(x, y, z, alpha, beta, gamma) -> np.ndarray:
    return matmul(translate(x, y, z), rotate3d(alpha, beta, gamma))


def cartesian(t):
    return np.array([t[0, 3], t[1, 3], t[2, 3]])


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


def euler2(r):
    if r[0, 2] < 1:
        if r[0, 2] > -1:
            thetaY = asin(r[0, 2])
            thetaX = atan2(-r[1, 2], r[2, 2])
            thetaZ = atan2(-r[0, 1], r[0, 0])
        else:
            thetaY = -pi / 2
            thetaX = -atan2(r[1, 0], r[1, 1])
            thetaZ = 0
    else:
        thetaY = pi / 2
        thetaX = atan2(r[1, 0], r[1, 1])
        thetaZ = 0
    return [thetaX, thetaY, thetaZ]


tool = transform6dof(-29.7 / 1000, 29.7 / 1000, 79.0 / 1000, 0.9142, 2.2072, -0.3787)
gripper = transform6dof(0, 0, 274/1000, 0, 0, 0)
gripper = transform6dof(0, 0, 0, 0.1, 0, 0)

# tcp = transform6dof(-29.7 / 1000, 29.7 / 1000, 79.0 / 1000, 0, 0, 0)

base = transform6dof(-0.28765982839401316, -0.48143664009368314, 0.8372100419534416,
                     0.5181872144358467, -0.5261257446012113, -0.7284338299497858)

base = transform6dof(-0.262977, -0.480038, 0.764635,
                     0.5181872144358467, -0.5261257446012113, -0.7284338299497858)

result = matmul(base, gripper)
# result = matmul(base, inv(translate(-29.7 / 1000, 29.7 / 1000, 79.0 / 1000)))

print(cartesian(base), euler2(base))
print(cartesian(result), euler2(result))
