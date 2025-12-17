import pygame
from game.ui.asset_manager import AssetManager
from game.audio import AudioManager

class GameWindow:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pokemon Python Version")
        
        # Cursor Setup
        pygame.mouse.set_visible(False)
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.asset_manager = AssetManager()
        self.asset_manager.initialize()
        
        self.audio_manager = AudioManager()
        self.audio_manager.initialize()
        
        # Load Cursor Image
        self.cursor_img = self.asset_manager.get_ui_image("cursor_hand.png")
        
        self.current_screen = None
        # Common data shared across screens (player, verification state)
        self.player = None 

    def set_screen(self, screen_class, **kwargs):
        if self.current_screen:
            # self.current_screen.on_exit() # If we had exit logic
            pass
        self.current_screen = screen_class(self, **kwargs)
        # self.current_screen.on_enter() # If we had enter logic

    def run(self):
        while self.running:
            dt = self.clock.tick(60) # 60 FPS cap
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.current_screen:
                    self.current_screen.handle_input(event)
            
            if self.current_screen:
                self.current_screen.update(dt)
                self.current_screen.draw(self.screen)
            else:
                self.screen.fill((0, 0, 0))
                
            # Draw Custom Cursor
            if self.cursor_img:
                mouse_pos = pygame.mouse.get_pos()
                # Use top-left of image as hotspot by default
                self.screen.blit(self.cursor_img, mouse_pos)
            
            pygame.display.flip()
        
        pygame.quit()
