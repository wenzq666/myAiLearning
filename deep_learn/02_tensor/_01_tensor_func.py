import torch


# 统计函数
# mean(dim=0/1)
# sum(dim=0/1)
t1 = torch.tensor([[1, 2, 3],
                        [4, 5, 6]],dtype=torch.float32)

print(t1)
print(t1.dtype)

# 张量的属性
print('*'*50)
print(t1.shape) # t1.size()

print('*'*50)

# 均值 不指定dim对所有元素求平均
print(t1.mean())

# dim是张量形状的索引 例如：torch.Size([2, 3])
# dim等于几 对应维度就会消失
# 按列求均值
print(t1.mean(dim=0))
# 按行求均值
print(t1.mean(dim=1))

print('***************高维张量****************')
t2 = torch.tensor([[[1,2,3],[4,5,6]],
              [[7,8,9],[10,11,12]],
              [[13,14,15],[16,17,18]]])

# 3组
print(t2.shape)
print('*'*50)

# 求和 sum()
t3 = torch.tensor([[1, 2, 3],
                        [4, 5, 6]],dtype=torch.float32)

print(t3.sum())
# 2行3列  维度2行消失 只剩下3列
print(t3.sum(dim=0))
# 2行3列  维度3列消失 只剩下2行
print(t3.sum(dim=1))

print('#'*50)
tr1 = torch.randint(0,10,size=(3,5),dtype=torch.float32)
print(tr1) # 3行5列
# 按行统计和
print(tr1.sum(dim=1))
# 按列统计平均值
print(tr1.mean(dim=0))

print('#'*50)

# 运算函数
# 求根 .sqrt()
# 求指数 .exp()
# 求对数 .log()

# 求根
t5 = torch.randn(3, 4)
print(t5)
print(f"求根:{t5.sqrt()}")
print(f"求指数:{t5.exp()}")
print(f"求对数:{t5.log()}")# 以自然常数e为底

t6 = torch.tensor([2])
print(t6.log2())

t7 = torch.tensor([100])
print(t7.log10())

print('#'*50)
tt1 = torch.tensor([10])
print(f"算数平方根:{tt1.sqrt()}")
print(f"指数:{tt1.exp()}")
print(f"以10为底的数:{tt1.log10()}")







