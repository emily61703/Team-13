# play_action_screen.py: The play action screen! The sections are:
#                           1. UI Creation
#                           2. Main Window

from tkinter import Toplevel, Frame, Label, Button, LEFT, RIGHT, TOP, X, BOTH

# Config
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900

# Global variable
play_window = None

# -----------------------
# UI Creation
# -----------------------

def create_team_display(parent, team_name, team_color, players):
    """Create a team window with player list"""
    frame = Frame(
        parent,
        bg="black",
        bd=2,
        relief="solid",
        highlightbackground=team_color,
        highlightthickness=3
    )
    frame.pack(
        side=LEFT if team_color == "red" else RIGHT,
        fill=BOTH,
        expand=True,
        padx=10
    )

    # Team title
    Label(
        frame,
        text=f"{team_name.upper()} TEAM",
        font=("Helvetica", 20, "bold"),
        fg=team_color,
        bg="black"
    ).pack(pady=10)

    # Players list
    for code, name in players:
        player_frame = Frame(frame, bg="black")
        player_frame.pack(fill=X, pady=5, padx=10)

        Label(
            player_frame,
            text=name,
            font=("Helvetica", 16),
            fg=team_color,
            bg="black",
            anchor="w"
        ).pack(side=LEFT, fill=X, expand=True)

# -----------------------
# Main Window
# -----------------------

def display_pa(red_players, green_players, return_to_login_callback):
    """Display the play action window"""
    global play_window

    # Check if the play window already exists
    if play_window is not None:
        try:
            if play_window.winfo_exists():
                play_window.deiconify()
                play_window.lift()
                return play_window
        except:
            pass

    # Create window
    play_window = Toplevel()
    play_window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    play_window.title("Play Action")
    play_window.configure(bg="black")

    # -----------------------
    # Top Frame (Back Button)
    # -----------------------
    top_frame = Frame(play_window, bg="black")
    top_frame.pack(side=TOP, fill=X)

    Button(
        top_frame,
        text="Back to Login",
        command=lambda: [play_window.withdraw(), return_to_login_callback()],
        bg="red",
        fg="black",
        font=("Helvetica", 12, "bold")
    ).pack(side=LEFT, padx=10, pady=10)

    # -----------------------
    # Main Content Frame
    # -----------------------
    main_frame = Frame(play_window, bg="black")
    main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

    # Title
    Label(
        main_frame,
        text="GAME IN PROGRESS",
        font=("Helvetica", 24, "bold"),
        fg="white",
        bg="black"
    ).pack(pady=10)

    # -----------------------
    # Teams Frame
    # -----------------------
    teams_frame = Frame(main_frame, bg="black")
    teams_frame.pack(fill=BOTH, expand=True)

    # Create both team displays
    create_team_display(teams_frame, "red", "red", red_players)
    create_team_display(teams_frame, "green", "green", green_players)

    return play_window