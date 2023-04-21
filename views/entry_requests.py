import sqlite3
import json

from models import Entries

def get_all_entries(): 
    """function to get all the journal entries from the database"""

    with sqlite3.connect("./dailyjournal.sqlite3") as conn: 
        conn.row_factory = sqlite3.Row 
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            id, 
            concept, 
            entry, 
            mood_id, 
            date
        FROM Entries
        """)

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset: 
            entry = Entries(row['id'], row['concept'], row['entry'], row['mood_id'], row['date'])

            entries.append(entry.__dict__)

        return entries
    
def get_single_entry(id): 
    with sqlite3.connect("./dailyjournal.sqlite3") as conn: 
        conn.row_factory = sqlite3.Row

        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            id, 
            concept, 
            entry, 
            mood_id, 
            date
        FROM Entries
        WHERE id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        entry = Entries(data['id'], data['concept'], data['entry'], data['mood_id'], data['date'])

        return entry.__dict__
