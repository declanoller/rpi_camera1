
import subprocess


def fn():
    print('hiiiii')
    subprocess.check_call(['sleep','3'])
    return(5)



fn()

print('done!')
