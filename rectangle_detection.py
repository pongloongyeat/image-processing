# Written by: https://www.pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/
# Last modified: 10/1/2019
# Dependencies: misc.py, pyimagesearch/transform.py

import cv2
import imutils
from pyimagesearch.transform import four_point_transform
import time


##################################################
# Description: Detects rectangle in image.       #
# Input:                                         #
#        @img: Str. Image path. Try to stick to  #
#              .jpg and .png for the image       #
#              filename.                         #
# Output:                                        #
#        @: None. Saves warped rectangle as      #
#           'warped.png' in /images.             #
# Usage:  detect_rect('rect_and_triangle.jpg')   #
# Expect: Perspective warped image of rectangle  #
#         saved in /images.                      #
##################################################
def detect_rect(img):

    start = time.time()

    # Read image
    img = cv2.imread(img)
    ratio = img.shape[0] / 480.0
    img_original = img.copy()
    img = imutils.resize(img, height=480)
    img_resize = img.copy()
    img = cv2.bilateralFilter(img, 9, 10, 70)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    _, _, img = cv2.split(img)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img = clahe.apply(img)
    # img = cv2.equalizeHist(img)

    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, (7, 7))
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, (7, 7))
    # img = cv2.GaussianBlur(img, (5, 5), 0)

    canny = cv2.Canny(img, 50, 150)
    cv2.imwrite("images/canny.png", canny)

    # cv2.imshow("Canny", canny)
    # cv2.imshow("Original", img_resize)

    contours_canny = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours_canny = imutils.grab_contours(contours_canny)
    contours_canny = sorted(contours_canny, key=cv2.contourArea, reverse=True)[:5]

    for c in contours_canny:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # if our approximated contour has four points, then we
        # can assume that we have found our screen
        if len(approx) == 4:
            screenCnt_canny = approx
            break

    # Show contour outline
    # img_canny = img_original.copy()
    cv2.drawContours(img_resize, [screenCnt_canny], -1, (0, 255, 0), 2)

    # cv2.imshow("Canny outline", img_resize)
    cv2.imwrite("images/canny_outline.png", img_resize)

    warped = four_point_transform(img_original, screenCnt_canny.reshape(4, 2) * ratio)

    # cv2.imshow("Perspective warped", warped)
    cv2.imwrite("images/warped.png", warped)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    end = time.time()
    print("[INFO] rectangular recognition took {:.6f} seconds".format(end - start))

    return warped

