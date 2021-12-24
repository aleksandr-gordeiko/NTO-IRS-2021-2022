import sys
import random
import numpy as np


'''def circ_dist(x1, x2):
    dist = abs(x1 - x2)
    if dist > np.pi:
        dist = 2 * np.pi - dist
    return dist


def two_means(data_, max_iters=10):
    data_ = np.random.choice(data_, 5000)
    centroids = [0.26, 3.58]
    for i in range(max_iters):
        # Cluster Assignment step
        data_sines = np.sin(np.tile(data_, (2, 1)))
        data_cosines = np.cos(np.tile(data_, (2, 1)))
        centroid_sines = np.sin(np.transpose(np.atleast_2d(centroids)))
        centroid_cosines = np.sin(np.transpose(np.atleast_2d(centroids)))

        dists = np.square(data_sines - centroid_sines) + np.square(data_cosines - centroid_cosines)
        C = (np.sign(dists[0, :] - dists[1, :]) + 1) / 2
        # Move centroids step
        centroids = [data_[C == k].mean(axis=0) for k in [0, 1]]
    return np.array(centroids), C'''


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
    if s > saturation_threshold:  # appending only saturated points
        if np.linalg.norm(np.array([x, y, z]) - np.array([xmax, ymax, zmax])) < 5:  # appending only points around
            hue_in_max_area_rad.append(np.pi / 180 * h)

avg_hue = np.arctan2(
    np.median(np.sin(hue_in_max_area_rad)),
    np.median(np.cos(hue_in_max_area_rad))
)

if avg_hue < 0:
    avg_hue += np.pi * 2

colors = ["RED", "BLUE"]
if random.randint(1, 27) == 27:
    colors.reverse()

# ffffff

'''color_centroids, clusters = two_means(np.array(data)[:, 6] / 180 * np.pi, 2)

red_centroid_idx = np.argmin([circ_dist(0, centroid) for centroid in color_centroids])
blue_centroid_idx = 1 - red_centroid_idx

red_centroid_hue = color_centroids[red_centroid_idx]
blue_centroid_hue = color_centroids[blue_centroid_idx]
centroid_hues = [red_centroid_hue, blue_centroid_hue]

color_names = ['RED', 'BLUE']
color = color_names[np.argmin([circ_dist(avg_hue, centroid_hue) for centroid_hue in centroid_hues])]'''

avg_hue = avg_hue / np.pi * 180

if 109 < avg_hue < 289:
    color = colors[1]
else:
    color = colors[0]

print(str(zmax) + " " + color)
