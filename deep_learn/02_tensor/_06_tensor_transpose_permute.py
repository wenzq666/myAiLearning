import torch


# 张量.transpose(交换维度1, 交换维度2)  / torch.transpose(张量, 交换维度1, 交换维度2)
t1 = torch.randn(size=(3, 4, 5))
# 转换成 (3, 5, 4)
# t2 = t1.transpose(1,2)
# print(t2)
# print(t2.shape)

# (3, 4, 5) 转换成 (4, 5, 3)
# t3 = t1.transpose(0, 1)
# print(t3.shape) # torch.Size([4, 3, 5])
# t4 = t3.transpose(1,2)
# print(t4.shape)

print('*'*50)
# 张量.permute()  可以一次交换多个维度
# 一次性转换
t5 = t1.permute(1, 2, 0)
print(t5.shape)

print('#'*50)
tr1 = torch.randn(size=(2, 1, 3, 4))

# 降维 去掉形状大小为1的维度
tr1_new = tr1.squeeze()
print(tr1_new.shape)

# 交换降维后张量的维度 最终的形状是(3, 4, 2)
tr_finally = tr1_new.permute(1, 2, 0)
print(tr_finally.shape)


















