import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def create_connection():
    return sqlite3.connect('users.db')

def get_user(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = create_connection() 
    cursor = conn.cursor() 
    cursor.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()  
    conn.close()
    return user

def verify_user(username, password):
    user = get_user(username)
    if user:
        if check_password_hash(user[2], password):
            return user[0]  
    return None 

def register_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    hashed_password = generate_password_hash(password)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
