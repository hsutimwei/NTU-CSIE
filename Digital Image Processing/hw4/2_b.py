import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread("SampleImage/sample2.png",cv2.IMREAD_GRAYSCALE)

img=np.fft.fftshift(np.fft.fft2(img))
#img=abs(np.fft.ifft2(img))
plt.figure(num=None, figsize=(8, 6), dpi=80)  
#img=np.log(abs(img))
img2=np.zeros((2048,1639),dtype=complex)


cutoff=20
for i in range(img2.shape[0]):
    for j in range(img2.shape[1]):
        img2[i,j]=1-np.exp((-(i-1024)**2-(j-820)**2)/2/cutoff**2)

img=np.multiply(img,img2)  
        

img=abs(np.fft.ifft2(img))

plt.imshow(img, cmap='gray') 
plt.savefig('result6.png')