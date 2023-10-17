import pandas as pd
#将txt文件转成csv文件

src_tgt_path = '/home/researcher/projects/T5fortextgeneration/baseline_easy_normal_hard_data/hard_test.txt'


def get_csv(file):
    df = pd.read_csv(file,delimiter=";",names=['src','tgt'])  #‘;’是分隔符
    # df.columns = ['id','file','text']
    # encoding='utf_8_sig'解决存储csv的乱码问题
    df.to_csv(f"{file}.csv", encoding='utf_8_sig', index=False)
    return df


get_csv(src_tgt_path)