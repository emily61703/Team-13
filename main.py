# main.py: This is the main entry point of our program! We are handling the
#          splash screen and transitioning to the login screen

from tkinter import Tk, Label
from PIL import Image, ImageTk
from login_screen import show_login_screen
from sfx_system import soundsystem

# Config
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
SPLASH_DURATION = 3000
LOGO_SCALE = 0.75  # means logo is 50% it's original size

def main():
    # Create the splash window
    splash_window = Tk()
    splash_window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    splash_window.title("PHOTON - The Ultimate Game on Planet Earth")
    splash_window.configure(bg="black")
    
    # play startup sound (Disabled because sound files are corrupted)
    #soundsystem.play_game_sound('start')
    

    # Open the image file
    image = Image.open("assets/logo.jpg")

    # Scale/resize image
    img_width, img_height = image.size
    scale = min(WINDOW_WIDTH / img_width, WINDOW_HEIGHT / img_height) * LOGO_SCALE
    new_width = int(img_width * scale)
    new_height = int(img_height * scale)

    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    img = ImageTk.PhotoImage(resized_image)

    # Display image
    splash_label = Label(splash_window, image=img, bg="black")
    splash_label.place(relx=0.5, rely=0.5, anchor="center")

    def transition_to_login():
        # Play exit sound and transition to login screen
        # soundsystem.play_game_sound('exit') - Disabled
        # soundsystem.cleanup() - Disabled
        splash_window.destroy()
        show_login_screen()

    splash_window.after(SPLASH_DURATION, transition_to_login)
    splash_window.mainloop()

if __name__ == "__main__":
    main()
