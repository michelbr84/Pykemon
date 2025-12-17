import json
import os
from game.models.trainer import Player
from game.models.pokemon import Pokemon

class GameState:
    @staticmethod
    def save_game(player, filename=None):
        """Returns (success, message)"""
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
            return True, f"Game saved as {filename}."
        except Exception as e:
            return False, f"Error saving game: {e}"

    @staticmethod
    def load_game(filename):
        """Returns (player_obj, message) or (None, error_message)"""
        try:
            with open(filename, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return None, "Save file not found."
        except Exception as e:
            return None, f"Error loading game: {e}"
            
        try:
            name = data["player_name"]
            
            # Helper to reconstruct Pokemon
            def reconstruct_mon(mon_info):
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
                return mon

            party_objs = [reconstruct_mon(info) for info in data["party"]]
            
            player = Player(name, [])
            player.pokemon = party_objs
            
            player.storage = [reconstruct_mon(info) for info in data.get("storage", [])]
            
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
            
            return player, f"Game loaded. Welcome back, {player.name}!"
        except Exception as e:
            return None, f"Error reconstructing player: {e}"
