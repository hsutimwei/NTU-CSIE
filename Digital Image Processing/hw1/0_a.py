import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread("sample1.png")

b, g, r = img[:,:,0], img[:,:,1], img[:,:,2]
img =  0.2126*r + 0.7152*g + 0.0722*b
#img = 0.299*r + 0.587*g + 0.114*b
img=img.astype(np.uint8)

cv2.imwrite("result1.png",img)