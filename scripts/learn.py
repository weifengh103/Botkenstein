
class MethodTypes:

    name = "Ragnar"

    def instanceMethod(self):
        # Creates an instance atribute through keyword self
        self.lastname = "Lothbrock"
    
        print(self.name)
        print(self.lastname)

    @classmethod
    def classMethod(cls):
        print(cls.name)
        # Access a class atribute through keyword cls
        cls.name = "Lagertha"
        
        print(cls.name)

   
    def staticMethod():
        print("This is a static method")

# Creates an instance of the class
MethodTypes.staticMethod()

MethodTypes.classMethod()
# Calls instance method
m = MethodTypes()
m.instanceMethod()


MethodTypes.classMethod()
MethodTypes.staticMethod()