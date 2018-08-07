from glob import glob
from datetime import datetime
import subprocess




class FileTools:

	def __init__(self,notes,close_event):

		#Filenames
		self.start_dt_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
		self.remote_host = "declan@TITTYWHISKERS88"
		self.remote_base_path = "/home/declan/Documents/code/data/rpi_incoming/motion_detection_incoming/"
		self.remote_host_path = '{}:{}'.format(self.remote_host,self.remote_base_path)
		self.mount_point = 'mntpt'

		#Create remote dir for images and prepare paths
		print('creating local mount point dir', self.mount_point)
		subprocess.check_call(['mkdir','-p',self.mount_point])
		print('mounting remote directory', self.remote_host_path)
		subprocess.check_call(['sshfs',self.remote_host_path, self.mount_point])

		self.local_path = self.mount_point + '/' + self.start_dt_string
		print('creating remote/mounted dir', self.local_path)
		subprocess.check_call(['mkdir',self.local_path])

		self.notes = notes
		self.close_event = close_event


	def unmountFS(self):
		print('unmounting remote directory', self.remote_base_path)
		subprocess.check_call(['fusermount','-u',self.mount_point])
		print('done!')













#
