import sys
import numpy as np
import cv2 as cv

def get_sift_correspondences(img1, img2):
    '''
    Input:
        img1: numpy array of the first image
        img2: numpy array of the second image

    Return:
        points1: numpy array [N, 2], N is the number of correspondences
        points2: numpy array [N, 2], N is the number of correspondences
    '''
    #sift = cv.xfeatures2d.SIFT_create()# opencv-python and opencv-contrib-python version == 3.4.2.16 or enable nonfree
    sift = cv.SIFT_create()             # opencv-python==4.5.1.48
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    matcher = cv.BFMatcher()
    matches = matcher.knnMatch(des1, des2, k=2)
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    good_matches = sorted(good_matches, key=lambda x: x.distance)
    k=20
    good_matches=good_matches[:k]
    points1 = np.array([kp1[m.queryIdx].pt for m in good_matches])
    points2 = np.array([kp2[m.trainIdx].pt for m in good_matches])
    
    img_draw_match = cv.drawMatches(img1, kp1, img2, kp2, good_matches, None, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    img_draw_match=cv.resize(img_draw_match, (0,0), fx=0.3, fy=0.3) 
    """cv.imshow('match', img_draw_match)
    cv.waitKey(0)"""
    cv.imwrite(f'img_draw_match_k_{k}.png', img_draw_match)
    return points1, points2

def err(p_s,p_t,H):
    
    ans=0
    l=len(p_s)
    
    p_s=np.concatenate((p_s,np.expand_dims(np.ones(p_s.shape[0]),axis=1)),axis=1)
    Hp=np.matmul(H,p_s.T)
   
    Hp[0:2]=Hp[0:2]/Hp[2]
    
    Hp=Hp.astype(np.longlong)
    
    square=np.square(Hp[:2]-p_t.T)
    return np.sqrt(square[0]+square[1]).sum()/len(p_t)
    

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

def run(points1,points2,DLT):
    
    for i in range(10000):
        
        H=DLT(points1,points2)

if __name__ == '__main__':
    img1 = cv.imread(sys.argv[1])
    img2 = cv.imread(sys.argv[2])
    gt_correspondences = np.load(sys.argv[3])
    p_s = gt_correspondences[0]
    p_t = gt_correspondences[1]
   
    points1, points2 = get_sift_correspondences(img1, img2)
    
    # DLT
    H=homography(points1,points2)
    
    error=err(p_s,p_t,H)

    print(f"error for DLT: {error}")
    
    H=norm_homography(points1,points2)
    
    error=err(p_s,p_t,H)

    print(f"error for normalized DLT: {error}")
    