from game.models.pokemon import Pokemon

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
        self.x = 400 # Default center
        self.y = 300
        self.facing = "down"
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
        """Returns a list of message strings."""
        messages = []
        if len(self.pokemon) >= 6:
            # Party full: send to storage
            self.storage.append(pokemon)
            messages.append(f"{pokemon.species} was sent to storage.")
        else:
            self.pokemon.append(pokemon)
            messages.append(f"{pokemon.species} added to party.")
        # Update Pokédex
        self.pokedex_seen.add(pokemon.species)
        self.pokedex_caught.add(pokemon.species)
        return messages

    def heal_all_pokemon(self):
        """Returns a list of message strings."""
        for mon in self.pokemon:
            mon.current_hp = mon.max_hp
            mon.status = None
        return ["All Pokemon have been healed to full health!"]
