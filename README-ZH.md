# PediaBench
**PediaBench：一个全面的中文儿科数据集，用于大型语言模型的基准测试**
![image](https://github.com/ACMISLab/PediaBench/blob/main/overview.png)
PediaBench是首个全面的中文儿科数据集，旨在评估大型语言模型（LLMs）在医学领域，特别是儿科问答（QA）中的性能。该数据集包含客观和主观问题，涵盖了广泛的儿科疾病，并评估模型在指令遵循、知识理解和临床案例分析方面的能力。

## 数据特点
- 多样的问题类型：包含4565个客观问题和1632个主观问题，跨越12个儿科疾病组。
- 综合评分标准：基于五种问题类型评估LLMs的熟练程度。

![image](https://github.com/ACMISLab/PediaBench/blob/main/data-example.png)

## 使用指南
pediabench数据集位于/data目录中，在获取到模型的回答之后，请将模型对于五种题目的回答汇总于一个xlsx文件中，接着使用评估代码xx运行得到结果。

您需要提交的xlsx文件应参照以下文件：samples.xlsx

通过evaluate代码，您将获得一个xlsx文件，其中包含不同题型在不同疾病组上的得分，以及最终加权得到的总分。

## 引用
如果您发现代码和测试集对您的研究有用，请考虑引用
```
**待添加引用**
```
