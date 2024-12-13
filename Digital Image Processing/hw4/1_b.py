import numpy as np
import cv2

img = cv2.imread("SampleImage/sample1.png",cv2.IMREAD_GRAYSCALE)

img2=np.zeros(img.shape)

dither_matrix=np.array([[1,2],[3,0]])
threshold_matrix=np.zeros((256,256))
size=4
a=dither_matrix
while(size<=256):
    big_dither_matrix=np.zeros((size,size))
    for i in range(0,big_dither_matrix.shape[0]-1,size//2):
        for j in range(0,big_dither_matrix.shape[1]-1,size//2):
            for x in range(size//2):
                for y in range(size//2):
                    big_dither_matrix[i+x,j+y]=4*a[x,y]+dither_matrix[i*2//size,j*2//size]
    a=big_dither_matrix
    size*=2
                

for i in range(256):
    for j in range(256):
        threshold_matrix[i,j]=int(255*(big_dither_matrix[i, j]+0.5)//256/256)

for i in range(0,img.shape[0]-1,256):
    for j in range(0,img.shape[1]-1,256):
        for x in range(256):
            for y in range(256):
                if i+x<622 and j+y<622 and img[i+x, j+y] >= threshold_matrix[x, y]:
                    img2[i+x, j+y]=255

cv2.imwrite("result2.png",img2)
        
#cv2.imshow("haha",img)
#cv2.waitKey(0)