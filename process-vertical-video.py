import sys
import os
import cv2
"""
This script creates frames from video present in input directory
Usage
$ python process-video.py <input-dir-containing-video>
"""
import cv2
import skvideo.io
import json


def getFrame(sec, framename):
    vidcap.set(cv2.CAP_PROP_POS_MSEC, sec*1000)
    hasFrames, image = vidcap.read()
    if hasFrames:
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        cv2.imwrite(framename, image)     # save frame as JPG file
    return hasFrames


if __name__ == "__main__":
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    frames_dir = os.path.join(output_dir, 'frames')
    if not os.path.isdir(frames_dir):
        print('making directory')
        os.makedirs(frames_dir)
    for file in os.listdir(input_dir):
        print(file)
        vidcap = cv2.VideoCapture(os.path.join(input_dir, file))
        sec = 0
        frameRate = 0.15  # //it will capture image in each 0.5 second
        count = 0
        framename = os.path.join(frames_dir, "image"+str(count)+".jpg")
        success = getFrame(sec, framename)
        print(success)
        while success and count < 100:
            count = count + 1
            sec = sec + frameRate
            sec = round(sec, 2)
            framename = os.path.join(frames_dir, "image"+str(count)+".jpg")
            success = getFrame(sec, framename)
