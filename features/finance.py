import sys
from pathlib import Path
from datetime import date, timedelta

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from db import get_connection

def add_transaction(amount, description, type, category, date):
    con = get_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO transactions (amount,description,type,category,date) VALUES (?,?,?,?,?)", (amount, description, type, category, date))
    con.commit()
    con.close()

def get_transactions():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM transactions")
    transactions = cur.fetchall()
    con.close()
    return transactions

def update_transaction(id, amount, description, type, category, date):
    con = get_connection()
    cur = con.cursor()
    cur.execute("UPDATE transactions SET amount=?, description=?, type=?, category=?, date=? WHERE id=?", (amount, description, type, category, date, id))
    con.commit()
    con.close()

def delete_transaction(id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM transactions WHERE id=?", (id,))
    con.commit()
    con.close()

def get_transactions_by_type(type):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM transactions WHERE type=?", (type,))
    transactions = cur.fetchall()
    con.close()
    return transactions

def get_balance():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT SUM(amount) from transactions WHERE type=?", ("income",))
    income = cur.fetchone()[0]
    cur.execute("SELECT SUM(amount) from transactions WHERE type=?", ("expense",))
    expense = cur.fetchone()[0]
    if income is None:
        income = 0
    if expense is None:
        expense = 0
    balance = income - expense
    con.close()
    return balance

def get_transactions_by_category(category):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM transactions WHERE category=?", (category,))
    transactions = cur.fetchall()
    con.close()
    return transactions

def get_transactions_by_date(date):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM transactions WHERE date=?", (date,))
    transactions = cur.fetchall()
    con.close()
    return transactions

def get_transactions_between_dates(start_date, end_date):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM transactions WHere date BETWEEN ? AND ?", (start_date, end_date))
    transactions = cur.fetchall()
    con.close()
    return transactions

