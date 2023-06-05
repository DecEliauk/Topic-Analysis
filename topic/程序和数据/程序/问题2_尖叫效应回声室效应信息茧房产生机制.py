import datetime
import re

import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

data = pd.read_csv("枪支话题评论原始数据.csv")
# data = pd.read_csv("堕胎话题评论原始数据.csv")
'''
子问题2：尖叫效应、回声室效应和信息茧房的形成机制
'''
# --------------统一评论时间格式-----------
def clentime(x):
    if len(x)>12:
        return x[:16]
    else:
        a = re.findall('.*?\d+月\d+日+\s+\d\d\S\d\d',x)
        # print('2022-'+a[0][:2]+'-'+a[0][3:5]+a[0][-6:])
        return '2022-'+a[0][:2]+'-'+a[0][3:5]+a[0][-6:]

data['评论时间']=data['评论时间'].apply(lambda x:clentime(x))
# datetime.datetime.strptime()
# --随时间增长评论数量变化情况
data = data.groupby(data['评论时间'].map(lambda x: x[0:13]))['评论时间'].count()
# print(data)
x = data.index
y=data.values
y1 = []

plt.plot(x[0:],y)
plt.xticks(x[:-1:10])
plt.xticks(rotation=30)
plt.title('枪支管控评论数量增长变化(/时)',fontdict={'weight': 'normal', 'size': 20})
plt.xlabel('时间', fontdict={'weight': 'normal', 'size': 17})  # 改变坐标轴标题字体
plt.ylabel('评论增长数量/时',fontdict={'weight': 'normal', 'size': 17})
plt.show()

# --单位时间内各立场变化情况
data1 = pd.read_csv('枪支评论情感分析.csv')
data1 = pd.read_csv('堕胎评论情感分析.csv')
data1['评论时间'] = data['评论时间']
data1 = data1.drop(index = data1[data1['立场']=='无法识别'].index.tolist())
data1['评论时间']=data1['评论时间'].apply(lambda x:clentime(x))
# datetime.datetime.strptime()
# data1 = data1.groupby(data1['评论时间'].map(lambda x: x[0:13]),data1['pi']).count()
data1['立场'] = pd.to_numeric(data1['立场'],errors='coerce')
data1 = data1.groupby(['立场','评论时间'])['立场'].count()
# print(a)

y1=[]
sen=['反对','中立','支持']
for id in range(3):
    c = data1[id]
    # print(c)
    c = c.groupby(c.index.map(lambda x: x[0:13])).count()
    # print(c)
    x=c.index
    y=c.values

    # for i in range(1,len(x)):
    #     y1.append((y[i] - y[i - 1]) / (int(x[i][11:13]) - int(x[i - 1][11:13])))
    plt.bar(x,y)
    plt.xticks(x[:-1:10])
    plt.xticks(rotation=30)
    plt.title('单位时间内枪支管控'+sen[id]+'评论立场变化',fontdict={'weight': 'normal', 'size': 20})
    plt.xlabel('时间', fontdict={'weight': 'normal', 'size': 17})  # 改变坐标轴标题字体
    plt.ylabel(sen[id]+'评论数量',fontdict={'weight': 'normal', 'size': 17})
    plt.show()

