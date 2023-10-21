class Reagent():
    """docstring for Reagent"""

    def __init__(self, name, rtype, score):
        # if rtype is not "PH":
        #     self.name = name.strip()
        # else:
        #     self.name = name

        self.name = name
        self.rtype = rtype
        self.score = score

    def __str__(self):
        return str(self.name)
