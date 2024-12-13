from scipy.spatial.transform import Rotation as R
import pandas as pd
import numpy as np
import cv2
import time
from tqdm import tqdm
import random
from scipy.spatial import distance

import open3d as o3d
from scipy.linalg import solve



points3D_df = pd.read_pickle("data/points3D.pkl")
data=pd.read_pickle("data/result.pkl")
"""data = {
    "groundtruthR": rotq_gt,
    "groundtruthT": tvec_gt,
    "rotqs": rotqs,
    "tvecs": tvecs
}"""
rotqs=np.array(data["rotqs"])
tvecs=np.array(data["tvecs"])
corner=np.array([[0,0,0,1],
                [0.3,0.3,1,1],
                [0.3,-0.3,1,1],
                [-0.3,0.3,1,1],
                [-0.3,-0.3,1,1]])
cameraMatrix = np.array([[1868.27,0,540],[0,1869.18,960],[0,0,1]]) 
cameras=np.empty((0,5,4))
for rvec,tvec in zip(rotqs,tvecs):
    m=np.concatenate((R.as_matrix(R.from_quat(rvec))[0],tvec.T),axis=1)
    m=np.linalg.inv(np.concatenate((m, [[0, 0, 0, 1]]), axis = 0))
    pyramid=m @ corner.T
    #print(pyramid/pyramid[-1])
    cameras=np.append(cameras,[(pyramid/pyramid[-1]).T],axis=0)

lines=[]
lcolor=[]
for i in range(0,len(cameras),5):
    lines.append(np.array([i, i + 5]))
    lcolor.append(np.array([0, 0, 0]))
    for j in [1,2,3,4]:
        lines.append(np.array([i, i + j]))
        lcolor.append(np.array([0, 0, 0]))
    for j in [1,3]:
        lines.append(np.array([i+j, i + j+1]))
        lcolor.append( np.array([0, 0, 0]))
    lines.append(np.array([i+4, i+2]))
    lcolor.append(np.array([0, 0, 0]))
    lines.append(np.array([i+3, i+1]))
    lcolor.append(np.array([0, 0, 0]))
    

line_set = o3d.geometry.LineSet()
#print(cameras.reshape((len(cameras)*5,4)))
line_set.points = o3d.utility.Vector3dVector(cameras.reshape((len(cameras)*5,4))[:,:3])
#print(np.array(lines).shape)
line_set.lines = o3d.utility.Vector2iVector(np.array(lines))
line_set.colors = o3d.utility.Vector3dVector(np.array(lcolor))

 
ntu=o3d.geometry.PointCloud()
ntu.points = o3d.utility.Vector3dVector(np.array(points3D_df["XYZ"].to_list()))
ntu.colors = o3d.utility.Vector3dVector(np.array(points3D_df["RGB"].to_list()) / 255)

o3d.visualization.draw_geometries([line_set],width=960,height=540)


