import pygame
from game.ui.screens.base_screen import BaseScreen
from game.logic.exploration import ExplorationLogic

class MapScreen(BaseScreen):
    def __init__(self, window):
        super().__init__(window)
        self.player = window.player
        self.update_map_image()
        
        # Player position visual state
        # Center of screen for now? Or keep player logic coordinates?
        # Logic has "location" string. We need valid coordinates for a real map.
        # For this modernization, we might need to fake a grid or just show a static screen with a character.
        # Let's assume the maps are 800x600 backgrounds and player moves loosely or just stands there.
        # User requested: "Overworld sprites... Used for map movement"
        # We will implement simple movement within the screen bounds.
        
        self.player_pos = [400, 300]
        self.speed = 4
        self.animation_frame = 0
        self.moving = False
        self.facing = "down" # down, up, left, right
        
        # Map music
        self.play_map_music()
        
    def update_map_image(self):
        # Map location string to filename
        loc = self.player.current_location
        filename = "map_pallet_town.png" # Default
        if "Pallet Town" in loc: filename = "map_pallet_town.png"
        elif "Route 1" in loc: filename = "map_route_1.png"
        elif "Viridian City" in loc: filename = "map_viridian_city.png"
        elif "Route 2" in loc: filename = "map_route_2.png"
        elif "Rocket" in loc: filename = "map_rocket_hideout.png"
        
        try:
            self.bg = self.manager.get_background(filename)
        except Exception as e:
            print(f"Map load failed: {e}")
            self.bg = None
        
    def play_map_music(self):
        loc = self.player.current_location
        track = "pallet_town"
        if "Route" in loc: track = "route"
        elif "City" in loc: track = "city"
        elif "Rocket" in loc: track = "team_rocket"
        elif "Gym" in loc: track = "gym"
        
        self.audio.play_bgm(track)
        
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Open Menu
                pass
                
    def update(self, dt):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -1
            self.facing = "left"
        elif keys[pygame.K_RIGHT]:
            dx = 1
            self.facing = "right"
        elif keys[pygame.K_UP]:
            dy = -1
            self.facing = "up"
        elif keys[pygame.K_DOWN]:
            dy = 1
            self.facing = "down"
            
        if dx != 0 or dy != 0:
            self.moving = True
            # Update animation
            self.animation_frame += dt * 0.01

            # Use MapLogic
            from game.logic.map_logic import MapLogic
            res = MapLogic.handle_movement(self.player, dx * self.speed, dy * self.speed)
            
            # Sync local pos for rendering
            self.player_pos[0] = self.player.x
            self.player_pos[1] = self.player.y
            
            if res["transition"]:
                # Map changed
                self.update_map_image()
                self.play_map_music()
                
            if res["message"]:
                 # Ideally show a toast or dialogue
                 print(res["message"]) 
                 
            if res["event"] and res["event"]["type"] == "battle":
                 # Transition to Battle Screen
                 from game.ui.screens.battle_screen import BattleScreen
                 self.window.set_screen(BattleScreen, encounter_event=res["event"])
                
        else:
            self.moving = False
            self.animation_frame = 0

    def check_encounter(self):
        # Call existing logic
        res = ExplorationLogic.explore(self.player)
        if res.get("event") and res["event"]["type"] == "battle":
            # Transition to Battle Screen
             from game.ui.screens.battle_screen import BattleScreen
             self.window.set_screen(BattleScreen, encounter_event=res["event"])

    def draw(self, surface):
        if self.bg:
            bg_scaled = pygame.transform.scale(self.bg, (self.window.width, self.window.height))
            surface.blit(bg_scaled, (0, 0))
        
        # Draw Player
        # Need character sprites: e.g. "player_down_1.png"
        # User provided: "assets/images/characters/"
        # We assume standard naming or just one file for now.
        # Plan says: "Overworld sprites: 64x64 px"
        # Let's try to load "hero_run_down_0.png" or similar if we knew the names.
        # User just said: `assets/images/characters/` exists.
        # We'll try generic names like "Red_down.png" or just reuse a placeholder if specific names unknown.
        # Actually, let's look at what files are in characters folder in next step or assume "player.png"?
        # User request didn't list specific character filenames, just resolution.
        # We'll use a placeholder colored rect if sprite load fails, or try "ash.png".
        
        # Simulating Sprite Animation
        sprite_name = "player_walk.png" # Placeholder
        # We'll just draw a Circle for the player if we don't have the exact filename right now
        # Actually we should use the asset manager to safely get a placeholder.
        
        color = (255, 0, 0)
        pygame.draw.circle(surface, color, (int(self.player_pos[0]), int(self.player_pos[1])), 16)
        
        # Draw UI Overlay (Location Name)
        text = self.title_font.render(self.player.current_location, True, (255, 255, 255))
        surface.blit(text, (20, 20))
