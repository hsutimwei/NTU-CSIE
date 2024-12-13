import numpy as np
import cv2

img = cv2.imread("SampleImage/sample1.png",cv2.IMREAD_GRAYSCALE)


#img2=np.zeros((445,640))# for erosion
img2=img.copy()
img3=img.copy()
for i in range(1,img.shape[0] - 1):
    for j in range(1,img.shape[1] - 1):
        for x in [-1,0,1]:
            for y in [-1,0,1]:
                if img[i,j]==0 and img2[i+x,j+y]==255:
                    img3[i,j]=255
             
for i in range(1,img.shape[0] - 1):
    for j in range(1,img.shape[1] - 1):
        if img[i,j]==0 and img3[i,j]==255:
            img3[i,j]=255
        else:
            img3[i,j]=0
cv2.imwrite("result1.png",img3)
#cv2.waitKey(0)
