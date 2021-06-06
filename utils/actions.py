class Action:
    def __init__(self, person='active', hearts=0, attacks=0, influence=0, cards=0, discard=0, discard_type='any', metal=0, cards_on_top=None, copy=None, search=None, passive=False, choice=False):
        self.person = person  # One of {'active', 'any', 'all'}
        self.hearts = hearts
        self.attacks = attacks
        self.influence = influence
        self.cards = cards
        self.discard = discard
        self.discard_type = discard_type
        self.metal = metal
        self.cards_on_top = cards_on_top  # One of {'spell', 'item', 'ally'}
        self.copy = copy
        self.search = search
        self.passive = passive
        self.choice = choice

    def get_information(self):
        text = f'{self.person} hero: '
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
        if self.cards_on_top is not None:
            text = text + f'{self.cards_on_top} cards purchased can go on top of deck || '
        if self.copy is not None:
            text = text + f'Copy the effects of a {self.copy} played this turn || '
        if self.search is not None:
            text = text + f'Search discard pile for a {self.search} || '
        if self.passive:
            text = text + f'for each card of type {self.passive} || '
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
            hero_name = input('Who would you like to apply this to? ')
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
        if current_location is not None:
            current_location.current += self.metal
            current_location.current = max(current_location.current, 0)

        # Apply the action
        for hero in hero_list:
            if self.choice:
                self.handle_choice(hero, game)
                continue

            # Passive action
            if self.passive:
                hero.good_passive[self.passive] = Action(person=self.person, hearts=self.hearts, attacks=self.attacks, influence=self.influence)
                continue
            # Active action
            if self.hearts < 0 and hero.cloaked:
                hero.hearts -= 1
            else:
                hero.hearts += self.hearts
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

            # Polyjuice Potion
            if self.copy is not None:
                copy_card = self.select_card(hero, hero.played, self.copy)
                if copy_card is not None:
                    copy_card.play(hero, game, retry=True)  # Retry true to prevent bertie botts from triggering

            # Searching the discard pile
            if self.search is not None:
                pull_card = self.select_card(hero, hero.discard, self.search)
                if pull_card is not None:
                    hero.hand.append(pull_card)

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

        choice = input(f'{hero.name}, choose either of {options}: ')
        if choice == 'hearts' or choice =='h':
            hero.hearts += self.hearts
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
        elif choice == 'search' or choice == 's':
            pull_card = self.select_card(hero, hero.discard, self.search)
            if pull_card is not None:
                hero.hand.append(pull_card)
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
            return
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

# Regular actions apply to heroes, game actions apply somewhere else on the board
class GameAction(Action):

    def apply(self, active_hero, all_heroes=None, current_location=None, game=None):

        # Remove attacks from all villains
        for villain in game.current_villains.values():
            villain.current += self.attacks
            if villain.current < 0:
                villain.current = 0
            print(f'{villain.name} is now at {villain.current}/{villain.strength}')
