import cv2 as cv
import numpy as np


def fill_gaps(mat: cv.mat_wrapper, n_iterations=20) -> cv.mat_wrapper:
    res = mat.copy()
    for i in range(n_iterations):
        cv.copyTo(cv.dilate(res, cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3)), iterations=2),
                  dst=res, mask=cv.inRange(res, np.array([0, 0, 0]), np.array([1, 1, 1])))
    return res
