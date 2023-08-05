class Livestock:
    def __init__(self, owner):
        try:
            if not isinstance(owner, str):
                raise TypeError("Owner must be a string")
        except TypeError:
            print("Owner must be a string")

        self.owner = owner

    def intoduce(self):
        print("Hi, I am %s's livestock" % self.owner)

    def display(self):
        print("Infor:")
        print("Owner: %s" % self.owner)
