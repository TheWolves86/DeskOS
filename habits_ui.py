import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from features import habits as habit_backend

BG = "#F5F4EF"
TEAL = "#075753"
TEAL_LIGHT = "#167E75"
TEXT = "#173C3A"
MUTED = "#71807A"

class HabitsScreen(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.search_var = tk.StringVar()
        self.filter_var = tk.StringVar(value="Active")
        self.setup_styles()
        self.build_header()
        self.build_summary()
        self.build_toolbar()
        self.build_habit_table()
        self.build_bottom_bar()

        self.refresh_habits()

    def setup_styles(self):
        style = ttk.Style()
        style.configure(
            "Habits.TFrame",
            background=BG
        )
        style.configure(
            "Habits.TLabel",
            background=BG,
            foreground=TEXT,
            font=("Segoe UI", 10)
        )