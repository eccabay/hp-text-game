from game import GameState
from cards.heroes import hero, Hero
from cards.dark_arts import DarkArtsCard
from cards.hogwarts.hogwarts_card import HogwartsCard
from cards.villains import VillainCard
from utils import Action

def test_villain_replacement():
    game = GameState(['harry', 'ron'], 1)
    assert len(game.current_villains) == 1

    test_villain = VillainCard('Test Villain', 1, reward=Action(hearts=1))
    game.current_villains[1] = test_villain
    assert len(game.current_villains) == 1

    test_villain.attack(1, game, '1')
    assert len(game.current_villains) == 1
    assert game.current_villains[1] is None

    game.end_turn()
    assert len(game.current_villains) == 1
    assert game.current_villains[1] != 'Test Villain'


def test_defeat_villain_removes_passive():
    test_villain = VillainCard('Test Villain', 1, passive_action=Action(person='all', passive='draw'), reward=Action('all', cards=1))
    game = GameState(['neville', 'ron'], 1)
    neville, ron = game.heroes

    test_villain.apply_passive(neville, game.heroes)
    assert 'draw' in neville.bad_passive
    assert 'draw' in ron.bad_passive

    assert len(ron.hand) == 5
    result = ron.draw_card()
    assert result == 0
    assert len(ron.hand) == 5

    test_villain.attack(1, game, '1')
    assert 'draw' not in neville.bad_passive
    assert 'draw' not in ron.bad_passive
    assert len(ron.hand) == 6
    ron.draw_card()
    assert len(ron.hand) == 7


def test_passive_only_on_bad():
    draco = VillainCard('Draco Malfoy', 6, passive_action=Action(hearts=-2, passive='metal'), reward=Action(metal=-1))
    hwmnbn = DarkArtsCard('He-Who-Must-Not-Be-Named', active=Action(metal=1))
    finite = HogwartsCard('Finite!', 'spell', 3, regular=Action(metal=-1))
    game = GameState(['neville', 'ron'], 1)
    neville = game.get_active_hero()

    draco.apply_passive(neville, game.heroes)
    hwmnbn.apply(neville, game)
    assert game.current_location.current == 1
    assert neville.hearts == 8

    finite.play(neville, game)
    assert game.current_location.current == 0
    assert neville.hearts == 8


def test_for_each():
    test_villain = VillainCard('Test Villain', 3, for_each_action={'spell': Action(hearts=-1)})
    test_spell = HogwartsCard('Test Spell', 'spell')
    test_item = HogwartsCard('Test Item', 'item')

    harry = Hero('harry')
    harry.hand = [test_spell, test_item, test_item, test_spell, test_spell]

    test_villain.apply_for_each(harry)
    assert harry.hearts == 7


def test_all_discard():
    crabbe_goyle = VillainCard('Crabbe & Goyle', 5, passive_action=Action(person='all', hearts=-1, passive='discard'), reward=Action(person='all', cards=1))
    game = GameState(['ron', 'neville'], 1)
    ron, neville = game.heroes

    input_values = [1, 1, 1]
    def mock_input(s):
        return input_values.pop(0)
    hero.input = mock_input
    discard_all_action = Action(person='all', discard=1)
    discard_active_action = Action(discard=1)

    crabbe_goyle.apply_passive(ron, game.heroes)
    assert ron.hearts == 10
    assert len(ron.hand) == 5
    assert neville.hearts == 10
    assert len(neville.hand) == 5

    discard_active_action.apply(ron, game)
    assert ron.hearts == 9
    assert len(ron.hand) == 4
    assert neville.hearts == 10
    assert len(neville.hand) == 5

    discard_all_action.apply(ron, game)
    assert ron.hearts == 8
    assert len(ron.hand) == 3
    assert neville.hearts == 9
    assert len(neville.hand) == 4
