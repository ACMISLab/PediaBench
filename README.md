# PediaBench: A Comprehensive Chinese Pediatric Dataset for Benchmarking Large Language Models






<p align="center">
<a href="https://github.com/SJTU-LIT/ceval/blob/main/README.md">English | <a href="https://github.com/SJTU-LIT/ceval/blob/main/README_zh.md">中文</a>
</p>


## 1. Introduction

PediaBench is the first comprehensive Chinese pediatric dataset designed to evaluate the performance of large language models (LLMs) in the medical field, particularly in pediatric question answering (QA). 

It comprises 4,565 objective and 1,632 subjective questions sourced from diverse channels, covering five distinct question types across 12 typical pediatric disease groups, as shown below. If you would like to learn more details, please check our [paper](https://arxiv.org/abs/xxxx).

![image](https://github.com/ACMISLab/PediaBench/blob/main/overview.png)

## 2.Dataset 
### 2.1 Types of Questions
To assess how well an LLM can serve as an AI assistant for pediatricians, PediaBench incorporates the following five typical types of medical questions for evaluation:

- **True or False (ToF)**: This type of question asks whether a statement is factual. It requires an LLM to match the statement with its corresponding concepts and facts in the corpus, to understand their semantic meanings, and to reason about them so as to detect possible errors and contradictions.
- **Multiple Choice (MC)**: This type of question asks for the selection of one (or more) appropriate choices from multiple candidates to complete a sentence or answer a question. It requires an LLM to distinguish between similar or related concepts. Some questions also evaluate the mathematical and logical skills of an LLM, as basic calculations are essential to obtain the correct answer.
- **Pairing (PA)**: This type of question requires exactly matching all sentences with their corresponding missing words from the candidate list. Distinguishing among similar concepts is also essential for PA. However, since any mismatch leads to an entirely erroneous answer, PA is even more challenging than MC.
- **Essay/Short Answer (ES)**: This type of question asks one to elaborate on a specific concept. It requires an LLM to generate coherent and accurate text relevant to the concept.
- **Case Analysis (CA)**: This type of question presents an LLM with a description of a particular instance and asks the LLM to make a medical diagnosis and provide treatment measures. It can comprehensively evaluate the medical capacity of an LLM in terms of comprehension, reasoning, and problem-solving.

![image](https://github.com/ACMISLab/PediaBench/blob/main/question-types.png)

### 2.2 Dataset Statistics
The PediaBench dataset consists of 5,749 questions, including 258 true-or-false questions, 3,576 multiple-choice questions, 283 pairing questions, 1,565 essay/short-answer questions, and 67 case analysis questions.

Referring to the International Classification of Diseases (ICD-11) standard issued by the WHO, except for case analysis questions, the remaining 5,682 questions are organized into 12 distinct disease groups, namely, diseases of the renal system, emergency and critical care, diseases of the infection system, diseases of the blood system, diseases of the cardiovascular system, diseases of the immune system, diseases of the respiratory system, endocrine or metabolic diseases, health care and developmental abnormalities, neonatal diseases, diseases of the alimentary system, and diseases of the nervous system.


![image](https://github.com/ACMISLab/PediaBench/blob/main/data-example.png)

### 2.3 Evaluation Criteria
**To provide an accurate evaluation of the performance of each LLM for QA in pediatrics, we use a scoring criterion that combines difficulty levels and automatic scoring.**

- **For ToF and MC:** We use accuracy as a basic performance measure for each question. And design a scoring scheme based on difficulty coefficient to assess the overall performance of each LLM.
All questions are then divided into four difficulty levels, namely **simple**, **normal**, **difficult**, and **extreme**

- **For PA:** We use the following scoring rules: (1) A completely correct answer gets 3 points; (2) a partially correct answer gets 1 point; and (3) a completely incorrect answer does not get any points.


- **For ES and CA:**They are open questions with no unique answers.
CA is even harder than ES so we assign a weight of 5 to each ES question and 10 to each CA question.
specially, we introduce an automated scoring scheme based on LLMs.
We set up prompts for GPT-4o to act as a referee to rate the responses of all other LLMs. and quantify the agreement between the human and GPT-4o scoring results.


The overall score of an LLM for all questions is the weighted sum of the scores of all correctly answered questions. The following is a statistics on the number of ToF and MC questions at different difficulty levels.

![image](https://github.com/ACMISLab/PediaBench/blob/main/difficult-level.png)

## 3. Experiment
### 3.1 Main Results

We validate PediaBench through experiments with 20 general-purpose and medical LLMs, including open-source and commercial models of various scales. A standardized prompt set was developed for all LLMs, and a zero-shot prompt setting was applied consistently across all experiments. The results for the overall performance of LLMs are shown below. BianQue-7B and QiZhenGPT-13B cannot correctly understand and follow the instructions for the objective questions, thus their scores are 0 for these types.

![image](https://github.com/ACMISLab/PediaBench/blob/main/main-results.png)

### 3.2 Results in different disease groups 
In order to quantify the score, we calculated the proportion of LLMs' score based on the inconsistent number of questions and scores for each disease group. Most models achieve their highest scores in the two disease groups of HCDA of DImS.
No models can perform well for subjective questions in all performance measures across different groups of diseases. 

![image](https://github.com/ACMISLab/PediaBench/blob/main/disease-group-results.png)

## 4. Usage Guide
The pediabench dataset is located in the /data directory. After obtaining the model's responses, please compile the model's answers to the five question types into an xlsx file. Then, use the evaluation code to obtain the results.

The xlsx file you need to submit should refer to the following file: `samples.xlsx`.

By running the evaluate code, you will receive an xlsx file containing scores for different question types across different disease groups, as well as a final weighted total score.

## 5. Side notes
### 5.1 Limilation
Despite the abundance of pediatric questions in the PediaBench dataset, it still cannot encompass many pediatric diseases and their corresponding treatments in the real world.
Therefore, the PediaBench dataset should be maintained with a continual effort for better coverage.
Currently, PediaBench is focusing primarily on pediatrics. In future work, we plan to extend it to more medical departments.
In addition, although the scoring method based on GPT-4o strongly correlates with human scoring, we cannot fully determine whether GPT-4o scoring tends towards a certain style, leading to potential biases. To address this issue, we will consider more rigorous scoring strategies in the future, such as using multiple LLMs for ensembling.
### 5.2 Ethics in Data Collection

All data sources we use to construct the PediaBench dataset are publicly available and free to use without copyright infringement. All questions in the PediaBench dataset have been appropriately anonymized so that they do not contain sensitive private information about patients. We do not foresee any other possible negative societal impacts of this work.


## Citation
If you find the code and test set useful for your research, please consider citing:

     @article{Pediabench,
      title={PediaBench: A Comprehensive Chinese Pediatric Dataset for Benchmarking Large Language Models},
      author={Qian Zhang,Panfeng Chen,  Jiali Li, Linkun Feng, Shuyu Liu, Mei Chen, Hui Li, Yanhao Wang},
      journal={arXiv preprint arXiv:xxxx},
      year={2024}
    }
