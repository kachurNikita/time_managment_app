import sqlite3

# connection to database
def create_conection():
    conn = sqlite3.connect('users.db')
    return conn

# users table creation
def create_table():
    conn = create_conection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )'''
                   )
    conn.commit()
    conn.close()