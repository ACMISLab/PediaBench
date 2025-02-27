# PediaBench: A Comprehensive Chinese Pediatric Dataset for Benchmarking Large Language Models






<p align="center">
<a href="https://github.com/ACMISLab/PediaBench/blob/main/README.md">🎨 English | <a href="https://github.com/ACMISLab/PediaBench/blob/main/README-ZH.md">🏞️ 中文</a>
</p>


## 👩‍🦱 1. Introduction

PediaBench is the first comprehensive Chinese pediatric dataset designed to evaluate the performance of large language models (LLMs) in the medical field, particularly in pediatric question answering (QA). 

It comprises 4,117 objective and 1,632 subjective questions sourced from diverse channels, covering five distinct question types across 12 typical pediatric disease groups, as shown below. If you would like to learn more details, please check our [paper](https://arxiv.org/abs/2412.06287).

![image](https://github.com/ACMISLab/PediaBench/blob/main/figure/overview.png)

## 📚 2.Dataset 
### 2.1 Types of Questions
To assess how well an LLM can serve as an AI assistant for pediatricians, PediaBench incorporates the following five typical types of medical questions for evaluation:

- **True or False (ToF)**: This type of question asks whether a statement is factual. It requires an LLM to match the statement with its corresponding concepts and facts in the corpus, to understand their semantic meanings, and to reason about them so as to detect possible errors and contradictions.
- **Multiple Choice (MC)**: This type of question asks for the selection of one (or more) appropriate choices from multiple candidates to complete a sentence or answer a question. It requires an LLM to distinguish between similar or related concepts. Some questions also evaluate the mathematical and logical skills of an LLM, as basic calculations are essential to obtain the correct answer.
- **Pairing (PA)**: This type of question requires exactly matching all sentences with their corresponding missing words from the candidate list. Distinguishing among similar concepts is also essential for PA. However, since any mismatch leads to an entirely erroneous answer, PA is even more challenging than MC.
- **Essay/Short Answer (ES)**: This type of question asks one to elaborate on a specific concept. It requires an LLM to generate coherent and accurate text relevant to the concept.
- **Case Analysis (CA)**: This type of question presents an LLM with a description of a particular instance and asks the LLM to make a medical diagnosis and provide treatment measures. It can comprehensively evaluate the medical capacity of an LLM in terms of comprehension, reasoning, and problem-solving.

![image](https://github.com/ACMISLab/PediaBench/blob/main/figure/questions-types.png)

### 2.2 Dataset Statistics
The PediaBench dataset consists of 5,749 questions, including 258 true-or-false questions, 3,576 multiple-choice questions, 283 pairing questions, 1,565 essay/short-answer questions, and 67 case analysis questions.

Referring to the International Classification of Diseases (ICD-11) standard issued by the WHO, except for case analysis questions, the remaining 5,682 questions are organized into 12 distinct disease groups, namely, diseases of the renal system, emergency and critical care, diseases of the infection system, diseases of the blood system, diseases of the cardiovascular system, diseases of the immune system, diseases of the respiratory system, endocrine or metabolic diseases, health care and developmental abnormalities, neonatal diseases, diseases of the alimentary system, and diseases of the nervous system.


![image](https://github.com/ACMISLab/PediaBench/blob/main/figure/data-example.png)

### 2.3 Evaluation Criteria
**To provide an accurate evaluation of the performance of each LLM for QA in pediatrics, we use a scoring criterion that combines difficulty levels and automatic scoring.**

- **For ToF and MC:** We use \emph{accuracy} as a basic performance measure for each question.
Then, we design a scoring scheme based on \emph{difficulty coefficient} to assess the overall performance of each LLM.
We calculate the difficulty coefficient $Dc_i$ of each question $i$ based on the accuracy of each LLM's answer.
Specifically, we have $Dc_{i}=1-\frac{num^{acc_i}}{num^{llm_i}}$, where $num^{acc}_i$ is the number of LLMs that correctly answer question $i$ and $num^{llm}_i$ is the total number of LLMs in the evaluation.
All questions are then divided into four \emph{difficulty levels}, namely \emph{simple}, \emph{normal}, \emph{difficult}, and \emph{extreme}, with different weights $w_i$ based on $Dc_i$ in the scoring scheme as follows: $Dc_i \in [0,0.2)$, score=0.5; $Dc_i \in [0.2,0.5)$, score=1; $Dc_i \in [0.5,0.8)$, score=1.5; $Dc_i \in [0.8,1]$, score=2.

- **For PA:** We use the following scoring rules: (1) A completely correct answer gets 3 points; (2) a partially correct answer gets 1 point; and (3) a completely incorrect answer does not get any points.


- **For ES and CA:** They are open questions with no unique answers.
CA is even harder than ES so we assign a weight of 5 to each ES question and 10 to each CA question.
specially, we introduce an automated scoring scheme based on LLMs.
We set up prompts for GPT-4o to act as a referee to rate the responses of all other LLMs. and quantify the agreement between the human and GPT-4o scoring results.

We first calculate the accuracy of different types of questions based on the above criteria, and then assign different scores to them (10 points for ToF questions, 40 points for MC questions, 10 points for PA questions, 30 points for ES questions, and 10 points for CA questions). Then final total score of LLMs is obtained by: $\mathrm{S}_{\text{total}} = \mathrm{S}_{\text{ToF}} \times {10} + \mathrm{S}_{\text{MC}} \times {40} + \mathrm{S}_{\text{PA}} \times{10} + \mathrm{S}_{\text{ES}} \times{30} + \mathrm{S}_{\text{CA}} \times{10}$. 

The following is the statistical data on the number of ToF and MC questions at different difficulty levels.

![image](https://github.com/ACMISLab/PediaBench/blob/main/figure/difficult-level.png)

## 🎡 3. Experiment

### 3.1 List of LLMs in the Experiments
Table 6 presents detailed information on the LLMs we evaluate and use, where “Domain” indicates whether an LLM is of general purpose or specialized in the medical domain, “#Parameters” presents the number of parameters of an LLM (“n/a” for commercial models with disclosed parameter numbers), “Context Window” reveals the size of the context window of an LLM, “How Accessed” indicates how we accessed an LLM for experimentation (open-source models are obtained through their weights and deployed locally on our own servers and commercial models are accessed via their official APIs).

![image](https://github.com/ACMISLab/PediaBench/blob/main/figure/models-list.png)


### 3.2 Main Results

We validate PediaBench through experiments with 20 general-purpose and medical LLMs, including open-source and commercial models of various scales. A standardized prompt set was developed for all LLMs, and a zero-shot prompt setting was applied consistently across all experiments. The results for the overall performance of LLMs are shown below. BianQue-7B and QiZhenGPT-13B cannot correctly understand and follow the instructions for the objective questions, thus their scores are 0 for these types.

![image](https://github.com/ACMISLab/PediaBench/blob/main/figure/main-result2.png)


🎯 **Result Analysis**

🎐 Based on the benchmark results, we have observed that the performance of LLMs varies across different question types. Most LLMs perform better on ToF and ES questions, while they struggle with PA and CA questions. This is because ToF questions can be regarded as a binary classification problem, where LLMs have a 50% chance of guessing the correct answer even without any medical knowledge. In contrast, MC questions, with four options, are harder to guess correctly. PA questions are the most challenging type of objective questions. Additionally, ES questions have no fixed answers. As long as the LLM’s response is relevant and factual, it can earn some points. However, CA questions have relatively fixed answers, which require LLMs to have medical diagnostic capabilities. Therefore, LLMs perform better on
the ToF and ES questions.

🎣 Our results show that LLMs have the potential to assist patients and doctors in understanding and treating diseases. Some well-performing commercial LLMs, such as Qwen-MAX, ERNIE-3.5-8K-0329, and GLM-4, scored over 70 in our evaluation. They have strong logical reasoning abilities and can effectively address disease diagnosis and treatment issues. However, given the rigor of the medical field and the strict requirement for safety, ensuring the reliability of intelligent diagnosis is crucial when applying LLMs to real-world diagnostic and treatment scenarios. Further exploration is still needed to achieve these goals.

🪁 Currently, LLMs’ responses cannot be considered as reliable for any type of question. We analyzed the models’ answers and explanations and found that even the most advanced model in our study, Qwen-MAX, still has unavoidable hallucination issues. For questions that the LLM answered incorrectly, its responses and explanations were also wrong, showing that LLMs’ responses to medical questions are unreliable. Therefore, LLMs need to be used cautiously in practical medical applications, especially in complex clinical decision making.

### 3.3 Results for ES questions

We designed prompts for GPT-4o to serve as a referee, evaluating the answers of other LLMs to ES questions. We assessed the model responses across four dimensions: accuracy, comprehensiveness, fluency, and overall rating. The overall score was then used as the final evaluation metric for the LLMs' performance on ES questions.

![image](https://github.com/ACMISLab/PediaBench/blob/main/figure/total-radar.png)

Most LLMs perform well in terms of fluency but require further improvements in terms of comprehensiveness and accuracy. Especially in the medical field, accuracy should be considered a crucial and indispensable issue. Therefore, in-depth investigations should be performed to avoid hallucination and ensure the correctness of the LLM responses.


### 3.4 Results in different disease groups 
In order to quantify the score, we calculated the proportion of LLMs' score based on the inconsistent number of questions and scores for each disease group. Most models achieve their highest scores in the two disease groups of HCDA of DImS.
No models can perform well for subjective questions in all performance measures across different groups of diseases. 

![image](https://github.com/ACMISLab/PediaBench/blob/main/figure/disease-group-results.png)



## 🚀 4. Usage Guide
- The pediabench dataset is located in the `/data` directory. After obtaining the model's responses, please compile the model's answers to the five question types into an `.xlsx` file. Then, use the evaluation code to obtain the results.

- The `.xlsx` file you need to submit should refer to the following file: `samples.xlsx`.

- By running the evaluate code, you will receive an `.xlsx` file containing scores for different question types across different disease groups, as well as a final weighted total score.

## 😄 5. Side notes
### 5.1 Limilation
Despite the abundance of pediatric questions in the PediaBench dataset, it still cannot encompass many pediatric diseases and their corresponding treatments in the real world.
Therefore, the PediaBench dataset should be maintained with a continual effort for better coverage.
Currently, PediaBench is focusing primarily on pediatrics. In future work, we plan to extend it to more medical departments.
In addition, although the scoring method based on GPT-4o strongly correlates with human scoring, we cannot fully determine whether GPT-4o scoring tends towards a certain style, leading to potential biases. To address this issue, we will consider more rigorous scoring strategies in the future, such as using multiple LLMs for ensembling.
### 5.2 Ethics in Data Collection

All data sources we use to construct the PediaBench dataset are publicly available and free to use without copyright infringement. All questions in the PediaBench dataset have been appropriately anonymized so that they do not contain sensitive private information about patients. We do not foresee any other possible negative societal impacts of this work.


## Citation
If you find the code and test set useful for your research, please consider citing:

    @misc{zhang2024pediabenchcomprehensivechinesepediatric,
      title={PediaBench: A Comprehensive Chinese Pediatric Dataset for Benchmarking Large Language Models}, 
      author={Qian Zhang and Panfeng Chen and Jiali Li and Linkun Feng and Shuyu Liu and Mei Chen and Hui Li and Yanhao Wang},
      year={2024},
      eprint={2412.06287},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2412.06287}, 
    }
    