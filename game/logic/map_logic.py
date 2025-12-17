from game.logic.exploration import ExplorationLogic
import random

class MapLogic:
    # Define exits for each map
    # Structure: Location -> Direction -> {target: "Name", spawn_x: int, spawn_y: int}
    # Directions: "top", "bottom", "left", "right"
    EXITS = {
        "Pallet Town": {
            "top": {"target": "Route 1", "spawn_x": 400, "spawn_y": 550}
        },
        "Route 1": {
            "bottom": {"target": "Pallet Town", "spawn_x": 400, "spawn_y": 50},
            "top": {"target": "Viridian City", "spawn_x": 400, "spawn_y": 550}
        },
        "Viridian City": {
            "bottom": {"target": "Route 1", "spawn_x": 400, "spawn_y": 50},
            "top": {"target": "Route 2", "spawn_x": 400, "spawn_y": 550}
        },
        "Route 2": {
            "bottom": {"target": "Viridian City", "spawn_x": 400, "spawn_y": 50},
            "top": {"target": "Rocket Hideout", "spawn_x": 400, "spawn_y": 550}
        },
        "Rocket Hideout": {
            "bottom": {"target": "Route 2", "spawn_x": 400, "spawn_y": 50}
        }
    }

    # Dimensions
    WIDTH = 800
    HEIGHT = 600
    MARGIN = 32 # Player radius/bounding box

    @staticmethod
    def handle_movement(player, dx, dy):
        """
        Updates player position and checks for edge transitions.
        Returns: {
            "moved": bool,
            "transition": bool,
            "message": str or None,
            "event": dict or None
        }
        """
        # Calculate new pos
        new_x = player.x + dx
        new_y = player.y + dy
        
        transition_occurred = False
        message = None
        event = None

        # Check Bounds and Exits
        loc = player.current_location
        new_loc = None
        
        # Check Top Exit
        if new_y < MapLogic.MARGIN:
            exit_data = MapLogic.EXITS.get(loc, {}).get("top")
            if exit_data:
                # Check Logic Travel (Handles barriers/badges)
                t_res = ExplorationLogic.travel(player, exit_data["target"])
                if t_res["success"]:
                    new_x = exit_data["spawn_x"]
                    new_y = exit_data["spawn_y"]
                    transition_occurred = True
                    message = t_res["message"]
                    event = t_res["event"]
                    new_loc = exit_data["target"]
                else:
                    message = t_res["message"]
                    event = t_res["event"]
                    # Block movement
                    new_y = player.y

        # Check Bottom Exit
        elif new_y > MapLogic.HEIGHT - MapLogic.MARGIN:
            exit_data = MapLogic.EXITS.get(loc, {}).get("bottom")
            if exit_data:
                t_res = ExplorationLogic.travel(player, exit_data["target"])
                if t_res["success"]:
                    new_x = exit_data["spawn_x"]
                    new_y = exit_data["spawn_y"]
                    transition_occurred = True
                    message = t_res["message"]
                    event = t_res["event"]
                    new_loc = exit_data["target"]
                else:
                     message = t_res["message"]
                     event = t_res["event"]
                     new_y = player.y

        # Check Left/Right (not implemented in this vertical slice map, just block)
        if new_x < MapLogic.MARGIN: new_x = MapLogic.MARGIN
        if new_x > MapLogic.WIDTH - MapLogic.MARGIN: new_x = MapLogic.WIDTH - MapLogic.MARGIN
        
        # Ensure Y bounds if no exit triggered
        if not transition_occurred:
            new_y = max(MapLogic.MARGIN, min(MapLogic.HEIGHT - MapLogic.MARGIN, new_y))

        # Update Player
        player.x = new_x
        player.y = new_y
        
        # Random Encounters (Only if moved and not transitioning)
        if not transition_occurred and (dx!=0 or dy!=0) and not event:
            # Chance to encounter: 1 in 200 steps roughly
            # logic.explore uses high chances (0.7) because it was designed for menu "Travel".
            # For continuous movement, we need lower probability per frame.
            if random.random() < 0.01: 
                res = ExplorationLogic.explore(player)
                if res.get("event"):
                    event = res["event"]
                    message = res["message"]

        return {
            "moved": (dx!=0 or dy!=0),
            "transition": transition_occurred,
            "message": message,
            "event": event
        }
