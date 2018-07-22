from keras.applications import VGG16
from keras.applications import imagenet_utils
from keras.preprocessing.image import load_img,img_to_array

from PIL import ImageFile
from math import ceil,floor

import warnings
import numpy as np

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=FutureWarning)
    import keras


class myImgTools:


    def loadKerasModel(self,fName):
        #Load model
        print('\n\nloading keras model...')
        self.keras_model = keras.models.load_model(fName)
        print('done!\n')


    def loadVGGmodel(self):
        print('loading model')
        self.VGG_model = VGG16(weights="imagenet")
        print('loaded')
        self.inputShape = (224, 224)
        self.car_indices = [407, 436, 468, 511, 609, 627, 656, 661, 751, 817]


    def classifyVGG(self,fname,coords):

        img = load_img(fname)

        #crop to square, resize, to array, increase dim
        img = self.cropToSquare(img,coords)
        img = img.resize(self.inputShape)
        img = img_to_array(img)
        img_array = np.expand_dims(img,axis=0)

        img = imagenet_utils.preprocess_input(img_array)

        print('predicting')
        pred = self.VGG_model.predict(img)
        print('predicted')

        car_types = [pred[0][i] for i in self.car_indices]

        total_pred = sum(car_types)*100

        P = imagenet_utils.decode_predictions(pred)
        print(P)
        for (i, (imagenetID, label, prob)) in enumerate(P[0]):
            print("{}. {}: {:.2f}%".format(i + 1, label, prob * 100))

        return(total_pred)


    def cropToSquare(self,img,coords):

        (x1,y1,x2,y2) = coords

        boxThickness = 3
        (x1,y1,x2,y2) = (x1+boxThickness,y1+boxThickness,x2-boxThickness,y2-boxThickness)

        #print('orig box',(x1,y1,x2,y2))

        xdim = x2-x1
        ydim = y2-y1
        #print(xdim,ydim)

        if xdim>ydim:
            #print('xdim bigger')
            extra = xdim-ydim
            padding = extra/2.0
            #print('padding',padding)
            car_area = (x1,max(0,y1-padding),x2,min(img.size[1],y2+padding))
        else:
            #print('ydim bigger')
            extra = ydim-xdim
            padding = extra/2.0
            car_area = (max(0,x1-padding),y1,min(img.size[0],x2+padding),y2)

        img = img.crop(car_area)
        return(img)




    def getWindows(self,img,window_div):
        min_dim = min(img.size)
        max_dim = max(img.size)

        #This is the size of the window in terms of a fraction of the image max dim size.
        #window_div = 3
        window_div_width = ceil(max_dim/window_div)

        window_width = min(min_dim,window_div_width)

        N = 10
        N_windows_max_dim = max(N,ceil(max_dim/window_width))

        stride = floor((max_dim-window_width)/(N_windows_max_dim-1))

        N_windows_x = ceil(1 + (img.size[0]-window_width)/stride)
        N_windows_y = ceil(1 + (img.size[1]-window_width)/stride)

        sub_imgs = []

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

                sub_imgs.append((x1,y1,x2,y2))
        return(sub_imgs)



    def classifyImage(self,fName,coords):

        (x1,y1,x2,y2) = coords

        #This is to get rid of the green box
        boxThickness = 3
        (x1,y1,x2,y2) = (x1+boxThickness,y1+boxThickness,x2-boxThickness,y2-boxThickness)

        img = keras.preprocessing.image.load_img(fName)
        img = img.crop((x1,y1,x2,y2))
        imgSize = (32,32)
        img = img.resize(imgSize)

        imgArray = np.array([keras.preprocessing.image.img_to_array(img)])
        imgArrayNormed = imgArray.astype('float32')/255.0
        return('car',round(self.keras_model.predict([imgArrayNormed])[0][0],5))



    def classifyImageSlidingWindows(self,fName,coords):

        (x1,y1,x2,y2) = coords

        #This is to get rid of the green box
        boxThickness = 3
        (x1,y1,x2,y2) = (x1+boxThickness,y1+boxThickness,x2-boxThickness,y2-boxThickness)

        img = keras.preprocessing.image.load_img(fName)
        img = img.crop((x1,y1,x2,y2))
        imgSize = (32,32)

        sub_windows = getWindows(img,1.5)+getWindows(img,2)
        certs = []
        for window in sub_windows:
            sub_img = img.crop(window)
            sub_img = sub_img.resize(imgSize)
            imgArray = np.array([keras.preprocessing.image.img_to_array(sub_img)])
            imgArrayNormed = imgArray.astype('float32')/255.0
            cert = round(self.keras_model.predict([imgArrayNormed])[0][0],5)
            certs.append(cert)

        max_cert = max(certs)
        return('car',max_cert)
