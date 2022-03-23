import cv2 as cv
import numpy as np
import copy


def fill_gaps(mat: cv.mat_wrapper, n_iterations=20) -> cv.mat_wrapper:
    res = mat.copy()
    for i in range(n_iterations):
        cv.copyTo(cv.dilate(res, cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3)), iterations=2),
                  dst=res, mask=cv.inRange(res, np.array([0, 0, 0]), np.array([1, 1, 1])))
    return res


def slip_obj(src, bin_src):
    img_test = cv.Canny(src, 0, 255, None, 3, 0)
    dst = cv.addWeighted(bin_src, 1, img_test, -1, 0.0)
    dist = cv.distanceTransform(dst, cv.DIST_L2, 3)
    cv.normalize(dist, dist, 0, 1.0, cv.NORM_MINMAX)
    dist = dist.astype("float32")
    dst = dst.astype("float32")
    final = cv.addWeighted(dst, 0.001, dist, 1, 0.0)
    # cv.imshow("final", final)
    # cv.imshow("dst", dst)
    # cv.imshow("dist", dist)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    _, final = cv.threshold(final, 0.37, 255, cv.THRESH_BINARY)
    return copy.deepcopy(final.astype("uint8"))
