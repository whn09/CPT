# CPT

This repository contains code and checkpoints for **CPT**.

[**CPT: A Pre-Trained Unbalanced Transformer for Both Chinese Language Understanding and Generation**](https://arxiv.org/pdf/2109.05729.pdf)

Yunfan Shao, Zhichao Geng, Yitao Liu, Junqi Dai, Fei Yang, Li Zhe, Hujun Bao, Xipeng Qiu

## Introduction

Aiming to unify both NLU and NLG tasks, We propose a novel **C**hinese **P**re-trained Un-balanced **T**ransformer (**CPT**), which is an unbalanced Transformer encoder-decoder pre-trained with MLM and DAE jointly.

<p align="center">
	<br>
 	<img src="./misc\cpt-architecture-v1.png" width = "700" align=center />
	<br>
</p>

The architecture of CPT is a variant of the full Transformer and consists of three parts:

1. **Shared Encoder** (S-Enc): a Transformer encoder with fully-connected self-attention, which is designed to capture the common semantic representation for both language understanding and generation.
2. **Understanding Decoder** (U-Dec): a shallow Transformer encoder with fully-connected self-attention, which is designed for NLU tasks. The input of U-Dec is the output of S-Enc.
3. **Generation Decoder** (G-Dec): a Transformer decoder with masked self-attention, which is designed for generation tasks with auto-regressive fashion. G-Dec utilizes the output of S-Enc with cross-attention.

## Pre-Trained Models
We provide the pre-trained weights of CPT and Chinese BART with source code, which can be directly used in Huggingface-Transformers.

- **`Chinese BART-base`**: 6 layers Encoder, 6 layers Decoder, 12 Heads and 768 Model dim.
- **`Chinese BART-large`**: 12 layers Encoder, 12 layers Decoder, 16 Heads and 1024 Model dim.
- **`CPT-base`**: 10 layers S-Enc, 2 layers U-Dec/G-Dec, 12 Heads and 768 Model dim.
- **`CPT-large`**: 20 layers S-Enc, 4 layers U-Dec/G-Dec, 16 Heads and 1024 Model dim.

The pre-trained weights can be downloaded here.
| Model | `MODEL_NAME`|
| --- | --- |
| **`Chinese BART-base`**  | [fnlp/bart-base-chinese](https://huggingface.co/fnlp/bart-base-chinese) | 
| **`Chinese BART-large`**   | [fnlp/bart-large-chinese](https://huggingface.co/fnlp/bart-large-chinese) |
| **`CPT-base`**   | [fnlp/cpt-base](https://huggingface.co/fnlp/cpt-base) | 
| **`CPT-large`**   | [fnlp/cpt-large](https://huggingface.co/fnlp/cpt-large) |

### Requirements:
- pytorch==1.8.1
- transformers==4.4.1

To use CPT, please import the file `finetune/modeling_cpt.py` that define the architecture of CPT into your project.
Then, use the PTMs as the following example, where `MODEL_NAME` is the corresponding  string that refers to the model.

For CPT:
```python
from modeling_cpt import BertTokenizer, CPTForConditionalGeneration
tokenizer = BertTokenizer.from_pretrained("MODEL_NAME")
model = CPTForConditionalGeneration.from_pretrained("MODEL_NAME")
print(model)
```

For Chinese BART:
```python
from transformers import BertTokenizer, BartForConditionalGeneration
tokenizer = BertTokenizer.from_pretrained("MODEL_NAME")
model = BartForConditionalGeneration.from_pretrained("MODEL_NAME")
print(model)
```

## Pre-Training
Pre-training code and examples can be find [Here](pretrain/README.md).


## Fine-Tuning
Fine-tuning code and examples can be find [Here](finetune/README.md).

## Deploy 
## deploy on AWS SageMaker Endpoint

run locally
~~~
#make sure you got trained models in 6 folder
cd endpoint
sh build_and_push.sh
docker run -v -d -p 8080:8080 cpt
~~~

```python
# test 
#curl http://localhost:8080/ping 

# curl
import requests
import json

url='http://localhost:8080/invocations'
data={"data": "《半導體》Q1展望保守，世界垂淚2019/02/11 10:28時報資訊【時報記者沈培華台北報導】世界先進 (5347) 去年營運創歷史新高，每股純益達3.72元。但對今年首季展望保守，預計營收將比上季高點減近一成。世界先進於封關前股價拉高，今早則是開平走低。世界先進於年前台股封關後舉行法說會公布財報。公司去年營運表現亮麗，營收與獲利同創歷史新高紀錄。2018年全年營收289.28億元，年增16.1%，毛利率35.2%，拉升3.2個百分點，稅後淨利61.66億元，年增36.9%，營收與獲利同創歷史新高，每股純益3.72元。董事會通過去年度擬配發現金股利3.2元。展望第一季，受到客戶進入庫存調整，公司預期，本季營收估在67億至71億元，將季減8%至13%，毛利率將約34.5%至36.5%。此外，因應客戶需求，世界先進決定斥資2.36億美元，收購格芯新加坡8吋晶圓廠。世界先進於年前宣布，將購買格芯位於新加坡Tampines的8吋晶圓3E廠房、廠務設施、機器設備及微機電(MEMS)智財權與業務，交易總金額2.36億美元，交割日訂108年12月31日。格芯晶圓3E廠現有月產能3.5萬片8吋晶圓，世界先進每年將可增加超過40萬片8吋晶圓產能，增進公司明年起業績成長動能。TOP關閉"}
data = json.dumps(data)
r = requests.post(url,data=data)

#show result
print (r.text)
```

结果如下
```json
{"摘要": "2011 年 f1 周 年 展 望 保 守 保 守 世 界 第 一 (图 )"}
```

run on endpoint

```shell script
endpoint_ecr_image="847380964353.dkr.ecr.us-east-2.amazonaws.com/cpt"
python create_endpoint.py \
--endpoint_ecr_image_path ${endpoint_ecr_image} \
--endpoint_name 'cpt' \
--instance_type "ml.g4dn.xlarge"
```

在部署结束后，看到SageMaker控制台生成了对应的endpoint,可以使用如下客户端代码测试调用
```python
from boto3.session import Session
import json
data={"data": "《半導體》Q1展望保守，世界垂淚2019/02/11 10:28時報資訊【時報記者沈培華台北報導】世界先進 (5347) 去年營運創歷史新高，每股純益達3.72元。但對今年首季展望保守，預計營收將比上季高點減近一成。世界先進於封關前股價拉高，今早則是開平走低。世界先進於年前台股封關後舉行法說會公布財報。公司去年營運表現亮麗，營收與獲利同創歷史新高紀錄。2018年全年營收289.28億元，年增16.1%，毛利率35.2%，拉升3.2個百分點，稅後淨利61.66億元，年增36.9%，營收與獲利同創歷史新高，每股純益3.72元。董事會通過去年度擬配發現金股利3.2元。展望第一季，受到客戶進入庫存調整，公司預期，本季營收估在67億至71億元，將季減8%至13%，毛利率將約34.5%至36.5%。此外，因應客戶需求，世界先進決定斥資2.36億美元，收購格芯新加坡8吋晶圓廠。世界先進於年前宣布，將購買格芯位於新加坡Tampines的8吋晶圓3E廠房、廠務設施、機器設備及微機電(MEMS)智財權與業務，交易總金額2.36億美元，交割日訂108年12月31日。格芯晶圓3E廠現有月產能3.5萬片8吋晶圓，世界先進每年將可增加超過40萬片8吋晶圓產能，增進公司明年起業績成長動能。TOP關閉"}

session = Session()
    
runtime = session.client("runtime.sagemaker")
response = runtime.invoke_endpoint(
    EndpointName='cpt',
    ContentType="application/json",
    Body=json.dumps(data),
)

result = json.loads(response["Body"].read())
print (result)
```





## Citation

```bibtex
@article{shao2021cpt,
  title={CPT: A Pre-Trained Unbalanced Transformer for Both Chinese Language Understanding and Generation}, 
  author={Yunfan Shao and Zhichao Geng and Yitao Liu and Junqi Dai and Fei Yang and Li Zhe and Hujun Bao and Xipeng Qiu},
  journal={arXiv preprint arXiv:2109.05729},
  year={2021}
}
```

