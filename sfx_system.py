import pygame
import os
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SFXSystem:
    """Game Sound Effects System"""
    GAME_SOUNDS = {} # Removed since these are corrupted
    HELMET_SOUNDS = {        'hit': 'assets/sounds/helmet/hit.wav',
        'gethit': 'assets/sounds/helmet/gethit.wav',
        'hitown': 'assets/sounds/helmet/hitown.wav',
        'miss': 'assets/sounds/helmet/miss.wav',
        'reset': 'assets/sounds/helmet/reset.wav'}
    def __init__(self, enable_audio=True):
        """enable the sound effects system"""
        self.enable_audio = enable_audio
        self.pygame_initialized = False
        self.loaded_sounds = {}
        self.current_channel = None
        
        if self.enable_audio:
            self._init_pygame()
            self._load_sounds()
            
    def _init_pygame(self):
        """Initialize pygame mixer"""
        try:
            pygame.mixer.init()
            self.pygame_initialized = True
            logger.info("Pygame mixer initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize pygame mixer: {e}")
            self.pygame_initialized = False
            self.enable_audio = False
            
    def _load_sounds(self):
        """Load all sound effects"""
        all_sounds = {**self.GAME_SOUNDS, **self.HELMET_SOUNDS}
        
        for sound_name, sound_path in all_sounds.items():
            try:
                if os.path.exists(sound_path):
                    sound = pygame.mixer.Sound(sound_path)
                    self.loaded_sounds[sound_name] = sound
                    logger.info(f"Loaded sound: {sound_name}")
                else:
                    logger.warning(f"Sound file not found: {sound_path}")
            except Exception as e:
                logger.warning(f"Failed to load sound '{sound_name}': {e}")
        
    def play_game_sound(self, sound_key: str, wait=False):
        """Play a game sound effect by key"""
        
        if not self.enable_audio or not self.pygame_initialized:
            return
        
        if sound_key not in self.loaded_sounds:
            logger.warning(f"Sound not found: {sound_key}")
            return
        
        try:
            sound = self.loaded_sounds[sound_key]
            channel = pygame.mixer.find_channel()
            if channel:
                channel.play(sound)
                logger.info(f"Playing game sound: {sound_key}")
                
                if wait:
                    # Wait for sound to finish (blocking)
                    while channel.get_busy():
                        pygame.time.delay(10)
        except Exception as e:
            logger.error(f"Error playing sound '{sound_key}': {e}")
    def play_helmet_sound(self, sound_key: str, wait=False):
        """Play a helmet sound effect by key"""
        
        if not self.enable_audio or not self.pygame_initialized:
            return
        
        if sound_key not in self.loaded_sounds:
            logger.warning(f"Sound not found: {sound_key}")
            return
        
        try:
            sound = self.loaded_sounds[sound_key]
            channel = pygame.mixer.find_channel()
            if channel:
                channel.play(sound)
                logger.info(f"Playing helmet sound: {sound_key}")
                
                if wait:
                    # Wait for sound to finish (blocking)
                    while channel.get_busy():
                        pygame.time.delay(10)
        except Exception as e:
            logger.error(f"Error playing sound '{sound_key}': {e}")
    
    def stop_all_sounds(self):
        if self.enable_audio and self.pygame_initialized:
            pygame.mixer.stop()
            logger.info("All sounds stopped.")
    
    def cleanup(self):
        """Cleanup pygame mixer"""
        if self.enable_audio and self.pygame_initialized:
            pygame.mixer.quit()
            logger.info("Pygame mixer quit.")
    
    def get_sound_duration(self, sound_key: str) -> Optional[float]:
        """Get the duration of sound"""
        if sound_key not in self.loaded_sounds:
            return 0.0
        try:
            return self.loaded_sounds[sound_key].get_length()
        except Exception as e:
            logger.error(f"Error getting sound duration: {e}")
            return 0.0
        
soundsystem = SFXSystem(enable_audio=True)
