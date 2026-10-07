import sys
from pathlib import Path
from datetime import date, timedelta

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from db import get_connection

def add_habit(habit_name, description, category, created_at, active=1):
    con = get_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO habits(habit_name, description, category, created_at, active) VALUES(?,?,?,?,?)", (habit_name, description, category, created_at, active))
    con.commit()
    con.close()

def get_habits():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM habits")
    habits = cur.fetchall()
    con.close()
    return habits

def update_habit(habit_id, habit_name, description, category, active):
    con = get_connection()
    cur = con.cursor()
    cur.execute("UPDATE habits SET habit_name = ?, description = ?, category = ?, active = ? WHERE id = ?", (habit_name, description, category, active, habit_id))
    con.commit()
    con.close()

def delete_habit(habit_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    con.commit()
    con.close()

def log_habit(habit_id, date, completed):
    con = get_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO habit_logs(habit_id, date, completed) VALUES(?,?,?)", (habit_id, date, completed))
    con.commit()
    con.close()

def mark_habit_done_today(habit_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT id FROM habit_logs WHERE habit_id = ? AND date = date('now')", (habit_id,))
    log = cur.fetchone()
    if log:
        cur.execute("UPDATE habit_logs SET completed = 1 WHERE id=?", (log[0],))
    else:
        cur.execute("INSERT INTO habit_logs(habit_id, date, completed) VALUES(?, date('now'), 1)", (habit_id,))
    con.commit()
    con.close()

def is_habit_done_today(habit_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT completed FROM habit_logs WHERE habit_id = ? AND date = date('now')", (habit_id,))
    log = cur.fetchone()
    if log and log[0] == 1:
        con.close()
        return True
    else:
        con.close()
        return False
    
def mark_habit_undone_today(habit_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT id FROM habit_logs WHERE habit_id = ? AND date = date('now')", (habit_id,))
    log = cur.fetchone()
    if log:
        cur.execute("UPDATE habit_logs SET completed = 0 WHERE id=?", (log[0],))
        con.commit()
        con.close()
    else:
        con.close()

def get_habit_history(habit_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT date,completed FROM habit_logs WHERE habit_id=?", (habit_id,))
    logs = cur.fetchall()
    con.close()
    return logs

def get_habit_streak(habit_id):
    history = get_habit_history(habit_id)
    completed_dates = set()

    for log in history:
        if log[1] == 1:
            completed_dates.add(date.fromisoformat(log[0]))

    today = date.today()
    streak = 0
    current_day = today
    while current_day in completed_dates:
        streak += 1
        current_day -= timedelta(days=1)

    return streak




