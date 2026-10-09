import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from db import get_connection

#this adds a task duuh
def add_task(task_name,description, priority, due_date, category, completed=0):
    con = get_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO tasks(task_name, description, priority, due_date, category, completed) VALUES(?,?,?,?,?,?) ", (task_name,description, priority, due_date, category, completed))
    con.commit()
    con.close()

#This gets all the task
def get_tasks():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    con.close()
    return tasks

#this updates a task so u can correct ur mistakes
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

#It deletes a task so u can delete when u didnt do something iykyk
def delete_task(task_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    con.commit()
    con.close()

#this completes a task
def complete_task(task_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    con.commit()
    con.close()

#this uncompletes a task and u r only gonna use it if u r honest
def uncomplete_task(task_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("UPDATE tasks SET completed = 0 WHERE id = ?", (task_id,))
    con.commit()
    con.close()

#it fetches the task by its id 
def get_task_by_id(task_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cur.fetchone()
    con.close()
    return task

#It fetches the task by name so u can search it
def get_task_by_name(task_name):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM tasks WHERE task_name = ?", (task_name,))
    task = cur.fetchone()
    con.close()
    return task

#fetches the task by category
def get_tasks_by_category(category):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM tasks WHERE category = ?", (category,))
    tasks = cur.fetchall()
    con.close()
    return tasks

#fetches all the tasks which are completed so u can flex it
def get_tasks_by_completed():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM tasks WHERE completed = ?", (1,))
    tasks = cur.fetchall()
    con.close()
    return tasks

#fetches all the tasks which ae not completed
def get_tasks_by_uncompleted():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM tasks WHERE completed = ?", (0,))
    tasks = cur.fetchall()
    con.close()
    return tasks

#gets all the tasks for today
def get_today_tasks():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM tasks WHERE due_date = date('now')")
    tasks = cur.fetchall()
    con.close()
    return tasks

#gets the tasks which are due so u can complete them 
def get_overdue_tasks():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM tasks WHERE due_date < date('now') AND completed = 0")
    tasks = cur.fetchall()
    con.close()
    return tasks

