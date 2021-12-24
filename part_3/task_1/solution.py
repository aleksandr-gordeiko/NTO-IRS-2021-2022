from math import sqrt, atan2, acos, pi


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
    return min <= x <= max


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
    at = float(atan2(gy, gx))
    if not is_valid_triangle(l1, l2, l12):
        return None
    a1, b1, c1 = solve_triangle(l2, l12, l1)
    l3_direction = pi if l3_negative else 0
    ans = solve_for_first_two_joints(a1, at, b1, amin, amax, bmin, bmax, cmin, cmax, l3_direction, False)
    if ans == None:
        ans = solve_for_first_two_joints(a1, at, b1, amin, amax, bmin, bmax, cmin, cmax, l3_direction, True)
    return ans


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
        print(ans[0], ans[1], ans[2])
    else:
        print(None)


if __name__ == '__main__':
    main()
