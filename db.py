import sqlite3
from datetime import datetime

DB_PATH = 'monitor.db'

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS endpoints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            failures INTEGER DEFAULT 0,
            last_checked TEXT)''')
        conn.commit()

def get_all_endpoints():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM endpoints")
        return c.fetchall()

def add_endpoint(name, url):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO endpoints (name, url) VALUES (?, ?)", (name, url))
        conn.commit()

def delete_endpoint_by_id(id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM endpoints WHERE id = ?", (id,))
        conn.commit()

def update_endpoint(id, failures):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("UPDATE endpoints SET failures = ?, last_checked = ? WHERE id = ?", (failures, datetime.now(), id))
        conn.commit()

def reset_failures(id):
    update_endpoint(id, 0)