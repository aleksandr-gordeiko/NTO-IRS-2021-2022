from colorsys import rgb_to_hsv
import numpy as np
from sys import maxsize

zpeak = -int(maxsize)
color = ""
bluedata = []
reddata = []

# input data, convert to hsv, find peak z
for line in open('input.txt').readlines():
    x, y, z, r, g, b = [int(p) for p in line.split()]
    h, s, v = rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    h, s, v = h*360, s*100, v*100
    if s > 25.0 and ((h < 60.0 or h > 300.0) or (300 > h > 180)):
        if 300 > h > 180:
            bluedata.append([x, y, z])
        else:
            reddata.append([x, y, z])
        if z > zpeak:
            zpeak = z
            color = 'b' if 300 > h > 180 else 'r'

# pick a peak color
if color == 'b':
    data = np.array(bluedata)
else:
    data = np.array(reddata)

# find all coordinates with z nearby zpeak
rectangle_points = []
for i in range(data.shape[0]):
    x, y, z = data[i]
    if abs(zpeak - z) < 6:
        rectangle_points.append([x, y, z])

# find the average coordinates
x, y, z = np.mean(rectangle_points, axis=0, dtype=np.float64)
print(str(round(x)) + " " + str(round(y)) + " " + str(round(z)))
