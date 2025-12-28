import sqlite3

DB_NAME = "todo.db"

def get_sqlite_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_sqlite_db():
    conn = get_sqlite_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            status TEXT DEFAULT 'pending'
        )
    """)
    conn.commit()
    conn.close()


import psycopg2
from app.config import DATABASE_URL

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        due_date DATE,
        status TEXT DEFAULT 'pending',
        user_id INTEGER REFERENCES users(id)
    );
    """)

    conn.commit()
    cur.close()
    conn.close()
