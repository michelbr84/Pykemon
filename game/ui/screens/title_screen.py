import pygame
import sys
from game.ui.screens.base_screen import BaseScreen
from game.models.pokemon import Pokemon
from game.models.trainer import Player
from game.state import GameState

class TitleScreen(BaseScreen):
    def __init__(self, window):
        super().__init__(window)
        self.bg = self.manager.get_background("bg_title_screen.png")
        self.options = ["New Game", "Load Game", "Quit"]
        self.selected_index = 0
        self.audio.play_bgm("title")
        
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
                self.audio.play_sfx("menu_select") # Assuming generic sfx name, or need to verify file
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)
                self.audio.play_sfx("menu_select")
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.audio.play_sfx("menu_confirm") # Assuming generic sfx name
                self.select_option()

    def select_option(self):
        choice = self.options[self.selected_index]
        if choice == "New Game":
            self.start_new_game()
        elif choice == "Load Game":
            self.load_game_screen() # Simplified: just load "Ash" for now or show input
        elif choice == "Quit":
            self.window.running = False

    def start_new_game(self):
        # Create default starter
        starter = Pokemon("Pyron", level=5)
        self.window.player = Player("Ash", [starter])
        self.window.player.current_location = "Pallet Town"
        
        # Import here to avoid circular dependency
        from game.ui.screens.map_screen import MapScreen
        self.window.set_screen(MapScreen)

    def load_game_screen(self):
        # For this verification phase, try loading "Ash.json" directly
        player, msg = GameState.load_game("Ash.json")
        if player:
            self.window.player = player
            from game.ui.screens.map_screen import MapScreen
            self.window.set_screen(MapScreen)
        else:
            print(f"Load failed: {msg}")

    def update(self, dt):
        pass

    def draw(self, surface):
        # Draw BG centered/scaled
        if self.bg:
            bg_scaled = pygame.transform.scale(self.bg, (self.window.width, self.window.height))
            surface.blit(bg_scaled, (0, 0))
        else:
            surface.fill((50, 50, 150))
            
        # Draw Title Text (using system font for now if logo not in BG)
        # title_surf = self.title_font.render("Pokemon Python", True, (255, 255, 0))
        # surface.blit(title_surf, (self.window.width//2 - title_surf.get_width()//2, 100))
        
        # Draw Options
        start_y = 400
        for i, option in enumerate(self.options):
            color = (255, 255, 255)
            if i == self.selected_index:
                color = (255, 0, 0) # Highlight selected
                
            text_surf = self.title_font.render(option, True, color)
            rect = text_surf.get_rect(center=(self.window.width//2, start_y + i * 60))
            
            # Draw shadow
            shadow_surf = self.title_font.render(option, True, (0, 0, 0))
            shadow_rect = shadow_surf.get_rect(center=(self.window.width//2 + 2, start_y + i * 60 + 2))
            surface.blit(shadow_surf, shadow_rect)
            
            surface.blit(text_surf, rect)
            
            # Draw cursor/hand if selected
            if i == self.selected_index:
                cursor = self.manager.get_ui_image("cursor_hand.png")
                if cursor:
                    # Align cursor to left of text
                    c_rect = cursor.get_rect(midright=(rect.left - 10, rect.centery))
                    surface.blit(cursor, c_rect)
