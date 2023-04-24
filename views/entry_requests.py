import sqlite3
import json
from datetime import datetime

from models import Entries, Moods

def get_all_entries(): 
    """function to get all the journal entries from the database"""

    with sqlite3.connect("./dailyjournal.sqlite3") as conn: 
        conn.row_factory = sqlite3.Row 
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            e.id as entry_id, 
            e.concept, 
            e.entry, 
            e.mood_id, 
            e.date,
            m.id as mood_id,
            m.label
        FROM Entries e
        JOIN Moods m
            ON e.mood_id = m.id
        """)

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset: 
            entry = Entries(row['entry_id'], row['concept'], row['entry'], row['mood_id'], row['date'],)
            mood = Moods(row['mood_id'], row['label'])
            entry.mood=mood.__dict__

            entries.append(entry.__dict__)


        return entries
    
def get_single_entry(id): 
    with sqlite3.connect("./dailyjournal.sqlite3") as conn: 
        conn.row_factory = sqlite3.Row

        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            e.id as entry_id, 
            e.concept, 
            e.entry, 
            e.mood_id, 
            e.date,
            m.id as mood_id,
            m.label
        FROM Entries e
        JOIN Moods m
            ON e.mood_id = m.id
        WHERE e.id = ?
        """, (id, ))

        data = db_cursor.fetchone()
        print(data)

        entry = Entries(data['entry_id'], data['concept'], data['entry'], data['mood_id'], data['date'],)
        mood = Moods(data['mood_id'], data['label'])
        entry.mood = mood.__dict__

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
