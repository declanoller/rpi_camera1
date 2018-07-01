
import matplotlib.pyplot as plt
from os import sys
import os
import pandas as pd
from tabulate import tabulate
import numpy as np
import subprocess
import seaborn as sns



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


sns.distplot(df[['Certainty']],kde=False,axlabel='Certainty')
plt.ylim((0,100))

plt.show()




























#
