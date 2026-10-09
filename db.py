import sqlite3
#opens ups a connection to the database
def get_connection():
    return sqlite3.connect("deskos.db")
con = get_connection()
cur = con.cursor()
#Creates the tasks table
cur.execute("CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY AUTOINCREMENT, task_name TEXT, description TEXT, priority TEXT, due_date TEXT, category TEXT, completed INTEGER)")
columns = {row[1] for row in cur.execute("PRAGMA table_info(tasks)")}
if "description" not in columns:
    cur.execute("ALTER TABLE tasks ADD COLUMN description TEXT")
#Creates the habits table
cur.execute("CREATE TABLE IF NOT EXISTS habits(id INTEGER PRIMARY KEY AUTOINCREMENT, habit_name TEXT, description TEXT, category TEXT, created_at TEXT, active INTEGER)")
#creates the habit logs table
cur.execute("CREATE TABLE IF NOT EXISTS habit_logs(id INTEGER PRIMARY KEY AUTOINCREMENT, habit_id INTEGER, date TEXT, completed INTEGER,Unique(habit_id, date), FOREIGN KEY (habit_id) REFERENCES habits(id))")
#creates the transactions table
cur.execute("CREATE TABLE IF NOT EXISTS transactions(id INTEGER PRIMARY KEY AUTOINCREMENT,amount REAL, description TEXT, type TEXT, category TEXT, date TEXT)")
#creates the notes table
cur.execute("CREATE TABLE IF NOT EXISTS notes(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, category TEXT, created_at TEXT)")
con.commit()
con.close()
