from nltk.translate.bleu_score import SmoothingFunction
from nltk.translate.bleu_score import sentence_bleu

reference_path = '/home/ysp2018/projects/m_t5/baseline_easy_noram_hard_data/hard_test_ground_truth.txt'
candidate_path = '/home/ysp2018/projects/m_t5/inference_result/baseline_hard_test_result.txt'

def load_reference():
    reference_list = []
    with open(reference_path,"r") as f:
        for line in f:
            line = line.strip()
            reference_list.append(line)
            
    return reference_list

def load_candidate():
    candidate_list = []
    with open(candidate_path,"r") as f:
        for line in f:
            line = line.strip()
            candidate_list.append(line)
            
    return candidate_list

def main():
    ref_list = load_reference()
    can_list = load_candidate()
    all_score = 0
    for tup in zip(ref_list,can_list):
        reference = list(tup[0])
        candidate = list(tup[1])
        refer = [reference]
        temp_score = sentence_bleu(refer, candidate,smoothing_function=SmoothingFunction().method1)                #注意，参考应该是列表的列表，候选应是列表，不然会计算出错误的结果
        all_score += temp_score
    
    avg_score = all_score/len(ref_list)
    print(avg_score)
    
main()