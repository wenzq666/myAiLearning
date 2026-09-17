from student import Student

class StudentCMS:

    # 属性
    def __init__(self):
        # 空列表用于存储学生对象信息
        self.stu_list = []

    # 定义界面
    @staticmethod
    def show_view():
        print('*' * 23)
        print('学生信息管理系统')
        print('\t1.添加学生信息')
        print('\t2.修改学生信息')
        print('\t3.删除学生信息')
        print('\t4.查询单个学生信息')
        print('\t5.查询所有学生信息')
        print('\t6.保存学生信息')
        print('\t0.退出')
        print('*' * 23)
        print()


    # 定义函数 实现功能
    # 添加学生信息
    def add_student(self):
        # id,name,gender,age,phone,desc
        in_stu_id = input('输入学生姓名id:')
        in_name = input('输入学生姓名:')
        in_gender = input('输入学生性别:')
        in_age = input('输入学生年龄:')
        in_phone = input('输入学生手机:')
        in_desc= input('输入学生描述:')
        stu = Student(in_stu_id,in_name,in_gender,in_age,in_phone,in_desc)
        self.stu_list.append(stu)
        print(f'添加{in_name}信息成功')

    # 修改学生信息
    def update_student(self):
        in_id = input('输入要修改学生的id:')
        for stu in self.stu_list:
            if in_id == stu.stu_id:
                stu.age = input('输入修改后的年龄:')
                stu.phone = input('输入修改后的电话:')
                stu.desc = input('输入修改后的描述:')

                print(f'修改{stu}成功')
                break
            else:
                print('查无此人')


    # 删除学生信息
    def del_student(self):
        in_id = input('输入要删除学生的id:')
        for stu in self.stu_list:
            if in_id == stu.stu_id:
                self.stu_list.remove(stu)
                print(f'删除{stu}成功')
                break
            else:
                print('查无此人')


    # 查询单个学生信息
    def find_one_student(self):
        in_id = input('输入要查询学生的id:')
        for stu in self.stu_list:
            if in_id == stu.stu_id:
                print(f'查询{stu}成功')
                break
            else:
                print('查无此人')


    # 查询所有学生信息
    def find_all_student(self):
        if len(self.stu_list) == 0:
            print('暂无学生信息\n')
        else:
            for stu in self.stu_list:
                print(stu)
            print()


    # 保存学生信息
    def save_student(self):
        with open('./stu_data.txt','w',encoding='utf-8') as dest_f:
            stu_dict = [stu.__dict__ for stu in self.stu_list]
            dest_f.write(str(stu_dict))
            print(f'保存学生信息成功')


    # 加载学生信息
    def load_student(self):
        # try:
            with open('./stu_data.txt','r',encoding='utf-8') as src_f:
                stu_data = src_f.read()
                stu_list = eval(stu_data)
                if len(stu_list) == 0:
                    self.stu_list = []
                self.stu_list = [Student(**stu_dict) for stu_dict in stu_list]
        # except:
        #     with open('./stu_data.txt', 'w', encoding='utf-8') as dest_f:
        #         pass

    # 开始
    def exec_cms(self):
        self.load_student()
        # 循环
        while True:
            StudentCMS.show_view()
            input_num = input('输入要操作的编号:')
            # 根据输入的编号判断进入不同的功能
            if input_num == '1':
                # 添加学生信息
                print('添加学生信息\n')
                self.add_student()

            elif input_num == '2':
                print('修改学生信息\n')
                # 修改学生信息
                self.update_student()
            elif input_num == '3':
                print('删除学生信息\n')
                # 删除学生信息
                self.del_student()
            elif input_num == '4':
                print('查询单个学生信息\n')
                # 查询单个学生信息
                self.find_one_student()
            elif input_num == '5':
                print('查询所有学生信息\n')
                # 查询所有学生信息
                self.find_all_student()
            elif input_num == '6':
                print('保存学生信息\n')
                # 保存学生信息
                self.save_student()
            elif input_num == '0':
                # 退出系统
                res = input('要退出吗?(Y/N):')
                if res.lower() == 'y':
                    self.save_student()
                    print('已退出')
                    break
            else:
                print('录入有误,重新输入\n')








if __name__ == '__main__':
    cms = StudentCMS()
    cms.exec_cms()















