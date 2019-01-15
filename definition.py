#Autonomous indoor navigation robot
#Created by: Ricky sutopo
#Imported by: Calvin
#Date modified: 1/10/2018




from __future__ import division
import cv2
import numpy as np
import time
from matplotlib import pyplot as plt
ratio=1
from text_recognition import read_text



def extractDir(oneArrow):
    # input: oneArrow: single arrow image
    # output: out: direction of the arrow
    imgGray = cv2.cvtColor(oneArrow, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(imgGray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    thresholded_open = cv2.morphologyEx(thresholded, cv2.MORPH_OPEN, (7, 7))
    thresholded_close = cv2.morphologyEx(thresholded_open, cv2.MORPH_CLOSE, (7, 7))
    edges = cv2.Canny(thresholded_close, 50, 200)
    cnts = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    outCnt = None
    cntM = cnts[0]
    M = cv2.moments(cntM)

    ##    for c in cnts:
    ##        peri = cv2.arcLength(c, True)
    ##        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    ##        if len(approx) == 7 or len(approx) == 9:
    ##            outCnt = approx
    ##            break
    ##    print len(approx)
    ##    if len(approx) == 7:
    ##        points = outCnt.reshape(7,2)
    ##    elif len(approx) == 9:
    ##        points = outCnt.reshape(9,2)

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) > 5:
            outCnt = approx
            break
    ##    print len(approx)
    points = outCnt.reshape(len(approx), 2)

    x = points[:, 0]
    y = points[:, 1]
    xmin = x[np.argmin(x)]
    xmax = x[np.argmax(x)]
    ymin = y[np.argmin(y)]
    ymax = y[np.argmax(y)]
    focus = oneArrow[ymin:ymax, xmin:xmax]

    # Find the centroid of the contour
    cx = int(M['m10'] / M['m00']) - xmin
    cy = int(M['m01'] / M['m00']) - ymin

    arrowX = xmax - xmin
    arrowY = ymax - ymin
    # Un-comment to draw the contours, centroid on the arrow
    ##    dot = cv2.line(focus,(0,0),(arrowX,arrowY),(0,0,255),3)
    ##    dot = cv2.line(focus,(arrowX,0),(0,arrowY),(0,0,255),3)
    ##    dot = cv2.line(focus,(cx,cy),(cx,cy),(255,0,0),3)
    ##    cv2.imshow("Final",dot)

    # Check the direction of the arrow
    if (isInside(0, 0, int(arrowX / 2), int(arrowY / 2), 0, arrowY, cx, cy)):
        out = 'Left'
    elif (isInside(0, 0, int(arrowX / 2), int(arrowY / 2), arrowX, 0, cx, cy)):
        out = 'Up'
    elif (isInside(arrowX, 0, int(arrowX / 2), int(arrowY / 2), arrowX, arrowY, cx, cy)):
        out = 'Right'
    else:
        out = 'No arrow'
    return out

def isInside(x1, y1, x2, y2, x3, y3, x, y):
    # Check if the centroid at x,y is inside the triangle
    A = area(x1, y1, x2, y2, x3, y3)
    A1 = area(x, y, x2, y2, x3, y3)
    A2 = area(x1, y1, x, y, x3, y3)
    A3 = area(x1, y1, x2, y2, x, y)

    if (A == A1 + A2 + A3):
        return True
    else:
        return False
def area(x1, y1, x2, y2, x3, y3):
    # Find the area of a triangle using 3 coordinate points
     return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

# Can be deleted if not needed
def cutimage(image,w,h):
    y1 = 0
    M = h #// 20
    N = w // 20

    for y in range(0, h, M):
        for x in range(0, w, N):
            y1 = y + M
            x1 = x + N
            tiles = image[y:y + M, x:x + N]

            cv2.rectangle(image, (x, y), (x1, y1), (0, 255, 0))
            cv2.imwrite("save/" + str(x) + '_' + str(y) + ".png", tiles)

    cv2.imwrite("asas.png", image)

def cut_sign(image,w,h):
    # Inputs
    # image = RGB image of sign
    # w = width of image
    # h = height of image
    # Outputs
    # sign_col= image of sign
    # word_col= image of word
    col_div = 120 #width of sign image to crop

    sign_col = image[0:h, w-col_div:w]
    word_col = image[0:h, 0:w-col_div]
    cv2.imwrite("col_word.png", word_col)
    cv2.imwrite("col_sign.png", sign_col)
    return sign_col,word_col

def separate_sign(image,w,h,n):
    # Inputs
    # image = RGB image of sign
    # w = width of image
    # h = height of image
    # n = number of column
    # Outputs
    # img = an array of direction of the signs in order
    ##Debugging also
    #count =0
    N = h // n

    dir_array = []

    for y in range(0, h, N):

        tiles = image[y:y + N, 0:w]
        if tiles.shape[0]>5:
            dir_array.append(extractDir(tiles))
        ## For debugging only where it will produce the png files
        #     cv2.imwrite("save/" + "sign" + str(count) + ".png", tiles)
        # count += 1
    return dir_array

# Used for debugging

src_path = "D:/Documents/Dog Robot Project/navigation/pic/"
img_path = src_path + "warped.png"

img = cv2.imread(img_path)
height, width = img.shape[:2]
sign_pic,word_pic = cut_sign(img,width,height)

sign_dir = separate_sign(sign_pic,width,height,4)
#print(read_text("col_sign.png"))
print(sign_dir)