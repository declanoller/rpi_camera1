from os import sys
import os
import sys
from time import sleep
import datetime
from queue import Queue as Q
import pandas as pd
from tabulate import tabulate
ImageFile.LOAD_TRUNCATED_IMAGES = True
import warnings
from myImgTools import myImgTools




model_path = '/home/declan/Documents/code/ML and DS/keras1'+'/'+'CIFAR-10-model_CAR.h5'

it = myImgTools()
it.loadKerasModel(model_path)

#CLI arguments
if len(sys.argv)>1:
    dir = sys.argv[1]
else:
    print("provide path")
    exit(0)


runDate = os.path.split(dir)[-1]

#Check if log file exists, if not, quit
logFileName = dir+'/Log_'+runDate+'.txt'
if not os.path.exists(logFileName):
    print("no log file, exiting.")
    exit(0)

#Check if CSV pandas file exists, if not, create one
csvFileName = dir+'/'+runDate+'.csv'
CSVexists = os.path.exists(csvFileName)

if not CSVexists:
    print("no pandas cvs file, creating one.")
    csvFile = open(csvFileName,'w+')
    csvFile.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format("DateTime","x1","y1","x2","y2","Object","Certainty"))
    csvFile.close()




#Get data from CSV and files that have already been processed
df = pd.read_csv(csvFileName,delimiter='\t')
print('\nCSV file:')
print(tabulate(df.head(), headers=df.columns.values, tablefmt='psql'))
processedFiles = set(df["DateTime"].values.tolist())
print('this many values in CSV:',len(processedFiles),'\n\n')
checked_unprocessed = set([])

#Create queue for files to be processed
q = Q()
images_analyzed = 0

#Import log file, convert to pandas
print('\nLog file:')
log_df = pd.read_csv(logFileName,delimiter='\t',skiprows=1)
print(tabulate(log_df.head(), headers=log_df.columns.values, tablefmt='psql'))
logDates = log_df["DateTime"].values.tolist()
print('\nthis many values in log file:',len(logDates))



print('\nWaiting for new files...\n')
while True:
    #Read in log file
    log_df = pd.read_csv(logFileName,delimiter='\t',skiprows=1)
    logDates = log_df["DateTime"].values.tolist()

    if len(logDates)>(len(processedFiles)+len(checked_unprocessed)):
        print('{} file(s) to be processed \n\n'.format(len(logDates)-len(processedFiles)))
        [q.put(date) for date in logDates if not date in processedFiles]


        while not q.empty():
            date = q.get()
            #print("\ndate:",date)
            tempdf = log_df.loc[log_df["DateTime"]==date]

            coords = tempdf[['x1','y1','x2','y2']].values[0]

            pad_space = ' '*30
            sys.stdout.write('\r' + 'image #{}. Analyzing image {}.jpg at coords {}'.format(images_analyzed,date,coords) + pad_space)
            sys.stdout.flush()
            #print('analyzing image',date+'.jpg'+' at coords '+str(coords))
            #Analyze with keras
            imgFileName = dir+'/'+date+'.jpg'
            if os.path.exists(imgFileName):


                file_size = os.path.getsize(imgFileName)
                if file_size > 2000:

                    obj,cert = 'car',0.5
                    obj,cert = it.classifyImageSlidingWindows(imgFileName,coords)
                    #obj,cert = it.classifyImage(imgFileName,coords)

                    #print('detected '+obj+' with certainty '+str(cert))

                    df = df.append(tempdf)

                    df.loc[df['DateTime']==date,'Object'] = obj
                    df.loc[df['DateTime']==date,'Certainty'] = str(round(cert,5))

                    df.to_csv(csvFileName,sep="\t",index=False)

                else:
                    print('file is too small ({}), probably incomplete, not adding to csv'.format(file_size))

                processedFiles.add(date)
                images_analyzed += 1

            else:
                if date not in checked_unprocessed:
                    print('image not found yet, putting back on the queue')
                    q.put(date)
                    checked_unprocessed.add(date)
                    continue


        print('\nWaiting for new files...\n')

    sleep(1.0)













exit(0)
