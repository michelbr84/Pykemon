import pygame
import os

class AudioManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AudioManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def initialize(self):
        if self.initialized:
            return
        
        pygame.mixer.init()
        self.music_volume = 0.5
        self.sfx_volume = 0.7
        pygame.mixer.music.set_volume(self.music_volume)
        
        self.base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sounds")
        
        # Track mapping to filenames
        self.music_tracks = {
            "title": "bgm_title.mp3",
            "pallet_town": "bgm_pallet_town.mp3",
            "route": "bgm_route.mp3", 
            "city": "bgm_city.mp3",
            "gym": "bgm_gym.mp3",
            "team_rocket": "bgm_team_rocket.mp3",
            "battle_wild": "bgm_battle_wild.mp3",
            "battle_trainer": "bgm_battle_trainer.mp3",
            "battle_gym": "bgm_battle_gym.mp3",
            "victory": "bgm_victory.mp3",
            "evolution": "bgm_evolution.mp3"
        }
        
        # Preload SFX if needed, or load on demand
        self.sfx_cache = {}
        self.sfx_files = {
            # Add specific SFX mappings here if they have specific names, 
            # otherwise we can try to load by filename directly
        }
        
        self.current_track = None
        self.initialized = True

    def play_bgm(self, track_key):
        if not self.initialized: return
        
        if track_key not in self.music_tracks:
            print(f"Warning: Music track '{track_key}' not found.")
            return

        if self.current_track == track_key:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
            return

        filename = self.music_tracks[track_key]
        path = os.path.join(self.base_path, "music", filename)
        
        if not os.path.exists(path):
            print(f"Warning: Music file not found at {path}")
            return
            
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(-1) # Loop indefinitely
            self.current_track = track_key
        except Exception as e:
            print(f"Error playing music {track_key}: {e}")

    def stop_bgm(self):
        if not self.initialized: return
        pygame.mixer.music.stop()
        self.current_track = None

    def fade_out_bgm(self, duration=1000):
        if not self.initialized: return
        pygame.mixer.music.fadeout(duration)
        self.current_track = None

    def play_sfx(self, sfx_name):
        if not self.initialized: return
        
        # Determine path - sfx_name could be a key in sfx_files or a raw filename (without .mp3)
        filename = self.sfx_files.get(sfx_name, f"{sfx_name}.mp3")
        
        if sfx_name not in self.sfx_cache:
            path = os.path.join(self.base_path, "sfx", filename)
            if not os.path.exists(path):
                # Try checking if sfx_name already included extension
                if filename.endswith(".mp3"):
                     path = os.path.join(self.base_path, "sfx", sfx_name)
                
                if not os.path.exists(path):
                    print(f"Warning: SFX file not found at {path}")
                    return None
            
            try:
                sound = pygame.mixer.Sound(path)
                sound.set_volume(self.sfx_volume)
                self.sfx_cache[sfx_name] = sound
            except Exception as e:
                print(f"Error loading SFX {sfx_name}: {e}")
                return

        try:
            self.sfx_cache[sfx_name].play()
        except Exception as e:
            print(f"Error playing SFX {sfx_name}: {e}")
