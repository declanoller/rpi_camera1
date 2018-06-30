import glob
import os
import sys
import datetime


if len(sys.argv)>1:
	picPath = sys.argv[1]
else:
	print('need path to analyze')
	exit(0)

dateString = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

gif_name = "gif_" + dateString
ext = ".jpg"
file_list = glob.glob(picPath + '/' + '*' + ext) # Get all the pngs in the current directory
#list.sort(file_list, key=lambda x: int(x.split('_')[1].split('.png')[0])) # Sort the images by #, this may need to be tweaked for your use case
list.sort(file_list) # Sort the images by #, this may need to be tweaked for your use case
print(file_list)
with open('image_list.txt', 'w') as file:
    for item in file_list:
        file.write("%s\n" % item)

os.system('convert @image_list.txt {}/{}.gif'.format(picPath,gif_name)) # On windows convert is 'magick'
