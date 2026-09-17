import torch
import numpy as np


# 第三题：请使用 torch.tensor() 方法创建一个包含数据 [[1.5, 2.5], [3.5, 4.5]] 的二维张量（矩阵）
t1 = torch.tensor([[1.5, 2.5], [3.5, 4.5]])
print(t1)


# 第四题：请使用 torch.Tensor() 方法创建一个 **3行4列** 的张量，并打印输出结果。
T1 = torch.Tensor(3, 4)
print(T1)


# 第五题：请使用 torch.IntTensor() 创建一个包含元素 [5, 10, 15, 20] 的一维整型张量，并打印输出结果。
ti1 = torch.IntTensor([5, 10, 15, 20])
print(ti1)

# 第六题：请使用 torch.arange() 方法创建一个从 10 开始，到 50 结束（不包含50），步长为 5 的一维张量，并打印输出结果
a1 = torch.arange(10, 50, 5)
print(a1)


# 第七题：请使用 torch.linspace() 方法，在区间 0 到 100 之间均匀地生成 11 个数字组成的一维张量，并打印输出结果。
l1 = torch.linspace(0 ,100 ,11)
print(l1)


#第八题：为了保证每次生成的随机数一致，请先使用 torch.random.manual_seed() 将随机数种子设置为 88，
# 然后再使用 torch.randn() 创建一个 **2行4列** 的随机张量，并打印该张量。
torch.random.manual_seed(88)
tr1 = torch.randn(2, 4)
print(tr1)


# 第九题：请使用 torch.full() 方法创建一个形状为 **3行3列**，且所有元素值均为数字 7 的张量，并打印输出结果。
f1 = torch.full(size=(3, 3),fill_value=7)
print(f1)

# - 第一步：使用 torch.ones(2, 2) 创建一个 2x2 的全1张量，命名为 x
# - 第二步：将 x 的数据类型转换为 float64，命名为 y。
# - 第三步：分别打印 x.dtype 和 y.dtype。
x = torch.ones(2, 2)
y = x.float()
print(x.dtype)
print(y.dtype)


# - 第一步： 使用numpy创建一个3行5列的随机数矩阵
# - 第二步：转成张量， 要求内存不共享
# - 第三步：将转换后的张量的元素类型转为double精度的浮点数类型
n1 = np.random.randn(3,5)
tt1 = torch.tensor(n1)
tt1 = tt1.double()
print(tt1)

# - 第一步：创建一个3行5列的随机张量， 一个5行3列的随机张量， 计算二者的矩阵乘法结果
# - 第二步：将第一步矩阵乘法结果， 与一个3行3列的全1张量做Hardamard(点乘)运算
# - 第三步：将第二步点乘运算结果取反
tr1 = torch.randn(3, 5)
tr2 = torch.randn(5, 3)
tmm = torch.matmul(tr1, tr2)
print(tmm)
to = torch.ones_like(tmm)
tm = torch.mul(tmm, to)
print(tm)
tn = tm.neg()
print(tn)





