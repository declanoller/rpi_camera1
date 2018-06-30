from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import warnings
import datetime
import imutils
import time
import cv2
import os
import sys
from glob import glob
from multiprocessing import Pool



def processFile(fName,remoteHost,remotePath):
	scpCommandImg = ("scp {} {}:{}".format(fName,remoteHost,remotePath))
	os.system(scpCommandImg)
	rmCommand = 'rm ' + fName
	os.system(rmCommand)


def fileMonitor(logFileName,localPath,remoteHost,remotePath):
	print("entering filemonitor")
	processedFiles = []

	while True:
		#files = os.listdir(dir)
		files = glob(localPath+'/'+'*.jpg')
		if len(files)>0:
			print("sending these files:",files)
			[processFile(file,remoteHost,remotePath) for file in files if file not in processedFiles]
			[processedFiles.append(file) for file in files if file not in processedFiles]
			scpCommandLog = 'scp %s %s:%s' % (logFileName, remoteHost, remotePath)
			os.system(scpCommandLog)


def cameraStream(logFileName,localPath,startDateTimeString):


	#Conf stuff
	conf = {
		"min_upload_seconds" : 3.0,
		"min_motion_frames" : 8,
		"camera_warmup_time" : 2.5,
		"delta_thresh" : 45,
		"resolution" : [640, 480],
		"fps" : 16,
		"min_area" : 1500,
		"dil_iters" : 20
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

	print("Starting to detect!")

	# capture frames from the camera
	for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

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

		alpha = .5
		frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))


		# threshold the delta image, dilate the thresholded image to fill
		# in holes, then find contours on thresholded image
		thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255,
			cv2.THRESH_BINARY)[1]
		thresh = cv2.dilate(thresh, None, iterations=conf["dil_iters"])
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if imutils.is_cv2() else cnts[1]

		# loop over the contours
		for i,c in enumerate(cnts):
			# if the contour is too small, ignore it
			if cv2.contourArea(c) < conf["min_area"]:
				continue

			occupied = True
			# compute the bounding box for the contour, draw it on the frame,
			# and update the text
			print("Object detected!")
			(x, y, w, h) = cv2.boundingRect(c)
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

			# draw the text and timestamp on the frame
			#dateString = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
			dateString = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+"."+str(int(int(datetime.now().strftime("%f"))/1000.0))

			#ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
			#cv2.putText(frame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
			cv2.putText(frame, dateString, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

			ext = ".jpg"
			tempPicName = dateString + '_' + str(i) + ext
			cv2.imwrite(localPath + '/' + tempPicName,frame)

			fLog = open(logFileName,'a')
			fLog.write("{}\t{}\t{}\t{}\t{}\n".format(dateString,x,y,x + w,y + h))
			fLog.close()



		if not occupied:
			cv2.accumulateWeighted(gray, avg, alpha)


		rawCapture.truncate(0)



#Get CLI arguments for notes for a run
if len(sys.argv)>1:
	notes = sys.argv[1]
else:
	notes = "no notes"


startDateTimeString = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

remoteHost = "declan@TITTYWHISKERS88"
remotePath = "/home/declan/Documents/code/data/rpi_incoming/motion_detection_incoming/"

#Create remote dir for images and prepare paths
localPath = startDateTimeString
os.system("mkdir "+localPath)
scpCommandDir = 'scp -r %s %s:%s' % (startDateTimeString, remoteHost, remotePath)
os.system(scpCommandDir)
remotePath = remotePath + startDateTimeString

#Prepare log file
logFileName = "Log_" + startDateTimeString + '.txt'
fLog = open(localPath + '/' + logFileName,'w')
fLog.write("Run notes: " + notes + "\n")
fLog.write("{}\t{}\t{}\t{}\t{}\n".format("DateTime","x1","y1","x2","y2"))
fLog.close()


pool = Pool(processes=2)

p1 = pool.apply_async(fileMonitor,args=(logFileName,localPath,remoteHost,remotePath))

p2 = pool.apply_async(cameraStream,args=(logFileName,localPath,startDateTimeString))


print(p1.get(timeout=1800))

print(p2.get(timeout=1800))

'''print(p1.get(timeout=None))

print(p2.get(timeout=None))'''











#
