import numpy as np
import cv2
import matplotlib.pyplot as plt


def solve(name1,name2,name3):
    img = cv2.imread(name1,cv2.IMREAD_GRAYSCALE)
    img=np.pad(img, (1,1), 'constant', constant_values=(0, 0))
    img2=np.zeros((600,800),dtype=int)
    for y in range(1,img.shape[0]-1):
        for x in range(1,img.shape[1]-1):
            mask=np.array([img[y-1:y+2,x-1:x+2]],dtype=int)
            img2[y-1][x-1]=mask[mask<=img[y][x]].size/mask.size*255
    img2 = img2.astype(np.uint8)        
    cv2.imwrite(name2,img2)

    plt.hist(img2.flatten(),bins =  [x for x in range(256)])
    plt.show()
    plt.savefig(name3)
    plt.clf()

solve("sample2.png","result8.png","result8_hist.png")
solve("result3.png","result9.png","result9_hist.png")
solve("result4.png","result10.png","result10_hist.png")