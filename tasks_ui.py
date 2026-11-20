
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from features import tasks as backend


BG = "#F4F6F3"
WHITE = "#FFFFFF"
TEAL = "#268477"
DARK = "#123B38"
TEXT = "#243532"
MUTED = "#7B8985"
BORDER = "#E3EAE6"


class TasksScreen(ttk.Frame):
    #initializez the application
    def __init__(self, parent):
        super().__init__(parent, padding=24)

        self.selected_id = None
        self.tasks = []

        self.setup_styles()
        self.build_ui()
        self.refresh_tasks()

    #setups the style
    def setup_styles(self):
        style = ttk.Style()
        style.configure(
            "Tasks.Treeview",
            background=WHITE,
            foreground=TEXT,
            fieldbackground=WHITE,
            rowheight=38,
            font=("Segoe UI", 10),
            borderwidth=0
        )
        style.configure(
            "Tasks.Treeview.Heading",
            background="#EDF2EF",
            foreground=DARK,
            font=("Segoe UI", 9, "bold"),
            relief="flat"
        )
        style.map(
            "Tasks.Treeview",
            background=[("selected", "#DCEDE8")],
            foreground=[("selected", DARK)]
        )

    #builds the ui
    def build_ui(self):
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0, 20))

        ttk.Label(
            header,
            text="Tasks",
            font=("Segoe UI", 23, "bold"),
            foreground=DARK
        ).pack(side="left")

        ttk.Label(
            header,
            text="Plan your work and get things done.",
            foreground=MUTED,
            font=("Segoe UI", 10)
        ).pack(side="left", padx=16, pady=(9, 0))

        tk.Button(
            header,
            text="+ New Task",
            command=self.new_task,
            bg=TEAL,
            fg="white",
            activebackground=DARK,
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=18,
            pady=9,
            cursor="hand2"
        ).pack(side="right")

        # Summary cards
        summary = tk.Frame(self, bg=BG)
        summary.pack(fill="x", pady=(0, 18))

        self.pending_label = self.create_stat(summary, "Pending", "0")
        self.completed_label = self.create_stat(summary, "Completed", "0")
        self.total_label = self.create_stat(summary, "Total tasks", "0")

        # Main layout
        body = ttk.Frame(self)
        body.pack(fill="both", expand=True)

        left = tk.Frame(
            body,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))

        ttk.Label(
            left,
            text="Task List",
            font=("Segoe UI", 13, "bold"),
            foreground=DARK,
            background=WHITE
        ).pack(anchor="w", padx=16, pady=(16, 12))

        filters = tk.Frame(left, bg=WHITE)
        filters.pack(fill="x", padx=16, pady=(0, 12))

        self.search_var = tk.StringVar()
        ttk.Entry(
            filters,
            textvariable=self.search_var
        ).pack(side="left", fill="x", expand=True)

        self.search_var.trace_add(
            "write",
            lambda *_: self.refresh_tasks()
        )

        self.filter_var = tk.StringVar(value="All")

        self.filter_box = ttk.Combobox(
            filters,
            textvariable=self.filter_var,
            values=["All", "Pending", "Completed"],
            state="readonly",
            width=12
        )
        self.filter_box.pack(side="right", padx=(8, 0))
        self.filter_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.refresh_tasks()
        )

        columns = ("task", "priority", "due", "status")

        self.tree = ttk.Treeview(
            left,
            columns=columns,
            show="headings",
            style="Tasks.Treeview"
        )

        for column, heading in [
            ("task", "TASK"),
            ("priority", "PRIORITY"),
            ("due", "DUE DATE"),
            ("status", "STATUS")
        ]:
            self.tree.heading(column, text=heading)

        self.tree.column("task", width=180)
        self.tree.column("priority", width=85)
        self.tree.column("due", width=100)
        self.tree.column("status", width=85)

        self.tree.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 12)
        )
        self.tree.bind("<<TreeviewSelect>>", self.select_task)

        # Editor
        right = tk.Frame(
            body,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        right.pack(side="right", fill="both", expand=True)

        ttk.Label(
            right,
            text="Task Details",
            font=("Segoe UI", 13, "bold"),
            foreground=DARK,
            background=WHITE
        ).pack(anchor="w", padx=20, pady=(18, 16))

        self.name_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.priority_var = tk.StringVar(value="Medium")
        self.due_var = tk.StringVar()
        self.category_var = tk.StringVar()

        self.add_field(right, "TASK NAME", self.name_var)
        self.add_field(right, "DESCRIPTION", self.description_var)
        self.add_field(right, "CATEGORY", self.category_var)

        ttk.Label(
            right,
            text="PRIORITY",
            background=WHITE,
            foreground=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", padx=20, pady=(8, 4))

        ttk.Combobox(
            right,
            textvariable=self.priority_var,
            values=["Low", "Medium", "High"],
            state="readonly"
        ).pack(fill="x", padx=20, pady=(0, 12))

        self.add_field(right, "DUE DATE (YYYY-MM-DD)", self.due_var)

        self.completed_var = tk.BooleanVar(value=False)

        tk.Checkbutton(
            right,
            text="Mark as completed",
            variable=self.completed_var,
            bg=WHITE,
            fg=TEXT,
            activebackground=WHITE,
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=20, pady=10)

        actions = tk.Frame(right, bg=WHITE)
        actions.pack(fill="x", padx=20, pady=(12, 18))

        tk.Button(
            actions,
            text="Save Task",
            command=self.save_task,
            bg=TEAL,
            fg="white",
            activebackground=DARK,
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=18,
            pady=9,
            cursor="hand2"
        ).pack(side="left")

        tk.Button(
            actions,
            text="Delete",
            command=self.delete_task,
            bg="#FCEBE9",
            fg="#B64D45",
            relief="flat",
            padx=14,
            pady=9,
            cursor="hand2"
        ).pack(side="right")

    #Creates a stat ig
    def create_stat(self, parent, title, value):
        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        card.pack(side="left", fill="x", expand=True, padx=(0, 10))

        tk.Label(
            card,
            text=title,
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=14, pady=(10, 0))

        label = tk.Label(
            card,
            text=value,
            bg=WHITE,
            fg=DARK,
            font=("Segoe UI", 19, "bold")
        )
        label.pack(anchor="w", padx=14, pady=(0, 10))

        return label

    #adds a field
    def add_field(self, parent, label, variable):
        ttk.Label(
            parent,
            text=label,
            background=WHITE,
            foreground=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", padx=20, pady=(6, 4))

        ttk.Entry(
            parent,
            textvariable=variable
        ).pack(fill="x", padx=20, pady=(0, 8))

    #Refreshes the tasks
    def refresh_tasks(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.tasks = backend.get_tasks()

        completed = sum(1 for task in self.tasks if task[6])
        total = len(self.tasks)

        self.pending_label.config(text=str(total - completed))
        self.completed_label.config(text=str(completed))
        self.total_label.config(text=str(total))

        query = self.search_var.get().lower().strip()
        selected_filter = self.filter_var.get()

        for task in self.tasks:
            task_id, name, description, priority, due, category, done = task

            if query and query not in (
                str(name) + " " + str(description) + " " + str(category)
            ).lower():
                continue

            if selected_filter == "Pending" and done:
                continue

            if selected_filter == "Completed" and not done:
                continue

            self.tree.insert(
                "",
                "end",
                iid=str(task_id),
                values=(
                    name,
                    priority,
                    due or "—",
                    "Completed" if done else "Pending"
                )
            )

    #opens up a form for new task
    def new_task(self):
        self.selected_id = None

        self.name_var.set("")
        self.description_var.set("")
        self.category_var.set("")
        self.priority_var.set("Medium")
        self.due_var.set("")
        self.completed_var.set(False)

        for item in self.tree.selection():
            self.tree.selection_remove(item)

    #selectes a task so we can perform crud
    def select_task(self, event=None):
        selection = self.tree.selection()
        if not selection:
            return

        task_id = int(selection[0])

        for task in self.tasks:
            if task[0] == task_id:
                self.selected_id = task_id
                self.name_var.set(task[1] or "")
                self.description_var.set(task[2] or "")
                self.priority_var.set(task[3] or "Medium")
                self.due_var.set(task[4] or "")
                self.category_var.set(task[5] or "")
                self.completed_var.set(bool(task[6]))
                break

    #Saves a task
    def save_task(self):
        name = self.name_var.get().strip()
        description = self.description_var.get().strip()
        priority = self.priority_var.get()
        due = self.due_var.get().strip()
        category = self.category_var.get().strip()
        completed = int(self.completed_var.get())

        if not name:
            messagebox.showwarning("Missing name", "Enter a task name.")
            return

        if due:
            try:
                date.fromisoformat(due)
            except ValueError:
                messagebox.showerror(
                    "Invalid date",
                    "Use YYYY-MM-DD format."
                )
                return

        try:
            if self.selected_id is None:
                backend.add_task(
                    name, description, priority, due, category, completed
                )
            else:
                backend.update_task(
                    self.selected_id,
                    name,
                    description,
                    priority,
                    due,
                    category
                )

                if completed:
                    backend.complete_task(self.selected_id)
                else:
                    backend.uncomplete_task(self.selected_id)

            self.refresh_tasks()
            self.new_task()

        except Exception as error:
            messagebox.showerror("Error", str(error))

    #Deletes a task
    def delete_task(self):
        if self.selected_id is None:
            messagebox.showwarning(
                "No task selected",
                "Select a task first."
            )
            return

        if not messagebox.askyesno(
            "Delete task",
            "Are you sure you want to delete this task?"
        ):
            return

        try:
            backend.delete_task(self.selected_id)
            self.new_task()
            self.refresh_tasks()
        except Exception as error:
            messagebox.showerror("Error", str(error))
