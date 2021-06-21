import random
random.seed(42)

from game import GameState
from utils import Action


def test_basic_rolling():
    gryffindor_action = Action(roll='gryffindor')
    hufflepuff_action = Action(roll='hufflepuff')
    ravenclaw_action = Action(roll='ravenclaw')
    slytherin_action = Action(roll='slytherin')

    game = GameState(['harry', 'ron', 'hermione', 'neville'], 1)
    for hero in game.heroes:
        hero.hearts = 5
        hero.influence = 1
    harry = game.get_active_hero()

    gryffindor_action.apply(harry, game)
    for hero in game.heroes:
        assert hero.hearts == 5
        assert hero.attacks == 0
        assert hero.influence == 2
        assert len(hero.hand) == 5
        
    hufflepuff_action.apply(harry, game)
    for hero in game.heroes:
        assert hero.hearts == 6
        assert hero.attacks == 0
        assert hero.influence == 2
        assert len(hero.hand) == 5

    ravenclaw_action.apply(harry, game)
    for hero in game.heroes:
        assert hero.hearts == 6
        assert hero.attacks == 1
        assert hero.influence == 2
        assert len(hero.hand) == 5

    slytherin_action.apply(harry, game)
    for hero in game.heroes:
        assert hero.hearts == 6
        assert hero.attacks == 2
        assert hero.influence == 2
        assert len(hero.hand) == 5


def test_neville_hufflepuff():
    hufflepuff_action = Action(roll='hufflepuff')

    game = GameState(['neville', 'harry', 'ron', 'hermione'], 3)
    for hero in game.heroes:
        hero.hearts = 5
    neville = game.get_active_hero()
    game.start_turn()

    hufflepuff_action.apply(neville, game)
    for hero in game.heroes:
        assert hero.hearts == 7
        assert hero.attacks == 0
        assert hero.influence == 0
        assert len(hero.hand) == 5


def test_heir_of_slytherin():
    heir_action = Action(roll='heir')
    game = GameState(['harry', 'ron', 'hermione', 'neville'], 1)
    game.current_villains[1].current = 2
    harry = game.get_active_hero()

    heir_action.apply(harry, game)  # Roll attack
    for hero in game.heroes:
        assert hero.hearts == 9
        assert len(hero.hand) == 5
    assert game.current_location.current == 0
    assert game.current_villains[1].current == 2

    heir_action.apply(harry, game)  # Roll heart/attack
    for hero in game.heroes:
        assert (hero.hearts == 9 or hero.hearts == 8)
        assert len(hero.hand) == 5
    assert game.current_location.current == 0
    assert (game.current_villains[1].current == 1 or game.current_villains[1].current == 2)

    heir_action.apply(harry, game)  # Roll influence/attacl
    for hero in game.heroes:
        assert (hero.hearts == 9 or hero.hearts == 7)
        assert len(hero.hand) == 5
    assert (game.current_location.current == 1 or game.current_location.current == 0)
    assert (game.current_villains[1].current == 1 or game.current_villains[1].current == 2)
