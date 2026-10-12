import sys
from pathlib import Path
from datetime import date, timedelta

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from db import get_connection


def get_today():
    return date.today().isoformat()

def current_month():
    return date.today().replace(day=1).isoformat()

def get_task_summary():
    con = get_connection()
    try:
        cur = con.cursor()
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
        return {
            "active": active_habits,
            "completed_today": completed_today,
            "remaining": active_habits - completed_today
        }
    finally:
        con.close()

    
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

def get_upcoming_tasks():
    con = get_connection()