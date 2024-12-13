from scipy.spatial.transform import Rotation as R
import pandas as pd
import numpy as np
import cv2
import time
from tqdm import tqdm
import random
from scipy.spatial import distance


images_df = pd.read_pickle("data/images.pkl")
train_df = pd.read_pickle("data/train.pkl")
points3D_df = pd.read_pickle("data/points3D.pkl")
point_desc_df = pd.read_pickle("data/point_desc.pkl")

def average(x):
    return list(np.mean(x,axis=0))

def average_desc(train_df, points3D_df):
    train_df = train_df[["POINT_ID","XYZ","RGB","DESCRIPTORS"]]
    desc = train_df.groupby("POINT_ID")["DESCRIPTORS"].apply(np.vstack)
    desc = desc.apply(average)
    desc = desc.reset_index()
    desc = desc.join(points3D_df.set_index("POINT_ID"), on="POINT_ID")
    return desc

def pnpsolver(query,model,cameraMatrix=0,distortion=0):
    kp_query, desc_query = query
    kp_model, desc_model = model

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(desc_query,desc_model,k=2)

    gmatches = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            gmatches.append(m)

    points2D = np.empty((0,2))
    points3D = np.empty((0,3))

    for mat in gmatches:
        query_idx = mat.queryIdx
        model_idx = mat.trainIdx
        points2D = np.vstack((points2D,kp_query[query_idx]))
        points3D = np.vstack((points3D,kp_model[model_idx]))

    cameraMatrix = np.array([[1868.27,0,540],[0,1869.18,960],[0,0,1]])    
    distCoeffs = np.array([0.0847023,-0.192929,-0.000201144,-0.000725352])

    return solvePnPRansac(points3D, points2D, cameraMatrix, distCoeffs)

def DLT(points3D, points2D, cameraMatrix, distCoeffs):
    # cited: https://zhuanlan.zhihu.com/p/58648937
    # cited: https://github.com/ydsf16/PnP_Solver/blob/master/pnp_solver.cpp
    l = []
    for i in range(len(points3D)):
        x, y, z, _ = points3D[i]
        u, v, _ = points2D[i]

        cx, cy = cameraMatrix[0, 2], cameraMatrix[1, 2]
        fx, fy = cameraMatrix[0, 0], cameraMatrix[1, 1]
        
        l.append([x * fx, y * fx, z * fx, fx, 0, 0, 0, 0, x * (cx-u), y * (cx-u), z * (cx-u), cx-u])
        l.append([0, 0, 0, 0, x * fy, y * fy, z * fy, fy, x * (cy-v), y * (cy-v), z * (cy-v), cy-v])

    U, S, VH1 = np.linalg.svd(l)
    
    U, S, VH = np.linalg.svd([[VH1[-1, 0], VH1[-1, 1], VH1[-1, 2]],
                             [VH1[-1, 4], VH1[-1, 5], VH1[-1, 6]],
                             [VH1[-1, 8],VH1[-1, 9], VH1[-1, 10]]])
    R = U @ VH
    t = np.array([[VH1[-1, 3]], [VH1[-1, 7]], [VH1[-1, 11]]]) / (np.sum(S) / 3)
    
    if (x * VH1[-1, 8] + y * VH1[-1, 9] + z * VH1[-1, 10] + VH1[-1, 11]) / (np.sum(S) / 3) < 0:
        R = -R
        t=-t
        
    return R, t

def solvePnPRansac(points3D, points2D, cameraMatrix, distCoeffs):
    
    error=float("inf")
    bestR=None
    bestT=None
    bestin=0
    bestinliers=None
    #points2D = cv2.undistortImagePoints(points2D, cameraMatrix, distCoeffs).reshape(len(points2D),2)
    points2D = np.insert(points2D, 2, 1,axis=1)
    points3D = np.insert(points3D, 3, 1,axis=1)
    for i in range(50):
        idxs = random.sample(range(points2D.shape[0]), 7)
        #idxs=[3335, 3127, 1136]
        
        rvec, tvec = DLT(points3D[idxs], points2D[idxs], cameraMatrix, distCoeffs)
        
        homo = cameraMatrix @ np.concatenate((rvec,tvec),axis=1) @ points3D.T
        
        homo= (homo/homo[2])[:2].T#(?,2)
        evec=np.sum((homo-points2D[:,:2])**2,axis=1)**0.5
        err=np.sum(evec)/len(evec)
        
        inliers=len(evec[evec<=10])

        if inliers>bestin:
            bestR=rvec
            bestT=tvec
            bestin=inliers
            bestinliers=np.where(evec<=10)[0]

    rvec, tvec = DLT(points3D[bestinliers], points2D[bestinliers], cameraMatrix, distCoeffs)
    return R.from_matrix(bestR).as_rotvec(),bestT,bestin

def solveP3P(points3D, points2D, cameraMatrix, distCoeffs):
    
    points2D=(np.linalg.inv(cameraMatrix) @ points2D.T).T

    Cab, Cac, Cbc = distance.cosine(points2D[0], points2D[1]), distance.cosine(points2D[0], points2D[2]), distance.cosine(points2D[1], points2D[2])
    Rab, Rac, Rbc = distance.euclidean(points3D[0], points3D[1]), distance.euclidean(points3D[0], points3D[2]), distance.euclidean(points3D[1], points3D[2])

    K1=(Rbc / Rac)**2
    K2=(Rbc / Rab)**2
    
    G4 = (K1 * K2 - K1 - K2) ** 2 - 4 * K1 * K2 * (Cbc ** 2)
    G3 = 4 * (K1 * K2 - K1 - K2) * K2 * (1 - K1) * Cab + 4 * K1 * Cbc * ((K1 * K2 - K1 + K2) * Cac + 2 * K2 * Cab * Cbc)
    G2 = (2 * K2 * (1 - K1) * Cab) ** 2 + 2 * (K1 * K2 - K1 - K2) * (K1 * K2 + K1 - K2) + 4 * K1 * ((K1 - K2) * (Cbc ** 2) + K1 * (1 - K2) * (Cac ** 2) - 2 * (1 + K1) * K2 * Cab * Cac * Cbc)
    G1 = 4 * (K1 * K2 + K1 - K2) * K2 * (1 - K1) * Cab + 4 * K1 * ((K1 * K2 - K1 + K2) * Cac * Cbc + 2 * K1 * K2 * Cab * Cac ** 2)
    G0 = (K1 * K2 + K1 - K2) ** 2 - 4 * (K1 ** 2) * K2 * (Cac ** 2)
    
    roots=np.roots([G4,G3,G2,G1,G0])

    roots=roots[np.isreal(roots)].real
    bestT=[]
    bestR=[]

    
    for x in roots:

        m=1-K1
        m_=1
        p=2*(K1*Cac-x*Cbc)
        p_=2*(-x*Cbc)
        q=x**2-K1
        q_=x**2*(1-K2)-K2+2*x*K2*Cab
        y = -(p_ * q - p * q_) / (m_*q - m*q_)
        a = np.sqrt(max(0,((Rab ** 2) / (1+ x ** 2 - 2 * x * Cab))))
        b = x*a
        c=y*a
        
        # cited: https://en.wikipedia.org/wiki/True-range_multilateration#Three_Cartesian_dimensions,_three_measured_slant_ranges
        
        p1 = points3D[1]-points3D[0]
        p2 = points3D[2]-points3D[0]

        Xn = (p1)/np.linalg.norm(p1)

        tmp = np.cross(p1, p2)

        Zn = (tmp)/np.linalg.norm(tmp)

        Yn = np.cross(Xn, Zn)

        i = np.dot(Xn, p2)
        d = np.dot(Xn, p1)
        j = np.dot(Yn, p2)

        X = ((a**2)-(b**2)+(d**2))/(2*d)
        Y = (((a**2)-(c**2)+(i**2)+(j**2))/(2*j))-((i/j)*(X))
        Z1 = np.sqrt(max(0, a**2-X**2-Y**2))
        Z2 = -Z1 

        t1 = points3D[0] + X * Xn + Y * Yn + Z1 * Zn
        t2 = points3D[0] + X * Xn + Y * Yn + Z2 * Zn
        print(t1,t2)
        for t in [t1,t2]:
            V=np.empty((0,3))
            xt=np.empty((0,3))

            for i in range(3):
                
                V=np.concatenate((V,[np.linalg.norm(points3D[i] - t) / np.linalg.norm(points2D[i])*points2D[i]]),axis=0)
                xt=np.concatenate((xt,[points3D[i] - t]),axis=0)
            #print(np.linalg.det(V),np.linalg.det(xt))
            #exit()
            try:
                R = V.T @ np.linalg.inv(xt.T)
            except:
                R=np.zeros((3,3))
            if np.linalg.det(R)>0:
                bestT.append(t)
                bestR.append(R)


    return bestR,bestT
# Process model descriptors
desc_df = average_desc(train_df, points3D_df)
kp_model = np.array(desc_df["XYZ"].to_list())
desc_model = np.array(desc_df["DESCRIPTORS"].to_list()).astype(np.float32)

# Load quaery image
train_img = images_df[images_df['NAME'].str.startswith('valid') == True]
idxs=train_img["IMAGE_ID"].to_list()
rotqs=[]
tvecs=[]
rotq_gt=[]
tvec_gt=[]
angles=[]
dis=[]
for idx in tqdm(idxs):

    fname = ((images_df.loc[images_df["IMAGE_ID"] == idx])["NAME"].values)[0]
    rimg = cv2.imread("data/frames/"+fname,cv2.IMREAD_GRAYSCALE)

    # Load query keypoints and descriptors
    points = point_desc_df.loc[point_desc_df["IMAGE_ID"]==idx]
    kp_query = np.array(points["XY"].to_list())
    desc_query = np.array(points["DESCRIPTORS"].to_list()).astype(np.float32)

    # Find correspondance and solve pnp
    rvec, tvec, inliers = pnpsolver((kp_query, desc_query),(kp_model, desc_model))
    rotqs.append(R.from_rotvec(rvec.reshape(1,3)).as_quat())
    tvecs.append(tvec.reshape(1,3))

    # Get camera pose groudtruth 
    ground_truth = images_df.loc[images_df["IMAGE_ID"]==idx]
    rotq_gt.append(ground_truth[["QX","QY","QZ","QW"]].values)
    tvec_gt.append(ground_truth[["TX","TY","TZ"]].values)
    theta=np.abs(ground_truth[["QX","QY","QZ","QW"]].values.dot((R.from_rotvec(rvec.reshape(1,3)).as_quat().T)))
    if -1<=theta<=1:
        angle = np.arccos(theta)
    else:
        angle=np.array([[0]])

    angles.append(angle)
    dis.append(np.sum((ground_truth[["TX","TY","TZ"]].values[0]-tvec.reshape(3))**2)**0.5)
    
#print(ground_truth[["QX","QY","QZ","QW"]].values, ground_truth[["TX","TY","TZ"]].values)
data = {
    "groundtruthR": rotq_gt,
    "groundtruthT": tvec_gt,
    "rotqs": rotqs,
    "tvecs": tvecs
}
my_dataframe = pd.DataFrame(data)
my_dataframe.to_pickle("./data/result.pkl")
print(np.median(angles), np.median(dis))
#print(np.sum(np.array(rotqs)-np.array(rotq_gt)),np.sum(np.array(tvecs)-np.array(tvec_gt)))
