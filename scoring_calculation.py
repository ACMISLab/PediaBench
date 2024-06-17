#学校：贵州大学
#编写人：冯林坤
#创建时间：2024/6/16 14:50
import pandas as pd
from openpyxl import Workbook
import jieba
import math
from rouge import Rouge
from nltk.translate.bleu_score import sentence_bleu

def write_QC_to_excel(new_data,write_excel,columns=[]):  # 向excel文件中写入数据,new_data是一个二维列表，每一元素表示一行数据,columns是一个一位列表
    columns = ['疾病组', '选择题得分', '判断题得分', '连线题得分', '简答题得分', '客观题科室均分', '案例题得分']
    df = pd.DataFrame(new_data, columns=columns)#sheet列名
    # 读取已存在的Excel文件
    existing_df = pd.read_excel(write_excel, sheet_name='Sheet1')
    # 使用concat函数将新数据和旧数据合并，忽略原索引
    combined_df = pd.concat([existing_df, df], ignore_index=True)
    # 将连接后的数据写入excel，即实现了数据的追加
    combined_df.to_excel(write_excel, sheet_name='Sheet1', index=False)


def get_different_question_types(excel_path):#按题型进行分类，每一类题型被分到一个二维列表中
    pre_department = ''
    type_result=[]
    question_types=[]
    df = pd.read_excel(excel_path)
    for index, row in df.iterrows():
        row=list(row)
        if pre_department=='':
            pre_department=row[0]
        if row[0]==pre_department:
            type_result.append(row)
        else:
            pre_department=row[0]
            question_types.append(type_result)
            type_result=[]
            type_result.append(row)
    question_types.append(type_result)
    return question_types

def get_department(question_type):#按科室进行分类，每一类科室被分到一个二维列表中
    departments=[]
    department_types=[]
    for question in question_type:
        if question[1] in departments:
            pass
        else:
            departments.append(question[1])
    for i in departments:
        department_types.append([])
    for question in question_type:
        i=departments.index(question[1])
        department_types[i].append(question)
    return department_types


def create_new_Excel_files(full_file_address,columns=[]):
    wb = Workbook()
    # 创建一个新的工作表
    wb.create_sheet(title="Sheet1")
    df = pd.DataFrame(columns=columns)  # sheet列名
    df.to_excel(full_file_address,sheet_name='Sheet1',index=False)


def get_rouge(real,model):
    re = " ".join(jieba.cut(real))      #分词
    pre = " ".join(jieba.cut(model))
    rouge = Rouge()
    rouge_scores=rouge.get_scores(re,pre)
    rouge_1=rouge_scores[0].get('rouge-1')['r']
    rouge_2=rouge_scores[0].get('rouge-2')['r']
    rouge_3=rouge_scores[0].get('rouge-l')['r']
    return [rouge_1,rouge_2,rouge_3]


def get_bleu(real,model):
    re = " ".join(jieba.cut(real))      #分词
    pre = " ".join(jieba.cut(model))
    score_1 = sentence_bleu([re.split()], pre.split(), weights=[1, 0, 0, 0])
    score_4 = sentence_bleu([re.split()], pre.split(), weights=[0, 0, 0, 1])
    return [score_1,score_4]

def short_answer_questions_statistics_by_departmental(type_departments):#简答题实验结果统计
    ls={}
    total_number = rouge_1 = rouge_2 = rouge_l = blue_1 = blue_4 = 0
    for class_departpent in type_departments:
        rouge_1 = rouge_2 = rouge_l = blue_1 = blue_4 = 0
        for row in class_departpent:
            new_rouge_1,new_rouge_2,new_rouge_l=get_rouge(row[2],row[3])
            new_blue_1,new_blue_4=get_bleu(row[2],row[3])

            rouge_1+=new_rouge_1
            rouge_2 += new_rouge_2
            rouge_l += new_rouge_l
            blue_1+=new_blue_1
            blue_4 += new_blue_4
            mean_score=(rouge_1+rouge_2+rouge_l+blue_1)/4/len(class_departpent)
        ls[class_departpent[0][1]]=[mean_score,len(class_departpent)]
        total_number+=len(class_departpent)
    ls['总题数']=total_number
    return ls

def case_question_Statistics(question_type):#案例题实验结果统计
    ls={}
    rouge_1 = rouge_2 = rouge_l = blue_1 = 0
    for row in question_type:
        new_rouge_1, new_rouge_2, new_rouge_l = get_rouge(row[2], row[3])
        new_blue_1, new_blue_4 = get_bleu(row[2], row[3])
        rouge_1 += new_rouge_1
        rouge_2 += new_rouge_2
        rouge_l += new_rouge_l
        blue_1 += new_blue_1
    mean_score = (rouge_1 / (len(question_type)) + rouge_2 / (len(question_type)) + rouge_l / (len(question_type)) + blue_1 / (len(question_type))) / 4
    ls['案例题均分']=mean_score
    return ls


def true_or_false_Statistics(type_departments):#判断题统计
    ls={}
    total_number=0
    for class_departpent in type_departments:
        total=correct=0
        max=3
        for row in class_departpent:
            if len(row[3]) < 3:
                max = len(row[3])
            if row[2].strip() == '对':
                total += 1
                if '对' in row[3][0:max] or '正确' in row[3][0:max]:
                    correct += 1
            else:
                total += 1
                if '错' in row[3][0:max]:
                    correct += 1
        ls[class_departpent[0][1]]=[correct/total,len(class_departpent)]
        total_number+=len(class_departpent)
    ls['总题数']=total_number
    return ls


def choice_question_statistics(type_departments):#选择题统计
    ls = {}
    total_number=0
    for class_departpent in type_departments:
        total=correct=0
        max=8
        for row in class_departpent:
            if len(str(row[3])) < 8:
                max = len(str(row[3]))
            if len(row[2])<=1:
                total += 1
                if row[2].strip() in row[3][0:max]:
                    correct += 1
            else:
                total += 1
                choice_num=0
                for ch in row[2]:
                    if ch in row[3][0:max]:
                        choice_num+=1
                if choice_num==len(row[2]):
                    correct+=1
        total_number+=len(class_departpent)
        ls[class_departpent[0][1]]=[correct/total,len(class_departpent)]
    ls['总题数']=total_number
    return ls

def connect_question(department_types):#连线题结果统计
    ls = {}
    total_number=0
    for department_type in department_types:
        total = 0
        correct_num = 0
        for row in department_type:
            correct_answers = row[2].split('\n')
            correct_answer_index = []
            total += 1
            for per_answer in correct_answers:
                i = str(row[3]).find(per_answer.strip())
                correct_answer_index.append(i)
            if -1 in correct_answer_index:
                continue
            rank_index = get_rank_index(correct_answer_index)
            data = statistical_data(rank_index, correct_answers)
            if data[-1] == True:
                correct_num += 1
        ls[department_type[0][1]]=[correct_num / total ,len(department_type)]
        total_number+=len(department_type)
    ls['总题数']=total_number
    return ls


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


def data_adjustment(all_results,departments):
    excel_rows=[]
    record=[]#用于记录客观题每个科室的题目数，最后一个数字是所有客观题的总题数
    select_mean=connect_mean=judge_mean=concise_mean=objective_score=0
    for department in departments:
        excel_row=[]
        if department !='总题数':
            excel_row.append(department)
            try:  ##选择题
                excel_row.append((all_results['选择题'][department][0])*100)
                select_mean += (all_results['选择题'][department][0]) * (all_results['选择题'][department][1] / all_results['选择题']['总题数'])*100
            except Exception as e:
                excel_row.append('此题型无该类科室')

            try:   ##判断题
                excel_row.append((all_results['判断题'][department][0])*100)
                judge_mean += (all_results['判断题'][department][0]) * (all_results['判断题'][department][1] / all_results['判断题']['总题数'])*100
            except Exception as e:
                excel_row.append('此题型无该类科室')

            try:  ##连线题
                excel_row.append((all_results['连线题'][department][0])*100)
                connect_mean += (all_results['连线题'][department][0]) * (all_results['连线题'][department][1] / all_results['连线题']['总题数'])*100
            except Exception as e:
                excel_row.append('此题型无该类科室')

            try:   ##简答题
                excel_row.append((all_results['简答题'][department][0])*100)
                concise_mean += (all_results['简答题'][department][0]) * (all_results['简答题'][department][1] / all_results['简答题']['总题数'])*100
            except Exception as e:
                excel_row.append('此题型无该类科室')

            try:
                connect_question_number_a_department = all_results['连线题'][department][1]
                connect_question_score_a_department=(all_results['连线题'][department][0])*100
            except Exception as e:
                connect_question_number_a_department = 0
                connect_question_score_a_department=0
            try:
                judge_question_number_a_department = all_results['判断题'][department][1]
                judge_question_score_a_department=(all_results['判断题'][department][0])*100
            except Exception as e:
                judge_question_number_a_department = 0
                judge_question_score_a_department=0
            try:
                select_question_number_a_department = all_results['选择题'][department][1]
                select_question_score_a_department=(all_results['选择题'][department][0])*100
            except Exception as e:
                select_question_number_a_department = 0
                select_question_score_a_department=0
            weight_base=(select_question_score_a_department!=0)*0.15+(judge_question_score_a_department!=0)*0.1+(connect_question_score_a_department!=0)*0.2
            if weight_base==0:
                weight_base=1
            objective_question_mean = (select_question_score_a_department * 0.15 + judge_question_score_a_department * 0.1 + connect_question_score_a_department * 0.2)/weight_base
            excel_row.append(objective_question_mean)

            excel_row.append('案例题无科室区分')
            excel_rows.append(excel_row)

            record.append(judge_question_number_a_department + select_question_number_a_department + connect_question_number_a_department)

    record.append(all_results['选择题']['总题数']+all_results['连线题']['总题数']+all_results['判断题']['总题数'])
    for i,re in enumerate(record[0:-1]):
        objective_score+= excel_rows[i][5]*(re/record[-1])
    excel_rows.append([' ',' ',' ',' ',' ',' ',' '])
    total=select_mean*0.15+judge_mean*0.1+connect_mean*0.2+concise_mean*0.25+all_results['案例题']['案例题均分']*100*0.3
    print('total score:',total)
    excel_rows.append(['题型均分',select_mean,judge_mean,connect_mean,concise_mean,objective_score,all_results['案例题']['案例题均分']*100])
    excel_rows.append([' ',' ',' ',' ',' ',' ',' '])

    excel_rows.append(['总得分',total])

    return excel_rows

def get_all_departments_type(question_types):
    ls=[]
    for question_type in question_types:
        for question in question_type:
            if question[1] in ls:
                pass
            else:
                ls.append(question[1])
    ls=pd.Series(ls).dropna().tolist()
    return ls

def score_computer(input_excel):
    all_results={}
    question_types=get_different_question_types(input_excel)
    departments=get_all_departments_type(question_types)
    for question_type in question_types:
        if '案例' in question_type[0][0]:
            try:
                case_question_results = case_question_Statistics(question_type)
                all_results['案例题'] = case_question_results

            except Exception as e:
                all_results['案例题']=' '
        else:
            department_types = get_department(question_type)
            if '判断' in question_type[0][0]:
                true_or_false_results=true_or_false_Statistics(department_types)
                all_results['判断题']=true_or_false_results
            if '选择' in question_type[0][0]:
                choice_question_results=choice_question_statistics(department_types)
                all_results['选择题']=choice_question_results
            if '配对' in question_type[0][0] or '连线' in question_type[0][0]:
                connect_question_results=connect_question(department_types)
                all_results['连线题']=connect_question_results
            if '简答' in question_type[0][0]:
                try:
                    concise_question_results = short_answer_questions_statistics_by_departmental(department_types)
                    all_results['简答题'] = concise_question_results
                except Exception as e:
                    all_results['简答题']=' '
    data=data_adjustment(all_results,departments)
    return data


if __name__=='__main__':
    input_excel='C:\\Users\\11048\Desktop\\evaluate.xlsx'#输入文件有4列：题型、科室、LLM回答、真实答案；
    output_excel='C:\\Users\\11048\Desktop\\out_evaluate.xlsx'#评估结果输出地址,指定地址即可，会自动创建
    data=score_computer(input_excel)
    #create_new_Excel_files(output_excel)
    write_QC_to_excel(data,output_excel)


