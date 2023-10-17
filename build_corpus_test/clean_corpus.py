import re

corpus_path = '/home/researcher/projects/T5fortextgeneration/build_corpus_test/test.txt'
save_path = '/home/researcher/projects/T5fortextgeneration/build_corpus_test/format_corpus.txt'

def clean_data(path,save_path):
    with open(path,"r") as f , open(save_path,"w") as w:
        for line in f:
            line = line.strip()
            pattern = '第\d[^\t]+专栏\s：\s'
            new_line = re.sub(pattern,'',line)          #删去每篇报道的前缀
            sen_list = new_line.split("\t")
            for sen in sen_list:
                word_list = sen.split(" ")
                str = "".join(word_list)
                w.write(str)
                w.write('\n')
                
clean_data(corpus_path,save_path)