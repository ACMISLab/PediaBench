
# PediaBench：一个全面的中文儿科数据集，用于大型语言模型的基准测试

<p align="center">
<a href="https://github.com/ACMISLab/PediaBench/blob/main/README.md">🎨 English | <a href="https://github.com/ACMISLab/PediaBench/blob/main/README-ZH.md">🏞️ 中文</a>
</p>

## 👩‍🦱 1.介绍

PediaBench是首个全面的中国儿科数据集，旨在评估大型语言模型（LLM）在医学领域特别是在儿科问答（QA）方面的性能。
它包括来自不同数据源的4117个客观问题和1632个主观问题，涵盖了12类典型儿科疾病组的五种不同问题类型，如下所示。如果您想了解更多细节，请查看我们的[论文](https://arxiv.org/abs/2412.06287).

![image](https://github.com/ACMISLab/PediaBench/blob/main/figure/overview.png)


## 📚 2.数据集 
### 2.1 问题类型
为了评估LLMs在儿科领域的性能，PediaBench收集了以下五种类型的医学问题：

- **判断题 (ToF)**：这类问题询问一段陈述是否属实。它要求LLMs将陈述与自身知识中相应的概念和事实相匹配，理解它们的语义含义，并给出这段表述正确或者错误的判断。
- **多项选择题（MC）**：这类问题要求从多个选项中选择一个（或多个）合适的选项来完成一个句子或回答一个问题。它要求LLMs区分相似或相关的概念。有些问题还考察了LLMs的逻辑计算能力。
- **配对题（PA）**：这类问题要求将所有句子与候选列表中全匹配，区分相似的概念。因为任何不匹配都会导致完全错误的答案，所以PA比MC更难。
- **简答题（ES）**：这类问题要求人们详细阐述一个特定的概念。它要求LLMs生成与概念相关的连贯准确的文本。
- **案例分析（CA）**：这类问题向LLMs给出一个特定病例的描述，要求LLMs进行医学诊断并提供治疗措施。它可以全面评估LLMs在理解、推理和解决问题方面的医疗能力。


![image](https://github.com/ACMISLab/PediaBench/blob/main/figure/questions-types.png)



### 2.2数据统计
PediaBench数据集包含5749个问题，其中包括258个判断题、3576个选择题、283个配对题、1565个简答题和67个案例分析题。

根据世界卫生组织发布的国际疾病分类（ICD-11）标准，除病例分析问题外，其余5682个问题分为12个不同的疾病组，即肾系统疾病、急诊和重症监护、感染系统疾病、血液系统疾病、心血管系统疾病、免疫系统疾病、呼吸系统疾病、内分泌或代谢疾病、保健和发育异常、新生儿疾病、消化系统疾病和神经系统疾病。


![image](https://github.com/ACMISLab/PediaBench/blob/main/figure/data-example.png)


### 2.3评估标准
**为了准确评估儿科问答中每个LLM的表现，我们结合难度水平和自动评分构建了一套评分标准**

- **对于ToF和MC**：对于ToF和MC，我们s使用accuracy作为每个问题的性能指标。然后，我们设计了一个基于难度系数的评分方案来评估每个LLM的整体表现。首先我们根据每个LLM回答的准确性计算问题i的难度系数$Dc_i$。
具体来说，有$Dc_{i}=1-\frac{num^{acc_i}}{num^{llm_i}}$，其中$num^{acc}_i$是正确回答问题$i$的llm数量，$num^{llm}_i$是评估中所有llm的总数。
然后我们便可以将所有问题分为四个难度级别，即简单、一般、困难和超难，根据评分方案中的$Dc_i$为每个题目分配不同的权重$w_i$，分配标准如下所示： $Dc_i \in [0,0.2)$, score=0.5; $Dc_i \in [0.2,0.5)$, score=1; $Dc_i \in [0.5,0.8)$, score=1.5; $Dc_i \in [0.8,1]$, score=2。

- **对于PA**：我们规定：（1）完全正确的答案得3分；（2） 部分正确的答案得1分；（3）完全错误的答案得0分。

- **对于ES和CA**：它们是开放式问题，没有唯一的答案。CA比ES更难，因此为每个ES问题分配5分，为每个CA问题分配10分。基于LLMs的自动评分方案：为GPT-4o设置提示，让其充当裁判，对所有其他LLM的回答进行评分。并量化了人类和GPT-4o评分结果之间的一致性。

我们先基于上述标准计算出不同题目类型的准确率，再为每种题型赋予不同的分值（判断题 10 分，选择题 40 分，配对题 10 分，简答题 30 分，案例题 10 分）。最终LLMs的总分 $\mathrm{S}_{\text{total}} = \mathrm{S}_{\text{ToF}} \times {10} + \mathrm{S}_{\text{MC}} \times {40} + \mathrm{S}_{\text{PA}} \times{10} + \mathrm{S}_{\text{ES}} \times{30} + \mathrm{S}_{\text{CA}} \times{10}$

以下是不同难度级别的ToF和MC问题数量的统计数据。

![image](https://github.com/ACMISLab/PediaBench/blob/main/figure/difficult-level.png)


## 🎡 3.实验

### 3.1 待评测的模型信息

表格展示了待评测LLMs的详细信息。其中“Domain”表示LLM是通用模型还是专门用于医疗领域的模型，“#Parameters”表示LLM的参数数量（“n/a”表示没有公布参数大小的商业模型）， “Context Window”显示LLM上下文窗口的大小， “How Accessed”表示我们如何访问LLM进行实验（开源模型下载其权重并在我们自己的服务器上本地部署，商业模型通过其官方API访问）。

![image](https://github.com/ACMISLab/PediaBench/blob/main/figure/models-list.png)


### 3.2 主要结果

我们在20个通用和医学LLM上验证了PediaBench，其中包括各种规模的开源和商业模型。我们为所有LLM设置了标准化的提示集，并在所有实验中一致采用zero-shot。LLM的整体性能结果如下所示。BianQue-7B和QizhenGPT-13B不能正确理解和遵循客观题的回复要求，因此他们在这些类型中的得分为0。

![image](https://github.com/ACMISLab/PediaBench/blob/main/figure/main-result2.png)


🎯 **结果分析**

🎐 基于基准测试结果，我们观察到llm的性能在不同的问题类型中有所不同。大多数llm在ToF和ES问题上表现更好，而他们在PA和CA问题上表现困难。这是因为ToF问题可以被视为一个二分类问题，即使没有任何相关的医学知识，LLM也有50%的机会猜出正确的答案。相比之下，有四种选择的MC问题更难猜出正确结果。PA问题是最具挑战性的客观问题类型。此外，ES问题没有固定的答案。只要LLM的回答是相关且真实的，它就可以得到相应的分数。然而，CA问题的答案相对固定，这要求llm具有医疗诊断能力。因此，llm在ToF和ES问题上表现得更好。

🎣 我们的研究结果表明，LLM有潜力帮助患者和医生理解和治疗疾病。一些表现良好的商业LLM，如Qwen-MAX、ERNIE-3.5和GLM-4，在我们的评估中得分超过70分。他们具有较强的逻辑推理能力，能够有效地解决疾病的诊断和治疗问题。然而，考虑到医疗领域的严谨性和对安全性的严格要求，在将llm应用于现实世界的诊断和治疗场景时，确保智能诊断的可靠性至关重要的。要实现理由LLM帮助患者和医生理解和治疗疾病的目标，仍需要进一步的探索。

🪁 目前，LLM的回答不能被认为是可靠的任何类型的问题。我们分析了模型的答案和解释，发现即使是我们研究中最先进的模型Qwen-MAX，仍然存在不可避免的幻觉问题。对于LLM回答错误的问题，其回答和解释也是错误的，这表明LLM对医学问题的回答是不可靠的。因此，LLM在实际医疗应用中需要谨慎使用，特别是在复杂的临床决策中。

### 3.3 ES题目的多维度实验结果
我们为GPT-4o设置提示，让其充当裁判，对所有其他LLM对ES题目的回答进行评分。我们对模型回答的四个维度进行评估：准确性、全面性、流畅性、总体评分。最后我们将总体评分的分数作为LLMs在ES问题上的最终得分。


![image](https://github.com/ACMISLab/PediaBench/blob/main/figure/total-radar.png)

可以看出，大多数LLM在流畅性方面表现良好，但在全面性和准确性方面需要进一步改进。特别是在医疗领域，准确性是一个十分关键的问题。在后续的研究中，应该避免模型产生幻觉，并确保LLM回复的正确性。

### 3.4 不同疾病组的结果
我们给出了不同LLMs在不同疾病组上的分数，大多数模型在DImS的HCDA两个疾病组中得分较高。任何模型都不能很好地回答主观题。

![image](https://github.com/ACMISLab/PediaBench/blob/main/figure/disease-group-results.png)




## 🚀 4.使用指南
- pediabench数据集位于`/data`目录中。在获得模型的答案后，请将模型对于五种类问题的回答整理成`.xlsx`文件。然后使用评估代码获得结果。

- 您需要提交的`.xlsx`文件应该类似于`samples.xlsx`。

- 通过运行评估代码，您将收到一个`.xlsx`文件，其中包含不同疾病组不同问题类型的分数，以及最终的加权总分。


## 😄 5.其他
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
    




