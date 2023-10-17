# Hard-Constrained-Text-Generation-with-Controllable-Word-Complexity

## background and introduction

* 2022 BLCU Thesis
* 该项目微调mt5模型用填空任务的模式实现例句生成任务，并用prompt实现了词汇难度风格的迁移，可以生成简单普通困难三种风格的例句
* code目录中包含了训练模型的代码
* ins_gen_website目录是展示demo的前后端代码，前端vue,后端tornado
* build_corpus_test中是构建数据集的代码，按照一种全新的自动标注方案进行标注
* nginx.conf则是部署demo的nginx配置文件，用以解决跨域问题


## requirements
* python3.6
* pytorch 1.6
* wandb
* argparse
* transformers
* datasets

## code usage
从hugging face上下载mt5模型
```
python baseline.py  #训练例句生成模型，自定义token
python baseline_orgin_token.py   #例句生成模型，mt5词表中自带的mask_token
python m_t5.py      #训练prompt风格迁移模型，可以直接finetune也可以在baseline的基础上做增量训练
python calculate_ppl_with_gpt   #使用中文gpt2计算ppl,并生成预测结果所对应的ppl值文件
python cal_avg_ppl.py    #计算预测结果的平均ppl
python cal_bleu.py       #计算BLEU
python calculate_wde.py  #计算预测结果的平均词汇难度期望以及迁移准确率

#code目录中baseline_transfer_XXX.py的代码是使用多模型来实现词汇难度风格的迁移
#命名中有predict的脚本是用来生成测试集上的预测结果的。
```

## run demo
* predict_api_10000.py 将模型的预测部署为一个可供访问的api
* 详细内容可见开发文档   【腾讯文档】文心·例句生成系统开发文档  https://docs.qq.com/doc/DS1hCTEx1Z3ZValVF

## dataset
* 构建数据集的语料来源是人民日报，使用HSK词表来划分词语难度
```
python clean_corpus.py     #清洗人民日报语料
python build_hsk_voc.py    #生成单词性和多词性词语标注词典
python get_jieba_user_dict.py  #将HSK词表处理为自定义分词字典
python corpus_filter.py    #对语料中不合法语句进行过滤
python count_corpus.py     #计算数据集中语句的词汇难度期望得分
python draw_score_distribution.py #画出数据集中语句得分的分布图，用以确定标签划定范围
python map_score_to_label.py   #将得分映射至标签，最终完成数据集构建
extract_keywords.py  baseline_data.py  baseline_origintoken_data.py    #将数据处理成transformers库所要求的格式，分为src和tgt
python split_data.py     #切分训练集验证集和测试集
python text_to_csv.py    #将txt文件转为csv文件
python split_easy_normal_hard_dataset.py   #将数据集按照三种标签切分为三种风格的数据集分别训练单独的风格迁移模型
python restore_test_ground_truth.py   #还原ground truth 用以计算bleu

```