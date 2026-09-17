import torch

t1 = torch.tensor([1, 2, 3, 4, 5])
t1 = t1.float()

# t1_new = t1 + 10
t1_add = t1.add(10)
print(t1_add)

# t1_sub = t1 - 10
t1_sub = t1.sub(10)
print(t1_sub)

# 取反
t1_neg = t1.neg()
print(t1_neg)

print('*'*50)

# 在元数据做修改
t1.add_(10)
print(t1)
t1.sub_(10)
print(t1)

