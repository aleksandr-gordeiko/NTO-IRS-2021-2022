from math import atan2

from numpy import ascontiguousarray, uint32, uint8, array


def main():
    zmax = -1000000
    for line in open('input.txt').readlines():
        pixel = line.split()
        z = int(pixel[2])
        b, g, r, _ = ascontiguousarray(array(int(pixel[3], 16), dtype=uint32)).view(uint8)
        maxc, minc = max(r, g, b), min(r, g, b)
        if (.0 if minc == maxc else (maxc - minc) / maxc) > .6 and z > zmax:
            atan = atan2(r, b)
            zmax, color = z, 0 if atan > .78 or .23 > atan > .21 else 1
    print(str(-zmax) + " " + ["RED", "BLUE"][color])


if __name__ == '__main__':
    main()
