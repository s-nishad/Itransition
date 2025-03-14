import random

class Dice:
    def __init__(self, faces):
        self.faces = faces

    def roll(self):
        return random.choice(self.faces)

    def __str__(self):
        return ",".join(map(str, self.faces))