from time import sleep
import sys


print('should increase:')

for i in range(10):
    sys.stdout.write('\r'+str(i)+'\n')
    sys.stdout.write('\r'+str(i**2))

    sys.stdout.flush()
    sleep(.5)



print('\n\n\n')
