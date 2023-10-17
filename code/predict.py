from transformers import MT5Tokenizer, MT5ForConditionalGeneration
import torch
import argparse
import csv
import re

test_path = '/home/ysp2018/projects/m_t5/data/test.csv'
save_path = '/home/ysp2018/projects/m_t5/inference_result/hard_prefix_mt5_test_result.txt'

def generate_sentence(input, model, tokenizer):
    model.eval()                 
    input_ids = tokenizer.encode(input, return_tensors="pt").to('cuda')  
    outputs = model.generate(input_ids=input_ids,num_beams=20, max_length=128, repetition_penalty=10.0)
    output_str = tokenizer.decode(outputs.reshape(-1), skip_special_tokens=True)
    return output_str

def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str, default='/home/ysp2018/projects/m_t5/checkpoints_baseline_orgin_prefix_tuning/checkpoint-714942')
    parser.add_argument("--model_name", type=str, default='mt5')
    args = parser.parse_args()
    return args

def load_test_data(path):
    with open(path,'r') as csvfile:
        reader = csv.DictReader(csvfile)
        src_list = [row['\ufeffsrc'] for row in reader]   # src部分的关键词数据
        pattern = '<[a-z]+>'                    #删去prompt
        new_src_list = []
        for src in src_list:
            new_src = re.sub(pattern,"",src)
            new_src_list.append(new_src)
    return  new_src_list


if __name__ == '__main__':
    args = args()
    if args.model_name == 'mt5':
        model = MT5ForConditionalGeneration.from_pretrained(args.model_path).to('cuda')
        tokenizer = MT5Tokenizer.from_pretrained(args.model_path)
        
    # print(generate_sentence(keyword, model, tokenizer))
    task_prefix = 'trigger:'
    prefix_prompt = '<hard>'
    input = '<extra_id_0>妻子▁<extra_id_1>'
    complete_input = task_prefix + prefix_prompt + input
    output = (generate_sentence(complete_input,model,tokenizer))
    mode1 = r'[a-z<>0123456789_▁]+([^a-z<>]*)'                 
    mode2 = r'[^a-z<>0123456789_▁]+'
    mask_group = re.finditer(mode1,output)
    word_group = re.findall(mode2,input)
    mask_list = []
    for mask in mask_group:
        mask_list.append(mask.group(1))
    complete_str = ''
    temp_i = 0
    for i in range(len(word_group)):
        complete_str = complete_str +mask_list[i] + word_group[i]
        temp_i = i + 1
    complete_str = complete_str + mask_list[temp_i]
    print(complete_str)
    
    
            