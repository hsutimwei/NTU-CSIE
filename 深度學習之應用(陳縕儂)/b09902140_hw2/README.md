# Homework 2 ADL
## file
train_select.py : 訓練context selection，並將predict出的結果pred.json放在data資料夾裡。
train_QA.py : 訓練Question Answering，並將結果放在qaout資料夾裡。我是用sample code，所以除了config和pred.json外還有一些檔案
dataset.py : 有2個class。TrainDataset是context selection時用的。Mydataset是Question Answering時為了應對datasets套件的load_dataset用的
qadataset.py : 是test context selection時用的。因為除了讀取text data外，我們還需要讀取前面context selection所predict出的結果，所以跟訓練用的dataset分開寫。
test_select.py : 是拿context selection訓練好的model來做test data的prediction。
test_qa.py : 是拿Question Answering訓練好的model和前面test_select.py predict出的結果來做rediction。
## demo
``` shell
bash ./download.sh
bash ./run.sh {cotext file} {test file} {pred file}
```

## training
```shell
python train_select.py
python train_QA.py
```