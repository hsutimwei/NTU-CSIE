import numpy as np
import cv2

def getDarkChannel(image , size):   

    B,G,R = cv2.split(image)
    min_Jc = cv2.min(cv2.min(B,R),G)
    kernel = np.ones((size,size),dtype=np.uint8)
    dark_channel = cv2.erode(min_Jc , kernel)

    return dark_channel


def Atmospheric_Light(img , dark_channel ,threshold = 0.999):

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height,width = img.shape[:2]
    pixel_num = height * width#imsz

    dark_channel_vector = dark_channel.reshape(pixel_num)
    img = img.reshape((pixel_num,3))
    gray_img = gray_img.reshape(pixel_num)

    index = dark_channel_vector.argsort()
    index = index[ int(pixel_num * threshold): ]
    
    max_A = -1
    max_index = -1
    for i in index:
        if(gray_img[i] > max_A):
            max_A = gray_img[i]
            max_index = i

    A = img[max_index]

    return A


def Transmission(img , A , size ,omega = 0.9):
    nor_img = np.zeros_like(img,dtype=np.float64)

    for i in range(3):
        nor_img[:,:,i] = img[:,:,i] / A[i]

    transmission = 1 - omega * getDarkChannel(nor_img , size)

    return transmission


def RefineTransMap_Guassian(trans):
    sigma = 5   
    refine_trans = cv2.GaussianBlur(trans, (5, 5),sigma)

    return refine_trans


def Recovering(img , A , transmission , t_x = 0.1):

    t = cv2.max( t_x, transmission)
    result = np.zeros_like(img)
    img=img.astype(np.int64)
    for i in range(3):
        result[: ,: ,i] = ((img[: ,: ,i] - A[i]) / t) + A[i]
        #print(img[: ,: ,i] - A[i])
    
    return result



sample1 = cv2.imread("foggy_picture4.jpg",cv2.IMREAD_COLOR)
window_size = 9

darkchannel = getDarkChannel(sample1, window_size)
A = Atmospheric_Light(sample1, darkchannel)
trans = Transmission(sample1, A , window_size )
retrans = RefineTransMap_Guassian(trans)
result = Recovering(sample1 , A , retrans)

#cv2.imshow("sample1",sample1)
#cv2.imshow("dark",darkchannel)
#cv2.imshow("trans" , trans)
#cv2.imshow("retrans" , retrans)


#print(np.max(result))
cv2.imshow("result",result)
cv2.imwrite("haha.png",result)
cv2.waitKey()