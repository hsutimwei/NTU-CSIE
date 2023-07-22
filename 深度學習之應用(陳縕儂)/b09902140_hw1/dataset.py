from typing import List, Dict

from torch.utils.data import Dataset

from utils import Vocab
from utils import pad_to_len
import torch

class SeqClsDataset(Dataset):
    def __init__(
        self,
        data: List[Dict],
        vocab: Vocab,
        label_mapping: Dict[str, int],
        max_len: int,
    ):
        self.data = data
        self.vocab = vocab
        self.label_mapping = label_mapping
        self._idx2label = {idx: intent for intent, idx in self.label_mapping.items()}
        self.max_len = max_len

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, index) -> Dict:
        return self.data[index]


    @property
    def num_classes(self) -> int:
        return len(self.label_mapping)

    def collate_fn(self, samples: List[Dict]) -> Dict:
        batch = {}
        batch['text'] = [data['text'].split() for data in samples]
        batch['text'] = self.vocab.encode_batch(batch['text'] , self.max_len)
        batch['text'] = torch.LongTensor(batch['text'])

        if 'intent' in samples[0].keys():
            batch['intent'] = [data['intent'] for data in samples]
            #print(len(batch['intent'])) // batch_size
            batch['intent'] = [self.label2idx(intent) for intent in batch['intent']]
            batch['intent'] = torch.LongTensor(batch['intent'])
            return batch['text'],batch['intent']
        return batch['text']
    
    def label2idx(self, label: str):
        return self.label_mapping[label]

    def idx2label(self, idx: int):
        return self._idx2label[idx]


class SeqTaggingClsDataset(Dataset):
    def __init__(
        self,
        data: List[Dict],
        vocab: Vocab,
        label_mapping: Dict[str, int],
        max_len: int,
    ):
        self.data = data
        self.vocab = vocab
        self.label_mapping = label_mapping
        self.idx2label = {idx: tag for tag, idx in self.label_mapping.items()}
        self.max_len = max_len

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, index):
            return self.data[index]

    @property
    def num_classes(self) -> int:
        return len(self.label_mapping)

    def collate_fn(self, samples: List[Dict]):
        # TODO: implement collate_fn
        text = [data['tokens'] for data in samples]
        text = self.vocab.encode_batch(text , self.max_len)
        text = torch.LongTensor(text)
        lens = [len(data['tokens']) for data in samples]
        #print(text.shape)
        if 'tags' in samples[0].keys():
            labels = [[self.label2idx(tag) for tag in data['tags']] for data in samples]
            labels = pad_to_len(labels, self.max_len, 9)
            #print(labels)
            labels = torch.LongTensor(labels)#[batch,max_len]
            return text , labels, lens
        return text, lens
            
    def label2idx(self, label: str):
        return self.label_mapping[label]

    def idx2label(self, idx: int):
        return self.idx2label[idx]
