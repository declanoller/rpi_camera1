import multiprocessing
import time

def myfunction(i, event):
    while not event.is_set():
        print(i)
        time.sleep(.5)
        if i>6:
            event.set()
        i += 1


if __name__ == "__main__":
    p= multiprocessing.Pool(10)
    m = multiprocessing.Manager()
    event = m.Event()
    for i in range(4):
        p.apply_async(myfunction , (i, event))
    print('meow')

    event.wait()  # We'll block here until a worker calls `event.set()`

    exit(0)

    #p.close()

    p.terminate() # Terminate all processes in the Pool
