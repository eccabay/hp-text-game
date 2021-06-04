class HogwartsCard:
    def __init__(self, name, type, cost=0, regular=None, discard=None, buy=None, other=None, defeat=None, regular_choice=False):
        self.name = name
        self.type = type
        self.cost = cost
        self.regular = regular
        self.discard = discard
        self.buy = buy
        self.other = other
        self.defeat = defeat
        self.regular_choice = regular_choice

    def get_information(self):
        text = ''
        if self.cost != 0:
            text = text + f'({self.cost})  '

        # Basic information
        text = text + f'{self.name} ({self.type}) '

        # Normal action item(s)
        if self.regular is not None:
            if isinstance(self.regular, list):
                for i in range(len(self.regular)):
                    text = text + self.regular[i].get_information()
                    if i != len(self.regular)-1:
                        if self.regular_choice:
                            text = text + ' OR '
                        else:
                            text = text + ' AND '
            else:
                text = text + self.regular.get_information() + ' '

        # Discard action
        if self.discard is not None:
            text = text + f'discard: {self.discard.get_information()} '

        # Buying action
        if self.buy is not None:
            text = text + self.buy.get_information() + ' '

        # Action when other cards are played
        if self.other is not None:
            text = text + self.other.get_information() + ' '

        # Action on defeating a villain
        if self.defeat is not None:
            text = text + f'if you defeat a villain: {self.defeat.get_information()}'
        return text

    def __str__(self):
        return self.get_information()

    def play(self, hero, game, retry=False):
        # If this triggers the bonus of a previously played card
        if len(hero.good_passive) > 0 and not retry:
            if self.type in hero.good_passive:
                hero.good_passive[self.type].apply(hero)

        if self.regular is not None:
            if self.regular_choice:
                try:
                    move = int(input(f'Choose: 1 - {self.regular[0]} OR 2 - {self.regular[1]}'))-1
                    if not (move == 0 or move == 1):
                        print('Invalid choice. Try again')
                        self.play(hero, game, retry=True)
                        return
                except ValueError:
                    print('Invalid choice. Try again')
                    self.play(hero, game, retry=True)
                    return
                self.regular[move].apply(hero, game.heroes, game.current_location, game)
            elif isinstance(self.regular, list):
                for action in self.regular:
                    action.apply(hero, game.heroes, game.current_location, game)
            else:
                self.regular.apply(hero, game.heroes, game.current_location, game)

        if self.buy is not None:
            self.buy.apply(hero)

        if self.other is not None:
            self.other.apply(hero)

        if self.defeat is not None:
            if 'defeat' not in hero.good_passive:
                hero.good_passive['defeat'] = []
            hero.good_passive['defeat'].append(self.defeat)