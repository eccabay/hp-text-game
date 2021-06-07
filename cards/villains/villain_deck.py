import random
import copy

from utils import Action, GameAction
from .villain_card import VillainCard

# Game 1 Villains

crabbe_goyle = VillainCard('Crabbe & Goyle', 5, passive_action=Action(person='all', hearts=-1, passive='discard'), reward=Action(person='all', cards=1))
draco = VillainCard('Draco Malfoy', 6, passive_action=Action(hearts=-2, passive='metal'), reward=Action(metal=-1))
quirrell = VillainCard('Quirinus Quirrell', 6, active_action=Action(hearts=-1), reward=Action(person='all', hearts=1, influence=1))

game_1_cards = [crabbe_goyle, draco, quirrell]

def game_1_deck():
    deck = copy.deepcopy(game_1_cards)
    random.shuffle(deck)
    return deck


# Game 2 Villains

basilisk = VillainCard('Basilisk', 8, passive_action=Action(person='all', passive='draw'), reward=Action(person='all', cards=1, metal=-1))
lucius = VillainCard('Lucius Malfoy', 7, passive_action=GameAction(attacks=-1, passive='metal'), reward=Action(person='all', influence=1, metal=-1))
riddle = VillainCard('Tom Riddle', 6, for_each_action={'ally': Action(hearts=-2, discard=1, choice=True)}, reward=Action(person='all', hearts=2, search='ally', choice=True))

game_2_cards = [basilisk, lucius, riddle]

def game_2_deck():
    deck = copy.deepcopy(game_1_cards) + copy.deepcopy(game_2_cards)
    random.shuffle(deck)
    return deck

# Game 3 Villains

dementor = VillainCard('Dementor', 8, active_action=Action(hearts=-2), reward=Action(person='all', metal=-1))
pettigrew = VillainCard('Peter Pettigrew', 7, active_action=Action(reveal='value', metal=1), reward=Action(person='all', search='spell', metal=-1))

game_3_cards = [dementor, pettigrew]

def game_3_deck():
    deck = copy.deepcopy(game_1_cards) + copy.deepcopy(game_2_cards) + copy.deepcopy(game_3_cards)
    random.shuffle(deck)
    return deck


def get_requested_deck(game):
    if game == 1:
        return game_1_deck()
    if game == 2:
        return game_2_deck()
    if game == 3:
        return game_3_deck()
    else:
        raise ValueError('Game not supported yet')