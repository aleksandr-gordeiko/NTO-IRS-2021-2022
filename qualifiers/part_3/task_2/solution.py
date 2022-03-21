from math import sin, cos


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


n = int(input())

points = []
points.append([0, 0])
currentangle = 0
intersections = []

for i in range(n):
    length, angle = [float(i) for i in input().split()]
    currentpoint = points[i]
    currentangle = currentangle + angle
    nextpoint = forwardkinematics(currentpoint, length, currentangle)
    for j in range(i - 1):
        if intersects(points[j], points[j + 1], currentpoint, nextpoint):
            intersections.append(intersect([points[j], points[j + 1]], [currentpoint, nextpoint]))
    points.append(nextpoint)

print(len(intersections))
for intr in intersections:
    print("{x} {y}".format(x=intr[0], y=intr[1]))
