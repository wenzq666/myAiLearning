import torch


# 修改张量的数据类型
# 张量.type(转换的类型)
# 张量.类型()


data = torch.randn(3, 5)
print(data.dtype) # torch.float32


# 转换成 double 类型
# data2 = data.type(dtype = torch.DoubleTensor)
data2 = data.type(dtype = torch.float64)
print(data2.dtype) # torch.float64


data3 = data.double()
print(data3.dtype) # torch.float64

print('#' * 50)


rand1 = torch.randn(5, 5)
print(rand1)

rand2 = rand1.double()
print(rand2.dtype)
print(rand2)

rand3 = rand1.long()
print(rand3.dtype)
print(rand3)









