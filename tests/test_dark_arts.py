from utils import actions, Action, GameAction
from cards.dark_arts import DarkArtsCard
from cards.hogwarts import HogwartsCard
from game import GameState
from cards import hero

def test_discard_or_lose():
    game = GameState(['ron', 'neville'], 1)
    ron, neville = game.heroes

    action_input_values = ['hearts', 'discard', 'discard', 'hearts', 'hearts', 'discard']
    def mock_action_input(s):
        return action_input_values.pop(0)
    actions.input = mock_action_input

    hero_input_values = ['2', '1', '2']  # Neville discards a spell
    def mock_hero_input(s):
        return hero_input_values.pop(0)
    hero.input = mock_hero_input

    spell = HogwartsCard('Test Spell', 'spell')
    item = HogwartsCard('Test Item', 'item')
    ally = HogwartsCard('Test Ally', 'ally')

    ron.hand = [spell, item, ally]
    neville.hand = [spell, item, ally]

    relashio = DarkArtsCard('Relashio!', active=Action(person='all', hearts=-2, discard=1, discard_type='item', choice=True))
    obliviate = DarkArtsCard('Obliviate!', active=Action(person='all', hearts=-2, discard=1, discard_type='spell', choice=True))
    poison = DarkArtsCard('Poison', active=Action(person='all', hearts=-2, discard=1, discard_type='ally', choice=True))

    relashio.apply(ron, game)
    assert ron.hearts == 8
    assert neville.hearts == 10
    assert len(ron.hand) == 3
    assert len(neville.hand) == 2

    obliviate.apply(neville, game)
    assert ron.hearts == 8
    assert neville.hearts == 8
    assert len(ron.hand) == 2
    assert len(neville.hand) == 2

    poison.apply(neville, game)
    assert ron.hearts == 6
    assert neville.hearts == 8
    assert len(ron.hand) == 2
    assert len(neville.hand) == 1


def test_petrification():
    game = GameState(['harry'], 1)
    petrification = DarkArtsCard('Petrification', active=Action(person='all', hearts=-1), passive=Action(person='all', passive='draw'))
    draw_card = HogwartsCard('test card', 'item', regular=Action(cards=1))
    
    harry = game.get_active_hero()
    harry.hand = [draw_card]

    petrification.apply(harry, game)
    assert harry.hearts == 9

    assert len(harry.hand) == 1
    harry.process_input(1, game)
    assert len(harry.hand) == 0


def test_tarantallegra():
    game = GameState(['harry'], 1)
    tarantallegra = DarkArtsCard('Tarantallegra', active=[Action(hearts=-1), GameAction(limit=True)])
    harry = game.get_active_hero()
    harry.attacks = 2
    villain = game.current_villains[1]

    assert not villain.limited
    tarantallegra.apply(harry, game)
    assert harry.hearts == 9
    assert villain.limited

    hero_input_values = ['2']
    def mock_hero_input(s):
        return hero_input_values.pop(0)
    hero.input = mock_hero_input

    harry.attack_villain(game)
    assert villain.current == 1

    game.end_turn()
    assert not villain.limited
