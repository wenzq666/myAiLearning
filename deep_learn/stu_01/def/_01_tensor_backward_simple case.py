import torch



w1 = torch.tensor(10.0, requires_grad=True)
loss = 2 + w1

print(loss)
print(type(loss))
print(type(loss.grad_fn))
print(w1.grad)

print("===========================================================")
# 创建两个需要求导的张量
x = torch.tensor(2.0, requires_grad=True)
y = torch.tensor([10.0, 20.], requires_grad=True)

# 进行乘法运算
z = x * y  # 20 = 2 * 10

print(z)
# 输出: tensor(20., grad_fn=<MulBackward0>)


z.sum().backward()
print("反向传播就是求导，先对x求偏导:")
print(f"第一次反向传播的x梯度值:{x.grad}") # 10.0

print("对y求偏导:")
print(f"第一次反向传播的y梯度值:{y.grad}") # 2.0


# 权重更新
x.data = x.data - 0.001 * x.grad
print(f"x更新权重：{x.data}")

y.data = y.data - 0.001 * y.grad
print(f"y更新权重：{y.data}")

# x.grad.zero_()
# y.grad.zero_()
# 进行乘法运算
z2 = x * y  # 20 = 2 * 10

# 再次计算并反向传播
z2.sum().backward()
print("第二次先对x求偏导:")
print(f"第二次反向传播的x梯度值:{x.grad}")  # 输出: 20.  <-- 梯度累加了！

print("第二次先对y求偏导:")
print(f"第二次反向传播的y梯度值:{y.grad}")


# 权重更新
x.data = x.data - 0.001 * x.grad
print(f"第二次x更新权重：{x.data}")

y.data = y.data - 0.001 * y.grad
print(f"第二次y更新权重：{y.data}")


print("=======================================================")









