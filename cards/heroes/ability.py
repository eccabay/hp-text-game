from utils import Action

class Ability:
    def __init__(self, trigger=None, trigger_max=0, action=None):
        self.trigger = trigger
        self.trigger_max = trigger_max
        self.trigger_current = 0
        self.action = action
        self.completed = False

    def __str__(self):
        if self.trigger_max > 0:
            return f'If you play more than {self.trigger_max} {self.trigger}, {self.action}'
        else:
            return f'If {self.trigger}, then {self.action}'

    def check(self, hero, trigger, game):
        if trigger != self.trigger:
            raise ValueError('Something went wrong with the abilities')

        if trigger == 'spell' or trigger == 'attacks':
            self.trigger_current += 1
            if self.trigger_current == self.trigger_max and not self.completed:
                self.action.apply(hero, game)
                self.completed = True

        elif trigger == 'metal' or trigger == 'hearts':
            if not self.completed:
                self.completed = True
                self.action.apply(hero, game)


def get_harry_ability(game):
    if game < 3:
        return None
    else:
        return Ability('metal', action=Action(person='any', attacks=1))


def get_ron_ability(game):
    if game < 3:
        return None
    else:
        return Ability('attacks', trigger_max=3, action=Action(person='any', hearts=2))


def get_hermione_ability(game):
    if game < 3:
        return None
    else:
        return Ability('spell', trigger_max=4, action=Action(person='any', influence=1))


def get_neville_ability(game):
    if game < 3:
        return None
    else:
        return Ability('hearts', action=Action(hearts=1))