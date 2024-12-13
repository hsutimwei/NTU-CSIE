from libsvm.svmutil import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

y_train, X_train = svm_read_problem("train.txt")
y_train=np.array(y_train)
y_train[y_train != 1] = -1

ans=10000000000
C_ans=0
c=[]
for i in range(1000):
    print(i)
    np.random.seed(i)
    x_train, x_valid, Y_train, Y_valid = train_test_split(X_train, y_train, test_size=200/4435, random_state=i)
    for C in [0.01, 0.1, 1, 10, 100]:
        model = svm_train(Y_train, x_train, f'-c {C} -s 0 -t 2 -g 1')
        p_labels, p_acc, p_vals = svm_predict(Y_valid, x_valid, model)
        Evalid = 100 - p_acc[0]
        if Evalid<ans:
            ans=Evalid
            C_ans=C
    c.append(C_ans)


unique, counts = np.unique(c, return_counts=True)

d=dict(zip(unique, counts))
print(d)

CC = ["0.01", "0.1", "1", "10", "100"]      
h = [0,0,1000,0,0]   
plt.bar(CC,h)
plt.savefig("11.png")
