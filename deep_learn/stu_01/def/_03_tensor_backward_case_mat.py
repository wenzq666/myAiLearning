import torch


# 特征 x  2行5列 全1矩阵
x = torch.ones(2, 5)
print(f"x:{x}")

# 标签 y(真实值) 2行3列 全0矩阵
y = torch.zeros(2, 3)
print(f"y:{y}")

# 初始化 w(权重)
torch.manual_seed(66)
w = torch.randn(5, 3, requires_grad=True)
print(f"w:{w}")

# 初始化 b(偏置)
b = torch.randn(2, 3, requires_grad=True)
print(f"b:{b}")

# 前向传播 算出 z(预测值)
z = torch.matmul(x, w) + b
print(f"z:{z}")

# 损失函数
criterion = torch.nn.MSELoss()
# 损失
loss = criterion(z, y)

# 自动微分
loss.sum().backward()

# 打印w,b用来更新的梯度
print(f"w的梯度{w.grad}")
print(f"b的梯度{b.grad}")

# 更新参数
w = w - 0.01 * w.grad
print(f"w更新更细后的参数{w}")















