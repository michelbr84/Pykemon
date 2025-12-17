import pygame
from game.ui.screens.base_screen import BaseScreen
from game.logic.battle import Battle

class BattleScreen(BaseScreen):
    def __init__(self, window, encounter_event):
        super().__init__(window)
        
        # Setup Battle Logic
        self.battle = Battle(
            window.player, 
            encounter_event["opponent"], 
            is_wild=encounter_event["is_wild"]
        )
        self.encounter_event = encounter_event
        
        # Determine Background
        # Logic: If wild, maybe 'battle_grass', if city 'battle_city'. Defaults to grass.
        loc = window.player.current_location
        bg_name = "battle_grass.png"
        if "City" in loc: bg_name = "battle_city.png"
        elif "Cave" in loc: bg_name = "battle_cave.png"
        elif "Indoor" in loc or "Gym" in loc: bg_name = "battle_indoor.png"
        
        self.bg = self.manager.get_image(["backgrounds", bg_name])
        
        # UI Elements
        self.dialogue_box = self.manager.get_ui_image("dialogue_box.png")
        self.hp_frame = self.manager.get_ui_image("hp_bar_frame.png")
        self.hp_green = self.manager.get_ui_image("hp_bar_fill_green.png")
        self.hp_yellow = self.manager.get_ui_image("hp_bar_fill_yellow.png")
        self.hp_red = self.manager.get_ui_image("hp_bar_fill_red.png")
        self.cursor = self.manager.get_ui_image("cursor_hand.png")
        self.menu_box = self.manager.get_ui_image("battle_menu_box.png")
        
        # State
        self.state = "INTRO" # INTRO, MAIN_MENU, MOVE_MENU, BAG_MENU, POKEMON_MENU, ANIMATING, TEXT_WAIT, FINISHED
        self.message_queue = list(self.battle.logs) # Start with intro logs
        self.battle.logs = [] # Clear logic logs
        self.current_message = ""
        self.message_timer = 0
        self.waiting_for_input = False
        
        # Layout Constants
        self.opp_pos = (500, 50)
        self.player_pos = (50, 250)
        
        # Music
        track = "battle_wild"
        if not encounter_event["is_wild"]:
            track = "battle_trainer"
            if "Gym" in window.player.current_location: track = "battle_gym"
            # Special check for Rocket/Rival if identifiable
            if "Rocket" in window.player.current_location: track = "team_rocket"
            
        self.audio.play_bgm(track)
        
        # Advance first message
        self.next_message()

    def next_message(self):
        if self.message_queue:
            self.current_message = self.message_queue.pop(0)
            self.waiting_for_input = True
        else:
            if self.battle.finished:
                self.end_battle()
            else:
                self.state = "MAIN_MENU"

    def end_battle(self):
        # Result handling
        if self.battle.won:
            if self.encounter_event.get("flag_on_win"):
                self.window.player.story_flags[self.encounter_event["flag_on_win"]] = True
            
            # Transition back to Map
            self.audio.play_bgm("victory") # Brief victory tune?
            # Ideally wait a bit then switch
            # For now, immediate switch after last text input
            from game.ui.screens.map_screen import MapScreen
            self.window.set_screen(MapScreen)
        else:
             # Lost - in Pokemon usually Whiteout -> Center. Simple restart for now?
             # Logic says "You lost...".
             # Restore sanity or just reload Map at start
             # For modernization polish: Heal and warp to Pallet Town
             self.window.player.heal_all_pokemon()
             self.window.player.current_location = "Pallet Town"
             from game.ui.screens.map_screen import MapScreen
             self.window.set_screen(MapScreen)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_z:
                if self.waiting_for_input:
                    self.waiting_for_input = False
                    self.next_message()
                    return
                
                # Menus
                if self.state == "MAIN_MENU":
                    # 1. Fight, 2. Bag, 3. Poke, 4. Run
                    # Simplified selection: 1,2,3,4 number keys or arrow keys?
                    # Let's use numeric for simplicity in prototype, or simple index
                    pass

    # We'll use a simple index for menus
    selection_index = 0
    
    def handle_input(self, event):
        if event.type != pygame.KEYDOWN: return
        
        key = event.key
        
        if self.waiting_for_input:
            if key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_z):
                self.waiting_for_input = False
                self.next_message()
            return
            
        if self.state == "MAIN_MENU":
            if key == pygame.K_1: # Fight
                self.state = "MOVE_MENU"
            elif key == pygame.K_2: # Bag
                # TODO: Bag Implementation
                self.message_queue.append("Bag not implemented yet!")
                self.next_message()
            elif key == pygame.K_3: # Pokemon
                 # TODO: Switch Implementation
                self.message_queue.append("Switch not implemented yet!")
                self.next_message()
            elif key == pygame.K_4: # Run
                res = self.battle.execute_turn(("run",))
                self.process_turn_result(res)
                
        elif self.state == "MOVE_MENU":
            moves = self.battle.active_player_mon.moves
            if key == pygame.K_1 and len(moves) >= 1:
                self.do_move(moves[0])
            elif key == pygame.K_2 and len(moves) >= 2:
                self.do_move(moves[1])
            elif key == pygame.K_3 and len(moves) >= 3:
                self.do_move(moves[2])
            elif key == pygame.K_4 and len(moves) >= 4:
                self.do_move(moves[3])
            elif key == pygame.K_ESCAPE or key == pygame.K_x:
                self.state = "MAIN_MENU"

    def do_move(self, move_name):
        res = self.battle.execute_turn(("fight", move_name))
        self.process_turn_result(res)

    def process_turn_result(self, res):
        self.message_queue.extend(res['logs'])
        self.state = "TEXT_WAIT"
        self.next_message()

    def update(self, dt):
        pass

    def draw(self, surface):
        # Draw BG
        if self.bg:
            bg_scaled = pygame.transform.scale(self.bg, (800, 600))
            surface.blit(bg_scaled, (0,0))
            
        # Draw Opponent
        opp_mon = self.battle.active_opponent_mon
        opp_sprite = self.manager.get_sprite(f"{opp_mon.species.lower()}_front.png")
        if opp_sprite:
             # Scale if needed? spec says 256x256. 
             # Opponent Position: Top Right (500, 50)
             surface.blit(opp_sprite, self.opp_pos)
             
        # Draw Player Pokemon
        player_mon = self.battle.active_player_mon
        player_sprite = self.manager.get_sprite(f"{player_mon.species.lower()}_back.png")
        if player_sprite:
             # Player Position: Bottom Left (50, 250) (Base Y 600 - 180 (dialogue) - 256?)
             # Actually Dialogue is 180px tall. Screen 600. Dialogue starts at 420.
             # Player sprite bottom should be around 420.
             # 420 - 256 = 164. So Y=164 is too high.
             # Let's adjust positions:
             # Opponent: Right side, Y=50.
             # Player: Left side, Y=200.
             surface.blit(player_sprite, self.player_pos)
             
        # Draw Dialogue Box
        if self.dialogue_box:
             surface.blit(self.dialogue_box, (0, 600 - 180))
             
        # Draw Text
        if self.current_message:
            # Wrap text?
            text_surf = self.font.render(self.current_message, True, (0, 0, 0))
            surface.blit(text_surf, (40, 600 - 140))
        elif self.state == "MAIN_MENU":
            # Draw Menu Box
            if self.menu_box:
                surface.blit(self.menu_box, (480, 600 - 180 - 200 + 40)) # Arbitrary placement
                
            # Draw Options
            menu_x = 520
            menu_y = 300
            options = ["1. Fight", "2. Bag", "3. PKMN", "4. Run"]
            for i, opt in enumerate(options):
                txt = self.font.render(opt, True, (0, 0, 0))
                surface.blit(txt, (menu_x, menu_y + i * 40))
                
        elif self.state == "MOVE_MENU":
             # Draw Moves
             menu_x = 40
             menu_y = 600 - 140
             moves = self.battle.active_player_mon.moves
             for i, m in enumerate(moves):
                 txt = self.font.render(f"{i+1}. {m}", True, (0, 0, 0))
                 surface.blit(txt, (menu_x, menu_y + i * 30))
                 
        # Draw HP Bars
        self.draw_hp_bar(surface, opp_mon, 50, 50, is_opponent=True)
        self.draw_hp_bar(surface, player_mon, 500, 350, is_opponent=False) # Positions guessed

    def draw_hp_bar(self, surface, mon, x, y, is_opponent):
        # Name
        name_txt = self.font.render(mon.species, True, (0, 0, 0))
        surface.blit(name_txt, (x, y - 30))
        
        # Level
        lvl_txt = self.small_font.render(f"Lv{mon.level}", True, (0, 0, 0))
        surface.blit(lvl_txt, (x + 150, y - 30))
        
        # Frame
        if self.hp_frame:
            surface.blit(self.hp_frame, (x, y))
            
        # Fill
        ratio = mon.current_hp / mon.max_hp
        fill_width = int(196 * ratio) # 196 is max fill width from spec
        
        fill_img = self.hp_green
        if ratio < 0.2: fill_img = self.hp_red
        elif ratio < 0.5: fill_img = self.hp_yellow
        
        if fill_img and fill_width > 0:
            # Scale or subsection? Spec says "hp_bar_fill_green.png -> 196x20 px"
            # It's a full bar image. We should crop it or scale it.
            # Crop is better for "bar" effect usually.
            # area = (0, 0, fill_width, 20)
            surface.blit(fill_img, (x + 2, y + 2), (0, 0, fill_width, 20)) # Offset for frame
            
        # HP Text (Player only usually)
        if not is_opponent:
            hp_txt = self.small_font.render(f"{mon.current_hp}/{mon.max_hp}", True, (0, 0, 0))
            surface.blit(hp_txt, (x + 50, y + 25))
