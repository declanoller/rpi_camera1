from datetime import datetime
import psutil
import subprocess


class DebugFile:


    def __init__(self,file_tool):
        #Prepare debug file
        self.debug_fname = 'Debug_' + file_tool.start_dt_string + '.txt'
        self.local_path = file_tool.local_path
        self.full_path_name = self.local_path + '/' + self.debug_fname
        self.notes = file_tool.notes

        self.close_event = file_tool.close_event

        fDebug = open(self.full_path_name,'w+')
        fDebug.write('Run notes: ' + self.notes + '\n\n\n')
        fDebug.close()



    def writeToDebug(self,write_string):
        fDebug = open(self.full_path_name,'a')
        dateString = datetime.now().strftime("[%H:%M:%S") + '.' + str(int(int(datetime.now().strftime("%f"))/1000.0))+datetime.now().strftime("   %Y-%m-%d]")
        fDebug.write(dateString + '\t' + write_string + '\n')
        fDebug.close()


    def recordTempMemCPU(self):
        CPU_str = 'CPU=' + str(psutil.cpu_percent())
        mem_str = 'Mem=' + str(psutil.virtual_memory()[2])

        temp_cmd = 'cat'
        temp_arg = '/sys/class/thermal/thermal_zone0/temp'
        temp_str = 'temp=' + str(int(subprocess.check_output([temp_cmd,temp_arg]))/1000.0)

        self.writeToDebug(CPU_str + ', ' + mem_str + ', ' + temp_str + '\n')


    def debugUpdateLoop(self):
    	self.file_send_period = 10
    	while not self.close_event.is_set():
    		sec_count = int(datetime.now().strftime('%S'))
    		if sec_count%self.file_send_period==0:
    			self.recordTempMemCPU()
    			self.writeToDebug('Sending Debug File from debug send loop\n')
    			#self.sendDebugFile()
    			time.sleep(1.0)

        self.writeToDebug('Close event triggered, exiting debug loop\n')










#
