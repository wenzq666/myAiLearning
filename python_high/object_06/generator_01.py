"""
根据规则不断生成数据的容器   (本质是迭代器)
节约内存  适用于大量数据读取
    1惰性生成
    2本身不存储数据，存生成数据的规则
    3已生成会销毁 不会再生成
"""
# import sys
#
# # 生成器推导式
# g1 = (i**2 for i in range(10))
# print(type(g1))
# print(g1)
# print(sys.getsizeof(g1))
# # 获取数据
# print(next(g1))
# print(next(g1))
# print("="*50)
# # 遍历生成器
# for i in g1:
#     print(i)

# yield
def g1():
    for i in range(10):
        print("start...")
        yield i  # 1暂停等待  2返回数据
        print("end...")

g = g1()
print(type(g))
print(g)

print(next(g))
print(next(g))
print("="*20)

for i in g:
    print(i)
