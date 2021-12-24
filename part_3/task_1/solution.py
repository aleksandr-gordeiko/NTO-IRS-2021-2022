from math import sqrt, atan2, acos, pi, cos, sin


def law_of_cosines(a, b, c):
    return acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))


def pythagorean(a, b):
    return sqrt(a ** 2 + b ** 2)


def unwrap(a):
    while a < -pi:
        a += 2 * pi
    while a >= pi:
        a -= 2 * pi
    return a


def inrange(x, min, max):
    return min < x < max


# solve for angles
def solve_triangle(a, b, c):
    return law_of_cosines(a, b, c), law_of_cosines(b, c, a), law_of_cosines(c, a, b)


def solve_for_first_two_joints(a1, at, b1, amin, amax, bmin, bmax, cmin, cmax, l3_direction, triangle_flip):
    alpha = unwrap(at - a1) if triangle_flip else unwrap(a1 + at)
    beta = unwrap(pi - b1) if triangle_flip else unwrap(b1 - pi)
    gamma = unwrap(l3_direction - alpha - beta)
    if inrange(alpha, amin, amax) and inrange(beta, bmin, bmax) and inrange(gamma, cmin, cmax):
        return alpha, beta, gamma
    else:
        return None


def is_valid_triangle(a, b, c):
    if a + b >= c and b + c >= a and c + a >= b:
        return True
    else:
        return False


def solve_assuming_l3(l1, l2, l3, amin, amax, bmin, bmax, cmin, cmax, hx, hy, l3_negative):
    gy = hy
    gx = hx + l3 if l3_negative else hx - l3
    l12 = pythagorean(gx, gy)
    at = atan2(gy, gx)
    if not is_valid_triangle(l1, l2, l12):
        return None
    a1, b1, c1 = solve_triangle(l2, l12, l1)
    l3_direction = -pi if l3_negative else 0
    ans = solve_for_first_two_joints(a1, at, b1, amin, amax, bmin, bmax, cmin, cmax, l3_direction, False)
    if ans is None:
        ans = solve_for_first_two_joints(a1, at, b1, amin, amax, bmin, bmax, cmin, cmax, l3_direction, True)
    return ans


#########################

def forwardkinematics(p0, l1, alpha):
    return p0[0] + l1 * cos(alpha), p0[1] + l1 * sin(alpha)


def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])


# Return true if line segments AB and CD intersect
def intersects(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


def intersect(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


#########################


def main():
    l1, l2, l3 = [float(i) for i in input().split()]
    amin, amax = [float(i) for i in input().split()]
    bmin, bmax = [float(i) for i in input().split()]
    cmin, cmax = [float(i) for i in input().split()]
    hx, hy = [float(i) for i in input().split()]

    ans = solve_assuming_l3(l1, l2, l3, amin, amax, bmin, bmax, cmin, cmax, hx, hy, False)
    if ans is None:
        ans = solve_assuming_l3(l1, l2, l3, amin, amax, bmin, bmax, cmin, cmax, hx, hy, True)
    if ans is not None:
        points = []
        points.append([0, 0])
        points.append(forwardkinematics(points[len(points) - 1], l1, ans[0]))
        points.append(forwardkinematics(points[len(points) - 1], l2, ans[0] + ans[1]))
        points.append(forwardkinematics(points[len(points) - 1], l3, ans[0] + ans[1] + ans[2]))
        if not intersects(points[0], points[1], points[2], points[3]) \
                and abs(points[3][0] - hx) < float(1.0e-7) and abs(points[3][1] - hy) < float(1.0e-7) \
                and inrange(ans[0], amin, amax) and inrange(ans[1], bmin, bmax) and inrange(ans[2], cmin, cmax):
            print(ans[0], ans[1], ans[2])
        else:
            print(None)
    else:
        print(None)


if __name__ == '__main__':
    main()
