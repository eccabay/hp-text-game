import random
import math

from cards.hogwarts import hogwarts_deck

class Hero:
    def __init__(self, name):
        self.name = name

        self.hearts = 10
        self.influence = 0
        self.attacks = 0
        self.stunned = False
        self.cards_on_top = []
        self.good_passive = {}
        self.bad_passive = {}
        self.end = False
        self.cloaked = False

        # Get starting deck
        if name == 'harry':
            self.deck = hogwarts_deck.get_harry_starting_cards()
        elif name == 'ron': 
            self.deck = hogwarts_deck.get_ron_starting_cards()
        elif name == 'hermione':
            self.deck = hogwarts_deck.get_hermione_starting_cards()
        else:
            self.deck = hogwarts_deck.get_neville_starting_cards()
        random.shuffle(self.deck)

        self.discard = []
        self.hand = []
        for i in range(5):
            self.draw_card(new_turn=True)
        self.played = []

    def __str__(self):
        text = f'{self.name}   Hearts: {self.hearts}   Influence: {self.influence}   Attacks: {self.attacks}'
        if self.stunned:
            text = text + '  STUNNED'
        if self.cloaked:
            text = text + '  CLOAKED'
        if len(self.good_passive) > 0:
            text = text + '\nPositive passive effects: ' 
            for reason, action in self.good_passive.items():
                text = text + f'{reason}: {action}, '
        if len(self.bad_passive) > 0:
            text = text + '\nNegative passive effects: ' 
            for reason, action in self.bad_passive.items():
                text = text + f'{reason}: {action}, '
        if len(self.cards_on_top) > 0:
            text = text + f'\nCards of type(s) {self.cards_on_top} go on top of deck'
        text = text + '\nCards in hand:'
        for card in self.hand:
            text = text + '\n' + str(card)
        return text

    def correct_hearts(self):
        if self.hearts > 10:
            self.hearts = 10
        if self.hearts < 0:
            self.hearts = 0

    def stun(self, all_heroes, current_location):
        if self.hearts <= 0 and not self.stunned:
            self.stunned = True
            current_location.current += 1
            cards_to_discard = math.floor(len(self.deck)/2)
            print(f'Stunned! Current location has {current_location.current} metal. Discard {cards_to_discard} cards')
            for card in range(cards_to_discard):
                self.prompt_discard(all_heroes)

    def prompt_discard(self, all_heroes, discard_type):
        print('Cards:')
        for i, card in enumerate(self.hand):
            print(f'{i+1} {card.get_information()}')
        discard_index = input('Choose a card to discard: ')

        # Try to discard, if the input is invalid just retry
        try:
            discarded = self.hand[int(discard_index)-1]
            if discard_type != 'any':
                if discarded.type != discard_type:
                    print(f'Card {discarded.name} is not of type {discard_type}. Try again')
                    self.prompt_discard(all_heroes, discard_type)
                    return
        except (IndexError, ValueError):
            print(f'Index {discard_index} is not valid')
            self.prompt_discard(all_heroes, discard_type)
            return
        
        discarded = self.hand.pop(int(discard_index)-1)

        # Apply any discarding bonus
        if discarded.discard is not None:
            discarded.discard.apply(self, all_heroes=all_heroes)
        # Place the card in the discard pile
        self.discard.append(discarded)

    def check_bad_condition(self, condition, current_location):
        if condition in self.bad_passive:
            self.bad_passive[condition].apply(self, current_location=current_location)

    def draw_card(self, new_turn=False):
        if 'draw' in self.bad_passive:
            print('Cannot draw cards this turn')
            return 0
        if len(self.deck) == 0:
            self.deck = self.discard
            self.discard = []
            random.shuffle(self.deck)
        new_card = self.deck.pop()
        if new_card.name == 'Invisibility Cloak':
            self.cloaked = True
        self.hand.append(new_card)
        if not new_turn:
            print(f'{self.name} drew card: {new_card.get_information()}')

    def process_input(self, move, game):
        print()
        # End turn
        if move == 'end':
            self.end = True
            return

        # Various status checks
        if move == 'status':
            print(self)
            return
        if move == 'game status' or move == 'game':
            game.print_state()
            return
        if move == 'location status' or move == 'location':
            print(game.current_location)
            return
        if move == 'hero status' or move == 'heroes':
            for hero in game.heroes:
                print(f'{hero.name}   Hearts: {hero.hearts}   Influence: {hero.influence}   Attacks: {hero.attacks}')
            return

        # Buy a card
        if move == 'buy' or move == 'b':
            self.buy_card(game)
            return

        # Attack a villain
        if move == 'attack' or move == 'a':
            self.attack_villain(game)
            return

        # Play a card
        try:
            card_index = int(move)
        except ValueError:
            print(f'Invalid input of {move}. Please try again')
            self.play_turn(game)
            return
        try:
            card = self.hand.pop(card_index-1)
        except IndexError:
            print(f'Index {card_index} is not valid. Please try again')
            self.play_turn(game)
            return
        card.play(self, game)
        self.played.append(card)
        self.correct_hearts()
        print(f'Hearts: {self.hearts}   Influence: {self.influence}   Attacks: {self.attacks}')

    def play_turn(self, game):
        print(f'\nHearts: {self.hearts}   Influence: {self.influence}   Attacks: {self.attacks}')

        while len(self.hand) > 0:

            # Show options
            print('Cards:')
            for i, card in enumerate(self.hand):
                print(f'{i+1} {card.get_information()}')
            move = input('Buy a card, attack a villain, or choose a card to play: ')
            self.process_input(move, game)

        # Leave room at the end to play things
        if self.influence > 0 or self.attacks > 0:
            while not self.end and (self.influence > 0 or self.attacks > 0):
                if len(self.hand) == 0:
                    move = input('Would you like to buy a card or attack a villain? ')
                else:
                    move = input('Buy a card, attack a villain, or choose a card to play: ')
                self.process_input(move, game)

        if len(self.hand) > 0:
            self.play_turn(game)

    def buy_card(self, game):
        # Preliminary checks and information display
        if self.influence <= 0:
            print('You have no influence, you cannot buy cards right now')
            return
        print(f'You have {self.influence} influence')
        print('Available Hogwarts Cards:')
        for i, hogwarts_card in enumerate(game.store):
            print(i+1, hogwarts_card.get_information())

        try:
            card_index = int(input('Which card would you like to buy? '))-1
        except ValueError:
            print(f'Card does not exist. Try again')
            self.buy_card(game)
            return
            
        # Check to make sure you can afford the card, and that it exists
        try:
            card = game.store[card_index]
            if card.cost > self.influence:
                print('You cannot afford this card. Try again')
                self.play_turn(game)
                return
        except IndexError:
            print(f'Card index {card_index} does not exist. Try again')
            self.buy_card(game)
            return

        card = game.store.pop(card_index)
        self.influence -= card.cost
        print(f'\nYou bought {card.name}. You now have {self.influence} influence')
        game.new_hogwarts_card()

        if len(self.cards_on_top) > 0:
            for hero_card_type in self.cards_on_top:
                if hero_card_type == card.type:
                    self.deck.append(card)
                    return
        self.discard.append(card)

    def attack_villain(self, game):
        if self.attacks <= 0:
            print('You have no attacks, you cannot attack villains right now')
            return

        # Choose a villain to attack, and make sure the villain exists
        for villain_number, villain in game.current_villains.items():
            print(f'{villain_number} - {villain.name} ({villain.current}/{villain.strength})')
        villain_index = input('Who would you like to attack? ')
        try:
            villain = game.current_villains[int(villain_index)]
        except (IndexError, ValueError):
            print('Invalid villain selection. Try again')
            self.attack_villain(game)
            return

        # Select the number of attacks to assign, and make sure the input is correct
        try:
            num_attacks = int(input(f'You have {self.attacks} attacks. How many would you like to use? '))
            if num_attacks > self.attacks:
                print('You cannot play that many attacks. Try again')
                self.attack_villain(game)
                return
        except ValueError:
            print('That is not an integer number of attacks. Try again')
            self.attack_villain(game)
            return

        # Attack the villain
        self.attacks -= num_attacks
        villain.attack(num_attacks, game, villain_index)
        print(f'You now have {self.attacks} attacks')

    def end_turn(self):
        self.cloaked = False
        self.end = False
        self.cards_on_top = []
        self.good_passive = {}
        self.bad_passive = {}
        self.discard += self.played
        self.played = []

        self.influence = 0
        self.attacks = 0
        for i in range(5):
            self.draw_card(new_turn=True)

        print(f'{self.name}\'s turn is over. New cards:')
        for card in self.hand:
            print(card)
