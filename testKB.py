from Test1 import Test1
from Test2 import Test2
import multiprocessing
import sys
import os


def watchKB(event,stdin):
    print('start kb loop')
    while True:
        k = stdin.readline().strip()
        print(k)
        if k=='q':
            print('you pressed q!')
            event.set()
            return(0)


if __name__ == '__main__':

    
    m = multiprocessing.Manager()
    event = m.Event()

    print(sys.stdin)
    newstdin = os.fdopen(os.dup(sys.stdin.fileno()))
    print(newstdin)
    #t1 = Test1()
    t1 = Test1(event)
    t2 = Test2()


    pool = multiprocessing.Pool(processes=2)
    #p1 = pool.apply_async(t1.loop,args=(event,))
    p1 = pool.apply_async(t1.loop)
    #p2 = pool.apply_async(t2.watchKB,args=(event,sys.stdin))
    #p2 = pool.apply_async(t2.watchKB,args=(event,sys.stdin))

    watchKB(event,sys.stdin)
    #watchKB(event,newstdin)

    print(p1.get(timeout=1000))
    #print(p2.get(timeout=1000))


    exit(0)
