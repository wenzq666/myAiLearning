# 定义类
class Car:
    # 定义方法
    def run(self):
        print(self)
        print("car running...")

    def show(self):
        self.color = "red"
        print(f"车的颜色是{self.color}")
        print(f"车的轮胎数量是{self.number}")

car = Car()
car.number = 4
#car.run()
car.show()
print(car.color)







# car2 = Car()
# car2.run()


# class Animal:
#     def run(self):
#         print("dog running...")
#
#
#
# dog = Animal()
# dog.run()