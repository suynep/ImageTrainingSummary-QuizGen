import sqlite3
import hashlib
import os
from typing import Optional, Tuple

# Database setup
DB_PATH = "users.db"

def init_db():
    """Initialize the SQLite database with users table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username: str, email: str, password: str) -> Tuple[bool, str]:
    """Create a new user account"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if username or email already exists
        cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
        if cursor.fetchone():
            conn.close()
            return False, "Username or email already exists"
        
        # Create new user
        password_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash)
        )
        
        conn.commit()
        conn.close()
        return True, "User created successfully"
        
    except Exception as e:
        return False, f"Error creating user: {str(e)}"

def verify_user(username: str, password: str) -> Tuple[bool, Optional[dict], str]:
    """Verify user login credentials"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, username, email FROM users WHERE username = ? AND password_hash = ?",
            (username, hash_password(password))
        )
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return True, {
                "id": user[0],
                "username": user[1],
                "email": user[2]
            }, "Login successful"
        else:
            return False, None, "Invalid username or password"
            
    except Exception as e:
        return False, None, f"Error verifying user: {str(e)}"

def get_user_by_id(user_id: int) -> Optional[dict]:
    """Get user information by ID"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, username, email FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                "id": user[0],
                "username": user[1],
                "email": user[2]
            }
        return None
        
    except Exception as e:
        print(f"Error getting user: {str(e)}")
        return None

# Initialize database when module is imported
init_db()
