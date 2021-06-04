import random
import copy

from utils import Action
from .dark_arts_card import DarkArtsCard

# Game 1 Dark Arts

expulso = DarkArtsCard('Expulso!', active=Action(hearts=-2))
flipendo = DarkArtsCard('Flipendo!', active=Action(hearts=-1, discard=1))
petrification = DarkArtsCard('Petrification', active=Action(person='all', hearts=-1), passive=Action(person='all', passive='draw'))
hwmnbn = DarkArtsCard('He-Who-Must-Not-Be-Named', active=Action(metal=1))

game_1_cards = [expulso, expulso, expulso, flipendo, flipendo, petrification, petrification, hwmnbn, hwmnbn, hwmnbn]

def game_1_deck():
    deck = game_1_cards
    random.shuffle(deck)
    return deck


# Game 2 Dark Arts

hand_of_glory = DarkArtsCard('Hand of Glory', active=Action(hearts=-1, metal=1))
relashio = DarkArtsCard('Relashio!', active=Action(person='all', hearts=-2, discard=1, discard_type='item', choice=True))
obliviate = DarkArtsCard('Obliviate!', active=Action(person='all', hearts=-2, discard=1, discard_type='spell', choice=True))
poison = DarkArtsCard('Poison', active=Action(person='all', hearts=-2, discard=1, discard_type='ally', choice=True))

game_2_cards = [hand_of_glory, hand_of_glory, relashio, obliviate, poison]

def game_2_deck():
    deck = copy.deepcopy(game_1_cards) + copy.deepcopy(game_2_cards)
    random.shuffle(deck)
    return deck

def get_requested_deck(game):
    if game == 1:
        return game_1_deck()
    if game == 2:
        return game_2_deck()
    else:
        raise ValueError('Game not supported yet')