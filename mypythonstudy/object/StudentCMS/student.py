"""
学生类  姓名,性别,年龄,手机号,描述信息
"""

class Student:

    # 初始化属性信息
    def __init__(self,stu_id,name,gender,age,phone,desc):
        """
        初始化学生属性信息
        :param stu_id:stu_id
        :param name:姓名
        :param gender:性别
        :param age:年龄
        :param phone:手机号
        :param desc:描述
        """
        self.stu_id = stu_id
        self.name = name
        self.gender = gender
        self.age = age
        self.phone = phone
        self.desc = desc


    # 相当于重写打印方法
    def __str__(self):
        """
        打印学生信息
        :return:
        """
        return (f'stu_id:{self.stu_id},name:{self.name},gender:{self.gender}'
                f'age:{self.age},phone:{self.phone},desc:{self.desc}')

if __name__ == '__main__':
    s = Student('1001','迪丽热巴','女','11','133545135','xxx.xx.xx')
    print(s)