from math import cos, asin, atan2, pi

from numpy import transpose, dot, array
from numpy.linalg import inv


def cartesian(t):
    return [t[0, 3], t[1, 3], t[2, 3]]


def euler(r):
    if r[2, 0] != 1 and r[2, 0] != -1:
        rot_y = -1 * asin(r[2, 0])
        rot_x = atan2(r[2, 1] / cos(rot_y), r[2, 2] / cos(rot_y))
        rot_z = atan2(r[1, 0] / cos(rot_y), r[0, 0] / cos(rot_y))
    else:
        rot_z = 0
        if r[2, 0] == -1:
            rot_y = pi / 2
            rot_x = rot_z + atan2(r[0, 1], r[0, 2])
        else:
            rot_y = -pi / 2
            rot_x = -1 * rot_z + atan2(-1 * r[0, 1], -1 * r[0, 2])

    return [rot_x, rot_y, rot_z]


def main():
    tr = array([float(i) for i in input().split()]).reshape(4, 4)
    tf = array([float(i) for i in input().split()]).reshape(4, 4)
    tt = dot(inv(tr), tf)
    tx, ty, tz = [str(round(t, 3)) for t in cartesian(tt)]
    rx, ry, rz = [(-round(r, 3)) for r in euler(transpose(tt))]
    print(tx, ty, tz, rx, ry, rz)


if __name__ == '__main__':
    main()
