import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # 底层基于matplotlib


train_data = pd.read_csv("./data/train.tsv", sep="\t")
dev_data = pd.read_csv("./data/dev.tsv", sep="\t")


pd.set_option('display.max_colwidth', None)

train_data.info()
print(train_data[:])


# 分析训练集标签数量分布
train_label_value_counts = train_data['label'].value_counts()
# 0    1518
# 1    1442
# 结论基本均衡
print(train_label_value_counts)

sns.countplot(data=train_data, x='label', hue='label')
# plt.show()


# 分析验证集的标签分布
dev_label_value_counts = dev_data['label'].value_counts()
print(dev_label_value_counts)

sns.countplot(data=dev_data, x='label', hue='label')
# plt.show()















