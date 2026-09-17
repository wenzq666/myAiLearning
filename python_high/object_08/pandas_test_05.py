import pandas as pd


# 加载csv文件
df = pd.read_csv('./data/分组聚合数据.csv',sep=',')

# 等同于 select 产品,sum(销售额) from df group by 产品
res1 = df.groupby(by=['产品'])['销售额'].sum()
print(res1)


# 等同于 select 产品,sum(销售额),sum(数量) from df group by 产品
res2 = df.groupby(by=['产品'])[['销售额','数量']].sum()
print(res2)

# 等同于 select 产品,sum(销售额) from df group by 产品,地区
res3 = df.groupby(by=['产品','地区'])['销售额'].sum()
print(res3)


# 等同于 select 产品,sum(销售额),max(数量) from df group by 产品
res4 = df.groupby(by=['产品']).agg({'销售额':'sum','数量':'max'})
print(res4)
print('*'*50)
# 需求: 过滤掉上海的数据, 然后统计不同地区的总销售额, 并基于总销售额进行降序
res5 = df[df['地区']!='上海'].groupby(by=['地区'])['销售额'].sum().sort_values(ascending=False)
print(res5)








