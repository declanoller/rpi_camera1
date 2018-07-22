
from os import sys
import os
from time import sleep
import datetime
import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate
from PIL import ImageFile,Image,ImageDraw
from math import ceil,floor



filename = '2018-07-01_14-42-14.362_1'+'.jpg'
(x1,y1,x2,y2) = (64,22,354,199)
outline_width = 3
box_bds = (x1+outline_width,y1+outline_width,x2-outline_width,y2-outline_width)

img = Image.open(filename)

img.show()


img = img.crop(box_bds)
print('img size is: ',img.size)
#img.show()

draw = ImageDraw.Draw(img)



min_dim = min(img.size)
max_dim = max(img.size)
print('max dim size is:',max_dim)

window_div = 3
window_div_width = ceil(max_dim/window_div)
print('div max dim by {} gives a window width of {}'.format(window_div,window_div_width))

window_width = min(min_dim,window_div_width)
print('window width: ',window_width)

N = 5
N_windows_max_dim = max(N,ceil(max_dim/window_width))
print('there will be this many window scans in the max dim',N_windows_max_dim)

stride = floor((max_dim-window_width)/(N_windows_max_dim-1))

N_windows_x = ceil(1 + (img.size[0]-window_width)/stride)
N_windows_y = ceil(1 + (img.size[1]-window_width)/stride)
print('there will be this many window scans in the x dim',N_windows_x)
print('there will be this many window scans in the y dim',N_windows_y)


for i in range(N_windows_x):
    for j in range(N_windows_y):
        x1 = i*stride
        y1 = j*stride
        x2 = x1 + window_width
        y2 = y1 + window_width

        if x2>img.size[0]:
            x2 = img.size[0]
            x1 = x2 - window_width
        if y2>img.size[1]:
            y2 = img.size[1]-2
            y1 = y2 - window_width


        draw.rectangle([x1,y1,x2,y2],outline=(255,0,0))
        print('({},{}): ({},{},{},{})'.format(i,j,x1,y1,x2,y2))

img.show()















#
