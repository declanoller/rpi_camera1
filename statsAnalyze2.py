
import matplotlib.pyplot as plt
from os import sys
import os
import pandas as pd
from tabulate import tabulate
import numpy as np
import subprocess
import seaborn as sns
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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


#Check if CSV pandas file exists
csvFileName = dir+'/'+runDate+'.csv'
CSVexists = os.path.exists(csvFileName)

if not CSVexists:
    print("no pandas cvs file, exiting.")
    exit(0)

#Get data from CSV and files that have already been processed
df = pd.read_csv(csvFileName,delimiter='\t')
print('\nCSV file:')
print(tabulate(df.head(), headers=df.columns.values, tablefmt='psql'))



df['Time'] = df['DateTime'].apply(lambda x: datetime.strptime(x[:-2], '%Y-%m-%d_%H-%M-%S.%f'))


certThresh = 0.5
detected = df[df['Certainty']>=certThresh]
not_detected = df[df['Certainty']<certThresh]

fig, ax = plt.subplots(3,1)
fig.set_size_inches(8,8)
ax[0].hist(mdates.date2num(df['Time'].tolist()), bins=50, color='lightblue')
ax[1].hist(mdates.date2num(detected['Time'].tolist()), bins=50, color='lightcoral')
ax[2].hist(mdates.date2num(not_detected['Time'].tolist()), bins=50, color='palegreen')
#plt.margins(0.2)

bottom_plot = 2
ax[0].set_xticks([])
ax[1].set_xticks([])
ax[bottom_plot].xaxis.set_major_locator(mdates.MinuteLocator())
ax[bottom_plot].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.setp(ax[bottom_plot].xaxis.get_majorticklabels(), rotation='vertical' )
plt.subplots_adjust(bottom=0.2)

plt.savefig(dir+'/'+'timehist_all_detected_notdet_'+runDate+'.png')
plt.show()




exit(0)













'''fig, ax = plt.subplots(1,1)
ax.hist(mdates.date2num(df['Time'].tolist()), bins=50, color='lightblue')
ax.xaxis.set_major_locator(mdates.MinuteLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.setp(ax.xaxis.get_majorticklabels(), rotation='vertical' )
#plt.margins(0.2)
plt.subplots_adjust(bottom=0.2)
plt.savefig(dir+'/'+'timehist_'+runDate+'.png')
plt.show()



certThresh = 0.5
detected = df[df['Certainty']>=certThresh]


fig, ax = plt.subplots(1,1)
ax.hist(mdates.date2num(detected['Time'].tolist()), bins=50, color='lightcoral')
ax.xaxis.set_major_locator(mdates.MinuteLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.setp(ax.xaxis.get_majorticklabels(), rotation='vertical' )
#plt.margins(0.2)
plt.subplots_adjust(bottom=0.2)
plt.savefig(dir+'/'+'timehist_detected_'+runDate+'.png')
plt.show()'''




exit(0)





























#
