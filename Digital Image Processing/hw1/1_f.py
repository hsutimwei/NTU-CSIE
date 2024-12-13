import numpy as np
import cv2
import matplotlib.pyplot as plt

#1_f
img = cv2.imread("sample2.png",cv2.IMREAD_GRAYSCALE)
hist,bins = np.histogram(img.flatten(),bins =  [x for x in range(257)])
cdf = hist.cumsum() #算cdf

for y in range(img.shape[0]):
    for x in range(img.shape[1]):
        img[y][x]=cdf[img[y][x]]/cdf.max()*255

img = img.astype(np.float64)
img /= 255
img = img ** (0.8)
img *= 255
img = img.astype(np.uint8)

cv2.imwrite("result11.png",img)
plt.hist(img.flatten(),bins =  [x for x in range(256)])
plt.savefig("result11_hist.png")
plt.show()
#cv2.imshow("haha",img)
#cv2.waitKey(0)
