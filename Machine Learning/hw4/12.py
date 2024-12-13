from liblinear.liblinearutil import *
import numpy as np
import matplotlib.pyplot as plt
a=np.genfromtxt("hw4_train.dat", delimiter=" ")


def transform(X_train):
    X=[]
    for i in X_train:
        X_=[1.]
        for i1 in range(6):
            X_.append(i[i1])
        for i1 in range(6):
            for i2 in range(i1,6):
                    X_.append(i[i1]*i[i2])
        for i1 in range(6):
            for i2 in range(i1,6):
                for i3 in range(i2,6):
                    X_.append(i[i1]*i[i2]*i[i3])
        
        X.append(X_)
    X=np.array(X)

    
    return X

b=[]
for j in range(128):
    np.random.seed(j)
    best=0
    error=float("inf")
    np.random.shuffle(a)
    X_train=a[:,:6]
    y_train=a[:,6]
    X_train=transform(X_train)
    for lam in [-6,-4,-2,0,2]:
        C=1/(10**lam)/2
        err_all=0
        for i in range(5):
            
            X_valid = X_train[i*40:(i+1)*40]
            y_valid = y_train[i*40:(i+1)*40]
            
            x_train = np.delete(X_train,range(i*40,(i+1)*40),axis=0)
            Y_train = np.delete(y_train,range(i*40,(i+1)*40))
            
            model = train(Y_train, x_train, '-s 0 -c ' + str(C) + ' -e 0.000001 -q')
            pred, _, _ = predict(y_valid, X_valid, model)
            err=np.mean(y_valid != pred)
    
            err_all+=err
        if err_all<=error:
            error=err_all
            best=lam
    b.append(best)
    
print(b)
plt.hist(b, bins="auto")
plt.savefig("12.png")