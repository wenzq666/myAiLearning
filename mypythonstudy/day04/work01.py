# 演示: 列表的查询API


# 1- 定义一个列表
list1 = ['张三', '李四', 5, 10, True, False, 5, '张三', '张三']

print(list1)

# 2- 演示相关的API
# 2.1 index:  判断 李四在列表中下标位置
print(list1.index('李四'))


# 2.2 count : 统计 张三在列表中出现了多少次呢
list1.count('张三')


# 2.3 in 和 not in
# 判断 数字5 是否在 容器中, 如果在, 帮我统计 数字5 出现了多少次
print(5 in list1)
if 5 in list1:
    print(list1.count(5))


# 演示 列表的添加操作


# 定义一个列表
list2 = [7, 5, 3, 9, 10, 2]
print(list2)
# 需求1: 向列表添加一个数字 20
list2.append(20)
print(list2)


# 需求2: 有以下一个列表, 请将该列表中元素添加到 list2中
list3_tmp = [15,19,13]
list2.extend(list3_tmp)
print(list2)

# 需求3: 在索引 2的位置 添加一个 100
list2.insert(2,100)
print(list2)

# 需求4: 删除 索引下标为 2 的数据
list2.pop(2)
print(list2)

# 需求5: 从直接弹出当前列表中最后一个元素,并且拿到该元素的内容
print(list2.pop())
print(list2)
# 需求6: 删除列表中 数字 20
list2.remove(20)
print(list2)
# 需求7: 请修改 第5个索引的数据, 将其更改4
list2[5] = 4
print(list2)
# 需求8: 对列表进行反转:
list2.reverse()
print(list2)

# 需求9: 对数据进行排序操作
list2.sort()
print(list2)




#  求相邻元素最大值.编写一个程序，求一个正整数数组中每对相邻元素的最大值。
#  例如, 输入: [7 8 9 5 6 7 2 3] 输出: [8, 9, 9, 6, 7, 7, 3]
list3 = [7, 8, 9, 5, 6, 7, 2, 3]
list4 = []
for i in range(0,len(list3)-1):
    if list3[i] > list3[i+ 1]:
        list4.append(list3[i])
    else:
        list4.append(list3[i+ 1])
print(list4)



# 演示元组的相关操作


# 1- 定义一个元组:
tuple_1 = ('张三', '李四', '王五', 5, 10, 15, 5)

# 2- 获取元组中的数据:
# 根据索引获取指定的元素  查询索引为2
print(tuple_1[2])


# 获取某个元素的索引值: 获取索引10
print(tuple_1.index(10))


# 获取某个元素出现了几次: 统计5出现了几次
print(tuple_1.count(5))

# 获取元组的长度
print(len(tuple_1))

# 3- 如何遍历元组: 与 列表是一样的
for i in tuple_1:
    print(i)



# 编写一个程序来提取嵌套元组中的唯一元素。
# 例如: 在嵌套元组((1,2,3),(2,4,6),(2,3,5))中, 2重复出现了3次，3重复出现了2次，但我们的输出列表只会包含2、3一次。
# 即：[1, 2, 3, 4, 5, 6]
tuple_tmp1,tuple_tmp2,tuple_tmp3 = ((1,2,3),(2,4,6),(2,3,5))
s1 = set(tuple_tmp1)
s2 = set(tuple_tmp2)
s3 = set(tuple_tmp3)
s1.update(s2)
s1.update(s3)
list2 = list(s1)
print(list2)



# 给定一个元组my_tuple，里面包含1, 2, 3, 4, 5, 6, 7, 8, 9元素，要求统计数字元组中, 奇数的个数
my_tuple = (1, 2, 3, 4, 5, 6, 7, 8, 9)
n = 0;
for i in my_tuple:
    if i % 2 != 0:
        n += 1
print(n)

list3 =  [i for i in my_tuple if i % 2 != 0]
print(len(list3))


# 演示集合操作


# 1- 如何定义集合
# 方式一
set1 = {1, 2, 3, 2, 6, '张三', '李四', '张三'}

print(set1)

# 方式二:
set2 = set()

print(set2)

# 2- 相关的操作:
# 2.1 添加数据: 给 set2 添加  1  2  3  三个元素
set2.add(1)
set2.add(2)
set2.add(3)
print(set2)

# 2.2 删除数据:  请将 set1中 张三 删除
set1.remove('张三')
print(set1)
# 2.3 查找操作: 查询 在 set1中是否有 王五 如果没有 请添加
if '王五' not in set1:
    set1.add('王五')
print(set1)
# 2.4 遍历操作
for i in set1:
    print(i)

print('----------------')
# 编写一个程序来统计缺失的数字并返回它们的总和。缺失的数字是指给定列表中两个极端（最大和最小数字）之间没有出现的数字。
# 例如，在集合{2, 5, 3, 7, 5, 7}中，两个极端（即2和7）之间缺失的数字是4和6。
set3 = {5, 2, 3, 7, 7, 5}
list4 = list(set3)
print(list4)
list4.sort()
list5 = []

for i in range(0,len(list4)-1):
    if list4[i+1] - list4[i] != 1:
        list5.append(list4[i]+1)

sum = 0
for i in list5:
    sum += i
print(sum)


# 演示 字典的相关操作

# 需求: 定义一个字典 用于保存一个用户信息
# 信息如下:  姓名为张三  年龄为 20岁  出生日期: 2005-10-25 地址为北京市昌平区建材城西路  爱好有 篮球 足球 台球
dict1 = {"name":"张三","age":20,"birth":"2005-10-25","addr":"北京市昌平区建材城西路","loves":['篮球','足球','台球']}

# 相关API演示:
#  1- 添加数据:  请添加一个性别 为 男
dict1.update({"gender":"男"})
print(dict1)

# 2- 修改数据: 请将出生日期 修改为 2005-03-15
dict1.update({"birth":"2005-03-15"})
print(dict1)

# 3- 删除数据: 删除 爱好
dict1.pop("loves")
print(dict1)

# 4- 查询API
# 4.1 根据key 获取 value: 获取 address信息
print(dict1["addr"])

# 4.2 获取所有的key  并遍历
for i in dict1.keys():
    print(i)

# 4.3 获取所有的value  并遍历
for i in dict1.values():
    print(i)

# 4.4 获取kv对   并遍历
for k,v in dict1.items():
    print(f'{k}{v}')




# 给定一个字符串my_string，现在要求统计每个字符出现的次数: 形成结果: {'字符':出现次数,'字符2':次数}
# 例如: 'abceacf' ==> {'a':2,'b':1,'c':2,'e':1,'f':1}

my_string = 'asdfasdfghjn'
dict2 = {}
for i in my_string:
    if dict2.get(i) is None:
        dict2.update({i : 1})
    else:
        dict2.update({i:dict2[i]+1})

print(dict2)



# 需求: 编写一个程序将字符串转换为字典  例如:输入: '5=Five 6=Six 7=Seven'   输出: {'5': 'Five', '6': 'Six', '7': 'Seven'}
str1 = '5=Five 6=Six 7=Seven'
print(str1.split())
dict3 = {}
for item in str1.split():
    list_new = item.split("=")
    dict3.update({list_new[0]:list_new[1]})
print(dict3)





