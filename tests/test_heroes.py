from cards.heroes import Hero
from cards.hogwarts.hogwarts_card import HogwartsCard
from cards.villains import VillainCard
from game import GameState
from utils import Action


def test_harry_cloak():
    harry = Hero('harry', 1)
    cloak = HogwartsCard('Invisibility Cloak', 'item', regular=Action(influence=1))
    harry.deck.append(cloak)

    harry.cloaked = False
    assert harry.hearts == 10

    action = Action(hearts=-3)
    action.apply(harry)
    assert harry.hearts == 7

    harry.draw_card()
    assert harry.cloaked == True
    action.apply(harry)
    assert harry.hearts == 6


def test_end_turn_resets_cards_on_top():
    hero = Hero('neville', 1)
    hero.cards_on_top.append('spell')

    hero.end_turn()
    assert hero.cards_on_top == []


def test_defeat_villain_card_reward():
    firebolt = HogwartsCard('Firebolt', 'item', regular=Action(attacks=1), defeat=Action(influence=1))
    villain = VillainCard('Test Villain', 1, reward=Action(hearts=1))
    game = GameState(['harry', 'ron'], 1)
    harry = game.get_active_hero()

    harry.hand = [firebolt]
    assert harry.attacks == harry.influence == 0
    firebolt.play(harry, game)
    assert harry.attacks == 1
    assert harry.influence == 0
    assert 'defeat' in harry.good_passive

    villain.attack(1, game, '1')
    assert harry.attacks == 1
    assert harry.influence == 1


def test_play_purchased_card():
    game = GameState(['harry', 'ron'], 1)
    harry = game.get_active_hero()
    incendio = HogwartsCard('Incendio!', 'spell', cost=4, regular=Action(attacks=1, cards=1))

    harry.hand = [incendio]

    assert harry.attacks == 0
    incendio.play(harry, game)
    assert harry.attacks == 1
    assert len(harry.hand) == 2


def test_multiple_defeat_bonus():
    firebolt = HogwartsCard('Firebolt', 'item', regular=Action(attacks=1), defeat=Action(influence=1))
    oliver = HogwartsCard('Oliver Wood', 'ally', cost=3, regular=Action(attacks=1), defeat=Action(hearts=2))
    villain = VillainCard('Test Villain', 1, reward=Action(hearts=1))
    game = GameState(['harry', 'ron'], 1)
    harry = game.get_active_hero()

    harry.hand = [firebolt, oliver]
    harry.hearts = 5
    assert harry.influence == 0

    firebolt.play(harry, game)
    oliver.play(harry, game)

    assert harry.attacks == 2
    assert harry.influence == 0
    assert harry.hearts == 5

    villain.attack(1, game, '1')
    assert harry.attacks == 2
    assert harry.influence == 1
    assert harry.hearts == 8  # +1 for defeating the villain, +2 for oliver wood