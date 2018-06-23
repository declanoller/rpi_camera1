import os
import datetime


dateString = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

ext = ".jpg"
tempPicName = dateString + ext
print(tempPicName)

takePicCommand = "fswebcam --input 0 --resolution \'1280x960\' %s"%tempPicName
print(takePicCommand)

remoteHost = "declan@TITTYWHISKERS88"
remotePath = "~/Documents/code/data/rpi_incoming/"
#scpCommand = 'scp "%s" "%s:%s"' % (tempPicName, remoteHost, remotePath)
scpCommand = 'scp %s %s:%s' % (tempPicName, remoteHost, remotePath)
print(scpCommand)

#exit(0)

os.system(takePicCommand)

os.system(scpCommand)
