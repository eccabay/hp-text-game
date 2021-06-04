from utils import Action, GameAction

class VillainCard:
    def __init__(self, name, strength, active_action=None, passive_action=None, for_each_action=None, reward=None):
        self.name = name
        self.strength = strength
        self.active_action = active_action
        self.passive_action = passive_action
        self.for_each_action = for_each_action
        self.reward = reward
        self.current = 0

    def __str__(self):
        text = f'{self.name}   Attacks: {self.current}/{self.strength}'
        if self.active_action is not None:
            text = text + f'\n{self.active_action.get_information()}'
        if self.passive_action is not None:
            text = text + f'\n{self.passive_action.get_information()}'
        text = text + f'\nReward: {self.reward.get_information()}'
        return text

    def apply_passive(self, active_hero, all_heroes):
        if self.passive_action is not None:
            action = self.passive_action
            if action.person == 'active':
                if isinstance(action, GameAction):
                    active_hero.bad_passive[action.passive] = GameAction(person=action.person, attacks=action.attacks)
                else:
                    active_hero.bad_passive[action.passive] = Action(person=action.person, hearts=action.hearts)
            else:
                for hero in all_heroes:
                    hero.bad_passive[action.passive] = Action(hearts=action.hearts)
    
    def apply_for_each(self, active_hero):
        if self.for_each_action is not None:
            for card_type, action in self.for_each_action.items():
                print(f'Villain {self.name}: {action} for each {card_type}')
                for card in active_hero.hand:
                    if card.type == card_type:
                        action.apply(active_hero)

    def apply_active(self, active_hero, all_heroes, current_location):
        if self.active_action is not None:
            print(f'Villain {self.name}: {self.active_action}')
            self.active_action.apply(active_hero, all_heroes, current_location)

    def attack(self, num_attacks, game, villain_index):
        self.current += num_attacks
        print(f'{self.name}   Attacks: {self.current}/{self.strength}')
        if self.current >= self.strength:
            self.defeat(game, villain_index)

    def defeat(self, game, villain_index):
        print(f'Defeated!\nReward: {self.reward.get_information()}')
        for hero in game.heroes:
            if 'defeat' in hero.good_passive:
                for reward in hero.good_passive['defeat']:
                    print(f"{hero.name} gets reward {reward}")
                    reward.apply(game.get_active_hero(), game.heroes, game.current_location)
            if self.passive_action is not None:
                remove_effect = self.passive_action.passive
                if remove_effect in hero.bad_passive:
                    hero.bad_passive.pop(remove_effect)
        self.reward.apply(game.get_active_hero(), game.heroes, game.current_location)
        game.current_villains[int(villain_index)] = None