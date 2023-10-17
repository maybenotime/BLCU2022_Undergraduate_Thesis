score_path = '/home/researcher/projects/T5fortextgeneration/data/corpus_score.txt'   
corpus_path = '/home/researcher/projects/T5fortextgeneration/data/final_corpus.txt'
easy_path = '/home/researcher/projects/T5fortextgeneration/baseline_easy_normal_hard_data/easy_data.txt'
normal_path = '/home/researcher/projects/T5fortextgeneration/baseline_easy_normal_hard_data/normal_data.txt'
hard_path = '/home/researcher/projects/T5fortextgeneration/baseline_easy_normal_hard_data/hard_data.txt'

easy,normal,hard = 0,0,0

with open(corpus_path,"r") as f_1, open(score_path,"r") as f_2, open(easy_path,"w") as w_e, open(normal_path,"w") as w_n, open(hard_path,"w") as w_h:
    for sen,score in zip(f_1,f_2):
        score = float(score)
        sen = sen.strip()
        if 1.0 <= score <= 2.3:
            w_e.write(sen)
            w_e.write('\n')
            easy += 1
        elif 2.9 <= score <= 3.1:
            w_n.write(sen)
            w_n.write('\n')
            normal += 1
        elif 3.7 <= score <= 7.0:
            w_h.write(sen)
            w_h.write('\n')
            hard += 1
    print(easy,normal,hard)