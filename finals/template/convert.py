import cv2
import numpy as np
import open3d as o3d
import copy

redPoints = []
bluePoints = []
cur = 0

minY = 0
maxY = 0
minX = 0
maxX = 0

dots = o3d.io.read_point_cloud("1.ply")

for i in dots.colors:
    if (int(i[0] * 255) - 5. > int(i[1] * 255)) and (int(i[0] * 255) - 10. > int(i[2] * 255)) \
            and (int(dots.points[cur][2]*1000) > -630):
        redPoints.append([int(dots.points[cur][0]*1000), int(dots.points[cur][1]*1000), int(dots.points[cur][2]*1000),
                          (int(i[2]*255), int(i[1]*255), int(i[0]*255))])

    elif (int(i[2] * 255) - 5. > int(i[0] * 255)) and (int(i[2] * 255) - 10. > int(i[1] * 255)) \
            and (int(dots.points[cur][2] * 1000) > -630):
        bluePoints.append(
            [int(dots.points[cur][0] * 1000), int(dots.points[cur][1] * 1000), int(dots.points[cur][2] * 1000),
             (int(i[2] * 255), int(i[1] * 255), int(i[0] * 255))])

    minY = min(minY, int(dots.points[cur][1] * 1000))
    minX = min(minX, int(dots.points[cur][0] * 1000))
    maxY = max(maxY, int(dots.points[cur][1] * 1000))
    maxX = max(maxX, int(dots.points[cur][0] * 1000))

    cur += 1

img = np.zeros((maxY-minY+1, maxX-minX+1, 3), np.uint8)
for i in redPoints:
    img[i[1]-minY][i[0]-minX] = i[3]
for i in bluePoints:
    img[i[1]-minY][i[0]-minX] = i[3]

img = cv2.flip(img, 1)
# imgCopy = copy.deepcopy(img)

