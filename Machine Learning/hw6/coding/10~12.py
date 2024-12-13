from libsvm.svmutil import *
import numpy as np
import matplotlib.pyplot as plt 
from tqdm import tqdm
np.random.seed(0)


class DecisionTree:
    def __init__(self, max_depth: int = 5):
        self.max_depth = max_depth


    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        self.tree = self._build_tree(X, y, 0)

    def predict(self, X: np.ndarray) -> np.ndarray:
        return np.array([self._traverse_tree(x, self.tree) for x in X])

    def _build_tree(self, X: np.ndarray, y: np.ndarray, depth: int) -> dict:
        if depth >= self.max_depth or len(set(y)) == 1:
            return self._create_leaf(y)
        feature, threshold = self._find_best_split(X, y)
        left_child=self._build_tree(X[X[:,feature]<=threshold], y[X[:,feature]<=threshold], depth+1)
        right_child=self._build_tree(X[X[:,feature]>threshold], y[X[:,feature]>threshold], depth+1)
        return {
            "feature": feature,
            "threshold": threshold,
            "left": left_child,
            "right": right_child,
        }

    def _create_leaf(self, y: np.ndarray):

        return y[0]


    def _find_best_split(self, X: np.ndarray, y: np.ndarray) -> tuple[int, float]:
        best_gini = float("inf")
        best_feature = None
        best_threshold = None

        for feature in range(X.shape[1]): #1~8
            sorted_indices = np.argsort(X[:, feature])
            
            for i in range(1, len(X)):
                
                if X[sorted_indices[i - 1], feature] != X[sorted_indices[i], feature]:
                    threshold = (
                        X[sorted_indices[i - 1], feature]
                        + X[sorted_indices[i], feature]
                    ) / 2#就是挑個數字不一樣的，平均當邊界
                    mask = X[:, feature] <= threshold
                    left_y, right_y = y[mask], y[~mask]
                    gini = self._gini_index(left_y, right_y)#算最小的gini
                    if gini < best_gini:
                        best_gini = gini
                        best_feature = feature
                        best_threshold = threshold


        return best_feature, best_threshold

    def _gini_index(self, left_y: np.ndarray, right_y: np.ndarray) -> float:

        left=1
        lefty=set(left_y)
        lenl=len(left_y)
        for i in lefty:
            left-=((i==left_y).sum()/lenl)**2
            
        right=1
        righty=set(right_y)
        rightl=len(right_y)
        for i in righty:
            right-=((i==right_y).sum()/rightl)**2
            
        return (left*lenl+right*rightl)/(lenl+rightl)


    def _traverse_tree(self, x: np.ndarray, node: dict):
        if isinstance(node, dict):
            feature, threshold = node["feature"], node["threshold"]
            if x[feature] <= threshold:
                return self._traverse_tree(x, node["left"])
            else:
                return self._traverse_tree(x, node["right"])
        else:
            return node

class RandomForest:
    def __init__(
        self,
        n_estimators: int = 2000,
    ):

        self.n_estimators=n_estimators
        self.trees=np.array([DecisionTree() for i in range(self.n_estimators)])

        
    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        for tree in tqdm(self.trees):

            indices=np.random.choice(len(X),int(len(X)*0.5),replace=True)
            tree.fit(X[indices], y[indices])
            
        

    def predict10(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:

        Eout=[]
        for tree in self.trees:
            result=tree.predict(X)
            Eout.append(mean_squared_error(y, result))
            
        
        plt.hist(Eout,bins="auto")
        plt.savefig("10.png")
        plt.clf()

    def predict11(self, X_train, y_train, X_test,y_test) -> np.ndarray:

        Ein=[]
        Eout=[]
        for tree in self.trees:
            result=tree.predict(X_train)
            Ein.append(mean_squared_error(y_train, result))
            result=tree.predict(X_test)
            Eout.append(mean_squared_error(y_test, result))

        Gin=np.mean(Ein)
        Gout=np.mean(Eout)
        plt.scatter(Ein,Eout,c='b')
        plt.scatter(Gin,Gout,c='r')
        plt.savefig("11.png")
        plt.clf()

    def predict12(self, X_test,y_test) -> np.ndarray:


        Eout=[]
        Gout=[]
        for tree in self.trees:
            result=tree.predict(X_test)
            Eout.append(mean_squared_error(y_test, result))
            G=np.mean(Eout)
            Gout.append(G)


        plt.scatter(range(2000),Eout,c='b')
        plt.scatter(range(2000),Gout,c='r')
        plt.savefig("12.png")
        plt.clf()



def mean_squared_error(y_true, y_pred):

    return np.mean((y_true - y_pred)**2)



def main():
    y_train, X_train = svm_read_problem("train.txt")
    y_test, X_test = svm_read_problem("test.txt")
    X=[]
    for i in X_train:
        X.append([i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]])
    X_train=np.array(X)

    y_train=np.array(y_train)
    X=[]
    for i in X_test:
        X.append([i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]])
    X_test=np.array(X)
    y_test=np.array(y_test)
    decision_tree_classifier = RandomForest()
    decision_tree_classifier.fit(X_train, y_train)
    decision_tree_classifier.predict10(X_test,y_test)
    decision_tree_classifier.predict11(X_train, y_train, X_test,y_test)
    decision_tree_classifier.predict12(X_test,y_test)
    
    
if __name__ == "__main__":
    main()
