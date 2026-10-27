import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from features import tasks as task_backend

BG = "#F5F4EF"
TEAL = "#075753"
TEAL_LIGHT = "#167E75"
TEXT = "#173C3A"
MUTED = "#71807A"
WHITE = "#FFFFFF"

class TasksScreen(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.configure(style="Tasks.TFrame")

        self.search_var = tk.StringVar()
        self.filter_var = tk.StringVar(value="All")

        self.setup_styles()
        self.build_header()
        self.build_toolbar()
        self.build_task_table()
        self.build_bottom_bar()
        self.refresh_tasks()

    def setup_styles(self):
        style = ttk.Style()
        style.configure(
            "Tasks.TFrame",
            background=BG
        )
        style.configure(
            "Tasks.TLabel",
            background=BG,
            foreground=TEXT,
            font=("Segoe UI", 10)
        )
        style.configure(
            "TasksTitle.TLabel",
            background=BG,
            foreground=TEXT,
            font=("Segoe UI", 24, "bold")
        )

        style.configure(
            "Tasks.Treeview",
            font=("Segoe UI", 10),
            rowheight = 36,
            background=WHITE,
            fieldbackground=WHITE
        )

        style.configure(
            "Tasks.Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )

    def build_header(self):
        header = ttk.Frame(
            self,
            style="Tasks.TFrame",
            padding=(25, 25, 25, 12)
        )
        header.pack(fill="x")

        title = ttk.Label(
            header,
            text="Tasks",
            style="TasksTitle.TLabel"
        )
        title.pack(anchor="w")

        subtitle = ttk.Label(
            header,
            text="Manage your tasks and stay productive",
            style="Tasks.TLabel"
        )
        subtitle.pack(anchor="w", pady=(4, 0))

    def build_toolbar(self):
        toolbar = ttk.Frame(
            self,
            style="Tasks.TFrame",
            padding=(25, 10)
        )
        toolbar.pack(fill="x")

        self.search_entry = ttk.Entry(
            toolbar,
            textvariable=self.search_var,
            width=25
        )
        self.search_entry.pack(side="left", fill="x", expand=True)

        self.search_entry.bind(
             "<KeyRelease>",
             lambda event: self.refresh_tasks()
        )

        filters = ttk.Combobox(
            toolbar,
            textvariable=self.filter_var,
            values=["All", "Today", "Upcoming", "Completed"],
            state="readonly",
            width=12
        )