from math import sqrt

import numpy as np
from math3d import Transform, Orientation, Vector
from numpy import sin, cos, matmul


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


def main():
    orv = Orientation([0.9142, 2.2072, -0.3787])
    vec = Vector(29.7 / 1000, -29.7 / 1000, 79.0 / 1000)
    tf = Transform(Orientation([0.9142, 2.2072, -0.3787]), Vector(29.7 / 1000, -29.7 / 1000, 79.0 / 1000))

    print(tf.pose_vector)

    offset = Transform(Orientation(), Vector(0, 17.5/1000, 0))

    tf = tf * offset


    print(tf.pose_vector)


if __name__ == "__main__":
    main()
