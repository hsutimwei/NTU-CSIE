import numpy as np
import cv2

img = cv2.imread("SampleImage/sample1.png",cv2.IMREAD_GRAYSCALE)

img2=np.zeros(img.shape, dtype=float)
img=img.astype(np.float64)
img=np.pad(img, ((1, 1), (1, 1)), 'edge')

for i in range(1,img.shape[0]-1):
    for j in range(1,img.shape[1]-1):

        if img[i,j]<128:
            img2[i-1,j-1]=0
        else:
            img2[i-1,j-1]=255
        
        error=img[i,j]-img2[i-1,j-1]
            
        img[i,j+1]+=error*7/16
        img[i+1,j]+=error*5/16
        img[i+1,j+1]+=error*1/16
        img[i+1,j-1]+=error*3/16
            
cv2.imwrite("result3.png",img2)

img = cv2.imread("SampleImage/sample1.png",cv2.IMREAD_GRAYSCALE)

img2=np.zeros(img.shape, dtype=float)
img=img.astype(np.float64)
img=np.pad(img, ((2, 2), (2, 2)), 'edge')

for i in range(2,img.shape[0]-2):
    for j in range(2,img.shape[1]-2):

        if img[i,j]<128:
            img2[i-2,j-2]=0
        else:
            img2[i-2,j-2]=255
        
        error=img[i,j]-img2[i-2,j-2]
            
        img[i,j+1]+=error*7/48
        img[i,j+2]+=error*5/48
        img[i+1,j-2]+=error*3/48
        img[i+1,j-1]+=error*5/48
        img[i+1,j]+=error*7/48
        img[i+1,j+1]+=error*5/48
        img[i+1,j+2]+=error*3/48
        img[i+2,j-2]+=error*1/48
        img[i+2,j-1]+=error*3/48
        img[i+2,j]+=error*5/48
        img[i+2,j+1]+=error*3/48
        img[i+2,j+2]+=error*1/48

cv2.imwrite("result4.png",img2)
'''
img = cv2.imread("SampleImage/sample1.png",cv2.IMREAD_GRAYSCALE)

img2=np.zeros(img.shape, dtype=float)
img=img.astype(np.float64)
img=np.pad(img, ((2, 2), (2, 2)), 'edge')

for i in range(2,img.shape[0]-2):
    for j in range(2,img.shape[1]-2):

        if img[i,j]<128:
            img2[i-2,j-2]=0
        else:
            img2[i-2,j-2]=255
        
        error=img[i,j]-img2[i-2,j-2]
            
        img[i,j+1]+=error*8/32
        img[i,j+2]+=error*4/32
        img[i+1,j-2]+=error*2/32
        img[i+1,j-1]+=error*4/32
        img[i+1,j]+=error*8/32
        img[i+1,j+1]+=error*4/32
        img[i+1,j+2]+=error*2/32


cv2.imwrite("haha.png",img2)'''