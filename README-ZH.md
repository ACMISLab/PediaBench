
# PediaBench：一个全面的中文儿科数据集，用于大型语言模型的基准测试

<p align="center">
<a href="https://github.com/ACMISLab/PediaBench/blob/main/README.md">English | <a href="https://github.com/ACMISLab/PediaBench/blob/main/README_ZH.md">中文</a>
</p>

## 1.介绍

PediaBench是首个全面的中国儿科数据集，旨在评估大型语言模型（LLM）在医学领域特别是在儿科问答（QA）方面的性能。
它包括来自不同数据源的4565个客观问题和1632个主观问题，涵盖了12类典型儿科疾病组的五种不同问题类型，如下所示。如果您想了解更多细节，请查看我们的[论文](https://arxiv.org/abs/2412.06287).

![image](https://github.com/ACMISLab/PediaBench/blob/main/figure/overview.png)


## 2.数据集 
### 2.1 问题类型
为了评估LLMs在儿科领域的性能，PediaBench收集了以下五种类型的医学问题：

- **判断题 (ToF)**：这类问题询问一段陈述是否属实。它要求LLMs将陈述与自身知识中相应的概念和事实相匹配，理解它们的语义含义，并给出这段表述正确或者错误的判断。
- **多项选择题（MC）**：这类问题要求从多个选项中选择一个（或多个）合适的选项来完成一个句子或回答一个问题。它要求LLMs区分相似或相关的概念。有些问题还考察了LLMs的逻辑计算能力。
- **配对题（PA）**：这类问题要求将所有句子与候选列表中全匹配，区分相似的概念。因为任何不匹配都会导致完全错误的答案，所以PA比MC更难。
- **简答题（ES）**：这类问题要求人们详细阐述一个特定的概念。它要求LLMs生成与概念相关的连贯准确的文本。
- **案例分析（CA）**：这类问题向LLMs给出一个特定病例的描述，要求LLMs进行医学诊断并提供治疗措施。它可以全面评估LLMs在理解、推理和解决问题方面的医疗能力。


![image](https://github.com/ACMISLab/PediaBench/blob/main/figure/questions-types.png)



###2.2数据统计
PediaBench数据集包含5749个问题，其中包括258个判断题、3576个选择题、283个配对题、1565个简答题和67个案例分析题。

根据世界卫生组织发布的国际疾病分类（ICD-11）标准，除病例分析问题外，其余5682个问题分为12个不同的疾病组，即肾系统疾病、急诊和重症监护、感染系统疾病、血液系统疾病、心血管系统疾病、免疫系统疾病、呼吸系统疾病、内分泌或代谢疾病、保健和发育异常、新生儿疾病、消化系统疾病和神经系统疾病。


![image](https://github.com/ACMISLab/PediaBench/blob/main/figure/data-example.png)


###2.3评估标准
**为了准确评估儿科问答中每个LLM的表现，我们结合难度水平和自动评分构建了一套评分标准**

- **对于ToF和MC：**我们将准确性作为每个问题的基本绩效衡量标准。并设计了一个基于难度系数的评分方案，然后将所有问题分为四个难度级别，即简单、正常、困难和超难。

- **对于PA：**我们规定：（1）完全正确的答案得3分；（2） 部分正确的答案得1分；（3）完全错误的答案得0分。

- **对于ES和CA：**它们是开放式问题，没有唯一的答案。CA比ES更难，因此为每个ES问题分配5个权重，为每个CA问题分配10个权重。基于LLMs的自动评分方案：为GPT-4o设置提示，让其充当裁判，对所有其他LLM的回答进行评分。并量化了人类和GPT-4o评分结果之间的一致性。


LLMs得到的总分为正确回答问题的得分的总和。以下是不同难度级别的ToF和MC问题数量的统计数据。

![image](https://github.com/ACMISLab/PediaBench/blob/main/figure/difficult-level.png)


## 3.实验
### 3.1主要结果

我们在20个通用和医学LLM上验证了PediaBench，其中包括各种规模的开源和商业模型。我们为所有LLM设置了标准化的提示集，并在所有实验中一致采用zero-shot。LLM的整体性能结果如下所示。BianQue-7B和QizhenGPT-13B不能正确理解和遵循客观题的回复要求，因此他们在这些类型中的得分为0。

![image](https://github.com/ACMISLab/PediaBench/blob/main/figure/main-results.png)

### 3.2不同疾病组的结果
我们给出了不同LLMs在不同疾病组上的分数，大多数模型在DImS的HCDA两个疾病组中得分较高。任何模型都不能很好地回答主观题。

![image](https://github.com/ACMISLab/PediaBench/blob/main/figure/disease-group-results.png)

## 4.使用指南
- pediabench数据集位于`/data`目录中。在获得模型的答案后，请将模型对于五种类问题的回答整理成`.xlsx`文件。然后使用评估代码获得结果。

- 您需要提交的`.xlsx`文件应该类似于`samples.xlsx`。

- 通过运行评估代码，您将收到一个`.xlsx`文件，其中包含不同疾病组不同问题类型的分数，以及最终的加权总分。


## 5.其他
### 5.1 限制
- 尽管PediaBench数据集中有大量的儿科问题，但它仍然无法涵盖现实世界中的许多儿科疾病及其相应的治疗方法。
因此，我们后续将持续维护和更新PediaBench数据集，以覆盖更广泛的疾病。
- 目前PediaBench主要专注于儿科。在未来的工作中，我们计划将其扩展到更多的医疗科室。
- 尽管基于GPT-4o的评分方法与人类评分存在较高的相关性，但我们无法完全确定GPT-4o评分是否倾向于某种风格，从而导致潜在的偏差。为了解决这个问题，我们将在未来考虑更严格的评分策略，例如使用多个LLM进行组合。
### 5.2 伦理道德

我们用于构建PediaBench数据集的所有数据源都是公开可用的，可以免费使用，不侵犯版权。PediaBench数据集中的所有问题都经过了适当的匿名处理，因此不包含有关患者的敏感私人信息。我们预计这项工作不会产生任何其他可能的负面社会影响。




## 引用
如果您发现代码和测试集对您的研究有用，请考虑引用：

    @misc{zhang2024pediabenchcomprehensivechinesepediatric,
      title={PediaBench: A Comprehensive Chinese Pediatric Dataset for Benchmarking Large Language Models}, 
      author={Qian Zhang and Panfeng Chen and Jiali Li and Linkun Feng and Shuyu Liu and Mei Chen and Hui Li and Yanhao Wang},
      year={2024},
      eprint={2412.06287},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2412.06287}, 
    }
    




