import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread("SampleImage/sample2.png",cv2.IMREAD_GRAYSCALE)

rate=2
img2=np.zeros((img.shape[0]//rate,img.shape[1]//rate))
for i in range(0,img.shape[0]-rate,rate):
    for j in range(0,img.shape[1]-rate,rate):
        img2[i//rate,j//rate]=img[i,j]
        
cv2.imwrite("result5.png",img2)
