from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk

# Create object
splash_window = Tk()

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
                save_player(code, name, team)

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

def lookup_player_by_code(code):
    """
    Placeholder for database lookup logic.
    Takes in:
        code (str): Player code to search in database.
    Returns:
        str | None: Player name if found, else None.
    """
    return

                
def save_player(code, name, team):
    """
    Save a single player's code and name to the database.
    Takes in:
        code_entry (Entry): Tkinter Entry widget for code.
        name_entry (Entry): Tkinter Entry widget for name.
        team (str): 'red' or 'green'
    """
    return

# -----------------------
# Main Window
# -----------------------
def main():
    # Close splash window
    splash_window.destroy()

    # Open login window
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
    def start_game():
       messagebox.showinfo("Get Ready","Game Starting Soon")
    
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
    
    Button(
        footer_frame,
        text="Start",
        fg="green",
        command=start_game).pack(side=RIGHT, padx=10, pady=5)

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
    # Create Inital Player Boxes
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
                    returned_name = lookup_player_by_code(code)
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

                save_player(code, name, team)

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
