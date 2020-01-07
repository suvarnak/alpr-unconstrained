import os
import sys
import cv2
import numpy as np
import glob

if __name__ == "__main__":
	input_dir  = sys.argv[1]
	output_dir = sys.argv[2]
	if not os.path.isdir(output_dir):
		print('making directory')
		os.makedirs(output_dir)
	# Fetch all the image file names using glob.
	img_array = []
	size = (640,360)
	for filename in glob.glob(os.path.join(input_dir,'*_output.png')):
	# Read all the images using cv2. imread()
	# Store all the images into a list.
		print(filename)
		img = cv2.imread(filename)
		height, width, layers = img.shape
		size = (width,height)
		img_array.append(img)
	# Create a VideoWriter object using cv2. VideoWriter()
	out = cv2.VideoWriter('test.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
	# Save the images to video file using cv2. VideoWriter(). write()
	for i in range(len(img_array)):
		out.write(img_array[i])
	# Release the VideoWriter and destroy all windows.
	out.release()
	



 
