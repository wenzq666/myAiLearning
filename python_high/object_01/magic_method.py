class Student(object):

    # 初始化方法
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"学生姓名:{self.name},学生年龄:{self.age}"

    def __del__(self):
        print(f"{self}对象被删除")


stu = Student("迪丽热巴",18)
print(stu.name)
print(stu)

