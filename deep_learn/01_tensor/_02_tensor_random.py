import torch
from h5py.h5pl import size

# 正态分布
rand1 = torch.randn(size=(3,4))
print(rand1)
# 查看种子
print(torch.initial_seed())

print('*'*50)
# 设置固定种子
torch.manual_seed(666)
# 查看种子

rand2 = torch.randn(2,3)
print(f"rand2_seed:{torch.initial_seed()}")
print(f"rand2:{rand2}")

print('-'*50)

rand3 = torch.randn(2,3)
print(f"rand3_seed:{torch.initial_seed()}")
print(f"rand3:{rand3}")


print('*'*50)

rand4 = torch.randint(0,99,size = (3,4))
print(rand4)


print('#'*50)
torch.manual_seed(22)
rand5 = torch.randn(3,5)
print(torch.initial_seed())
print(rand5)

print('*'*50)

rand6 = torch.randint(0,5,size=(5,5))
print(rand6)







