
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('personnages.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS personnages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        profession TEXT,
        age INTEGER,
        univers TEXT,
        score INTEGER,
        niveau TEXT,
        badge TEXT
    )
    ''')
    conn.commit()
    conn.close()
