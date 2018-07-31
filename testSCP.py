import subprocess
from time import time




files = ['smallfile.txt','mediumfile.txt','bigfile.txt']
#files = ['smallfile.txt']

remoteHostPath = 'declan@declan-ASSBOT:~/Documents/code/data/test_incoming'
times = []
#for file in files:
for i in range(10):
    file = files[0]
    print('processing file',file)
    start = time()
    #subprocess.check_call(['scp','-c','aes128-gcm@openssh.com',file,remoteHostPath])
    #subprocess.check_call(['rcp',file,remoteHostPath])
    subprocess.check_call(['cp',file,'./mntpt/'])
    total = time()-start
    print('time elapsed:',total)
    times.append(total)


print('done')
print(times)






#
