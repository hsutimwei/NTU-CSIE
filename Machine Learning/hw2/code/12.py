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

    Theta=np.random.random_sample(1)[0]*2-1
    S=random.sample([-1,1],1)[0]
    min_error=np.count_nonzero(S*np.where(data > Theta, 1, -1) != label)/len(label)
    All_thetas.append(Theta)
    ALL_error.append(min_error)
    ALL_s.append(S)
    ALL_errorout.append( 0.5- 0.4*S + 0.4*S*abs(Theta))
    
plt.scatter(range(2000),ALL_error,label="in")
plt.scatter(range(2000),ALL_errorout,label="out")
plt.legend()
plt.savefig("12.png")
ALL=[]
for i in range(2000):
    ALL.append(ALL_errorout[i]-ALL_error[i])
print(statistics.median(ALL))