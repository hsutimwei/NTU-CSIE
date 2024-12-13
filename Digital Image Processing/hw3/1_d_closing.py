import numpy as np
import cv2

threshold=1
img = cv2.imread("SampleImage/sample1.png",cv2.IMREAD_GRAYSCALE)

img2=img.copy()
for i in range(threshold,img.shape[0] - threshold):
    for j in range(threshold,img.shape[1] - threshold):
        for x in range(-threshold,threshold+1):
            for y in range(-threshold,threshold+1):
                if img[i,j]==0 and img[i+x,j+y]==255:# and x*y==0:
                    img2[i,j]=255
img3=img2.copy()

for i in range(threshold,img.shape[0] - threshold):
    for j in range(threshold,img.shape[1] - threshold):
        for x in range(-threshold,threshold+1):
            for y in range(-threshold,threshold+1):
                if img2[i,j]==255 and img2[i+x,j+y]==0:# and x*y==0:
                    img3[i,j]=0

cv2.imwrite("result4.png",img3)