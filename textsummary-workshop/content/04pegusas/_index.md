+++
title = "基于Amazon SageMaker的PEGUSAS模型部署动手实验"
weight = 4
chapter = true
pre = "<b>4. </b>"
+++

使用谷歌2020pegasus模型进行中文文档摘要

谷歌于去年年底发布了一个精简型的机器语义分析项目：飞马(PEGASUS)：预先机器学习及训练后的自动文章摘要项目。近期这个项目迎来的新的版本，这个小型项目可以非常精准的自动提取出文章中的摘要，并且只用一千个训练模型就可以生成媲美人类的摘要内容。
利用提取的间隙句进行摘要概括的预训练模型（Pre-training with Extracted Gap-sentences for Abstractive Summarization）。就是设计一种间隙句生成的自监督预训练目标，来改进生成摘要的微调性能。

![](../pegasus.png)

本项目参考开源论坛对于中文版本的实现，以mT5为基础架构和初始权重，通过类似PEGASUS的方式进行预训练。





