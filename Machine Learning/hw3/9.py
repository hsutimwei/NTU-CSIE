import numpy as np
import matplotlib.pyplot as plt

def generate():

    xin=np.empty((0,3))
    yin=np.empty((0))
    for i in range(256):
        y1=np.random.randint(2)

        if y1==0:
            mean = [3, 2]
            cov = [[0.4, 0], [0, 0.4]]
            x1= np.random.multivariate_normal(mean, cov, 1)

            xin=np.concatenate((xin,[[1.0,x1[0][0],x1[0][1]]]),axis=0)
            yin=np.concatenate((yin,[1]))
        elif y1==1:
            mean = [5, 0]
            cov = [[0.6, 0], [0, 0.6]]
            x1= np.random.multivariate_normal(mean, cov, 1)

            xin=np.concatenate((xin,[[1.0,x1[0][0],x1[0][1]]]),axis=0)
            yin=np.concatenate((yin,[-1]))

    xout=np.empty((0,3))
    yout=np.empty((0))
    for i in range(4096):
        y1=np.random.randint(2)

        if y1==0:
            mean = [3, 2]
            cov = [[0.4, 0], [0, 0.4]]
            x1= np.random.multivariate_normal(mean, cov, 1)

            xout=np.concatenate((xout,[[1.0,x1[0][0],x1[0][1]]]),axis=0)
            yout=np.concatenate((yout,[1]))
        elif y1==1:
            mean = [5, 0]
            cov = [[0.6, 0], [0, 0.6]]
            x1= np.random.multivariate_normal(mean, cov, 1)

            xout=np.concatenate((xout,[[1.0,x1[0][0],x1[0][1]]]),axis=0)
            yout=np.concatenate((yout,[-1]))
    
    return xin,yin,xout,yout

l=[]
for i in range(128):
    np.random.seed(i)
    X,y,xout,yout=generate()
    
    w=np.linalg.inv(X.T @ X) @ X.T @ y
    
    l.append(np.mean((X@w-y)**2))
    print(i,end="\r")
plt.hist(l,bins=128)
plt.savefig("9.png")
print(np.median(l))