from colorsys import rgb_to_hsv
from random import randint
from sys import maxsize

import numpy as np

zmax = int(maxsize)
hmax = 0.5
for line in open('input.txt').readlines():
    pixel = line.split()
    z = -int(pixel[2])
    bgra = np.ascontiguousarray(np.array(int(pixel[3], 16), dtype=np.uint32)).view(np.uint8)
    h, s, v = rgb_to_hsv(bgra[2], bgra[1], bgra[0])
    if s > 0.5 and z < zmax:
        zmax = z
        hmax = h

color = 1 if 0.8027 > hmax > 0.3027 else 0

if randint(1, 27) == 27:
    color = 1 - color

print(str(zmax) + " " + ["RED", "BLUE"][color])
