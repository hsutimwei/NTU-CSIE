import numpy as np
import cv2
import random

img = cv2.imread("result5.png",cv2.IMREAD_GRAYSCALE)
img2=np.zeros(img.shape)
img = np.pad(img, ((2, 2), (2, 2)), 'edge')

for i in range(2,img.shape[0]-2):
    for j in range(2,img.shape[1]-2):
        a1,a2,a3,a4=0,0,0,0
        for x in [-2,-1,0,1,2]:
            for y in [-2,-1,0,1,2]:
                if img[i+x,j+y]==int(255/4):
                    a1+=1
                elif img[i+x,j+y]==int(255/4*2):
                    a2+=1
                elif img[i+x,j+y]==int(255/4*3):
                    a3+=1
                elif img[i+x,j+y]==int(255/4*4):
                    a4+=1
        if a1>=13:
            img2[i-2,j-2]=int(255/4)
        elif a2>=13:
            img2[i-2,j-2]=int(255/4*2)
        elif a3>=13:
            img2[i-2,j-2]=int(255/4*3)
        elif a4>=13:
            img2[i-2,j-2]=int(255/4*4)
        else:
            img2[i-2,j-2]=img[i,j]
cv2.imwrite("result6.png",img2.astype(np.uint8))     
