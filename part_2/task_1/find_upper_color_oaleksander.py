import random
import sys

import numpy as np
from math import sqrt
from colorsys import rgb_to_hls, rgb_to_hsv


def hex2rgb(hexcode):
    num = int(hexcode, 16)
    bgra = np.ascontiguousarray(np.array(num, dtype=np.uint32)).view(np.uint8).reshape(1, 1, 4)
    return bgra[0][0][2], bgra[0][0][1], bgra[0][0][0]


data = []
for line in open('input.txt').readlines():
    pixel = line.split()
    x, y, z = int(pixel[0]), int(pixel[1]), int(abs(int(pixel[2])))
    r, g, b = hex2rgb(pixel[3])
    h, v, s = rgb_to_hls(r / 255, g / 255, b / 255)
    h, s, v = h * 360, s * 100, v * 100
    data.append([x, y, z, r, g, b, h, s, v])


def main():
    color = ""
    xmax = 0
    ymax = 0
    zmax = int(sys.maxsize)
    for dt in data:
        x, y, z, r, g, b, h, s, v = dt
        if s > 50 and 10 < v < 90 and z < zmax:  # and ((h < 60 or h >= 300) or (300 > h > 180)) and 0 < v < 100:
            xmax, ymax, zmax = x, y, z

    rgbmax = []
    for dt in data:
        x, y, z, r, g, b, h, s, v = dt
        if s > 50 and 10 < v < 90:  # and ((h < 60 or h >= 300) or (300 > h > 180)) and 3 < v < 100:
            if abs(z - zmax) <= 1 and sqrt((x - xmax) ** 2 + (y - ymax) ** 2) <= 1:
                rgbmax.append([r, g, b])

    greyrgb = []
    '''for dt in data:
        x, y, z, r, g, b, h, s, v = dt
        if s < 10:
            greyrgb.append([r, g, b])
    '''

    # rg, gg, bg = np.mean(greyrgb, axis=0, dtype=np.float64)

    r, g, b = np.mean(rgbmax, axis=0, dtype=np.float64)
    # r, g, b = r / rg, g / gg, b / bg
    h, s, v = rgb_to_hsv(r / 255, g / 255, b / 255)

    # print(h, s, v)

    green_border = 109

    bmax = (green_border + 180) / 360  # 290

    bmin = green_border / 360  # 110

    if random.randint(1, 27) == 27:
        if bmax > h > bmin:  # inverse
            color = "BLUE"
        else:
            color = "RED"
    else:
        if bmax > h > bmin:  # forward
            color = "BLUE"
        else:
            color = "RED"

    print(str(zmax) + " " + color)


if __name__ == '__main__':
    main()
