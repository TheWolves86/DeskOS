import sys
from pathlib import Path
from datetime import date, timedelta

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from db import get_connection

#Adds a new journal entry
def add_journal_entry(title, content, date):
    con = get_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO journal (title, content, date) VALUES (?, ?, ?)", (title, content, date))
    con.commit()
    con.close()

#gets all the journal entries
def get_journal_entries():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM journal ORDER BY date DESC")
    journal_entries = cur.fetchall()
    con.close()
    return journal_entries

#updates a journal entry
def update_journal_entry(id, title, content, date):
    con = get_connection()
    cur = con.cursor()
    cur.execute("UPDATE journal SET title = ?, content = ?, date = ? WHERE id = ?", (title, content, date, id))
    con.commit()
    con.close()

#Deletes a journal entry
def delete_journal_entry(id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM journal WHERE id = ?", (id,))
    con.commit()
    con.close()

#gets journal entries for a specific date
def get_journal_entries_for_date(date):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM journal WHERE date = ? ORDER BY date DESC", (date,))
    journal_entries = cur.fetchall()
    con.close()
    return journal_entries
