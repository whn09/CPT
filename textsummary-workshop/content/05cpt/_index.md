+++
title = "动手实验4: 基于Amazon SageMaker的CPT中文摘要模型训练动手实验型"
weight = 5
chapter = true
pre = "<b>5. </b>"
+++

## 模型架构

CPT的具体结构可以看作一个输入，多个输出的非对称结构，主要包括三个部分: 
* S-Enc (Shared Encoder): 共享Encoder，双向attention结构，建模输入文本。 
* U-Dec (Understanding Decoder): 理解用Decoder，双向attention结构，输入S-Enc得到的表示，输出MLM的结果。为模型增强理解任务。 
* G-Dec (Generation Decoder): 生成用Decoder，正如BART中的Decoder模块，利用encoder-decoder attention与S-Enc相连，用于生成。  


![](../pics/05CPT/1.png)

## 模型介绍

该模型的结果SOTA：在生成任务上，在生成任务上CPT拥有与BART匹配的能力。在两个摘要数据集 (LCSTS和CSL) 和一个长文本生成数据集ADGEN测试的模型。 
![](../pics/05CPT/2.png)

## reference

* paper： https://arxiv.org/pdf/2109.05729.pdf
* source code：https://github.com/fastnlp/CPT 

@article{shao2021cpt,
  title={CPT: A Pre-Trained Unbalanced Transformer for Both Chinese Language Understanding and Generation}, 
  author={Yunfan Shao and Zhichao Geng and Yitao Liu and Junqi Dai and Fei Yang and Li Zhe and Hujun Bao and Xipeng Qiu},
  journal={arXiv preprint arXiv:2109.05729},
  year={2021}
}


