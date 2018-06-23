import glob
import os
import datetime


dateString = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

gif_name = "gif_" + dateString
ext = ".jpg"
file_list = glob.glob('*' + ext) # Get all the pngs in the current directory
#list.sort(file_list, key=lambda x: int(x.split('_')[1].split('.png')[0])) # Sort the images by #, this may need to be tweaked for your use case
list.sort(file_list) # Sort the images by #, this may need to be tweaked for your use case

with open('image_list.txt', 'w') as file:
    for item in file_list:
        file.write("%s\n" % item)

os.system('convert @image_list.txt {}.gif'.format(gif_name)) # On windows convert is 'magick'
