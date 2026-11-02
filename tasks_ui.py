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
            displayed_date = due_date if due_date else "Not Set"

            self.table.insert(
                "",
                "end",
                iid=str(task_id),
                values=(
                    task_id,
                    name,
                    priority,
                    displayed_date,
                    category,
                    status
                )
            )


            visible_count += 1

        self.count_label.configure(
            text=f"{visible_count} tasks"
        )

    def open_task_form(self, task=None):
        editing = task is not None

        window = tk.Toplevel(self)
        window.title("Edit Task" if editing else "Add Task")
        window.geometry("420x460")
        window.resizable(False, False)
        window.configure(bg=BG)
        window.transient(self.winfo_toplevel())
        window.grab_set()

        tk.Label(
            window,
            text="Edit Task" if editing else "Add New Task",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w", padx=25, pady=(22, 15))

        form = tk.Frame(window, bg=BG)
        form.pack(fill="both", expand=True, padx=25)

        def add_field(label_text, default=""):
            tk.Label(
                form,
                text=label_text,
                bg=BG,
                fg=TEXT,
                font=("Segoe UI", 10)
            ).pack(anchor="w", pady=(7, 3))

            entry =ttk.Entry(form)
            entry.pack(fill="x")
            entry.insert(0, default)
            return entry

        name_entry = add_field(
            "Task name *",
            task[1] if editing else ""
        )

        description_entry = add_field(
            "Description",
            task[2] if editing else ""
        )

        tk.Label(
            form,
            text="Priority",
            bg=BG,
            fg=TEXT
        ).pack(anchor="w", pady=(7, 3))

        priority_var = tk.StringVar(
            value=task[3] if editing else "Medium"
        )

        ttk.Combobox(
            form,
            textvariable=priority_var,
            values=["Low", "Medium", "High"],
            state="readonly"
        ).pack(fill="x")

        due_entry = add_field(
            "Due date (YYYY-MM-DD, optional)",
            task[4] or "" if editing else ""
        )

        category_entry = add_field(
            "Category",
            task[5] or "" if editing else "Personal"
        )

        def save_task():
            name = name_entry.get().strip()
            description = description_entry.get().strip()
            priority = priority_var.get()
            due_date = due_entry.get().strip()
            category = category_entry.get().strip()

            if not name:
                messagebox.showwarning(
                    "Missing Information",
                    "Please enter a task name.",
                    parent=window
                )
                return

            if due_date:
                try:
                    parsed_date = date.fromisoformat(due_date)
                    if parsed_date.isoformat() != due_date:
                        raise ValueError
                except ValueError:
                    messagebox.showwarning(
                        "Invalid Date",
                        "Use the YYYY-MM-DD format.",
                        parent=window
                    )
                    return

                try:
                    if editing:
                        task_backend.update_task(
                            task[0],
                            name,
                            description,
                            priority,
                            due_date,
                            category
                        )
                    else:
                        task_backend.add_task(
                            name,
                            description,
                            priority,
                            due_date,
                            category
                        )

                    window.destroy()
                    self.refresh_tasks()

                except Exception as error:
                    messagebox.showerror(
                        "Could Not Save",
                        str(error),
                        parent=window
                    )

            tk.Button(
                window,
                text="Save Task",
                command=save_task,
                bg=TEAL,
                fg=WHITE,
                relief="flat",
                padx=18,
                pady=9,
                cursor="hand2"
            ).pack(anchor="e", padx=25, pady=20)

        def get_selected_task(self):
            selected = self.table.selection()

            if not selected:
                messagebox.showinfo(
                    "Select a Task",
                    "Please select a task first."
                )
                return None

            task_id = int(selected[0])

            for task in task_backend.get_tasks():
                if task[0] == task_id:
                    return task

            messagebox.showerror(
                "Task Not Found",
                "This task could not be found in the database."
            )
            return None

        def edit_selected_task(self):
            task = self.get_selected_task()

            if task is not None:
                self.open_task_form(task)

        def complete_selected_task(self):
            task = self.get_selected_task()

            if task is None:
                return

            if task[6]:
                messagebox.showinfo(
                    "Task Already Completed",
                    "This task is already marked as completed."
                )
                return

            try:
                task_backend.complete_task(task[0])
                self.refresh_tasks()
            except Exception as error:
                messagebox.showerror(
                    "Could Not Complete Task",
                    str(error)
                )

        def delete_selected_task(self):
            task = self.get_selected_task()

        if task is None:
            return

        confirm = messagebox.askyesno(
            "Delete Task",
            f"Delete '{task[1]}'?\nThis cannot be undone."
        )

        if not confirm:
            return

        try:
            task_backend.delete_task(task[0])
            self.refresh_tasks()
        except Exception as error:
            messagebox.showerror(
                "Could Not Delete Task",
                str(error)
            )

