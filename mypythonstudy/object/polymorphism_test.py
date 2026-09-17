class Animal:
    def speek(self):
        pass


class Dog(Animal):
    def speek(self):
        print('www')


class Cat(Animal):
    def speek(self):
        print('mmm')


class Car():
    def speek(self):
        print('ddd')


def make_sounds(an:Animal):
    an.speek()

d:Animal = Dog()
c:Animal = Cat()

car = Car()
make_sounds(car)

make_sounds(d)
make_sounds(c)
