+++
title = " bert-seq2seq模型实验"
weight = 0310
chapter = true
pre = "<b>3.1</b>"
+++

首先下载代码
```
cd SageMaker
git clone https://github.com/jackie930/bert-seq2seq-textsummary.git
```

然后部署一个预置的endpoint

```shell script
#sin
endpoint_ecr_image="847380964353.dkr.ecr.ap-southeast-1.amazonaws.com/bertseq2seq"
#ningxia
#endpoint_ecr_image="251885400447.dkr.ecr.cn-northwest-1.amazonaws.com.cn/bertseq2seq"
python create_endpoint.py \
--endpoint_ecr_image_path ${endpoint_ecr_image} \
--endpoint_name 'bertseq2seq' \
--instance_type "ml.p2.xlarge"
```

在部署结束后，看到SageMaker控制台生成了对应的endpoint,可以使用如下客户端代码测试调用
```python
from boto3.session import Session
import json
txt = "嘉实基金推出旗下第3只成长基金——嘉实领先成长股票型基金，目前该基金已获得证监会批复，将于近期正式发行。据悉，嘉实领先成长基金股票资产占基金资产的60%～95%，其中不低于80%的比例投资于领先成长企业。嘉实领先成长基金具有鲜明的“全市场成长风格”，其重点投资于中国经济中快速成长行业中的领先成长企业，力争获得双重超额收益。嘉实基金认为，伴随中国经济的深入调整，未来成长行业也将呈现鱼目混杂现象。需要通过在全市场范围中精选快速成长行业中成长战略清晰的领先成长企业，才有望获取丰厚的投资收益。据悉，嘉实领先成长基金将由嘉实策略增长的基金经理之一邵秋涛执掌"
data={"data": txt}
session = Session()
    
runtime = session.client("runtime.sagemaker")
response = runtime.invoke_endpoint(
    EndpointName='bertseq2seq',
    ContentType="application/json",
    Body=json.dumps(data),
)

result = json.loads(response["Body"].read())
print (result)
```

结果如下
```
{'摘要': '嘉 实 领 先 成 长 基 金 获 证 监 会 批 复'}
CPU times: user 72.6 ms, sys: 20.7 ms, total: 93.3 ms
Wall time: 807 ms
```

训练部分可以参考github中readme部分。