import numpy as np
import cv2
import matplotlib.pyplot as plt

mse=0

img=cv2.imread("sample3.png",cv2.IMREAD_GRAYSCALE)
img2=cv2.imread("result12.png",cv2.IMREAD_GRAYSCALE)
img = img.astype(np.int32)
img2 = img2.astype(np.int32)
for y in range(img.shape[0]):
    for x in range(img.shape[1]):
        mse+=(img[y][x]-img2[y][x])**2
mse/=img.shape[0]*img.shape[1]
psnr=10*np.log10(255**2/mse)
print(psnr)

mse=0
img=cv2.imread("sample3.png",cv2.IMREAD_GRAYSCALE)
img2=cv2.imread("result13.png",cv2.IMREAD_GRAYSCALE)
img = img.astype(np.int32)
img2 = img2.astype(np.int32)
for y in range(img.shape[0]):
    for x in range(img.shape[1]):
        mse+=(img[y][x]-img2[y][x])**2
mse/=img.shape[0]*img.shape[1]
psnr=10*np.log10(255**2/mse)
print(psnr)