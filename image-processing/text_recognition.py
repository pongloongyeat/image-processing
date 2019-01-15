# Written by: http://www.tramvm.com/2017/05/recognize-text-from-image-with-python.html
# Last modified: 10/1/2019
# Dependencies: -

import cv2
import numpy as np
import pytesseract
import time


##################################################
# Description: Reads text from a close-up image. #
# Input:                                         #
#        @img_path: Str. Image path. Try to      #
#                   stick# to .jpg and .png for  #
#                   the image filename.          #
# Output:                                        #
#        @result: Str. Detected text at          #
#                 @img_path.                     #
# Usage:  read_text('images/coke_label.png')     #
# Expect: 'COKE'                                 #
##################################################
def read_text(img_path=""):

    # Check if img_name is str and exists
    if img_path == "":
        print("Error (read_text): @img_path not specified!")
        return

    if not isinstance(img_path, str):
        print("Error (read_text): @img_name is not of type str!")
        return

    start = time.time()

    # Read image
    img = cv2.imread(img_path)

    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # Write image after removed noise
    # cv2.imwrite("images/removed_noise.png", img)

    # Apply threshold to get image with only black and white
    # img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(img)

    end = time.time()

    # show timing information on text prediction
    print("[INFO] text recognition took {:.6f} seconds".format(end - start))

    # Remove template file
    # os.remove(temp)

    return result
