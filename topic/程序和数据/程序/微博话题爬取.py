import time
import xlrd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import excelSave as save

# 用来控制页面滚动
def Transfer_Clicks(browser):
    time.sleep(5)
    try:
        browser.execute_script("window.scrollBy(0,document.body.scrollHeight)", "")
    except:
        pass
    return "Transfer successfully \n"

#判断页面是否加载出来
def isPresent():
    temp =1
    try: 
        driver.find_elements(By.CSS_SELECTOR,'div.line-around.layout-box.mod-pagination > a:nth-child(2) > div > select > option')
    except:
        temp =0
    return temp
#把超话页面滚动到底
def SuperwordRollToTheEnd():
    before = 0
    after = 0
    n = 0
    timeToSleep = 50
    while True:
        before = after
        Transfer_Clicks(driver)
        time.sleep(3)
        elems = driver.find_elements(By.CSS_SELECTOR,'div.m-box')
        print("当前包含超话最大数量:%d,n当前的值为:%d,当n为5无法解析出新的超话" % (len(elems),n))
        after = len(elems)
        if after > before:
            n = 0
        if after == before:
            n = n + 1
        if n == 5:
            print("当前包含最大超话数为：%d" % after)
            break
        if after > timeToSleep:
            print("抓取到%d多条超话，休眠5秒" % timeToSleep)
            timeToSleep = timeToSleep + 50
            time.sleep(5)
#插入数据
def insert_data(elems,path,name,yuedu,taolun):
    for elem in elems:
        workbook = xlrd.open_workbook(path)  # 打开工作簿
        sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
        worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
        rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数       
        rid = rows_old
        #用户名
        weibo_username = elem.find_elements(By.CSS_SELECTOR,'h3.m-text-cut')[0].text
        weibo_userlevel = "普通用户"
        #微博等级
        try: 
            weibo_userlevel_color_class = elem.find_elements(By.CSS_SELECTOR,"i.m-icon")[0].get_attribute("class").replace("m-icon ","")
            if weibo_userlevel_color_class == "m-icon-yellowv":
                weibo_userlevel = "黄v"
            if weibo_userlevel_color_class == "m-icon-bluev":
                weibo_userlevel = "蓝v"
            if weibo_userlevel_color_class == "m-icon-goldv-static":
                weibo_userlevel = "金v"
            if weibo_userlevel_color_class == "m-icon-club":
                weibo_userlevel = "微博达人"     
        except:
            weibo_userlevel = "普通用户"
        #微博内容
        weibo_content = elem.find_elements(By.CSS_SELECTOR,'div.weibo-text')[0].text
        shares = elem.find_elements(By.CSS_SELECTOR,'i.m-font.m-font-forward + h4')[0].text
        comments = elem.find_elements(By.CSS_SELECTOR,'i.m-font.m-font-comment + h4')[0].text
        likes = elem.find_elements(By.CSS_SELECTOR,'i.m-icon.m-icon-like + h4')[0].text

        #发布时间
        weibo_time = elem.find_elements(By.CSS_SELECTOR,'span.time')[0].text
        '''
        print("用户名："+ weibo_username + "|"
              "微博等级："+ weibo_userlevel + "|"
              "微博内容："+ weibo_content + "|"
              "转发："+ shares + "|"
              "评论数："+ comments + "|"
              "点赞数："+ likes + "|"
              "发布时间："+ weibo_time + "|"
              "话题名称" + name + "|" 
              "话题讨论数" + yuedu + "|"
              "话题阅读数" + taolun)
        '''
        value1 = [[rid, weibo_username, weibo_userlevel,weibo_content, shares,comments,likes,weibo_time,keyword,name,yuedu,taolun],]
        print("当前插入第%d条数据" % rid)
        save.write_excel_xls_append_norepeat(book_name_xls, value1)
#获取当前页面的数据
def get_current_weibo_data(elems,book_name_xls,name,yuedu,taolun,maxWeibo):
    #开始爬取数据
        before = 0 
        after = 0
        n = 0 
        timeToSleep = 100
        while True:
            before = after
            Transfer_Clicks(driver)
            time.sleep(3)
            elems = driver.find_elements(By.CSS_SELECTOR,'div.card.m-panel.card9')
            print("当前包含微博最大数量：%d,n当前的值为：%d, n值到5说明已无法解析出新的微博" % (len(elems),n))
            after = len(elems)
            if after > before:
                n = 0
            if after == before:        
                n = n + 1
            if n == 5:
                print("当前关键词最大微博数为：%d" % after)
                insert_data(elems,book_name_xls,name,yuedu,taolun)
                break
            if len(elems)>maxWeibo:
                print("当前微博数以达到%d条"%maxWeibo)
                insert_data(elems,book_name_xls,name,yuedu,taolun)
                break

            if after > timeToSleep:
                print("抓取到%d多条，插入当前新抓取数据并休眠5秒" % timeToSleep)
                timeToSleep = timeToSleep + 100
                insert_data(elems,book_name_xls,name,yuedu,taolun) 
                time.sleep(5)
                # 点击超话按钮，获取超话页面
#点击超话按钮，获取超话页面
def get_superWords():
    time.sleep(5)
    elem = driver.find_element(By.XPATH,"//*[@class='scroll-box nav_item']/ul/li/span[text()='话题']")
    elem.click()
    #获取所有超话
    SuperwordRollToTheEnd()
    elemsOfSuper = driver.find_elements(By.CSS_SELECTOR,'div.card.m-panel.card26')
    return elemsOfSuper
#获取超话链接、名称、讨论量、阅读量
def get_superwordsUrl():
    elemsOfSuper = get_superWords()
    superWords_url = []
    for i in range(0,len(elemsOfSuper)):
        superwordsInfo = []
        print("当前获取第%d个超话链接，共有%d个超话"% (i+1,len(elemsOfSuper)))
        time.sleep(1)
        element = driver.find_elements(By.CSS_SELECTOR,'div.card.m-panel.card26')[i]
        name = driver.find_elements(By.CSS_SELECTOR,'div.card.m-panel.card26 h3')[i].text
        yuedu_taolun = driver.find_elements(By.CSS_SELECTOR,'div.card.m-panel.card26 h4:nth-last-child(1)')[i].text
        yuedu = yuedu_taolun.split(" ")[0]
        taolun = yuedu_taolun.split(" ")[1]
        #获取话题名称，话题讨论数，阅读数
        print(name)
        print(taolun)
        print(yuedu)
        #获取超话链接
        driver.execute_script('arguments[0].click()',element)
        time.sleep(3)
        print(driver.current_url)
        #把链接和超话信息一起存放于列表中
        superwordsInfo = [driver.current_url,name,taolun,yuedu]
        superWords_url.append(superwordsInfo)
        driver.back()
    return superWords_url

#爬虫运行 
def spider(driver,book_name_xls,sheet_name_xls,keyword,maxWeibo):
    
    #创建文件
    if os.path.exists(book_name_xls):
        print("文件已存在")
    else:
        print("文件不存在，重新创建")
        value_title = [["rid", "用户名称", "微博等级", "微博内容", "微博转发量","微博评论量","微博点赞","发布时间","搜索关键词","话题名称","话题讨论数","话题阅读数"],]
        save.write_excel_xls(book_name_xls, sheet_name_xls, value_title)
    
    #加载驱动，使用浏览器打开指定网址  
    driver.set_window_size(452, 790)
    driver.get("https://passport.weibo.cn/signin/login")
    print("开始自动登陆，若出现验证码手动验证")
    time.sleep(3)


    elem = driver.find_element(By.XPATH,"//*[@id='loginName']");
    elem.send_keys(username)
    elem = driver.find_element(By.XPATH,"//*[@id='loginPassword']");
    elem.send_keys(password)
    elem = driver.find_element(By.XPATH,"//*[@id='loginAction']");
    elem.send_keys(Keys.ENTER)  
    print("暂停20秒，用于验证码验证")
    time.sleep(2)

    while 1:  # 循环条件为1必定成立
        result = isPresent()
        # 解决输入验证码无法跳转的问题
        driver.get('https://m.weibo.cn/') 
        print ('判断页面1成功 0失败  结果是=%d' % result )
        if result == 1:
            elems = driver.find_elements(By.CSS_SELECTOR,'div.line-around.layout-box.mod-pagination > a:nth-child(2) > div > select > option')
            #return elems #如果封装函数，返回页面
            break
        else:
            print ('页面还没加载出来呢')
            time.sleep(20)

    time.sleep(2)

    #搜索关键词
    elem = driver.find_element(By.XPATH,"//*[@class='m-text-cut']").click();
    time.sleep(2)
    elem = driver.find_element(By.XPATH,"//*[@type='search']");
    elem.send_keys(keyword)
    elem.send_keys(Keys.ENTER)
    time.sleep(5)

    superWords_url = get_superwordsUrl()
    print("话题链接获取完毕，休眠2秒")
    time.sleep(2)

    for url in superWords_url:
        driver.get(url[0])
        time.sleep(3)
        name = url[1]
        taolun = url[2]
        yuedu = url[3]
        get_current_weibo_data(elems, book_name_xls, name, yuedu, taolun, maxWeibo)  # 爬取综合
        time.sleep(3)
        shishi_element = driver.find_element(By.XPATH,"//*[@class='scroll-box nav_item']/ul/li/span[text()='实时']")
        driver.execute_script('arguments[0].click()', shishi_element)
        get_current_weibo_data(elems, book_name_xls, name, yuedu, taolun, maxWeibo)  # 爬取实时
        time.sleep(5)
        remen_element = driver.find_element(By.XPATH,"//*[@class='scroll-box nav_item']/ul/li/span[text()='热门']")
        driver.execute_script('arguments[0].click()', remen_element)
        get_current_weibo_data(elems, book_name_xls, name, yuedu, taolun, maxWeibo)  # 爬取热门



if __name__ == '__main__':
    username = "18145102375" #你的微博登录名
    password = "hou120149" #你的密码
    driver = webdriver.Edge()#你的chromedriver的地址
    book_name_xls = "weibogun3.xls" #填写你想存放excel的路径，没有文件会自动创建
    sheet_name_xls = '微博数据' #sheet表名
    maxWeibo = 7 #设置最多多少条微博
    keywords = ["禁止堕胎"] # 此处可以设置多个话题，#必须要加上
    for keyword in keywords:
        spider(driver,book_name_xls,sheet_name_xls,keyword,maxWeibo)