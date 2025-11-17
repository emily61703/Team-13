# play_action_screen.py: The play action screen!

from tkinter import Toplevel, Frame, Label, Button, LEFT, RIGHT, TOP, X, BOTH, Text, END
from PIL import Image, ImageTk
import time
from music_select import stop_music
from udpclient import send_game_start, send_acknowledgment
from udpserver import udp_server
from sfx_system import soundsystem

# Config
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
UDP_SEND_PORT = 7500
GAME_DURATION = 360

# Global variables
play_window = None
event_display = None
base_icon_photo = None

# Game state
game_state = {
    "red_score": 0,
    "green_score": 0,
    "start_time": None,
    "players_with_base": set(),
    "player_map": {}
}

score_labels = {"red": None, "green": None}
timer_label = None
team_displays = {"red": {}, "green": {}}


def load_base_icon():
    """Load base icon image"""
    global base_icon_photo
    try:
        base_icon_image = Image.open("assets/base-icon.jpg")
        base_icon_image = base_icon_image.resize((20, 20), Image.Resampling.LANCZOS)
        base_icon_photo = ImageTk.PhotoImage(base_icon_image)
    except Exception as e:
        print(f"Could not load base icon: {e}")
        base_icon_photo = None


def create_team_display(parent, team_name, team_color, players):
    """Create a team window with player list"""
    global team_displays

    frame = Frame(parent, bg="#1a1a1a", bd=0)
    frame.pack(
        side=LEFT if team_color == "red" else RIGHT,
        fill=BOTH,
        expand=True,
        padx=10,
        pady=0
    )

    header_frame = Frame(frame, bg="#1a1a1a")
    header_frame.pack(fill=X, pady=(0, 5))

    Label(
        header_frame,
        text=team_name.upper(),
        font=("Helvetica", 24, "bold"),
        fg=team_color,
        bg="#1a1a1a"
    ).pack()

    score_label = Label(
        header_frame,
        text="Score: 0",
        font=("Helvetica", 18),
        fg=team_color,
        bg="#1a1a1a"
    )
    score_label.pack(pady=(5, 10))
    score_labels[team_color] = score_label

    for code, name in players:
        player_frame = Frame(frame, bg="#1a1a1a")
        player_frame.pack(fill=X, pady=4)

        player_label = Label(
            player_frame,
            text=name,
            font=("Helvetica", 14),
            fg="white",
            bg="#1a1a1a",
            anchor="w"
        )
        player_label.pack(side=LEFT)

        team_displays[team_color][code] = player_label
        game_state["player_map"][code] = (name, team_color)

    return frame


def create_timer_display(parent):
    """Create game timer display"""
    global timer_label

    timer_frame = Frame(parent, bg="#1a1a1a")
    timer_frame.pack(pady=(0, 15))

    Label(
        timer_frame,
        text="Time Remaining",
        font=("Helvetica", 20),
        fg="white",
        bg="#1a1a1a"
    ).pack()

    timer_label = Label(
        timer_frame,
        text="6:00",
        font=("Helvetica", 36, "bold"),
        fg="white",
        bg="#1a1a1a"
    )
    timer_label.pack()

    return timer_frame


def create_event_display(parent):
    """Create event display"""
    global event_display

    frame = Frame(parent, bg="#1a1a1a")
    frame.pack(fill=BOTH, expand=True, padx=10, pady=20)

    Label(
        frame,
        text="Events",
        font=("Helvetica", 22, "bold"),
        fg="white",
        bg="#1a1a1a"
    ).pack(pady=(0, 10))

    event_display = Text(
        frame,
        bg="#0a0a0a",
        fg="#888888",
        font=("Monaco", 16),
        state="disabled",
        wrap="word",
        padx=15,
        pady=15,
        bd=0,
        highlightthickness=0
    )
    event_display.pack(fill=BOTH, expand=True)

    event_display.tag_config("red", foreground="#ff6b6b")
    event_display.tag_config("green", foreground="#51cf66")
    event_display.tag_config("system", foreground="#ffd43b")
    event_display.tag_config("base", foreground="#00bcd4")
    event_display.tag_config("friendly_fire", foreground="#ff9800")

    return frame


def update_score(team, points=10):
    """Update team score"""
    game_state[f"{team}_score"] += points
    if score_labels[team]:
        score_labels[team].config(text=f"Score: {game_state[f'{team}_score']}")


def add_base_icon(equipment_code):
    """Add base icon to player"""
    if equipment_code in game_state["player_map"]:
        name, team = game_state["player_map"][equipment_code]
        game_state["players_with_base"].add(equipment_code)

        if equipment_code in team_displays[team] and base_icon_photo:
            label = team_displays[team][equipment_code]
            label.config(image=base_icon_photo, compound="right")


def get_player_name(equipment_code):
    """Get player name from equipment code"""
    if equipment_code in game_state["player_map"]:
        return game_state["player_map"][equipment_code][0]
    return f"Equipment {equipment_code}"


def get_player_team(equipment_code):
    """Get player team from equipment code"""
    if equipment_code in game_state["player_map"]:
        return game_state["player_map"][equipment_code][1]
    return None


def start_game_timer():
    """Start the 6-minute game timer"""
    global timer_label
    game_state["start_time"] = time.time()

    def update_timer():
        if not udp_server.running or timer_label is None:
            return

        elapsed = time.time() - game_state["start_time"]
        remaining = max(0, GAME_DURATION - elapsed)

        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        timer_label.config(text=f"{minutes}:{seconds:02d}")

        if remaining < 60:
            timer_label.config(fg="#ff4444")
        elif remaining < 120:
            timer_label.config(fg="#ff9800")

        if remaining <= 0:
            end_game()
            return

        if timer_label and timer_label.winfo_exists():
            timer_label.after(1000, update_timer)

    update_timer()


def end_game():
    """Handle game end"""
    add_event_message("=" * 10, "system")
    add_event_message("Game Over!", "system")
    add_event_message(f"Red Team: {game_state['red_score']} points", "red")
    add_event_message(f"Green Team: {game_state['green_score']} points", "green")

    if game_state['red_score'] > game_state['green_score']:
        winner = "red"
    elif game_state['green_score'] > game_state['red_score']:
        winner = "green"
    else:
        winner = None

    if winner:
        add_event_message(f"{winner.capitalize()} Team Wins!", winner)
    else:
        add_event_message("It's a Tie!", "system")

    add_event_message("=" * 10, "system")

    send_acknowledgment(("127.0.0.1", UDP_SEND_PORT), "221")
    udp_server.stop()


def add_event_message(message, tag="system"):
    """Add a message to the event display"""
    global event_display
    if event_display is None:
        return

    def update():
        if event_display is None:
            return
        try:
            event_display.config(state="normal")
            event_display.insert(END, message + "\n", tag)
            event_display.see(END)
            event_display.config(state="disabled")
        except:
            pass

    try:
        event_display.after(0, update)
    except:
        pass


def process_hit(attacker_code, target_code):
    """Process a hit event"""
    attacker_name = get_player_name(attacker_code)
    attacker_team = get_player_team(attacker_code)
    target_name = get_player_name(target_code)
    target_team = get_player_team(target_code)

    is_friendly_fire = False

    if target_code == "43":
        add_event_message(f"{attacker_name} hit Red Base!", "base")
        add_base_icon(attacker_code)
        if attacker_team == "green":
            update_score("green", 100)
            soundsystem.play_helmet_sound('hit')
        return is_friendly_fire

    if target_code == "53":
        add_event_message(f"{attacker_name} hit Green Base!", "base")
        add_base_icon(attacker_code)
        if attacker_team == "red":
            update_score("red", 100)
            soundsystem.play_helmet_sound('hit')
        return is_friendly_fire

    if attacker_team == target_team and attacker_team is not None:
        add_event_message(f"Friendly Fire: {attacker_name} hit teammate {target_name}!", "friendly_fire")
        update_score(attacker_team, -10)
        is_friendly_fire = True
        
        soundsystem.play_helmet_sound('hitown')
        
        return is_friendly_fire

    if attacker_team and target_team:
        add_event_message(f"{attacker_name} hit {target_name}", attacker_team)
        update_score(attacker_team, 10)
        
        soundsystem.play_helmet_sound('hit')

    return is_friendly_fire


def handle_udp_message(message, address):
    """Callback for incoming UDP messages"""
    if message == "221":
        add_event_message("Game end signal received", "system")
        send_acknowledgment((address[0], UDP_SEND_PORT), "221")
        end_game()
        return

    if ':' in message:
        attacker, target = message.split(':')
        is_friendly_fire = process_hit(attacker, target)
        send_acknowledgment((address[0], UDP_SEND_PORT), "200")

        if is_friendly_fire:
            send_acknowledgment((address[0], UDP_SEND_PORT), "200")
    else:
        add_event_message(f"Unknown format: {message}", "system")


def display_pa(red_players, green_players, return_to_login_callback):
    """Display the play action window"""
    global play_window, game_state, score_labels, timer_label, team_displays, event_display

    udp_server.stop()
    time.sleep(0.5)

    game_state = {
        "red_score": 0,
        "green_score": 0,
        "start_time": None,
        "players_with_base": set(),
        "player_map": {}
    }
    score_labels = {"red": None, "green": None}
    timer_label = None
    team_displays = {"red": {}, "green": {}}
    event_display = None

    if play_window is not None:
        try:
            if play_window.winfo_exists():
                play_window.destroy()
        except:
            pass

    play_window = Toplevel()
    play_window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    play_window.title("Play Action")
    play_window.configure(bg="black")

    load_base_icon()

    def on_closing():
        global event_display, timer_label
        send_acknowledgment(("127.0.0.1", UDP_SEND_PORT), "221")
        udp_server.stop()
        stop_music()
        soundsystem.cleanup()
        event_display = None
        timer_label = None
        play_window.destroy()
        return_to_login_callback()

    play_window.protocol("WM_DELETE_WINDOW", on_closing)

    top_frame = Frame(play_window, bg="black")
    top_frame.pack(side=TOP, fill=X)

    Button(
        top_frame,
        text="Exit",
        command=on_closing,
        bg="red",
        fg="black",
        font=("Helvetica", 12, "bold")
    ).pack(side=LEFT, padx=10, pady=10)

    main_frame = Frame(play_window, bg="#1a1a1a")
    main_frame.pack(fill=BOTH, expand=True, padx=30, pady=30)

    create_timer_display(main_frame)

    teams_frame = Frame(main_frame, bg="#1a1a1a")
    teams_frame.pack(fill=BOTH, expand=True, pady=(0, 10))

    create_team_display(teams_frame, "red team", "red", red_players)
    create_team_display(teams_frame, "green team", "green", green_players)

    create_event_display(main_frame)

    # Start UDP server with callback
    udp_server.start(handle_udp_message)


    # Send game start signal
    add_event_message("UDP server listening on port 7501", "system")
    add_event_message("Sending game start signal (202)...", "system")
    send_game_start()
    add_event_message("Game started!", "system")
    start_game_timer()

    return play_window
