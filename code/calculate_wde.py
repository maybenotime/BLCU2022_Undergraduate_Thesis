from collections import Counter
import jieba.posseg as pseg                 #jieba 词性标注
import json

from numpy import around

corpus_path = '/home/ysp2018/projects/m_t5/inference_result/baseline_hard_test_result.txt'
stop_pos_dict = '/home/ysp2018/projects/m_t5/data/stop_pos.txt'       #停用词性表
single_pos_voc_path = '/home/ysp2018/projects/m_t5/data/single_pos_voc'
multi_pos_voc_path = '/home/ysp2018/projects/m_t5/data/multipos_voc'

def get_corpus_score(path,stop_pos,s_voc,m_voc):
    all_score = []
    with open(path,"r") as f:
        for line in f:
            cut_result = pseg.lcut(line)
            legal_pos_result = []
            for word,pos in cut_result:
                if pos not in stop_pos:                         #删去停用词性
                    temp_tuple = (word,pos)
                    legal_pos_result.append(temp_tuple)
            score_list = get_score_list(legal_pos_result,s_voc,m_voc)       #获得难度列表
            score_list = map(int , score_list)                 #统一列表内元素属性
            score = calculate_score(list(score_list))                  #计算期望
            true_score = around(score,2)
            all_score.append(true_score)
            
    total_score = 0
    for score in all_score:
        total_score += score
    corpus_score = total_score/len(all_score)
    score_result = around(corpus_score,2)
    
    return all_score,score_result 
            

def load_single_voc(path):
    single_voc = {}
    with open(path,"r") as f:
        for line in f:
            line = line.strip()
            word, level = line.split('\t')
            single_voc[word] = level
            
    return single_voc

def load_multi_voc(path):
    multi_voc = {}
    with open(path,"r") as f:
        for line in f:
            line = line.strip()
            word, level = line.split('\t')
            multi_voc[word] = json.loads(level)

    return multi_voc

def load_stop_dic(path):
    stop_pos = []
    with open(path,"r") as f:
        for line in f:
            word = line.strip()
            stop_pos.append(word)
    return stop_pos

def get_score_list(pos_list,s_voc,m_voc):
    score_list = []
    for word,pos in pos_list:       
        if word in m_voc:                               #词存在
            if pos in m_voc[word]:                      #词性存在
                score_list.append(m_voc[word][pos])
        elif word in s_voc:
            score_list.append(s_voc[word])
        elif pos == 'i':
            score_list.append(7)
    return  score_list

def calculate_score(score_list):
    all_len = len(score_list)
    count_dict = Counter(score_list)
    score = 0
    for level,count in count_dict.items():
        score += level * (count/all_len)
        
    return score

def get_transfer_accuracy(score_list):
    count = 0
    for score in score_list:
        if 3.7 <= score <= 6.0:
            count += 1
    return around(count/len(score_list),3)
    
    
def main():
    single_voc = load_single_voc(single_pos_voc_path)
    multi_voc = load_multi_voc(multi_pos_voc_path)
    stop_pos = load_stop_dic(stop_pos_dict)
    score_list, corpus_score = get_corpus_score(corpus_path,stop_pos,single_voc,multi_voc)
    transfer_accuracy = get_transfer_accuracy(score_list)
    print(corpus_score)
    print(transfer_accuracy)
    
    
if __name__ == '__main__':
    main()

