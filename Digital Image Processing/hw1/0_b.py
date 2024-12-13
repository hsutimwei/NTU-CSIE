import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread("result1.png")
img=np.flip(img,0)
cv2.imwrite("result2.png",img)