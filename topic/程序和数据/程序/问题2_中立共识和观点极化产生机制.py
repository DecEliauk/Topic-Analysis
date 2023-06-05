
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import linear_model

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

# data = pd.read_csv("枪支评论情感分析.csv")
data = pd.read_csv("堕胎评论情感分析.csv")

data = data.drop(index = data[data['立场']=='无法识别'].index.tolist())
data['立场'] = pd.to_numeric(data['立场'],errors='coerce')
data1 = data.groupby(['立场','评论时间'])['立场'].count()
data2 = data.groupby(['评论时间'])['立场'].count()

a=[[] for i in range(3)]
b = [[] for i in range(3)]

for id in range(3):
    for i, j in data1[id].items():
        if i in data2.index:#不同评论站总评论的比例
            a[id].append(data1[id][i] / data2[i])

sen=['反对','中立','支持']

for i in range(3):
    x = data1[i].index
    # x =[datetime.datetime.strptime(j,'%Y-%m-%d') for j in data1[i].index]
    y = a[i]
    plt.figure(figsize=(15, 7))
    plt.plot(x, y,marker='.')

    # plt.axhline(1,c="r", ls="--", lw=2)
    plt.xticks(rotation=30)
    plt.title('堕胎评论观点'+sen[i]+'立场随时间的变化', fontdict={'weight': 'normal', 'size': 20})
    plt.xlabel('时间', fontdict={'weight': 'normal', 'size': 17})  # 改变坐标轴标题字体
    plt.ylabel(sen[i]+'立场占比变化', fontdict={'weight': 'normal', 'size': 17})
    plt.savefig('abor_评论观点随时间的变化立场'+str(i)+'.jpg')

    plt.show()


