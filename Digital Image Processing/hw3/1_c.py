import numpy as np
import cv2

img = cv2.imread("SampleImage/sample1.png",cv2.IMREAD_GRAYSCALE)


def bfs(x,y):
    img2=np.zeros(img.shape)
    tocheck=np.array([[x,y]])
    incheck=np.zeros(img.shape)
    while True:
        if tocheck.size!=0:
            i,j=tocheck[0]
            img2[i,j]=255
        
            if 445>i-1>=0 and 640>j>=0 and img2[i-1,j]!=255 and img[i-1,j]==255 and incheck[i-1,j]!=1:
                incheck[i-1,j]=1
                tocheck=np.append(tocheck,[[i-1,j]], axis=0)
            if 445>i+1>=0 and 640>j>=0 and img2[i+1,j]!=255 and img[i+1,j]==255 and incheck[i+1,j]!=1:
                incheck[i+1,j]=1
                tocheck=np.append(tocheck,[[i+1,j]], axis=0)
            if 445>i>=0 and 640>j-1>=0 and img2[i,j-1]!=255 and img[i,j-1]==255 and incheck[i,j-1]!=1:
                incheck[i,j-1]=1
                tocheck=np.append(tocheck,[[i,j-1]], axis=0)
            if 445>i>=0 and 640>j+1>=0 and img2[i,j+1]!=255 and img[i,j+1]==255 and incheck[i,j+1]!=1:
                incheck[i,j+1]=1
                tocheck=np.append(tocheck,[[i,j+1]], axis=0)
            
            '''if 445>i-1>=0 and 640>j+1>=0 and img2[i-1,j+1]!=255 and img[i-1,j+1]==255 and incheck[i-1,j+1]!=1:
                incheck[i-1,j+1]=1
                tocheck=np.append(tocheck,[[i-1,j+1]], axis=0)
            if 445>i-1>=0 and 640>j-1>=0 and img2[i-1,j-1]!=255 and img[i-1,j-1]==255 and incheck[i-1,j-1]!=1:
                incheck[i-1,j-1]=1
                tocheck=np.append(tocheck,[[i-1,j-1]], axis=0)
            if 445>i+1>=0 and 640>j-1>=0 and img2[i+1,j-1]!=255 and img[i+1,j-1]==255 and incheck[i+1,j-1]!=1:
                incheck[i+1,j-1]=1
                tocheck=np.append(tocheck,[[i+1,j-1]], axis=0)
            if 445>i+1>=0 and 640>j+1>=0 and img2[i+1,j+1]!=255 and img[i+1,j+1]==255 and incheck[i+1,j+1]!=1:
                incheck[i+1,j+1]=1
                tocheck=np.append(tocheck,[[i+1,j+1]], axis=0)'''
            tocheck = np.delete(tocheck,0, 0)

        else:
            return img2

count=0
check=0
while True:

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i,j]==255:
                img3=bfs(i,j)
                object=(img3==255)
                img[object]=0
                check=0#還有剩
                count+=1
                #cv2.imwrite(f"result{count+20}.png",img)
            else:
                check=1
    if check==1:
        break
print(count)