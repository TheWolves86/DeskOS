import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from db import get_connection

def add_task(task_name,description, priority, due_date, category, completed=0):
    con = get_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO tasks(task_name, description, priority, due_date, category, completed) VALUES(?,?,?,?,?,?) ", (task_name,description, priority, due_date, category, completed))
    con.commit()
    con.close()

def get_tasks():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    con.close()
    return tasks

def update_task(task_id,task_name, description, priority, due_date, category):
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        """
        UPDATE tasks
        SET task_name = ?,
            description = ?,
            priority = ?,
            due_date = ?,
            category = ?
        WHERE id =?
        """,
        (task_name, description, priority, due_date, category, task_id)
    )
    con.commit()
    con.close()

