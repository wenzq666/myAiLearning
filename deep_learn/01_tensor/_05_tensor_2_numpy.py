import numpy as np
import torch
import numpy as pd


# 张量转numpy  张量.numpy()
# 内存共享
# t1 = torch.randn(4, 5)
# print(type(t1))
#
#
# n1 = t1.numpy()
# print(type(n1))
# print(n1)
#
# n1[0][0] = 666
# print(n1)
#
# print(t1)

print('*'*50)

# 避免内存共享
# n2 = t1.numpy().copy()
# n2[0][0] = 999
#
# print(n2)
#
# print(t1)


print("############ numpy 2 tensor ############")
arr1 = pd.array([1,2,3,4,5,6])

# arr1.copy() 避免内存共享
t3 = torch.from_numpy(arr1.copy())
print(t3)

# 不共享内存
t4 = torch.tensor(arr1)
print(t4)

print('*'*50)
arr1[0] = 888
print(arr1)
print(t3)

print('*'*50)


print('$'*50)

arr3 = np.array([5, 6, 7, 8])
# arr3转张量 要求内存共享
t5 = torch.from_numpy(arr3)
arr3[0] = 0.0
print(arr3)
print(t5)

print('￥'*30)


t6 = torch.randn(3, 5)
# t6 转 numpy 要求内存不共享
n6 = t6.numpy().copy()
n6[0] = 0.00
print(n6)
print(t6)



print('==========================')

arr11 = np.array([1,2,3,4])
print(arr11)

t11 = torch.from_numpy(arr11)

arr11 = np.array([6,6,6,6])
print(arr11)
print(t11)








