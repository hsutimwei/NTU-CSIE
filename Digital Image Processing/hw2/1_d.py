import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread("SampleImage/sample2.png",cv2.IMREAD_GRAYSCALE)

x = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
img = np.pad(img, ((1, 1), (1, 1)), 'edge')
img2 = np.zeros((600,800))
for i in range(1,img.shape[0] - 1):
    for j in range(1,img.shape[1] - 1):
        img2[i-1,j-1] = np.sum(np.multiply(x, img[i-1:i+2, j-1:j+2]))
        if img2[i-1,j-1]<0:
            img2[i-1,j-1]=0
        elif img2[i-1,j-1]>255:
            img2[i-1,j-1]=255
'''x = (1/9)*np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
img = np.pad(img, ((1, 1), (1, 1)), 'edge')
img2 = np.zeros((600,800))
for i in range(1,img.shape[0] - 1):
    for j in range(1,img.shape[1] - 1):
        img2[i-1,j-1] = np.sum(np.multiply(x, img[i-1:i+2, j-1:j+2]))

c=5/6
img3 = np.zeros((600,800))
for i in range(img2.shape[0]):
    for j in range(img2.shape[1]):
        img3[i,j] = c/(2*c-1)*img[i+1,j+1]-(1-c)/(2*c-1)*img2[i,j]
img3=img3.astype(np.uint8)'''
cv2.imwrite("result5.png",img2)
#cv2.imshow("haha",img)
#cv2.waitKey(0)