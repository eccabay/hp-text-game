from utils import actions, Action
from cards.dark_arts import DarkArtsCard
from cards.hogwarts import HogwartsCard
from game_state import GameState
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

    relashio.apply(ron, game.heroes, game.current_location)
    assert ron.hearts == 8
    assert neville.hearts == 10
    assert len(ron.hand) == 3
    assert len(neville.hand) == 2

    obliviate.apply(neville, game.heroes, game.current_location)
    assert ron.hearts == 8
    assert neville.hearts == 8
    assert len(ron.hand) == 2
    assert len(neville.hand) == 2

    poison.apply(neville, game.heroes, game.current_location)
    assert ron.hearts == 6
    assert neville.hearts == 8
    assert len(ron.hand) == 2
    assert len(neville.hand) == 1
