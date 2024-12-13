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
    
    for lam in [-6,-4,-2,0,2]:
        C=1/(10**lam)/2
        np.random.shuffle(a)
        X_train, X_valid = a[:120,:6], a[120:,:6]
        y_train, y_valid = a[:120,6], a[120:,6]

        X_train=transform(X_train)
        X_valid=transform(X_valid)
        model = train(y_train, X_train, '-s 0 -c ' + str(C) + ' -e 0.000001 -q')
        pred, _, _ = predict(y_valid, X_valid, model)
        err=np.mean(y_valid != pred)
    
        if err<=error:
            error=err
            best=lam

    b.append(best)

plt.hist(b, bins="auto")
plt.savefig("11.png")