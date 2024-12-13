import numpy as np
import cv2
import matplotlib.pyplot as plt
import math
img = cv2.imread("result5.png",cv2.IMREAD_GRAYSCALE)
#step 1
gaussianfilter = (1/159)*np.array([[2 , 4 , 5 , 4 , 2 ],
                                   [4 , 9 , 12, 9 , 4 ],
                                   [5 , 12, 15, 12, 5 ],
                                   [4 , 9 , 12, 9 , 4 ],
                                   [2 , 4 , 5 , 4 , 2 ]],dtype=float)
img=np.pad(img, ((2, 2), (2, 2)), 'edge')
img2 = np.zeros((600,800))
for i in range(2,img.shape[0] - 2):
    for j in range(2,img.shape[1] - 2):
        img2[i-2,j-2] = np.sum(np.multiply(gaussianfilter, img[i-2:i+3, j-2:j+3]))

#step 2
x = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
img3 = np.zeros((600,800))
img4 = np.zeros((600,800))
for i in range(1,img2.shape[0] - 1):
    for j in range(1,img2.shape[1] - 1):
        gx = np.sum(np.multiply(x, img2[i-1:i+2, j-1:j+2]))
        gy = np.sum(np.multiply(y, img2[i-1:i+2, j-1:j+2]))
        img3[i-1,j-1] = np.sqrt(gx**2+gy**2)
        if gx == 0:                                    # avoid divide by zero
            gx = 0.000001
        img4[y-1,x-1] = math.atan(gy/gx)
#cv2.imwrite("img3.png",img3)
img5 = img3.copy()
img3=np.pad(img3, ((1, 1), (1, 1)), 'edge')
#img3=img3.astype(np.uint8)
img4=np.degrees(img4)
img4[img4<0]+=180
for i in range(1, img3.shape[0]-1):
    for j in range(1, img3.shape[1]-1):
        if img4[i-1,j-1] < 22.5 or img4[i-1,j-1] >= 157.5:
            if img3[i,j] < img3[i, j+1] or img3[i, j] < img3[i, j-1]:
                img5[i-1, j-1] = 0
        elif 67.5> img4[i-1,j-1] >= 22.5:
            if img3[i, j] < img3[i-1, j+1] or img3[i, j] < img3[i+1, j-1]:
                img5[i-1, j-1] = 0
        elif 112.5 > img4[i-1,j-1] >= 67.5:
            if img3[i, j] < img3[i-1, j] or img3[i, j] < img3[i+1, j]:
                img5[i-1, j-1] = 0
        elif 157.5> img4[i-1,j-1] >= 112.5:
            if img3[i, j] < img3[i-1, j-1] or img3[i, j] < img3[i+1, j+1]:
                img5[i-1, j-1] = 0
img5=img5.astype(np.uint8)
#cv2.imwrite("img5.png",img5)
#cv2.imshow("haha",img5)
#cv2.waitKey(0)

#step 4
img6 = np.zeros((600,800))
edge=np.where(img5>50)
nonedge=np.where(img5<25)
candidate=np.where((img5<=50) & (img5>=25))
img6[edge]=255
img6[nonedge]=0
img6[candidate]=120
#cv2.imwrite("img6.png",img6)
img7 = np.zeros((600,800))
#step 5
img6=np.pad(img6, ((1, 1), (1, 1)), 'edge')
for i in range(1,img6.shape[0] - 1):
    for j in range(1,img6.shape[1] - 1):
        if img6[i,j]==120:
            if img6[i+1,j]==255 or img6[i+1,j+1]==255 or img6[i+1,j-1]==255 or img6[i,j+1]==255 or img6[i,j-1]==255 or img6[i-1,j+1]==255 or img6[i-1,j]==255 or img6[i-1,j-1]==255:
                img7[i-1,j-1]=255
        elif img6[i,j]==255:
            img7[i-1,j-1]=255

cv2.imwrite("result6.png",img7)
#cited:https://tempflip.medium.com/lane-detection-with-numpy-2-hough-transform-f4c017f4da39
hough_space = np.zeros((1000,1000))
for i in range(img7.shape[0]):
    for j in range(img7.shape[1]):   
        if img7[i,j] == 255: 
            for x in range(180):
                d = int(i * np.cos(x*3.1415926/180) + j * np.sin(x*3.1415926/180))
                hough_space[x, d] += 3
            
            

cv2.imwrite("result7.png",hough_space)