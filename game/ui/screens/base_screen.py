class BaseScreen:
    def __init__(self, window):
        self.window = window
        self.manager = window.asset_manager
        self.audio = window.audio_manager
        self.font = self.manager.default_font
        self.small_font = self.manager.small_font
        self.title_font = self.manager.title_font

    def handle_input(self, event):
        """Handle individual pygame events"""
        pass

    def update(self, dt):
        """Update logic, dt is time in milliseconds"""
        pass

    def draw(self, surface):
        """Render to the surface"""
        pass
