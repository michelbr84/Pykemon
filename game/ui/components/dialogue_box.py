import pygame

class DialogueBox:
    def __init__(self, manager, window_height):
        self.manager = manager
        self.window_height = window_height
        self.bg = self.manager.get_ui_image("dialogue_box.png")
        self.font = pygame.font.Font(None, 24) # Fallback if manager font not available
        if hasattr(manager, "font"):
             self.font = manager.font
             
        self.visible = False
        self.message = ""
        self.waiting_for_input = False
        
        # Dimensions
        self.height = 180
        self.y_pos = window_height - self.height
        self.text_margin = 40
        
    def show_message(self, message):
        self.message = message
        self.visible = True
        self.waiting_for_input = True
        
    def hide(self):
        self.visible = False
        self.message = ""
        self.waiting_for_input = False
        
    def handle_input(self, event):
        if not self.visible:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_z):
                self.hide()
                return True # Input consumed
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Click anywhere to advance text for now
                self.hide()
                return True
                
        return False # Input not consumed (e.g. movement, but usually we block movement)

    def draw(self, surface):
        if not self.visible:
            return
            
        if self.bg:
            surface.blit(self.bg, (0, self.y_pos))
        else:
            # Fallback black rect
            pygame.draw.rect(surface, (0, 0, 0), (0, self.y_pos, 800, self.height))
            pygame.draw.rect(surface, (255, 255, 255), (0, self.y_pos, 800, self.height), 2)
            
        # Draw Text
        # Simple wrapping or single line for now?
        # Requirement: "Ensure text is visible, readable"
        # We'll implement basic wrapping.
        words = self.message.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            w, h = self.font.size(test_line)
            if w < 720: # 800 width - 2*margin
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))
        
        y_text = self.y_pos + self.text_margin
        for line in lines:
            text_surf = self.font.render(line, True, (0, 0, 0)) # Black text on white box usually
            surface.blit(text_surf, (self.text_margin, y_text))
            y_text += 30
            
        # Draw waiting indicator
        if self.waiting_for_input:
             # Draw a small arrow at bottom right
             pygame.draw.polygon(surface, (255, 0, 0), [(750, self.y_pos + 150), (770, self.y_pos + 150), (760, self.y_pos + 160)])
