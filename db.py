import sqlite3
def get_connection():
    return sqlite3.connect("deskos.db")
con = get_connection()
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY AUTOINCREMENT, task_name TEXT, description TEXT, priority TEXT, due_date TEXT, category TEXT, completed INTEGER)")
columns = {row[1] for row in cur.execute("PRAGMA table_info(tasks)")}
if "description" not in columns:
    cur.execute("ALTER TABLE tasks ADD COLUMN description TEXT")
cur.execute("CREATE TABLE IF NOT EXISTS habits(id INTEGER PRIMARY KEY AUTOINCREMENT, habit_name TEXT, description TEXT, category TEXT, created_at TEXT, active INTEGER)")
cur.execute("CREATE TABLE IF NOT EXISTS habit_logs(id INTEGER PRIMARY KEY AUTOINCREMENT, habit_id INTEGER, date TEXT, completed INTEGER, FOREIGN KEY (habit_id) REFERENCES habits(id))")
con.commit()

con.close()
