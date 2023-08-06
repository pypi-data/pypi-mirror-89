# AutoPhraseX

![Python package](https://github.com/luozhouyang/autophrasex/workflows/Python%20package/badge.svg)
[![PyPI version](https://badge.fury.io/py/autophrasex.svg)](https://badge.fury.io/py/autophrasex)
[![Python](https://img.shields.io/pypi/pyversions/autophrasex.svg?style=plastic)](https://badge.fury.io/py/autophrasex)


Automated Phrase Mining from Massive Text Corpora in Python.

实现思路参考 [shangjingbo1226/AutoPhrase](https://github.com/shangjingbo1226/AutoPhrase)，并不完全一致。

## 安装

```bash
pip install -U autophrasex
```

## 使用

```python
from autophrasex import AutoPhrase, BaiduLacTokenizer, Strategy

tokenizer = BaiduLacTokenizer()
strategy = Strategy(
    tokenizer=tokenizer,
    N=4,
    threshold=0.45,
    threshold_schedule_factor=1.0)

autophrase = AutoPhrase()
predictions = autophrase.mine(
    input_doc_files=['/path/to/doc/files'],
    quality_phrase_files=['/path/to/quality/phrase'],
    strategy=strategy,
    N=4,
    epochs=10)

for pred in predictions:
    print(pred)
```

## 结果示例

新闻语料上的抽取结果示例：

```bash
成品油价格, 0.992766816097071
股份制银行, 0.992766816097071
公务船, 0.992766816097071
中国留学生, 0.992766816097071
贷款基准, 0.992766816097071
欧足联, 0.992766816097071
新局面, 0.992766816097071
淘汰赛, 0.992766816097071
反动派, 0.992766816097071
生命危险, 0.992766816097071
新台阶, 0.992766816097071
知名度, 0.992766816097071
新兴产业, 0.9925660976153782
安全感, 0.9925660976153782
战斗力, 0.9925660976153782
战略性, 0.9925660976153782
私家车, 0.9925660976153782
环球网, 0.9925660976153782
副校长, 0.9925660976153782
流行语, 0.9925660976153782
债务危机, 0.9925660976153782
保险资产, 0.9920376397372204
保险机构, 0.9920376397372204
豪华车, 0.9920376397372204
环境质量, 0.9920376397372204
瑞典队, 0.9919345469537152
交强险, 0.9919345469537152
马卡报, 0.9919345469537152
生产力, 0.9911077251879798
```

医疗对话语料的抽取示例：

```bash
左眉弓, 1.0
支原体, 1.0
mri, 1.0
颈动脉, 0.9854149008885851
结核病, 0.9670815675552518
手术室, 0.9617546444783288
平扫示, 0.9570324222561065
左手拇指, 0.94
双膝关节, 0.94
右手中指, 0.94
拇指末节, 0.94
cm皮肤, 0.94
肝胆脾, 0.94
抗体阳性, 0.94
igm抗体阳性, 0.94
左侧面颊, 0.94
膀胱结石, 0.94
左侧基底节, 0.94
腰椎正侧, 0.94
软组织肿胀, 0.94
手术瘢痕, 0.94
枕顶部, 0.94
左膝关节正侧, 0.94
膝关节正侧位, 0.94
腰椎椎体, 0.94
承德市医院, 0.94
性脑梗塞, 0.94
颈椎dr, 0.94
泌尿系超声, 0.94
双侧阴囊, 0.94
右颞部, 0.94
肺炎支原体, 0.94
```