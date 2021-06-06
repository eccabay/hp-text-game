class DarkArtsCard:
    def __init__(self, name, active=None, passive=None):
        self.name = name
        self.active = active
        self.passive = passive

    def __str__(self):
        text = self.name
        if self.active is not None:
            text = text + f' {self.active.get_information()}'
        if self.passive is not None:
            text = text + f' {self.passive.get_information()}'
        return text

    def apply(self, active_hero, game):
        print(self)
        if self.active is not None:
            self.active.apply(active_hero, game)
        if self.passive is not None:
            self.passive.apply(active_hero, game)
        return