import cv2 as cv
import numpy as np
from scipy.spatial.transform import Rotation as R
import sys, os
import pandas as pd


def get_transform_mat(rotation, translation, scale):
    r_mat = R.from_euler('xyz', rotation, degrees=True).as_matrix()
    scale_mat = np.eye(3) * scale
    transform_mat = np.concatenate([scale_mat @ r_mat, translation.reshape(3, 1)], axis=1)
    return transform_mat

data=pd.read_pickle("data/result.pkl")
"""data = {
    "groundtruthR": rotq_gt,
    "groundtruthT": tvec_gt,
    "rotqs": rotqs,
    "tvecs": tvecs
}"""
rotqs=np.array(data["rotqs"])
tvecs=np.array(data["tvecs"])
groundtruthR=np.array(data["groundtruthR"])
groundtruthT=np.array(data["groundtruthT"])
points = np.load('cube_vertices.npy')
color=np.array([[0,0,0],[0,0,255],
                [0,255,0],[255,0,0],
                [0,255,255],[255,255,0],
                [255,0,255],[255,255,255]])
for i in np.arange(0,1.1,0.05):
    for j in np.arange(0,1.1,0.05):
        for k in np.arange(0,1.1,0.05):
            if k==0:
                points=np.append(points,[[i,j,k]],axis=0)
                color=np.append(color,[[0,0,255]],axis=0)
            elif k==1:
                points=np.append(points,[[i,j,k]],axis=0)
                color=np.append(color,[[0,255,0]],axis=0)
            elif j==0:
                points=np.append(points,[[i,j,k]],axis=0)
                color=np.append(color,[[255,0,0]],axis=0)
            elif j==1:
                points=np.append(points,[[i,j,k]],axis=0)
                color=np.append(color,[[0,255,255]],axis=0)
            elif i==0:
                points=np.append(points,[[i,j,k]],axis=0)
                color=np.append(color,[[255,0,255]],axis=0)
            elif i==1:
                points=np.append(points,[[i,j,k]],axis=0)
                color=np.append(color,[[255,255,255]],axis=0)

images_df = pd.read_pickle("data/images.pkl")
train_img = images_df[images_df['NAME'].str.startswith('valid') == True]
idxs=train_img["IMAGE_ID"].to_list()

cameraMatrix = np.array([[1868.27,0,540],[0,1869.18,960],[0,0,1]]) 
video = cv.VideoWriter("ntu.mp4", cv.VideoWriter_fourcc(*'mp4v'), 15, (1080, 1920))
for i in range(len(idxs)):
    
    img = cv.imread("data/frames/"+f"valid_img{i*5+5}.jpg")
    id = images_df[images_df['NAME']==f"valid_img{i*5+5}.jpg"]["IMAGE_ID"]
    id=np.where(idxs==np.array(id)[0])[0]

    """ground_truth = images_df.loc[images_df["IMAGE_ID"]==id[0]]

    rvec=R.as_matrix(R.from_quat(ground_truth[["QX","QY","QZ","QW"]].values))
    tvec=np.array([ground_truth[["TX","TY","TZ"]].values[0]]).T"""
    rvec=R.as_matrix(R.from_quat(rotqs[id][0]))[0]
    tvec=tvecs[id][0].T

    matrix=cameraMatrix @ np.concatenate((rvec,tvec),axis=1)
    
    for j in range(len(points)):
        point=matrix @ np.append(points[j],1)
        point=point/point[-1]
        if 0<=point[0]<=1080 and 0<=point[1]<=1920:
            img = cv.circle(img, point.astype(int)[:2], 6, tuple(( int (color[j] [ 0 ]), int (color[j] [ 1 ]), int (color[j] [ 2 ]))))
    video.write(img)

video.release()