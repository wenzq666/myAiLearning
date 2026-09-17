"""
    线性回归
"""
# 导入库
from sklearn.linear_model import LinearRegression

# 准备数据
x = [[160],
     [166],
     [172],
     [174],
     [180]]
y = [56.3, 60.6, 65.1, 68.5, 75]

# 实例化模型
model = LinearRegression()

# 模型训练
model.fit(x,y)
print(model.coef_) # 权重/斜率
print(model.intercept_) # 截距/偏置

# 模型预测
pred = model.predict([[176]])

print(pred)

















