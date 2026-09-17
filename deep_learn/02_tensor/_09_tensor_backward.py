import torch


# 允许求导的张量 w
# 通过w计算损失
# 同损失计算导数

# 创建允许求导的张量 w
w = torch.tensor([10.,20.], requires_grad=True, dtype=torch.float32)
print(w)

loss = 2 * (w**2)
# 打印出加工loss路径上的导函数
print(loss.grad_fn)

# 计算导数   不需要显示对谁进行求导 只需要对loss.backward() 就会自动求导
# loss是标量 需要对loss进行聚合
loss.sum().backward()
# grad记录了损失函数对w的导数
print(w.grad)


























