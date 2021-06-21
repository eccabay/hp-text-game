class DarkArtsCard:
    def __init__(self, name, active=None, passive=None, reveal=False):
        self.name = name
        self.active = active
        self.passive = passive
        self.reveal = reveal

    def __str__(self):
        text = self.name
        if self.active is not None:
            if isinstance(self.active, list):
                for action in self.active:
                    text = text + f'\n{action.get_information()}'
            else:
                text = text + f'\n{self.active.get_information()}'
        if self.passive is not None:
            text = text + f' {self.passive.get_information()}'
        if self.reveal:
            text = text + '\nReveal an additional Dark Arts event'
        return text

    def apply(self, active_hero, game):
        print(self)
        if self.passive is not None:
            self.passive.apply(active_hero, game)
        if self.active is not None:
            if isinstance(self.active, list):
                for action in self.active:
                    action.apply(active_hero, game)
            else:
                self.active.apply(active_hero, game)
        if 'stun' in active_hero.bad_passive:
            active_hero.bad_passive.pop('stun')
        if self.name == 'Morsmordre!' and 'death eater' in active_hero.bad_passive:
            active_hero.bad_passive['death eater'].apply(active_hero, game)
        if self.reveal:
            game.draw_dark_arts(1)
        return
