class Animal:
    def call(self):
        print("动物叫...")

class Dog(Animal):
    def call(self):
        print("狗叫...")

class Cat(Animal):
    def call(self):
        print("猫叫...")


if __name__ == '__main__':
    dog:Animal = Dog()
    dog.call()

