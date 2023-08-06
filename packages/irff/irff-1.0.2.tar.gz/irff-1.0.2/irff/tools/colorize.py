#!/usr/bin/env python
# coding: utf-8
from tensorflow.keras.layers import Conv2D, UpSampling2D, InputLayer, Conv2DTranspose
from tensorflow.keras.layers import Activation, Dense, Dropout, Flatten
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from skimage.color import rgb2lab, lab2rgb, rgb2gray, xyz2lab
from skimage.io import imsave
import numpy as np
import os
import random
import tensorflow as tf
import matplotlib.pyplot as plt
# %matplotlib inline 
# Using TensorFlow backend.# Get images
image1 = img_to_array(load_img('000140.png')) 
image1 = np.array(image1, dtype=float) 

image2 = img_to_array(load_img('头像.jpg')) 
image2 = np.array(image2, dtype=float) 

X = rgb2lab(1.0/255*image1)[:,:,0] 
Y = rgb2lab(1.0/255*image2)[:,:,1:] 
# print(X.shape,Y.shape)
s = X.shape[0]
Y /= 128
X = X.reshape(1, s,s, 1) 
Y = Y.reshape(1, s,s, 2)

# Building the neural network
model = Sequential() 
model.add(InputLayer(input_shape=(None, None, 1))) 
model.add(Conv2D(8, (3, 3), activation='relu', padding='same', strides=2)) 
model.add(Conv2D(8, (3, 3), activation='relu', padding='same')) 
model.add(Conv2D(16, (3, 3), activation='relu', padding='same')) 
model.add(Conv2D(16, (3, 3), activation='relu', padding='same', strides=2)) 
model.add(Conv2D(32, (3, 3), activation='relu', padding='same')) 
model.add(Conv2D(32, (3, 3), activation='relu', padding='same', strides=2)) 
model.add(UpSampling2D((2, 2))) 
model.add(Conv2D(32, (3, 3), activation='relu', padding='same')) 
model.add(UpSampling2D((2, 2))) 
model.add(Conv2D(16, (3, 3), activation='relu', padding='same')) 
model.add(UpSampling2D((2, 2))) 
model.add(Conv2D(2, (3, 3), activation='tanh', padding='same'))

# Finish model
model.compile(optimizer='rmsprop', loss='mse') 
model.fit(x=X, y=Y, batch_size=1, epochs=1000)
print(model.evaluate(X, Y, batch_size=1)) 
output = model.predict(X) 
output *= 128# Output 
colorizationscur = np.zeros((400, 400, 3)) 
cur[:,:,0] = X[0][:,:,0] 
cur[:,:,1:] = output[0] 
imsave("img_result.png", lab2rgb(cur)) 
imsave("img_gray_version.png", rgb2gray(lab2rgb(cur)))



# 可视化数据集  
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
img = lab2rgb(cur) 
title = '黑白照片自动着色的神经网络-Alpha版'
plt.imshow(img) 
plt.title(title)
plt.show()



