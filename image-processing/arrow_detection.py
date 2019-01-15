import cv2
import numpy as np


def detect_arrow(img_path):

    if not isinstance(img_path, str):
        print("Error (detect_arrow): @img_path is not of type str!")
        return

    img = cv2.imread(img_path)
    # Convert the image to grayscale
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Apply canny edge detection to the image
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Perform Hough Lines on the image
    lines = cv2.HoughLines(edges, 1, np.pi/180, 20)

    # Create an array for each direction, where array[0] indicates one of the lines and array[1] indicates the other,
    # for which if both > 0 will tell us the orientation
    left = [0, 0]
    right = [0, 0]
    up = [0, 0]
    down = [0, 0]

    # Iterate through the lines that the houghlines function returned
    for obj in lines:
        theta = obj[0][1]
        rho = obj[0][0]
        # Cases for right/left arrows
        if 1.0 <= (np.round(theta, 2) <= 1.1)\
                or 2.0 <= np.round(theta, 2) <= 2.1:
            if 20 <= rho <= 30:
                left[0] += 1
            elif 60 <= rho <= 65:
                left[1] += 1
            elif -73 <= rho <= -57:
                right[0] += 1
            elif 148 <= rho <= 176:
                right[1] += 1
        # Cases for up/down arrows
        elif 0.4 <= np.round(theta, 2) <= 0.6\
                or 2.6 <= np.round(theta, 2) <= 2.7:
            if -15 <= rho <= 63:
                up[0] += 1
            elif 67 <= rho <= 74:
                down[1] += 1
                up[1] += 1
            elif 160 <= rho <= 171:
                down[0] += 1

    if left[0] >= 1 and left[1] >= 1:
        return 'left'
    elif right[0] >= 1 and right[1] >= 1:
        return 'right'
    elif up[0] >= 1 and up[1] >= 1:
        return 'up'
    elif down[0] >= 1 and down[1] >= 1:
        return 'down'


direction = detect_arrow('images/warped_arrow.png')
print(direction)
