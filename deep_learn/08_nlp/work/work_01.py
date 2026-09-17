"""
1. **现有ana_data.tsv文件在作业的data文件夹中,  针对这样一个数据集做如下分析:**

- 分析标签数量分布, 给出样本是否均衡的结论
- 分析句子长度分布, 给出规范的句子长度的结论, 并说明理由

- 生成一张词云图片, 分析一下高频出现的词
"""


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import chain
from wordcloud import WordCloud
import jieba.posseg as pos


def ana_label():

    ana_data.info()
    counts = ana_data['label'].value_counts()
    # label
    # 8    1000
    # 5    1000
    # 2    1000
    # 0    1000
    # 7    1000
    # 1    1000
    # 3    1000
    # 6    1000
    # 4    1000
    # 9    1000
    # 样本是均衡的
    # print(counts)





def ana_sentence():
    ana_data['sentence_len'] = ana_data['sentence'].apply(lambda x: len(x))

    print(ana_data['sentence_len'].max())  # 33
    print(ana_data['sentence_len'].min())  # 4
    print(ana_data['sentence_len'].mean())  # 19.1369

    plt.hist(ana_data['sentence_len'])
    sns.countplot(data=ana_data, x='sentence_len')
    plt.show()

    # 累计长度占比折线图
    total_samples = ana_data.shape[0]
    ratio_list = []
    for l in range(ana_data['sentence_len'].max()):
        # 遍历句子长度 从0到最大长度的所有值
        # 计算句子长度 <= l 的样本总数
        samples = ana_data[ana_data['sentence_len'] <= l].shape[0]
        ratio = samples / total_samples
        ratio_list.append(ratio)

    plt.plot(range(ana_data['sentence_len'].max()), ratio_list)
    plt.grid()
    plt.show()

    sns.boxplot(x=ana_data['sentence_len'])
    plt.show()


def get_a_list(text):
    # 根据传进来的句子找出形容词 并返回
    cut_words = pos.lcut(text)
    a_list = []
    for word, flag in cut_words:
        if flag == 'a':
            # print(word,flag)
            a_list.append(word)

    return a_list


def ana_word_cloud():
    # 进行词云可视化
    word_cloud = WordCloud(font_path='./data/SimHei.ttf', max_words=100, background_color='pink')

    # 进行切词
    keywords_list = list(chain(*map(lambda x: get_a_list(x), ana_data['sentence'])))

    # 生成词云
    word_cloud.generate_from_text(" ".join(keywords_list))
    # 可视化展示
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.show()



if __name__ == '__main__':
    ana_data = pd.read_csv("./data/ana_data.tsv", sep="\t")
    # 每个样本的输出数量是一致的 所以样本是均衡的
    ana_label()
    # 通过图例分析，句子长度在21-28之间分布的最多
    ana_sentence()
    # 词频云图
    ana_word_cloud()





















