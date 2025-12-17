# Type effectiveness lookup: (attacking_type, defending_type) -> damage multiplier
type_effectiveness = {
    ("Fire", "Grass"): 2.0,
    ("Grass", "Fire"): 0.5,
    ("Water", "Fire"): 2.0,
    ("Fire", "Water"): 0.5,
    ("Grass", "Water"): 2.0,
    ("Water", "Grass"): 0.5,
    ("Water", "Rock"): 2.0,
    ("Grass", "Rock"): 2.0,
    ("Fire", "Rock"): 0.5, # Rock resists Fire
    ("Rock", "Fire"): 2.0,
    ("Electric", "Water"): 2.0,
    ("Rock", "Flying"): 2.0,
    ("Flying", "Rock"): 0.5, # Rock resists Flying
    ("Electric", "Flying"): 2.0,
    ("Poison", "Grass"): 2.0,
    ("Normal", "Rock"): 0.5 # Rock resists Normal attacks
}

# Define Pokemon species data with stats, moves, and evolution info
species_data = {
    "Pyron": {
        "type": "Fire",
        "base_stats": {"hp": 20, "atk": 12, "def": 10, "spd": 10},
        "growth": {"hp": 5, "atk": 3, "def": 2, "spd": 2},
        "evolve_level": 10,
        "evolves_to": "Pyronite",
        "moves": {1: ["Tackle"], 5: ["Ember"], 10: ["Flamethrower"]}
    },
    "Pyronite": {
        "type": "Fire",
        "base_stats": {"hp": 35, "atk": 18, "def": 14, "spd": 14},
        "growth": {"hp": 6, "atk": 4, "def": 3, "spd": 3},
        "moves": {1: ["Tackle"], 5: ["Ember"], 10: ["Flamethrower"]}
    },
    "Aquade": {
        "type": "Water",
        "base_stats": {"hp": 22, "atk": 11, "def": 11, "spd": 10},
        "growth": {"hp": 5, "atk": 3, "def": 3, "spd": 2},
        "evolve_level": 10,
        "evolves_to": "Aquaria",
        "moves": {1: ["Tackle"], 5: ["Water Gun"], 8: ["Bubble"], 10: ["Hydro Pump"]}
    },
    "Aquaria": {
        "type": "Water",
        "base_stats": {"hp": 38, "atk": 16, "def": 15, "spd": 13},
        "growth": {"hp": 6, "atk": 4, "def": 4, "spd": 3},
        "moves": {1: ["Tackle"], 5: ["Water Gun"], 8: ["Bubble"], 10: ["Hydro Pump"]}
    },
    "Florin": {
        "type": "Grass",
        "base_stats": {"hp": 21, "atk": 11, "def": 10, "spd": 10},
        "growth": {"hp": 5, "atk": 3, "def": 2, "spd": 2},
        "evolve_level": 10,
        "evolves_to": "Florac",
        "moves": {1: ["Tackle"], 5: ["Vine Whip"], 8: ["Razor Leaf"], 10: ["Stun Spore"]}
    },
    "Florac": {
        "type": "Grass",
        "base_stats": {"hp": 36, "atk": 17, "def": 14, "spd": 13},
        "growth": {"hp": 6, "atk": 4, "def": 3, "spd": 3},
        "moves": {1: ["Tackle"], 5: ["Vine Whip"], 8: ["Razor Leaf"], 10: ["Stun Spore"]}
    },
    "Zappet": {
        "type": "Electric",
        "base_stats": {"hp": 18, "atk": 12, "def": 9, "spd": 14},
        "growth": {"hp": 4, "atk": 3, "def": 2, "spd": 4},
        "evolve_item": "Thunder Stone",
        "evolves_to": "Zapton",
        "moves": {1: ["Tackle"], 5: ["Thunder Shock"], 7: ["Thunder Wave"], 10: ["Thunderbolt"]}
    },
    "Zapton": {
        "type": "Electric",
        "base_stats": {"hp": 30, "atk": 18, "def": 12, "spd": 20},
        "growth": {"hp": 5, "atk": 4, "def": 3, "spd": 5},
        "moves": {1: ["Tackle"], 5: ["Thunder Shock"], 7: ["Thunder Wave"], 10: ["Thunderbolt"]}
    },
    "Geon": {
        "type": "Rock",
        "base_stats": {"hp": 25, "atk": 14, "def": 15, "spd": 6},
        "growth": {"hp": 6, "atk": 4, "def": 4, "spd": 1},
        "evolve_level": 12,
        "evolves_to": "Geodon",
        "moves": {1: ["Tackle"], 7: ["Rock Throw"]}
    },
    "Geodon": {
        "type": "Rock",
        "base_stats": {"hp": 40, "atk": 20, "def": 20, "spd": 8},
        "growth": {"hp": 7, "atk": 5, "def": 5, "spd": 2},
        "moves": {1: ["Tackle"], 7: ["Rock Throw"]}
    },
    "Wingon": {
        "type": "Flying",
        "base_stats": {"hp": 18, "atk": 12, "def": 8, "spd": 14},
        "growth": {"hp": 4, "atk": 3, "def": 2, "spd": 4},
        "moves": {1: ["Tackle"], 3: ["Gust"], 6: ["Quick Attack"]}
    },
    "Slimer": {
        "type": "Poison",
        "base_stats": {"hp": 22, "atk": 10, "def": 12, "spd": 8},
        "growth": {"hp": 5, "atk": 3, "def": 3, "spd": 2},
        "moves": {1: ["Poison Sting"], 7: ["Sludge"]}
    },
    "Rattatak": {
        "type": "Normal",
        "base_stats": {"hp": 16, "atk": 11, "def": 8, "spd": 12},
        "growth": {"hp": 4, "atk": 3, "def": 2, "spd": 3},
        "evolve_level": 8,
        "evolves_to": "Rattitan",
        "moves": {1: ["Tackle"], 4: ["Quick Attack"], 7: ["Bite"]}
    },
    "Rattitan": {
        "type": "Normal",
        "base_stats": {"hp": 30, "atk": 18, "def": 12, "spd": 18},
        "growth": {"hp": 5, "atk": 4, "def": 3, "spd": 4},
        "moves": {1: ["Tackle"], 4: ["Quick Attack"], 7: ["Bite"]}
    }
}
