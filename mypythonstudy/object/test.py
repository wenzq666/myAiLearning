class Student(object):
    # 初始化属性
    def __init__(self , name ,age):
        self.name = name
        self.age = age

    # 函数
    def study(self):
        print(f'{self.name}在睡觉')

    # 重写 __str__
    def __str__(self):
        return (f'姓名:{self.name},年龄{self.age}')

    # 重写 __del__
    def __del__(self):
        print(f'{self.name}被开除了')

###
s1 = Student("张三",18)
s1.study()
print(s1)

s2 = Student("lisi",20)
s2.study()
print(s2)