from keras.applications import VGG16
from keras.applications import imagenet_utils
from keras.preprocessing.image import load_img,img_to_array
import numpy as np
from myImgTools import myImgTools


inputShape = (224, 224)
preprocess = imagenet_utils.preprocess_input

path = '/home/declan/Documents/code/data/rpi_incoming/good_ones/2018-07-01_14-38-23_subset/'
#file = '2018-07-01_14-38-47.874_0.jpg'
#(x1,y1,x2,y2) = (93,77,293,201)

file = '2018-07-01_14-39-37.815_0.jpg'
(x1,y1,x2,y2) = (78,118,324,246)


it = myImgTools()
it.loadVGGmodel()

it.classifyVGG(path+file,(x1,y1,x2,y2))


exit(0)














#
