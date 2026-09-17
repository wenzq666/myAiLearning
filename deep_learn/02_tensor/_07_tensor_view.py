import torch


# view() 与原张量公用同一块内存 只是不通的表现  只有连续的张量才能进行view转换
t1 = torch.randn(3, 4)

# 判断张量在内存中是否连续
print(t1.is_contiguous())

t2 = t1.view(2, 6)
print(t2.shape)

t3 = t1.transpose(0,1)
print(t3.shape)
print(t3.is_contiguous())
# 张量不连续 无法进行view()转换
# t4 = t3.view(6, 2)
t4 = t3.reshape(6, 2)
print(t4.shape)

# 非用view()对不连续的张量转换 ： 把不连续的张量转为连续的
t5 = t3.contiguous()
print(t5.is_contiguous())
t6 = t5.view(6, 2)
print(t6.shape)


print('#'*50)
tr1 = torch.randn(size=(3, 8))

tv1 = tr1.view(8,3)
print(tv1.shape)
tv2 = tv1.view(4,6)
# tv2 = tv1.view(4,-1) 只有一个位置可以写-1 自动计算维度
print(tv2.shape)






