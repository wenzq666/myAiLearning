import torch


# 先设置一个初始值
w = torch.tensor(10.0, requires_grad=True)


# 定义损失函数
loss = w ** 2 + 20

print(f"权重初始值:{w}, loss: {loss}")

# 循环100次求最优解
for i in range(1, 101):
    # 损失计算
    loss = w ** 2 + 20

    # 梯度清零
    if w.grad is not None:
        w.grad.zero_()

    # 反向传播
    loss.backward()

    # 梯度更新
    w.data = w.data - 0.01 * w.grad
    print(f"第{i}次求解后,权重值:{w:.2f}, 0.01 * w.grad:{(0.01 * w.grad):.2f}, loss: {loss:.2f}")





















