import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1-加载数据集
data = pd.read_csv('data/1960-2019全球GDP数据.csv', sep=',', encoding='gbk')
print(data.head())
# 查看数据集
print(data.shape)
data.info()

# 2-删除缺失值行数据
data.dropna(inplace=True)
print(data.shape)

# 3-获取中美日三个国家的数据 3个df对象
df_cn = data.query('country=="中国"')
df_us = data[data['country'] == '美国']
df_jp = data[data['country'] == '日本']
print(df_cn.shape)
print(df_us.shape)
print(df_jp.shape)
print(df_cn.head())

# 4-将year列设置为行索引值
df_cn.set_index(keys='year', inplace=True)
df_us.set_index(keys='year', inplace=True)
df_jp.set_index(keys='year', inplace=True)
print(df_cn.head())

# 5-修改GDP列名为各自国家名
df_cn.rename(columns={'GDP': '中国'}, inplace=True)
df_us.rename(columns={'GDP': '美国'}, inplace=True)
df_jp.rename(columns={'GDP': '日本'}, inplace=True)
print(df_cn.head())

# 6-绘制折线图
plt.figure(figsize=(5, 1))
plt.plot(df_cn.index, df_cn['中国'], label='中国', color='red')
plt.plot(df_us.index, df_us['美国'], label='美国')
plt.plot(df_jp.index, df_jp['日本'], label='日本')
plt.xlabel('年份')
plt.ylabel('GDP')
plt.legend()
plt.grid()
plt.show()