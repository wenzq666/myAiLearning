import torch


# 初始值
w = torch.tensor(10, requires_grad=True, dtype=torch.float32)
print(w.grad)

# 1.前向传播 (暂无)

for i in range(100000):
    # 2.损失计算
    loss = w**2
    # 3.梯度清零  求导前比做 原因：torch会对多次迭代的导数自动累加
    if w.grad is not None:
        w.grad.zero_()

    # 4.自动求导  自动加工出loss路径上 所有requires_grad=True的张量求导
    loss.backward()
    # print(w.grad)
    # print(w.data)
    # 5.参数更新
    w.data = w.data - 0.01 * w.grad

print(f'100轮后：{w.data}')













