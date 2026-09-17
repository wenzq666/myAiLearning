import torch


# 布尔索引  在索引的位置写筛选条件
torch.manual_seed(66)
t1 = torch.randint(0, 10, size=(3, 5))
print(t1)

# 行筛选
# 第三列 小于5的行
print(t1[t1[:,2]<5,:])

# 筛选第2行 大于5的列
print(t1[ : , t1[1] > 5])

print('#'*50)
tr1 = torch.randint(-5, 5, size=(5, 7))
print(tr1)
# 筛选第3行大于0的列
print(tr1[:,tr1[2] > 0])

# 筛选出第5列小于0的行
print(tr1[ tr1[:,4] <0])

print('#'*50)

# 多维索引  语法同上
tr3 = torch.randint(0, 10, size=(2, 3, 5))
print(tr3.shape)

print(tr3)

# 筛选出第1组 第2行第3列 的元素
print(tr3[0, 1, 2])


















































