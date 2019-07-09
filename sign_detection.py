# Written by: Pong Loong Yeat, Calvin Low
# Last modified: 16/1/2019
# Dependencies: misc.py, rectangle_detection.py, text_recognition.py

from rectangle_detection import detect_rect
from text_recognition import read_text
import time
from misc import *
from picamera import PiCamera
from time import sleep
import subprocess
from arrow_detection import *


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
def detect_sign(img_path):

    if not isinstance(img_path, str):
        print("Error (detect_sign): @img_path is not of type str!")
        return

    start = time.time()

    # SHIT GOES HERE
    warped = detect_rect(img_path)
    height, width = warped.shape[:2]
    arrow, directories = cut_sign(warped,width,height)

    end = time.time()
    print("[INFO] process took {:.6f} seconds".format(end - start))

    return arrow, directories


def img_capture(img_path):
    src_path = "/home/pi/indoor_navigation/summer_2019/"
    cmd = "raspistill -q 100 -md 2 -vf -hf -o " + src_path + img_path
    subprocess.call(cmd, shell=True)


def process_directories(img_path, chosen_dir):

    if not isinstance(img_path, str):
        print("Error (detect_sign): @img_path is not of type str!")
        return

    if not isinstance(chosen_dir, str):
        print("Error (detect_sign): @chosen_dir is not of type str!")
        return

    start = time.time()

    result = read_text(img_path)
    directories = separate(result)
    i = choose_word(chosen_dir, directories)

    end = time.time()
    print("[INFO] process took {:.6f} seconds".format(end - start))

    return i


def process_arrow(img_arrow, i):
    start = time.time()

    height, width = img_arrow.shape[:2]
    arrow_dir = separate_sign(img_arrow, width, height, 4)

    end = time.time()
    print("[INFO] process took {:.6f} seconds".format(end - start))

    return arrow_dir[i]


src_path = "/home/pi/indoor_navigation/summer_2019/images/"
arrow_image, directories = detect_sign(src_path + "test4.jpg")
index = process_directories("directories.png", "LAB")
arrow_direction = process_arrow(arrow_image, index)

print(arrow_direction)

# image_path = 'images/test4.jpg'
# img_capture(image_path)
# detect_sign(image_path)
# src_path = "/home/pi/indoor_navigation/summer_2019/images/"
# img_path = src_path + "warped.png"
# img = cv2.imread(img_path)
# height, width = img.shape[:2]
# sign_pic,word_pic = cut_sign(img,width,height)
#
# sign_dir = separate_sign(sign_pic,width,height,4)
# print(read_text("col_word.png"))
# print(sign_dir)
