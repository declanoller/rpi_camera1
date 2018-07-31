from datetime import datetime
import time
import sys

from multiprocessing import Pool,Manager
import subprocess
from LogFile import LogFile
from DebugFile import DebugFile
from CameraTools import CameraTools
from FileTools import FileTools


def watchKB(event,stdin):
    print('start kb loop')
    while True:
        k = stdin.readline().strip()
        print(k)watchKB(event,stdin)
        if k=='q':
            print('you pressed q!')
            event.set()
            return(0)


#Get CLI arguments for notes for a run
if len(sys.argv)>1:
	notes = sys.argv[1]
else:
	notes = "no notes"

#Get event manager to close nicely
m = Manager()
close_event = m.Event()

ft = FileTools(notes,close_event)

lf = LogFile(ft)

df = DebugFile(ft)

ct = CameraTools(ft)


pool = Pool(processes=2)

p1 = pool.apply_async(ct.cameraStream,args=(ft,lf,df))
p2 = pool.apply_async(df.debugUpdateLoop)

timeout_hours = 10
timeout_s = timeout_hours*3600
print(p1.get(timeout=timeout_s))
print(p2.get(timeout=timeout_s))


watchKB(event,stdin)



#
