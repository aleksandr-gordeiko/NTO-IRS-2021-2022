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
    return min < x < max


# solve for angles
def solve_triangle(a, b, c):
    return law_of_cosines(a, b, c), law_of_cosines(b, c, a), law_of_cosines(c, a, b)


def create_triangle(a1, at, b1, amin, amax, bmin, bmax, cmin, cmax, triangle_flip):
    alpha = unwrap(at - a1) if triangle_flip else unwrap(at + a1)
    beta = unwrap(pi - b1) if triangle_flip else unwrap(b1 - pi)
    gamma = unwrap(0 - alpha - beta)
    if inrange(alpha, amin, amax) and inrange(beta, bmin, bmax) and inrange(gamma, cmin, cmax):
        return alpha, beta, gamma
    return None


def is_valid_triangle(a, b, c):
    return a + b >= c and b + c >= a and c + a >= b


def main():
    l1, l2, l3 = [float(i) for i in input().split()]
    amin, amax = [float(i) for i in input().split()]
    bmin, bmax = [float(i) for i in input().split()]
    cmin, cmax = [float(i) for i in input().split()]
    hx, hy = [float(i) for i in input().split()]

    gy = hy
    gx = hx - l3
    l12 = pythagorean(gx, gy)
    at = atan2(gy, gx)
    if not is_valid_triangle(l1, l2, l12):
        return None
    a1, b1, c1 = solve_triangle(l2, l12, l1)
    ans = create_triangle(a1, at, b1, amin, amax, bmin, bmax, cmin, cmax, False)
    if ans is None:
        ans = create_triangle(a1, at, b1, amin, amax, bmin, bmax, cmin, cmax, True)

    if ans is not None:
        print(ans[0], ans[1], ans[2])
    else:
        print(None)


if __name__ == '__main__':
    main()
