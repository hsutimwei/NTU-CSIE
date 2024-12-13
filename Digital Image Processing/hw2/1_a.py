import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread("SampleImage/sample1.png",cv2.IMREAD_GRAYSCALE)

x = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
img = np.pad(img, ((1, 1), (1, 1)), 'edge')
img2 = np.zeros((512,512))
img3 = np.zeros((512,512))
for i in range(1,img.shape[0] - 1):
    for j in range(1,img.shape[1] - 1):
        gx = np.sum(np.multiply(x, img[i-1:i+2, j-1:j+2]))
        gy = np.sum(np.multiply(y, img[i-1:i+2, j-1:j+2]))
        img3[i-1][j-1] = np.sqrt(gx**2+gy**2)
        if img3[i-1][j-1]>100:
            img2[i-1][j-1]=255
        else:
            img2[i-1][j-1]=0
img2=img2.astype(np.uint8)
img3=img3.astype(np.uint8)
cv2.imwrite("result1.png",img3)
cv2.imwrite("result2.png",img2)
#cv2.imshow("haha",img)
#cv2.waitKey(0)