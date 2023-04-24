import sqlite3
import json
from datetime import datetime

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
            entry = Entries(row['id'], row['concept'], row['entry'], row['mood_id'], row['date'],)

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
    
def delete_entry(id): 
    """function to delete a journal entry"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn: 
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Entries 
        WHERE id = ? 
        """, (id, ))

def create_entry(entry):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn: 
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Entries
            ( concept, entry, mood_id, date )
        VALUES ( ?, ?, ?, ? )
        """, (entry['concept'], entry['entry'], entry['mood_id'], entry['date'],))

        id = db_cursor.lastrowid
        entry['id'] = id 

    return entry

def update_entry(id, new_entry): 
    with sqlite3.connect("./dailyjournal.sqlite3") as conn: 
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Entries 
            SET 
                concept = ?, 
                entry = ?, 
                mood_id = ?, 
                date = ?
        WHERE id = ?
        """, (new_entry['concept'], new_entry['entry'], new_entry['mood_id'], new_entry['date'], id, ))
    row_affected = db_cursor.rowcount

    if row_affected == 0:
        return False
    else: 
        return True
    
def get_entry_by_search(searchTerm): 
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
        WHERE entry LIKE ? 
        """,(f"%{searchTerm}%", ))

        entries = []
        dataset = db_cursor.fetchall()
        for row in dataset: 
            entry = Entries(row['id'], row['concept'], row['entry'], row['mood_id'], row['date'])
            entries.append(entry.__dict__)
            
    return entries
