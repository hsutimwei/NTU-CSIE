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
    

#k-mean
features=np.zeros((energy[0].shape[0],energy[0].shape[1],9))#把每個pixel的9個features合成1個9維的features，增加一個維度是放原圖的顏色
for i in range(energy[0].shape[0]):
    for j in range(energy[0].shape[1]):
        for x in range(9):
            features[i,j,x]=energy[x-1][i,j]
        
k=4

center=np.zeros((k,9))#設k的中心，每個中心都是10維的值

for i in range(k):
    for x in range(9):
        center[i,x]=random.uniform(0,2)#features[i*135,i*135]

a=0

classified=np.zeros((600,900))#
while a<=50:
    a+=1
    #算energy每個值對每個center的距離，然後歸類是哪個center的cluster
    
    for i in range(600):
        for j in range(900):
            mindistance=100000000000
            mink=10000000
            for x in range(k):
                distance=np.sum(np.square(features[i,j]-center[x]))
                if distance<mindistance:
                    mindistance=distance
                    mink=x
            classified[i,j]=mink
    
    #再根據每個cluster去算center
    sum=np.zeros((k,9))
    cnt=np.zeros(k)
    for i in range(600):
        for j in range(900):
            sum[int(classified[i,j])]+=features[i,j]
            cnt[int(classified[i,j])]+=1
    
    for x in range(k):
        if cnt[x]!=0:
            center[x]=sum[x]/cnt[x]
            
img2=np.zeros((600,900))
for i in range(600):
    for j in range(900):
        img2[i,j]=classified[i,j]*255/k
            
cv2.imwrite("result5.png",img2.astype(np.uint8))       
#好了這時候應該做完了，要把每個類別的影像標出來
