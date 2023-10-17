import torch
from transformers import BertTokenizer, GPT2LMHeadModel
from torch.nn import CrossEntropyLoss
from numpy import around

test_result_path = '/home/ysp2018/projects/m_t5/inference_result/baseline_hard_test_result.txt'
save_ppl_result = '/home/ysp2018/projects/m_t5/inference_result/hard_baseline_ppl.txt'

def list_split(items, n):
    return [items[i:i+n] for i in range(0, len(items), n)]


def get_test_result(path):
    sens_list = []
    with open(path,"r") as f:
        for line in f:
            line = line.strip()
            sens_list.append(line)
    return sens_list

def cal_ppl_bygpt2(sens):
    tokenizer = BertTokenizer.from_pretrained("uer/gpt2-chinese-cluecorpussmall",cache_dir='/home/ysp2018/projects/m_t5/model_gpt2')
    model = GPT2LMHeadModel.from_pretrained("uer/gpt2-chinese-cluecorpussmall",cache_dir='/home/ysp2018/projects/m_t5/model_gpt2').to('cuda')
    model.eval()
    inputs = tokenizer(sens, padding='max_length', max_length=50, truncation=True, return_tensors="pt").to('cuda')
    bs, sl = inputs['input_ids'].size()
    outputs = model(**inputs, labels=inputs['input_ids'])
    logits = outputs[1]
    # Shift so that tokens < n predict n
    shift_logits = logits[:, :-1, :].contiguous()
    shift_labels = inputs['input_ids'][:, 1:].contiguous()
    shift_attentions = inputs['attention_mask'][:, 1:].contiguous()
    # Flatten the tokens
    loss_fct = CrossEntropyLoss(ignore_index=0, reduction="none")
    loss = loss_fct(shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1)).detach().reshape(bs, -1)
    meanloss = loss.sum(1) / shift_attentions.sum(1)
    ppl = torch.exp(meanloss).cpu().numpy().tolist()
    return ppl


if __name__ == '__main__':
    sens = get_test_result(test_result_path)
    sens_split = list_split(sens,100)
    i = 0
    with open(save_ppl_result,"w") as w:
        for sen_piece in sens_split:
            i += 1
            ppl_list = cal_ppl_bygpt2(sen_piece)
            for ppl in ppl_list:
                score = around(ppl,3)
                w.write(str(score))
                w.write('\n')
            print("{}%".format(i))
