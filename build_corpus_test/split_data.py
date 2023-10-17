import torch
from torch.utils.data import random_split

train_path = '/home/researcher/projects/T5fortextgeneration/baseline_easy_normal_hard_data/hard_train.txt'
valid_path = '/home/researcher/projects/T5fortextgeneration/baseline_easy_normal_hard_data/hard_valid.txt'
test_path = '/home/researcher/projects/T5fortextgeneration/baseline_easy_normal_hard_data/hard_test.txt'

def load_data(path):
    data = []
    with open(path,"r") as f:
        for line in f:
            line = line.strip()
            data.append(line)
    return data
    

def split(data):
    train_size = int(len(data)*0.98)
    valid_size = int(len(data)*0.01)
    test_size = len(data) - train_size - valid_size
    train_dataset, valid_data, test_dataset = random_split(
    dataset=data,
    lengths=[train_size, valid_size, test_size],
    generator=torch.Generator().manual_seed(0)
    )
    with open(train_path,"w") as w_train, open(valid_path,"w") as w_valid, open(test_path,"w") as w_test:
        for sen in train_dataset:
            w_train.write(sen)
            w_train.write('\n')
        
        for sen in valid_data:
            w_valid.write(sen)
            w_valid.write('\n')
        
        for sen in test_dataset:
            w_test.write(sen)
            w_test.write('\n')
            
data = load_data('/home/researcher/projects/T5fortextgeneration/baseline_easy_normal_hard_data/hard_src_tgt.txt')
split(data)

