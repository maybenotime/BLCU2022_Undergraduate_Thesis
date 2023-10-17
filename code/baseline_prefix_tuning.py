import torch
import wandb
import argparse
from transformers import MT5Tokenizer, MT5ForConditionalGeneration
from datasets import load_dataset
from transformers import DataCollatorForSeq2Seq, Seq2SeqTrainingArguments, Seq2SeqTrainer
from transformers import EarlyStoppingCallback
#再训练了例句生成的基础上进行prefix_tuning学习风格迁移


#语料路径
train_csv = '/home/ysp2018/projects/m_t5/data/train.csv'
valid_csv = '/home/ysp2018/projects/m_t5/data/valid.csv'
test_csv = '/home/ysp2018/projects/m_t5/data/test.csv'

save_model_dir = '../checkpoints_baseline_orgin_prefix_tuning'

#加载model和tokenizer
tokenizer = MT5Tokenizer.from_pretrained('/home/ysp2018/projects/m_t5/baseline_orgin_checkpoints/checkpoint-556066')
mt5model = MT5ForConditionalGeneration.from_pretrained('/home/ysp2018/projects/m_t5/baseline_orgin_checkpoints/checkpoint-556066')

max_input_length = 32
max_target_length = 128

task_prefix = 'trigger:'            #其实prefix是啥都无所谓啦


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_model_dir", type=str,default=save_model_dir)   #保存模型的路径
    parser.add_argument("--batch_size_on_train", type=int, default=8)
    parser.add_argument("--batch_size_on_eval", type=int, default=4)
    parser.add_argument("--num_workers", type=int, default=4)
    parser.add_argument("--num_epochs", type=int, default=100)     #跑几个epoch
    parser.add_argument("--lr", type=float, default=1e-5)
    parser.add_argument("--patience", type=int, default=5)         #几个epoch loss没有下降则停止训练
    parser.add_argument("--wandb_running_name", type=str, default='test_mt5')
    args = parser.parse_args()
    return args




def main(args):
    tokenizer.add_special_tokens({'additional_special_tokens':["<easy>","<normal>","<hard>"]})  #添加自定义token
    print(tokenizer.additional_special_tokens_ids) # 查看特殊token id是否已添加
    mt5model.resize_token_embeddings(len(tokenizer)) #这个操作只是pad 新的token或cut已有的token，其他位置token的预训练词向量不会被重新初始化
    
    dataset = load_dataset('csv',data_files={'train':train_csv, 'validation':valid_csv, 'test':test_csv})   #加载数据集
    
    tokenizer_datasets = dataset.map(preprocess_function, batched=True)   #将数据预处理函数应用到所有数据样本上
    
    wandb.init(project="mt5_prefix_tuning_v2")
    
    parameters = list(mt5model.parameters())            #将模型中所有参数全都冻结
    for x in parameters:
        x.requires_grad = False
        
    
    for name, param in mt5model.named_parameters():     #允许embedding层进行参数更新
        print(name)                                     #embedding层的名字为shared.weight            
        #允许参数更新
        param.requires_grad = True
        break
    
    # embeddings = mt5model.get_input_embeddings()   #返回模型的embedding，检查参数情况
    # trs = embeddings.weight[250099:]               #取出自定义token的embedding
    # for tr in trs:
    #     print(tr.requires_grad)
 
        
    
    
    
    
   
    
    #配置trainer参数
    args = Seq2SeqTrainingArguments(                        
        output_dir=args.output_model_dir,
        overwrite_output_dir=True,
        evaluation_strategy="epoch",
        learning_rate=args.lr,
        per_device_train_batch_size=args.batch_size_on_train,
        per_device_eval_batch_size=args.batch_size_on_eval,
        weight_decay=0.01,
        save_total_limit=10,                #checkpoints中最多会保留几个模型
        num_train_epochs=args.num_epochs,
        predict_with_generate=True,
        fp16=False,
        save_strategy='epoch', 
        dataloader_num_workers=args.num_workers,
        load_best_model_at_end=True,
        gradient_accumulation_steps=2,
        run_name=args.wandb_running_name,
        report_to='wandb',                      #报告结果和日志的平台
        logging_dir='../logs',
        generation_max_length=128,
        generation_num_beams=10,
    )
    
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=mt5model)  #类似于pytorch中的dataloader
    # patience = EarlyStoppingCallback(early_stopping_patience=args.patience)   #早停策略

    trainer = Seq2SeqTrainer(
        mt5model,
        args,
        train_dataset=tokenizer_datasets["train"],
        eval_dataset=tokenizer_datasets["validation"],
        data_collator=data_collator,
        tokenizer=tokenizer,
        # callbacks=[patience],
    )
    
    trainer.train()         #进行微调

def preprocess_function(examples):          #数据预处理
    inputs = [task_prefix + line for line in examples['src']] 
    targets = [line for line in examples['tgt']]
    model_inputs = tokenizer(inputs, max_length=max_input_length, truncation=True, padding='longest')       #encoder的输入

    with tokenizer.as_target_tokenizer():                   #针对targets的tokenizer
        decoder_inputs = tokenizer(targets, max_length=max_target_length, truncation=True, padding='longest')       #实际得到的是decoder的output,模型forward时会自动右移添加sos token得到decoder_input
        
    model_inputs['labels'] = decoder_inputs['input_ids']                #labels这个key最好别改

    return model_inputs


if __name__ == '__main__':
    arg = args()
    main(arg)
    

