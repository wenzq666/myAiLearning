class Girl():
    def __init__(self,name,age):
        self.name = name
        self.__age = age

    def get_age(self):
        return self.__age

    def set_age(self,age):
        self.__age = age

girl = Girl("迪丽热巴",20)
print(girl.get_age())










