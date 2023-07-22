from typing import Dict, List
import torch
from torch.utils.data import Dataset
from torch.nn.utils.rnn import pad_sequence
import datasets
import json
class TrainDataset(Dataset):
    def __init__(self, data: List[Dict]):
        self.data: List[Dict] = data
        
    
    def __len__(self)->int:
        return len(self.data)
        
    def __getitem__(self, index):
        return self.data[index]
    
    def collate_fn(self,data: List[Dict]):
        inputs=[i["inputs"] for i in data]
        attention_masks=[i["attention_masks"] for i in data]
        tokens_type=[i["tokens_type"] for i in data]
        inputs = pad_sequence(inputs, batch_first=True)
        attention_masks = pad_sequence(attention_masks, batch_first=True)
        tokens_type = pad_sequence(tokens_type, batch_first=True)
        if "label" in data[0].keys():
            label=[i["label"] for i in data]
            label = torch.stack(label)
            label = torch.flatten(label)
            return inputs, attention_masks, tokens_type, label
        return inputs, attention_masks, tokens_type

class Mydataset(datasets.GeneratorBasedBuilder):
   #cite:https://blog.csdn.net/qq_42388742/article/details/114293746
    def _info(self):
       return datasets.DatasetInfo(
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answers": datasets.features.Sequence(
                        {"text": datasets.Value("string"),"answer_start": datasets.Value("int32")}
                    ),
                }
            ),supervised_keys=None
        )

    def _split_generators(self, filepath):

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": self.config.data_files['train']}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": self.config.data_files['validation']}),
        ]

    def _generate_examples(self, filepath):
        data_name = filepath[0]
        
        context_path = "./data/context.json"
        data_path = open(data_name , encoding = "utf-8")
        context = open(context_path , encoding = "utf-8")
        all_data = json.load(data_path)
        context_data = json.load(context)
        for data in all_data:
          id = data['id']
          question = data['question']
          context = context_data[data['relevant']]
          answer_starts = [data['answer']["start"]]
          text = [data['answer']["text"]]
          yield id,{
            "id": id,
            "question": question,
            "context": context,
            "answers": {"answer_start": answer_starts,"text": text},
            }
        