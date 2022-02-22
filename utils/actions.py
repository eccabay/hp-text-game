import random

from utils import gryffindor, hufflepuff, ravenclaw, slytherin

class Action:
    def __init__(self, person='active', hearts=0, attacks=0, influence=0, cards=0, discard=0, discard_type='any', metal=0, roll=None,
                 cards_on_top=None, copy=None, search=None, passive=False, choice=False, reveal=None, trigger_amt=None, **kwargs):
        self.person = person  # One of {'active', 'any', 'all'}
        self.hearts = hearts
        self.attacks = attacks
        self.influence = influence
        self.cards = cards
        self.discard = discard
        self.discard_type = discard_type
        self.metal = metal
        self.roll = roll
        self.cards_on_top = cards_on_top  # One of {'spell', 'item', 'ally'}
        self.copy = copy
        self.search = search
        self.passive = passive
        self.choice = choice
        self.reveal = reveal
        self.trigger = [trigger_amt, 0] if trigger_amt is not None else None
        self.kwargs = kwargs

    def get_information(self):
        if self.person != 'active':
            text = f'{self.person} hero: '
        else:
            text = f'hero: '

        if self.reveal is not None:
            text = text + f'Reveal top card of deck, if {self.reveal}: '
        if self.hearts != 0:
            text = text + f'Hearts: {self.hearts} || '
        if self.attacks != 0:
            text = text + f'Attacks: {self.attacks} || '
        if self.influence != 0:
            text = text + f'Influence: {self.influence} || '
        if self.cards != 0:
            text = text + f'Cards: {self.cards} || '
        if self.discard != 0:
            text = text + f'Discard {self.discard} card(s) of type {self.discard_type} || '
        if self.metal != 0:
            text = text + f'Metal: {self.metal} || '
        if self.roll is not None:
            text = text + f'Roll {self.roll} die || '
        if self.cards_on_top is not None:
            text = text + f'{self.cards_on_top} cards purchased can go on top of deck || '
        if self.copy is not None:
            text = text + f'Copy the effects of a {self.copy} played this turn || '
        if self.search is not None:
            text = text + f'Search discard pile for a {self.search} || '
        if self.passive:
            text = text + f'for each {self.passive} || '
        if self.choice:
            text = text + '(choose one)'
        return text

    def __str__(self):
        return self.get_information()

    def apply(self, active_hero, game=None):
        if game is not None:
            all_heroes = game.heroes
            current_location = game.current_location
        else:
            all_heroes = None
            current_location = None

        # Determine who this action applies to
        hero_list = []
        if self.person == 'active':
            hero_list = [active_hero]
        elif self.person == 'any':
            hero_name = input(f'Who would you like to apply {self} to? ')
            for hero in all_heroes:
                if hero_name == hero.name:
                    hero_list = [hero]
                    break
            if len(hero_list) == 0:
                print('That person does not exist. Try again')
                self.apply(active_hero, game)
                return
        else:
            hero_list = all_heroes

        # Adding/removing metal doesn't depend on the number of heroes
        if current_location is not None and self.reveal is None:
            if self.metal < 0 and 'metal' in active_hero.good_passive and current_location.current > 0 and 'no metal' not in active_hero.bad_passive:
                active_hero.good_passive['metal'].check(active_hero, 'metal', game)
            
            current_location.current += self.metal
            current_location.current = max(current_location.current, 0)
            current_location.current = min(current_location.current, current_location.max)
        if self.metal < 0 and 'no metal' in active_hero.bad_passive:
            print('Cannot remove metal this turn')

        # Apply the action
        for hero in hero_list:

            # Check for a Weasley in other hands
            if 'weasley' in self.kwargs:
                cont = False
                for other_hero in all_heroes:
                    if other_hero.name != active_hero.name and other_hero.has_weasley():
                        cont = True
                        print(f'{other_hero.name} has a Weasley! Applying bonus.')
                        break
                if not cont:
                    print('No other hero has a Weasley in hand.')
                    return

            if self.choice:
                self.handle_choice(hero, game)
                continue

            # Passive action
            if self.passive:
                if self.passive == 'draw':
                    hero.bad_passive['draw'] = None
                elif self.passive == 'stun':
                    hero.bad_passive['stun'] = 1
                else:
                    hero.good_passive[self.passive] = Action(person=self.person, hearts=self.hearts, attacks=self.attacks, influence=self.influence, discard_type=self.discard_type, trigger_amt=self.trigger[0])
                continue

            # Reveal top card
            if self.reveal is not None:
                if len(hero.deck) == 0:
                    hero.deck = hero.discard
                    hero.discard = []
                    random.shuffle(hero.deck)
                top_card = hero.deck[-1]
                print(f'{hero.name} top card of deck: {top_card}')
                if self.reveal == 'value':
                    if top_card.cost > 0:  # If it satisfies the condition, execute the rest of the action
                        top_card = hero.deck.pop()
                        if top_card.discard is not None:
                            top_card.discard.apply(hero, game)
                        hero.discard.append(top_card)
                        if current_location is not None:
                            current_location.current += self.metal
                            current_location.current = min(current_location.current, current_location.max)
                        print('Discarded card')
                    else:
                        print('Safe!')
                        continue  # If it doesn't, continue to the next hero
                else:  # Should be one of {ally, item, spell}
                    if top_card.type == self.reveal:
                        top_card = hero.deck.pop()
                        hero.discard.append(top_card)
                        if current_location is not None:
                            current_location.current += self.metal
                        print('Discarded card')
                    else:
                        print('Safe!')
                        continue

            # Active action
            if self.hearts < 0 and hero.cloaked:
                hero.hearts -= 1
            elif not hero.stunned:
                hero.hearts += self.hearts
                if self.hearts > 0 and 'hearts' in hero.good_passive:
                    hero.good_passive['hearts'].check(hero, 'hearts', game)

            hero.stun(game)
            hero.correct_hearts()
            hero.attacks += self.attacks
            hero.influence += self.influence
            if self.cards > 0:
                for i in range(self.cards):
                    hero.draw_card()
            if self.discard > 0:
                hero.prompt_discard(game, self.discard_type)
                hero.check_bad_condition('discard', game)
            if self.metal > 0:
                hero.check_bad_condition('metal', game)
            if self.cards_on_top is not None:
                hero.cards_on_top.append(self.cards_on_top)

            if self.roll is not None:
                self.roll_die(hero, game)

            # Polyjuice Potion
            if self.copy is not None:
                copy_card = self.select_card(hero, hero.played, self.copy)
                if copy_card is not False:
                    copy_card.play(hero, game, retry=True)  # Retry true to prevent bertie botts from triggering

            # Searching the discard pile
            if self.search is not None:
                pull_card = self.select_card(hero, hero.discard, self.search)
                if pull_card is not False:
                    hero.hand.append(pull_card)

            # Anything else:
            if 'silencio' in self.kwargs:
                game.silencio = True

    def handle_choice(self, hero, game):
        options = {}
        if self.hearts != 0:
            options['hearts'] = self.hearts
        if self.attacks != 0:
            options['attacks'] = self.attacks
        if self.influence != 0:
            options['influence'] = self.influence
        if self.cards != 0:
            options['cards'] = self.cards
        if self.discard != 0:
            options['discard'] = self.discard
        if self.search is not None:
            options['search'] = self.search
        if self.metal != 0:
            options['metal'] = self.metal

        choice = input(f'{hero.name}, choose either of {options}: ')
        if choice == 'hearts' or choice =='h':
            if self.hearts < 0 and hero.cloaked:
                hero.hearts -= 1
            elif not hero.stunned:
                hero.hearts += self.hearts
                if self.hearts > 0 and 'hearts' in hero.good_passive:
                    hero.good_passive['hearts'].check(hero, 'hearts', game)
            hero.stun(game)
        elif choice == 'attacks' or choice == 'a':
            hero.attacks += self.attacks
        elif choice == 'influence' or choice == 'i':
            hero.influence += self.influence
        elif choice == 'cards' or choice == 'c':
            for i in range(self.cards):
                hero.draw_card()
        elif choice == 'discard' or choice == 'd':
            # Check to make sure you have the right type of card to discard
            if self.discard_type != 'any':
                card_types = set()
                for card in hero.hand:
                    card_types.add(card.type)
                if self.discard_type not in card_types:
                    print(f'You do not have any cards of type {self.discard_type} to discard. Try again')
                    self.handle_choice(hero, game)
                    return
            # Discard the correct number of cards
            for i in range(self.discard):
                hero.prompt_discard(game, self.discard_type)
                hero.check_bad_condition('discard', game)
        elif choice == 'search' or choice == 's':
            pull_card = self.select_card(hero, hero.discard, self.search)
            if pull_card is False:
                self.handle_choice(hero, game)
                return
            if pull_card is not None:
                hero.hand.append(pull_card)
        elif choice == 'metal' or 'm':
            loc = game.current_location
            loc.current += self.metal
            loc.current = max(loc.current, 0)
            loc.current = min(loc.current, loc.max)
        else:
            print(f'Choice of {choice} is invalid. Try again')
            self.handle_choice(hero, game)
            return

    def select_card(self, hero, search_pile, card_type, pop=False):
        available_cards = []
        for card in search_pile:
            if card.type == card_type:
                available_cards.append(card)
        if len(available_cards) == 0:
            print(f'No cards of type {card_type} available')
            return False
        # Pick which card to copy/pull back
        for i, card in enumerate(available_cards):
            print(i+1, card)
        choice = input(f'{hero.name}, choose a {card_type} ')
        try:
            choice = int(choice)-1
            card_choice = available_cards[choice]
            if pop:
                card_choice = available_cards.pop(choice)
        except (ValueError, IndexError):
            print(f'Invalid choice of {choice}, try again')
            self.select_card(hero, search_pile, card_type, pop)
            return
        return card_choice

    def roll_die(self, hero, game):

        # Heir of Slytherin
        if self.roll == 'heir':
            result = slytherin.roll()
            if result == 'influence':
                print('Added 1 metal to the location')
                action = Action(metal=1)
            elif result == 'heart':
                print('Removed an attack from all villains')
                action = GameAction(attacks=-1)
            elif result == 'card':
                print('All heroes discard a card')
                action = Action(person='all', discard=1)
            else:
                print('All heroes lose a heart')
                action = Action(person='all', hearts=-1)
            action.apply(hero, game)
            return

        # Choose which die to roll
        if self.roll == 'any':
            options = ['gryffindor', 'hufflepuff', 'ravenclaw', 'slytherin']
            die_name = input('Which die would you like to roll? ')
            if die_name not in options:
                print('Unknown die choice, try again')
                self.roll_die(hero, game)
                return
        else:
            die_name = self.roll
        die = eval(die_name)

        # Roll the die
        result = die.roll()
        if result == 'influence':
            action = Action(person='all', influence=1)
        elif result == 'heart':
            action = Action(person='all', hearts=1)
        elif result == 'card':
            action = Action(person='all', cards=1)
        else:
            action = Action(person='all', attacks=1)
        action.apply(hero, game)


# Regular actions apply to heroes, game actions apply somewhere else on the board
class GameAction(Action):

    def __init__(self, mute=False, limit=False, **kwargs):
        self.mute = mute
        self.limit = limit
        super(GameAction, self).__init__(**kwargs)

    def get_information(self):
        text =  super().get_information()
        if self.mute:
            text = text + 'Mute a selected villain || '
        if self.limit:
            text = text + 'Can only assign one attack to each villain this turn || '
        return text

    def __str__(self):
        return self.get_information()

    def apply(self, active_hero, game=None):

        # Limit a villain from more than one attack this turn
        if self.limit:
            for villain in game.current_villains.values():
                villain.limited = True

        # Petrify a villain
        if self.mute:
            for villain_id, villain in game.current_villains.items():
                print(villain_id, villain)

            # Get which villain to mute
            move = input('Which villain would you like to mute? ')
            try:
                villain_id = int(move)
                if villain_id > len(game.current_villains) or villain_id <= 0:
                    print('Not a valid villain. Please try again.')
                    self.apply(active_hero, game)
                    return
            except ValueError:
                print('Not a valid villain number. Please try again')
                self.apply(active_hero, game)
                return

            # Mute the villain
            muted_villain = game.current_villains[villain_id]
            muted_villain.muted = active_hero.name
            if muted_villain.passive_action is not None:
                for hero in game.heroes:
                    remove_effect = muted_villain.passive_action.passive
                    if remove_effect in hero.bad_passive:
                        hero.bad_passive.pop(remove_effect)

        # Remove attacks from all villains
        if self.attacks != 0:
            for villain in game.current_villains.values():
                villain.current += self.attacks
                if villain.current < 0:
                    villain.current = 0
                print(f'{villain.name} is now at {villain.current}/{villain.strength}')
