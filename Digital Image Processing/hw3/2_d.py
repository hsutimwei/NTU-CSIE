import numpy as np
import cv2
import random
#cited:https://github.com/axu2/image-quilting/blob/master/Final_Project_COS429%20(1).ipynb

img = cv2.imread("SampleImage/sample3.png",cv2.IMREAD_GRAYSCALE)#texture
img2= cv2.imread("result6.png",cv2.IMREAD_GRAYSCALE)#img
#patchLength: 一個patch要多大
#texture: 材質的圖
patchLength=50
overlap=7
#h = (numPatchesHigh * patchLength) - (numPatchesHigh - 1) * overlap =600
#w = (numPatchesWide * patchLength) - (numPatchesWide - 1) * overlap =900
#numPatchesHigh=15
#numPatchesWide=25
result=np.zeros((1100,1100))

for i in range(15):
    for j in range(25):
        y = i * (patchLength - overlap)
        x = j * (patchLength - overlap)

        errors = np.zeros((img.shape[0] - patchLength, img.shape[1] - patchLength))
        minerror=1000000000000
        min_a=1000000000000
        min_b=1000000000000
        for a in range(img.shape[0] - patchLength):
            for b in range(img.shape[1] - patchLength):
                patch = img[a:a+patchLength, b:b+patchLength]
                error = np.sum(np.square(patch[:, :overlap] - result[y:y+patchLength, x:x+overlap])) + np.sum(np.square(patch[:overlap, :] - result[y:y+overlap, x:x+patchLength])) + np.sum(np.square(patch[:overlap, :overlap] - result[y:y+overlap, x:x+overlap]))

                if minerror> error:
                    minerror=error
                    min_a=a
                    min_b=b
        patch = img[min_a:min_a+patchLength, min_b:min_b+patchLength]
        minCut = np.zeros(patch.shape)
        

        patch = minCutPatch(patch, patchLength, overlap, result, y, x)
            
        result[y:y+patchLength, x:x+patchLength] = patch