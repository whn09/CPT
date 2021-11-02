+++
title = " CPT模型增强训练"
weight = 0520
chapter = true
pre = "<b>5.2</b>"
+++

在完成本地训练后，接下来我们模拟一个增强训练过程。在我们刚才完成的训练任务中，产生了模型文件`output/hk01meta/1`目录下，然后，我们运行

```
!python run_gen_v2.py --model_path 'output/hk01meta/1' --dataset hk01meta --data_dir demo_data --epoch '1' --batch_size '4' 
```

我们可以看到，在训练时，日志中有如下的记录`loading weights file output/hk01meta/2/pytorch_model.bin`说明模型是导入了一个之前训练的基础版本，也可以通过训练的loss值判断出这个结果是增强训练产生的。

同样的，我们可以利用本地推理进行测试。

