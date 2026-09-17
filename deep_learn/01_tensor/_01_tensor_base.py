import torch
import numpy as np


print(torch.__version__)


# 张量的基础创建
# 0维张量
t1 = torch.tensor(1.234)
print(t1)


# 1维张量
t2 = torch.tensor([1, 2, 3, 4])
print(t2)
print(t2.dtype) # torch.int64

# 2维张量
t3 = torch.tensor([[1, 2, 3, 4],[5, 6, 7, 8]])
print(t3)

# 通过numpy数组创建张量
arr1 = np.array([[1, 2, 3, 4],[5, 6, 7, 8]])
print(f"arr1:{arr1},type:{type(arr1)}")

t4 = torch.tensor(arr1)
print(f"t4:{t4},type:{type(t4)}")

print('*'*50)

ts1 = torch.tensor(6.6666)
print(ts1)

ts2 = torch.tensor([[7,4,1],[8,5,2],[9,6,3]])
print(ts2)

arr = np.random.randn(3,5)
print(f"arr:{arr},type:{type(arr)}")
ts3 = torch.tensor(arr)
print(f"ts3:{ts3},type:{type(ts3)}")

print('*'*50)
# 通过指定形状创建张量
T1 = torch.Tensor(2, 3) # 指定2行3列  数字是torch自动生成
print(T1)
print(T1.dtype)

T2 = torch.Tensor([2, 3])
print(T2)

print('*'*50)
# 创建指定元素类型的张量
i1 = torch.IntTensor([1,2,3,4.2])
print(i1)

s1 = torch.ShortTensor()
print(s1)

l1 = torch.LongTensor()
print(l1)

f1 = torch.FloatTensor()
print(f1)
print(f1.dtype)

d1 = torch.DoubleTensor()
print(d1)

h1 = torch.HalfTensor()
print(h1)


print('#'*50)

T3 = torch.Tensor(2,4)
print(T3)
print(T3.dtype)

F2 = torch.FloatTensor(3,3)
print(F2)
print(F2.dtype)



print('#'*50)
# 特殊张量创建
# 线性张量
# 左闭右开
a1 = torch.arange(0, 10 ,1)
print(a1)
print(a1.dtype)

#
lin1 = torch.linspace(0, 10, 5)
print(lin1)
print(lin1.dtype)


print('#'*50)

arr2 = torch.arange(0, 100 ,2)
print(arr2)

line2 = torch.linspace(0,100,10000)
print(line2)










