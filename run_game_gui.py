import pygame
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game.ui.window import GameWindow
from game.ui.screens.title_screen import TitleScreen

def main():
    print("Starting Pokemon Python Version (GUI)...")
    
    # Initialize Core
    pygame.init()
    
    # Create Window
    window = GameWindow(800, 600)
    
    # Start at Title Screen
    window.set_screen(TitleScreen)
    
    # Run Loop
    try:
        window.run()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Critical Error: {e}")
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
