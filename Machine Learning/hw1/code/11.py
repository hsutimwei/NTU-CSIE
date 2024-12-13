import numpy as np
import matplotlib.pyplot as plt

a=np.genfromtxt("hw1_train.dat", delimiter=" ")
a=np.insert(a,12, 11.26,axis=1)

l=[]
for i in range(1000):
    
    np.random.seed(i)
    
    w=np.zeros(13)
    
    cnt=0 #need 5*256=1024 times
    totalcnt=0
    while True:
        
        index = np.random.randint(0, 256)
        
        sign=np.sign(w.transpose().dot(a[index][0:13]))
        
        if sign!=a[index][13]:
            cnt=0
            w+=a[index][13]*a[index][0:13]
        else:
            cnt+=1
        totalcnt+=1
        if cnt==1024:
            break
        
    l+=[totalcnt]
    print(f"{i}'th run",end="\r")
    
plt.hist(l, bins='auto')
plt.savefig("11.png")
print(np.median(l))