import json
import pickle
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Dict
from model import SeqClassifier
import torch
from tqdm import trange
from torch.utils.data import DataLoader
from dataset import SeqClsDataset
from utils import Vocab

TRAIN = "train"
DEV = "eval"
SPLITS = [TRAIN, DEV]

def main(args):
    with open(args.cache_dir / "vocab.pkl", "rb") as f:
        vocab: Vocab = pickle.load(f)

    intent_idx_path = args.cache_dir / "intent2idx.json"
    intent2idx: Dict[str, int] = json.loads(intent_idx_path.read_text())

    data_paths = {split: args.data_dir / f"{split}.json" for split in SPLITS}
    data = {split: json.loads(path.read_text()) for split, path in data_paths.items()}
    
    datasets: Dict[str, SeqClsDataset] = {
        split: SeqClsDataset(split_data, vocab, intent2idx, args.max_len)
        for split, split_data in data.items()
    }
    # TODO: crecate DataLoader for train / dev datasets
    
    dataloaders: Dict[str, DataLoader] = {
        split: DataLoader(split_dataset, args.batch_size, shuffle=True, num_workers = 2, collate_fn=split_dataset.collate_fn)
        for split, split_dataset in datasets.items()
    }

    embeddings = torch.load(args.cache_dir / "embeddings.pt")
    #print(embeddings.shape)

    # TODO: init model and move model to target device(cpu / gpu)
    model = SeqClassifier(
        embeddings,
        args.hidden_size,
        args.num_layers,
        args.dropout,
        args.bidirectional,
        datasets[TRAIN].num_classes)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    # TODO: init optimizer

    print('\nstart training')

    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    criterion = torch.nn.CrossEntropyLoss()
    
    model.train()
    tlen = len(datasets[TRAIN].data) # len(dataset)/batch_size =15000個data/150的batch_size=100
    vlen = len(datasets[DEV].data)
    best_acc = 0
    
    epoch_pbar = trange(args.num_epoch, desc="Epoch")
    for epoch in epoch_pbar:
        total_loss, total_acc = 0, 0
        # TODO: Training loop - iterate over train dataloader and update model weights
        for i, (inputs, labels) in enumerate(dataloaders[TRAIN]):
            inputs = inputs.to(device) #(batch_size, max_len)
            labels = labels.to(device) #(batch_size, max_len)
            
            optimizer.zero_grad()
            outputs = model(inputs) #機率預測 (batch_size, outputs_dim)
            
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            predict=torch.argmax(outputs, 1)#把概率最大的挑出來
            correct = (predict == labels).sum().item()
            total_acc += (correct / args.batch_size)
            total_loss += loss.item() * inputs.size(0) # loss.item()是current batch的平均loss，total_loss是這個batch的loss總和
            print('[ Epoch{}: {}/{} ] loss:{:.3f} acc:{:.3f} '.format(epoch+1, i+1, int(tlen/args.batch_size), loss.item(), correct/args.batch_size), end='\r')
        print('\nTrain | Loss:{:.5f} Acc: {:.3f}'.format(total_loss/tlen, total_acc/tlen*args.batch_size)) # total_loss/tlen就是所有data的平均loss
        # TODO: Evaluation loop - calculate accuracy and save model weights
        model.eval()
        with torch.no_grad():
            total_loss, total_acc = 0, 0
            for i, (inputs, labels) in enumerate(dataloaders[DEV]):
                inputs = inputs.to(device)
                labels = labels.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                predict=torch.argmax(outputs, 1) #把概率最大的挑出來
                correct = (predict == labels).sum().item() #計算跟正確情況的差距
                total_acc += (correct / args.batch_size)
                total_loss += loss.item() * inputs.size(0)

            print("Valid | Loss:{:.5f} Acc: {:.3f} ".format(total_loss/vlen, total_acc/vlen*args.batch_size))
            if total_acc > best_acc:
                best_acc = total_acc
                
                torch.save(model.state_dict(), f"{args.ckpt_dir}/intent.model")
                print('saving model with acc {:.3f}'.format(total_acc/vlen*args.batch_size))
        print('-----------------------------------------------')
        model.train()



def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "--data_dir",
        type=Path,
        help="Directory to the dataset.",
        default="./data/intent/",
    )
    parser.add_argument(
        "--cache_dir",
        type=Path,
        help="Directory to the preprocessed caches.",
        default="./cache/intent/",
    )
    parser.add_argument(
        "--ckpt_dir",
        type=Path,
        help="Directory to save the model file.",
        default="./ckpt/intent/",
    )

    # data
    parser.add_argument("--max_len", type=int, default=128)

    # model
    parser.add_argument("--hidden_size", type=int, default=512)
    parser.add_argument("--num_layers", type=int, default=2)
    parser.add_argument("--dropout", type=float, default=0.1)
    parser.add_argument("--bidirectional", type=bool, default=True)

    # optimizer
    parser.add_argument("--lr", type=float, default=1e-3)

    # data loader
    parser.add_argument("--batch_size", type=int, default=100)

    # training
    parser.add_argument(
        "--device", type=torch.device, help="cpu, cuda, cuda:0, cuda:1", default="cpu"
    )
    parser.add_argument("--num_epoch", type=int, default=100)

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    args.ckpt_dir.mkdir(parents=True, exist_ok=True)
    main(args)
