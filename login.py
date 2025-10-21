from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

from PIL import Image, ImageTk

import database
from udpclient import broadcast_equipment

from play_action import display_pa

# Create windows
splash_window = Tk()
login_window = None

# Adjust size
width = 1000
height = 800
screen_size = str(width)+'x'+str(height)
splash_window.geometry(screen_size)

# Attributes
image = Image.open("logo.jpg")
resized_image = image.resize((width, height))
img = ImageTk.PhotoImage(resized_image)

# Set Label
splash_label = Label(splash_window, image=img)
splash_label.pack()

# Store player information for database reference
player_entries = {"red": [], "green": []}

start_row = 6
player_start_row = start_row+2

# -----------------------
# Functions
# -----------------------
def initialize_rows():
    # Initialize rows: disable all except first row per team
    for team in ["red", "green"]:
        entries = player_entries[team]
        for i, (code_entry, name_entry) in enumerate(entries):
            if i == 0:
                code_entry.config(state="normal")
                name_entry.config(state="normal")
                code_entry.focus_set()  # optionally focus the first code
            else:
                code_entry.config(state="disabled")
                name_entry.config(state="disabled")

def save_all_players():
    for team, entries in player_entries.items():
        for code_entry, name_entry in entries:
            code = code_entry.get().strip()
            name = name_entry.get().strip()
            if code and name:
                save_player(code, name)

def clear_all_players():
    # Clear on screen textboxes
    for team, entries in player_entries.items():
        for code_entry, name_entry in entries:
            code_entry.delete(0, END)
            name_entry.delete(0, END)

    # Diable rows again
    initialize_rows()

def create_player_entry(num_player, team,  login_window): 
    global player_entries
    row = num_player + player_start_row

    if team == 'red':
        Label(login_window, text=num_player).grid(row=row, column=1)
        player_code = Entry(login_window, fg="red", bg="black")
        player_name = Entry(login_window, fg="red", bg="black")
        player_code.grid(row=row, column=2)
        player_name.grid(row=row, column=3)
        
        player_name.bind("<Return>", lambda event, c=player_code, n=player_name: save_player(c, n, "red"))
        player_entries["red"].append((player_code, player_name))

    elif team == 'green':
        Label(login_window, text=num_player).grid(row=row, column=4)
        player_code = Entry(login_window, fg="green", bg="black")
        player_name = Entry(login_window, fg="green", bg="black")
        player_code.grid(row=row, column=5)
        player_name.grid(row=row, column=6)

        player_name.bind("<Return>", lambda event, c=player_code, n=player_name: save_player(c, n, "green"))
        player_entries["green"].append((player_code, player_name))

def save_player(code, name):
    if code and name:
        try:
            database.add_player(int(code), name)
            print(f"Saved player: {name} with code {code}")
        except ValueError:
            print(f"Error: Player code '{code}' must be a number")
        except Exception as e:
            print(f"Error saving player {name}: {e}")

# Handles saving to DB from widget objects
def save_player_from_widgets(code_entry, name_entry, team):
    code = code_entry.get().strip()
    name = name_entry.get().strip()
    if code and name:
        try:
            database.add_player(int(code), name)

            # Broadcast the new player's equipment code
            broadcast_success = broadcast_equipment(
                player_id=name,
                equipment_code=code,
                team=team
            )
            
            messagebox.showinfo("Success", f"Player {name} saved!")
        except ValueError:
            messagebox.showwarning("Error", "Player code must be a number")
        except Exception as e:
            messagebox.showwarning("Error", f"Could not save player: {e}")

def ask_equipment_id(parent):
    """
    Pops up a dialog asking for an equipment ID.
    Returns:
        str: Equipment ID entered, or None if canceled.
    """
    equipment_id = simpledialog.askinteger("Equipment ID", "Enter Equipment ID:", parent=parent)
    return equipment_id

# -----------------------
# Main Window
# -----------------------
def main():
    # Collect our global windows so we always reference the same one!
    global splash_window, login_window

    # Close splash window IF it is open
    if splash_window is not None:
        try:
            splash_window.destroy()
            splash_window = None
        except:
            pass

    # If we already have a login_window, return to the same one!
    if login_window is not None:
        try:
            if login_window.winfo_exists():
                login_window.deiconify()
                login_window.lift()
                return
        except:
            pass

    # If there is no login_window, create it!
    login_window = Tk()
    login_window.geometry(screen_size)
    login_window.title("Login")

    # -----------------------
    # Player Frame
    # -----------------------
    entry_frame = Frame(login_window)
    entry_frame.pack(side=TOP, fill=BOTH, expand=True)

    # -----------------------
    # Footer Frame
    # -----------------------

    countdown_id = [None]
    countdown_label_ref = [None]

    def start_game():
        # Disable start button after countdown begins
        start_button.config(state="disabled")

        # Create label
        countdown_label = Label(login_window, text="Game start in: 30 seconds", font=("Helvetica", 20))
        countdown_label.pack()
        countdown_label_ref[0] = countdown_label

        def countdown(count):
            if count > 0:
                countdown_label.config(text=f"Game start in: {count} seconds")
                countdown_id[0] = login_window.after(1000, countdown, count - 1)
            else:
                # Destroy the countdown label
                if countdown_label_ref[0] is not None:
                    countdown_label_ref[0].destroy()

                # Clear the ID and label reference
                countdown_id[0] = None
                countdown_label_ref[0] = None

                # Gather player data
                red_players = [(code_entry.get().strip(), name_entry.get().strip())
                               for code_entry, name_entry in player_entries["red"]]
                green_players = [(code_entry.get().strip(), name_entry.get().strip())
                                 for code_entry, name_entry in player_entries["green"]]

                # Callback used for resetting the UI when returning
                def on_return_from_countdown():
                    start_button.config(state="normal") # Enable the start button

                # Open the play action display and pass the main function as a callback
                display_pa(red_players, green_players, return_to_login_callback=on_return_from_countdown)

        countdown(5)

    def go_to_play_action():
        """Immediately go to play action display without countdown"""
        # Cancel a running countdown, if it exists
        if countdown_id[0] is not None:
            login_window.after_cancel(countdown_id[0])
            countdown_id[0] = None

        # Destroy the countdown label, if it exists
        if countdown_label_ref[0] is not None:
            countdown_label_ref[0].destroy()
            countdown_label_ref[0] = None

        start_button.config(state="normal")
        
        red_players = [(code_entry.get().strip(), name_entry.get().strip())
                    for code_entry, name_entry in player_entries["red"]]
        green_players = [(code_entry.get().strip(), name_entry.get().strip())
                        for code_entry, name_entry in player_entries["green"]]

        display_pa(red_players, green_players, return_to_login_callback=lambda: None)
    
    footer_frame = Frame(login_window)
    footer_frame.pack(side=BOTTOM, fill=X)
    
    Button(
        footer_frame,
        text="Save All Player Entries",
        fg="green",
        command=save_all_players).pack(side=LEFT, padx=10, pady=5)
    
    Button(
        footer_frame,
        text="Clear All Player Entries",
        fg="red",
        command=clear_all_players).pack(side=LEFT, padx=10, pady=5)
    
    # Button to go directly to play action
    Button(
        footer_frame,
        text="Play Action",
        fg="blue",
        command=go_to_play_action).pack(side=LEFT, padx=10, pady=5)
    
    start_button = Button(
        footer_frame,
        text="Start",
        fg="green",
        command=start_game)
    start_button.pack(side=RIGHT, padx=10, pady=5)

    # -----------------------
    # Add Labels for Teams
    # -----------------------
    Label(entry_frame, text='Red Team', fg="red", font=("Helvetica", 16)).grid(row=start_row, column=2,columnspan=2)
    Label(entry_frame, text='Green Team', fg="green", font=("Helvetica", 16)).grid(row=start_row, column=5,columnspan=2)
    Label(entry_frame, text='Player Code').grid(row=start_row+1, column=2)
    Label(entry_frame, text='Player Name').grid(row=start_row+1, column=3)
    Label(entry_frame, text='Player Code').grid(row=start_row+1, column=5)
    Label(entry_frame, text='Player Name').grid(row=start_row+1, column=6)

    # -----------------------
    # Create Initial Player Boxes
    # -----------------------
    num_red_players = 15
    num_green_players = 15
    for i in range(1, num_red_players + 1):
        create_player_entry(i, 'red', entry_frame)
    for i in range(1, num_green_players + 1):
        create_player_entry(i, 'green', entry_frame)
    
    initialize_rows()

    # -----------------------
    # Enter-key navigation
    # -----------------------
    def bind_navigation(team):
        entries = player_entries[team]
        for i, (code_entry, name_entry) in enumerate(entries):

            def on_code_enter(event, c=code_entry, n=name_entry):
                code = c.get().strip()
                if code:
                    returned_name = database.lookup_player(code)
                    if returned_name is None:
                        messagebox.showwarning("No Name", "Name not Found: Please enter a name before continuing.")
                    else:
                        n.delete(0, "end")
                        n.insert(0, returned_name)
                    n.focus_set()

            def on_name_enter(event, idx=i, t=team, c=code_entry, n=name_entry):
                code = c.get().strip()
                name = n.get().strip()

                if not name:
                    # Don't proceed if name box is empty
                    messagebox.showwarning("No Name", "Name not Found: Please enter a name before continuing.")
                    return

                # Ask for equipment ID
                equipment_id = ask_equipment_id(n.winfo_toplevel())
                if equipment_id is None:  # User canceled
                    messagebox.showwarning("No Equipment ID", "You must enter a valid equipment ID.")
                    return

                save_player_from_widgets(c, n, team)

                # Enable next row if available
                if idx + 1 < len(entries):
                    next_code, next_name = entries[idx + 1]
                    next_code.config(state="normal")
                    next_name.config(state="normal")
                    next_code.focus_set()

            code_entry.bind("<Return>", on_code_enter)
            name_entry.bind("<Return>", on_name_enter)

    # Bind navigation separately for each team
    bind_navigation("red")
    bind_navigation("green")
    
# Open splash window
splash_window.after(3000, main)

# Execute tkinter
mainloop()