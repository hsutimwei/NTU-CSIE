import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread("SampleImage/sample3.png",cv2.IMREAD_GRAYSCALE)
img2=np.zeros(img.shape)
img2[img2==0]=255
cnt=0
cut=0
for j in range(img.shape[1]):
    cntj=0
    for i in range(img.shape[0]):
        if img[i,j]!=255:
            cntj=1
        if cntj==1:
            cnt=1
        if cut!=0:
            img2[i,j]=img[i,j]
    if cntj==0 and cnt==1 and cut==0:
        cut=j
        
img4 = np.zeros(img.shape) 
img4[img4==0]=255

#scaling
for j in range(img.shape[1]):
    for i in range(img.shape[0]):
        if i>150:
            img4[i,j]=img2[int(i/2.15-150/2.15+260),j]
        else:
            img4[i,j]=img2[i+110,j]
#rotate
angle=-np.pi/180*22
angle_mat = np.transpose(np.array([[np.cos(angle),-np.sin(angle)],
                                      [np.sin(angle),np.cos(angle)]]))

img3 = np.zeros((800,800)) 
img3[img3==0]=255
for i in range(img3.shape[0]):
    for j in range(img3.shape[1]):
        mat = np.array([[i],[j]])
            
        rotate_mat = np.dot(angle_mat,mat)

        x =int(rotate_mat[0])
        y =int(rotate_mat[1])

        if 0<=x<=img.shape[1]-1 and 0<=y<=img.shape[0]-1: 
            img3[i,j] = img4[x,y]

#move2
img5 = np.zeros(img.shape) 
img5[img5==0]=255

for j in range(img3.shape[1]):
    for i in range(img3.shape[0]):
        if i<img.shape[0] and j-100>0 and j<img.shape[1]:
            img5[i,j]=img3[i+97,j-118]



#加回來
img6 = np.zeros(img.shape) 
img6[img6==0]=255
for j in range(img.shape[1]):
    for i in range(img.shape[0]):
        if j<cut:
            img6[i,j]=img[i,j]
        else:
            img6[i,j]=img5[i,j]

img6=img6.astype(np.uint8)
cv2.imwrite("result8.png",img6)
#cv2.imshow("haha",img)
#cv2.waitKey(0)