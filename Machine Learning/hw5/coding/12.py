from libsvm.svmutil import *
import numpy as np
import matplotlib.pyplot as plt
y_train, X_train = svm_read_problem("train.txt")
y_train=np.array(y_train)
y_train[y_train != 3] = -1
y_train[y_train == 3] = 1
ans=10000000000
C_ans=0

y=[]
for C in [0.01, 0.1, 1, 10, 100]:
    model = svm_train(y_train, X_train, f'-c {C} -s 0 -t 2 -g 1')
    support_vector_coefficients = model.get_sv_coef()
    y.append(np.linalg.norm(support_vector_coefficients))
    print(C,np.linalg.norm(support_vector_coefficients))
    
x = ["0.01", "0.1", "1", "10", "100"]
plt.plot(x, y)
plt.savefig("12.png")