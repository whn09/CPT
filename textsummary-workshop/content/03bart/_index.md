+++
title = "动手实验2: 基于Amazon SageMaker的Huggingface训练一个BART英文摘要模型"
weight = 3
chapter = true
pre = "<b>3. </b>"
+++

## 模型架构

BART架构由两个主要组件组成：编码器和解码器。
* 使用BERT的编码器组件，该组件用于从两个方向对输入语句进行编码，以获得更多上下文信息。
* BART使用了来自GPT的解码器组件，该解码器组件用于重构噪声输入。然而，单词只能在leftward上下文使用，所以它不能学习双向互动。

除了解码器部分使用GeLU激活函数而非ReLU外，BART使用标准的序列到序列transformer架构，参数的初始化是从N(0.0, 0.02)开始的。BART有两种变体，基本模型在编码器和解码器中使用6层，而大型模型则每个使用12层。

![](../pics/03bart/1.png)

## 模型介绍

BART是一种采用序列到序列模型构建的降噪自编码器，适用于各种最终任务。它使用基于标准transformer的神经机器翻译架构。BART的预训练包括：

1）使用噪声函数破坏文本;
![](../pics/03bart/3.png)

2）学习序列到序列模型以重建原始文本。

这些预训练步骤的主要优势在于：该模型可以灵活处理原始输入文本，并学会有效地重建文本。

当为文本生成进行微调（fine-tuned）时，BART提供了健壮的性能，并且在理解任务中也能很好地工作。

该模型的结果SOTA：
![](../pics/03bart/2.png)

结果范例： BART在摘要任务上做得非常出色。以下示例摘要由BART生成。示例取自Wikinews文章。正如您所看到的，模型输出是流利且符合语法的英语。然而，模型输出也是高度抽象的，从输入中复制的短语很少
![](../pics/03bart/4.png)

## reference

* paper： https://arxiv.org/pdf/1910.13461.pdf
* source code： https://github.com/pytorch/fairseq/tree/main/examples/bart 

@article{lewis2019bart,
    title = {BART: Denoising Sequence-to-Sequence Pre-training for Natural
Language Generation, Translation, and Comprehension},
    author = {Mike Lewis and Yinhan Liu and Naman Goyal and Marjan Ghazvininejad and
              Abdelrahman Mohamed and Omer Levy and Veselin Stoyanov
              and Luke Zettlemoyer },
    journal={arXiv preprint arXiv:1910.13461},
    year = {2019},
}

