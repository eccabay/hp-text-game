import getopt
import random
import time
import sys

from cards.hogwarts import hogwarts_deck
from cards.dark_arts import dark_arts_deck
from cards.villains import villain_deck
from cards import Hero, locations

class GameState:
    def __init__(self, players, game_number):
        self.turn = 0

        # Initialize players
        self.heroes = []
        for player in players:
            self.heroes.append(Hero(player.lower()))

        # Initialize locations
        self.locations = locations.get_requested_deck(game_number)
        self.current_location = self.locations.pop(0)

        # Initialize Dark Arts
        self.dark_arts_draw = dark_arts_deck.get_requested_deck(game_number)
        self.dark_arts_discard = []

        # Initialize Villains
        if game_number == 1 or game_number == 2:
            self.num_villains = 1
        else:
            raise ValueError('Game not supported yet')

        self.villain_deck = villain_deck.get_requested_deck(game_number)
        self.current_villains = {}
        for villain in range(self.num_villains):
            self.current_villains[int(villain+1)] = self.villain_deck.pop()

        # Initialize Hogwarts Cards
        self.hogwarts_cards = hogwarts_deck.get_requested_deck(game_number)
        self.store = []
        for i in range(6):
            self.store.append(self.hogwarts_cards.pop())

        self.game_over = False

    def print_state(self):
        print(f'Active hero: {self.get_active_hero().name}')

        print('\nLocation:')
        print(self.current_location)

        print('\nHeroes:')
        for hero in self.heroes:
            print(hero)
            print()

        print('\nVillains:')
        for villain_number in self.current_villains.keys():
            print(f'Villain {villain_number}:')
            print(self.current_villains[villain_number])

        print('\nAvailable Hogwarts Cards:')
        for hogwarts_card in self.store:
            print(hogwarts_card)

    def get_active_hero(self):
        hero_number = self.turn % len(self.heroes)
        return self.heroes[hero_number]

    def draw_dark_arts(self):
        # Conditional checks for villains first
        for villain in self.current_villains.values():
            villain.apply_passive(self.get_active_hero(), self.heroes)

        for i in range(self.current_location.dark_arts):
            
            # Reshuffle deck if necessary
            if len(self.dark_arts_draw) == 0:
                self.dark_arts_draw = self.dark_arts_discard
                self.dark_arts_discard = []
                random.shuffle(self.dark_arts_draw)

            dark_arts_card = self.dark_arts_draw.pop()
            dark_arts_card.apply(self.get_active_hero(), self)
            self.dark_arts_discard.append(dark_arts_card)

    def apply_villains(self):
        for villain in self.current_villains.values():
            villain.apply_for_each(self.get_active_hero())
            villain.apply_active(self.get_active_hero(), self)

    def play_turn(self):
        active_hero = self.get_active_hero()
        print(f'{active_hero.name}\'s turn')
        active_hero.play_turn(self)

    def new_hogwarts_card(self):
        new_card = self.hogwarts_cards.pop()
        self.store.append(new_card)
        print(f'New Hogwarts Card: {new_card}')

    def end_turn(self):
        # Replace any defeated villians
        for villian_number, villain in self.current_villains.items():
            if villain is None:
                if len(self.villain_deck) == 0:
                    print('You Win!')
                    self.game_over = True
                    return
                new_villain = self.villain_deck.pop()
                print(f'The new villian is {new_villain}\n')
                self.current_villains[int(villian_number)] = new_villain

        # Lose the location, if neccessary
        if self.current_location.current >= self.current_location.max:
            if len(self.locations) == 0:
                print('You Lose :(')
                self.game_over = True
                return
            new_location = self.locations.pop(0)
            print(f'The new location is {new_location}')
            self.current_location = new_location
        if self.current_location.current < 0:
            self.current_location.current = 0

        # Un-stun all heroes and reset passive actions
        for hero in self.heroes:
            hero.good_passive = {}
            hero.bad_passive = {}
            if hero.hearts <= 0:
                hero.hearts = 10
                hero.stunned = False
                print(f'Unstunned {hero.name}')

        # Active hero loses tokens and gets new hand
        active_hero = self.get_active_hero()
        active_hero.end_turn()

        # Increase turn number
        self.turn += 1

    def play_game(self):
        while not self.game_over:
            print('**************************************************')
            self.print_state()
            print('**************************************************\n')
            active_hero = self.get_active_hero()
            print(f'{active_hero.name} Hearts: {active_hero.hearts}   Influence: {active_hero.influence}   Attacks: {active_hero.attacks}\n')
            self.draw_dark_arts()
            print()
            self.apply_villains()
            print()
            self.play_turn()
            print()
            self.end_turn()
            print()
            time.sleep(5)


def main(argv):
    players = []
    game = 0

    try:
        opts, args = getopt.getopt(argv, "p:g:", ["players=", "game="])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-p', '--players'):
            arg = arg.split(' ')
            players = arg
        elif opt in ('-g', '--game'):
            game = int(arg)

    game = GameState(players, game)
    game.play_game()


if __name__ == '__main__':
    main(sys.argv[1:])