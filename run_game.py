import sys
from game.state import GameState
from game.models.pokemon import Pokemon
from game.models.trainer import Player
from game.logic.exploration import ExplorationLogic
from game.logic.battle import Battle
from game.logic.shop import ShopLogic

# Simple Terminal UI specific to modernization verification
def print_logs(logs):
    for log in logs:
        print(log)

def run_battle(player, opponent, is_wild):
    battle = Battle(player, opponent, is_wild)
    print_logs(battle.logs)
    
    while not battle.finished:
        print("\n--- Battle ---")
        print(f"Your {battle.active_player_mon.species}: {battle.active_player_mon.current_hp}/{battle.active_player_mon.max_hp}")
        opp_hp = battle.active_opponent_mon.current_hp
        print(f"Opponent {battle.active_opponent_mon.species}: {opp_hp} HP")
        
        print("1. Fight  2. Bag  3. Pokemon  4. Run")
        choice = input("> ").strip().lower()
        
        action = None
        if choice == "1" or choice == "fight":
             moves = battle.active_player_mon.moves
             for idx, m in enumerate(moves):
                 print(f"{idx+1}. {m}")
             try:
                 idx = int(input("Move: ")) - 1
                 if 0 <= idx < len(moves):
                     action = ("fight", moves[idx])
             except: pass
        elif choice == "2" or choice == "bag":
             print("Items:", player.inventory)
             # Simplification for test: type name
             iname = input("Item name: ")
             if iname: action = ("item", iname)
        elif choice == "4" or choice == "run":
             action = ("run",)
             
        if action:
            res = battle.execute_turn(action)
            print_logs(res['logs'])
            if res['ended']:
                break
        else:
            print("Invalid input.")

def main():
    print("=== Modernized Pokemon Core Verification ===")
    print("1. New Game")
    print("2. Load Game")
    choice = input("> ")
    
    player = None
    if choice == "2":
        name = input("Save file name (e.g. Ash): ")
        player, msg = GameState.load_game(f"{name}.json")
        print(msg)
        if not player: return
    else:
        print("Starting new game...")
        starter = Pokemon("Pyron", level=5)
        player = Player("Ash", [starter])
        player.current_location = "Pallet Town"
        print("Created Ash with Pyron.")

    while True:
        print(f"\nLocation: {player.current_location}")
        
        # Check Exploration
        res = ExplorationLogic.explore(player)
        if res.get("message"): print(res["message"])
        if res.get("event"):
            evt = res["event"]
            if evt["type"] == "battle":
                print("!! Battle Started !!")
                run_battle(player, evt["opponent"], evt["is_wild"])
                # After battle check win?
                if evt.get("flag_on_win"):
                    # Check if player won (alive)
                    if any(p.current_hp > 0 for p in player.pokemon):
                        player.story_flags[evt["flag_on_win"]] = True
                        print(f"Victory! Flag {evt['flag_on_win']} set.")
                    else:
                        print("You lost...")
                continue

        print("\nOptions:")
        print("1. Travel")
        print("2. Save")
        print("3. Quit")
        c = input("> ")
        
        if c == "1":
            neighbors = ExplorationLogic.get_neighbors(player.current_location)
            for i, n in enumerate(neighbors):
                print(f"{i+1}. {n}")
            try:
                idx = int(input("> ")) - 1
                dest = neighbors[idx]
                t_res = ExplorationLogic.travel(player, dest)
                if not t_res["success"]:
                    print(t_res["message"])
                    if t_res["event"] and t_res["event"]["type"] == "battle":
                        print("!! Blocking Battle Started !!")
                        run_battle(player, t_res["event"]["opponent"], False)
                        if any(p.current_hp > 0 for p in player.pokemon):
                             player.story_flags[t_res["event"]["flag_on_win"]] = True
                             # Retry travel logic? For now just loop
                else:
                    print(t_res["message"])
            except: pass
            
        elif c == "2":
            GameState.save_game(player)
            print("Saved.")
        elif c == "3":
            break

if __name__ == "__main__":
    main()
