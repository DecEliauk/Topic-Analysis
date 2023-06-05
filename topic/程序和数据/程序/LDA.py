import codecs
import pyLDAvis
import pyLDAvis.gensim_models
from gensim import corpora
from gensim.models import LdaModel
from gensim.corpora import Dictionary

train = []

fp = codecs.open('result/gun_cut.txt', 'r', encoding='utf8')
# fp = codecs.open('result/abortion_cut.txt', 'r', encoding='utf8')

for line in fp:
    if line != '':
        line = line.split()
        train.append([w for w in line])

dictionary = corpora.Dictionary(train)
corpus = [dictionary.doc2bow(text) for text in train]
lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=5, passes=100)

# num_topics：主题数目
# passes：训练伦次
# num_words：每个主题下输出的term的数目
topics = open('result_lda/gun_topics.txt', 'w', encoding='utf-8')
# topics = open('result_lda/aobrtion_topics.txt', 'w', encoding='utf-8')

for topic in lda.print_topics(num_words=20):
    termNumber = topic[0]
    topics_num = str(topic[0])+':'
    print(topic[0], ':', sep='')
    topics.write(topics_num + '\n')
    listOfTerms = topic[1].split('+')
    for term in listOfTerms:
        listItems = term.split('*')
        topics_words = '  '+ str(listItems[1])+'('+str(listItems[0])+')'
        print('  ', listItems[1], '(', listItems[0], ')', sep='')
        topics.write(topics_words + '\n')
d = pyLDAvis.gensim_models.prepare(lda, corpus, dictionary)

'''
lda: 计算好的话题模型
corpus: 文档词频矩阵
dictionary: 词语空间
'''
pyLDAvis.save_html(d, 'lda_pass4_gun.html')
# pyLDAvis.save_html(d, 'lda_pass4_abortion.html')

