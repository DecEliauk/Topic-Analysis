#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 14:53:28 2017

@author: Ming JIN
"""
#import re
import importlib
#import string
import sys
#import os
import time
#import urllib3
#from bs4 import BeautifulSoup
from datetime import datetime

import requests
from lxml import etree
import pymysql
importlib.reload(sys)
from selenium.webdriver.common.by import By
from selenium import webdriver

cookie = {'Cookie' : '_T_WM=58aad7dff13d67b74d8ef8c7186cb121; '
                   'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFn25lUWkT0ZAddRQxOcpcF5NHD95QNS0Mf1hzRSoqfWs4DqcjzxsHoS0z0S0-t; '
                   'H5_wentry=H5; backURL=https%3A%2F%2Fweibo.cn%2Fcomment%2FLv4v5jBkf%3Fuid%3D1887344341%26rl%3D1%26page%3D1; '
                   'SUB=_2A25P2z7pDeRhGeFJ7FcZ8ibKzTmIHXVtJEKhrDV6PUJbktANLXfZkW1NfzZZqY905tJQ5gq_mp-TGDqYp_RfoEy1',}

def get_url(index):
    print("连接Mysql数据库读入数据...")

    db1 = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='123456',
                          db='URL_database',charset='utf8mb4',cursorclass = pymysql.cursors.DictCursor)
 
    cursor1 = db1.cursor()
    
    #str_index = 'id' + str(index)
    str_index = str(index)
    
    sql_1 = "select url from weibo_full_url_gun where weibo_id ="+ "'" + str_index + "'" ""#枪支
    # sql_1 = "select url from weibo_full_url_abortion where weibo_id ="+ "'" + str_index + "'" ""#堕胎

    cursor1.execute(sql_1)
    result1 = cursor1.fetchall()
    result = result1[0]['url']
    db1.close()
    return result


def create_table(index):
    
    db3 = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='123456',#枪支
                          db='url',charset='utf8mb4',cursorclass = pymysql.cursors.DictCursor)
                          # db='url',charset='utf8',cursorclass = pymysql.cursors.DictCursor)
    # db3 = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456',#堕胎
    #                       db='url2', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor3 = db3.cursor()
    sql_4 = "DROP TABLE IF EXISTS ID" + str(index)
    cursor3.execute(sql_4)
    
    sql_3 = "CREATE TABLE ID" + str(index) + \
            "(comment_num int NOT NULL AUTO_INCREMENT,user_id  VARCHAR(40),user_level VARCHAR(40)," \
            "comment VARCHAR(600),comment_date VARCHAR(40),PRIMARY KEY (comment_num)) default charset = utf8mb4 "
    # comment_date TIMESTAMP,
    cursor3.execute(sql_3)
    db3.close()

def write_in_database(text1,text2,text3,text4,ctime,index):
    
    db2 = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='123456',#枪支
                          db='url',charset='utf8mb4',cursorclass = pymysql.cursors.DictCursor)
                          # db='url',charset='utf8',cursorclass = pymysql.cursors.DictCursor)
    # db2 = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456',#堕胎
    #                       db='url2', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor2 = db2.cursor()
    sql_2 = "INSERT INTO ID" + str(index) + " (user_id,user_level,comment,comment_date)" +" VALUES(%s,%s,%s,%s)"
    cursor2.execute(sql_2,(text2,text3,text4,ctime))
    db2.commit()
    db2.close()

def get_url_data(base_url,pageNum,word_count,index):
        
    print("爬虫准备就绪...")
    
    base_url_deal = base_url + '%d'
    base_url_final = str(base_url_deal)
    for page in range(1,pageNum+1):

        print("获取第",page,"页评论……")
        url = base_url_final%(page)
        lxml = requests.get(url, cookies = cookie).content
        selector = etree.HTML(lxml)
        weiboitems = selector.xpath('//div[@class="c"][@id]')

        time.sleep(8)  
        
        for item in weiboitems:

            weibo_id = item.xpath('./@id')[0]
            ctt = item.xpath('./span[@class="ctt"]/text()')
            level = item.xpath('./img_cloud_bar/@alt')
            tim = item.xpath('./span[@class="ct"]/text()')
            tim,tim2,tim3 = str(tim).partition(r'\xa0')#
            tim =tim.lstrip("['")

            text1 = str(word_count)
            text2 = str(weibo_id)
            text4 = str(ctt)
            text3 = str(level)

            write_in_database(text1,text2,text3,text4,tim,index)
            word_count += 1
        print("爬取成功！")
    print("本事件微博信息入库完毕，共%d条" % (word_count - 4))

if __name__ == '__main__':
    
    for index in range(1,16):
        
        create_table(index)
        word_count = 1
        base_url = get_url(index)
        first_url = base_url + '1'
        print(first_url)

        html = requests.get(first_url,cookies=cookie).content
        selector = etree.HTML(html)
        controls = selector.xpath('//input[@name="mp"]')

        if controls:
            pageNum = int(controls[0].attrib['value'])
            print("评论共%d页"%pageNum)
        else:
            pageNum = 1
        get_url_data(base_url,pageNum,word_count,index)
        index += 1
        print("进行下一条微博爬取...")
    print("全部完成！")
