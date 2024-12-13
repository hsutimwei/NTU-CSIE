import sys
import numpy as np
import cv2 as cv

WINDOW_NAME = 'window'


def on_mouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        param[0].append([x, y])  
        
        
def homography(points1,points2):
    DLT = []
    for i in range(len(points1)):
        u1, v1 = points1[i]
        u2, v2 = points2[i]
        DLT.append([u1, v1, 1, 0, 0, 0, -u1*u2, -u2*v1, -u2])
        DLT.append([0, 0, 0, u1, v1, 1, -u1*v2, -v2*v1, -v2])
    U, S, Vh = np.linalg.svd(DLT)
    #print(Vh[-1].reshape((3, 3)))
    return Vh[-1].reshape((3, 3))
    
def norm_homography(points1,points2):
    points1,m1=norm(points1)
    points2,m2=norm(points2)
    H=homography(points1,points2)
    
    return np.matmul(np.linalg.inv(m2), np.matmul(H, m1))


def norm(point):
    
    matrix=np.array([[np.std(point)/np.sqrt(2),0,np.mean(point[:,0])],
                  [0,np.std(point)/np.sqrt(2),np.mean(point[:,1])],
                  [0,0,1]])
    matrix=np.linalg.inv(matrix)


    point=np.concatenate((point,np.expand_dims(np.ones(point.shape[0]),axis=1)),axis=1)
    point=point.T
    point=matrix.dot(point)
    
    return point[0:2].T, matrix

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('[USAGE] python3 mouse_click_example.py [IMAGE PATH]')
        sys.exit(1)

    img = cv.imread(sys.argv[1])
    img=cv.resize(img, (0,0), fx=0.2, fy=0.2) 
    
    h,w,_=img.shape
    points2 = np.array([[0, 0],[0, w-1],[h-1, w-1],[h-1, 0]])
    
    points1= []
    cv.namedWindow(WINDOW_NAME)
    cv.setMouseCallback(WINDOW_NAME, on_mouse, [points1])
    while True:
        img_ = img.copy()
        for i, p in enumerate(points1):
            # draw points on img_
            cv.circle(img_, tuple(p), 2, (0, 255, 0), -1)
        cv.imshow(WINDOW_NAME, img_)

        key = cv.waitKey(20) % 0xFF
        if key == 27: break # exist when pressing ESC

    cv.destroyAllWindows()

    points1=np.array(points1)
    H=norm_homography(points2,points1)
    
    img2 = np.zeros((h, w, 3))
    for i in range(h):
        for j in range(w):
            x, y, z = np.matmul(H,np.array([i, j, 1]))

            x=np.clip(x/z,0,923)
            y=np.clip(y/z,0,692)
            img2[i, j]= (int(x+1)-x)*(int(y+1)-y) * img[int(y), int(x)] + \
                        (x-int(x))*(int(y+1)-y) * img[int(y), int(x+1)] + \
                        (int(x+1)-x)*(y-int(y)) * img[int(y+1), int(x)] + \
                        (x-int(x))*(y-int(y)) * img[int(y+1), int(x+1)]

        cv.imwrite("rectified result.png",img2)

