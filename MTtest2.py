from multiprocessing import Pool
#import threading
#import datetime
from time import sleep
import os
import sys
import signal

def f1():
    for i in range(10):
        sleep(.1)
        print("f1:",i)
    print("f1 exiting")
    os.kill(os.getpid(), signal.SIGINT)

def f2():
    for i in range(20):
        sleep(.1)
        print("f2:",i)
    print("f2 exiting")
    return(0)



pool = Pool(processes=2)

p1 = pool.apply_async(f1)

p2 = pool.apply_async(f2)

print(p1.get(timeout=10))

print(p2.get(timeout=10))
