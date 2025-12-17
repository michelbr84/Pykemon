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
                # Placeholder for menu if needed, but we use shortcuts now
                self.dialogue_ui.show_message("Menu not implemented. Use 'S' to Save.")
            elif event.key == pygame.K_g:
                # Challenge Gym Shortcut
                if "Viridian City" in self.player.current_location:
                    from game.logic.exploration import ExplorationLogic
                    res = ExplorationLogic.challenge_gym(self.player)
                    if res["success"]:
                        self.dialogue_ui.show_message(res["message"])
                         # Wait for dialogue close to trigger battle? 
                         # DialogueBox currently "hides" on input. 
                         # We need a callback or queue system? 
                         # Actually MapScreen.update checks res["event"]. 
                         # Here we are bypassing update() logic.
                         # We should duplicate the event handling from update.
                        if res.get("event") and res["event"]["type"] == "battle":
                             from game.ui.screens.battle_screen import BattleScreen
                             # We can't switch immediately if we want to show the message.
                             # But DialogueBox blocks update.
                             # Simple solution: Show message, and hook the callback? 
                             # Or just switch immediately. "Prepare for battle!" might be lost.
                             # Let's switch immediately for stability, or implement a delay.
                             # Better: Check existing update logic `res` handling. 
                             # `update` handles map movement results. This is manual trigger.
                             self.window.set_screen(BattleScreen, encounter_event=res["event"])
                    else:
                        self.dialogue_ui.show_message(res["message"])
                else:
                    self.dialogue_ui.show_message("There is no Gym here.")
                    
            elif event.key == pygame.K_s:
                # Save Game
                from game.state import GameState
                success, msg = GameState.save_game(self.player)
                self.dialogue_ui.show_message(msg)
                
            elif event.key == pygame.K_h:
                # Heal Party
                # Logic check: usually only at Center. But simplified for now:
                # If only in cities? Or everywhere? Guide instructions will clarify ("At Pokemon Centers... implemented as shortcut H in cities").
                # Let's allow H everywhere for "usability" or strictness? 
                # User prompted "How to unlock...". Let's say H works in Towns.
                loc = self.player.current_location
                if "Town" in loc or "City" in loc:
                     self.player.heal_all_pokemon()
                     self.dialogue_ui.show_message("Your party has been fully healed!")
                else:
                     self.dialogue_ui.show_message("Can only heal in Towns/Cities.")
                
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
                
                # Check for Controls Tutorial (One-time)
                if "Viridian City" in self.player.current_location:
                    if not self.player.story_flags.get("seen_controls_viridian"):
                        self.player.story_flags["seen_controls_viridian"] = True
                        msg = "CONTROLS: Arrow Keys to Move | [G] Challenge Gym | [H] Heal Party | [S] Save Game"
                        self.dialogue_ui.show_message(msg)
                        res["message"] = None # Suppress "Traveled to..." message
                
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
