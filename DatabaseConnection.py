import sqlite3

def connect_db():
    # Connect to SQLite database
    conn = sqlite3.connect('RideEaseDatabase.db')
    cursor = conn.cursor()
    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        password TEXT NOT NULL,
                        email TEXT NOT NULL
                    )''')
    conn.commit()
    return conn




