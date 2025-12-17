class Move:
    def __init__(self, name, type, power, accuracy=1.0, effect=None, effect_chance=0.0):
        self.name = name
        self.type = type
        self.power = power
        self.accuracy = accuracy
        self.effect = effect # e.g. 'poison', 'paralyze', 'burn'
        self.effect_chance = effect_chance
