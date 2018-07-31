from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime
import imutils
import time
import cv2
import sys
from glob import glob
from multiprocessing import Pool
import subprocess
from LogFile import LogFile
from DebugFile import DebugFile

def debugFileSend(debugfile):
	file_send_period = 10
	while True:
		sec_count = int(datetime.now().strftime('%S'))
		if sec_count%file_send_period==0:
			debugfile.recordTempMemCPU()
			debugfile.writeToDebug('Sending Debug File from debug send loop\n')
			debugfile.sendDebugFile()
			time.sleep(1.0)


def processFile(fName,remoteHost,remotePath,debugfile):
	remoteHostPath = '{}:{}'.format(remoteHost,remotePath)
	debugfile.writeToDebug('Sending file '+fName)
	subprocess.check_call(['scp','-q',fName,remoteHostPath])
	debugfile.writeToDebug('Removing file '+fName)
	subprocess.check_call(['rm',fName])


def fileMonitor(localPath,remoteHost,remotePath,logfile,debugfile):
	print('entering filemonitor')
	#could it be that it gets difficult to search processed_files once it gets huge?
	processed_files = set([])
	remoteHostPath = '{}:{}'.format(remoteHost,remotePath)

	while True:
		files = glob(localPath+'/'+'*.jpg')
		if len(files)>0:
			debugfile.writeToDebug('Found '+str(len(files))+' new files, processing. processed_files is currently this long: ' + str(len(processed_files)) + '\n')
			for file in files:
				if file not in processed_files:
					processFile(file,remoteHost,remotePath,debugfile)
					processed_files.add(file)
					debugfile.writeToDebug('Sending Debug File from file monitor loop')
					debugfile.sendDebugFile()

			debugfile.writeToDebug('All files in this batch processed\n')
			debugfile.recordTempMemCPU()
			time.sleep(0.5)
			debugfile.writeToDebug('Sending Log File')
			logfile.sendLogFile()


def cameraStream(localPath,startDateTimeString,logfile,debugfile):

	#Conf stuff
	conf = {
		"min_upload_seconds" : 3.0,
		"min_motion_frames" : 8,
		"camera_warmup_time" : 2.5,
		"delta_thresh" : 45,
		"resolution" : [640, 480],
		"fps" : 16,
		"min_area" : 2500,
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
	print("Starting to detect!")
	debugfile.writeToDebug('Starting to detect images')

	# capture frames from the camera
	for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

		occupied = False

		frame = f.array
		timestamp = datetime.now()

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

		frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))


		# threshold the delta image, dilate the thresholded image to fill
		# in holes, then find contours on thresholded image
		thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255, cv2.THRESH_BINARY)[1]
		thresh = cv2.dilate(thresh, None, iterations=conf["dil_iters"])
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if imutils.is_cv2() else cnts[1]

		dateString = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+"."+str(int(int(datetime.now().strftime("%f"))/1000.0))
		# loop over the contours
		boxCounter = 0
		for c in cnts:
			# if the contour is too small, ignore it
			if cv2.contourArea(c) < conf["min_area"]:
				continue

			#This is so it only draws it on a copy of frame for each box
			frameDraw = frame.copy()
			occupied = True
			# compute the bounding box for the contour, draw it on the frame,
			# and update the text
			(x, y, w, h) = cv2.boundingRect(c)
			print(dateString + ': ' + "Object detected in {}".format((x,y,w,h)))
			cv2.rectangle(frameDraw, (x, y), (x + w, y + h), (0, 255, 0), 2)
			# draw the text and timestamp on the frameDraw

			cv2.putText(frameDraw, dateString, (10, frameDraw.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

			ext = ".jpg"
			tempFName = dateString + '_' + str(boxCounter)
			tempPicName = tempFName + ext

			debugfile.writeToDebug('Saving image ' + tempPicName)
			cv2.imwrite(localPath + '/' + tempPicName,frameDraw)

			logfile.writeToLog("{}\t{}\t{}\t{}\t{}\n".format(tempFName,x,y,x + w,y + h))
			boxCounter += 1

		if not occupied:
			alpha = .5
			cv2.accumulateWeighted(gray, avg, alpha)


		rawCapture.truncate(0)



#Get CLI arguments for notes for a run
if len(sys.argv)>1:
	notes = sys.argv[1]
else:
	notes = "no notes"


startDateTimeString = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

remoteHost = "declan@TITTYWHISKERS88"
remotePath = "/home/declan/Documents/code/data/rpi_incoming/motion_detection_incoming/"

#Create remote dir for images and prepare paths
localPath = startDateTimeString
subprocess.check_call(['mkdir',localPath])
remoteHostPath = '{}:{}'.format(remoteHost,remotePath)
subprocess.check_call(['scp','-q','-r',startDateTimeString,remoteHostPath])
remotePath = remotePath + startDateTimeString

lf = LogFile(localPath,startDateTimeString,notes,remoteHost,remotePath)
df = DebugFile(localPath,startDateTimeString,notes,remoteHost,remotePath)
df.recordTempMemCPU()
df.sendDebugFile()

pool = Pool(processes=3)

p1 = pool.apply_async(fileMonitor,args=(localPath,remoteHost,remotePath,lf,df))
p2 = pool.apply_async(cameraStream,args=(localPath,startDateTimeString,lf,df))
p3 = pool.apply_async(debugFileSend,args=(df,))

timeout_hours = 10
timeout_s = timeout_hours*3600
print(p1.get(timeout=timeout_s))
print(p2.get(timeout=timeout_s))
print(p3.get(timeout=timeout_s))





#
