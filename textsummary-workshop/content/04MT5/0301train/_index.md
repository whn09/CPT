+++
title = "MT5模型实验"
weight = 0410
chapter = true
pre = "<b>4.1</b>"
+++

然后打开`/home/ec2-user/SageMaker/notebooks/sagemaker/08_distributed_summarization_bart_t5/train-huggingface.ipynb`运行

训练开启后，可以看到产生了对应的训练日志

![](./1.png)

及对应的训练任务


![](./2.png)

大约25min完成训练，结束后可以直接部署模型文件为endpoint并进行推理。注意这里只用了1000条数据训练1轮，所以模型效果不佳。

![](./3.png)



