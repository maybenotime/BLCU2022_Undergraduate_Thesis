import csv
import re

test_path = '/home/researcher/projects/T5fortextgeneration/baseline_easy_normal_hard_data/hard_test.txt.csv'
save_ground_truth = '/home/researcher/projects/T5fortextgeneration/data/hard_test_ground_truth.txt'

def load_test_data(path):
    with open(path,'r') as csvfile:
        reader = csv.DictReader(csvfile)
        src_tgt = [(row['\ufeffsrc'],row['tgt']) for row in reader]   # src部分的关键词数据

    return  src_tgt


def main():
    src_tgt =load_test_data(test_path)
    with open(save_ground_truth,"w") as w:
        for tup in src_tgt:
            input = tup[0]
            output = tup[1]
            mode1 = r'[a-z<>]{3}([^a-z<>]*)'                 
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
            w.write(complete_str)
            w.write('\n')
   
main()