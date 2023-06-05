#导入所需包
import os
import matplotlib.pyplot as plt
import numpy as np
import xlrd
import pandas as pd
from datetime import datetime
from pandas import Series,DataFrame
import re

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

# data = pd.read_csv('gun_comment.csv')
data = pd.read_csv('枪支评论情感分析.csv')
data_ = pd.read_csv('gun_话题原始数据.csv')
# data = pd.read_csv('abortion_comment.csv')
# data = pd.read_csv('堕胎评论情感分析.csv')
# data_ = pd.read_csv('abortion_话题原始数据.csv')
# print(data.head())
# print(data.shape)
# print(data['评论时间'].head())

# 处理时间格式
a=re.findall('.*?\d+月\d+日','05月28日 11:00')
# print('2022-'+a[0][:2]+'-'+a[0][-3:-1])
# print(len('06月25日 10:42'))#12
# --------------统一评论时间格式-----------
def clentime(x):
    if len(x)>12:
        return x[:10]
    else:
        a = re.findall('.*?\d+月\d+日',x)
        return '2022-'+a[0][:2]+'-'+a[0][-3:-1]

data['评论时间']=data['评论时间'].apply(lambda x:clentime(x))
data.to_csv("gun_comment.csv", index=False, sep=',')
# data.to_csv("abortion_comment.csv", index=False, sep=',')


# 按日期统计评论次数---------------------时序分布
time_commment=[]
count_comment=[]
c_c=0
time_put=[]
count_put=[]
# print('评论时间')
for i in sorted(data['评论时间'].unique()):
    time_commment.append(i)
    count_comment.append(data[data['评论时间']==i].shape[0])
    # print(i,data[data['评论时间']==i].shape[0])

# print('发布时间')
for i in sorted(data_['发布时间'].unique()):
    time_put.append(i)
    count_put.append(data_[data_['发布时间'] == i].shape[0])
    # print(i, data[data_['发布时间'] == i].shape[0])

plt.figure()
plt.subplot(2,1,1)
plt.plot(time_commment,count_comment)
plt.xticks(rotation=30)
plt.title("评论时间")

plt.subplot(2,1,2)
plt.subplots_adjust(left=0.03, bottom=0.08, right=0.98, top=0.95, wspace=None, hspace=0.3)
plt.plot(time_put,count_put)
plt.xticks(rotation=30)
plt.title("发布时间")
plt.savefig("result/话题评论时序分布_gun.jpg", dpi=360)
# plt.savefig("result/话题评论时序分布_abortion.jpg", dpi=360)
plt.show()


#处理原始话题数据获取热点词个数、阅读量、讨论量等数据
f = open(r'gun_keywords.txt',encoding = "utf-8")
keywords = list(f)
keywords = keywords[0].split()

import re
import jieba as jb
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords
def seg_sentence(sentence):
    sentence = re.sub(u'[#a-zA-Z\.]+', u'', str(sentence))#去除英文和数字
    # jb.add_word('data/my_dict_gun.txt')      # 这里是加入自定义的词来补充jieba词典
    # jb.add_word('data/my_dict_abortion.txt')      # 这里是加入自定义的词来补充jieba词典
    sentence_seged = jb.cut(sentence.strip())
    stopwords = stopwordslist('data/Stopword.txt')  # 这里加载停用词的路径
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords and word.__len__() > 1:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr

data1=pd.DataFrame(columns=['话题','话题热点词个数','评论量','阅读量(万)','讨论量'])
topic_read=[]
topic_discuss=[]
topic_com=[]
topic_num=[]
# data1['话题']=data_['话题名称'].unique()#枪支
data1['话题']=data_['话题名称'].unique()[:-1]#堕胎

for i in data1['话题']:
    print(type(data_[data_['话题名称']==i]['话题阅读数'].unique()[0]))
    topic_read.append(float(data_[data_['话题名称']==i]['话题阅读数'].unique()[0].strip('万阅读')))
    topic_discuss.append(float(data_[data_['话题名称'] == i]['话题讨论数'].unique()[0].strip('讨论')))
    topic_com.append(data_[data_['话题名称'] == i]['微博评论量'].sum())
    topNum = seg_sentence(i).split()
    print(topNum)
    c = [x for x in topNum if x in keywords]#找出主题中包含热门词汇
    print("222222",c)
    topic_num.append(len(c)/len(topNum))

data1['话题热点词个数'] = topic_num
data1['评论量'] = topic_com
data1['阅读量(万)'] = topic_read
data1['讨论量'] = topic_discuss
# print(data1)
data1.to_csv("gun_话题热点词阅读量等.csv")
# data1.to_csv("abortion_话题热点词阅读量等.csv")

