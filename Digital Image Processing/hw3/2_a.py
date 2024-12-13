import numpy as np
import cv2
import random
img = cv2.imread("SampleImage/sample2.png",cv2.IMREAD_GRAYSCALE)
mask=[0,0,0,0,0,0,0,0,0]
mask[0] = 1/36*np.array([[1, 2, 1],
                         [2, 4, 2],
                         [1, 2, 1]])
mask[1] = 1/12*np.array([[1, 2, 1],
                         [0, 0, 0],
                         [-1, -2, -1]])
mask[2] = 1/12*np.array([[-1, 2, -1],
                         [-2, 4, -2],
                         [-1, 2, -1]])
mask[3] = 1/12*np.array([[-1, -2, -1],
                         [0, 0, 0],
                         [1, 2, 1]])
mask[4] = 1/4*np.array([[1, 0, -1],
                        [0, 0, 0],
                        [-1, 0, 1]])
mask[5] = 1/4*np.array([[-1, 2, -1],
                        [0, 0, 0],
                        [1, -2, 1]])
mask[6] = 1/12*np.array([[-1, -2, -1],
                         [2, 4, 2],
                         [-1, -2, -1]])
mask[7] = 1/4*np.array([[-1, 0, 1],
                        [2, 0, -2],
                        [-1, 0, 1]])
mask[8] = 1/4*np.array([[1, -2, 1],
                        [-2, 4, -2],
                        [1, -2, 1]])


Map1 = np.zeros(img.shape)
Map2 = np.zeros(img.shape)
Map3 = np.zeros(img.shape)
Map4 = np.zeros(img.shape)
Map5 = np.zeros(img.shape)
Map6 = np.zeros(img.shape)
Map7 = np.zeros(img.shape)
Map8 = np.zeros(img.shape)
Map9 = np.zeros(img.shape)
energy=np.zeros((9,img.shape[0],img.shape[1]))
threshold=2

img = np.pad(img, ((1, 1), (1, 1)), 'edge')
#算乘上9個mask的結果
for i in range(1,img.shape[0] - 1):
    for j in range(1,img.shape[1] - 1):
        Map1[i-1,j-1] = np.sum(np.multiply(mask[0], img[i-1:i+2, j-1:j+2]))
        Map2[i-1,j-1] = np.sum(np.multiply(mask[1], img[i-1:i+2, j-1:j+2]))
        Map3[i-1,j-1] = np.sum(np.multiply(mask[2], img[i-1:i+2, j-1:j+2]))
        Map4[i-1,j-1] = np.sum(np.multiply(mask[3], img[i-1:i+2, j-1:j+2]))
        Map5[i-1,j-1] = np.sum(np.multiply(mask[4], img[i-1:i+2, j-1:j+2]))
        Map6[i-1,j-1] = np.sum(np.multiply(mask[5], img[i-1:i+2, j-1:j+2]))
        Map7[i-1,j-1] = np.sum(np.multiply(mask[6], img[i-1:i+2, j-1:j+2]))
        Map8[i-1,j-1] = np.sum(np.multiply(mask[7], img[i-1:i+2, j-1:j+2]))
        Map9[i-1,j-1] = np.sum(np.multiply(mask[8], img[i-1:i+2, j-1:j+2]))

#算energy

Map1= np.pad(Map1, ((1, 1), (1, 1)), 'edge')
Map2= np.pad(Map2, ((1, 1), (1, 1)), 'edge')
Map3= np.pad(Map3, ((1, 1), (1, 1)), 'edge')
Map4= np.pad(Map4, ((1, 1), (1, 1)), 'edge')
Map5= np.pad(Map5, ((1, 1), (1, 1)), 'edge')
Map6= np.pad(Map6, ((1, 1), (1, 1)), 'edge')
Map7= np.pad(Map7, ((1, 1), (1, 1)), 'edge')
Map8= np.pad(Map8, ((1, 1), (1, 1)), 'edge')
Map9= np.pad(Map9, ((1, 1), (1, 1)), 'edge')
for i in range(1,Map1.shape[0] -1):
    for j in range(1,Map1.shape[1] -1):
        energy[0][i-1,j-1] = np.sum(np.square(Map1[i-1:i+threshold, j-1:j+threshold]))
        energy[1][i-1,j-1] = np.sum(np.square(Map2[i-1:i+threshold, j-1:j+threshold]))
        energy[2][i-1,j-1] = np.sum(np.square(Map3[i-1:i+threshold, j-1:j+threshold]))
        energy[3][i-1,j-1] = np.sum(np.square(Map4[i-1:i+threshold, j-1:j+threshold]))
        energy[4][i-1,j-1] = np.sum(np.square(Map5[i-1:i+threshold, j-1:j+threshold]))
        energy[5][i-1,j-1] = np.sum(np.square(Map6[i-1:i+threshold, j-1:j+threshold]))
        energy[6][i-1,j-1] = np.sum(np.square(Map7[i-1:i+threshold, j-1:j+threshold]))
        energy[7][i-1,j-1] = np.sum(np.square(Map8[i-1:i+threshold, j-1:j+threshold]))
        energy[8][i-1,j-1] = np.sum(np.square(Map9[i-1:i+threshold, j-1:j+threshold]))
energy1=energy.copy()
min0=np.min(energy[0])
min1=np.min(energy[1])
min2=np.min(energy[2])
min3=np.min(energy[3])
min4=np.min(energy[4])
min5=np.min(energy[5])
min6=np.min(energy[6])
min7=np.min(energy[7])
min8=np.min(energy[8])

for i in range(1,energy[0].shape[0] - 1):
    for j in range(1,energy[0].shape[1] - 1):
        energy[0][i-1,j-1] = energy[0][i-1,j-1]-min0
        energy[1][i-1,j-1] = energy[1][i-1,j-1]-min1
        energy[2][i-1,j-1] = energy[2][i-1,j-1]-min2
        energy[3][i-1,j-1] = energy[3][i-1,j-1]-min3
        energy[4][i-1,j-1] = energy[4][i-1,j-1]-min4
        energy[5][i-1,j-1] = energy[5][i-1,j-1]-min5
        energy[6][i-1,j-1] = energy[6][i-1,j-1]-min6
        energy[7][i-1,j-1] = energy[7][i-1,j-1]-min7
        energy[8][i-1,j-1] = energy[8][i-1,j-1]-min8

max0=np.max(energy[0])
max1=np.max(energy[1])
max2=np.max(energy[2])
max3=np.max(energy[3])
max4=np.max(energy[4])
max5=np.max(energy[5])
max6=np.max(energy[6])
max7=np.max(energy[7])
max8=np.max(energy[8])

for i in range(energy[0].shape[0]):
    for j in range(energy[0].shape[1]):
        energy[0][i,j] = energy[0][i,j]/max0*255
        energy[1][i,j] = energy[1][i,j]/max1*255
        energy[2][i,j] = energy[2][i,j]/max2*255
        energy[3][i,j] = energy[3][i,j]/max3*255
        energy[4][i,j] = energy[4][i,j]/max4*255
        energy[5][i,j] = energy[5][i,j]/max5*255
        energy[6][i,j] = energy[6][i,j]/max6*255
        energy[7][i,j] = energy[7][i,j]/max7*255
        energy[8][i,j] = energy[8][i,j]/max8*255

for i in range(9):
    cv2.imwrite(f"energy{i}.png",energy[i].astype(np.uint8))
        