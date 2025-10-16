from tkinter import *
import database

# Create a team window with player list
def create_window(parent, team_name, team_color, players):
    frame = Frame(parent, bg="black", bd=2, relief="solid",
                  highlightbackground=team_color, highlightthickness=3)
    frame.pack(
        side=LEFT if team_color == "red" else RIGHT,
        fill=BOTH, expand=True, padx=10
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

# Diplay the play action window
def Display_PA(red_players, green_players):
    play_window = Tk()
    play_window.geometry("1400x900")
    play_window.title("Play Action Display")
    play_window.configure(bg="black")

    # Main container
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

    # Teams container
    teams_frame = Frame(main_frame, bg="black")
    teams_frame.pack(fill=BOTH, expand=True)

    # Create both team windows
    create_team_window(teams_frame, "red", "red", red_players)
    create_team_window(teams_frame, "green", "green", green_players)

    play_window.mainloop()
