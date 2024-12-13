import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread("sample2.png")
plt.hist(img.flatten(),bins =  [x for x in range(256)])
plt.title("histogram") 
plt.savefig('sample2_hist.png')
plt.show()
plt.clf()

img = cv2.imread("result3.png")
plt.hist(img.flatten(),bins =  [x for x in range(256)])
plt.title("histogram") 
plt.savefig('result3_hist.png')
plt.show()
plt.clf()

img = cv2.imread("result4.png")
plt.hist(img.flatten(),bins =  [x for x in range(256)])
plt.title("histogram") 
plt.savefig('result4_hist.png')
plt.show()
