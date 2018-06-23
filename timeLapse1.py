import os
import datetime
import time

ext = ".jpg"
remoteHost = "declan@TITTYWHISKERS88"
remotePath = "~/Documents/code/data/rpi_incoming/"

for i in range(120):

    dateString = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


    tempPicName = dateString + ext

    takePicCommand = "fswebcam --input 0 --resolution \'1280x960\' %s"%tempPicName
    scpCommand = 'scp %s %s:%s' % (tempPicName, remoteHost, remotePath)
    rmCommand = 'rm ' + tempPicName

    os.system(takePicCommand)
    os.system(scpCommand)
    time.sleep(.5)
    os.system(rmCommand)
    time.sleep(30)

exit(0)
