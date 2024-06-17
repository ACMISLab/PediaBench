# PediaBench
## PediaBench: A Comprehensive Chinese Pediatric Dataset for Benchmarking Large Language Models
![image](https://github.com/ACMISLab/PediaBench/blob/main/overview.png)
PediaBench is the first comprehensive Chinese pediatric dataset designed to evaluate the performance of large language models (LLMs) in the medical field, particularly in pediatric question answering (QA). The dataset comprises both objective and subjective questions covering a wide range of pediatric diseases and assesses the models' capabilities in instruction following, knowledge understanding, and clinical case analysis.

## Dataset Features
Diverse Types of Questions : Includes 4,565 objective questions and 1,632 subjective questions spanning 12 pediatric disease groups.
Comprehensive Scoring Criteria: Assesses LLMs' proficiency based on five question types.
![image](https://github.com/ACMISLab/PediaBench/blob/main/data example.png)

## Usage Guide
The pediabench dataset is located in the /data directory. After obtaining the model's responses, please compile the model's answers to the five question types into an xlsx file. Then, use the evaluation code to obtain the results.

The xlsx file you need to submit should refer to the following file: samples.xlsx.

By running the evaluate code, you will receive an xlsx file containing scores for different question types across different disease groups, as well as a final weighted total score.

Citation
If you find the code and test set useful for your research, please consider citing

**Citation to be added**
