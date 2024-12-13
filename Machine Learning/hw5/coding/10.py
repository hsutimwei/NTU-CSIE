from libsvm.svmutil import *
import numpy as np

y_train, X_train = svm_read_problem("train.txt")
y_test, X_test = svm_read_problem("test.txt")
y_train=np.array(y_train)
y_test=np.array(y_test)
y_train[y_train != 1] = -1
y_test[y_test != 1] = -1

ans=10000000000
C_ans=0
for C in [0.01, 0.1, 1, 10, 100]:
    model = svm_train(y_train, X_train, f'-c {C} -s 0 -t 2 -g 1')
    p_labels, p_acc, p_vals = svm_predict(y_test, X_test, model)
    Eout = 100 - p_acc[0]
    if Eout<ans:
        ans=Eout
        C_ans=C
    print(ans,C)
        