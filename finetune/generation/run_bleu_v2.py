import os
from utils import load_json
from transformers import BertTokenizer
from bleu_metric import Metric
from datasets import load_dataset

#需要计算bleu的文本文件所在的目录
arch='output'
tokenizer=BertTokenizer.from_pretrained('output/hk01/6')
dataset='hk01'
test_set= datasets = load_dataset("csv", data_files='demo_data/SUMMARY.hk01/test.csv',split='train')

labels=[]
for data in test_set:
    ids=tokenizer.encode(data['summarization'])
    labels.append(tokenizer.decode(ids,skip_special_tokens=True))
    
labels=[[label.strip().split(' ')] for label in labels][:100]

metric=Metric(None)
idxs=os.listdir(os.path.join(arch,dataset))
scores=[]

idx = '6'
path=os.path.join(arch,dataset,idx,'test_generations.txt')
with open(path,encoding='utf-8') as f:
    lines=f.readlines()
lines=list(map(lambda x:x.strip(),lines))
lines=[line.split(' ') for line in lines]

print (len(lines))
print (len(labels))

metric.hyps=lines
metric.refs=labels

print (metric.calc_bleu_k(1))