from typing import Dict

import torch
from torch.nn import Embedding
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
class SeqClassifier(torch.nn.Module):
    def __init__(
        self,
        embeddings: torch.tensor,
        hidden_size: int,
        num_layers: int,
        dropout: float,
        bidirectional: bool,
        num_class: int,
    ) -> None:
        super(SeqClassifier, self).__init__()
        self.embeddings = Embedding.from_pretrained(embeddings, freeze=False)
        # TODO: model architecture
        self.embedding_dim = embeddings.size(1)
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.dropout = dropout
        self.output_dim = num_class
        self.rnn = nn.LSTM(embeddings.size(1), hidden_size, num_layers = num_layers,bidirectional = bidirectional ,
        batch_first= True)
        self.classifier = nn.Sequential( nn.Dropout(dropout),
                                         nn.Linear(self.hidden_size * 256, self.output_dim) #self.hidden_size * 2 * max_len
                                        )
        self.LogSoftmax = nn.LogSoftmax(dim=1)
        
    @property
    def encoder_output_size(self) -> int:
        # TODO: calculate the output dimension of rnn
        raise NotImplementedError

    def forward(self, batch) -> Dict[str, torch.Tensor]:
        # TODO: implement model forward
        embed = self.embeddings(batch)# embed:[150,128,300]:[batch_size,max_len,list of one word]
        x, y  = self.rnn(embed,None)# [150,128,hidden_size * 2]
        #print(x.shape)
        #x = self.LogSoftmax(x) 
        x=x.reshape(100,-1)
        #x = torch.mean(x, dim = 1)
        #
        #x=x[:,-1,:]
        x = self.classifier(x)
        #print(x.shape)
        return x


class SeqTagger(torch.nn.Module):
    def __init__(
        self,
        embeddings: torch.tensor,
        hidden_size: int,
        num_layers: int,
        dropout: float,
        bidirectional: bool,
        num_class: int,
    ) -> None:
        super(SeqTagger, self).__init__()
        self.embeddings = Embedding.from_pretrained(embeddings, freeze=False)
        # TODO: model architecture
        self.embedding_dim = embeddings.size(1)
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.output_dim = num_class
        self.rnn = nn.LSTM(embeddings.size(1), hidden_size, num_layers = num_layers,bidirectional = bidirectional ,
        batch_first= True)
        self.classifier = nn.Sequential( nn.Dropout(dropout),
                                         nn.Linear(self.hidden_size * 2, self.output_dim)
                                        )

                                        

    @property
    def encoder_output_size(self) -> int:
        # TODO: calculate the output dimension of rnn
        raise NotImplementedError

    def forward(self, batch, x_lens):
        # TODO: implement model forward
        embed = self.embeddings(batch)# embed:[150,128,300]:[batch_size,max_len,list of one word]
        #x, y  = self.rnn(embed,None)# [150,128,hidden_size * 2]
        #x = nn.LogSoftmax(x) 
        #print(embed.shape) #[batch_size,max_len,embed]
        #x = torch.mean(x, dim = 1)
        
        #x=x[:,-1,:]
        
        x_packed = pack_padded_sequence(embed, x_lens, batch_first=True, enforce_sorted=False)
        output_packed, y = self.rnn(x_packed)
        outputs, output_lengths = pad_packed_sequence(output_packed, batch_first=True, total_length=128)
        outputs = self.classifier(outputs)
        #print(outputs)
        return outputs
