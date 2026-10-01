import sqlite3
def get_connection():
    return sqlite3.connect("deskos.db")
con = get_connection()
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY AUTOINCREMENT, task_name TEXT, description TEXT, priority TEXT, due_date TEXT, category TEXT, completed INTEGER)")
columns = {row[1] for row in cur.execute("PRAGMA table_info(tasks)")}
if "description" not in columns:
    cur.execute("ALTER TABLE tasks ADD COLUMN description TEXT")
con.commit()

con.close()
