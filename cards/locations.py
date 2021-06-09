import copy

class Location:
    def __init__(self, name, max, dark_arts):
        self.name = name
        self.max = max
        self.dark_arts = dark_arts
        self.current = 0

    def __str__(self):
        return f'{self.name}   Metal: {self.current}/{self.max}   {self.dark_arts} Dark Arts Events'


# Game 1 Locations
diagon_alley = Location('1 of 2 - Diagon Alley', 4, 1)
mirror = Location('2 of 2- Mirror of Erised', 4, 1)

game_1_cards = [diagon_alley, mirror]

def game_1_deck():
    return copy.deepcopy(game_1_cards)


# Game 2 Locations
forbidden_forest = Location('1 of 3 - Forbidden Forest', 4, 1)
quidditch_pitch = Location('2 of 3 - Quidditch Pitch', 4, 1)
chamber_of_secrets = Location('3 of 3 - Chamber of Secrets', 5, 2)

game_2_cards = [forbidden_forest, quidditch_pitch, chamber_of_secrets]

def game_2_deck():
    return copy.deepcopy(game_2_cards)


# Game 3 Locations
hogwarts_express = Location('1 of 3 - Hogwarts Express', 5, 1)
hogsmeade = Location('2 of 3 - Hogsmeade Village', 6, 2)
shrieking_shack = Location('3 of 3 - Shrieking Shack', 6, 2)

game_3_cards = [hogwarts_express, hogsmeade, shrieking_shack]

def game_3_deck():
    return copy.deepcopy(game_3_cards)


def get_requested_deck(game):
    if game == 1:
        return game_1_deck()
    elif game == 2:
        return game_2_deck()
    elif game == 3:
        return game_3_deck()
    else:
        raise ValueError('Game not supported yet')
