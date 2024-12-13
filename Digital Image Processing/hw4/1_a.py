import numpy as np
import cv2

img = cv2.imread("SampleImage/sample1.png",cv2.IMREAD_GRAYSCALE)

img2=np.zeros(img.shape)

dither_matrix=np.array([[1,2],[3,0]])
threshold_matrix=np.array([[1,2],[3,0]])
for i in range(2):
    for j in range(2):
        threshold_matrix[i,j]=int(255*(dither_matrix[i, j]+0.5)//4)

for i in range(0,img.shape[0]-1,2):
    for j in range(0,img.shape[1]-1,2):
        for x in range(2):
            for y in range(2):
                if i+x<622 and j+y<622 and img[i+x, j+y] >= threshold_matrix[x, y]:
                    img2[i+x, j+y]=255

cv2.imwrite("result1.png",img2)
        
#cv2.imshow("haha",img)
#cv2.waitKey(0)