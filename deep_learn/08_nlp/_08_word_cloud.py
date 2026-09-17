import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # 底层基于matplotlib
import jieba.posseg as pos
from wordcloud import WordCloud
from itertools import chain




def get_a_list(text):
    # 根据传进来的句子找出形容词 并返回
    cut_words = pos.lcut(text)
    a_list = []
    for word, flag in cut_words:
        if flag == 'a':
            # print(word,flag)
            a_list.append(word)

    return a_list


def get_word_cloud(keywords_list):
    # 进行词云可视化
    word_cloud = WordCloud(font_path='./data/SimHei.ttf', max_words=100, background_color='pink')
    # 生成词云
    word_cloud.generate_from_text(" ".join(keywords_list))
    # 可视化展示
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.show()


def gen_cloud():
    train_data = pd.read_csv("./data/train.tsv", sep="\t")
    dev_data = pd.read_csv("./data/dev.tsv", sep="\t")
    # 筛选好评论
    good_data = train_data[train_data['label'] == 1]
    bad_data = train_data[train_data['label'] == 0]

    good_keyword_list = list(chain(*map(lambda x:get_a_list(x),good_data['sentence'])))
    print(good_keyword_list)

    bad_keyword_list = list(chain(*map(lambda x: get_a_list(x), bad_data['sentence'])))
    print(bad_keyword_list)

    get_word_cloud(good_keyword_list)
    get_word_cloud(bad_keyword_list)





if __name__ == '__main__':
    gen_cloud()

    # train_data = train_data['sentence']
    # keyword = []
    # for data in train_data:
    #
    #     keyword.extend(get_a_list(data))
    #
    # get_word_cloud(keyword)


















