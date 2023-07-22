import json
import pickle
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Dict
import csv
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

from dataset import SeqTaggingClsDataset
from model import SeqTagger
from utils import Vocab


def main(args):
    with open(args.cache_dir / "vocab.pkl", "rb") as f:
        vocab: Vocab = pickle.load(f)

    tag_idx_path = args.cache_dir / "tag2idx.json"
    tag2idx: Dict[str, int] = json.loads(tag_idx_path.read_text())
    tag2idx["pad"]=9
    data = json.loads(args.test_file.read_text())
    dataset = SeqTaggingClsDataset(data, vocab, tag2idx, args.max_len)
    # TODO: crecate DataLoader for test dataset
    test_loader = DataLoader(dataset = dataset,batch_size = args.batch_size,shuffle = False,num_workers = 2, collate_fn=dataset.collate_fn)
    
    embeddings = torch.load(args.cache_dir / "embeddings.pt")

    model = SeqTagger(
        embeddings,
        args.hidden_size,
        args.num_layers,
        args.dropout,
        args.bidirectional,
        dataset.num_classes,
    )
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    model.load_state_dict(torch.load(args.ckpt_path))
    model = model.to(device)
    model.eval()
    id = [ id['id'] for id in data]
    predict_label = []
    with torch.no_grad():
        for i, (inputs, lens) in enumerate(test_loader):
            inputs = inputs.to(device)
            outputs = model(inputs,lens)
            predict = torch.argmax(outputs , dim = 2)
            predict_output = predict.int().tolist()
            for predict in predict_output:
                predict_label.append([dataset.idx2label[tag]  for tag in predict if tag!=9])
                #print(predict_label)

    
    
    
    with open(args.pred_file, 'w+' , encoding="utf-8", newline='') as fp:
      wr = csv.writer(fp)
      wr.writerow(("id", "tags"))
      for i in range(len(data)):
          s=''
          for j in predict_label[i]:
              s+=j
              s+=' '
          s=s.strip()
          wr.writerow((id[i],s))
    fp.close()
    


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "--test_file",
        type=Path,
        help="Path to the test file.",
        default="./data/slot/test.json",
    )
    parser.add_argument(
        "--cache_dir",
        type=Path,
        help="Directory to the preprocessed caches.",
        default="./cache/slot/",
    )
    parser.add_argument(
        "--ckpt_path",
        type=Path,
        help="Path to model checkpoint.",
        default="./ckpt/slot/intent.model",
    )
    parser.add_argument("--pred_file", type=Path, default="pred.slot.csv")

    # data
    parser.add_argument("--max_len", type=int, default=128)

    # model
    parser.add_argument("--hidden_size", type=int, default=512)
    parser.add_argument("--num_layers", type=int, default=2)
    parser.add_argument("--dropout", type=float, default=0.1)
    parser.add_argument("--bidirectional", type=bool, default=True)

    # data loader
    parser.add_argument("--batch_size", type=int, default=128)

    parser.add_argument(
        "--device", type=torch.device, help="cpu, cuda, cuda:0, cuda:1", default="cpu"
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    main(args)