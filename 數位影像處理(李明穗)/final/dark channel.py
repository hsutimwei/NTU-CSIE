import numpy as np
import cv2

def getDarkChannel(image , size=9):   # change size

    B,G,R = cv2.split(image)
    min_Jc = cv2.min(cv2.min(B,R),G)
    kernel = np.ones((size,size),dtype=np.uint8)
    dark_channel = cv2.erode(min_Jc , kernel)

    return dark_channel

def Atmospheric_Light(img , dark_channel):
 
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height,width = img.shape[:2]
    pixel_num = height * width

    dark_channel_vector = dark_channel.reshape(pixel_num)
    img = img.reshape((pixel_num,3))
    gray_img = gray_img.reshape(pixel_num)
    
    index = dark_channel_vector.argsort()
    index = index[ int(pixel_num*0.999): ]
    
    max_A = -1
    max_index = -1
    for i in index:
        if(gray_img[i] > max_A):
            max_A = gray_img[i]
            max_index = i

    A = img[max_index]

    return A