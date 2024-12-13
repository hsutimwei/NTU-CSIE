import numpy as np
import random
import matplotlib.pyplot as plt
import statistics 

def generate(i):
    np.random.seed(i)
    data=np.random.random_sample(8)*2-1
    data=np.sort(data)
    label=np.sign(data)
    for i in range(8):
        if random.randint(0,100)<10:
            label[i]=-1
    
    return data,label

All_thetas=[]
ALL_error=[]
ALL_errorout=[]
ALL_s=[]
for i in range(2000):
    data,label=generate(i)
    thetas=np.zeros(8)
    thetas[0]=-1

    for i in range(1,7):
        thetas[i]=(data[i-1]+data[i])/2
    
    min_error=1
    Theta=0
    S=0
    for theta in thetas:
        for s in [-1,1]:
            error=np.count_nonzero(s*np.where(data > theta, 1, -1) != label)/len(label)
            if min_error>error:
                min_error=error
                Theta=theta
                S=s
    All_thetas.append(Theta)
    ALL_error.append(min_error)
    ALL_s.append(S)
    ALL_errorout.append( 0.5- 0.4*S + 0.4*S*abs(Theta))
    
plt.scatter(range(2000),ALL_error,label="in")
plt.scatter(range(2000),ALL_errorout,label="out")
plt.legend()
plt.savefig("11.png")
ALL=[]
for i in range(2000):
    ALL.append(ALL_errorout[i]-ALL_error[i])
print(statistics.median(ALL))