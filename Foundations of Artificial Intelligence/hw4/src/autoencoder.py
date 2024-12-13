import torch
from tqdm.auto import tqdm
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader
import numpy as np
"""
Implementation of Autoencoder
"""
class Autoencoder(nn.Module):
    def __init__(self, input_dim: int, encoding_dim: int) -> None:
        """
        Modify the model architecture here for comparison
        """
        super(Autoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, encoding_dim),
            nn.Linear(encoding_dim, encoding_dim//2),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(encoding_dim//2, encoding_dim),
            nn.Linear(encoding_dim, input_dim),
        )
    
    def forward(self, x):
        #TODO: 5%
        # Hint: a forward pass includes one pass of encoder and decoder
        y = self.encoder(x)
        z = self.decoder(y)
        return z
    
    def fit(self, X ,epochs=10, batch_size=32):
        #TODO: 5%
        # Hint: a regular pytorch training includes:
        # 1. define optimizer
        optimizer = torch.optim.SGD(self.parameters(), lr=0.04)#0.07,0.48
        # 2. define loss function
        loss_function=nn.MSELoss()
        # 3. define number of epochs
        # 4. define batch size
        # 5. define data loader
        data_loader=DataLoader(X,batch_size=batch_size,shuffle=False)
        # 6. define training loop
        decoded=0
        for epoch in range(epochs):
            total_loss=0
            for data in data_loader:
                data=data.type(torch.float32)
                self.zero_grad()
                decoded = self(data)
                loss=loss_function(decoded,data)
                total_loss+=loss
                loss.backward()
                optimizer.step()
                
            total_loss/=len(data_loader)
            
            print(f'Epoch:{epoch+1}/{epochs} Loss:{total_loss.item()}',end="\r")
            
        print(f'Fishish! Loss:{total_loss.item()}')
        
        # 7. record loss history 
        # Note that you can use `self(X)` to make forward pass.

    
    def transform(self, X):
        #TODO: 2%
        #Hint: Use the encoder to transofrm X
        return self.encoder(torch.tensor(X,dtype=torch.float32)).clone().detach().numpy()
    
    def reconstruct(self, X):
        #TODO: 2%
        #Hint: Use the decoder to reconstruct transformed X
        return self.forward(torch.tensor(X,dtype=torch.float32)).clone().detach().numpy()


"""
Implementation of DenoisingAutoencoder
"""
class DenoisingAutoencoder(Autoencoder):
    def __init__(self, input_dim, encoding_dim, noise_factor=0.2):
        super(DenoisingAutoencoder, self).__init__(input_dim,encoding_dim)
        self.noise_factor = noise_factor
    
    def add_noise(self, x):
        #TODO: 3%
        #Hint: Generate Gaussian noise with noise_factor
        return x+np.random.normal(0, self.noise_factor, len(x))
    
    def fit(self, X, epochs=10, batch_size=32):
        #TODO: 4%
        #Hint: Follow the same procedure above but remember to add_noise before training.
        optimizer = torch.optim.SGD(self.parameters(), lr=0.04)#0.07,0.48

        loss_function=nn.MSELoss()

        for i in range(len(X)):
            X[i]=self.add_noise(X[i])
            
        data_loader=DataLoader(X,batch_size=batch_size,shuffle=False)
        decoded=0
        for epoch in range(epochs):
            total_loss=0
            for data in data_loader:
                data=data.type(torch.float32)
                self.zero_grad()
                decoded = self(data)
                loss=loss_function(decoded,data)
                total_loss+=loss
                loss.backward()
                optimizer.step()
                
            total_loss/=len(data_loader)
            
            print(f'Epoch:{epoch+1}/{epochs} Loss:{total_loss.item()}',end="\r")
        print(f'Fishish! Loss:{total_loss.item()}')
