class Test2:

    def watchKB(self,event,stdin):
        print('start kb loop')
        while True:
            #k = stdin.readline().strip()
            k = 0
            print(k)
            if k=='q':
                print('you pressed q!')
                event.set()
                return(0)
