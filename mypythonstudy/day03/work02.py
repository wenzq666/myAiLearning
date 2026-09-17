# 1.需求:定义空列表:  列表名 = []   或者   列表名 = list()
#
# 2.需求: 定义一个列表存储'张三','李四','王五'等多个学生姓名
#
# 3.需求: 在所有姓名列表中找到下标索引为1的姓名
#
# 4.需求: 在所有姓名列表中找到下标索引为-1的姓名
#
# 5.需求: 在所有姓名列表中找到张三

list1 = []
list2 = list()

names = ['张三','李四','王五']

print(names[1])
print(names[-1])
print(names[0])


# 1.需求: 做核酸早上刚开始没有人排队(定义空列表)
# 2.需求: 张三排队到末尾
# 3.需求: 李四和王五夫妻俩一起排队到末尾
# 4.需求: 赵六走关系需要插队到第一个位置
# 5.需求: 删除第一个位置的元素
# 6.需求: 移除做完核酸的张三
# 7.需求: 清空列表中所有元素
people = []
people.append('张三')
print(people)
people.append('李四')
people.append('王五')
print(people)
people.insert(0, '赵六')
print(people)
del people[0]
print(people)
people.remove('张三')
print(people)
people.clear()
print(people)



# 1.需求: 定义列表,已知数据['张三','李四','王五','张三']
# 2.需求: 查询张三在列表中出现次数
# 3.需求: 查询李四在列表中的下标索引
# 4.需求: 查询names列表中有多少个元素
names = ['张三','李四','王五','张三']
print(names.count('张三'))
print(names.index('李四'))
print(len(names))


# 1.需求: 定义 空元组格式两种方式
# 2.需求: 定义一个元组,存储'张三','李四','王五','张三'
# 3.需求: 查询第一个位置的元素
# 4.需求: 查询张三元素在元组中出现次数
# 5.需求: 查询李四元素在元组中的下标索引
# 6.需求: 查询names元组当前元素的个数
tuple1 = ()
tuple2 = tuple()
tuple3 = ('张三','李四','王五','张三')
print(tuple3[0])
print(tuple3.count('张三'))
print(tuple3.index('李四'))
print(len(tuple3))


#james有一个关于爬虫的项目，他需要在一个字符串中查找python这个关键字，
#当前他通过index()函数进行查找，虽然可以实现查找的需求，但是总会在
#没有查找到关键字的时候报错，为什么会报错，如何优化？
str1 = 'sjahdkssjdjsa'
#print(str1.index('python'))
print(str1.find('python'))

#1.需求: 定义字符串 存储 '你TMD哦'
#2.需求: 利用replace把TMD替换成挺萌的
str1 = '你TMD哦'
str2 = str1.replace('TMD', '挺萌的')
print(str2)


#1.需求: 定义字符串'苹果,香蕉,橘子,橙子,榴莲'
#2.需求: 要求把所有水果分开单独放到一个容器中要求结果:['苹果', '香蕉', '橘子', '橙子', '榴莲']
#3.需求: 查看切割后容器类型
#4.需求: 使用切割后生成的列表
fruits = '苹果,香蕉,橘子,橙子,榴莲'
fruits_list = fruits.split(',')
print(type(fruits_list))
print(fruits_list)


# 1.请创建一个空集合set1
# 2. 给set1添加一个元素5
set1 = set()
set1.add(5)
print(set1)



#现有字典dict1 = {'name':'chuanzhi','age':18}
# 要求：
#    1.使用循环将字典中所有的键输出到屏幕上
#     2.使用循环将字典中所有的键输出到屏幕上
#     3.使用循环将字典中所有的键值对输出到屏幕上
#       输出方式：  name：chuanzhi
#                               age :   18
dict1 = {'name':'chuanzhi','age':18}
print(dict1.keys())

print(dict1.values())

print(dict1.items())

for key, value in dict1.items():
    print(f'{key} : {value}')



# 编写一个程序，该程序从控制台接受一个逗号分隔的数字序列，并生成一个列表和一个包含每个数字的元组。
# 假设向该程序提供了以下输入：34,67,55,33,12,98
# 然后，输出应为
# ['34', '67', '55', '33', '12', '98']
# ('34', '67', '55', '33', '12', '98')
# input_str = input('请输入一个逗号分隔的数字序列：')
# input_list = input_str.split(',')
# input_tuple = tuple(input_list)
# print(input_list)
# print(input_tuple)



#编写一个程序，该程序接受一系列由'空格'分隔的单词作为输入，并在删除所有重复的单词并将其按 字母数字顺序排序后打印这些单词。
#假设将以下输入提供给程序：hello world and practice makes perfect and hello world again
#最终输出结果为: again and hello makes perfect practice world
# input_str = input('请输入一系列由空格分隔的单词：')
# words_list = input_str.split(' ')
# unique_words_list = list(set(words_list))
# unique_words_list.sort()
# print(' '.join(unique_words_list))


#有这样的一个列表
# product=[
# {"name":"电脑","price":7000},
# {"name":"鼠标","price":30},
# {"name":"usb电动小风扇","price":20},
# {"name":"遮阳伞","price":50}
# ]，然后小明一共有8000块钱，那么他能不能买下这所有商品？
# 如果能，请输出“能”，否则输出“不能”
product=[
{"name":"电脑","price":7000},
{"name":"鼠标","price":30},
{"name":"usb电动小风扇","price":20},
{"name":"遮阳伞","price":50}]
total_price = sum([item['price'] for item in product])
print(total_price)
if total_price <= 8000:
    print("能")
else:
    print("不能")



# 使用给定的整数n，编写程序以生成包含（i，ixi）的字典，该字典为1到n之间的整数（都包括在
# 内）。然后程序应打印字典。假设向程序提供了以下输入：8
# 然后，输出应为：{1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 6: 36, 7: 49, 8: 64}

n = int(input('输入n:'))
dict1 = {i:i*i for i in range(1, n + 1)}
print(dict1)


# 给定一个列表，首先删除以s开头的元素，
# 删除后，修改第一个元素为"joke"，
# 并且把最后一个元素复制一份，放在joke的后边
my_list = ["spring", "look", "strange", "curious", "black", "hope"]

for item in my_list:
    if item.startswith('s'):
        my_list.remove(item)
my_list[0] = 'joke'
temp_name = my_list[-1]
my_list.insert(my_list.index('joke')+1,temp_name)
print(my_list)






