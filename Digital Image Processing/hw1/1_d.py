import numpy as np
import cv2
import matplotlib.pyplot as plt


def solve(name1,name2,name3):
    img = cv2.imread(name1,cv2.IMREAD_GRAYSCALE)
    hist,bins = np.histogram(img.flatten(),bins =  [x for x in range(256)])
    cdf = hist.cumsum() #算cdf

    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            img[y][x]=cdf[img[y][x]]/cdf.max()*255

    cv2.imwrite(name2,img)

    plt.hist(img.flatten(),bins =  [x for x in range(256)])
    plt.savefig(name3)
    plt.show()

solve("sample2.png","result5.png","result5_hist.png")
solve("result3.png","result6.png","result6_hist.png")
solve("result4.png","result7.png","result7_hist.png")