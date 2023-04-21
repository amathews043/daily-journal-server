import sqlite3
import json

from models import Moods

def get_all_moods(): 
    """function to get all the moods from the database"""

    with sqlite3.connect("./dailyjournal.sqlite3") as conn: 
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            id,
            label
        FROM Moods
        """)

        moods = []

        dataset = db_cursor.fetchall()

        for row in dataset: 
            mood = Moods(row['id'], row['label'],)

            moods.append(mood.__dict__) 
        return moods 
    
def get_single_mood(id): 
    with sqlite3.connect("./dailyjournal.sqlite3") as conn: 
        conn.row_factory = sqlite3.Row

        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            id, 
            label
        FROM Moods
        WHERE id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        mood = Moods(data['id'], data['label'])

        return mood.__dict__
