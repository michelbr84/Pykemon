from game.data.pokemon_data import species_data

class Pokemon:
    def __init__(self, species_name, level=1):
        self.species = species_name
        self.level = level
        if species_name not in species_data:
             # Fallback or error handling if species doesn't exist
             raise ValueError(f"Unknown species: {species_name}")
             
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
        """Returns a list of message strings describing what happened."""
        messages = []
        if move_name in self.moves:
            return messages
        if len(self.moves) < 4:
            self.moves.append(move_name)
            if not silent:
                messages.append(f"{self.species} learned {move_name}!")
        else:
            forgotten = self.moves.pop(0)
            self.moves.append(move_name)
            if not silent:
                messages.append(f"{self.species} forgot {forgotten} and learned {move_name}!")
        return messages

    def evolve(self, new_species):
        """Returns a list of message strings."""
        messages = []
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
        
        messages.append(f"{old_species} evolved into {self.species}!")
        return messages

    def gain_exp(self, amount):
        """
        Gains experience and handles leveling up.
        Returns a dictionary:
        {
            'leveled_up': bool,
            'messages': list[str]
        }
        """
        self.exp += amount
        leveled_up = False
        messages = []
        
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
            
            messages.append(f"{self.species} leveled up to level {self.level}!")
            
            # Learn new moves at this level, if any
            if self.level in species_data[self.species]["moves"]:
                for move_name in species_data[self.species]["moves"][self.level]:
                    msgs = self.learn_move(move_name)
                    messages.extend(msgs)
            
            # Check for evolution by level
            if "evolve_level" in species_data[self.species] and species_data[self.species]["evolve_level"] == self.level:
                new_species = species_data[self.species]["evolves_to"]
                msgs = self.evolve(new_species)
                messages.extend(msgs)
                # Immediately learn moves of new species at this level, if any
                if self.level in species_data[self.species]["moves"]:
                    for move_name in species_data[self.species]["moves"][self.level]:
                        msgs = self.learn_move(move_name)
                        messages.extend(msgs)
            
            self.exp_to_next = 50 + self.level * 10
            
        return {
            'leveled_up': leveled_up,
            'messages': messages
        }
