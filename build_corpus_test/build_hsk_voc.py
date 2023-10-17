import json
import pandas as pd
import jieba.posseg as pseg                 #jieba 词性标注

single_pos_voc_path = '/home/researcher/projects/T5fortextgeneration/data/single_pos_voc'
multi_pos_voc_path = '/home/researcher/projects/T5fortextgeneration/data/multipos_voc'

def main():
    df = pd.read_csv('../data/voc_file.CSV', encoding='gbk')
    df_dict = df.to_dict('records')        
    multi_pos_word = dict()                 #存储多词性的词
    with open(single_pos_voc_path,"w") as w_s:
        for temp_word in df_dict:
            word, level = temp_word['词语'], temp_word['等级']
            
            if '（' in word:                    #处理有括号注明词性的词
                left_bound = word.index('（')
                right_bound = word.index('）')
                pos = word[left_bound + 1:right_bound]  #词性
                pos_list = pos.split('、')              #获得词性列表
                true_word = word[:left_bound]           
                if true_word not in multi_pos_word:
                    multi_pos_word[true_word] = {}      #key为多词性词，value是一个字典
                for pos in pos_list:
                    if pos not in multi_pos_word[true_word]:  
                        multi_pos_word[true_word][pos] = level  #key是词性，value是等级
            else:
                w_s.write('{}\t{}'.format(word,level))
                w_s.write('\n')
    
    legal_pos_set = ['动','名','量','形','助','副','数','代','介','连']     #合法词性
    mapping = {'动':'v','名':'n','量':'q','形':'a','助':'u','副':'d','数':'m','代':'r','介':'p','连':'c'}
    
    with open(multi_pos_voc_path,"w") as w_m:
        for word, pos_dict in multi_pos_word.items():
            pos_num = len(pos_dict)
            if pos_num > 1:                               #词性数目大于1
                to_json = 1
                map_pos = dict()
                for pos, level in pos_dict.items():
                    if pos not in legal_pos_set:
                        to_json = 0
                    else:
                        map_pos[mapping[pos]] = level
                        
                if to_json == 1:            #没有非法词性则输出
                    pos_js = json.dumps(map_pos)
                    w_m.write(word)
                    w_m.write('\t')
                    w_m.write(pos_js)
                    w_m.write('\n')
                            
            

if __name__ == '__main__':
    main()