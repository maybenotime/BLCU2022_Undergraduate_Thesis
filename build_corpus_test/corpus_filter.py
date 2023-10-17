import jieba
import jieba.posseg as pseg                 #jieba 词性标注

user_dict_path =  '/home/researcher/projects/T5fortextgeneration/data/user_dict.txt'        #hsk词表
corpus_path = '/home/researcher/projects/T5fortextgeneration/build_corpus_test/format_corpus.txt'   #语料路径
stop_pos_dict = '/home/researcher/projects/T5fortextgeneration/data/stop_pos.txt'       #停用词性表
save_path = '/home/researcher/projects/T5fortextgeneration/data/final_corpus.txt'         #筛选后语料存储路径

jieba.load_userdict(user_dict_path)             #hsk词表作为自定义分词词典

def load_hsk_voc(path):                         #load 自定义词表
    hsk = []
    with open(path,"r") as f:
        for line in f:
            word = line.strip()
            hsk.append(word)
    return hsk

def load_stop_dic(path):
    stop_pos = []
    with open(path,"r") as f:
        for line in f:
            word = line.strip()
            stop_pos.append(word)
    return stop_pos
    
def load_format_corpus(path,hsk,stop_pos,save_path):
    with open(path,"r") as f, open(save_path,"w") as w:
        for line in f:
            line = line.strip()
            cut_result = pseg.lcut(line)
            legal_pos_result = []
            for word,pos in cut_result:
                if pos not in stop_pos:                         #删去停用词性
                    temp_tuple = (word,pos)
                    legal_pos_result.append(temp_tuple)
            
            if len(legal_pos_result) > 10:                      #合法分词长度大于10
                if len(legal_pos_result)/len(cut_result) > 0.7:         #合法长度占源句长度70%以上视为有效语料
                    hsk_list = []                                       #存储hsk词表中出现的词   
                    for word,pos in legal_pos_result:
                        if word in hsk or pos == 'i':                   #成语也算hsk词汇
                            hsk_list.append(word)
                    rate = len(hsk_list)/len(legal_pos_result)          
                    if rate > 0.8:                                      #80%的词在hsk词表中出现过视为有效语料
                        w.write(line)
                        w.write('\n')

    
    
            
            
def main():
    hsk_voc = load_hsk_voc(user_dict_path)
    stop_pos = load_stop_dic(stop_pos_dict)
    load_format_corpus(corpus_path,hsk_voc,stop_pos,save_path)
    
main()

