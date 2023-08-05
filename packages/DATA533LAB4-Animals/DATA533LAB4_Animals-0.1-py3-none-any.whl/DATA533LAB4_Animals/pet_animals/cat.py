from DATA533LAB4_Animals.pet_animals.pet import Pet
from DATA533LAB4_Animals.userDefineException2.myException2 import feedError


class Cat(Pet):

    def __init__(self, name, color):
        try:
            assert type(name) == str
        except AssertionError:
            print ("Cat's name should be in string format")
        else:
            self.name = name
        try:
            assert type(color) == str
        except AssertionError:
            print ("Cat's color should be in string format")
        else:
            self.color = color
        self.weight = 6.0 

    def sound(self):
        print("Meow meow prrrrrr")

    def describe(self, adj):
        print("{}, the {}, {} cat".format(self.name, adj, self.color))
        
    def feed(self, cans=1.0):
        kg = cans * .1
        self.weight += kg
        
        try:
            if cans < 0:
                raise feedError("Cans should be a non-negative number")
        except feedError as FE:
            print("Exception raised: ", FE.value)
        
        if self.weight > 6.0:
            print("{} is overweighted. You shouldn't have fed him that much. Check his weight!".format(self.name))
        else:
            print("{} looks happy and satisfied. You should watch-out for his weight though!".format(self.name))
            
    def getWeight(self):
        print ("{} weights {} kg.".format(self.name, self.weight))
        
    def on_a_diet(self, kg_down):
        self.kg_down = kg_down
        self.weight -= kg_down
        print ("{} has been doing a good job, he lost {} kg, and is now {} kg.".format(self.name, self.kg_down, self.weight))
        
    def setWeight(self, weight):
        self.weight = weight 
        print ("{} weights {} kg.".format(self.name, self.weight))