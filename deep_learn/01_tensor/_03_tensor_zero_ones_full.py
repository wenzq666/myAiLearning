import torch


# 全0张量
# zero(形状)
# zero_like(张量)
z1 = torch.zeros(3, 5)
print(z1)

r1 = torch.randn(4,2)
z2 = torch.zeros_like(r1)
print(z2)

print('*'*50)
# 全1张量
o1 = torch.ones(3, 4)
print(o1)

r1 = torch.randn(2,5)
o2 = torch.ones_like(r1)
print(o2)

print('*'*50)


# 全指定值张量
# full(形状, 填充值)
# full_like(张量, 填充值)
f1 = torch.full(size=(3, 5), fill_value=66.66)
print(f1)

f2 = torch.full_like(r1,99.99)
print(f2)



print('#'*50)
torch.manual_seed(22)
rand1 = torch.randn(4, 4)

print(torch.zeros_like(rand1))

print(torch.full(size=(8, 8), fill_value=255))




