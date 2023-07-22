# ADL22-HW2
Dataset & evaluation script for ADL 2022 homework 3
## file
train.py : 訓練text generation，並將訓練出的model和tokenizer放在./output裡面。
dataset.py : Mydataset是text generation時為了應對datasets套件的load_dataset用的，會回傳id、text、summary三種資料。
testdataset.py : 是test text generation時用的，會回傳id、text三種資料。
test.py : 是拿text generation訓練好的model來做test data的prediction。
eval.py : 就是sample code，完全沒改。
plot.py : 畫圖用的。
## demo
``` shell
bash ./download.sh
bash ./run.sh {test file} {pred file}
```

## training
```shell
python train.py
```