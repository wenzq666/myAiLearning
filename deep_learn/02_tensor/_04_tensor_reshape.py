import torch


# .reshape(修改后的形状) 在不修改数据的情况下 改变张量的形状
t1 = torch.tensor([[1,2,3,4,5],[6,7,8,9,0]])
print(t1)
print(t1.shape)
t2 = t1.reshape(1,10)
print(t2)
print(t2.shape)

print('#'*50)
ta1 = torch.arange(0,100)
print(ta1)
print(ta1.shape)

# 转4行25列
ta1_new = ta1.reshape(4, 25)
print(ta1_new)
print(ta1_new.shape)

























