class Pet:

    def __init__(self, name):
        try:
            assert type(name) == str
        except AssertionError:
            print ("Pet's name should be in string format")
        else:
            self.name = name

    def intro(self):
        print("Hello, my name is {}, I'm your pet".format(self.name))

    def display(self):
        print("Pet's name: {}".format(self.name))
