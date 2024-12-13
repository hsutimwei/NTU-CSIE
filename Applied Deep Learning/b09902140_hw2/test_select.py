import torch
import json
from argparse import ArgumentParser, Namespace
from pathlib import Path
from transformers import AutoTokenizer, BertForMultipleChoice
from tqdm import trange
from torch.utils.data import DataLoader
from dataset import TrainDataset  
from torch.nn.utils.rnn import pad_sequence
import os
#os.environ['CUDA_VISIBLE_DEVICES']='4'
os.environ["TOKENIZERS_PARALLELISM"] = "false"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def main(args):
    
    test_path=open(args.test_file,encoding="utf-8")
    test_datas=json.load(test_path)
    print("dealing with test data")
    ids=[]
    for i,data in enumerate(test_datas):
        ids.append(data['id'])
    
    test_data=preprocess(args,test_datas)
    
    test_dataset=TrainDataset(test_data)
    
    test_dataloader=DataLoader(test_dataset, collate_fn = test_dataset.collate_fn, shuffle=False, batch_size = args.batch_size)
    
    model = BertForMultipleChoice.from_pretrained(args.model_name)
    
    model.to(device)
    model.eval()
    

    print("test start")
    a={}
    for i, batch in enumerate(test_dataloader):

        batch=(i.to(device) for i in batch)
        input_ids,attention_mask,token_type_ids=batch

        outputs = model(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        predict = torch.argmax(outputs.logits , dim = 1).int().tolist()
        a[ids[i]]=test_datas[i]["paragraphs"][predict[0]]
        
    with open( './data/pred.json', 'w', encoding='utf-8') as f:
        json.dump(a, f,indent=4)
    print('-----------------------------------------------')
        
def preprocess(args,train_data):
    #question+context
    context_path=open(args.data_file,encoding="utf-8")
    
    context_data=json.load(context_path)
    
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer_name)

    datas=[]
    for i,data in enumerate(train_data):
        #有len(train_data)組，每組都有3個question+context
        max_input_length = 512

        question=data['question']
        question=tokenizer.encode(data['question'])
        
        paragraphs = data['paragraphs']
        
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
        inputs = torch.LongTensor(inputs)#應該要是[4,512]
        attention_masks = torch.LongTensor(attention_masks)
        tokens_type = torch.LongTensor(tokens_type)
        
        dataa={}
        dataa['inputs']=inputs
        dataa['attention_masks']=attention_masks
        dataa['tokens_type']=tokens_type
        datas.append(dataa)
        #print(dataa)
        print(f"Finish {i}'th data",end='\r')
        '''if i>=100:
            break'''
        
    return datas
def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "--data_file",
        type=Path,
        help="Directory to the dataset.",
        default="./data/context.json",
    )
    parser.add_argument(
        "--test_file",
        type=Path,
        help="Directory to the dataset.",
        default="./data/test.json",
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
        default = './ckpt/select',
    )
    parser.add_argument(
        "--tokenizer_name",
        type=str,
        help="Pretrained tokenizer name",
        default= 'hfl/chinese-roberta-wwm-ext',
    )
    parser.add_argument("--lr", type=float, default=3e-5)

    parser.add_argument("--batch_size", type=int, default = 1)

    parser.add_argument("--num_epoch", type=int, default = 5)

    args = parser.parse_args()

    return args

if __name__ == "__main__":
    args = parse_args()
    args.ckpt_dir.mkdir(parents=True, exist_ok=True)
    main(args)