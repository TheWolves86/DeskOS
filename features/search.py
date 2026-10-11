import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from db import get_connection


def _normalize_query(query):
    if query is None:
        return ""
    return str(query).strip()


def _search_table(table_name, columns, query):
    keyword = _normalize_query(query)
    if not keyword:
        return []

    pattern = f"%{keyword}%"
    clause = " OR ".join(f"{column} LIKE ?" for column in columns)
    sql = f"SELECT * FROM {table_name} WHERE {clause}"

    con = get_connection()
    try:
        cur = con.cursor()
        return cur.execute(sql, (pattern,) * len(columns)).fetchall()
    finally:
        con.close()


def search_tasks(query):
    return _search_table("tasks", ("task_name", "description", "category", "priority"), query)


def search_journal(query):
    return _search_table("journal", ("title", "content", "date", "created_at"), query)


def search_habits(query):
    return _search_table("habits", ("habit_name", "description", "category"), query)


def search_notes(query):
    return _search_table("notes", ("title", "content", "category"), query)


def search_finances(query):
    return _search_table("transactions", ("description", "category", "type"), query)

def global_search(query):
    results = []

    for row in search_tasks(query):
        results.append(("task", row))
    for row in search_journal(query):
        results.append(("journal", row))
    for row in search_habits(query):
        results.append(("habit", row))
    for row in search_notes(query):
        results.append(("note", row))
    for row in search_finances(query):
        results.append(("finance", row))

    return results

