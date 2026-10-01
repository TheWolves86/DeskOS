import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from db import get_connection

con = get_connection()
cur = con.cursor()

def add_task(task_name,description, priority, due_date, category, completed=0):
    cur.execute("INSERT INTO tasks(task_name, description, priority, due_date, category, completed) VALUES(?,?,?,?,?,?) ", (task_name,description, priority, due_date, category, completed))
    con.commit()
add_task("Task 1", "This is a task", 1, "2023-01-01", "Personal", 0)