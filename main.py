import random
import json

# Define the Move class and moves dictionary
class Move:
    def __init__(self, name, type, power, accuracy=1.0, effect=None, effect_chance=0.0):
        self.name = name
        self.type = type
        self.power = power
        self.accuracy = accuracy
        self.effect = effect # e.g. 'poison', 'paralyze', 'burn'
        self.effect_chance = effect_chance

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

# Item class and item definitions
class Item:
    def __init__(self, name, category, price=0, **kwargs):
        self.name = name
        self.category = category # e.g. 'heal', 'ball', 'status', 'evolve'
        self.price = price
        # Additional fields depending on category
        self.heal_amount = kwargs.get('heal', 0)
        self.cure_status = kwargs.get('cure_status', None)
        self.catch_rate = kwargs.get('catch_rate', 1.0)

# Predefined available item data (used for Mart pricing and effects)
items = {
    "Pokeball": Item("Pokeball", "ball", price=100, catch_rate=1.0),
    "Potion": Item("Potion", "heal", price=100, heal=20),
    "Super Potion": Item("Super Potion", "heal", price=300, heal=50),
    "Antidote": Item("Antidote", "status", price=50, cure_status="poisoned"),
    "Paralyze Heal": Item("Paralyze Heal", "status", price=50, cure_status="paralyzed"),
    "Thunder Stone": Item("Thunder Stone", "evolve", price=1000)
}

# Trainer and Player classes
class Trainer:
    def __init__(self, name, pokemon_list, prize=0, is_gym_leader=False, badge_reward=None):
        self.name = name
        self.pokemon = []
        for p in pokemon_list:
            if isinstance(p, Pokemon):
                self.pokemon.append(p)
            elif isinstance(p, tuple):
                species, lvl = p
                self.pokemon.append(Pokemon(species, level=lvl))
        self.prize = prize
        self.is_gym_leader = is_gym_leader
        self.badge_reward = badge_reward

class Player(Trainer):
    def __init__(self, name, pokemon_list):
        super().__init__(name, pokemon_list)
        self.money = 0
        self.badges = []
        self.inventory = {}
        self.pokedex_seen = set()
        self.pokedex_caught = set()
        self.current_location = None
        self.story_flags = {
            "gym1_beaten": False,
            "rival1_done": False,
            "rival2_done": False,
            "grunt_defeated": False,
            "rocket_defeated": False,
            "joey_defeated": False
        }
        self.rival_name = "Rival"
        self.storage = []
    def add_pokemon(self, pokemon):
        if len(self.pokemon) >= 6:
            # Party full: send to storage
            self.storage.append(pokemon)
            print(f"{pokemon.species} was sent to storage.")
        else:
            self.pokemon.append(pokemon)
            print(f"{pokemon.species} added to party.")
        # Update Pokédex
        self.pokedex_seen.add(pokemon.species)
        self.pokedex_caught.add(pokemon.species)
    def heal_all_pokemon(self):
        for mon in self.pokemon:
            mon.current_hp = mon.max_hp
            mon.status = None
        print("All Pokemon have been healed to full health!")

# Pokemon class
class Pokemon:
    def __init__(self, species_name, level=1):
        self.species = species_name
        self.level = level
        data = species_data[species_name]
        self.type = data["type"]
        # Calculate stats based on base and growth
        base = data["base_stats"]; growth = data["growth"]
        self.max_hp = base["hp"] + (level - 1) * growth["hp"]
        self.attack = base["atk"] + (level - 1) * growth["atk"]
        self.defense = base["def"] + (level - 1) * growth["def"]
        self.speed = base["spd"] + (level - 1) * growth["spd"]
        self.current_hp = self.max_hp
        self.status = None # status condition
        self.moves = []
        self.exp = 0
        self.exp_to_next = 50 + self.level * 10
        # Learn moves up to current level
        for lv in sorted(species_data[species_name]["moves"].keys()):
            if lv <= self.level:
                for move_name in species_data[species_name]["moves"][lv]:
                    self.learn_move(move_name, silent=True)
    def learn_move(self, move_name, silent=False):
        if move_name in self.moves:
            return
        if len(self.moves) < 4:
            self.moves.append(move_name)
            if not silent:
                print(f"{self.species} learned {move_name}!")
        else:
            forgotten = self.moves.pop(0)
            self.moves.append(move_name)
            if not silent:
                print(f"{self.species} forgot {forgotten} and learned {move_name}!")
    def evolve(self, new_species):
        old_species = self.species
        # Preserve current HP percentage
        old_max_hp = self.max_hp
        self.species = new_species
        self.type = species_data[new_species]["type"]
        base = species_data[new_species]["base_stats"]; growth = species_data[new_species]["growth"]
        self.max_hp = base["hp"] + (self.level - 1) * growth["hp"]
        self.attack = base["atk"] + (self.level - 1) * growth["atk"]
        self.defense = base["def"] + (self.level - 1) * growth["def"]
        self.speed = base["spd"] + (self.level - 1) * growth["spd"]
        if old_max_hp > 0:
            # Adjust current HP proportional to new max HP
            self.current_hp = int(self.current_hp * self.max_hp / old_max_hp)
            if self.current_hp < 1:
                self.current_hp = 1
        else:
            self.current_hp = self.max_hp
        print(f"{old_species} evolved into {self.species}!")
    def gain_exp(self, amount):
        self.exp += amount
        leveled_up = False
        # Loop in case multiple levels gained
        while self.exp >= self.exp_to_next:
            self.exp -= self.exp_to_next
            self.level += 1
            leveled_up = True
            base = species_data[self.species]["base_stats"]; growth = species_data[self.species]["growth"]
            old_max = self.max_hp
            self.max_hp = base["hp"] + (self.level - 1) * growth["hp"]
            self.attack = base["atk"] + (self.level - 1) * growth["atk"]
            self.defense = base["def"] + (self.level - 1) * growth["def"]
            self.speed = base["spd"] + (self.level - 1) * growth["spd"]
            # Increase current HP by the amount max HP increased (to maintain HP ratio)
            self.current_hp += (self.max_hp - old_max)
            if self.current_hp > self.max_hp:
                self.current_hp = self.max_hp
            print(f"{self.species} leveled up to level {self.level}!")
            # Learn new moves at this level, if any
            if self.level in species_data[self.species]["moves"]:
                for move_name in species_data[self.species]["moves"][self.level]:
                    self.learn_move(move_name)
            # Check for evolution by level
            if "evolve_level" in species_data[self.species] and species_data[self.species]["evolve_level"] == self.level:
                new_species = species_data[self.species]["evolves_to"]
                self.evolve(new_species)
                # Immediately learn moves of new species at this level, if any
                if self.level in species_data[self.species]["moves"]:
                    for move_name in species_data[self.species]["moves"][self.level]:
                        self.learn_move(move_name)
            self.exp_to_next = 50 + self.level * 10
        return leveled_up

# Function to use an item (in or out of battle)
def use_item(player, item_name, target=None, is_wild=False, battle=False, opponent=None):
    if item_name not in player.inventory or player.inventory[item_name] <= 0:
        print("You don't have that item.")
        return False
    item = items.get(item_name)
    if not item:
        print("Unknown item.")
        return False
    # Poké Ball usage
    if item.category == "ball":
        if not battle:
            print("You can't use that here.")
            return False
        if not is_wild:
            print("You can't use that on someone else's Pokemon!")
            return False
        if target is None or target.current_hp <= 0:
            print("There's no valid target for the ball.")
            return False
        # Use the Poké Ball
        player.inventory[item_name] -= 1
        if player.inventory[item_name] == 0:
            del player.inventory[item_name]
        # Catch chance calculation
        health_ratio = target.current_hp / target.max_hp
        catch_chance = (0.8 * (1 - health_ratio) + 0.1) * item.catch_rate
        if catch_chance > 0.95:
            catch_chance = 0.95
        if catch_chance < 0.05:
            catch_chance = 0.05
        if random.random() < catch_chance:
            print(f"Gotcha! {target.species} was caught!")
            player.add_pokemon(target)
            return True # battle ends
        else:
            print(f"The wild {target.species} broke free!")
            return False
    elif item.category == "heal":
        if target is None:
            print("No target specified.")
            return False
        if target.current_hp <= 0:
            print(f"{target.species} is fainted and can't be healed by a {item_name}!")
            return False
        original_hp = target.current_hp
        target.current_hp += item.heal_amount
        if target.current_hp > target.max_hp:
            target.current_hp = target.max_hp
        healed = target.current_hp - original_hp
        print(f"{target.species} regained {healed} HP.")
        player.inventory[item_name] -= 1
        if player.inventory[item_name] == 0:
            del player.inventory[item_name]
        return False
    elif item.category == "status":
        if target is None:
            print("No target specified.")
            return False
        if target.status is None:
            print(f"{target.species} has no status condition.")
            return False
        if item.cure_status and target.status == item.cure_status:
            target.status = None
            print(f"{target.species} was cured of its {item.cure_status} condition!")
        else:
            print("It had no effect.")
            return False
        player.inventory[item_name] -= 1
        if player.inventory[item_name] == 0:
            del player.inventory[item_name]
        return False
    elif item.category == "evolve":
        if battle:
            print("You can't use that in the middle of a battle!")
            return False
        if target is None:
            print("No target specified for evolution.")
            return False
        if "evolve_item" in species_data[target.species] and species_data[target.species]["evolve_item"] == item_name:
            new_species = species_data[target.species]["evolves_to"]
            target.evolve(new_species)
            # Update Pokédex for new species
            player.pokedex_seen.add(new_species)
            player.pokedex_caught.add(new_species)
        else:
            print("It had no effect.")
            return False
        player.inventory[item_name] -= 1
        if player.inventory[item_name] == 0:
            del player.inventory[item_name]
        return False
    else:
        print("This item cannot be used now.")
        return False

# Battle function handling wild and trainer battles
def battle(player, opponent, is_wild=False, link_battle=False):
    if is_wild:
        opponent_name = None
        opponent_active = opponent # opponent is a Pokemon object
    else:
        opponent_name = opponent.name
        # Heal opponent's Pokémon at battle start for fairness
        for mon in opponent.pokemon:
            if mon.current_hp <= 0:
                mon.current_hp = mon.max_hp
                mon.status = None
        opp_index = 0
        # Get first available Pokémon for opponent
        while opp_index < len(opponent.pokemon) and opponent.pokemon[opp_index].current_hp <= 0:
            opp_index += 1
        if opp_index >= len(opponent.pokemon):
            print(f"{opponent_name} has no Pokemon able to battle!")
            return
        opponent_active = opponent.pokemon[opp_index]
    # Determine player's first active Pokémon
    player_index = 0
    while player_index < len(player.pokemon) and player.pokemon[player_index].current_hp <= 0:
        player_index += 1
    if player_index >= len(player.pokemon):
        print("You have no Pokemon able to battle!")
        return
    player_active = player.pokemon[player_index]
    # Save state for link battle (to restore later)
    saved_states = []
    if link_battle:
        for mon in player.pokemon:
            saved_states.append((mon, mon.current_hp, mon.status))
        if not is_wild:
            for mon in opponent.pokemon:
                saved_states.append((mon, mon.current_hp, mon.status))
    # Battle start messages
    if is_wild:
        print(f"A wild {opponent_active.species} appeared!")
    else:
        print(f"{opponent_name} wants to battle!")
        print(f"{opponent_name} sent out {opponent_active.species}!")
    print(f"Go! {player_active.species}!")
    # Mark seen Pokémon in Pokédex
    if is_wild:
        player.pokedex_seen.add(opponent_active.species)
    else:
        player.pokedex_seen.add(opponent_active.species)
    battle_over = False
    ran_away = False
    caught_pokemon = False
    # Battle loop
    while not battle_over:
        # Display HP of active Pokémon
        print(f"Your {player_active.species}: {player_active.current_hp}/{player_active.max_hp} HP")
        if is_wild:
            print(f"Wild {opponent_active.species}: {opponent_active.current_hp}/{opponent_active.max_hp} HP")
        else:
            print(f"{opponent_name}'s {opponent_active.species}: {opponent_active.current_hp}/{opponent_active.max_hp} HP")
        # Player action choice
        print("Choose an action: [1] Fight [2] Bag [3] Pokemon [4] Run")
        choice = input("> ").strip()
        if choice == "1" or choice.lower() == "fight":
            if not player_active.moves:
                print("No moves available!")
                continue
            print("Choose a move:")
            for idx, mname in enumerate(player_active.moves, start=1):
                mv = moves[mname]
                print(f"{idx}. {mname} (Type: {mv.type}, Power: {mv.power})")
            try:
                m_choice = int(input("> "))
                if m_choice < 1 or m_choice > len(player_active.moves):
                    print("Invalid move choice!")
                    continue
            except ValueError:
                print("Invalid input.")
                continue
            move_name = player_active.moves[m_choice - 1]
            action = ("move", move_name)
        elif choice == "2" or choice.lower() == "bag":
            if not player.inventory:
                print("Your bag is empty!")
                continue
            print("Items:")
            item_list = list(player.inventory.keys())
            for idx, item_name in enumerate(item_list, start=1):
                print(f"{idx}. {item_name} x{player.inventory[item_name]}")
            try:
                i_choice = int(input("> "))
                if i_choice < 1 or i_choice > len(item_list):
                    print("Invalid choice!")
                    continue
            except ValueError:
                print("Invalid input.")
                continue
            item_name = item_list[i_choice - 1]
            if items[item_name].category == "ball" and not is_wild:
                print("You can't use that here!")
                continue
            if items[item_name].category == "evolve":
                print("You can't use that in battle!")
                continue
            target_mon = None
            if items[item_name].category in ["heal", "status"]:
                print("Use on which Pokemon?")
                for idx, mon in enumerate(player.pokemon, start=1):
                    status_text = ""
                    if mon.status:
                        status_text = f" ({mon.status})"
                    fainted_text = " [Fainted]" if mon.current_hp <= 0 else ""
                    print(f"{idx}. {mon.species} - HP {mon.current_hp}/{mon.max_hp}{status_text}{fainted_text}")
                try:
                    t_choice = int(input("> "))
                    if t_choice < 1 or t_choice > len(player.pokemon):
                        print("Invalid choice!")
                        continue
                except ValueError:
                    print("Invalid input.")
                    continue
                target_mon = player.pokemon[t_choice - 1]
            item_ends_battle = use_item(player, item_name, target=target_mon, is_wild=is_wild, battle=True, opponent=opponent_active)
            if item_ends_battle:
                caught_pokemon = True
                battle_over = True
                continue
            action = ("item_used", item_name)
        elif choice == "3" or choice.lower() == "pokemon":
            # Switch Pokémon
            available_switches = [mon for mon in player.pokemon if mon.current_hp > 0 and mon != player_active]
            if not available_switches:
                print("No other Pokemon to switch to!")
                continue
            print("Switch to which Pokemon?")
            for idx, mon in enumerate(player.pokemon, start=1):
                if mon == player_active or mon.current_hp <= 0:
                    print(f"{idx}. {mon.species} (Cannot switch)")
                else:
                    print(f"{idx}. {mon.species} - HP {mon.current_hp}/{mon.max_hp}")
            try:
                s_choice = int(input("> "))
                if s_choice < 1 or s_choice > len(player.pokemon):
                    print("Invalid choice!")
                    continue
            except ValueError:
                print("Invalid input.")
                continue
            new_mon = player.pokemon[s_choice - 1]
            if new_mon.current_hp <= 0 or new_mon == player_active:
                print("Cannot switch to that Pokemon!")
                continue
            print(f"Come back, {player_active.species}! Go, {new_mon.species}!")
            player_active = new_mon
            action = "switch"
        elif choice == "4" or choice.lower() == "run":
            if not is_wild:
                print("You can't run from a trainer battle!")
                continue
            run_chance = 1.0
            if opponent_active.speed > player_active.speed:
                run_chance = 0.5
            if random.random() < run_chance:
                print("Got away safely!")
                ran_away = True
                battle_over = True
                continue
            else:
                print("Couldn't escape!")
                action = "run_failed"
        else:
            print("Invalid action. Choose 1-4.")
            continue

        # Determine and execute turn order and actions
        if isinstance(action, tuple) and action[0] == "move":
            move_name = action[1]
            move = moves[move_name]
            # Choose opponent's move if applicable
            if is_wild:
                opp_move_name = random.choice(opponent_active.moves) if opponent_active.moves else None
                opp_move = moves[opp_move_name] if opp_move_name else None
            else:
                opp_move_name = random.choice(opponent_active.moves) if opponent_active.moves else None
                opp_move = moves[opp_move_name] if opp_move_name else None
            # Decide order
            player_first = True
            if opp_move and opponent_active.speed > player_active.speed:
                player_first = False
            # If equal speed, player goes first (default player_first True covers it)
            if player_first:
                # Player attacks first
                print(f"Your {player_active.species} used {move_name}!")
                if random.random() > move.accuracy:
                    print("But it missed!")
                else:
                    damage = int(move.power * player_active.attack / max(1, opponent_active.defense) / 2)
                    if damage < 1:
                        damage = 1
                    effect_multiplier = 1.0
                    if move.type:
                        # Check type effectiveness
                        if (move.type, opponent_active.type) in type_effectiveness:
                            effect_multiplier = type_effectiveness[(move.type, opponent_active.type)]
                    damage = int(damage * effect_multiplier * random.uniform(0.85, 1.0))
                    if damage < 1:
                        damage = 1
                    opponent_active.current_hp -= damage
                    print(f"It did {damage} damage.")
                    if effect_multiplier > 1:
                        print("It's super effective!")
                    elif 0 < effect_multiplier < 1:
                        print("It's not very effective...")
                    if move.effect and opponent_active.current_hp > 0:
                        if opponent_active.status is None and random.random() < move.effect_chance:
                            opponent_active.status = move.effect + "ed" if move.effect != "paralyze" else "paralyzed"
                            # Grammar for status: we set status as "poisoned", "paralyzed", "burned"
                            if opponent_active.status == "poisoned":
                                print(f"{opponent_name or 'The wild'} {opponent_active.species} was poisoned!")
                            elif opponent_active.status == "paralyzed":
                                print(f"{opponent_name or 'The wild'} {opponent_active.species} was paralyzed! It may not attack!")
                            elif opponent_active.status == "burned":
                                print(f"{opponent_name or 'The wild'} {opponent_active.species} was burned!")
                # Check if opponent fainted
                if opponent_active.current_hp <= 0:
                    opponent_active.current_hp = 0
                    if is_wild:
                        print(f"Wild {opponent_active.species} fainted!")
                    else:
                        print(f"{opponent_name}'s {opponent_active.species} fainted!")
                    # Award experience if not a link battle
                    if not link_battle:
                        exp_gain = opponent_active.level * 20
                        player_active.gain_exp(exp_gain)
                        print(f"{player_active.species} gained {exp_gain} experience points!")
                    if not is_wild:
                        opp_index += 1
                        while opp_index < len(opponent.pokemon) and opponent.pokemon[opp_index].current_hp <= 0:
                            opp_index += 1
                        if opp_index < len(opponent.pokemon):
                            opponent_active = opponent.pokemon[opp_index]
                            print(f"{opponent_name} sent out {opponent_active.species}!")
                            player.pokedex_seen.add(opponent_active.species)
                        else:
                            battle_over = True
                    else:
                        battle_over = True
                    if battle_over:
                        continue # break out of turn loop to after battle processing
                # If opponent still alive, opponent attacks second
                if opp_move and opponent_active.current_hp > 0:
                    # Check paralysis
                    if opponent_active.status == "paralyzed":
                        if random.random() < 0.25:
                            print(f"{opponent_name or 'The wild'} {opponent_active.species} is paralyzed and can't move!")
                            opp_move = None # skip attack
                    if opp_move:
                        print(f"{opponent_name or 'The wild'} {opponent_active.species} used {opp_move_name}!")
                        if random.random() > opp_move.accuracy:
                            print("But it missed!")
                        else:
                            damage = int(opp_move.power * opponent_active.attack / max(1, player_active.defense) / 2)
                            if damage < 1:
                                damage = 1
                            effect_multiplier = 1.0
                            if opp_move.type:
                                if (opp_move.type, player_active.type) in type_effectiveness:
                                    effect_multiplier = type_effectiveness[(opp_move.type, player_active.type)]
                            damage = int(damage * effect_multiplier * random.uniform(0.85, 1.0))
                            if damage < 1:
                                damage = 1
                            player_active.current_hp -= damage
                            print(f"It did {damage} damage.")
                            if effect_multiplier > 1:
                                print("It's super effective!")
                            elif 0 < effect_multiplier < 1:
                                print("It's not very effective...")
                            if opp_move.effect and player_active.current_hp > 0:
                                if player_active.status is None and random.random() < opp_move.effect_chance:
                                    player_active.status = opp_move.effect + "ed" if opp_move.effect != "paralyze" else "paralyzed"
                                    if player_active.status == "poisoned":
                                        print(f"Your {player_active.species} was poisoned!")
                                    elif player_active.status == "paralyzed":
                                        print(f"Your {player_active.species} was paralyzed! It may not attack!")
                                    elif player_active.status == "burned":
                                        print(f"Your {player_active.species} was burned!")
            else:
                # Opponent attacks first
                if opp_move:
                    print(f"{opponent_name or 'The wild'} {opponent_active.species} used {opp_move_name}!")
                    if random.random() > opp_move.accuracy:
                        print("But it missed!")
                    else:
                        damage = int(opp_move.power * opponent_active.attack / max(1, player_active.defense) / 2)
                        if damage < 1:
                            damage = 1
                        effect_multiplier = 1.0
                        if opp_move.type:
                            if (opp_move.type, player_active.type) in type_effectiveness:
                                effect_multiplier = type_effectiveness[(opp_move.type, player_active.type)]
                        damage = int(damage * effect_multiplier * random.uniform(0.85, 1.0))
                        if damage < 1:
                            damage = 1
                        player_active.current_hp -= damage
                        print(f"It did {damage} damage.")
                        if effect_multiplier > 1:
                            print("It's super effective!")
                        elif 0 < effect_multiplier < 1:
                            print("It's not very effective...")
                        if opp_move.effect and player_active.current_hp > 0:
                            if player_active.status is None and random.random() < opp_move.effect_chance:
                                player_active.status = opp_move.effect + "ed" if opp_move.effect != "paralyze" else "paralyzed"
                                if player_active.status == "poisoned":
                                    print(f"Your {player_active.species} was poisoned!")
                                elif player_active.status == "paralyzed":
                                    print(f"Your {player_active.species} was paralyzed! It may not attack!")
                                elif player_active.status == "burned":
                                    print(f"Your {player_active.species} was burned!")
                # Check if player's Pokémon fainted
                if player_active.current_hp <= 0:
                    player_active.current_hp = 0
                    print(f"Your {player_active.species} fainted!")
                    player_active.status = None
                    # Choose next player Pokemon if available
                    next_alive = None
                    for mon in player.pokemon:
                        if mon.current_hp > 0:
                            next_alive = mon
                            break
                    if next_alive:
                        print("Choose a Pokemon to send out:")
                        for idx, mon in enumerate(player.pokemon, start=1):
                            if mon.current_hp > 0:
                                print(f"{idx}. {mon.species} - HP {mon.current_hp}/{mon.max_hp}")
                            else:
                                print(f"{idx}. {mon.species} - [Fainted]")
                        chosen = None
                        while chosen is None:
                            try:
                                c = int(input("> "))
                                if c < 1 or c > len(player.pokemon):
                                    print("Invalid choice.")
                                elif player.pokemon[c-1].current_hp <= 0:
                                    print("That Pokemon is unable to battle.")
                                else:
                                    chosen = player.pokemon[c-1]
                            except ValueError:
                                print("Invalid input.")
                        player_active = chosen
                        print(f"Go! {player_active.species}!")
                    else:
                        battle_over = True
                        continue
                # If player's Pokemon survived or switched, now player's attack
                if player_active.current_hp > 0:
                    print(f"Your {player_active.species} used {move_name}!")
                    if random.random() > move.accuracy:
                        print("But it missed!")
                    else:
                        damage = int(move.power * player_active.attack / max(1, opponent_active.defense) / 2)
                        if damage < 1:
                            damage = 1
                        effect_multiplier = 1.0
                        if move.type:
                            if (move.type, opponent_active.type) in type_effectiveness:
                                effect_multiplier = type_effectiveness[(move.type, opponent_active.type)]
                        damage = int(damage * effect_multiplier * random.uniform(0.85, 1.0))
                        if damage < 1:
                            damage = 1
                        opponent_active.current_hp -= damage
                        print(f"It did {damage} damage.")
                        if effect_multiplier > 1:
                            print("It's super effective!")
                        elif 0 < effect_multiplier < 1:
                            print("It's not very effective...")
                        if move.effect and opponent_active.current_hp > 0:
                            if opponent_active.status is None and random.random() < move.effect_chance:
                                opponent_active.status = move.effect + "ed" if move.effect != "paralyze" else "paralyzed"
                                if opponent_active.status == "poisoned":
                                    print(f"{opponent_name or 'The wild'} {opponent_active.species} was poisoned!")
                                elif opponent_active.status == "paralyzed":
                                    print(f"{opponent_name or 'The wild'} {opponent_active.species} was paralyzed! It may not attack!")
                                elif opponent_active.status == "burned":
                                    print(f"{opponent_name or 'The wild'} {opponent_active.species} was burned!")
                # Check if opponent fainted
                if opponent_active.current_hp <= 0:
                    opponent_active.current_hp = 0
                    if is_wild:
                        print(f"Wild {opponent_active.species} fainted!")
                    else:
                        print(f"{opponent_name}'s {opponent_active.species} fainted!")
                    if not link_battle:
                        exp_gain = opponent_active.level * 20
                        player_active.gain_exp(exp_gain)
                        print(f"{player_active.species} gained {exp_gain} experience points!")
                    if not is_wild:
                        opp_index += 1
                        while opp_index < len(opponent.pokemon) and opponent.pokemon[opp_index].current_hp <= 0:
                            opp_index += 1
                        if opp_index < len(opponent.pokemon):
                            opponent_active = opponent.pokemon[opp_index]
                            print(f"{opponent_name} sent out {opponent_active.species}!")
                            player.pokedex_seen.add(opponent_active.species)
                        else:
                            battle_over = True
                    else:
                        battle_over = True
                    if battle_over:
                        continue

        elif action == "switch":
            # After player switches, opponent gets a free attack
            if not is_wild or opponent_active.current_hp > 0:
                opp_move_name = None
                opp_move = None
                if is_wild:
                    opp_move_name = random.choice(opponent_active.moves) if opponent_active.moves else None
                else:
                    opp_move_name = random.choice(opponent_active.moves) if opponent_active.moves else None
                if opp_move_name:
                    opp_move = moves[opp_move_name]
                    print(f"{opponent_name or 'Wild'} {opponent_active.species} used {opp_move_name}!")
                    if random.random() > opp_move.accuracy:
                        print("But it missed!")
                    else:
                        damage = int(opp_move.power * opponent_active.attack / max(1, player_active.defense) / 2)
                        if damage < 1:
                            damage = 1
                        effect_multiplier = 1.0
                        if opp_move.type:
                            if (opp_move.type, player_active.type) in type_effectiveness:
                                effect_multiplier = type_effectiveness[(opp_move.type, player_active.type)]
                        damage = int(damage * effect_multiplier * random.uniform(0.85, 1.0))
                        if damage < 1:
                            damage = 1
                        player_active.current_hp -= damage
                        print(f"It did {damage} damage.")
                        if effect_multiplier > 1:
                            print("It's super effective!")
                        elif 0 < effect_multiplier < 1:
                            print("It's not very effective...")
                        if opp_move.effect and player_active.current_hp > 0:
                            if player_active.status is None and random.random() < opp_move.effect_chance:
                                player_active.status = opp_move.effect + "ed" if opp_move.effect != "paralyze" else "paralyzed"
                                if player_active.status == "poisoned":
                                    print(f"Your {player_active.species} was poisoned!")
                                elif player_active.status == "paralyzed":
                                    print(f"Your {player_active.species} was paralyzed! It may not attack!")
                                elif player_active.status == "burned":
                                    print(f"Your {player_active.species} was burned!")
            # If the new Pokemon fainted from the free hit, prompt for another
            if player_active.current_hp <= 0:
                player_active.current_hp = 0
                print(f"Your {player_active.species} fainted!")
                player_active.status = None
                next_alive = None
                for mon in player.pokemon:
                    if mon.current_hp > 0:
                        next_alive = mon
                        break
                if next_alive:
                    print("Choose a Pokemon to send out:")
                    for idx, mon in enumerate(player.pokemon, start=1):
                        if mon.current_hp > 0:
                            print(f"{idx}. {mon.species} - HP {mon.current_hp}/{mon.max_hp}")
                        else:
                            print(f"{idx}. {mon.species} - [Fainted]")
                    chosen = None
                    while chosen is None:
                        try:
                            c = int(input("> "))
                            if c < 1 or c > len(player.pokemon):
                                print("Invalid choice.")
                            elif player.pokemon[c-1].current_hp <= 0:
                                print("That Pokemon is unable to battle.")
                            else:
                                chosen = player.pokemon[c-1]
                        except ValueError:
                            print("Invalid input.")
                    player_active = chosen
                    print(f"Go! {player_active.species}!")
                else:
                    battle_over = True
                    continue

        elif action[0] == "item_used" or action == "run_failed":
            # If run failed or after using a non-catching item, opponent attacks if able
            if action == "run_failed":
                # If run fails, wild attacks
                opp_move_name = None
                if is_wild:
                    opp_move_name = random.choice(opponent_active.moves) if opponent_active.moves else None
                else:
                    opp_move_name = random.choice(opponent_active.moves) if opponent_active.moves else None
                if opp_move_name:
                    opp_move = moves[opp_move_name]
                    print(f"{opponent_name or 'Wild'} {opponent_active.species} used {opp_move_name}!")
                    if random.random() > opp_move.accuracy:
                        print("But it missed!")
                    else:
                        damage = int(opp_move.power * opponent_active.attack / max(1, player_active.defense) / 2)
                        if damage < 1:
                            damage = 1
                        effect_multiplier = 1.0
                        if opp_move.type:
                            if (opp_move.type, player_active.type) in type_effectiveness:
                                effect_multiplier = type_effectiveness[(opp_move.type, player_active.type)]
                        damage = int(damage * effect_multiplier * random.uniform(0.85, 1.0))
                        if damage < 1:
                            damage = 1
                        player_active.current_hp -= damage
                        print(f"It did {damage} damage.")
                        if effect_multiplier > 1:
                            print("It's super effective!")
                        elif 0 < effect_multiplier < 1:
                            print("It's not very effective...")
                        if opp_move.effect and player_active.current_hp > 0:
                            if player_active.status is None and random.random() < opp_move.effect_chance:
                                player_active.status = opp_move.effect + "ed" if opp_move.effect != "paralyze" else "paralyzed"
                                if player_active.status == "poisoned":
                                    print(f"Your {player_active.species} was poisoned!")
                                elif player_active.status == "paralyzed":
                                    print(f"Your {player_active.species} was paralyzed! It may not attack!")
                                elif player_active.status == "burned":
                                    print(f"Your {player_active.species} was burned!")
                if player_active.current_hp <= 0:
                    player_active.current_hp = 0
                    print(f"Your {player_active.species} fainted!")
                    player_active.status = None
                    next_alive = None
                    for mon in player.pokemon:
                        if mon.current_hp > 0:
                            next_alive = mon
                            break
                    if next_alive:
                        print("Choose a Pokemon to send out:")
                        for idx, mon in enumerate(player.pokemon, start=1):
                            if mon.current_hp > 0:
                                print(f"{idx}. {mon.species} - HP {mon.current_hp}/{mon.max_hp}")
                            else:
                                print(f"{idx}. {mon.species} - [Fainted]")
                        chosen = None
                        while chosen is None:
                            try:
                                c = int(input("> "))
                                if c < 1 or c > len(player.pokemon):
                                    print("Invalid choice.")
                                elif player.pokemon[c-1].current_hp <= 0:
                                    print("That Pokemon is unable to battle.")
                                else:
                                    chosen = player.pokemon[c-1]
                            except ValueError:
                                print("Invalid input.")
                        player_active = chosen
                        print(f"Go! {player_active.species}!")
                    else:
                        battle_over = True
                        continue

        # End-of-turn status effects (poison, burn)
        if battle_over:
            break
        # Player's Pokémon status effects
        if player_active.status == "poisoned":
            dmg = max(1, player_active.max_hp // 10)
            player_active.current_hp -= dmg
            print(f"{player_active.species} is hurt by poison! (-{dmg} HP)")
            if player_active.current_hp <= 0:
                player_active.current_hp = 0
                print(f"Your {player_active.species} fainted!")
                player_active.status = None
                next_alive = None
                for mon in player.pokemon:
                    if mon.current_hp > 0:
                        next_alive = mon
                        break
                if next_alive:
                    print("Choose a Pokemon to send out:")
                    for idx, mon in enumerate(player.pokemon, start=1):
                        if mon.current_hp > 0:
                            print(f"{idx}. {mon.species} - HP {mon.current_hp}/{mon.max_hp}")
                        else:
                            print(f"{idx}. {mon.species} - [Fainted]")
                    chosen = None
                    while chosen is None:
                        try:
                            c = int(input("> "))
                            if c < 1 or c > len(player.pokemon):
                                print("Invalid choice.")
                            elif player.pokemon[c-1].current_hp <= 0:
                                print("That Pokemon is unable to battle.")
                            else:
                                chosen = player.pokemon[c-1]
                        except ValueError:
                            print("Invalid input.")
                    player_active = chosen
                    print(f"Go! {player_active.species}!")
                else:
                    battle_over = True
        if opponent_active and opponent_active.status == "poisoned":
            dmg = max(1, opponent_active.max_hp // 10)
            opponent_active.current_hp -= dmg
            if is_wild:
                print(f"The wild {opponent_active.species} is hurt by poison! (-{dmg} HP)")
            else:
                print(f"{opponent_name}'s {opponent_active.species} is hurt by poison! (-{dmg} HP)")
            if opponent_active.current_hp <= 0:
                opponent_active.current_hp = 0
                if is_wild:
                    print(f"Wild {opponent_active.species} fainted!")
                else:
                    print(f"{opponent_name}'s {opponent_active.species} fainted!")
                if not link_battle:
                    exp_gain = opponent_active.level * 20
                    player_active.gain_exp(exp_gain)
                    print(f"{player_active.species} gained {exp_gain} experience points!")
                if not is_wild:
                    opp_index += 1
                    while opp_index < len(opponent.pokemon) and opponent.pokemon[opp_index].current_hp <= 0:
                        opp_index += 1
                    if opp_index < len(opponent.pokemon):
                        opponent_active = opponent.pokemon[opp_index]
                        print(f"{opponent_name} sent out {opponent_active.species}!")
                        player.pokedex_seen.add(opponent_active.species)
                    else:
                        battle_over = True
                else:
                    battle_over = True
                if battle_over:
                    continue
        if opponent_active and opponent_active.status == "burned":
            dmg = max(1, opponent_active.max_hp // 10)
            opponent_active.current_hp -= dmg
            if is_wild:
                print(f"The wild {opponent_active.species} is hurt by its burn! (-{dmg} HP)")
            else:
                print(f"{opponent_name}'s {opponent_active.species} is hurt by its burn! (-{dmg} HP)")
            if opponent_active.current_hp <= 0:
                opponent_active.current_hp = 0
                if is_wild:
                    print(f"Wild {opponent_active.species} fainted!")
                else:
                    print(f"{opponent_name}'s {opponent_active.species} fainted!")
                if not link_battle:
                    exp_gain = opponent_active.level * 20
                    player_active.gain_exp(exp_gain)
                    print(f"{player_active.species} gained {exp_gain} experience points!")
                if not is_wild:
                    opp_index += 1
                    while opp_index < len(opponent.pokemon) and opponent.pokemon[opp_index].current_hp <= 0:
                        opp_index += 1
                    if opp_index < len(opponent.pokemon):
                        opponent_active = opponent.pokemon[opp_index]
                        print(f"{opponent_name} sent out {opponent_active.species}!")
                        player.pokedex_seen.add(opponent_active.species)
                    else:
                        battle_over = True
                else:
                    battle_over = True
                if battle_over:
                    continue
        if player_active.status == "burned":
            dmg = max(1, player_active.max_hp // 10)
            player_active.current_hp -= dmg
            print(f"{player_active.species} is hurt by its burn! (-{dmg} HP)")
            if player_active.current_hp <= 0:
                player_active.current_hp = 0
                print(f"Your {player_active.species} fainted!")
                player_active.status = None
                next_alive = None
                for mon in player.pokemon:
                    if mon.current_hp > 0:
                        next_alive = mon
                        break
                if next_alive:
                    print("Choose a Pokemon to send out:")
                    for idx, mon in enumerate(player.pokemon, start=1):
                        if mon.current_hp > 0:
                            print(f"{idx}. {mon.species} - HP {mon.current_hp}/{mon.max_hp}")
                        else:
                            print(f"{idx}. {mon.species} - [Fainted]")
                    chosen = None
                    while chosen is None:
                        try:
                            c = int(input("> "))
                            if c < 1 or c > len(player.pokemon):
                                print("Invalid choice.")
                            elif player.pokemon[c-1].current_hp <= 0:
                                print("That Pokemon is unable to battle.")
                            else:
                                chosen = player.pokemon[c-1]
                        except ValueError:
                            print("Invalid input.")
                    player_active = chosen
                    print(f"Go! {player_active.species}!")
                else:
                    battle_over = True

    # After battle, determine outcome
    if link_battle:
        # Determine winner for link battle
        player_has_alive = any(mon.current_hp > 0 for mon in player.pokemon)
        opponent_has_alive = False
        if is_wild:
            opponent_has_alive = opponent_active.current_hp > 0
        else:
            opponent_has_alive = any(mon.current_hp > 0 for mon in opponent.pokemon)
        if player_has_alive and not opponent_has_alive:
            print("You won the match!")
        elif opponent_has_alive and not player_has_alive:
            print("You lost the match!")
        else:
            print("The match ended in a draw!")
        # Restore HP and status for all Pokemon (no lasting effects from link battle)
        for mon, hp, status in saved_states:
            mon.current_hp = hp
            mon.status = status
        return
    if ran_away:
        return
    if caught_pokemon:
        return
    # If a normal battle ended
    player_has_alive = any(mon.current_hp > 0 for mon in player.pokemon)
    if not player_has_alive:
        print("You were defeated...")
        if player.money > 0:
            lost_money = player.money // 2
            player.money -= lost_money
            print(f"You dropped ${lost_money} in panic!")
        # Move player to safe location (nearest Pokemon Center)
        if player.story_flags.get("gym1_beaten"):
            player.current_location = "Viridian City"
        else:
            player.current_location = "Pallet Town"
        player.heal_all_pokemon()
        return
    else:
        if is_wild:
            print("You defeated the wild Pokémon!")
        else:
            print(f"You defeated {opponent_name}!")
            if hasattr(opponent, "prize") and opponent.prize:
                player.money += opponent.prize
                print(f"You received ${opponent.prize} for winning!")
            if hasattr(opponent, "is_gym_leader") and opponent.is_gym_leader and opponent.badge_reward:
                if opponent.badge_reward not in player.badges:
                    player.badges.append(opponent.badge_reward)
                    print(f"You received the {opponent.badge_reward}!")
                player.story_flags["gym1_beaten"] = True
            if opponent_name and opponent_name.lower().startswith("team rocket"):
                player.story_flags["rocket_defeated"] = True
        # Rival default prize if not set
        if opponent_name and opponent_name == player.rival_name:
            if hasattr(opponent, "prize") and opponent.prize:
                pass
            else:
                reward = 300
                player.money += reward
                print(f"You received ${reward} for winning!")

# Saving and loading game state
def save_game(player, filename=None):
    data = {}
    data["player_name"] = player.name
    data["rival_name"] = player.rival_name
    data["money"] = player.money
    data["badges"] = player.badges
    data["current_location"] = player.current_location
    data["inventory"] = player.inventory
    data["story_flags"] = player.story_flags
    data["pokedex_seen"] = list(player.pokedex_seen)
    data["pokedex_caught"] = list(player.pokedex_caught)
    party_data = []
    for mon in player.pokemon:
        mon_info = {
            "species": mon.species,
            "level": mon.level,
            "current_hp": mon.current_hp,
            "max_hp": mon.max_hp,
            "status": mon.status,
            "moves": mon.moves[:],
            "exp": mon.exp
        }
        party_data.append(mon_info)
    data["party"] = party_data
    storage_data = []
    for mon in player.storage:
        mon_info = {
            "species": mon.species,
            "level": mon.level,
            "current_hp": mon.current_hp,
            "max_hp": mon.max_hp,
            "status": mon.status,
            "moves": mon.moves[:],
            "exp": mon.exp
        }
        storage_data.append(mon_info)
    data["storage"] = storage_data
    if not filename:
        filename = f"{player.name}.json"
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Game saved as {filename}.")
    except Exception as e:
        print(f"Error saving game: {e}")

def load_game(filename):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Save file not found.")
        return None
    except Exception as e:
        print(f"Error loading game: {e}")
        return None
    try:
        name = data["player_name"]
        party_objs = []
        for mon_info in data["party"]:
            species = mon_info["species"]
            level = mon_info["level"]
            mon = Pokemon(species, level=level)
            mon.current_hp = mon_info["current_hp"]
            if mon.current_hp > mon.max_hp:
                mon.current_hp = mon.max_hp
            mon.status = mon_info["status"]
            mon.exp = mon_info.get("exp", 0)
            mon.exp_to_next = 50 + mon.level * 10
            # Override moves to exactly what was saved
            mon.moves = mon_info["moves"]
            party_objs.append(mon)
        player = Player(name, [])
        player.pokemon = party_objs
        storage_objs = []
        for mon_info in data.get("storage", []):
            species = mon_info["species"]
            level = mon_info["level"]
            mon = Pokemon(species, level=level)
            mon.current_hp = mon_info["current_hp"]
            if mon.current_hp > mon.max_hp:
                mon.current_hp = mon.max_hp
            mon.status = mon_info["status"]
            mon.exp = mon_info.get("exp", 0)
            mon.exp_to_next = 50 + mon.level * 10
            mon.moves = mon_info["moves"]
            storage_objs.append(mon)
        player.storage = storage_objs
        player.rival_name = data.get("rival_name", "Rival")
        player.money = data.get("money", 0)
        player.badges = data.get("badges", [])
        player.current_location = data.get("current_location", "Pallet Town")
        player.inventory = data.get("inventory", {})
        flags = data.get("story_flags", {})
        for key, val in flags.items():
            player.story_flags[key] = val
        player.pokedex_seen = set(data.get("pokedex_seen", []))
        player.pokedex_caught = set(data.get("pokedex_caught", []))
        print(f"Game loaded. Player: {player.name}, Location: {player.current_location}")
        return player
    except Exception as e:
        print(f"Error reconstructing player: {e}")
        return None

# New game setup
def new_game():
    print("Welcome to the world of Pokémon!")
    name = input("Please enter your name: ").strip()
    if not name:
        name = "Ash"
    rival_name = input("Enter your rival's name: ").strip()
    if not rival_name:
        rival_name = "Gary"
    # Starter selection
    print("Choose your starter Pokémon:")
    starters = [("Pyron", "Fire"), ("Aquade", "Water"), ("Florin", "Grass")]
    for idx, (sname, stype) in enumerate(starters, start=1):
        print(f"{idx}. {sname} ({stype}-type)")
    choice = None
    while choice is None:
        try:
            sel = int(input("> "))
            if 1 <= sel <= len(starters):
                choice = sel
            else:
                print("Invalid choice. Enter 1-3.")
        except ValueError:
            print("Invalid input. Enter a number.")
    starter_species, starter_type = starters[choice-1]
    # Initialize player and starter Pokémon
    starter_mon = Pokemon(starter_species, level=5)
    player = Player(name, [starter_mon])
    player.current_location = "Pallet Town"
    player.rival_name = rival_name
    # Initial items and money
    player.money = 500
    player.inventory = {"Pokeball": 5, "Potion": 2}
    # Update Pokédex for starter
    player.pokedex_seen.add(starter_mon.species)
    player.pokedex_caught.add(starter_mon.species)
    # Story introduction
    print(f"Professor Oak: {player.name}, you received a {starter_mon.species}! Take good care of it.")
    print("Professor Oak: Here are 5 Poké Balls and 2 Potions to start your journey.")
    print(f"Your rival {rival_name} will take the Pokémon with a type advantage.")
    # Determine rival's starter
    if starter_type == "Fire":
        rival_starter_species = "Aquade"
    elif starter_type == "Water":
        rival_starter_species = "Florin"
    else:
        rival_starter_species = "Pyron"
    rival_starter = Pokemon(rival_starter_species, level=5)
    rival_trainer = Trainer(rival_name, [rival_starter], prize=100)
    print(f"{rival_name}: Let's have a battle with our new Pokémon!")
    battle(player, rival_trainer, is_wild=False, link_battle=False)
    player.story_flags["rival1_done"] = True
    print(f"{rival_name}: That was a good fight. I'll train my Pokémon and get stronger!")
    player.heal_all_pokemon()
    return player

# Main game loop for exploration and actions
def main_game_loop(player):
    print("Your journey begins now!")
    while True:
        loc = player.current_location
        # Define neighbors for each location
        neighbors = []
        if loc == "Pallet Town":
            neighbors = ["Route 1"]
        elif loc == "Route 1":
            neighbors = ["Pallet Town", "Viridian City"]
        elif loc == "Viridian City":
            neighbors = ["Route 1", "Route 2"]
        elif loc == "Route 2":
            neighbors = ["Viridian City", "Rocket Hideout"]
        elif loc == "Rocket Hideout":
            neighbors = ["Route 2"]
        print(f"\nCurrent location: {loc}")
        print("What would you like to do?")
        # Travel options
        for i, neigh in enumerate(neighbors, start=1):
            print(f"{i}. Go to {neigh}")
        # Location-specific and general actions
        actions = []
        if loc in ["Pallet Town", "Route 1", "Viridian City", "Route 2", "Rocket Hideout"]:
            actions.append(("E", "Explore"))
        if loc == "Viridian City":
            actions.append(("H", "Heal Pokémon at Center"))
            actions.append(("M", "Visit PokéMart"))
            actions.append(("G", "Challenge Gym Leader"))
        if loc == "Pallet Town":
            actions.append(("H", "Rest at home"))
        actions.append(("P", "View Pokémon"))
        actions.append(("B", "Open Bag"))
        actions.append(("D", "View Pokédex"))
        actions.append(("S", "Save Game"))
        actions.append(("Q", "Quit Game"))
        for letter, desc in actions:
            print(f"{letter}. {desc}")
        choice = input("> ").strip()
        # Travel choice
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(neighbors):
                dest = neighbors[idx-1]
                # Check for storyline gating on travel
                if loc == "Viridian City" and dest == "Route 2":
                    if not player.story_flags["gym1_beaten"]:
                        print("Policeman: The road ahead is closed due to Team Rocket. You need a Gym Badge to pass!")
                        continue
                    if not player.story_flags["rival2_done"]:
                        # Trigger Rival battle on Route 2 entrance
                        if player.pokemon:
                            p_type = player.pokemon[0].type
                        else:
                            p_type = "Fire"
                        if p_type == "Fire":
                            rival_starter_species = "Aquade"; rival_main_species = "Aquaria"
                        elif p_type == "Water":
                            rival_starter_species = "Florin"; rival_main_species = "Pyronite"
                        else:
                            rival_starter_species = "Pyron"; rival_main_species = "Aquaria" # Actually should be Aquaria for grass?
                            rival_main_species = "Pyronite" if p_type == "Grass" else rival_main_species
                        rival_main = Pokemon(rival_main_species, level=11)
                        rival_side = Pokemon("Rattatak", level=9)
                        rival_trainer = Trainer(player.rival_name, [rival_main, rival_side], prize=300)
                        print(f"{player.rival_name}: I've been training! Let's battle once more before you go ahead.")
                        battle(player, rival_trainer, is_wild=False, link_battle=False)
                        player.story_flags["rival2_done"] = True
                        if not any(mon.current_hp > 0 for mon in player.pokemon):
                            # If lost to rival, they are sent back to center (battle() handled it)
                            continue
                        else:
                            print(f"{player.rival_name}: Hmph, you won. I'll see you at the Pokémon League!")
                if dest == "Rocket Hideout":
                    if not player.story_flags["grunt_defeated"]:
                        # Rocket Grunt battle
                        grunt_mon1 = Pokemon("Rattatak", level=6)
                        grunt_mon2 = Pokemon("Wingon", level=6)
                        grunt_trainer = Trainer("Team Rocket Grunt", [grunt_mon1, grunt_mon2], prize=200)
                        print("Team Rocket Grunt: Stop right there, kid!")
                        battle(player, grunt_trainer, is_wild=False, link_battle=False)
                        if not any(mon.current_hp > 0 for mon in player.pokemon):
                            continue
                        else:
                            player.story_flags["grunt_defeated"] = True
                            print("You defeated the Rocket Grunt guarding the hideout.")
                    # After grunt defeated, allow entering hideout
                player.current_location = dest
                continue
            else:
                print("Invalid choice.")
                continue
        if not choice:
            continue
        choice = choice.upper()
        if choice == "E":
            if loc == "Pallet Town":
                print("Pallet Town: A small, quiet town. Professor Oak's Lab is here.")
                print("Your adventure starts here – perhaps check Route 1 for wild Pokémon.")
            elif loc == "Route 1":
                if not player.story_flags["joey_defeated"]:
                    joey_mon = Pokemon("Rattatak", level=3)
                    joey_trainer = Trainer("Youngster Joey", [joey_mon], prize=50)
                    print("Youngster Joey: Hey! I just caught a cool Rattatak. Battle me!")
                    battle(player, joey_trainer, is_wild=False, link_battle=False)
                    if not any(mon.current_hp > 0 for mon in player.pokemon):
                        continue
                    else:
                        player.story_flags["joey_defeated"] = True
                        print("Youngster Joey: Aw, I lost... maybe my Rattatak needs more training.")
                        continue
                if random.random() < 0.7:
                    wild_species = random.choice(["Rattatak", "Wingon"])
                    level = random.randint(2, 3)
                    wild_mon = Pokemon(wild_species, level=level)
                    battle(player, wild_mon, is_wild=True, link_battle=False)
                else:
                    print("You wander around but don't encounter any Pokémon this time.")
            elif loc == "Viridian City":
                print("You stroll through Viridian City. It's bustling with trainers and shops.")
                if not player.story_flags["gym1_beaten"]:
                    print("A townsperson mentions: 'The Gym Leader here is tough – you'd better train.'")
                else:
                    print("People applaud you for driving Team Rocket out of the area!")
            elif loc == "Route 2":
                if random.random() < 0.7:
                    wild_species = random.choice(["Zappet", "Slimer"])
                    level = random.randint(5, 6)
                    wild_mon = Pokemon(wild_species, level=level)
                    battle(player, wild_mon, is_wild=True, link_battle=False)
                else:
                    print("You explore the tall grass but find no Pokémon this time.")
            elif loc == "Rocket Hideout":
                if not player.story_flags["rocket_defeated"]:
                    boss_main_species = "Florac"
                    if player.pokemon:
                        starter_type = player.pokemon[0].type
                        if starter_type == "Fire":
                            boss_main_species = "Florac"
                        elif starter_type == "Water":
                            boss_main_species = "Pyronite"
                        elif starter_type == "Grass":
                            boss_main_species = "Aquaria"
                    boss_main = Pokemon(boss_main_species, level=12)
                    boss_side = Pokemon("Slimer", level=9)
                    boss_trainer = Trainer("Team Rocket Boss", [boss_side, boss_main], prize=1000)
                    print("Team Rocket Boss: So, you've come to stop me? Let's see you try!")
                    battle(player, boss_trainer, is_wild=False, link_battle=False)
                    if not any(mon.current_hp > 0 for mon in player.pokemon):
                        continue
                    else:
                        player.story_flags["rocket_defeated"] = True
                        print("Team Rocket Boss: This can't be! Team Rocket... blasting off...")
                        print("With the boss defeated, Team Rocket flees the hideout. You've saved the region!")
                        print("Congratulations, you completed the main story!")
                else:
                    print("The hideout is deserted now. Team Rocket is nowhere to be seen.")
            else:
                print("There's nothing of interest here.")
        elif choice == "H":
            player.heal_all_pokemon()
        elif choice == "M":
            print("Welcome to the PokéMart! What would you like to do?")
            mart_items = [("Pokeball", 100), ("Potion", 100), ("Super Potion", 300), ("Thunder Stone", 1000)]
            while True:
                print(f"Money: ${player.money}")
                print("Items for sale:")
                for idx, (item_name, price) in enumerate(mart_items, start=1):
                    print(f"{idx}. {item_name} - ${price}")
                print("5. Sell items")
                print("0. Exit Mart")
                mart_choice = input("> ").strip()
                if mart_choice == "0":
                    break
                if mart_choice == "5":
                    if not player.inventory:
                        print("You have nothing to sell.")
                        continue
                    inv_list = list(player.inventory.keys())
                    for idx, item_name in enumerate(inv_list, start=1):
                        sell_price = items[item_name].price // 2 if item_name in items else 0
                        print(f"{idx}. {item_name} x{player.inventory[item_name]} (Sell for ${sell_price} each)")
                    try:
                        sell_idx = int(input("Select item to sell (0 to cancel): "))
                    except ValueError:
                        print("Invalid input.")
                        continue
                    if sell_idx == 0:
                        continue
                    if 1 <= sell_idx <= len(inv_list):
                        sell_item = inv_list[sell_idx-1]
                        sell_price = items[sell_item].price // 2 if sell_item in items else 0
                        try:
                            sell_qty = int(input(f"How many {sell_item} to sell? "))
                        except ValueError:
                            print("Invalid quantity.")
                            continue
                        if sell_qty <= 0 or sell_qty > player.inventory.get(sell_item, 0):
                            print("Invalid quantity.")
                            continue
                        total_gain = sell_price * sell_qty
                        player.inventory[sell_item] -= sell_qty
                        if player.inventory[sell_item] == 0:
                            del player.inventory[sell_item]
                        player.money += total_gain
                        print(f"You sold {sell_qty} {sell_item}(s) for ${total_gain}.")
                    else:
                        print("Invalid choice.")
                else:
                    try:
                        buy_idx = int(mart_choice)
                    except ValueError:
                        print("Invalid input.")
                        continue
                    if 1 <= buy_idx <= len(mart_items):
                        item_name, price = mart_items[buy_idx-1]
                        try:
                            buy_qty = int(input(f"How many {item_name}? "))
                        except ValueError:
                            print("Invalid quantity.")
                            continue
                        if buy_qty <= 0:
                            print("Invalid quantity.")
                            continue
                        cost = price * buy_qty
                        if player.money < cost:
                            print("You don't have enough money.")
                            continue
                        player.money -= cost
                        player.inventory[item_name] = player.inventory.get(item_name, 0) + buy_qty
                        print(f"You bought {buy_qty} {item_name}(s).")
                    else:
                        print("Invalid choice.")
        elif choice == "G":
            if player.story_flags["gym1_beaten"]:
                print("The Gym is empty now. You've already earned the badge here.")
            else:
                gym_mon1 = Pokemon("Geon", level=8)
                gym_mon2 = Pokemon("Geodon", level=12)
                gym_leader = Trainer("Gym Leader Rocky", [gym_mon1, gym_mon2], prize=500, is_gym_leader=True, badge_reward="Boulder Badge")
                print("Gym Leader Rocky: You won't take my badge easily – prepare for a rock-hard battle!")
                battle(player, gym_leader, is_wild=False, link_battle=False)
                if not any(mon.current_hp > 0 for mon in player.pokemon):
                    continue
                else:
                    print("Gym Leader Rocky: Outstanding! You've earned the Boulder Badge!")
        elif choice == "P":
            print("Party Pokémon:")
            for idx, mon in enumerate(player.pokemon, start=1):
                status_text = f"{mon.current_hp}/{mon.max_hp} HP"
                if mon.status:
                    status_text += f", Status: {mon.status}"
                print(f"{idx}. {mon.species} (Lv{mon.level}) - {status_text}")
            if player.badges:
                print("Badges:", ", ".join(player.badges))
            else:
                print("Badges: (none)")
            if player.storage:
                swap = input("Switch Pokémon with storage? (y/n): ").strip().lower()
                if swap == 'y':
                    print("Storage Pokémon:")
                    for jdx, mon in enumerate(player.storage, start=1):
                        print(f"{jdx}. {mon.species} (Lv{mon.level})")
                    try:
                        party_idx = int(input("Select party Pokémon to send to storage (0 to cancel): "))
                    except ValueError:
                        continue
                    if party_idx == 0:
                        continue
                    try:
                        storage_idx = int(input("Select storage Pokémon to withdraw: "))
                    except ValueError:
                        continue
                    if 1 <= party_idx <= len(player.pokemon) and 1 <= storage_idx <= len(player.storage):
                        party_mon = player.pokemon[party_idx-1]
                        storage_mon = player.storage[storage_idx-1]
                        player.pokemon[party_idx-1] = storage_mon
                        player.storage[storage_idx-1] = party_mon
                        print(f"Switched {party_mon.species} with {storage_mon.species}.")
                    else:
                        print("Invalid selection.")
        elif choice == "B":
            if not player.inventory:
                print("Your bag is empty.")
            else:
                print("Your items:")
                inv_list = list(player.inventory.keys())
                for idx, item_name in enumerate(inv_list, start=1):
                    print(f"{idx}. {item_name} x{player.inventory[item_name]}")
                try:
                    item_idx = int(input("Choose an item to use (0 to cancel): "))
                except ValueError:
                    print("Invalid input.")
                    continue
                if item_idx == 0:
                    continue
                if 1 <= item_idx <= len(inv_list):
                    item_name = inv_list[item_idx-1]
                    item_obj = items.get(item_name)
                    if not item_obj:
                        print("Unknown item.")
                        continue
                    if item_obj.category == "ball":
                        print("You can't use that now.")
                        continue
                    target_mon = None
                    if item_obj.category == "evolve":
                        print("Use the stone on which Pokémon?")
                        for idx, mon in enumerate(player.pokemon, start=1):
                            print(f"{idx}. {mon.species} (Lv{mon.level})")
                        try:
                            poke_idx = int(input("> "))
                        except ValueError:
                            print("Invalid input.")
                            continue
                        if 1 <= poke_idx <= len(player.pokemon):
                            target_mon = player.pokemon[poke_idx-1]
                        else:
                            print("Invalid choice.")
                            continue
                        use_item(player, item_name, target=target_mon, is_wild=False, battle=False)
                    elif item_obj.category in ["heal", "status"]:
                        print("Use on which Pokémon?")
                        for idx, mon in enumerate(player.pokemon, start=1):
                            status_text = ""
                            if mon.status:
                                status_text = f" ({mon.status})"
                            faint_text = " [Fainted]" if mon.current_hp <= 0 else ""
                            print(f"{idx}. {mon.species} - {mon.current_hp}/{mon.max_hp} HP{status_text}{faint_text}")
                        try:
                            poke_idx = int(input("> "))
                        except ValueError:
                            print("Invalid input.")
                            continue
                        if 1 <= poke_idx <= len(player.pokemon):
                            target_mon = player.pokemon[poke_idx-1]
                        else:
                            print("Invalid choice.")
                            continue
                        use_item(player, item_name, target=target_mon, is_wild=False, battle=False)
                    else:
                        print("This item cannot be used from the Bag.")
                else:
                    print("Invalid choice.")
        elif choice == "D":
            seen_list = sorted(player.pokedex_seen)
            print(f"Pokédex: {len(player.pokedex_caught)} caught, {len(player.pokedex_seen)} seen")
            for species in seen_list:
                status = "Caught" if species in player.pokedex_caught else "Seen"
                print(f"{species} – {status}")
        elif choice == "S":
            save_game(player)
        elif choice == "Q":
            print("Thank you for playing! Goodbye.")
            break
        else:
            print("Invalid option.")

# Main menu and program entry point
def main():
    while True:
        print("\n--- Main Menu ---")
        print("1. New Game")
        print("2. Load Game")
        print("3. Trade Pokémon (between saved profiles)")
        print("4. PvP Battle (between saved profiles)")
        print("5. Quit")
        sel = input("> ").strip()
        if sel == "1":
            player = new_game()
            main_game_loop(player)
        elif sel == "2":
            filename = input("Enter your save file name (or player name): ").strip()
            if not filename:
                continue
            if not filename.endswith(".json"):
                filename += ".json"
            player = load_game(filename)
            if player:
                main_game_loop(player)
        elif sel == "3":
            name1 = input("Enter name of first player to trade: ").strip()
            name2 = input("Enter name of second player to trade: ").strip()
            if not name1 or not name2:
                print("Names cannot be empty.")
                continue
            file1 = name1 + ".json"; file2 = name2 + ".json"
            p1 = load_game(file1)
            p2 = load_game(file2)
            if not p1 or not p2:
                print("Failed to load one or both profiles.")
                continue
            print(f"{p1.name}'s Pokémon:")
            for idx, mon in enumerate(p1.pokemon, start=1):
                print(f"{idx}. {mon.species} (Lv{mon.level})")
            print(f"{p2.name}'s Pokémon:")
            for jdx, mon in enumerate(p2.pokemon, start=1):
                print(f"{jdx+len(p1.pokemon)}. {mon.species} (Lv{mon.level})")
            try:
                choice1 = int(input(f"Select a Pokémon from {p1.name} to trade: "))
                choice2 = int(input(f"Select a Pokémon from {p2.name} to trade: "))
            except ValueError:
                print("Invalid selection.")
                continue
            if choice1 < 1 or choice1 > len(p1.pokemon) or choice2 < 1 or choice2 > len(p2.pokemon):
                print("Invalid selection.")
                continue
            if len(p1.pokemon) == 1 or len(p2.pokemon) == 1:
                print("Trade canceled: A player only has one Pokémon (cannot be left without any).")
                continue
            mon1 = p1.pokemon.pop(choice1 - 1)
            mon2 = p2.pokemon.pop(choice2 - 1)
            p1.pokemon.append(mon2)
            p2.pokemon.append(mon1)
            p1.pokedex_seen.add(mon2.species); p1.pokedex_caught.add(mon2.species)
            p2.pokedex_seen.add(mon1.species); p2.pokedex_caught.add(mon1.species)
            print(f"Trade complete: {p1.name} received {mon2.species}, {p2.name} received {mon1.species}.")
            save_game(p1, file1); save_game(p2, file2)
        elif sel == "4":
            name1 = input("Enter name of first player: ").strip()
            name2 = input("Enter name of second player: ").strip()
            if not name1 or not name2:
                print("Names cannot be empty.")
                continue
            file1 = name1 + ".json"; file2 = name2 + ".json"
            p1 = load_game(file1)
            p2 = load_game(file2)
            if not p1 or not p2:
                print("Failed to load one or both profiles.")
                continue
            ctrl = input(f"Which player do you want to control? (1 = {p1.name}, 2 = {p2.name}): ").strip()
            if ctrl == "1":
                battle(p1, p2, is_wild=False, link_battle=True)
            elif ctrl == "2":
                battle(p2, p1, is_wild=False, link_battle=True)
            else:
                print("Invalid choice.")
        elif sel == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid menu option.")

# Run the main menu when the script is executed
if __name__ == "__main__":
    main()