from os import sys
import os
from time import sleep
import datetime

def processFile(logFile,fName):
    dtString = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    print("Processed file "+fName+" at time "+dtString+"\n")
    f = open(logFile,'a')
    f.write("Processed file "+fName+" at time "+dtString+"\n")
    f.close()


if len(sys.argv)>1:
    dir = sys.argv[1]
    print(dir)


processedFiles = []

files = os.listdir(dir)
nFiles = len(files)

print("there are {} files in the directory.".format(nFiles))

logfile = "logfile.txt"

while True:
    sleep(.5)
    files = os.listdir(dir)
    if len(files)>nFiles:
        print("new files found")
        nFiles = len(files)
        print("this many files now:",nFiles)
        [processFile(logfile,file) for file in files if file not in processedFiles]
        [processedFiles.append(file) for file in files if file not in processedFiles]























exit(0)
