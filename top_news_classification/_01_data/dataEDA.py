"""
数据探索性分析
"""
from config import Config
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt


# 实例化Config对象 获取训练集路径
config = Config()
train_file_path = config.train_datapath

# pd读取训练集数据
train_data = pd.read_csv(train_file_path, sep='\t', names=['text', 'label'])

# 查看前几行
print(train_data.head())
train_data.info()

# 统计标签分布  --> 结论： 各个样本都是18000行 样本均衡
print(train_data['label'].value_counts())
#Counter({3: 18000, 4: 18000, 1: 18000, 7: 18000, 5: 18000, 9: 18000, 8: 18000, 2: 18000, 6: 18000, 0: 18000})
# label_count = Counter(train_data['label'])
# print(label_count)
print('##############################################################')
# 分析文本长度
# 新增text_length
train_data['text_length'] = train_data['text'].apply(lambda x:len(x))
print(train_data.head())

print(train_data['text_length'].mean().round(2)) # 19.21
print(train_data['text_length'].std().round(2)) # 3.86
print(train_data['text_length'].min()) # 3
print(train_data['text_length'].max()) # 38

# 绘制text_length与label的直方图.
plt.hist(train_data['text_length'], bins=50)

plt.show()

print(f"3σ原则筛选 长度上限 = 均值 + 3标准差 = {19.21 + 3 * 3.86}")

# 绘制累积长度占比图
total_samples = len(train_data)
ratio_list = []
for length in range(train_data['text_length'].max() + 1):
    count_sample = train_data[train_data['text_length'] <= length].shape[0]
    ratio = count_sample / total_samples
    ratio_list.append(ratio)
plt.plot(range(train_data['text_length'].max() + 1), ratio_list)
plt.grid()
plt.show()


