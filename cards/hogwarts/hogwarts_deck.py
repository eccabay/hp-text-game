import random
import copy
from utils.actions import GameAction

from utils import Action
from .hogwarts_card import HogwartsCard

# Starting Cards
alohomora = HogwartsCard('Alohomora!', 'spell', regular=Action(influence=1))

# Harry
cloak = HogwartsCard('Invisibility Cloak', 'item', regular=Action(influence=1))
firebolt = HogwartsCard('Firebolt', 'item', regular=Action(attacks=1), defeat=Action(influence=1))
hedwig = HogwartsCard('Hedwig', 'ally', regular=Action(hearts=2, attacks=1, choice=True))

harry_starting_cards = [alohomora]*7 + [cloak, firebolt, hedwig]

def get_harry_starting_cards():
    return copy.deepcopy(harry_starting_cards)

# Ron
beans = HogwartsCard('Bertie Botts Every-Flavour Beans', 'item', regular=Action(influence=1), other=Action(attacks=1, passive='ally'))
cleansweep = HogwartsCard('Cleansweep 11', 'item', regular=Action(attacks=1), defeat=Action(influence=1))
pigwidgeon = HogwartsCard('Pigwidgeon', 'ally', regular=Action(hearts=2, attacks=1, choice=True))

ron_starting_cards = [alohomora]*7 + [beans, cleansweep, pigwidgeon]

def get_ron_starting_cards():
    return copy.deepcopy(ron_starting_cards)

# Hermione
time_turner = HogwartsCard('Time-Turner', 'item', regular=Action(influence=1), buy=Action(cards_on_top='spell'))
beedle_the_bard = HogwartsCard('The Tales of Beedle the Bard', 'item', regular=[Action(person='active', influence=2), Action(person='all', influence=1)], regular_choice=True)
crookshanks = HogwartsCard('Crookshanks', 'ally', regular=Action(hearts=2, attacks=1, choice=True))

hermione_starting_cards = [alohomora]*7 + [time_turner, beedle_the_bard, crookshanks]

def get_hermione_starting_cards():
    return copy.deepcopy(hermione_starting_cards)

# Neville
remembrall = HogwartsCard('Remembrall', 'item', regular=Action(influence=1), discard=Action(influence=2))
mandrake = HogwartsCard('Mandrake', 'item', regular=[Action(attacks=1), Action(person='any', hearts=2)], regular_choice=True)
trevor = HogwartsCard('Trevor', 'ally', regular=Action(hearts=2, attacks=1, choice=True))

neville_starting_cards = [alohomora]*7 + [remembrall, mandrake, trevor]

def get_neville_starting_cards():
    return copy.deepcopy(neville_starting_cards)

# Game 1 Cards

lumos = HogwartsCard('Lumos!', 'spell', cost=4, regular=Action(person='all', cards=1))
reparo = HogwartsCard('Reparo!', 'spell', cost=3, regular=Action(influence=2, cards=1, choice=True))
incendio = HogwartsCard('Incendio!', 'spell', cost=4, regular=Action(attacks=1, cards=1))
wingardium_leviosa = HogwartsCard('Wingardium Leviosa!', 'spell', cost=2, regular=Action(influence=1), buy=Action(cards_on_top='item'))
descendo = HogwartsCard('Descendo!', 'spell', cost=5, regular=Action(attacks=2))
sunshine_daisy = HogwartsCard('Sunshine Daisy Butter Mellow Turn This Stupid Fat Rat Yellow!', 'spell', cost=4, regular=Action(hearts=-1, cards=2))

dittany = HogwartsCard('Essence of Dittany', 'item', cost=2, regular=Action(person='any', hearts=2))
quidditch_gear = HogwartsCard('Quidditch Gear', 'item', cost=3, regular=Action(hearts=1, attacks=1))
sorting_hat = HogwartsCard('Sorting Hat', 'item', cost=4, regular=Action(influence=2), buy=Action(cards_on_top='ally'))
snitch = HogwartsCard('Golden Snitch', 'item', cost=5, regular=Action(influence=2, cards=1))

oliver = HogwartsCard('Oliver Wood', 'ally', cost=3, regular=Action(attacks=1), defeat=Action(person='any', hearts=2))
hagrid = HogwartsCard('Rubeus Hagrid', 'ally', cost=4, regular=[Action(attacks=1), Action(person='all', hearts=1)])
dumbledore = HogwartsCard('Albus Dumbledore', 'ally', cost=8, regular=Action(person='all', hearts=1, attacks=1, influence=1, cards=1))

game_1_cards = [lumos, lumos, reparo, reparo, reparo, reparo, reparo, reparo, incendio, incendio, incendio, incendio, wingardium_leviosa, wingardium_leviosa, wingardium_leviosa, descendo, descendo, sunshine_daisy,
                dittany, dittany, dittany, dittany, quidditch_gear, quidditch_gear, quidditch_gear, quidditch_gear, sorting_hat, snitch, oliver, hagrid, dumbledore]

def game_1_deck():
    deck = copy.deepcopy(game_1_cards)
    random.shuffle(deck)
    return deck

# Game 2 Cards

finite = HogwartsCard('Finite!', 'spell', cost=3, regular=Action(metal=-1))
expelliarmus = HogwartsCard('Expelliarmus!', 'spell', cost=6, regular=Action(attacks=2, cards=1))

polyjuice = HogwartsCard('Polyjuice Potion', 'item', cost=3, regular=Action(copy='ally'))
nimbus_2001 = HogwartsCard('Nimbus 2001', 'item', cost=5, regular=Action(attacks=2), defeat=Action(influence=2))

lockhart = HogwartsCard('Gilderoy Lockhart', 'ally', cost=2, regular=Action(cards=1, discard=1), discard=Action(cards=1))
dobby = HogwartsCard('Dobby the House-Elf', 'ally', cost=4, regular=Action(metal=-1, cards=1))
ginny = HogwartsCard('Ginny Weasley', 'ally', cost=4, regular=Action(attacks=1, influence=1))
fawkes = HogwartsCard('Fawkes the Phoenix', 'ally', cost=5, regular=[Action(attacks=2), Action(person='all', hearts=2)], regular_choice=True)
molly = HogwartsCard('Molly Weasley', 'ally', cost=6, regular=Action(person='all', influence=1, hearts=2))
arthur = HogwartsCard('Arthur Weasley', 'ally', cost=6, regular=Action(person='all', influence=2))

game_2_cards = [finite, finite, expelliarmus, expelliarmus, polyjuice, polyjuice, nimbus_2001, nimbus_2001,
                lockhart, dobby, ginny, fawkes, molly, arthur]

def game_2_deck():
    deck = copy.deepcopy(game_1_cards) + copy.deepcopy(game_2_cards)
    random.shuffle(deck)
    return deck


# Game 3 Cards

expecto_patronum = HogwartsCard('Expecto Patronum!', 'spell', cost=5, regular=Action(attacks=1, metal=-1))
petrificus = HogwartsCard('Petrificus Totalus!', 'spell', cost=6, regular=[Action(attacks=1), GameAction(mute=True)])

crystal_ball = HogwartsCard('Crystal Ball', 'item', cost=3, regular=Action(cards=2, discard=1))
marauders_map = HogwartsCard('Marauder\'s Map', 'item', cost=5, regular=Action(cards=2), discard=Action(person='all', cards=1))
chocolate_frog = HogwartsCard('Chocolate Frog', 'item', cost=2, regular=Action(person='any', hearts=1, influence=1), discard=Action(hearts=1, influence=1))
butterbeer = HogwartsCard('Butterbeer', 'item', cost=3, regular=[Action(person='any', hearts=1, influence=1), Action(person='any', hearts=1, influence=1)])

trelawney = HogwartsCard('Sybill Trelawney', 'ally', cost=4, regular=Action(cards=2, discard=1), other=Action(influence=2, passive='discard', discard_type='spell'))
sirius = HogwartsCard('Sirius Black', 'ally', cost=6, regular=Action(attacks=2, influence=1))
lupin = HogwartsCard('Remus Lupin', 'ally', cost=4, regular=[Action(attacks=1), Action(person='any', hearts=3)])

game_3_cards = [expecto_patronum, expecto_patronum, petrificus, petrificus, crystal_ball, crystal_ball, marauders_map,
                chocolate_frog, chocolate_frog, chocolate_frog, butterbeer, butterbeer, butterbeer, trelawney, sirius, lupin]

def game_3_deck():
    deck = copy.deepcopy(game_1_cards) + copy.deepcopy(game_2_cards) + copy.deepcopy(game_3_cards)
    random.shuffle(deck)
    return deck


# Game 4 Cards

accio = HogwartsCard('Accio!', 'spell', 4, regular=Action(influence=2, search='item', choice=True))
protego = HogwartsCard('Protego!', 'spell', 5, regular=Action(attacks=1, hearts=1), discard=Action(attacks=1, hearts=1))
silencio = HogwartsCard('Silencio!', 'spell', 5, regular=Action(attacks=1, silencio=True))

hogwarts_a_history = HogwartsCard('Hogwarts: A History', 'item', 4, regular=Action(roll='any'))
pensieve = HogwartsCard('Pensieve', 'item', 5, regular=[Action(person='any', influence=1, cards=1), Action(person='any', influence=1, cards=1)])
triwizard_cup = HogwartsCard('Triwizard Cup', 'item', 5, regular=Action(attacks=1, influence=1, hearts=1))

cedric = HogwartsCard('Cedric Diggory', 'ally', 4, regular=Action(attacks=1, roll='hufflepuff'))
fleur = HogwartsCard('Fleur Delacour', 'ally', 4, regular=Action(influence=2), other=Action(hearts=2, passive='ally'))
krum = HogwartsCard('Viktor Krum', 'ally', 5, regular=Action(attacks=2), defeat=Action(influence=1, hearts=1))
mcgonagall = HogwartsCard('Minerva McGonagall', 'ally', 6, regular=Action(influence=1, attacks=1, roll='gryffindor'))
sprout = HogwartsCard('Pomona Sprout', 'ally', 6, regular=[Action(influence=1), Action(person='any', hearts=2), Action(roll='hufflepuff')])
flitwick = HogwartsCard('Filius Flitwick', 'ally', 6, regular=Action(influence=1, cards=1, roll='ravenclaw'))
snape = HogwartsCard('Severus Snape', 'ally', 6, regular=Action(attacks=1, hearts=2, roll='slytherin'))
moody = HogwartsCard('Alastor "Mad-Eye" Moody', 'ally', 6, regular=Action(influence=2, metal=-1))


game_4_cards = [accio, accio, protego, protego, protego, silencio, hogwarts_a_history, hogwarts_a_history, hogwarts_a_history, hogwarts_a_history, hogwarts_a_history,
                hogwarts_a_history, pensieve, triwizard_cup, cedric, fleur, krum, mcgonagall, sprout, flitwick, snape, moody]

def game_4_deck():
    deck = copy.deepcopy(game_1_cards) + copy.deepcopy(game_2_cards) + copy.deepcopy(game_3_cards) + copy.deepcopy(game_4_cards)
    random.shuffle(deck)
    return deck


def get_requested_deck(game):
    if game == 1:
        return game_1_deck()
    elif game == 2:
        return game_2_deck()
    elif game == 3:
        return game_3_deck()
    elif game == 4:
        return game_4_deck()
    else:
        raise ValueError('Game not supported yet')
