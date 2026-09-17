import pandas as pd

# 创建示例数据
df = pd.DataFrame({
    '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
    '年龄': [25, 30, 35, 28, 32],
    '部门': ['技术部', '销售部', '技术部', '人事部', '销售部'],
    '工资': [5000, 7500, 6000, 5500, 7500]
})
print(df)

print('=' * 80)
# 条件筛选
# 获取部门名称为销售部的数据
print(df['部门'] == '销售部')
# 等同于 select * from 表名 where 部门='销售部'
result1 = df[df['部门'] == '销售部']
print(result1)
# 获取部门名称为销售部并且年龄大于30的数据
# & : and  | : or  ~ : not
# 等同于 select * from 表名 where 部门='销售部' and 年龄>30
result2 = df[(df['部门'] == '销售部') & (df['年龄'] > 30)]
# result2 = df[(df['部门'] == '销售部') | (df['年龄'] > 30)]
# result2 = df[~((df['部门'] == '销售部') & (df['年龄'] > 30))]
print(result2)
print('=' * 80)
# query() 等同于 sql中的 where
# result3 = df.query(expr="部门=='销售部'")
# result3 = df.query(expr="部门=='销售部' and 年龄>30")
result3 = df.query(expr="not (部门=='销售部' and 年龄>30)")
print(result3)

print('=' * 80)
# 排序：sort_values()
# by: 排序字段
# ascending: 排序方式, 默认为True->升序 False->降序
print(df.sort_values(by='年龄', ascending=True))
# 多列排序逻辑和sql一样
print(df.sort_values(by=['工资', '年龄'], ascending=True))
result4 = df.sort_values(by=['工资', '年龄'], ascending=[True, False])
print(result4)

