import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # 底层基于matplotlib
import numpy as np


train_data = pd.read_csv("./data/train.tsv", sep="\t")
dev_data = pd.read_csv("./data/dev.tsv", sep="\t")


pd.set_option('display.max_colwidth', None)


train_data['sentence_length']= train_data['sentence'].apply(lambda sentence:len(sentence))

# 句子长度分布
print(train_data['sentence_length'].max())# 3370
print(train_data['sentence_length'].min())# 2
print(train_data['sentence_length'].mean())# 83.70033783783784


print(train_data['sentence_length'].describe())


# 箱线图：一眼看出中位数、四分位距、离群点
# sns.boxplot(x=train_data['sentence_length'])
# plt.show()


# 小提琴图：箱线图 + 密度形状
# sns.violinplot(x=train_data['sentence_length'])
# plt.show()


# 核密度估计图（KDE）
# sns.kdeplot(train_data['sentence_length'], fill=True)
# plt.show()


# 累积分布函数（CDF / ECDF）
# sns.ecdfplot(train_data['sentence_length'])
# plt.axhline(0.98, color='r', linestyle='--')  # 95%分位参考线
# plt.axvline(350, color='g', linestyle='--')
# plt.show()

# sns.histplot(np.log1p(train_data['sentence_length']), bins=50, kde=True)
# plt.show()



bins = [0, 20, 50, 100, 200, 500, 3500]
labels = ['0-20', '21-50', '51-100', '101-200', '201-500', '500+']
train_data['len_bucket'] = pd.cut(train_data['sentence_length'], bins=bins, labels=labels)
print(train_data['len_bucket'].value_counts().sort_index())
print(train_data['len_bucket'].value_counts(normalize=True).sort_index())  # 比例

sns.countplot(data=train_data, x='len_bucket')  # 这里countplot就合适了，因为已经离散化
plt.show()


# 看分布
# plt.hist(train_data['sentence_length'])
# sns.countplot(data=train_data, x='sentence_length')
# plt.show()


#频率直方图



#累计长度占比折线图
# total_samples = train_data.shape[0]
# ratio_list = []
# for l in range(train_data['sentence_length'].max()):
#     # 遍历句子长度 从0到最大长度的所有值
#     # 计算句子长度 <= l 的样本总数
#     samples = train_data[train_data['sentence_length'] <= l].shape[0]
#     ratio = samples / total_samples
#     ratio_list.append(ratio)
#
#
#
# plt.plot(range(train_data['sentence_length'].max()), ratio_list)
# plt.grid()
# plt.show()

















