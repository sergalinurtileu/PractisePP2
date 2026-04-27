import psycopg2

# --- Connection Parameters ---
DB_CONFIG = {
    "host": "localhost",
    "database": "snake_db",
    "user": "postgres",
    "password": "Nuric2008", 
}

conn = None

def connect():
    """Establishes a connection to the PostgreSQL database."""
    global conn
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        # Enable autocommit so we don't have to call commit() manually after every query
        conn.autocommit = True 
        print("[DB] Connection successful")
    except Exception as e:
        print(f"[DB] Connection error: {e}")

def init_tables():
    """Creates the necessary tables if they do not already exist."""
    if not conn: return
    with conn.cursor() as cur:
        # Create both tables in a single transaction
        cur.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            );
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id),
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            );
        """)

def get_or_create_player(username):
    """Retrieves an existing player ID or creates a new entry if the username is new."""
    if not conn: return None
    with conn.cursor() as cur:
        # Check if the player already exists
        cur.execute("SELECT id FROM players WHERE username = %s", (username,))
        row = cur.fetchone()
        if row: return row[0]
        
        # If not, insert new player and return the generated ID
        cur.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
        return cur.fetchone()[0]

def save_result(p_id, score, lvl):
    """Logs the final score and level reached at the end of a game session."""
    if not conn or not p_id: return
    with conn.cursor() as cur:
        cur.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
                    (p_id, score, lvl))

def get_top10():
    """Fetches the top 10 highest scores along with player names and formatted dates."""
    if not conn: return []
    with conn.cursor() as cur:
        cur.execute("""
            SELECT p.username, s.score, s.level_reached, TO_CHAR(s.played_at, 'DD.MM.YY')
            FROM game_sessions s 
            JOIN players p ON p.id = s.player_id
            ORDER BY s.score DESC 
            LIMIT 10
        """)
        return cur.fetchall()

def get_best_score(p_id):
    """Retrieves the highest personal score for a specific player."""
    if not conn or not p_id: return 0
    with conn.cursor() as cur:
        cur.execute("SELECT MAX(score) FROM game_sessions WHERE player_id = %s", (p_id,))
        res = cur.fetchone()[0]
        return res if res else 0