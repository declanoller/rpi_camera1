from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime
import imutils
import time
import cv2


class CameraTools:


	def __init__(self,file_tool):

		#Conf stuff
		self.conf = {
			"min_upload_seconds" : 3.0,
			"min_motion_frames" : 8,
			"camera_warmup_time" : 2.5,
			"delta_thresh" : 45,
			"resolution" : [640, 480],
			"fps" : 16,
			"min_area" : 2500,
			"dil_iters" : 20
		}


		self.local_path = file_tool.local_path
		self.img_ext = '.jpg'

		self.close_event = file_tool.close_event


	def cameraStream(self,file_tool,logfile,debugfile):

		# initialize the camera and grab a reference to the raw camera capture
		camera = PiCamera()
		camera.resolution = tuple(self.conf["resolution"])
		camera.framerate = self.conf["fps"]
		rawCapture = PiRGBArray(camera, size=camera.resolution)

		# allow the camera to warmup, then initialize the average frame, last uploaded timestamp, and frame motion counter
		print("[INFO] warming up...")
		time.sleep(self.conf["camera_warmup_time"])
		avg = None

		print("Starting to detect!")
		debugfile.writeToDebug('Starting to detect images')

		# capture frames from the camera
		for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

			occupied = False

			frame = f.array

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
			thresh = cv2.threshold(frameDelta, self.conf["delta_thresh"], 255, cv2.THRESH_BINARY)[1]
			thresh = cv2.dilate(thresh, None, iterations=self.conf["dil_iters"])
			cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			cnts = cnts[0] if imutils.is_cv2() else cnts[1]

			dt_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+"."+str(int(int(datetime.now().strftime("%f"))/1000.0))
			# loop over the contours
			boxCounter = 0
			for c in cnts:
				# if the contour is too small, ignore it
				if cv2.contourArea(c) < self.conf["min_area"]:
					continue

				#This is so it only draws it on a copy of frame for each box
				frameDraw = frame.copy()
				occupied = True

				# compute the bounding box for the contour, draw it on the frame, and update the text
				(x, y, w, h) = cv2.boundingRect(c)
				print(dt_string + ': ' + "Object detected in {}".format((x,y,w,h)))
				cv2.rectangle(frameDraw, (x, y), (x + w, y + h), (0, 255, 0), 2)

				# draw the text and timestamp on the frameDraw
				cv2.putText(frameDraw, dt_string, (10, frameDraw.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

				temp_fname = dt_string + '_' + str(boxCounter)
				temp_pic_fname = temp_fname + self.img_ext

				debugfile.writeToDebug('Saving image ' + temp_pic_fname)
				cv2.imwrite(self.local_path + '/' + temp_pic_fname,frameDraw)

				logfile.writeToLog("{}\t{}\t{}\t{}\t{}\n".format(temp_fname,x,y,x + w,y + h))
				boxCounter += 1



			if not occupied:
				alpha = .5
				cv2.accumulateWeighted(gray, avg, alpha)

			if self.close_event.is_set():
				debugfile.writeToDebug('Close event triggered, exiting camera loop')
				time.sleep(0.5)
				file_tool.unmountFS()
				return(0)

			rawCapture.truncate(0)









#
