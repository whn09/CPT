+++
title = " texkrank模型实验"
weight = 0210
chapter = true
pre = "<b>2.1</b>"
+++


TextRank算法可以用来从文本中提取关键词和摘要（重要的句子）。TextRank4ZH是针对中文文本的TextRank算法的python算法实现。


## 原理

TextRank的详细原理请参考：

> Mihalcea R, Tarau P. TextRank: Bringing order into texts[C]. Association for Computational Linguistics, 2004.

### 关键词提取
将原文本拆分为句子，在每个句子中过滤掉停用词（可选），并只保留指定词性的单词（可选）。由此可以得到句子的集合和单词的集合。

每个单词作为pagerank中的一个节点。设定窗口大小为k，假设一个句子依次由下面的单词组成：
```
w1, w2, w3, w4, w5, ..., wn
```
`w1, w2, ..., wk`、`w2, w3, ...,wk+1`、`w3, w4, ...,wk+2`等都是一个窗口。在一个窗口中的任两个单词对应的节点之间存在一个无向无权的边。

基于上面构成图，可以计算出每个单词节点的重要性。最重要的若干单词可以作为关键词。


### 关键短语提取
参照[关键词提取](#关键词提取)提取出若干关键词。若原文本中存在若干个关键词相邻的情况，那么这些关键词可以构成一个关键词组。

例如，在一篇介绍`支持向量机`的文章中，可以找到关键词`支持`、`向量`、`机`，通过关键词组提取，可以得到`支持向量机`。

### 摘要生成
将每个句子看成图中的一个节点，若两个句子之间有相似性，认为对应的两个节点之间有一个无向有权边，权值是相似度。

通过pagerank算法计算得到的重要性最高的若干句子可以当作摘要。

## 使用说明

类TextRank4Keyword、TextRank4Sentence在处理一段文本时会将文本拆分成4种格式：

* sentences：由句子组成的列表。
* words_no_filter：对sentences中每个句子分词而得到的两级列表。
* words_no_stop_words：去掉words_no_filter中的停止词而得到的二维列表。
* words_all_filters：保留words_no_stop_words中指定词性的单词而得到的二维列表。


# 部署

 
```shell script

git clone https://github.com/jackie930/TextRank4ZH.git
cd TextRank4ZH/apps/text_summary_endpoint
#注意这里您可以部署自己的ecr image，也可以我们打包好的公共镜像，本次实验会跳过build image步骤
##sh build_and_push.sh
```

## Deploy endpoint on SageMaker 
```shell script
endpoint_ecr_image="847380964353.dkr.ecr.us-west-2.amazonaws.com/textrank"
python create_endpoint.py \
--endpoint_ecr_image_path ${endpoint_ecr_image} \
--endpoint_name 'textrank' \
--instance_type "ml.t2.medium"
```

在部署结束后，看到SageMaker控制台生成了对应的endpoint,可以使用如下客户端代码测试调用
```python
from boto3.session import Session
import json
data={"data": "台觀光局指出，先前已宣布2月1日至29日暫停旅行業組團前往中國大陸地區旅遊（含轉機前往其他地區旅遊）。為配合台疾病管制署提升港澳地區旅遊疫情等級為第二級，故2月6日起暫停台灣旅行社組團到港澳旅遊，但不含中轉港澳轉機到其他地區。台觀光局表示，持續配合台疾管署相關防疫作為，並視台疫情指揮中心發佈的疫情訊息綜合評估，隨時調整相關管制事宜。一、台籍人士：2月6日起，有陸港澳旅遊史者，需居家檢疫14天；申請獲准至港澳入境者，需自主健康管理14天。二、大陸人士：暫緩入境。三、港澳人士：2月7日起，入境後需居家檢疫14天。四、外籍人士：2月7日起，14天內曾經入境或居住於中國大陸、香港、澳門的外籍人士，暫緩入境。"}

session = Session()
    
runtime = session.client("runtime.sagemaker")
response = runtime.invoke_endpoint(
    EndpointName='textrank',
    ContentType="application/json",
    Body=json.dumps(data),
)

result = json.loads(response["Body"].read())
print (result)
```

结果如下
```
{'res': {'关键词列表': ['港澳', '需', '相關', '旅遊', '疫情', '地區', '管制', '光局', '大陸', '前往', '人士', '中國', '指出', '防疫', '中心', '綜合', '澳門', '表示', '持續', '配合'], '关键词权重': [0.06302083682777858, 0.03511030924850785, 0.033600141119327076, 0.030806166940925472, 0.029497862526199358, 0.02936235978105701, 0.027110814695381964, 0.02686551218821217, 0.02544770381895585, 0.025013920666751004, 0.02041656139425058, 0.019492944695266273, 0.01932912128465998, 0.01859340436433212, 0.018527042504337878, 0.018527042504337878, 0.017728167413452, 0.0175136542808295, 0.017279197108065837, 0.017116490039388914], '摘要列表': ['三、港澳人士：2月7日起，入境後需居家檢疫14天', '一、台籍人士：2月6日起，有陸港澳旅遊史者，需居家檢疫14天', '台觀光局指出，先前已宣布2月1日至29日暫停旅行業組團前往中國大陸地區旅遊（含轉機前往其他地區旅遊）'], '摘要位置index': [6, 3, 0], '摘要权重': [0.15060516235453508, 0.1490769827264645, 0.12750225410692212]}}
CPU times: user 166 ms, sys: 15.5 ms, total: 181 ms
Wall time: 4.53 s
```

