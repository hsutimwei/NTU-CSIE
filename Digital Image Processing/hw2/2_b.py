import numpy as np
import cv2
import matplotlib.pyplot as plt
import math
img = cv2.imread("SampleImage/sample5.png",cv2.IMREAD_GRAYSCALE)

img2=np.zeros(img.shape)

def f(x):
    #當x~90時，f(x)~x
    #當x降低過一個threshold時，f(x)~0
    return x**2.6/85**1.6

for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        img2[i,j]=img[i,j]
        a=math.sqrt((i-175)**2+(j-149)**2)
        if a<=85:
            dis=f(a)
            if a==0:
                a=10**10
            img2[i,j]=img[175+int(dis/a*(i-175)),149+int(dis/a*(j-149))]

img2=img2.astype(np.uint8)        
cv2.imwrite("result9.png",img2)