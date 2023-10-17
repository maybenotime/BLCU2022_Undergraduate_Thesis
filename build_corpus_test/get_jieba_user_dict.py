single_pos_path = '/home/researcher/projects/T5fortextgeneration/data/single_pos_voc'
muli_pos_path = '/home/researcher/projects/T5fortextgeneration/data/multipos_voc'
user_dict_path =  '/home/researcher/projects/T5fortextgeneration/data/user_dict.txt'

def combine(s_path,m_path,save_path):
    word_list = []
    with open(s_path,"r") as f, open(m_path,"r") as f_2:
        for line in f:
            word,level = line.split('\t')
            word_list.append(word)
        for line in f_2:
            word,dic = line.split('\t')
            word_list.append(word)
            
    with open(save_path,"w") as w:
        for word in word_list:
            w.write(word)
            w.write('\n')
        
combine(single_pos_path,muli_pos_path,user_dict_path)
        
     