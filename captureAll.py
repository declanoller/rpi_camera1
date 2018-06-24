
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

#Create remote dir for images and prepare paths
startDateTimeString = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
remoteHost = "declan@TITTYWHISKERS88"
remotePath = "/home/declan/Documents/code/data/rpi_incoming/motion_detection_incoming/"
os.system("mkdir "+startDateTimeString)
#scpCommandDir = 'scp -r %s %s:%s' % (startDateTimeString, remoteHost, remotePath)
#os.system(scpCommandDir)
#os.system('rm -r ' + startDateTimeString)
#remotePath = remotePath + startDateTimeString


#Get CLI arguments for notes for a run
if len(sys.argv)>1:
	recordTime = float(sys.argv[1])
else:
	recordTime = 8

print("Starting to detect!")

startTime = time.time()

# capture frames from the camera
for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

	if time.time()-startTime>recordTime:
		break

	frame = f.array

	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)

	# draw the text and timestamp on the frame
	dateString = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
	cv2.putText(frame, dateString, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

	ext = ".jpg"
	tempPicName = dateString + ext
	cv2.imwrite(startDateTimeString+'/'+tempPicName,frame)

	rawCapture.truncate(0)

print('capture done.')


print('sending directory...\n')
scpCommandDir = 'scp -r %s %s:%s' % (startDateTimeString, remoteHost, remotePath)
os.system(scpCommandDir)
time.sleep(2)
print('deleting dir...\n')
rmCommand = 'rm -r ' + startDateTimeString
os.system(rmCommand)
print('done!')



#
