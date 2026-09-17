# 编写一个程序，实现以下功能：
#
# 1. 创建一个列表`class_roster`，初始化包含5个学生姓名
# 2. 打印初始班级名单
# 3. 通过input()获取一个新学生姓名，使用append()方法添加到列表末尾
# 4. 通过input()获取一个学生姓名，判断该学生是否在名单中：
#    - 如果存在，使用remove()方法移除该学生
#    - 如果不存在，输出"该学生不在班级名单中"
# 5. 使用for循环遍历并打印更新后的班级名单
# 6. 为关键代码添加注释
# 1- 初始化一个班级的学生名单
class_roster = ['张三','李四','王五','赵六','田七']

# 2- 打印初始班级名单
print(f"目前存在学生信息有:{class_roster}")

# 3- 通过input录入一个新的学生的信息:
name = input("请输入一个新学生的姓名:")

# 3.1 将姓名添加到列表末尾
class_roster.append(name)

# 4- 通过input 获取一个要查找的学生姓名
name = input("请输入要查询的学生姓名:")

# 4.1 判断 用户输入的学生是否存在
if name in class_roster:
    # 说明学生存在, 如果存在 直接移除掉
    class_roster.remove(name)
else:
    # 说明学生不存在, 打印该学生不在班级名单中
    print("该学生不在班级名单中")

# 5 遍历当前的班级名单
for name in class_roster:
    print(name)