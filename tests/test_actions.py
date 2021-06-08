from cards.villains.villain_card import VillainCard
from cards.hogwarts.hogwarts_card import HogwartsCard
from game import GameState
from utils import actions, Action, GameAction
from cards import hero, Hero, Location


def get_test_hero():
    return Hero('ron')

def get_test_heroes():
    return [Hero('harry'), Hero('ron'), Hero('hermione'), Hero('neville')]

def get_test_game():
    return GameState(['harry', 'ron', 'hermione', 'neville'], 1)


def test_active_single_simple_action():
    test_hero = get_test_hero()
    test_hero.hearts = 5

    heart_action = Action('active', hearts=2)
    attack_action = Action('active', attacks=1)
    influence_action = Action('active', influence=3)
    cards_action = Action('active', cards=2)

    assert test_hero.hearts == len(test_hero.hand) == 5
    assert test_hero.influence == test_hero.attacks == 0

    heart_action.apply(test_hero)
    assert test_hero.hearts == 7
    assert test_hero.influence == test_hero.attacks == 0

    attack_action.apply(test_hero)
    assert test_hero.attacks == 1

    influence_action.apply(test_hero)
    assert test_hero.influence == 3

    cards_action.apply(test_hero)
    assert len(test_hero.hand) == 7

    heart_action.apply(test_hero)
    assert test_hero.hearts == 9
    assert test_hero.attacks == 1
    assert test_hero.influence == 3
    assert len(test_hero.hand) == 7


def test_all_single_simple_action():
    game = get_test_game()
    harry, ron, hermione, neville = game.heroes
    harry.hearts = 5
    ron.attacks = 2
    hermione.influence = 3
    neville.draw_card()

    heart_action = Action('all', hearts=2)
    attack_action = Action('all', attacks=1)
    influence_action = Action('all', influence=3)
    cards_action = Action('all', cards=2)

    heart_action.apply(ron, game)
    assert harry.hearts == 7
    assert hermione.hearts == ron.hearts == neville.hearts == 10

    attack_action.apply(hermione, game)
    assert ron.attacks == 3
    assert harry.attacks == hermione.attacks == neville.attacks == 1

    influence_action.apply(neville, game)
    assert hermione.influence == 6
    assert harry.influence == ron.influence == neville.influence == 3

    cards_action.apply(harry, game)
    assert len(neville.hand) == 8
    assert len(harry.hand) == len(ron.hand) == len(hermione.hand) == 7


def test_any_single_simple_action():
    test_hero = get_test_hero()
    other_hero = Hero('harry')
    other_hero.hearts = 1
    other_hero.influence = 2

    heart_action = Action('any', hearts=2)
    attack_action = Action('any', attacks=1)
    influence_action = Action('any', influence=3)
    cards_action = Action('any', cards=2)

    input_values = ['harry', 'ron', 'ron', 'harry']
    def mock_input(s):
        return input_values.pop(0)
    actions.input = mock_input

    game = GameState(players=['ron', 'harry'], game_number=1)
    game.heroes = [test_hero, other_hero]
    
    heart_action.apply(test_hero, game)
    assert test_hero.hearts == 10
    assert other_hero.hearts == 3

    attack_action.apply(test_hero, game)
    assert test_hero.attacks == 1
    assert other_hero.attacks == 0

    influence_action.apply(test_hero, game)
    assert test_hero.influence == 3
    assert other_hero.influence == 2

    cards_action.apply(test_hero, game)
    assert len(test_hero.hand) == 5
    assert len(other_hero.hand) == 7


def test_active_remove_metal():
    game = get_test_game()
    test_hero = game.get_active_hero()
    location = game.current_location
    location.current = 3

    action = Action(metal=-1)
    action.apply(test_hero, game)
    assert location.current == 2
    action.apply(test_hero, game)
    assert location.current == 1    


def test_active_cards_on_top():
    test_hero = get_test_hero()
    test_hero.influence = 14

    game = get_test_game()
    spell_card = HogwartsCard('Test Spell', 'spell', 1)
    item_card = HogwartsCard('Test Item', 'item', 5)
    ally_card = HogwartsCard('Test Ally', 'item', 4)
    game.store = [ally_card, spell_card, item_card, ally_card]

    top_spell_action = Action(cards_on_top='spell')
    top_item_action = Action(cards_on_top='item')
    top_ally_action = Action(cards_on_top='ally')

    input_values = [1, 1, 1, 1]
    def mock_input(s):
        return input_values.pop(0)
    hero.input = mock_input

    top_spell_action.apply(test_hero)
    assert test_hero.cards_on_top == ['spell']
    test_hero.buy_card(game)  # Buy an ally, goes in discard pile
    assert len(test_hero.discard) == 1
    test_hero.buy_card(game)  # Buy a spell, goes in deck
    assert len(test_hero.discard) == 1
    assert len(test_hero.deck) == 6
    assert test_hero.deck[-1].name == 'Test Spell'

    top_item_action.apply(test_hero)
    assert test_hero.cards_on_top == ['spell', 'item']
    test_hero.buy_card(game)
    assert len(test_hero.discard) == 1
    assert len(test_hero.deck) == 7
    assert test_hero.deck[-1].name == 'Test Item'
    
    top_ally_action.apply(test_hero)
    assert test_hero.cards_on_top == ['spell', 'item', 'ally']
    test_hero.buy_card(game)
    assert len(test_hero.discard) == 1
    assert len(test_hero.deck) == 8
    assert test_hero.deck[-1].name == 'Test Ally'


def test_copy_action():
    game = get_test_game()
    ginny = HogwartsCard('Ginny Weasley', 'ally', cost=4, regular=Action(attacks=1, influence=1))
    copy_action = Action(copy='ally')

    harry = game.get_active_hero()

    input_values = [1]
    def mock_input(s):
        return input_values.pop(0)
    actions.input = mock_input

    # Apply action with no allies - nothing changes
    copy_action.apply(harry, game=game)
    assert harry.influence == 0
    assert harry.attacks == 0

    # Apply action with ally in play pile - card is played
    harry.played = [ginny]
    copy_action.apply(harry, game=game)
    assert harry.influence == 1
    assert harry.attacks == 1


def test_search_action():
    game = get_test_game()
    ginny = HogwartsCard('Ginny Weasley', 'ally', cost=4, regular=Action(attacks=1, influence=1))
    test_spell = HogwartsCard('Test Spell', 'spell')
    search_action = Action(search='ally')

    harry = game.get_active_hero()
    harry.discard = [test_spell]

    input_values = [1]
    def mock_input(s):
        return input_values.pop(0)
    actions.input = mock_input

    # Apply action with no allies in discard - nothing changes
    search_action.apply(harry, game=game)
    assert len(harry.hand) == 5

    # Apply action with ally in play pile - card is played
    harry.discard.append(ginny)
    search_action.apply(harry, game=game)
    assert len(harry.hand) == 6


def test_choice_of_search():
    game = GameState(['ron'], 1)
    search_action = Action(influence=1, search='spell', choice=True)

    test_spell = HogwartsCard('Test Spell', 'spell')
    ron = game.get_active_hero()
    ron.discard = [test_spell]

    input_values = ['search', 1]
    def mock_input(s):
        return input_values.pop(0)
    actions.input = mock_input

    search_action.apply(ron, game)
    assert ron.influence == 0
    assert len(ron.hand) == 6


def test_discard_type_not_allowed():
    action = Action(hearts=-2, discard=1, discard_type='spell', choice=True)
    ron = Hero('ron')
    test_item = HogwartsCard('Test Item', 'item')
    ron.hand = [test_item, test_item, test_item]

    input_values = ['discard', 'hearts']
    def mock_input(s):
        return input_values.pop(0)
    actions.input = mock_input

    action.apply(ron)
    assert ron.hearts == 8
    assert len(ron.hand) == 3


def test_polyjuice_with_bertie():
    game = get_test_game()

    beans = HogwartsCard('Bertie Botts Every-Flavour Beans', 'item', regular=Action(influence=1), other=Action(attacks=1, passive='ally'))
    polyjuice = HogwartsCard('Polyjuice Potion', 'item', cost=3, regular=Action(copy='ally'))
    ally = HogwartsCard('Pigwidgeon', 'ally', regular=Action(hearts=1))

    input_values = [1]
    def mock_input(s):
        return input_values.pop(0)
    actions.input = mock_input

    harry = game.get_active_hero()
    harry.hand = [beans, ally, polyjuice]
    harry.hearts = 5

    harry.process_input(1, game)  # Play beans
    assert harry.influence == 1
    assert harry.attacks == 0
    assert harry.hearts == 5

    harry.process_input(1, game)  # Play the ally
    assert harry.influence == 1
    assert harry.attacks == 1
    assert harry.hearts == 6

    harry.process_input(1, game)
    assert harry.influence == 1
    assert harry.attacks == 1
    assert harry.hearts == 7


def test_game_action():
    game = get_test_game()
    game.current_villains[1].current = 3

    harry = game.get_active_hero()
    harry.attacks = 2

    action = GameAction(attacks=-1)
    action.apply(harry, game=game)

    assert game.current_villains[1].current == 2
    assert harry.attacks == 2


def test_mute_action():
    mute_action = GameAction(mute=True)
    game = GameState(['harry', 'ron'], 1)
    harry, ron = game.heroes
    villain = VillainCard('Test Villain', 4, active_action=Action(hearts=-1), passive_action=Action(hearts=-2, passive='metal'), reward=Action(hearts=3))
    game.current_villains[1] = villain

    input_values = [1]
    def mock_input(s):
        return input_values.pop(0)
    actions.input = mock_input

    game.apply_villains()
    villain.apply_passive(harry, game.heroes)
    assert 'metal' in harry.bad_passive
    assert harry.hearts == 9
    assert ron.hearts == 10

    mute_action.apply(harry, game)
    assert 'metal' not in harry.bad_passive
    assert villain.muted == 'harry'

    game.end_turn()  # End harry's turn
    assert villain.muted == 'harry'

    game.apply_villains()
    villain.apply_passive(ron, game.heroes)
    assert 'metal' not in ron.bad_passive
    assert harry.hearts == 9
    assert ron.hearts == 10
    game.end_turn()  # End ron's turn
    assert villain.muted == 'harry'

    game.draw_dark_arts()
    assert villain.muted is None


def test_reveal_action():
    game = get_test_game()
    reveal_action = Action(reveal='value', metal=1)

    test_novalue = HogwartsCard('Test No Value', 'spell')
    test_value = HogwartsCard('Test Value', 'spell', cost=3)

    harry = game.get_active_hero()
    harry.deck = [test_novalue, test_value]
    assert game.current_location.current == 0

    reveal_action.apply(harry, game)  # Reveal card with value
    assert len(harry.deck) == 1
    assert len(harry.discard) == 1
    assert game.current_location.current == 1

    reveal_action.apply(harry, game)  # Reveal card with no value
    assert len(harry.deck) == 1
    assert len(harry.discard) == 1
    assert game.current_location.current == 1
