from os import sys
import os
import pandas as pd
from tabulate import tabulate
import numpy as np
import subprocess



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


#Check if CSV pandas file exists, if not, create one
csvFileName = dir+'/'+runDate+'.csv'
CSVexists = os.path.exists(csvFileName)

if not CSVexists:
    print("no pandas cvs file, exiting.")
    exit(0)


#csvFile = open(csvFileName,'a')

#Get data from CSV and files that have already been processed
df = pd.read_csv(csvFileName,delimiter='\t')
print('\nCSV file:')
print(tabulate(df.head(), headers=df.columns.values, tablefmt='psql'))

certThresh = 0.5
detected = df[df['Certainty']>=certThresh]
not_detected = df[df['Certainty']<certThresh]

print('\ndetected:')
print(tabulate(detected.head(), headers=detected.columns.values, tablefmt='psql'))
print('\nnot_detected:')
print(tabulate(not_detected.head(), headers=not_detected.columns.values, tablefmt='psql'))

print('deleting old dirs...')
subprocess.check_call(['rm', '-rf',dir+'/'+'detected'])
subprocess.check_call(['rm', '-rf',dir+'/'+'not_detected'])
print('creating new dirs...')
subprocess.check_call(['mkdir',dir+'/'+'detected'])
subprocess.check_call(['mkdir',dir+'/'+'not_detected'])

detected_files = [f+'.jpg' for f in detected['DateTime'].values.tolist()]
not_detected_files = [f+'.jpg' for f in not_detected['DateTime'].values.tolist()]


print('copying files...')
[subprocess.check_call(['cp', dir+'/'+f,dir+'/'+'detected'+'/'+f]) for f in detected_files]
[subprocess.check_call(['cp', dir+'/'+f,dir+'/'+'not_detected'+'/'+f]) for f in not_detected_files]




















exit(0)
