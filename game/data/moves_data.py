from game.models.move import Move

# Predefined moves with types, power, accuracy, and potential effects
moves = {
    "Tackle": Move("Tackle", "Normal", 40, 1.0),
    "Ember": Move("Ember", "Fire", 40, 1.0, effect="burn", effect_chance=0.1),
    "Water Gun": Move("Water Gun", "Water", 40, 1.0),
    "Vine Whip": Move("Vine Whip", "Grass", 45, 1.0),
    "Flamethrower": Move("Flamethrower", "Fire", 90, 1.0, effect="burn", effect_chance=0.1),
    "Bubble": Move("Bubble", "Water", 20, 1.0),
    "Razor Leaf": Move("Razor Leaf", "Grass", 55, 0.95),
    "Thunder Shock": Move("Thunder Shock", "Electric", 40, 1.0, effect="paralyze", effect_chance=0.1),
    "Thunderbolt": Move("Thunderbolt", "Electric", 90, 1.0, effect="paralyze", effect_chance=0.1),
    "Thunder Wave": Move("Thunder Wave", "Electric", 0, 0.9, effect="paralyze", effect_chance=1.0),
    "Rock Throw": Move("Rock Throw", "Rock", 50, 0.9),
    "Poison Sting": Move("Poison Sting", "Poison", 15, 1.0, effect="poison", effect_chance=0.2),
    "Sludge": Move("Sludge", "Poison", 50, 1.0, effect="poison", effect_chance=0.3),
    "Quick Attack": Move("Quick Attack", "Normal", 40, 1.0),
    "Gust": Move("Gust", "Flying", 40, 1.0),
    "Bite": Move("Bite", "Dark", 40, 1.0),
    "Hydro Pump": Move("Hydro Pump", "Water", 90, 0.8),
    "Stun Spore": Move("Stun Spore", "Grass", 0, 0.75, effect="paralyze", effect_chance=1.0)
}
