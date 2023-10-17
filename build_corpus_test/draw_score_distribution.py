from collections import Counter
from numpy import around
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

score_path = '/home/researcher/projects/T5fortextgeneration/data/corpus_score.txt'

with open(score_path,"r") as f:
    all_score = []
    for line in f:
        line = line.strip()
        score = float(line)         #将字符串转换为浮点数
        all_score.append(around(score,1))   #四舍五入,保留一位小数

dic = Counter(all_score)

dic = Counter(all_score)

X = []
Y = []
for x,y in dic.items():
    X.append(x)
    Y.append(y)

fig = plt.figure()
plt.bar(X,Y,0.05,color="green")

plt.ylabel('Quantity', fontdict={'family' : 'Times New Roman', 'size'   : 22})
plt.xlabel('Score', fontdict={'family' : 'Times New Roman', 'size'   : 22})
plt.yticks(fontproperties = 'Times New Roman', size = 20)
plt.xticks(fontproperties = 'Times New Roman', size = 20)

plt.savefig("/home/researcher/projects/T5fortextgeneration/data/score_distribution.jpg")     #绘制分布图
plt.show()