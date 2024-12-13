import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread("sample5.png",cv2.IMREAD_GRAYSCALE)
img=np.pad(img, (1,1), 'constant', constant_values=(0, 0))
img2=np.zeros((320,313),dtype=int)
for y in range(1,img.shape[0]-1):
    for x in range(1,img.shape[1]-1):
        mask=np.array([img[y-1:y+2,x-1:x+2]],dtype=int)
        mask=np.sort(mask, axis=None)
        img2[y-1][x-1]=mask[4]
        
img = img2.astype(np.uint8)
cv2.imwrite("result13.png",img)

img = cv2.imread("sample4.png",cv2.IMREAD_GRAYSCALE)
img = img.astype(np.int32)
img=np.pad(img, (1,1), 'constant', constant_values=(0, 0))
img2=np.zeros((320,313),dtype=int)
for y in range(1,img.shape[0]-1):
    for x in range(1,img.shape[1]-1):
        mask=np.array([img[y-1:y+2,x-1:x+2]],dtype=int)
        img2[y-1][x-1]=img[y][x]*4+2*(img[y-1][x]+img[y][x-1]+img[y+1][x]+img[y][x+1])+img[y+1][x-1]+img[y+1][x+1]+img[y-1][x-1]+img[y-1][x+1]
        img2[y-1][x-1]/=16
img = img2.astype(np.uint8)
cv2.imwrite("result12.png",img)
        
