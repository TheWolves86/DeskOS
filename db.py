import sqlite3
con = sqlite3.connect("deskos.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY AUTOINCREMENT, task_name TEXT, priority TEXT, due_date TEXT, category TEXT, completed INTEGER)")
con.commit()
con.close()