class Employee:
    def work(self):
        pass

class Programmer(Employee):
    def work(self):
        print("编写代码...")

class Manager(Employee):
    def work(self):
        print("管理团队...")

class Company:
    def start_work(self,employee):
        employee.work()

programmer = Programmer()

company = Company()
company.start_work(programmer)

