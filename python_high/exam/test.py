class My:
    class_var = 0
    def __init__(self):
        self.ins = 0

obj1 = My()
obj2 = My()

My.class_var = 10
obj1.ins = 5

print(obj2.class_var)
print(obj2.ins)



