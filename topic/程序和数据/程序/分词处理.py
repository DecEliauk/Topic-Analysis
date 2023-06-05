
import re
import jieba as jb
import pandas as pd

def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords

# 对句子进行分词
def seg_sentence(sentence):
    sentence = re.sub(u'[#0-9a-zA-Z\.]+', u'', str(sentence))#去除英文和数字
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

# 读取评论内容并去除完全重复评论
# inputs = pd.read_csv('gun_comment.csv')['评论内容'].drop_duplicates()
# inputs = pd.read_csv('gun_话题热点词阅读量等.csv')['话题'].drop_duplicates()
inputs = pd.read_csv('abortion_话题热点词阅读量等.csv')['话题'].drop_duplicates()
# inputs = pd.read_csv('abortion_comment.csv')['评论内容'].drop_duplicates()

# outputs = open('result/gun_话题_cut.txt', 'w', encoding='utf-8')
outputs = open('result/abortion_话题_cut.txt', 'w', encoding='utf-8')
# outputs = open('result/abortion_cut.txt', 'w', encoding='utf-8')

for line in inputs:
    line_seg = seg_sentence(line)  # 这里的返回值是字符串
    if line_seg.split():#去除空行
        outputs.write(line_seg + '\n')
outputs.close()
# inputs.close()