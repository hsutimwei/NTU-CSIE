from liblinear.liblinearutil import *
import numpy as np

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

best=0
error=float("inf")
for lam in [-6,-4,-2,0,2]:
    C=1/(10**lam)/2
    X_train=a[:,:6]
    y_train=a[:,6]
    X_train=transform(X_train)

    model = train(y_train, X_train, '-s 0 -c ' + str(C) + ' -e 0.000001')
    pred, _, _ = predict(y_train, X_train, model)
    err=np.mean(y_train != pred)
    if err<=error:
        error=err
        best=lam

print(best)