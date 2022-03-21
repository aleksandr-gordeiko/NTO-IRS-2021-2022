from math import sqrt, atan2, acos, pi, radians, degrees


def law_of_cosines(a, b, c):
    return acos((b * b + c * c - a * a) / (2 * b * c))


def pythagorean(a, b):
    return sqrt(a * a + b * b)


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


def create_triangle(a1, at, b1, amin, amax, bmin, bmax, triangle_flip):
    alpha = unwrap(at - a1) if triangle_flip else unwrap(at + a1)
    beta = unwrap(pi - b1) if triangle_flip else unwrap(b1 - pi)
    if inrange(alpha, amin, amax) and inrange(beta, bmin, bmax):
        return alpha, beta
    return None


def is_valid_triangle(a, b, c):
    return a + b >= c and b + c >= a and c + a >= b


def main():
    l1, l2 = 225, 275
    amin, amax = -radians(132), radians(132)
    bmin, bmax = -radians(145), radians(145)
    hx, hy, hz = [int(i) for i in input().split()]
    l12 = pythagorean(hx, hy)
    at = atan2(hy, hx)
    if not is_valid_triangle(l1, l2, l12):
        q = [at, 0]
    else:
        a1, b1, c1 = solve_triangle(l2, l12, l1)
        q = create_triangle(a1, at, b1, amin, amax, bmin, bmax, True)
        if q is None:
            q = create_triangle(a1, at, b1, amin, amax, bmin, bmax, False)
    q = [round(degrees(i)) for i in q]
    q.append(round(hz - 200))
    q.append(int(0))
    print(*q, sep=' ')


if __name__ == '__main__':
    main()
