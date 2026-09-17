class Person:
    def __init__(self,name,age,role="普通人员"):
        self.name = name
        self.__age = age
        self.__role = role

    def get_name(self):
        return self.__age

    def set_age(self,age):
        self.__age = age

    def get_role(self):
        return self.__role

    def __str__(self):
        return f"姓名：{self.name}，年龄：{self.__age}，角色：{self.__role}"
    
class Teacher(Person):
    def __init__(self,name,age,course):
        super().__init__(name,age,"教师")
        self.course = course

    def teach(self):
        print(f"{self.name} 正在讲授 {self.course} 课程")

    def grade_student(self,teacher,student, score):
        print(f"{self.name}给{student.name}的‘{teacher.course}’课程打分为{score}分")

        student.add_score(teacher.course,score)


class Student(Person):
    def __init__(self, name, age, scores=None):
        super().__init__(name,age,"学生")
        if scores is None:
            scores = {}
        self.__scores = scores

    def add_score(self, course, score):
        self.__scores[course] = score

    def get_average(self):
        if self.__scores.values() is not None and len(self.__scores.values()) >0 :
            total = 0
            for i in self.__scores.values():
                total += i
            return total/len(self.__scores.values())
        else:
            return 0

    def is_passed(self):
        if self.__scores.values() is not None and len(self.__scores.values()) >0 :
            flag =  True
            for i in self.__scores.values():
                if i < 60 :
                    flag = False
            return flag
        return False

    def __str__(self):
        sup = super().__str__()
        return f"{sup}, 成绩：{self.__scores}"


class Course:
    total_courses = 0

    @classmethod
    def show_total(cls):
        print(f"学校共开设了 {cls.total_courses} 门课程")

    @staticmethod
    def is_valid_score(score):
        if 0 <= score <= 100:
            return True
        else:
            return False

    def __init__(self,name,teacher,students=None,max_students=30):
        self.name = name
        self.teacher = teacher
        if students is None:
            self.students = []
        else:
            self.students = students
        self.__max_students = max_students
        Course.total_courses += 1

    def add_student(self,student):
        self.students.append(student)

    def remove_student(self,student):
        self.students.remove(student)

    def show_info(self):
        print(f"课程名:{self.name},任课教师姓名{self.teacher.name},选课人数{len(self.students)}")

    def __str__(self):
        return f"课程名:{self.name},任课教师姓名{self.teacher.name},选课人数{len(self.students)}"

if __name__ == '__main__':
    # stu = Student("迪丽热巴",20,None)
    # stu.add_score("语文",59)
    # stu.add_score("数学",100)
    #
    # print(stu.get_average())
    #
    # print(stu.is_passed())
    #
    # print(stu)
    #
    # tea = Teacher("python老师",18,"python")
    #
    # course = Course("python",tea,None)
    # course.add_student(stu)
    # # print(course.students)
    #
    # course.show_info()


    tea1 = Teacher("张老师",35,"Python编程")
    tea2 = Teacher("李老师",42,"数据结构")

    stu1 = Student("小明",20)
    stu2 = Student("小红",19)
    stu3 = Student("小刚",21)

    cre1 = Course("Python编程",tea1)
    cre2 = Course("数据结构",tea2)

    cre1.add_student(stu1)
    cre1.add_student(stu2)

    cre2.add_student(stu2)
    cre2.add_student(stu3)


    cre1.show_info()
    cre2.show_info()

    # 张老师给小明打分 `95`，给小红打分 `82`
    tea1.grade_student(tea1,stu1,95)
    tea1.grade_student(tea1,stu2, 82)

    # 李老师给小刚打分 `58`，给小红打分 `90`
    tea2.grade_student(tea2,stu3,58)
    tea2.grade_student(tea2,stu2,90)

    print(stu1)
    print(stu2)
    print(stu3)

    print(f"小明成绩是否及格:{stu1.is_passed()}")

    Course.show_total()

    print(Course.is_valid_score(105))







