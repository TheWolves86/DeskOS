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
        filters.pack(side="left", padx=8)

        filters.bind(
            "<<ComboboxSelected>>",
            lambda event: self.refresh_tasks()
        )

        add_button = tk.Button(
            toolbar,
            text="+ Add Task",
            command=self.open_task_form(),
            bg=TEAL,
            fg=WHITE,
            activebackground=TEAL_LIGHT,
            activeforeground=WHITE,
            relief="flat",
            padx=14,
            pady=8,
            cursor="hand2"
        )
        add_button.pack(fill="both", expand=True)

    def build_task_table(self):
        table_frame = ttk.Frame(
            self,
            style="Tasks.TFrame",
            padding=(25,5,25,10)
        )
        table_frame.pack(fill="both", expand=True)

        columns=(
            "id",
            "task",
            "priority",
            "due_date",
            "category",
            "status"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Tasks.Treeview",
            selectmode="browse"
        )

        self.table.heading("id", text="ID")
        self.table.heading("task", text="Task")
        self.table.heading("priority", text="Priority")
        self.table.heading("due_date", text="Due Date")
        self.table.heading("category", text="Category")
        self.table.heading("status", text="Status")

        self.table.column("id", width=40, anchor="center")
        self.table.column("task", width=220)
        self.table.column("priority", width=85, anchor="center")
        self.table.column("due_date", width=105, anchor="center")
        self.table.column("category", width=100)
        self.table.column("status", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.table.bind(
            "<Double-1>",
            lambda event: self.edit_selected_task()
        )

    def build_bottom_bar(self):
        bottom = ttk.Frame(
            self,
            style="Tasks.TFrame",
            padding=(25, 10, 25, 20)
        )
        bottom.pack(fill="x")

        ttk.Button(
            bottom,
            text="Mark Complete",
            command=self.complete_selected_task
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            bottom,
            text="Edit",
            command=self.edit_selected_task
        ).pack(side="left", padx=8)

        ttk.Button(
            bottom,
            text="Delete",
            command=self.delete_selected_task
        ).pack(side="left", padx=8)

        self.count_label = ttk.Label(
            bottom,
            text="0 tasks",
            style="Tasks.TLabel"
        )
        self.count_label.pack(side="right")

    def refresh_tasks(self):
        for item in self.table.get_children():
            self.table.delete(item)

        try:
            tasks = task_backend.get_tasks()
        except Exception as error:
            messagebox.showerror(
                "Database Error",
                 f"Could not load tasks:\n{error}"
            )
            return

        search_text = self.search_var.get().strip().lower()
        selected_filter = self.filter_var.get()
        today = date.today().isoformat()
        visible_count = 0

        for task in tasks:
            task_id, name, description, priority, due_date, category, completed = task

            searchable_text = (
                f"{name} {description} {category} {priority}"
            ).lower()

            if search_text and search_text not in searchable_text:
                continue

            if selected_filter == "Completed" and not completed:
                continue

            if selected_filter == "Today":
                if due_date != today or completed:
                    continue

            if selected_filter == "Upcoming":
                if not due_date or due_date <= today or completed:
                    continue

            status = "Completed" if completed else "Pending"
            

