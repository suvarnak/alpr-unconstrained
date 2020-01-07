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

def save_frame(frame, frames_dir,count):
	cv2.imwrite(os.path.join(frames_dir, "frame"+str(count)+".jpg"), frame)     # save frame as JPG file

def get_vid_generator(filename):
	metadata = skvideo.io.ffprobe(filename)
	if(metadata):
		print(metadata.get('video').keys())
		width = (int)(metadata.get('video').get('@width'))
		height = (int)(metadata.get('video').get('@height'))
		print(metadata.get('video').get('@display_aspect_ratio'))
		print(width,height)
		if(width<height):
			print("rotated...........")
	videogen = skvideo.io.vreader(filename)#cv2.VideoCapture(filename)
	return videogen

if __name__ == "__main__":
		input_dir = sys.argv[1]
		output_dir = sys.argv[2]
		frames_dir = os.path.join(output_dir,'frames')
		if not os.path.isdir(frames_dir):
			print('making directory')
			os.makedirs(frames_dir)
		for file in os.listdir(input_dir):
			print(file)
			count = 0
			video_generator = get_vid_generator(os.path.join(input_dir,file))
			for frame in video_generator:
				save_frame(frame,frames_dir,count)
				count = count +1
				if count > 20:
					break


			

	
