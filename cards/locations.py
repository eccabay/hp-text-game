import copy

from utils import Action

class Location:
    def __init__(self, name, max, dark_arts, reveal_action=None):
        self.name = name
        self.max = max
        self.dark_arts = dark_arts
        self.reveal_action = reveal_action
        self.current = 0

    def __str__(self):
        return f'{self.name}   Metal: {self.current}/{self.max}   {self.dark_arts} Dark Arts Events'

    def reveal(self, game):
        if self.reveal_action is not None:
            self.reveal_action.apply(game.active_hero, game)


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


# Game 4 Locations
world_cup = Location('1 of 3 - Quidditch World Cup', 6, 1)
triwizard_tournament = Location('2 of 3 - Triwizard Tournament', 6, 2)
graveyard = Location('3 of 3 - Graveyard', 7, 2, Action(person='all', discard=1, discard_type='ally'))

game_4_cards = [world_cup, triwizard_tournament, graveyard]

def game_4_deck():
    return copy.deepcopy(game_4_cards)


# Game 5 Locations
azkaban = Location('1 of 3 - Azkaban', 7, 1)
hall_of_prophecy = Location('2 of 3 - Hall of Prophecy', 7, 2)
ministry_of_magic = Location('3 of 3 - Ministry of Magic', 7, 2, Action(person='all', discard=1, discard_type='spell'))

game_5_cards = [azkaban, hall_of_prophecy, ministry_of_magic]

def game_5_deck():
    return copy.deepcopy(game_5_cards)

def get_requested_deck(game):
    if game == 1:
        return game_1_deck()
    elif game == 2:
        return game_2_deck()
    elif game == 3:
        return game_3_deck()
    elif game == 4:
        return game_4_deck()
    elif game == 5:
        return game_5_deck()
    else:
        raise ValueError('Game not supported yet')
