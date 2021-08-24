#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 22:50:21 2021

@author: atte
"""
#import tensorflow as tf
import os
import random
import numpy as np
from tqdm import tqdm 
from skimage.io import imread, imshow
from skimage.transform import resize
import matplotlib.pyplot as plt
seed = 42
np.random.seed = seed

# IMG_WIDTH = 128
# IMG_HEIGHT = 128
# IMG_CHANNELS = 3

# VAL_IMG_DIR = "/home/inf-54-2020/experimental_cop/Val_H_Final/Images/"
# X_test=[]
# sizes_test = []
# n3 = 0
# print('starting...')
# for root, subdirectories, files in tqdm(os.walk(VAL_IMG_DIR)): #tqdm shows the progress bar of the for loop
#     #print(root)
#     for subdirectory in subdirectories:
#     #    print(subdirectory)
#         file_path = os.path.join(root, subdirectory)
#       #   print(file_path)
#         for f in os.listdir(file_path):
#             if not f.endswith('.png'):
#                 continue
#             img_path=file_path + '/' + f   #create first of dic values, i.e the path
#             #print(img_path)
#             #imagename=ntpath.basename(imagepath)#take the name of the file from the path and save it
#             img = imread(img_path)[:,:,:IMG_CHANNELS]
#             sizes_test.append([img.shape[0], img.shape[1]])
#             img = resize(img, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)
#             X_test.append(img)
#             #print(' loop of X_test done!')
# X_test = np.array(X_test)
# print(X_test.shape)

# np.save('/home/inf-54-2020/experimental_cop/scripts/X_test_size128.npy', X_test)
X_test = np.load('/home/inf-54-2020/experimental_cop/scripts/kd_X_test_size244.npy')
#upload the numpy files as well as the saved model location
#X_train = np.load('/home/inf-54-2020/experimental_cop/scripts/X_train_size128_Unet.npy')
#Y_train = np.load('/home/inf-54-2020/experimental_cop/scripts/Y_train_size128_Unet.npy')
Y_train = np.load('/home/inf-54-2020/experimental_cop/scripts/kd_Y_train_size244.npy')
X_train = np.load('/home/inf-54-2020/experimental_cop/scripts/kd_X_train_size244.npy')
#X_test = np.load('/home/inf-54-2020/experimental_cop/scripts/X_test_size128_Unet.npy')

cp_save_path = "/home/inf-54-2020/experimental_cop/scripts/kaggle_model.h5"
from tensorflow import keras

model_segm = keras.models.load_model(cp_save_path)

#model = pickle.load(open(cp_save_path,"rb"))

#model = keras.models.load_model(cp_save_path)
#results = model_segm.predict(X_test, verbose=1)

#print(X_test.shape)
####################################
#idx = random.randint(0, len(X_train))
#print(len(X_train))


# preds_train = model_segm.predict(X_train[:int(X_train.shape[0]*0.9)], verbose=1)
# preds_val = model_segm.predict(X_train[int(X_train.shape[0]*0.9):], verbose=1)
# preds_test = model_segm.predict(X_test, verbose=1)

 
# preds_train_t = (preds_train > 0.5).astype(np.uint8)
# preds_val_t = (preds_val > 0.5).astype(np.uint8)
# preds_test_t = (preds_test > 0.5).astype(np.uint8)
#print(preds_train_t)

#print(preds_train_t.shape)

import PIL
from PIL import Image, ImageOps
import cv2
from keras.utils import normalize
im_path = "/home/inf-54-2020/experimental_cop/saved_images/reconstruction_Earlier_10x.jpg"

#try out by adding normalization too!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def prediction(model, image, patch_size):
    segm_img = np.zeros(image.shape[:2])  #Array with zeros to be filled with segmented values
    patch_num=1
    for i in range(0, image.shape[0], 128):   #Steps of 256
        for j in range(0, image.shape[1], 128):  #Steps of 256
            #print(i, j)
            single_patch = image[i:i+patch_size, j:j+patch_size]
            #single_patch_norm = np.expand_dims(normalize(np.array(single_patch), axis=1),2)
            single_patch_shape = single_patch.shape[:2]
            single_patch_input = np.expand_dims(single_patch, 0)
            single_patch_prediction = (model.predict(single_patch_input)[0,:,:,0]).astype(np.uint8)
            segm_img[i:i+single_patch_shape[0], j:j+single_patch_shape[1]] += cv2.resize(single_patch_prediction, single_patch_shape[::-1])
          
            print("Finished processing patch number ", patch_num, " at position ", i,j)
            patch_num+=1
    return segm_img
large_image = Image.open('/home/inf-54-2020/experimental_cop/YZ003_SD_#17_HuNu-DAB-Ni_hCOL1A1-VB_30_min_10X.tif')
large_image=np.array(large_image)
h = large_image.shape[1]
new_size = (h,h,3)
large_image = np.resize(large_image,new_size)
print(large_image.shape)
model_segm = keras.models.load_model(cp_save_path)

model_segm.load_weights(cp_save_path)
patch_size = 128
segmented_image = prediction(model_segm, large_image, patch_size)
plt.imsave('/home/inf-54-2020/experimental_cop/saved_images/reconstruction_Earlier_10x.jpg', segmented_image, cmap='gray')
print('All done!')
# large_image = ImageOps.grayscale(large_image)
large_image = np.array(large_image)
# print(large_image)

# #large_image = np.expand_dims(large_image, axis=0)
# #large_image=np.array(large_image)
# patch_size=128
# print(large_image.shape)
#large_image = np.expand_dims(large_image, axis=2)

#h = large_image.shape[1]
#new_size = (h,h,3)
# large_image = np.resize(large_image,new_size)
# print(large_image.shape)
# #print('w: ' + str(width) + 'and h: ' + str(height))
# #segmented_image = prediction(model_segm, large_image, patch_size)

# #predicted_X_test = np.array(predicted_X_test)
# preds_test = model_segm.predict(X_test, verbose=1)
# preds_test_t = (preds_test > 0.5).astype(np.uint8)
# print(preds_test_t)
# im = Image.fromarray(preds_test_t)
# cv2.imwrite(im_path, im)
#Perform a sanity check on some random training samples
#ix = random.randint(0, len(preds_train_t))


# #Perform a sanity check on some random training samples
# for ix in preds_train_t:
#     arr = preds_train_t[ix]* 255
#     im = np.array(arr.astype(np.uint8))
#     im = Image.fromarray(im)
#     cv2.imwrite(im_path + 'preds_train_'+ str(ix) +'.png', im)
# # ix = random.randint(0, len(preds_train_t))
# # imshow(X_train[ix])
# # plt.savefig(im_path)im = Image.fromarray(X_train[ix])
# # im.save(im_path)

# #plt.savefig(im_path)

# #plt.show()
# im_path = "/home/inf-54-2020/experimental_cop/saved_images/Y_traintest1.png"

# i = np.squeeze(Y_train[ix])
# im = Image.fromarray(i)
# im.save(im_path)

# #plt.show()
# i = np.squeeze(preds_train_t[ix])
# im = Image.fromarray(i)
# im_path = "/home/inf-54-2020/experimental_cop/saved_images/preds_traintest2.png"
# im.save(im_path)

# #plt.show()

# #Perform a sanity check on some random validation samples
# ix = random.randint(0, len(preds_val_t))
# i = X_train[int(X_train.shape[0]*0.9):][ix]
# im = Image.fromarray(i)

# im_path = "/home/inf-54-2020/experimental_cop/saved_images/random_val_sample1.png"
# im.save(im_path)
# i = np.squeeze(Y_train[int(Y_train.shape[0]*0.9):][ix])
# im_path = "/home/inf-54-2020/experimental_cop/saved_images/random_val_sample2.png"
# im = Image.fromarray(i)

# i = np.squeeze(preds_val_t[ix])
# im = Image.fromarray(i)

# im_path = "/home/inf-54-2020/experimental_cop/saved_images/random_val_sample3.png"
# im = Image.fromarray(i)




