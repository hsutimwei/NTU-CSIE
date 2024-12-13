mkdir -p ckpt/intent
mkdir -p ckpt/slot
wget https://www.dropbox.com/s/5ic701mbxh81cub/slot.model?dl=0 -O ckpt/intent/best.pt
wget https://www.dropbox.com/s/3wkk8axtw5nw0mg/intent.model?dl=0 -O ckpt/slot/best.pt

mkdir -p cache/intent
mkdir -p cache/slot
wget https://www.dropbox.com/s/kzg5548uo1aw2bc/embeddings.pt?dl=0 -O cache/intent/embeddings.pt
wget https://www.dropbox.com/s/cu0s3unzc63suzk/vocab.pkl?dl=0 -O cache/intent/vocab.pkl
wget https://www.dropbox.com/s/w7f8kyztzc5271b/intent2idx.json?dl=0 -O cache/intent/intent2idx.json
wget https://www.dropbox.com/s/sqmenkdna4nedb8/embeddings.pt?dl=0 -O cache/slot/embeddings.pt
wget https://www.dropbox.com/s/aek8gged5ln3w4o/vocab.pkl?dl=0 -O cache/slot/vocab.pkl
wget https://www.dropbox.com/s/oe8dg5dj90yt9xh/tag2idx.json?dl=0 -O cache/slot/tag2idx.json