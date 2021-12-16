import cv2
import numpy as np
import sys


def count_contours(mat):
    _, contours, hierarchy = cv2.findContours(mat, cv2.RETR_TREE,
                                              cv2.CHAIN_APPROX_SIMPLE)  # cv2.dilate(mat, np.ones((10, 10), np.uint8))

    count = 0
    for i in range(len(contours)):
        if hierarchy[0][i][3] == -1:
            count = count + 1

    return count


def main():
    target = (1024, 1280)

    data = []
    with sys.stdin as input_stream:
        for i in range(target[0]):
            next_line = input_stream.readline()
            pointer = 0
            while pointer < (target[1] * (6 + 1)):
                if '0' <= next_line[pointer] <= '9' or 'A' <= next_line[pointer] <= 'F':
                    data.append(int(next_line[pointer:pointer + 6], 16))
                    pointer += 6
                else:
                    pointer += 1

    data = np.ascontiguousarray(np.array(data, dtype=np.uint32)).view(np.uint8).reshape((target[0], target[1], 4))

    results = {'B': count_contours(cv2.inRange(data, (0, 0, 168, 0), (47, 47, 255, 0))),
               'R': count_contours(cv2.inRange(data, (168, 0, 0, 0), (255, 47, 47, 0)))}

    if results['B'] != results['R']:
        key = max(results, key=results.get)
    else:
        key = 'S'

    sys.stdout.write('{letter} {count}'.format(letter=key, count=max([results['B'], results['R']])))


if __name__ == "__main__":
    main()
