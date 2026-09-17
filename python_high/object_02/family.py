class Father:
    def make_money(self):
        print("money.....")

class Mother:
    def cook(self):
        print("cook......")


class Son(Father,Mother):
    pass


son = Son()
son.make_money()

print(Son.__mro__)
print(Son.__bases__)