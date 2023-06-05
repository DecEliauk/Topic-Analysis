#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 09:59:46 2018
@author: Ming JIN
"""
#from snownlp import sentiment
#import numpy as np
import pandas as pd
from snownlp import SnowNLP
#from snownlp.sentiment import Sentiment
import matplotlib.pyplot as plt

comment = []
pos_count = 0
neg_count = 0
zl=0
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
# emo = pd.read_csv('枪支评论情感分析.csv')
emo = pd.read_csv('堕胎评论情感分析.csv')

emo = emo.drop(index = emo[emo['正面']=='无法识别'].index.tolist())
emo = emo['立场']

# for line_data in open("../step2_cut_words/data/data_keywords_gun.dat",encoding='utf-8'):
for line_data in emo:
# for line_data in open("abortion_cut.txt",encoding='utf-8'):
    print(line_data)
    if (float(line_data) == 2):
        pos_count += 1

    elif (float(line_data) == 0):
        neg_count += 1
    else :
        zl+=1

labels = 'Positive Side\n(eg. pray,eulogize and suggestion)', 'Negative Side\n(eg. abuse,sarcasm and indignation),' \
                                                              ,'Neutral Side\n(eg. abuse,sarcasm and indignation)'
fracs = [pos_count,neg_count,zl]
explode = [0.1,0,0] # 0.1 凸出这部分，
plt.axes(aspect=1)  # set this , Figure is round, otherwise it is an ellipse
#autopct ，show percet

plt.pie(x=fracs, labels=labels, explode=explode,autopct='%3.1f %%',
        shadow=True, labeldistance=1.1, startangle = 90,pctdistance = 0.6)
plt.title("堕胎话题各立场占比")

# plt.savefig("img_emo/pie_emo_枪支.jpg",dpi = 360)
plt.savefig("img_emo/pie_emo_堕胎.jpg",dpi = 360)

plt.show()
