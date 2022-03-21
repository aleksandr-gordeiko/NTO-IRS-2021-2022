from random import randint

from numpy import ascontiguousarray, uint32, uint8, array

zmax = -1000000
for line in open('input.txt').readlines():
    pixel = line.split()
    z = int(pixel[2])
    b, g, r, _ = ascontiguousarray(array(int(pixel[3], 16), dtype=uint32)).view(uint8)
    maxc, minc = max(r, g, b), min(r, g, b)
    s = .0 if minc == maxc else (maxc - minc) / maxc
    if s > .6 and z > zmax:
        zmax = z
        color = 1 if b > r else 0

color = 1 - color if randint(1, 27) == 1 else color

print(str(-zmax) + " " + ["RED", "BLUE"][color])
