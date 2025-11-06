import psycopg2

# Connection parameters
DB_NAME = 'photon'
DB_USER = 'student'

def get_connection():
    return psycopg2.connect(
        database=DB_NAME,
        user=DB_USER,
    )

# Lookup player by player ID
# Returns result, otherwise return None
def lookup_player(player_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT codename FROM players WHERE id = %s", (player_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except Exception as e:
        print(f"Database lookup error: {e}")
        return None

# Add player to DB, accepting ID and codename
# Returns boolean True if successful, False otherwise
def add_player(player_id, codename):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Use INSERT ... ON CONFLICT to prevent duplicates
        cursor.execute("""
            INSERT INTO players (id, codename) 
            VALUES (%s, %s)
            ON CONFLICT (id) DO UPDATE SET codename = EXCLUDED.codename
        """, (player_id, codename))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Database add error: {e}")
        return False