from colorsys import rgb_to_hsv
from random import randint
from sys import maxsize

from numpy import ascontiguousarray, uint32, uint8, array


def main():
    zmax = -int(maxsize)
    for line in open('input.txt').readlines():
        pixel = line.split()
        z = int(pixel[2])
        bgra = ascontiguousarray(array(int(pixel[3], 16), dtype=uint32)).view(uint8)
        h, s, _ = rgb_to_hsv(bgra[2], bgra[1], bgra[0])
        if s > 0.5 and z > zmax:
            zmax = z
            hmax = h

    color = 1 if .3027 < hmax < .8027 else 0

    if randint(1, 27) == 27:
        color = 1 - color

    print(str(-zmax) + " " + ["RED", "BLUE"][color])


if __name__ == '__main__':
    main()  # //////////////
