from transformers import MT5Tokenizer, MT5ForConditionalGeneration
import torch
import argparse
import csv
import re

test_path = '/home/ysp2018/projects/m_t5/baseline_easy_noram_hard_data/normal_test.txt.csv'
save_path = '/home/ysp2018/projects/m_t5/inference_result/baseline_normal_test_result.txt'

def generate_sentence(input, model, tokenizer):
    model.eval()                 
    input_ids = tokenizer.encode(input, return_tensors="pt").to('cuda')  
    outputs = model.generate(input_ids=input_ids,num_beams=20, max_length=128, repetition_penalty=10.0)
    output_str = tokenizer.decode(outputs.reshape(-1), skip_special_tokens=False)
    return output_str

def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str, default='/home/ysp2018/projects/m_t5/baseline_transfer_normal_checkpoints/checkpoint-147650')
    parser.add_argument("--model_name", type=str, default='mt5')
    args = parser.parse_args()
    return args

def load_test_data(path):
    with open(path,'r') as csvfile:
        reader = csv.DictReader(csvfile)
        src_list = [row['\ufeffsrc'] for row in reader]   # src部分的关键词数据
    return  src_list


if __name__ == '__main__':
    args = args()
    if args.model_name == 'mt5':
        model = MT5ForConditionalGeneration.from_pretrained(args.model_path).to('cuda')
        tokenizer = MT5Tokenizer.from_pretrained(args.model_path)
        
    task_prefix = 'trigger:'
    test_data = load_test_data(test_path)
    with open(save_path,"w") as w:
        for input in test_data:
            complete_input = task_prefix + input
            mode = r'[^a-z<>0123456789_▁]+'                 #删掉特殊token
            output = (generate_sentence(input,model,tokenizer))
            mask_group = re.findall(mode,output)
            word_group = re.findall(mode,input)
            mask_group.remove(mask_group[0])
            mask_group.remove(mask_group[-1])
            complete_str = ''
            temp_i = 0
            try:
                for i in range(len(word_group)):
                    complete_str = complete_str +mask_group[i] + word_group[i]
                    temp_i = i + 1
                complete_str = complete_str + mask_group[temp_i]
                if temp_i < len(mask_group) - 1:
                    temp_i += 1
                    complete_str += mask_group[temp_i]
                print(complete_str)
                w.write(complete_str.replace(" ",""))
                w.write('\n')
            except Exception as e:
                print(str(e))
            