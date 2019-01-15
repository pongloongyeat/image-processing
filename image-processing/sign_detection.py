# Written by: Pong Loong Yeat
# Last modified: 15/1/2019
# Dependencies: misc.py, rectangle_detection.py, text_recognition.py

from rectangle_detection import detect_rect
from text_recognition import read_text
import time
from misc import*


##################################################
# Description: Chooses index/row value of sign   #
#              from a chosen directory.          #
# Input:                                         #
#        @img_path: Str. Image path. Try to      #
#                   stick to .jpg and .png for   #
#                   the image filename.          #
#        @chosen_dir: Str. Chosen directory.     #
# Output:                                        #
#        @i: Int. Index in detected sign that    #
#            most closely matches @chosen_dir.   #
# Usage:  read_sign('lift_and_lab.jpg', 'lab')   #
# Expect: 1                                      #
##################################################
def detect_sign(img_path, chosen_dir):

    if not isinstance(img_path, str):
        print("Error (detect_sign): @img_path is not of type str!")
        return

    if not isinstance(chosen_dir, str):
        print("Error (detect_sign): @chosen_dir is not of type str!")
        return

    start = time.time()

    # SHIT GOES HERE
    detect_rect(img_path)
    result = read_text('images/warped.png')
    print(result)
    end = time.time()
    print("[INFO] process took {:.6f} seconds".format(end - start))

    directories = separate(result)
    i = choose_word(chosen_dir, directories)

    return directories[i]


detect_sign('images/test4.jpg', 'TOILET')
