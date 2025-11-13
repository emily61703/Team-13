# music_select.py: Module for selecting and playing background music tracks

import pygame
import os
import random
from tkinter import Toplevel, Listbox, Button, Label, Frame, MULTIPLE, END, messagebox

class MusicSelector:
    def __init__(self, music_folder="assets/music/"):
        """Initialize the music selector"""
        try:
            pygame.mixer.init()
            # only mark initialized if pygame reports it's actually initialized
            if pygame.mixer.get_init():
                self._mixer_initialized = True
                try:
                    pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
                except Exception:
                    pass
            else:
                self._mixer_initialized = False
        except Exception as e:
            print(f"Warning: pygame.mixer.init() failed: {e}")
            self._mixer_initialized = False
        
        self.music_folder = music_folder
        self.all_tracks = self.load_tracks()
        self.selected_tracks = []
        self.current_track_index = 0
        self.is_playing = False

        # NEW: ensure music starts once when countdown crosses threshold
        self._started_on_countdown = False
        
        # Set up event for when music ends (only if mixer initialized)
        if self._mixer_initialized:
            try:
                pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
            except Exception:
                pass
        
    def load_tracks(self):
        """Load all music files from folder"""
        if not os.path.exists(self.music_folder):
            os.makedirs(self.music_folder)
            return []
        
        music_extensions = ('.mp3', '.ogg', '.wav')
        tracks = []
        
        for file in os.listdir(self.music_folder):
            if file.lower().endswith(music_extensions):
                full_path = os.path.join(self.music_folder, file)
                display_name = os.path.splitext(file)[0]  # Remove extension
                tracks.append({
                    "path": full_path, 
                    "name": display_name,
                    "filename": file
                })
        
        return sorted(tracks, key=lambda x: x["name"])
    
    def show_selection_window(self, parent=None):
        """Display a window for selecting tracks"""
        if not self.all_tracks:
            messagebox.showinfo(
                "No Music Found",
                f"No Music files found in '{self.music_folder}' folder.\n\n"
                "Please add .mp3, .ogg, or .wav files to the music folder."
            )
            return
        
        # Create selection window
        window = Toplevel(parent)
        window.title("Select Music Tracks")
        window.geometry("500x600")
        window.configure(bg="black")
        
        # Title
        title_label = Label(
            window, 
            text="Select Music Tracks to Play",
            font=("Helvetica", 16, "bold"),
            fg="white",
            bg="black"
        )
        title_label.pack(pady=10)
        
        # Instructions
        instructions = Label(
            window,
            text="Hold Ctrl/Cmd to select multiple tracks\nSelected tracks will play randomly during the game",
            font=("Helvetica", 10),
            fg="gray",
            bg="black"
        )
        instructions.pack(pady=5)
        
        # Listbox frame
        listbox_frame = Frame(window, bg="black")
        listbox_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Listbox for tracks
        listbox = Listbox(
            listbox_frame,
            selectmode=MULTIPLE,
            font=("Helvetica", 12),
            bg="#1a1a1a",
            fg="white",
            selectbackground="#0066cc",
            height=15
        )
        listbox.pack(side="left", fill="both", expand=True)
        
        # Populate listbox
        for track in self.all_tracks:
            listbox.insert(END, track["name"])
        
        # Select all by default
        for i in range(len(self.all_tracks)):
            listbox.select_set(i)
        
        # Status label
        status_label = Label(
            window,
            text=f"{len(self.all_tracks)} tracks available",
            font=("Helvetica", 10),
            fg="lightgreen",
            bg="black"
        )
        status_label.pack(pady=5)
        
        # Button frame
        button_frame = Frame(window, bg="black")
        button_frame.pack(pady=10)
        
        def select_all():
            listbox.select_set(0, END)
        
        def deselect_all():
            listbox.selection_clear(0, END)
        
        def confirm_selection():
            selected_indices = listbox.curselection()
            
            if not selected_indices:
                messagebox.showwarning(
                    "No Selection",
                    "Please select at least one track!"
                )
                return
            
            self.selected_tracks = [self.all_tracks[i] for i in selected_indices]
            
            messagebox.showinfo(
                "Success",
                f"{len(self.selected_tracks)} track(s) selected!\n"
                "Music will play randomly during the game."
            )
            
            window.destroy()
        
        # Buttons
        Button(
            button_frame,
            text="Select All",
            command=select_all,
            fg="green",
            width=12
        ).pack(side="left", padx=5)
        
        Button(
            button_frame,
            text="Deselect All",
            command=deselect_all,
            fg="orange",
            width=12
        ).pack(side="left", padx=5)
        
        Button(
            button_frame,
            text="Confirm Selection",
            command=confirm_selection,
            fg="blue",
            font=("Helvetica", 10, "bold"),
            width=15
        ).pack(side="left", padx=5)
        
        Button(
            button_frame,
            text="Close",
            command=window.destroy,
            fg="red",
            width=12
        ).pack(side="left", padx=5)
    
    def ensure_mixer_initialized(self):
        """Try to initialize the pygame mixer on demand. Returns True if ready."""
        if getattr(self, "_mixer_initialized", False) and pygame.mixer.get_init():
            return True
        try:
            pygame.mixer.init()
            if pygame.mixer.get_init():
                try:
                    pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
                except Exception:
                    pass
                self._mixer_initialized = True
                return True
            else:
                self._mixer_initialized = False
                return False
        except Exception as e:
            print(f"Could not initialize mixer: {e}")
            self._mixer_initialized = False
            return False

    def play_random_track(self):
        """Play a random track from selected tracks"""
        if not self.selected_tracks:
            return

        # ensure mixer is ready, having mixer errors but they are handled 
        if not self.ensure_mixer_initialized():
            print("Mixer not initialized; cannot play music.")
            return

        try:
            # double-check mixer state before calling load/play
            if not pygame.mixer.get_init():
                raise RuntimeError("mixer not initialized")
            track = random.choice(self.selected_tracks)
            pygame.mixer.music.load(track["path"])
            pygame.mixer.music.play()
            self.is_playing = True
            print(f"Now playing: {track['name']}")
        except Exception as e:
            print(f"Error playing music: {e}")
            self.is_playing = False
            # if mixer was quit externally, mark for re-init on next attempt
            if "mixer not initialized" in str(e).lower() or isinstance(e, RuntimeError):
                self._mixer_initialized = False

    def play_random_track_with_retry(self):
        """Wrapper that plays music and retries after re-initializing mixer if needed"""
        if not self.selected_tracks:
            return

        # First attempt
        self.play_random_track()

        # If failed due to mixer, retry once after re-init
        if not self.is_playing:
            print("First attempt failed; re-initializing mixer...")
            self._mixer_initialized = False
            if self.ensure_mixer_initialized():
                print("Mixer re-initialized; retrying playback...")
                self.play_random_track()

    def stop_music(self):
        """Stop playing music (safe if mixer not initialized)"""
        try:
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
        except Exception as e:
            print(f"Warning stopping music: {e}")
        finally:
            # Always clear the playing flag so future start_music() calls work
            self.is_playing = False
    
    def set_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        pygame.mixer.music.set_volume(volume)
    
    def check_music_events(self, event):
        if event.type == pygame.USEREVENT + 1:
            self.play_random_track()

    def trigger_on_countdown(self, remaining_seconds, threshold=15):
        """
        Start music once when remaining_seconds <= threshold.
        This is so I can line up the game clock with the start music, off by like one second
        """
        try:
            remaining = int(remaining_seconds)
        except Exception:
            return

        if remaining <= threshold and not self._started_on_countdown:
            if not self.selected_tracks:
                self.selected_tracks = self.all_tracks
            self.play_random_track_with_retry()
            self._started_on_countdown = True

    def reset_countdown_trigger(self):
        """Reset the internal countdown-start flag for a new run."""
        self._started_on_countdown = False


# Global music selector instance
music_selector = MusicSelector()


def show_music_selector(parent=None):
    """Convenience function to show music selector"""
    music_selector.show_selection_window(parent)


def start_music():
    """Start playing selected music (do not restart if already playing)"""
    # avoid restarting if already playing
    if music_selector.is_playing:
        return

    # ensure mixer ready before attempting to start
    if not music_selector.ensure_mixer_initialized():
        print("Mixer not available; cannot start music.")
        return

    if music_selector.selected_tracks:
        music_selector.play_random_track_with_retry()
    else:
        # Default: select all tracks
        music_selector.selected_tracks = music_selector.all_tracks
        music_selector.play_random_track_with_retry()


def stop_music():
    """Stop playing music"""
    music_selector.stop_music()


def trigger_music_on_countdown(remaining_seconds, threshold=15):
    """Wrapper for use by external code (e.g. the Tk countdown)."""
    music_selector.trigger_on_countdown(remaining_seconds, threshold)

def reset_music_countdown_trigger():
    """Wrapper to reset the countdown trigger between runs."""
    music_selector.reset_countdown_trigger()