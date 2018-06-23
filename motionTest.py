
# import the necessary packages
#from pyimagesearch.tempimage import TempImage
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import warnings
import datetime
#import dropbox
import imutils
#import json
import time
import cv2
import os
import sys


conf = {
	"min_upload_seconds" : 3.0,
	"min_motion_frames" : 8,
	"camera_warmup_time" : 2.5,
	"delta_thresh" : 5,
	"resolution" : [640, 480],
	"fps" : 16,
	"min_area" : 5000
}

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = tuple(conf["resolution"])
camera.framerate = conf["fps"]
rawCapture = PiRGBArray(camera, size=tuple(conf["resolution"]))

# allow the camera to warmup, then initialize the average frame, last
# uploaded timestamp, and frame motion counter
print("[INFO] warming up...")
time.sleep(conf["camera_warmup_time"])
avg = None
lastUploaded = datetime.datetime.now()
motionCounter = 0

remoteHost = "declan@TITTYWHISKERS88"
remotePath = "/home/declan/Documents/code/data/rpi_incoming/motion_detection_incoming/"
#scpCommand = 'scp "%s" "%s:%s"' % (tempPicName, remoteHost, remotePath)

if len(sys.argv)>1:
	notes = sys.argv[1]
else:
	notes = "no notes"

startDateTimeString = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
logFileName = "Log_" + startDateTimeString + '.txt'
fLog = open(logFileName,'w')
fLog.write("Run notes: " + notes + "\n")
fLog.write("{}\t{}\t{}\t{}\t{}\n".format("DateTime","x1","y1","x2","y2"))
fLog.close()
fLog = open(logFileName,'a')


print("Starting to detect!")

# capture frames from the camera
for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image and initialize
	# the timestamp and occupied/unoccupied text

	occupied = False

	frame = f.array
	timestamp = datetime.datetime.now()
	text = "Unoccupied"

	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# if the average frame is None, initialize it
	if avg is None:
		print("[INFO] starting background model...")
		avg = gray.copy().astype("float")
		rawCapture.truncate(0)
		continue

	# accumulate the weighted average between the current frame and
	# previous frames, then compute the difference between the current
	# frame and running average
	alpha = .5
	#cv2.accumulateWeighted(gray, avg, alpha)
	frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))


	# threshold the delta image, dilate the thresholded image to fill
	# in holes, then find contours on thresholded image
	thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255,
		cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]

	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < conf["min_area"]:
			continue

		occupied = True
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		print("Object detected!")
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Occupied"

		# draw the text and timestamp on the frame
		dateString = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
		#ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
		#cv2.putText(frame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
		cv2.putText(frame, dateString, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

		ext = ".jpg"
		tempPicName = dateString + ext
		cv2.imwrite(tempPicName,frame)

		fLog.write("{}\t{}\t{}\t{}\t{}\n".format(dateString,x,y,x + w,y + h))


		scpCommandImg = 'scp %s %s:%s' % (tempPicName, remoteHost, remotePath)
		os.system(scpCommandImg)
		scpCommandLog = 'scp %s %s:%s' % (logFileName, remoteHost, remotePath)
		fLog.close()
		os.system(scpCommandLog)
		fLog = open(logFileName,'a')
		rmCommand = 'rm ' + tempPicName
		os.system(rmCommand)

	if not occupied:
		cv2.accumulateWeighted(gray, avg, alpha)


	rawCapture.truncate(0)
fLog.close()
