from utils import actions, Action
from game import GameState
from cards.hogwarts import HogwartsCard
from cards.heroes import hero


def get_test_game():
    return GameState(['harry', 'ron', 'hermione', 'neville'], 3)


def test_abilities_enacted():
    game = get_test_game()

    game.start_turn()  # Start harry's turn
    for hero in game.heroes:
        assert 'metal' in hero.good_passive
    game.end_turn()

    game.start_turn()  # Ron's turn
    hero = game.get_active_hero()
    assert 'attacks' in hero.good_passive
    for hero in game.heroes:
        assert 'metal' in hero.good_passive
    game.end_turn()

    game.start_turn()  # Hermione's turn
    hero = game.get_active_hero()
    assert 'spell' in hero.good_passive
    for hero in game.heroes:
        assert 'metal' in hero.good_passive
    game.end_turn()

    game.start_turn()  # Neville's turn
    for hero in game.heroes:
        assert 'metal' in hero.good_passive
        assert 'hearts' in hero.good_passive
        assert not 'spell' in hero.good_passive
        assert not 'attacks' in hero.good_passive
    game.end_turn()

    game.start_turn()  # Harry's turn again
    for hero in game.heroes:
        assert 'metal' in hero.good_passive
        assert not 'hearts' in hero.good_passive


def test_harry_ability():
    game = get_test_game()
    metal_action = Action(metal=-1)

    input_values = ['harry', 'neville']
    def mock_input(s):
        return input_values.pop(0)
    actions.input = mock_input

    game.start_turn()  # Harry's turn
    harry = game.get_active_hero()
    metal_action.apply(harry, game)
    assert harry.attacks == 1
    metal_action.apply(harry, game)  # Should not apply if used again on the same turn
    assert harry.attacks == 1
    game.end_turn()

    game.start_turn()  # Ron's turn
    neville = game.get_hero('neville')
    ron = game.get_active_hero()
    assert 'metal' in ron.good_passive
    metal_action.apply(ron, game)
    assert ron.attacks == 0
    assert neville.attacks == 1


def test_ron_ability_oneshot():
    game = GameState(['ron', 'hermione', 'neville'], 3)

    ron = game.get_active_hero()
    ron.attacks = 4
    hermione = game.get_hero('hermione')
    ron.hearts = 8
    hermione.hearts = 5

    game.start_turn()

    hero_input_values = [1, 3, 1, 1]
    def hero_mock_input(s):
        return hero_input_values.pop(0)
    hero.input = hero_mock_input

    action_input_values = ['hermione']
    def action_mock_input(s):
        return action_input_values.pop(0)
    actions.input = action_mock_input

    assert 'attacks' in ron.good_passive
    ron.attack_villain(game)
    assert ron.hearts == 8
    assert hermione.hearts == 7

    ron.attack_villain(game)  # Should not apply if used again on the same turn
    assert ron.hearts == 8
    assert hermione.hearts == 7


def test_ron_ability_multiple():
    game = GameState(['ron', 'hermione', 'neville'], 3)

    ron = game.get_active_hero()
    ron.attacks = 3
    hermione = game.get_hero('hermione')
    ron.hearts = 8
    hermione.hearts = 5

    game.start_turn()

    hero_input_values = [1, 2, 2, 1]
    def hero_mock_input(s):
        return hero_input_values.pop(0)
    hero.input = hero_mock_input

    action_input_values = ['hermione']
    def action_mock_input(s):
        return action_input_values.pop(0)
    actions.input = action_mock_input

    ron.attack_villain(game)  # Should not apply yet, minimum criteria hasn't been hit
    assert ron.hearts == 8
    assert hermione.hearts == 5

    ron.attack_villain(game)  # Now should apply
    assert ron.hearts == 8
    assert hermione.hearts == 7


def test_hermione_ability():
    game = GameState(['hermione', 'neville'], 3)

    hermione = game.get_active_hero()
    test_spell = HogwartsCard('Test Spell', 'spell')
    test_item = HogwartsCard('Test Item', 'item')

    game.start_turn()

    action_input_values = ['hermione']
    def action_mock_input(s):
        return action_input_values.pop(0)
    actions.input = action_mock_input

    # Play three spells
    test_spell.play(hermione, game)
    test_spell.play(hermione, game)
    test_spell.play(hermione, game)
    assert hermione.influence == 0

    # Playing a non-spell should not trigger the fourth
    test_item.play(hermione, game)
    assert hermione.influence == 0

    # Fourth spell should trigger ability
    test_spell.play(hermione, game)
    assert hermione.influence == 1


def test_neville_ability():
    game = GameState(['neville', 'ron', 'hermione'], 3)
    neville = game.get_active_hero()
    ron = game.get_hero('ron')
    hermione = game.get_hero('hermione')

    neville.hearts = 3
    ron.hearts = 5
    hermione.hearts = 6

    game.start_turn()

    heart_neville = Action(hearts=1)
    heart_all = Action(person='all', hearts=2)

    heart_neville.apply(neville, game)
    assert neville.hearts == 5
    assert ron.hearts == 5
    assert hermione.hearts == 6

    assert neville.good_passive['hearts'].completed == True
    assert ron.good_passive['hearts'].completed == False
    assert hermione.good_passive['hearts'].completed == False

    heart_all.apply(neville, game)
    assert neville.hearts == 7
    assert ron.hearts == 8
    assert hermione.hearts == 9