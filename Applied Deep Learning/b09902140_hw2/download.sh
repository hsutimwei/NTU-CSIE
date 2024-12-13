
mkdir -p ./ckpt/select 
wget -O ./ckpt/select/pytorch_model.bin "https://www.dropbox.com/s/fn0ito1gh35hhc8/pytorch_model.bin?dl=0"
wget -O ./ckpt/select/config.json "https://www.dropbox.com/s/2ov5in097mx3hdv/config.json?dl=0" 
mkdir -p ./qaout
wget -O ./qaout/vocab.txt "https://www.dropbox.com/s/en6ur880x5de9xt/vocab.txt?dl=0"
wget -O ./qaout/tokenizer.json "https://www.dropbox.com/s/7whqdd61x68jvzs/tokenizer.json?dl=0" 
wget -O ./qaout/tokenizer_config.json "https://www.dropbox.com/s/4huqeuc1lk7eilp/tokenizer_config.json?dl=0" 
wget -O ./qaout/special_tokens_map.json "https://www.dropbox.com/s/c95lvf19iprpklh/special_tokens_map.json?dl=0" 
wget -O ./qaout/pytorch_model.bin "https://www.dropbox.com/s/wltf9tgqj3yir3j/pytorch_model.bin?dl=0" 
wget -O ./qaout/pred.json "https://www.dropbox.com/s/nu3al4w1zgaft98/pred.json?dl=0" 
wget -O ./qaout/config.json "https://www.dropbox.com/s/fnuuvwpgfw6np3v/config.json?dl=0"
mkdir -p ./data
wget -O ./data/valid.json "https://www.dropbox.com/s/ztitaialgm154bt/valid.json?dl=0" 
wget -O ./data/train.json "https://www.dropbox.com/s/9v3l0eswoc5jue6/train.json?dl=0" 
wget -O ./data/test.json "https://www.dropbox.com/s/a5j2zatsi6wwebs/test.json?dl=0" 
wget -O ./data/pred.json "https://www.dropbox.com/s/erqvejhjszw8cse/pred.json?dl=0" 
wget -O ./data/context.json "https://www.dropbox.com/s/8o1hbsal510qxna/context.json?dl=0" 