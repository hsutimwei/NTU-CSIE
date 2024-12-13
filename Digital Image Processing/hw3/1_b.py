import numpy as np
import cv2

img = cv2.imread("SampleImage/sample1.png",cv2.IMREAD_GRAYSCALE)


#img2=np.zeros((445,640))# for erosion
img2=np.full(img.shape,255)

img3=img.copy()
tocheck=np.array([[0,0]])
incheck=np.zeros(img.shape)

while True:
    if tocheck.size!=0:
        i,j=tocheck[0]
        img2[i,j]=0
        
        if 445>i-1>=0 and 640>j>=0 and img2[i-1,j]!=0 and img[i-1,j]==0 and incheck[i-1,j]!=1:
            incheck[i-1,j]=1
            tocheck=np.append(tocheck,[[i-1,j]], axis=0)
        if 445>i+1>=0 and 640>j>=0 and img2[i+1,j]!=0 and img[i+1,j]==0 and incheck[i+1,j]!=1:
            incheck[i+1,j]=1
            tocheck=np.append(tocheck,[[i+1,j]], axis=0)
        if 445>i>=0 and 640>j-1>=0 and img2[i,j-1]!=0 and img[i,j-1]==0 and incheck[i,j-1]!=1:
            incheck[i,j-1]=1
            tocheck=np.append(tocheck,[[i,j-1]], axis=0)
        if 445>i>=0 and 640>j+1>=0 and img2[i,j+1]!=0 and img[i,j+1]==0 and incheck[i,j+1]!=1:
            incheck[i,j+1]=1
            tocheck=np.append(tocheck,[[i,j+1]], axis=0)
        tocheck = np.delete(tocheck,0, 0)

    else:
        break

cv2.imwrite("result2.png",img2)