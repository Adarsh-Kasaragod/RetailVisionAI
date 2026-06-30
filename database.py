import sqlite3
import os
from datetime import datetime

DB_NAME = 'retailvision.db'

def init_db():
    """Initialize the SQLite database and create the predictions table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            predicted_class TEXT NOT NULL,
            confidence REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_prediction(filename, predicted_class, confidence):
    """Save a prediction result into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO predictions (filename, predicted_class, confidence)
        VALUES (?, ?, ?)
    ''', (filename, predicted_class, confidence))
    conn.commit()
    conn.close()

def get_recent_predictions(limit=10):
    """Fetch the most recent predictions from the database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['col_name'] 
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, filename, predicted_class, confidence, timestamp 
        FROM predictions 
        ORDER BY timestamp DESC 
        LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
