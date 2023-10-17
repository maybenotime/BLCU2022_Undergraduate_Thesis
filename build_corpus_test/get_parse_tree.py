from corenlp_client import CoreNLP
from pathlib import Path
import re

current_path = Path('/home/ysp2018/chinese_news_data/rmrb_data.txt')  #语料路径
save_tree_path = Path('/home/ysp2018/chinese_news_data/parse_tree.txt') #存储路径

def get_tree(sent):
    annotator = CoreNLP(url="http://202.112.194.61:8085/", lang="zh")
    anno = annotator.annotate(sent)
    tree = anno.parse_tree
    return tree

def read_file(file_path,tree_path):
    count = 0
    with open(tree_path, 'a', encoding='utf-8') as w:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                sen_array = re.split("\t",line)
                del sen_array[-1]               #最后一个元素是空的，删去
                for sen in sen_array:
                    tree_str = str(get_tree(sen))
                    count += 1
                    w.write(tree_str)
                    w.write('\n')
                    print(count)
                    

if __name__ == '__main__':
    read_file(current_path,save_tree_path)