import sys
from pathlib import Path
from datetime import date, timedelta

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from db import get_connection

#It is for adding a note
def add_note(title, content, category, created_at):
    con = get_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO notes(title, content, category, created_at) VALUES (?,?,?,?)", (title, content, category, created_at))
    con.commit()
    con.close()

#it gets all the notes
def get_notes():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM notes")
    notes = cur.fetchall()
    con.close()
    return notes

#it updates the notes
def update_note(id, title, content, category):
    con = get_connection()
    cur = con.cursor()
    cur.execute("UPDATE notes SET title=?, content=?, category=? WHERE id=?", (title, content, category, id))
    con.commit()
    con.close()

#It deletes the note
def delete_note(id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM notes WHERE id=?", (id,))
    con.commit()
    con.close()

#It gets the notes by cateogry
def get_notes_by_category(category):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM notes WHERE category=?", (category,))
    notes = cur.fetchall()
    con.close()
    return notes

#Ut gets the notes by date range
def get_notes_by_date_range(start_date, end_date):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM notes WHERE created_at BETWEEN ? AND ?", (start_date, end_date))
    notes = cur.fetchall()
    con.close()
    return notes

#It searches the notes
def search_notes(query):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM notes WHERE title LIKE ? or content LIKE ?", (f'%{query}%', f'%{query}%'))
    notes = cur.fetchall()
    con.close()
    return notes
