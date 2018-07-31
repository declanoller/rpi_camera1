
class Test1:

    def __init__(self,event):
        self.event = event

    def loop(self):
        i = 0
        print('starting loop')
        while True:
            i += 1
            if i%10000==0:
                print(i)
            if self.event.is_set():
                print('loop broken!')
                return(0)
