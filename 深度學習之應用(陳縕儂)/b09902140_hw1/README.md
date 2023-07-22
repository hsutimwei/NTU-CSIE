# Sample Code for Homework 1 ADL NTU

## Environment
```shell
# If you have conda, we recommend you to build a conda environment called "adl-hw1"
#make
#conda activate adl-hw1
#pip install -r requirements.txt
# Otherwise
#pip install -r requirements.in
我沒有設定環境，因為我是用資工系工作站meow1的/tmp2進行訓練，而import的套件都是管理員設定好的，在/usr資料夾裡面。
```

## Preprocessing
```shell
# To preprocess intent detectiona and slot tagging datasets
bash preprocess.sh
```

## Training
```shell
python train_intent.py
python train_slot.py
```

## Testing
```shell
bash ./intent_cls.sh /path/to/test.json /path/to/pred.csv
bash ./slot_tag.sh /path/to/test.json /path/to/pred.csv
```