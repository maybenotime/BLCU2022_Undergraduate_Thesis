score_path = '/home/researcher/projects/T5fortextgeneration/data/corpus_score.txt'   
corpus_path = '/home/researcher/projects/T5fortextgeneration/data/final_corpus.txt'
save_path = '/home/researcher/projects/T5fortextgeneration/data/corpus_with_3label.txt'

easy,normal,hard = 0,0,0

with open(corpus_path,"r") as f_1, open(score_path,"r") as f_2, open(save_path,"w") as w:
    for sen,score in zip(f_1,f_2):
        score = float(score)
        sen = sen.strip()
        if 1.0 <= score <= 2.3:
            w.write(sen)
            w.write('\t')
            w.write('<easy>')
            w.write('\n')
            easy += 1
        elif 2.9 <= score <= 3.1:
            w.write(sen)
            w.write('\t')
            w.write('<normal>')
            w.write('\n')
            normal += 1
        elif 3.7 <= score <= 7.0:
            w.write(sen)
            w.write('\t')
            w.write('<hard>')
            w.write('\n')
            hard += 1
    print(easy,normal,hard)