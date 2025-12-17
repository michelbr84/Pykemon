import pygame
import os

class AssetManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AssetManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def initialize(self):
        if self.initialized:
            return
            
        self.base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "images")
        self.images = {}
        self.fonts = {}
        
        # Initialize default font
        pygame.font.init()
        self.default_font_size = 24
        self.default_font = pygame.font.SysFont("Arial", self.default_font_size)
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 16)
        
        self.initialized = True

    def get_image(self, path_components):
        """
        Load an image from assets/images/path_components.
        path_components can be a string (filename) or a list of directory/files.
        """
        if isinstance(path_components, str):
            path_components = [path_components]
            
        key = "/".join(path_components)
        if key in self.images:
            return self.images[key]
            
        full_path = os.path.join(self.base_path, *path_components)
        
        if not os.path.exists(full_path):
            print(f"CRITICAL ERROR: Image not found at {full_path}")
            # Raise error to stop execution and make it obvious as requested
            raise FileNotFoundError(f"Image not found: {full_path}")
            
        try:
            image = pygame.image.load(full_path).convert_alpha()
            self.images[key] = image
            return image
        except Exception as e:
            print(f"CRITICAL ERROR: Failed to load image {full_path}: {e}")
            raise e

    def get_ui_image(self, filename):
        return self.get_image(["ui", filename])
        
    def get_background(self, filename):
        return self.get_image(["backgrounds", filename])
        
    def get_character(self, filename):
        return self.get_image(["characters", filename])
        
    def get_sprite(self, filename):
        return self.get_image(["sprites", filename])

    def get_item_icon(self, filename):
        return self.get_image(["items", filename])

    def get_type_icon(self, type_name):
        """
        Extracts the specific type icon from type_icons.png sprite sheet.
        Sheet is 288x32, with 9 icons of 32x32.
        Order assumptions: Normal, Fire, Water, Grass, Electric, Rock, Poison, Flying, Dark (approx)
        Adjust mapping based on actual sheet content if needed.
        """
        # Mapping based on standard order or specific to the sheet provided by user
        # User said: 9 icons x 32x32 px.
        # Let's assume a mapping order. If uncertain, we'll verify or just return the whole sheet cropped.
        # Common simplified types in this game: Normal, Fire, Water, Grass, Electric, Rock, Poison, Flying, Dark
        type_order = ["Normal", "Fire", "Water", "Grass", "Electric", "Rock", "Poison", "Flying", "Dark"]
        
        if "type_icons.png" not in self.images:
            self.get_ui_image("type_icons.png")
            
        sheet = self.images.get("ui/type_icons.png")
        if not sheet: return None
        
        try:
            index = type_order.index(type_name)
        except ValueError:
            index = 0 # Default to first if unknown
            
        rect = pygame.Rect(index * 32, 0, 32, 32)
        return sheet.subsurface(rect)
