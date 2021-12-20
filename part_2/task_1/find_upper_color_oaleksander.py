import random
import sys

import numpy as np
from math import sqrt


def rgb2hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx - mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g - b) / df) + 360) % 360
    elif mx == g:
        h = (60 * ((b - r) / df) + 120) % 360
    elif mx == b:
        h = (60 * ((r - g) / df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df / mx) * 100
    v = mx * 100
    return h, s, v


def hex2rgb(hexcode):
    num = int(hexcode, 16)
    bgra = np.ascontiguousarray(np.array(num, dtype=np.uint32)).view(np.uint8).reshape(1, 1, 4)
    return bgra[0][0][2], bgra[0][0][1], bgra[0][0][0]


data = []
for line in open('input.txt').readlines():
    pixel = line.split()
    x, y, z = int(pixel[0]), int(pixel[1]), int(abs(int(pixel[2])))
    r, g, b = hex2rgb(pixel[3])
    h, s, v = rgb2hsv(r, g, b)
    data.append([x, y, z, r, g, b, h, s, v])

color = ""
xmax = 0
ymax = 0
zmax = int(sys.maxsize)
for dt in data:
    x, y, z, r, g, b, h, s, v = dt
    if s > 55 and ((h < 60 or h >= 300) or (300 > h > 180)) and 25 < v < 75 and z < zmax:
        xmax, ymax, zmax = x, y, z

rgbmax = []
for dt in data:
    x, y, z, r, g, b, h, s, v = dt
    if s > 55 and ((h < 60 or h >= 300) or (300 > h > 180)) and 25 < v < 75:
        if abs(z - zmax) <= 2 and sqrt((x - xmax) ** 2 + (y - ymax) ** 2) <= 10:
            rgbmax.append([r, g, b])

r, g, b = np.mean(rgbmax, axis=0, dtype=np.float64)
h, s, v = rgb2hsv(r, g, b)

if 300 > h > 180:
    color = "BLUE"
elif h < 60 or h >= 300:
    color = "RED"
else:
    color = random.choice(["RED", "BLUE"])

print(str(zmax) + " " + color)
