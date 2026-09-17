from object_02.animals_test.animals import Animal


# Define a Cat class that inherits from the Animal class
class Cat(Animal):
    # The pass statement is used as a placeholder for empty code
    # This class doesn't have any additional methods or attributes yet

    def __init__(self,name):
        super(Cat,self).__init__(name)


    def call(self):
        print("cat speaking.....")




