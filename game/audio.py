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
        # Mapping logical names to physical filenames as per user spec
        self.sfx_files = {
            # Menu
            "menu_select": "sfx_select.mp3",
            "menu_confirm": "sfx_confirm.mp3",
            "menu_cancel": "sfx_cancel.mp3", 
            "bump": "sfx_bump.mp3",
            "save": "sfx_save.mp3",
            
            # Battle
            "tackle": "sfx_tackle.mp3",
            "ember": "sfx_ember.mp3",
            "water_gun": "sfx_water_gun.mp3",
            "vine_whip": "sfx_vine_whip.mp3",
            "electric": "sfx_electric.mp3",
            "rock_smash": "sfx_rock_smash.mp3",
            "poison": "sfx_poison.mp3",
            "faint": "sfx_faint.mp3",
            "run": "sfx_run.mp3",
            "pokeball_throw": "sfx_pokeball_throw.mp3",
            "pokeball_shake": "sfx_pokeball_shake.mp3",
            "pokeball_catch": "sfx_pokeball_catch.mp3", 
            "pokeball_break": "sfx_pokeball_break.mp3",
            "level_up": "sfx_level_up.mp3",
            
            # Misc
            "heal": "sfx_heal.mp3",
            "item_get": "sfx_item_get.mp3",
            "evolution_complete": "sfx_evolution_complete.mp3"
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
