import torch

"""
1
"""
# 行列索引
# data[行索引, 列索引]
torch.manual_seed(66)
data = torch.randint(0, 10, size=(3, 5))
print(data)

# 获取第2行 第3列的数组
print(data[1, 2])

# 获取所有行 第4列
print(data[:, 3])

# 如果索引中只写一个数字 表示最前面维度的索引
print(data[0])

# 列表索引
# 选定的元素是 [0, 2]  和  [1, 3]
print(data[[0, 1], [2, 3]])




"""
    行索引 [[0],[1]]
    列索引 [1,2]
    底层 广播机制 同一成 2行2列
    行索引 [[0,0],[1,1]]
    列索引 [[1,2],[1,2]]
    对应元素绑定到一起
"""
# 选定元素是 [[0,1] [0,2]
#           [1,1] [1,2]]
print(data[[[0],[1]],[1, 2]])


print('#'*50)
# A B C D行  7列
tr1 = torch.randint(0, 10, size=(4, 7))
print(tr1)
# 找出第4行 找出第6列
print(tr1[3, 5])
# 找出A B C D 第5列的值
print(tr1[:, 4])
# 统计第六、七行 的数值
wdata = tr1[:, 5:]
print(wdata)
print(wdata.sum())
print('#'*50)

# 范围索引
print(tr1[:, -2:])

























































