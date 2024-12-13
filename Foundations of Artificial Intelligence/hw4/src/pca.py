import numpy as np
import matplotlib.pyplot as plt

"""
Implementation of Principal Component Analysis.
"""
class PCA:
    def __init__(self, n_components: int) -> None:
        self.n_components = n_components
        self.mean = None
        self.components = None

    def fit(self, X: np.ndarray) -> None:
        #TODO: 10%
        # Hint: Use existing method to calculate covariance matrix and its eigenvalues and eigenvectors
        self.mean=np.mean(X,axis=0)

        X_bar=X-self.mean#(135,4880)  
        X_bar=X_bar.T#(4880,40)  
        cov_mat = np.cov(X_bar)#np 想要(n_features,n_sample),4880*4880

        X_bar=X_bar.T
        
        eig_values, eig_vectors = np.linalg.eig(cov_mat)#cov_mat=eig_vectors@np.diag(eig_values)@eig_vectors.T
        e_indices=np.argsort(eig_values)[::-1]
        self.components=np.real(eig_vectors[:,e_indices][:,:self.n_components])
        
    def transform(self, X: np.ndarray) -> np.ndarray:
        #TODO: 2%
        # Hint: Use the calculated principal components to project the data onto a lower dimensional space
        return (X-np.mean(X,axis=0)) @ self.components 

    def reconstruct(self, X):
        #TODO: 2%
        # Hint: Use the calculated principal components to reconstruct the data back to its original space
        if X.ndim==1:
            X=np.array([X])
        return (X-np.mean(X,axis=0)) @ self.components @ self.components.T + np.mean(X,axis=0)
