import numpy as np

# 创建数组对象
# low: 最小值
# high: 最大值
# size: 创建数组的维度
arr1 = np.random.randint(low=0, high=10, size=(2, 3))
print(arr1.shape)
print(arr1)

# 修改数组的形状
# reshape(): 在不改变原数组的元素个数下, 修改数组的形状  ※※※
# arr2 = arr1.reshape((1, 6))  # (1, 6)
# arr2 = arr1.reshape((3, 2))  # (3, 2)
arr2 = arr1.reshape((6,))  # (6, )
print(arr2)
# arr2 = arr1.reshape((6, 2))  # 发生报错, 和原数组的元素个数不匹配
# -1: 会自动计算值 未知数x  3 * -1 = 3 * x = 2 * 3  x=2
arr2 = arr1.reshape((3, -1))
print(arr2.shape)
print(arr2)

# print('=' * 80)
# # 修改数组的形状 -> 新数组的元素个数可以和原数组的元素个数不一致
# # arr4 = np.resize(arr1, (3, 2))
# # arr4 = np.resize(arr1, (6,))
# # arr4 = np.resize(arr1, (10,))
# arr4 = np.resize(arr1, (3, 5))
# print(arr4.shape)
# print(arr4)
#
# print('=' * 80)
# # 转置 -> 行变列, 列变行
# # arr1 =  np.random.randint(low=0, high=10, size=(2, 3, 4))
# arr5 = arr1.T
# print(arr5.shape)
# print(arr5)
#
# print('=' * 80)
# # 展平 -> 将多维数组转换成一维数组
# arr1 = np.random.randint(low=0, high=10, size=(2, 3, 4))
# arr6 = arr1.flatten()
# print(arr6.shape)
# print(arr6)

