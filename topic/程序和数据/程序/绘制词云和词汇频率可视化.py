#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 15:06:18 2017
@author: Ming JIN
"""
import jieba.analyse
from PIL import Image,ImageSequence
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.font_manager import FontProperties  
from wordcloud import WordCloud,ImageColorGenerator
#import matplotlib.mlab as mlab    

font = FontProperties(fname='Songti.ttc')  
bar_width = 0.5
lyric= ''

f=open('result/gun_cut.txt', 'r',encoding='utf-8')#枪击
# f=open('result/abortion_cut.txt', 'r',encoding='utf-8')#堕胎

for i in f:
    lyric+=f.read()

result=jieba.analyse.textrank(lyric,topK=50,withWeight=True)

keywords = dict()
for i in result:    keywords[i[0]]=i[1]
print(keywords.keys())

# image= Image.open('background1.png')
image= Image.open('backgroung2.png')
graph = np.array(image)
image_color = ImageColorGenerator(graph)

wc = WordCloud(font_path='Songti.ttc', scale=3, background_color='black', max_words=55, mask=graph)

wc.generate_from_frequencies(keywords)

plt.imshow(wc)
plt.imshow(wc.recolor(color_func=image_color))
plt.axis("off")
plt.show()
wc.to_file('img_cloud_bar/cloud_gun_cut.png')
# wc.to_file('img_cloud_bar/cloud_abortion_cut.png')

X=[]
Y=[] 
for key in keywords:
    
    X.append(key)
    Y.append(keywords[key])
num = len(X)
   
fig = plt.figure(figsize=(28,10))  
plt.bar(range(num),Y,tick_label = X,width = bar_width)
#plt.xlabel("X-axis",fontproperties=font)  
#plt.ylabel("Y-axis",fontproperties=font)
plt.xticks(rotation = 50,fontproperties=font,fontsize=20)
plt.yticks(fontsize=20)
plt.title("words-frequency chart",fontproperties=font,fontsize=30)  
plt.savefig("img_cloud_bar/barChart_gun_cut.jpg",dpi = 360)
# plt.savefig("barChart_abortion_cut.jpg",dpi = 360)
plt.show()