import pygame
from game.ui.screens.base_screen import BaseScreen
from game.logic.exploration import ExplorationLogic
from game.ui.components.dialogue_box import DialogueBox

class MapScreen(BaseScreen):
    def __init__(self, window):
        super().__init__(window)
        self.player = window.player
        self.update_map_image()
        
        # Player Rendering
        self.player_pos = [400, 300]
        self.speed = 4
        self.animation_frame = 0
        self.moving = False
        self.facing = "down" # down, up, left, right
        
        # Load Player Sprite
        # Try specific user requested path first, then fallback to asset manager
        # User said: "assets/images/characters/player.png"
        self.player_sprite = self.manager.get_image(["characters", "player.png"])
        if not self.player_sprite:
             # Fallback if file not found exactly there
             self.player_sprite = self.manager.get_sprite("player.png")
        
        # Dialogue Component
        self.dialogue_ui = DialogueBox(self.manager, window.height)
        
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
        # Delegate to dialogue first
        if self.dialogue_ui.visible:
            if self.dialogue_ui.handle_input(event):
                return
            return # Block other input if dialogue is open
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Open Menu (TODO)
                pass
                
    def update(self, dt):
        if self.dialogue_ui.visible:
            return # Pause world while dialogue open
            
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
                 self.dialogue_ui.show_message(res["message"])
                 
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
        else:
            surface.fill((0, 0, 0))
        
        # Draw Player Sprite
        if self.player_sprite:
            # Center the sprite on the position? Or top-left?
            # Assuming sprite is 64x64 and pos is center:
            # rect = self.player_sprite.get_rect(center=(self.player_pos[0], self.player_pos[1]))
            # But earlier logic might have used top-left. Let's stick to center for safety with circle replacement.
            rect = self.player_sprite.get_rect(center=(int(self.player_pos[0]), int(self.player_pos[1])))
            surface.blit(self.player_sprite, rect)
        else:
            # Fallback (User said REMOVE red dot, but if sprite fails, we need something invisble or error?)
            # I will draw a placeholder "sprite missing" or just nothing if strictly following "remove red dot".
            # But "remove red dot" implied "replace with sprite".
            # I'll stick to sprite blit above. If None, nothing draws (Player invisible).
            pass
        
        # Draw UI Overlay (Location Name)
        text = self.title_font.render(self.player.current_location, True, (255, 255, 255))
        surface.blit(text, (20, 20))
        
        # Draw Dialogue
        self.dialogue_ui.draw(surface)
