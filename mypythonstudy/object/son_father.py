class GrandFather:
    # 定义属性
    def __init__(self):
        self.myopia = '老花眼'
        self.selfMoney = 1000.00


    # 定义方法
    def walk(self):
        print('只能慢慢走路')

    def extendMoney(self):
        print(f'家产有{self.selfMoney}元')

class Father:
    # 定义属性
    def __init__(self):
        self.myopia = '近视眼'
        self.selfMoney = 100.00

    # 定义方法
    def walk(self):
        print('能正常走路')

    def extendMoney(self):
        print(f'家产有{self.selfMoney}元')

class Son(Father,GrandFather):
    # 定义属性
    def __init__(self):
        self.myopia = '正常眼'
        self.selfMoney = 10.00

    # 定义方法
    def walk(self):
        print('能正跑')

    def extendMoney(self):
        super().__init__()
        super().extendMoney()



s = Son()
s.extendMoney()







