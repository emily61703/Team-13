import sqlite3

# Return DB
def get_db():
    conn = sqlite3.connect('players.db')
    conn.execute('CREATE TABLE IF NOT EXISTS players (id INT, codename VARCHAR(30))')
    conn.execute('INSERT OR IGNORE INTO players VALUES (1, "Opus")')
    conn.commit()
    return conn

# Add player to DB
def add_player(player_id, codename):
    conn = get_db()
    conn.execute('INSERT INTO players VALUES (?, ?)', (player_id, codename))
    conn.commit()
    conn.close()

# If player codename found in DB, return result
def lookup_player(codename):
    conn = get_db()
    result = conn.execute('SELECT id FROM players WHERE codename = ?', (codename,)).fetchone()
    conn.close()
    return result[0] if result else None