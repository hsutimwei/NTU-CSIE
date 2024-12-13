import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread("SampleImage/sample1.png",cv2.IMREAD_GRAYSCALE)
#step 1
mask = (1/273)*np.array([[1 , 4 , 7 , 4 , 1 ],
                         [4 , 16, 26, 16, 4 ],
                         [7 , 26, 41, 26, 7 ],
                         [4 , 16, 26, 16, 4 ],
                         [1 , 4 , 7 , 4 , 1 ]])
img2 = np.zeros((512,512))
img = np.pad(img, ((2, 2), (2, 2)), 'edge')
for i in range(2,img.shape[0] - 2):
    for j in range(2,img.shape[1] - 2):
        img2[i-2,j-2] = np.sum(np.multiply(mask, img[i-2:i+3, j-2:j+3]))
#cv2.imwrite("1.png",img2)
#step 2
mask = np.array([[-1, -1, -1],
                 [-1,  8, -1],
                 [-1, -1, -1]])
img = img2.copy()
img2 = np.zeros((512,512))
img = np.pad(img, ((1, 1), (1, 1)), 'edge')
for i in range(1,img.shape[0] - 1):
    for j in range(1,img.shape[1] - 1):
        img2[i-1][j-1] = np.sum(np.multiply(mask, img[i-1:i+2, j-1:j+2]))
#cv2.imwrite("2.png",img2)
#plt.hist(img2.flatten(),bins =  [x for x in range(-20,21)])
#plt.show()
#step 3
zero=np.where((img2<=18) & (img2>=-18))
img2[zero]=0
#cv2.imwrite("3.png",img2)
#step 4
img=np.zeros((512,512))
img2 = np.pad(img2, ((1, 1), (1, 1)), 'edge')
for i in range(1, img2.shape[0]-1):
    for j in range(1, img2.shape[1]-1):
        if img2[i, j] == 0:
            if img2[i, j-1]*img2[i, j+1] < 0 or img2[i+1, j-1]*img2[i-1, j+1] < 0 or img2[i-1, j]*img2[i+1, j] < 0 or img2[i-1, j-1]*img2[i+1, j+1] < 0:
                img[i-1,j-1]=255

img=img.astype(np.uint8)
cv2.imwrite("result4.png",img)
#cv2.imshow("haha",img)
#cv2.waitKey(0)