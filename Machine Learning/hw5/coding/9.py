from libsvm.svmutil import *
import numpy as np

y_train, X_train = svm_read_problem("train.txt")
y_train=np.array(y_train)
y_train[y_train != 4] = -1
y_train[y_train == 4] = 1

num=10000000000
for C in [0.1, 1, 10]:
    for Q in [2,3,4]:
        model = svm_train(y_train, X_train, f'-c {C} -s 0 -t 1 -d {Q} -g 1 -r 1')
        num_sv = model.get_nr_sv()
        print(f"C:{C}, Q:{Q}, num_sv={num_sv}")
        if num>num_sv:
            num=num_sv
            
print(num)
        