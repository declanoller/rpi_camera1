from multiprocessing import Pool, Value
import datetime
from time import sleep
import os

def processFile(fName):
    dtString = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    print("Processed file "+fName+" at time "+dtString+"\n")

def fileMonitor(dir):
    print("entering filemonitor")
    processedFiles = []

    files = os.listdir(dir)
    nFiles = len(files)

    print("there are {} files in the directory.".format(nFiles))

    while True:
        sleep(.5)
        files = os.listdir(dir)
        if len(files)>nFiles:
            print("new files found")
            nFiles = len(files)
            print("this many files now:",nFiles)
            [processFile(file) for file in files if file not in processedFiles]
            [processedFiles.append(file) for file in files if file not in processedFiles]



def fileSaver(path):
    print("entering filesaver")
    while True:
        sleep(3)
        dtString = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        fName = path+"/"+dtString+".txt"
        print("created new file "+fName+" at time "+dtString+"\n")
        f = open(fName,'w')
        f.write("created new file "+fName+" at time "+dtString+"\n")
        f.close()


if len(os.sys.argv)>1:
    dir = os.sys.argv[1]
    print(dir)
    print(len(dir))
    print(len((str(dir),)))

pool = Pool(processes=2)

p1 = pool.apply_async(fileMonitor,args=(dir,))

p2 = pool.apply_async(fileSaver,args=(dir,))

print(p1.get(timeout=30))

print(p2.get(timeout=30))
