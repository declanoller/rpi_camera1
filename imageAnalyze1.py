from os import sys
import os
from time import sleep
import datetime
from queue import Queue as Q
import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate
import numpy as np
import keras
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

global model
global dir




def classifyImage(fName,coords):

    (x1,y1,x2,y2) = coords

    #This is to get rid of the green box
    boxThickness = 3
    (x1,y1,x2,y2) = (x1+boxThickness,y1+boxThickness,x2-boxThickness,y2-boxThickness)

    global model
    global dir
    img = keras.preprocessing.image.load_img(fName)
    img = img.crop((x1,y1,x2,y2))
    imgSize = (32,32)
    img = img.resize(imgSize)

    imgArray = np.array([keras.preprocessing.image.img_to_array(img)])
    imgArrayNormed = imgArray.astype('float32')/255.0
    return('car',round(model.predict([imgArrayNormed])[0][0],5))

#Load model
print('\n\nloading model...')
model = keras.models.load_model('/home/declan/Documents/code/ML and DS/keras1'+'/'+'CIFAR-10-model_CAR.h5')
print('done!\n')


#CLI arguments
if len(sys.argv)>1:
    dir = sys.argv[1]
    #print(dir)
else:
    print("provide path")
    exit(0)

print(os.path.split(dir))
runDate = os.path.split(dir)[-1]
print(runDate)

#Check if log file exists, if not, quit
logFileName = dir+'/Log_'+runDate+'.txt'
if not os.path.exists(logFileName):
    print("no log file, exiting.")
    exit(0)

#Check if CSV pandas file exists, if not, create one
csvFileName = dir+'/'+runDate+'.csv'
CSVexists = os.path.exists(csvFileName)
print("csv exists:",CSVexists)

if not CSVexists:
    print("no pandas cvs file, creating one.")
    csvFile = open(csvFileName,'w+')
    csvFile.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format("DateTime","x1","y1","x2","y2","Object","Certainty"))
    csvFile.close()


#csvFile = open(csvFileName,'a')

#Get data from CSV and files that have already been processed
df = pd.read_csv(csvFileName,delimiter='\t')
print('\nCSV file:')
print(tabulate(df.head(), headers=df.columns.values, tablefmt='psql'))
processedFiles = set(df["DateTime"].values.tolist())
print('this many values in CSV:',len(processedFiles))
checked_unprocessed = set([])

#Create queue for files to be processed
q = Q()

print('\nLog file:')
log_df = pd.read_csv(logFileName,delimiter='\t',skiprows=1)
print(tabulate(log_df.head(), headers=log_df.columns.values, tablefmt='psql'))
logDates = log_df["DateTime"].values.tolist()
print('this many values in log file:',len(logDates))

print('\nWaiting for new files...\n')
while True:
    #Read in log file
    log_df = pd.read_csv(logFileName,delimiter='\t',skiprows=1)
    logDates = log_df["DateTime"].values.tolist()

    if len(logDates)>(len(processedFiles)+len(checked_unprocessed)):
        print('{} file(s) to be processed'.format(len(logDates)-len(processedFiles)))
        [q.put(date) for date in logDates if not date in processedFiles]


        while not q.empty():
            date = q.get()
            #print("\ndate:",date)
            tempdf = log_df.loc[log_df["DateTime"]==date]

            coords = tempdf[['x1','y1','x2','y2']].values[0]

            print('analyzing image',date+'.jpg'+' at coords '+str(coords))
            #Analyze with keras
            imgFileName = dir+'/'+date+'.jpg'
            if os.path.exists(imgFileName):
                obj,cert = classifyImage(imgFileName,coords)

                print('detected '+obj+' with certainty '+str(cert))

                df = df.append(tempdf)

                df.loc[df['DateTime']==date,'Object'] = obj
                df.loc[df['DateTime']==date,'Certainty'] = str(round(cert,5))

                df.to_csv(csvFileName,sep="\t",index=False)
                processedFiles.add(date)
                
            else:
                if date not in checked_unprocessed:
                    print('image not found yet, putting back on the queue')
                    q.put(date)
                    checked_unprocessed.add(date)
                    continue


        print('\nWaiting for new files...\n')

    sleep(1.0)













exit(0)
