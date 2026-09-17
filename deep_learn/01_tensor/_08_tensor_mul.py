import torch


# 两个张量进行哈达玛积 计算  两个张量形状一致 对应元素相乘
t1 = torch.tensor([[1,2],[3,4]])
t2 = torch.tensor([[5,6],[7,8]])

# t3 = t1 * t2
# t3 = t1.mul(t2)
t3 = torch.mul(t1, t2)
print(t3)

print('$'*50)

t11 = torch.randn(5, 5)
print(t11)

o1 = torch.ones_like(t11)

h1 = t11 * o1
print(h1)




