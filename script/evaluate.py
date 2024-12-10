
import pandas as pd
from openpyxl import Workbook
import jieba
import re
import math
from rouge import Rouge
from nltk.translate.bleu_score import sentence_bleu

file_path = "sample.xlsx"
data = pd.read_excel(file_path, sheet_name="Sheet1")
types=data['题型']
real_answer = data['正确回答']
model_answer = data['模型回答']
correct_answers = data['小题正确数量']
all_answers=data['小题总数量']
is_copy=data['是否抄录']
is_all_right=data['题组匹配是否正确']
difficult=data['难度系数']


def ToF(i):
    score=0
    if model_answer[i].strip()==real_answer[i]:
        score+=1*difficult[i]
    return score

def choice(i):
    score = 0
    if model_answer[i].strip() == real_answer[i]:
        score += 1*difficult[i]
    return score

def PA(i):
    score=0
    if is_copy=="0":
        if corect_answers[i]==all_answers[i]:
            score=score+3
        elif corect_answers[i]>0&corect_answers[i]<all_answers[i]:
            score=score+1
        else:
            score=score+0
    return score

def get_answer(type,real_answer,model_answer):
    if type=="essay":
        prompt = "你是一个专业的儿科医学考官，请你参考真实答案，综合考虑回答的完整性、流畅性和准确性，对考生的回答进行评分。满分为5分，注意！不需要给出评分理由。回复格式为：\"综合评分：x分。完整性：x分，流畅性：x分，准确性：x分。\"   真实答案为：\n" + real_answer + "\n考生回答为：\n" + model_answer
    elif type=="case":
        prompt = "你是一个专业的儿科医学考官，请你参考真实答案，综合考虑回答的准确性、合理性和完整性，对考生的回答进行评分。要求：1、若参考答案较为简略，但考生回答较为详细且没有错误的部分，则算满分；2、若考生回答中有错误的内容，则酌情减分；3、若诊断回答错误，则诊断依据不给分。答案总分为10分，参考答案中标记了相应的分值，请参考该分值进行评分，回复格式为：\"总得分：x分。\"   参考答案为：\n" + real_answer + "\n考生回答为：\n" + model_answer
    client = OpenAI(
          base_url="https://api.gptsapi.net/v1",
          api_key="")
    message = [{'role': "user", 'content': prompt}]
    rep = client.chat.completions.create(
        model="gpt-4o",
        messages=message,
        temperature=0  # 这个参数规定了输出的一致性，这个值越低代表输出越固定。如果想要提示词一样输出的结果也一样就把值设为0
    )
    generated_text = rep.choices[0].message.content
    return generated_text
def essay(i):#简答题实验结果统计
    score=0
    text = get_answer(type,real_answer[i], model_answer[i])
    print(i, score)
    a= re.findall('(?<=总得分：).*$', text)
    if a!=[]:
        score = score + int(a[0][0])
    return score


def case(i):#案例题实验结果统计
    score=0
    text = get_answer(type,real_answer[i], model_answer[i])
    print(i, score)
    a= re.findall('(?<=总得分：).*$', text)
    if a!=[]:
        score = score + int(a[0][0])
    return score

def get_rank_index(number):
    second_number=sorted(number)
    rank_index=[]
    for per_number in number:
        rank_index.append(second_number.index(per_number))
    return rank_index

def statistical_data(rank_index,correct_answers):
    correct_index=[i for i in range(len(correct_answers))]
    true_number=0
    for i,number in enumerate(rank_index):
        if number==correct_index[i]:
            true_number+=1
    return [true_number,len(correct_answers),true_number==len(correct_answers)]



if __name__=='__main__':
    input_excel='sample.xlsx'#模型回答的文件
    for i in range(len(data)):
        if types[i]=="连线题":
            score_PA=PA(i)
        elif types[i]=="判断题":
            score_ToF=ToF(i)
        elif types[i]=="选择题":
            score_choice=choice(i)
        elif types[i]=="简答题":
            score_essay=essay(i)
        elif types[i]=="案例题":
            score_case=case(i)
    print(score_PA,score_ToF,score_choice,score_essay,score_case)
    total=score_choice+score_PA+score_ToF+score_essay+score_case


