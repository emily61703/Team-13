# Login Page with Splash Screen

# Login Page
    # Enter numerical code
    # If a name is found in the database to match it, it fills it in
    # If a name is not found, allow for the entry of one
    # After a name is found/entered, pop up to enter the hardware code

# Import module
from tkinter import *
from PIL import Image, ImageTk

# Create object
splash_root = Tk()

# Adjust size
width = 400
height = 400
screen_size = str(width)+'x'+str(height)
splash_root.geometry(screen_size)

# Attributes
image = Image.open("logo.jpg")
resized_image = image.resize((width, height))
img = ImageTk.PhotoImage(resized_image)

# Set Label
splash_label = Label(splash_root, image=img)
splash_label.pack()

# main window function
def main():
    # destroy splash window
    splash_root.destroy()

    # Execute tkinter
    root = Tk()

    # Adjust size
    root.geometry(screen_size)
    root.title("Photon Game")

# Set Interval
splash_root.after(3000, main)

# Execute tkinter
mainloop()