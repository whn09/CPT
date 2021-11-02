+++
title = " CPT模型训练"
weight = 0510
chapter = true
pre = "<b>5.1</b>"
+++

我们现在会用sagemaker进行一个cpt模型的本地训练（从头训练），使用ML.P3.2xlarge机型。


## 数据准备 

首先下载代码
```
cd SageMaker
git clone https://github.com/jackie930/CPT.git
```

![](../pics/05CPT/3.png)

然后打开文件 `CPT/finetune/generation/train-meta-decription.ipynb`，逐行运行。

首先安装环境

![](../pics/05CPT/4.png)

然后处理数据`meta_description.parquet`，切分train/test/dev， 注意这里的数据您需要手动倒入到相应路径。
注意这里，为了快速产生结果，我们只要用1000条数据训练，200条测试，200条验证。
```
# use csv file to test 
x[:1000].to_csv(os.path.join(path,'train.csv'),index=False,encoding='utf-8')
x[1000:1200].to_csv(os.path.join(path,'test.csv'),index=False,encoding='utf-8')
x[1200:1400].to_csv(os.path.join(path,'dev.csv'),index=False,encoding='utf-8')
```

![](../pics/05CPT/5.png)

## 模型训练

接下来我们运行训练，为了演示目的，我们只运行一个epoch，大约需要10min
```
!python run_gen_v2.py --model_path 'fnlp/cpt-large' --dataset hk01meta --data_dir demo_data --epoch '1' --batch_size '4' 
```

训练完成后，会提示日志信息如下
* train
![](../pics/05CPT/6.png)
* eval
![](../pics/05CPT/7.png)
* predict
![](../pics/05CPT/8.png)

模型结果文件及相应的日志等信息会自动保存在`output/hk01/1`

![](../pics/05CPT/9.png)

## 结果本地测试

我们可以直接用这个产生的模型文件进行本地推理。注意这里的模型文件地址的指定为你刚刚训练产生的。

![](../pics/05CPT/10.png)

到这里，就完成了一个模型的训练过程。