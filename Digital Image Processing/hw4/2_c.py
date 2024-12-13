import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread("SampleImage/sample3.png",cv2.IMREAD_GRAYSCALE)

img=np.fft.fftshift(np.fft.fft2(img))
#img=abs(np.fft.ifft2(img))
plt.figure(num=None, figsize=(8, 6), dpi=80)  
#img=np.log(abs(img))
#img2=np.zeros((2048,1639),dtype=complex)
#(437, 363)

img[362, 363]=0
img[512, 363]=0
img=abs(np.fft.ifft2(img))
#plt.imshow(np.log(abs(img)), cmap='gray') 
plt.imshow(img, cmap='gray')                          
#plt.show()   
plt.savefig('result7.png')

