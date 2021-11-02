+++
title = " CPT模型部署"
weight = 0530
chapter = true
pre = "<b>5.3</b>"
+++

然后部署一个预置的endpoint

```shell script
endpoint_ecr_image="847380964353.dkr.ecr.us-east-2.amazonaws.com/cpt"

python create_endpoint.py \
--endpoint_ecr_image_path ${endpoint_ecr_image} \
--endpoint_name 'cpt' \
--instance_type "ml.p3.xlarge"
```

在部署结束后，看到SageMaker控制台生成了对应的endpoint,可以使用如下客户端代码测试调用

```python
%%time 

from boto3.session import Session
import json
data={"data": "台觀光局指出，先前已宣布2月1日至29日暫停旅行業組團前往中國大陸地區旅遊（含轉機前往其他地區旅遊）。為配合台疾病管制署提升港澳地區旅遊疫情等級為第二級，故2月6日起暫停台灣旅行社組團到港澳旅遊，但不含中轉港澳轉機到其他地區。台觀光局表示，持續配合台疾管署相關防疫作為，並視台疫情指揮中心發佈的疫情訊息綜合評估，隨時調整相關管制事宜。一、台籍人士：2月6日起，有陸港澳旅遊史者，需居家檢疫14天；申請獲准至港澳入境者，需自主健康管理14天。二、大陸人士：暫緩入境。三、港澳人士：2月7日起，入境後需居家檢疫14天。四、外籍人士：2月7日起，14天內曾經入境或居住於中國大陸、香港、澳門的外籍人士，暫緩入境。"}
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

结果如下
```
{'result': '[SEP] [CLS] 因 應 新 型 冠 狀 病 毒 肺 炎 （ 俗 稱 「 武 漢 肺 炎 」 ） 疫 情 ， 台 灣 觀 光 局 今 天 （ 7 日 ） 宣 布 ， 暫 停 台 灣 旅 行 社 組 團 到 港 澳 旅 遊 ， 但 不 含 中 轉 港 澳 轉 機 [SEP]', 'infer_time': '0:00:02.948025'}
CPU times: user 169 ms, sys: 30.9 ms, total: 200 ms
Wall time: 3.42 s

```

