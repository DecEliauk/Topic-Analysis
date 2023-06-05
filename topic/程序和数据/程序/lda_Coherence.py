import codecs
# import pylDAvis.gensim_models
import matplotlib
from gensim import corpora
from gensim.models import LdaModel, CoherenceModel
from gensim.corpora import Dictionary
import matplotlib.pyplot as plt
import pandas as pd

# 一致性模型确定主题个数
def coherence(num_topics):

    ldamodel = LdaModel(corpus = corpus,id2word=dictionary,num_topics=num_topics,
                        random_state=100,iterations=50)
    coherence_model_lda =CoherenceModel(model=ldamodel,texts=train,corpus=corpus,dictionary=dictionary,coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    print(ldamodel.print_topics(num_topics=num_topics, num_words=7))
    print('\nCoherence Score : ',coherence_lda)
    return coherence_lda

if __name__ == "__main__":

    train = []

    fp = codecs.open('result/gun_cut.txt', 'r', encoding='utf8')    #
    # fp = codecs.open('result/abortion_cut.txt', 'r', encoding='utf8')

    for line in fp:
        if line != '':
            line = line.split()
            train.append([w for w in line])
    # print(train)
    dictionary = Dictionary(train)
    corpus = [dictionary.doc2bow(text) for text in train]

    # 绘制一致性折线图
    x = range(1, 20)  # 主题范围数量
    y = [coherence(i) for i in x]
    plt.plot(x, y)
    plt.xlabel('主题数目')
    plt.ylabel('coherence大小')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False
    plt.title('枪支管控主题-coherence变化情况')
    plt.savefig("img_lda/主题-coherence变化_gun.jpg", dpi=360)
    # plt.savefig("img_lda/主题-coherence变化_abortion.jpg", dpi=360)
    plt.show()
