# login_screen.py: This is code relating to the login screen; the scope here is very wide and could do
#                  with being refactored into smaller modules.
#
#                  The sections are:
#                       1. Player Management
#                       2. UI Creation
#                       3. Game Start Logic
#                       4. Main Window

from tkinter import Tk, Frame, Label, Entry, Button, END, messagebox, simpledialog
import database
from udpclient import broadcast_equipment
from play_action_screen import display_pa
from music_select import show_music_selector, start_music

# Config
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 800
MAX_PLAYERS_PER_TEAM = 15
START_ROW = 6
PLAYER_START_ROW = START_ROW + 2
COUNTDOWN_SECONDS = 30

# Global variables
login_window = None
player_entries = {"red": [], "green": []}
player_equipment_map = {}

def save_player(code, name, team=None, equipment_id=None, show_dialog=False):
    """
    Save player to database and optionally broadcast equipment info.

    Args:
        code: Player code (int or string)
        name: Player name (string)
        team: Team color ('red' or 'green') - required for broadcast
        equipment_id: Equipment ID (optional, defaults to code)
        show_dialog: If True, show messagebox. If False, print to console.
    """
    if not code or not name:
        if show_dialog:
            messagebox.showwarning("Missing Info", "Both code and name required")
        return False

    try:
        code_int = int(code)

        # Save to database
        if not database.add_player(code_int, name):
            if show_dialog:
                messagebox.showwarning("Error", "Failed to save to database")
            else:
                print(f"Error saving player {name}")
            return False

        # Broadcast if team provided
        if team:
            broadcast_equipment(
                player_id=name,
                equipment_code=equipment_id if equipment_id else code_int,
                team=team
            )

        # Success feedback
        if show_dialog:
            messagebox.showinfo("Success", f"Player {name} saved!")
        else:
            print(f"Saved player: {name} with code {code}")

        return True

    except ValueError:
        if show_dialog:
            messagebox.showwarning("Error", "Player code must be a number")
        else:
            print(f"Error: Player code '{code}' must be a number")
        return False
    except Exception as e:
        if show_dialog:
            messagebox.showwarning("Error", f"Could not save player: {e}")
        else:
            print(f"Error saving player {name}: {e}")
        return False

def save_all_players():
    for team, entries in player_entries.items():
        for code_entry, name_entry in entries:
            code = code_entry.get().strip()
            name = name_entry.get().strip()
            if code and name:
                save_player(code, name, show_dialog=False)  # No team = no broadcast

def clear_all_players():
    """Clear all player entry fields"""
    for team, entries in player_entries.items():
        for code_entry, name_entry in entries:
            code_entry.delete(0, END)
            name_entry.delete(0, END)

    initialize_rows()

def initialize_rows():
    """Enable only the first row for each team"""
    for team in ["red", "green"]:
        entries = player_entries[team]
        for i, (code_entry, name_entry) in enumerate(entries):
            if i == 0:
                code_entry.config(state="normal")
                name_entry.config(state="normal")
                code_entry.focus_set()
            else:
                code_entry.config(state="disabled")
                name_entry.config(state="disabled")

def ask_equipment_id(parent):
    """Prompt user for equipment ID"""
    return simpledialog.askinteger(
        "Equipment ID",
        "Enter Equipment ID:",
        parent=parent
    )

def create_player_entry(num_player, team, parent_frame):
    """Create a single player entry row"""
    global player_entries
    row = num_player + PLAYER_START_ROW

    if team == 'red':
        Label(parent_frame, text=num_player).grid(row=row, column=1)
        player_code = Entry(parent_frame, fg="red", bg="black")
        player_name = Entry(parent_frame, fg="red", bg="black")
        player_code.grid(row=row, column=2)
        player_name.grid(row=row, column=3)
        player_entries["red"].append((player_code, player_name))

    elif team == 'green':
        Label(parent_frame, text=num_player).grid(row=row, column=4)
        player_code = Entry(parent_frame, fg="green", bg="black")
        player_name = Entry(parent_frame, fg="green", bg="black")
        player_code.grid(row=row, column=5)
        player_name.grid(row=row, column=6)
        player_entries["green"].append((player_code, player_name))

def setup_navigation(team):
    """Setup Enter key navigation for player entries"""
    entries = player_entries[team]

    for i, (code_entry, name_entry) in enumerate(entries):

        def on_code_enter(event, c=code_entry, n=name_entry):
            """When user presses Enter in code field"""
            code = c.get().strip()
            if code:
                returned_name = database.lookup_player(code)
                if returned_name is None:
                    messagebox.showwarning(
                        "No Name",
                        "Name not found. Please enter a name."
                    )
                else:
                    n.delete(0, END)
                    n.insert(0, returned_name)
                n.focus_set()

        def on_name_enter(event, idx=i, t=team, c=code_entry, n=name_entry):
            """When user presses Enter in name field"""
            code = c.get().strip()
            name = n.get().strip()

            if not name:
                messagebox.showwarning(
                    "No Name",
                    "Please enter a name before continuing."
                )
                return

            # Ask for equipment ID
            equipment_id = ask_equipment_id(n.winfo_toplevel())
            if equipment_id is None:
                messagebox.showwarning(
                    "No Equipment ID",
                    "You must enter a valid equipment ID."
                )
                return

            # Save player with equipment info
            if save_player(code, name, team=t, equipment_id=equipment_id, show_dialog=True):
                # Enable next row if available
                if idx + 1 < len(entries):
                    next_code, next_name = entries[idx + 1]
                    next_code.config(state="normal")
                    next_name.config(state="normal")
                    next_code.focus_set()
                player_equipment_map[(t, idx)] = (str(equipment_id), name)

        code_entry.bind("<Return>", on_code_enter)
        name_entry.bind("<Return>", on_name_enter)

def get_all_players():
    """Extract all player data - returns (equipment_code, name) tuples"""
    red_players = [
        player_equipment_map.get(("red", i), (None, None))
        for i in range(len(player_entries["red"]))
        if player_equipment_map.get(("red", i), (None, None))[0] is not None
    ]
    green_players = [
        player_equipment_map.get(("green", i), (None, None))
        for i in range(len(player_entries["green"]))
        if player_equipment_map.get(("green", i), (None, None))[0] is not None
    ]
    return red_players, green_players

def create_countdown_logic(parent_window, start_button):
    """Create countdown logic for game start"""
    countdown_state = {"timer_id": None, "label": None}

    def start_countdown():
        start_button.config(state="disabled")

        countdown_label = Label(
            parent_window,
            text=f"Game start in: {COUNTDOWN_SECONDS} seconds",
            font=("Helvetica", 20)
        )
        countdown_label.pack()
        countdown_state["label"] = countdown_label

        def countdown(count):
            if count > 0:
                countdown_label.config(text=f"Game start in: {count} seconds")
                countdown_state["timer_id"] = parent_window.after(1000, countdown, count - 1)
            else:
                # Cleanup countdown
                countdown_label.destroy()
                countdown_state["timer_id"] = None
                countdown_state["label"] = None

                # Start music when game begins
                start_music()

                # Start game
                red_players, green_players = get_all_players()
                display_pa(
                    red_players,
                    green_players,
                    return_to_login_callback=lambda: start_button.config(state="normal")
                )

        countdown(COUNTDOWN_SECONDS)

    def skip_to_play_action():
        """Go directly to play action without countdown"""
        # Cancel any running countdown
        if countdown_state["timer_id"] is not None:
            parent_window.after_cancel(countdown_state["timer_id"])
            countdown_state["timer_id"] = None

        if countdown_state["label"] is not None:
            countdown_state["label"].destroy()
            countdown_state["label"] = None

        start_button.config(state="normal")

        # Start music when game begins
        start_music()

        red_players, green_players = get_all_players()
        display_pa(red_players, green_players, return_to_login_callback=lambda: None)

    return start_countdown, skip_to_play_action

def show_login_screen():
    """Create and display the login screen"""
    global login_window, player_entries

    # Check if window already exists
    if login_window is not None:
        try:
            if login_window.winfo_exists():
                login_window.deiconify()
                login_window.lift()
                return
        except:
            pass

    # Reset player entries
    player_entries = {"red": [], "green": []}

    # Create window
    login_window = Tk()
    login_window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    login_window.title("Login")

    outer_container = Frame(login_window)
    outer_container.pack(side="top", fill="both", expand=True)

    entry_frame = Frame(outer_container)
    entry_frame.place(relx=0.5, rely=0, anchor="n")

    Label(
        entry_frame,
        text='Red Team',
        fg="red",
        font=("Helvetica", 16)
    ).grid(row=START_ROW, column=2, columnspan=2)

    Label(
        entry_frame,
        text='Green Team',
        fg="green",
        font=("Helvetica", 16)
    ).grid(row=START_ROW, column=5, columnspan=2)

    Label(entry_frame, text='Player Code').grid(row=START_ROW + 1, column=2)
    Label(entry_frame, text='Player Name').grid(row=START_ROW + 1, column=3)
    Label(entry_frame, text='Player Code').grid(row=START_ROW + 1, column=5)
    Label(entry_frame, text='Player Name').grid(row=START_ROW + 1, column=6)

    for i in range(1, MAX_PLAYERS_PER_TEAM + 1):
        create_player_entry(i, 'red', entry_frame)
        create_player_entry(i, 'green', entry_frame)

    initialize_rows()

    setup_navigation("red")
    setup_navigation("green")

    footer_frame = Frame(login_window)
    footer_frame.pack(side="bottom", fill="x")

    Button(
        footer_frame,
        text="Save All Player Entries",
        fg="green",
        command=save_all_players
    ).pack(side="left", padx=10, pady=5)

    Button(
        footer_frame,
        text="Clear All Player Entries",
        fg="red",
        command=clear_all_players
    ).pack(side="left", padx=10, pady=5)

    # music selection button
    Button(
        footer_frame,
        text="Select Music Tracks",
        fg="purple",
        command=lambda: show_music_selector(login_window)
    ).pack(side="left", padx=10, pady=5)

    # Create countdown and start button
    start_button = Button(footer_frame, text="Begin Countdown to Play Action", fg="green")
    start_countdown, skip_to_play = create_countdown_logic(login_window, start_button)

    start_button.config(command=start_countdown)
    start_button.pack(side="right", padx=10, pady=5)

    Button(
        footer_frame,
        text="Enter Play Action Immediately",
        fg="blue",
        command=skip_to_play
    ).pack(side="right", padx=10, pady=5)

    login_window.mainloop()