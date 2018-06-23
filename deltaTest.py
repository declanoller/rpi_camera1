#rom pyimagesearch.tempimage import TempImage
#from picamera.array import PiRGBArray
#from picamera import PiCamera
import argparse
import warnings
import datetime
#import dropbox
import imutils
import json
import time
import cv2
from PIL import Image
import numpy as np

def procImage(inImg):
    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(inImg, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    return(gray)


avg = None

path = "/home/declan/Documents/code/rpi_stuff/"
bg = Image.open(path + "static.jpg")
movement = Image.open(path + "movement.jpg")


orig_movement = np.array(movement)
orig_movement = imutils.resize(orig_movement, width=500)
timestamp = datetime.datetime.now()
text = "Unoccupied"

bg = procImage(np.array(bg))
movement = procImage(np.array(movement))


# accumulate the weighted average between the current frame and
# previous frames, then compute the difference between the current
# frame and running average

#bg = bg.astype("float32")
#cv2.accumulateWeighted(bg, bg, 0.5)
#frameDelta = cv2.absdiff(movement, bg)
frameDelta = cv2.absdiff(movement, cv2.convertScaleAbs(bg))
#Image.fromarray(frameDelta).show()
delta_thresh = 30
# threshold the delta image, dilate the thresholded image to fill
# in holes, then find contours on thresholded image

thresh = cv2.threshold(frameDelta, delta_thresh, 255,cv2.THRESH_BINARY)[1]
Image.fromarray(thresh).show()

thresh = cv2.dilate(thresh, None, iterations=2)
Image.fromarray(thresh).show()
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

min_area = 5000
# loop over the contours
for c in cnts:
	# if the contour is too small, ignore it
	if cv2.contourArea(c) < min_area:
		continue

	# compute the bounding box for the contour, draw it on the frame,
	# and update the text
	(x, y, w, h) = cv2.boundingRect(c)
	cv2.rectangle(orig_movement, (x, y), (x + w, y + h), (0, 255, 0), 2)
	text = "Occupied"



Image.fromarray(orig_movement).show()






exit(0)
