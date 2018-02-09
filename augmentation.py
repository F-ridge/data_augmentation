# -*- coding: utf-8 -*-
#Opencvをインストールしてから使う

import cv2
import os
import shutil
import numpy as np

def folder_copy(copyfrom, copyto):
    for filename in os.listdir(copyfrom):
        filepath = os.path.join(copyfrom, filename)
        
        if os.path.isdir(filepath):
            folder_copy(filepath, copyto)
            
        elif os.path.isfile(filepath):
            copypath = os.path.join(copyto, filename)
            shutil.copy(filepath, copypath)
            print('{0}から{1}にファイルをコピー'.format(filepath, copypath))

#グレースケールにする   
def rgb2gray(image_rgb):
    image = np.dot(image_rgb, [0.299, 0.587, 0.114])
    image = image / 255.0
    
    return image

def resize(image, cell, nucleus):
    image360 = cv2.resize(image, (360,360))
    image572 = cv2.resize(image, (572,572))
    cell388 = cv2.resize(cell, (388,388))
    nucleus388 = cv2.resize(nucleus, (388,388))
    
    return image360, image572, cell388, nucleus388

#x1~x2,y1~y2の範囲で切り抜き、それぞれ指定されたサイズまで引き延ばす
#np.random.randintの範囲は調整の余地あり
def shift_and_deformation(image, cell, nucleus):        
    x1 = np.random.randint(40,160)
    x2 = np.random.randint(200,320)
    y1 = np.random.randint(40,160)
    y2 = np.random.randint(200,320)
            
    image_trim = image[x1:x2, y1:y2]
    cell_trim = cell[x1:x2, y1:y2]
    nucleus_trim = nucleus[x1:x2, y1:y2]
        
    image_deform360 = cv2.resize(image_trim, (360,360))
    image_deform572 = cv2.resize(image_trim, (572,572))
    cell_deform = cv2.resize(cell_trim, (388,388))
    nucleus_deform = cv2.resize(nucleus_trim, (388,388))
            
    return image_deform360, image_deform572, cell_deform, nucleus_deform
   
#回転（転置は　image[:,::-1]　とすればよい）
def rotate(image360, image572, cell388,  nucleus388): 
    center_image360 = tuple(np.array([image360.shape[1] / 2, image360.shape[0] / 2]))
    center_image572 = tuple(np.array([image572.shape[1] / 2, image572.shape[0] / 2]))
    center_cell388 = tuple(np.array([cell388.shape[1] / 2, cell388.shape[0] / 2]))
    center_nucleus388 = tuple(np.array([cell388.shape[1] / 2, cell388.shape[0] / 2]))
    
    size_image360 = tuple(np.array([image360.shape[1], image360.shape[0]]))
    size_image572 = tuple(np.array([image572.shape[1], image572.shape[0]]))
    size_cell388 = tuple(np.array([cell388.shape[1], cell388.shape[0]]))
    size_nucleus388 = tuple(np.array([cell388.shape[1], cell388.shape[0]]))
    
    affine_matrix_image360 = cv2.getRotationMatrix2D(center_image360, 90.0, 1.0)
    affine_matrix_image572 = cv2.getRotationMatrix2D(center_image572, 90.0, 1.0)
    affine_matrix_cell388 = cv2.getRotationMatrix2D(center_cell388, 90.0, 1.0)
    affine_matrix_nucleus388 = cv2.getRotationMatrix2D(center_nucleus388, 90.0, 1.0)
    
    image360_r = cv2.warpAffine(image360, affine_matrix_image360, size_image360, flags=cv2.INTER_CUBIC)
    image572_r = cv2.warpAffine(image572, affine_matrix_image572, size_image572, flags=cv2.INTER_CUBIC)
    cell388_r = cv2.warpAffine(cell388, affine_matrix_cell388, size_cell388, flags=cv2.INTER_CUBIC)
    nucleus388_r = cv2.warpAffine(nucleus388, affine_matrix_nucleus388, size_nucleus388, flags=cv2.INTER_CUBIC)

    return image360_r, image572_r, cell388_r, nucleus388_r
