import csv
import re

from aip import AipNlp
import pandas as pd
import numpy as np
import time


# 此处输入baiduAIid
from snownlp import SnowNLP

APP_ID = '26928533'
API_KEY = 'EpYNOqoVcgIVNPWYP7VCgPj8'
SECRET_KEY = 'EsmGVOM2c9zBIYyHmYkDORfokU1UXKfQ'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

positive_prob=[]
negative_prob=[]
confidence=[]
# sentiment：0代表是负面情绪；1代表是中和；2代表是正面情绪。
sentiment=[]

def isPostive(text):
    items = []
    print(client.sentimentClassify(text))
    # print(type(client.sentimentClassify(text)['items'][0]))
    try:
        for key,values in client.sentimentClassify(text)['items'][0].items():
            items.append([key,values])
        print(items)
        positive_prob.append(items[0][1])
        negative_prob.append(items[2][1])
        confidence.append(items[1][1])
        sentiment.append(items[3][1])
        if items[0][1] > 0.5:
            return "积极",
        else:
            return "消极"
    except:
        print("")
        positive_prob.append("无法识别")
        negative_prob.append("无法识别")
        confidence.append("无法识别")
        sentiment.append("无法识别")
        return "无法识别"
    print(positive_prob)

# 读取文件，注意修改文件路径
# file_path = 'gun_comment.csv'
file_path = 'abortion_comment.csv'
data = pd.read_csv(file_path)

moods = []
count = 1
for i in data['评论内容']:
    i= re.findall('[\u4e00-\u9fa5a-zA-Z]',i)
    moods.append(isPostive(i))
    count+=1
    print("目前分析到：",count)
    time.sleep(3)

data['正面']=positive_prob
data['负面']=negative_prob
data['置信度']=confidence
data['立场']=sentiment
data['情感倾向'] = pd.Series(moods)

# 此处为覆盖保存
# data.to_csv("枪支评论情感分析.csv")
data.to_csv("堕胎评论情感分析.csv")
print("分析完成，已保存")


