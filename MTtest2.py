from multiprocessing import Pool
#import threading
#import datetime
from time import sleep
import os
import sys
import signal

def f1():
    for i in range(5):
        sleep(.1)
        print("f1:",i)
    print("f1 exiting")
    return('f1f1f1f1f1f1f1')

def f2():
    for i in range(10):
        sleep(.1)
        print("f2:",i)
    print("f2 exiting")
    return('f2f2f2ff2f2f2f2f2f')



pool = Pool(processes=2)

p1 = pool.apply_async(f1)

p2 = pool.apply_async(f2)

print(p1.get(timeout=10))

print(p2.get(timeout=10))

print('\n\n\ndone')

p1 = pool.apply_async(f1)

p2 = pool.apply_async(f2)
print(p1.get(timeout=10))

print(p2.get(timeout=10))
