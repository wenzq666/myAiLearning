class Person:
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def eat(self):
        print(f"{self.name}:eating....")

    def sleep(self):
        print(f"{self.name}:sleeping....")

class Student(Person):
    def __init__(self, name, age, score):
        super().__init__(name, age)
        self.score = score

    def __str__(self):
        return f"学生姓名:{self.name},学生年龄:{self.age},学生成绩:{self.score}"

class Teacher(Person):
    def teach(self):
        print(f"{self.name}:teaching....")


s = Student("迪丽热巴",20,100)
print(s)
s.eat()
s.sleep()

t = Teacher("古力娜扎",30)
t.eat()
t.sleep()
t.teach()















