import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # 底层基于matplotlib
import jieba
from itertools import chain


train_data = pd.read_csv("./data/train.tsv", sep="\t")
dev_data = pd.read_csv("./data/dev.tsv", sep="\t")


pd.set_option('display.max_colwidth', None)

train_data.info()
print(train_data[:])


# 不同词汇的统计
count = list(map(lambda x:jieba.lcut(x),train_data['sentence']))
# print(count)
cont_all = set(chain(*count))
print(cont_all)

print(len(cont_all))











