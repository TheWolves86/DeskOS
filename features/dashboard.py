import sys
from pathlib import Path
from datetime import date, timedelta

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from db import get_connection

#it gets today
def get_today():
    return date.today().isoformat()

#it gets current month
def current_month():
    return date.today().replace(day=1).isoformat()

#it gets the task summary
def get_task_summary():
    con = get_connection()
    try:
        cur = con.cursor()
        today = get_today()
        cur.execute(
            """
            SELECT
                COUNT(*),
                COALESCE(SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END), 0),
                COALESCE(SUM(CASE WHEN completed = 0 THEN 1 ELSE 0 END), 0),
                COALESCE(SUM(
                    CASE WHEN due_date = ? AND completed = 0
                    THEN 1 ELSE 0 END
                ), 0),
                COALESCE(SUM(
                    CASE WHEN due_date < ? AND completed = 0
                    THEN 1 ELSE 0 END
                ), 0)
            FROM tasks
            """,
            (today, today)
        )
        row = cur.fetchone()

        return {
            "total": row[0],
            "completed": row[1],
            "pending": row[2],
            "due_today": row[3],
            "overdue": row[4]
        }
    finally:
        con.close()

#it gets the summary of habits
def get_habit_summary():
    con = get_connection()
    try:
        cur = con.cursor()
        today = get_today()
        cur.execute("SELECT COUNT(*) FROM habits WHERE active = 1")
        active_habits = cur.fetchone()[0]
        cur.execute(
            """
            SELECT COUNT(*)
            FROM habits AS h
            JOIN habit_logs AS l ON h.id = l.habit_id
            WHERE h.active = 1
              AND l.date = ?
              AND l.completed = 1
            """,
            (today,)
        )
        completed_today = cur.fetchone()[0]
        remaining = max(0, active_habits - completed_today)
        return {
            "active": active_habits,
            "completed_today": completed_today,
            "remaining": remaining
        }
    finally:
        con.close()

#it gets the summary of finances
def get_finance_summary():
    con = get_connection()
    try:
        cur = con.cursor()
        month = current_month()

        cur.execute(
            """
            SELECT
                COALESCE(SUM(
                    CASE WHEN type = 'income'
                    THEN amount ELSE 0 END
                ), 0),
                COALESCE(SUM(
                    CASE WHEN type = 'expense'
                    THEN amount ELSE 0 END
                ), 0)
            FROM transactions
            """
        )

        all_income, all_expenses = cur.fetchone()

        cur.execute(
            """
            SELECT
                COALESCE(SUM(
                    CASE WHEN type = 'income'
                    THEN amount ELSE 0 END
                ), 0),
                COALESCE(SUM(
                    CASE WHEN type = 'expense'
                    THEN amount ELSE 0 END
                ), 0)
            FROM transactions
            WHERE substr(date, 1, 7) = ?
            """,
            (month,)
        )

        monthly_income, monthly_expenses = cur.fetchone()

        return {
            "total_income": all_income,
            "total_expenses": all_expenses,
            "balance": all_income - all_expenses,
            "monthly_income": monthly_income,
            "monthly_expenses": monthly_expenses,
            "monthly_balance": monthly_income - monthly_expenses
        }

    finally:
        con.close()

#It gets the upcoming tasks
def get_upcoming_tasks(days=7):
    con = get_connection()
    try:
        cur = con.cursor()
        today = date.today()
        end_date = (today + timedelta(days=days)).isoformat()
        cur.execute(
            """
            SELECT *
            FROM tasks
            WHERE completed = 0
                AND due_date >= ?
                AND due_date <= ?
            ORDER BY due_date ASC
            LIMIT 10
            """,
            (today.isoformat(), end_date)
        )

        return cur.fetchall()
    finally:
        con.close()

#it gets the recent notes
def get_recent_notes(limit=5):
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(
            """
            SELECT *
            FROM notes
            ORDER BY created_at DESC, id DESC
            LIMIT ?
            """,
            (limit,)
        )

        return cur.fetchall()

    finally:
        con.close()

#ut gets the summary of content
def get_content_summary():
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM notes")
        total_notes = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM journal")
        total_journal = cur.fetchone()[0]
        return {
            "total_notes": total_notes,
            "total_journal": total_journal
        }
    finally:
        con.close()

#It gets the summary of the dashboard
def get_dashboard_summary():
    return {
        "tasks": get_task_summary(),
        "habits": get_habit_summary(),
        "finance": get_finance_summary(),
        "content": get_content_summary(),
        "upcoming_tasks": get_upcoming_tasks(days=7),
        "recent_notes": get_recent_notes(limit=5),
    }

#