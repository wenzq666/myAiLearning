# 学生类
class Student:

    # 学习
    def study(self):
        print(f"{self.name}正在学习")

    # 吃饭
    def eat(self):
        self.food = '饭'
        print(f"{self.name}正在吃{self.food}")

# 定义
stu = Student()

stu.name = "迪丽热巴"
stu.study()

stu.eat()













