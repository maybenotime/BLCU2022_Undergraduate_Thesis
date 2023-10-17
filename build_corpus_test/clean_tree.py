import re
from pathlib import Path

save_tree_path = Path('/home/ysp2018/chinese_news_data/parse_tree.txt') 
clean_path = Path('/home/ysp2018/chinese_news_data/clean_parse_tree.txt')       #清洗后的语法树信息

def main(file_path,save_path):
    with open(file_path,"r",encoding='utf-8') as f:
        with open(save_path,"a",encoding='utf-8') as w:
            for line in f:
                tree = re.match("\['(.+)'\]",line)
                if tree:
                    w.write(tree.group(1))
                    w.write('\n')
                else:
                    next

if __name__ == "__main__":
    main(save_tree_path,clean_path)
