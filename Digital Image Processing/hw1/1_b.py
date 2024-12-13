import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread("result3.png")
img=img*3
img=img.astype(np.uint8)
cv2.imwrite("result4.png",img)