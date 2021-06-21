import random


class Die:
    def __init__(self, house, dominant):
        self.house = house
        self.sides = ['influence', 'attack', 'card', 'heart'] + [dominant]*2

    def roll(self):
        result = random.choice(self.sides)
        print(f'Rolled {result}')
        return result


gryffindor = Die('gryffindor', 'influence')
hufflepuff = Die('hufflepuff', 'heart')
ravenclaw = Die('ravenclaw', 'card')
slytherin = Die('slytherin', 'attack')