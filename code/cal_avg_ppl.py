ppl_path = '/home/ysp2018/projects/m_t5/inference_result/hard_baseline_ppl.txt'

ppl_list = []
with open(ppl_path,"r") as f:
    for line in f:
        line = line.strip()
        ppl_list.append(float(line))

total_ppl = sum(ppl_list)
avg_ppl = total_ppl/len(ppl_list)
print(avg_ppl)