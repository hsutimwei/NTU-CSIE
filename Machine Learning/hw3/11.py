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


def logistic(X,y):
    w=np.zeros(3)
    for i in range(500):
        grad=np.zeros(3)
        for j in range(256):
            grad+=1/(1+np.exp(y[j]*np.dot(X[j],w)))*(-y[j]*X[j])
        w=w-0.1*grad/256
    return w


l=[]
lo=[]
for i in range(128):
    np.random.seed(i)
    X,y,xout,yout=generate()
    
    w=np.linalg.inv(X.T @ X) @ X.T @ y
    cnt=0
    
    X_pred=xout@w
    for j in range(4096):
        if np.sign(X_pred[j])!=np.sign(yout[j]):
            cnt+=1

    err = cnt/4096

    l.append(err)
    
    cnt=0
    w=logistic(X,y)
    X_pred=xout@w
    for j in range(4096):
        if np.sign(X_pred[j])!=np.sign(yout[j]):
            cnt+=1
            
    err = cnt/4096
    
    lo.append(err)
    print(i,end="\r")
    
plt.scatter(range(128),l,c="r",label="linear")
plt.scatter(range(128),lo,c="b",label="logistic")
plt.legend()
plt.savefig("11.png")
print(np.median(l))
print(np.median(lo))