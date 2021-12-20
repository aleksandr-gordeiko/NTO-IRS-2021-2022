import sys
import numpy as np


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
saturation_threshold = 60

xmax = 0
ymax = 0
zmax = int(sys.maxsize)
for dt in data:
    x, y, z, r, g, b, h, s, v = dt
    if s > saturation_threshold and z < zmax:
        xmax, ymax, zmax = x, y, z

hue_in_max_area_rad = []
for dt in data:
    x, y, z, r, g, b, h, s, v = dt
    if s > saturation_threshold:                                # appending only saturated points
        if np.linalg.norm(np.array([x,y,z]) - np.array([xmax, ymax, zmax])) < 1:    # appending only points around 
            if not 45 < h < 160:                                    # excluding green points
                hue_in_max_area_rad.append(np.pi/180*h)

avg_hue = np.arctan2(
    sum([np.sin(a) for a in hue_in_max_area_rad])/len(hue_in_max_area_rad), 
    sum([np.cos(a) for a in hue_in_max_area_rad])/len(hue_in_max_area_rad)
)

if avg_hue < 0:
    avg_hue += np.pi*2

color = 'RED'
if 5.23599 > avg_hue > 2.0944:
    color = 'BLUE'

print(str(zmax) + " " + color)