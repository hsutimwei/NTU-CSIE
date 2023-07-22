import torch
import json
from argparse import ArgumentParser, Namespace
from pathlib import Path
from transformers import AutoTokenizer, BertForMultipleChoice
from tqdm import trange
from torch.utils.data import DataLoader
from dataset import TrainDataset  
import os
#os.environ['CUDA_VISIBLE_DEVICES']='4'
os.environ["TOKENIZERS_PARALLELISM"] = "false"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def main(args):
    
    train_path=open(args.data_dir/"train.json",encoding="utf-8")
    train_data=json.load(train_path)
    valid_path=open(args.data_dir/"valid.json",encoding="utf-8")
    valid_data=json.load(valid_path)
    print("dealing with train data")
    train_data=preprocess(args,train_data)
    print("dealing with valid data")
    valid_data=preprocess(args,valid_data)
    
    train_dataset=TrainDataset(train_data)
    valid_dataset=TrainDataset(valid_data)
    
    train_dataloader=DataLoader(train_dataset, collate_fn = train_dataset.collate_fn, shuffle=True, batch_size = args.batch_size)
    valid_dataloader=DataLoader(valid_dataset, collate_fn = valid_dataset.collate_fn, shuffle=True, batch_size = args.batch_size)
    
    model = BertForMultipleChoice.from_pretrained(args.model_name)
    
    model.to(device)
    
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    
    tlen = len(train_dataloader)
    vlen = len(valid_dataloader)
    
    best_acc=0
    model.train()
    epoch_pbar = trange(args.num_epoch, desc="Epoch")
    print("train start")
    accum_iter = 4
    optimizer.zero_grad()
    for epoch in epoch_pbar:
        total_loss, total_acc = 0, 0
        for i, batch in enumerate(train_dataloader):

            batch=(i.to(device) for i in batch)
            input_ids,attention_mask,token_type_ids,labels=batch

            outputs = model(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids, labels=labels)

            loss = outputs.loss
            loss = loss / accum_iter 
            loss.backward()

            if ((i + 1) % accum_iter == 0) or (i + 1 == tlen):
                optimizer.step()
                optimizer.zero_grad()

            predict = torch.argmax(outputs.logits , dim = 1)
            correct = (predict == labels).sum().item()
            total_acc += (correct / args.batch_size)
            total_loss += loss.item()
            print("[ Epoch{}: {}/{} ] loss:{:.3f} acc:{:.3f}".format(epoch+1,i+1, tlen, loss.item(), correct / args.batch_size), end='\r')
        print('\nTrain | Loss:{:.5f} Acc: {:.5f}'.format(total_loss/tlen, total_acc/tlen))
        
        model.eval()
        with torch.no_grad():
            total_loss, total_acc = 0, 0
            for i, batch in enumerate(valid_dataloader):
                batch=(i.to(device) for i in batch)
                input_ids,attention_mask,token_type_ids,labels=batch
                outputs = model(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids, labels=labels)
                loss = outputs.loss
                predict = torch.argmax(outputs.logits , dim = 1)
                correct = (predict == labels).sum().item()
                total_acc += (correct / args.batch_size)
                total_loss += loss.item()

            print("Valid | Loss:{:.5f} Acc: {:.3f} ".format(total_loss/vlen, total_acc/vlen))
            if total_acc > best_acc:
                best_acc = total_acc
                
                model.save_pretrained(f"{args.ckpt_dir}")
                print('saving model with acc {:.3f}'.format(total_acc/vlen))
        print('-----------------------------------------------')
        model.train()
        
def preprocess(args,train_data):
    #question+context
    context_path=open(args.data_dir/"context.json",encoding="utf-8")
    
    context_data=json.load(context_path)
    
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer_name)

    datas=[]
    for i,data in enumerate(train_data):
        #有len(train_data)組，每組都有3個question+context
        max_input_length = 512
        
        question=data['question']
        question=tokenizer.encode(data['question'])
        
        paragraphs = data['paragraphs']
        relevant = data['relevant']
        
        inputs = []
        attention_masks = []
        tokens_type = []
        for context_id in paragraphs:
            
            context=context_data[context_id]
            context = tokenizer.tokenize(context)
            context = tokenizer.convert_tokens_to_ids(context)
            
            input=question+context
            input=input[:max_input_length-1]
            input+=[tokenizer.sep_token_id]
            attention_mask=[1 for i in input]
            while(len(input)<max_input_length):
                input+=[tokenizer.pad_token_id]
                
            while(len(attention_mask)<max_input_length):
                attention_mask+=[0]
            
            token = [0 for i in question]+[1 for i in context]
            token=token[:max_input_length-1]
            while(len(token)<max_input_length):
                token+=[1]
            
            inputs.append(input)
            attention_masks.append(attention_mask)
            tokens_type.append(token)
        label=torch.LongTensor([paragraphs.index(relevant)])
        #label=label.to(device)
        inputs = torch.LongTensor(inputs)#應該要是[4,512]
        attention_masks = torch.LongTensor(attention_masks)
        tokens_type = torch.LongTensor(tokens_type)
        
        dataa={}
        dataa['inputs']=inputs
        dataa['attention_masks']=attention_masks
        dataa['tokens_type']=tokens_type
        dataa['label']=label
        datas.append(dataa)
        #print(dataa)
        print(f"Finish {i}'th data",end='\r')
        '''if i>=100:
            break'''
        
    return datas
def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "--data_dir",
        type=Path,
        help="Directory to the dataset.",
        default="./data",
    )
    parser.add_argument(
        "--ckpt_dir",
        type = Path,
        help="Directory to save the model file.",
        default="./ckpt/select/",
    )
    parser.add_argument(
        "--model_name",
        type = str,
        help = "BERT model_name",
        default = 'hfl/chinese-roberta-wwm-ext',
    )
    parser.add_argument(
        "--tokenizer_name",
        type=str,
        help="Pretrained tokenizer name",
        default= 'hfl/chinese-roberta-wwm-ext',
    )
    parser.add_argument("--lr", type=float, default=3e-5)

    parser.add_argument("--batch_size", type=int, default = 1)

    parser.add_argument("--num_epoch", type=int, default = 2)

    args = parser.parse_args()

    return args

if __name__ == "__main__":
    args = parse_args()
    args.ckpt_dir.mkdir(parents=True, exist_ok=True)
    main(args)