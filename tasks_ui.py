import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from features import tasks as task_backend



#DeskOs Colours
BG = "#F5F4EF"
TEAL = "#075753"
TEAL_LIGHT = "#167E75"
TEXT = "#173C3A"
MUTED = "#71807A"
WHITE = "#FFFFFF"


#Tasks Screen
class TasksScreen(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.search_var = tk.StringVar()
        self.filter_var = tk.StringVar(value="All")

        self.setup_styles()

        self.build_header()
        self.build_toolbar()
        self.build_task_table()
        self.build_bottom_bar()

        self.refresh_tasks()

    #Styles
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
            rowheight=36,
            background=WHITE,
            fieldbackground=WHITE
        )

        style.configure(
            "Tasks.Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )

    #Header
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
            text="Manage your tasks and stay productive.",
            style="Tasks.TLabel"
        )

        subtitle.pack(anchor="w", pady=(4, 0))

    #Toolbar
    def build_toolbar(self):

        toolbar = ttk.Frame(
            self,
            style="Tasks.TFrame",
            padding=(25, 10)
        )

        toolbar.pack(fill="x")

        #Search bar
        self.search_entry = ttk.Entry(
            toolbar,
            textvariable=self.search_var,
            width=25
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.refresh_tasks()
        )

        #Task filters
        filters = ttk.Combobox(
            toolbar,
            textvariable=self.filter_var,
            values=[
                "All",
                "Today",
                "Upcoming",
                "Completed"
            ],
            state="readonly",
            width=12
        )

        filters.pack(side="left", padx=8)

        filters.bind(
            "<<ComboboxSelected>>",
            lambda event: self.refresh_tasks()
        )

        #Add task button
        add_button = tk.Button(
            toolbar,
            text="+ Add Task",
            command=self.open_task_form,
            bg=TEAL,
            fg=WHITE,
            activebackground=TEAL_LIGHT,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=8,
            cursor="hand2"
        )

        add_button.pack(side="right")

    #Task Table
    def build_task_table(self):

        table_frame = ttk.Frame(
            self,
            style="Tasks.TFrame",
            padding=(25, 5, 25, 10)
        )

        table_frame.pack(
            fill="both",
            expand=True
        )

        columns = (
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

        self.table.column(
            "id",
            width=40,
            anchor="center"
        )

        self.table.column(
            "task",
            width=220
        )

        self.table.column(
            "priority",
            width=85,
            anchor="center"
        )

        self.table.column(
            "due_date",
            width=105,
            anchor="center"
        )

        self.table.column(
            "category",
            width=100
        )

        self.table.column(
            "status",
            width=100,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.table.bind(
            "<Double-1>",
            lambda event: self.edit_selected_task()
        )

    #Bottom Buttons
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
            text="Mark Pending",
            command=self.uncomplete_selected_task
        ).pack(side="left", padx=8)

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

    
    #Refresh Tasks
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

            (
                task_id,
                name,
                description,
                priority,
                due_date,
                category,
                completed
            ) = task

            #Search filter
            searchable_text = (
                f"{name or ''} "
                f"{description or ''} "
                f"{category or ''} "
                f"{priority or ''}"
            ).lower()

            if search_text and search_text not in searchable_text:
                continue

            #Completed filter
            if selected_filter == "Completed" and not completed:
                continue

            #Today's tasks filter
            if selected_filter == "Today":

                if due_date != today or completed:
                    continue

            #Upcoming tasks filter
            if selected_filter == "Upcoming":

                if not due_date or due_date <= today or completed:
                    continue

            #Task status
            status = "Completed" if completed else "Pending"

            displayed_date = due_date if due_date else "Not Set"

            #Insert task into table
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

    # Add / Edit Task Form
    def open_task_form(self, task=None):

        editing = task is not None

        window = tk.Toplevel(self)

        window.title(
            "Edit Task" if editing else "Add Task"
        )

        window.geometry("420x460")
        window.resizable(False, False)
        window.configure(bg=BG)

        window.transient(self.winfo_toplevel())

        #Form heading
        tk.Label(
            window,
            text="Edit Task" if editing else "Add New Task",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 20, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(22, 15)
        )

        form = tk.Frame(
            window,
            bg=BG
        )

        form.pack(
            fill="both",
            expand=True,
            padx=25
        )

        #Reusable form field creator
        def add_field(label_text, default=""):

            tk.Label(
                form,
                text=label_text,
                bg=BG,
                fg=TEXT,
                font=("Segoe UI", 10)
            ).pack(
                anchor="w",
                pady=(7, 3)
            )

            entry = ttk.Entry(form)

            entry.pack(fill="x")

            entry.insert(0, default)

            return entry

        #Task name
        name_entry = add_field(
            "Task name *",
            task[1] if editing else ""
        )

        #Description
        description_entry = add_field(
            "Description",
            task[2] or "" if editing else ""
        )

        #Priority
        tk.Label(
            form,
            text="Priority",
            bg=BG,
            fg=TEXT
        ).pack(
            anchor="w",
            pady=(7, 3)
        )

        priority_var = tk.StringVar(
            value=task[3] if editing else "Medium"
        )

        ttk.Combobox(
            form,
            textvariable=priority_var,
            values=["Low", "Medium", "High"],
            state="readonly"
        ).pack(fill="x")

        #Due date
        due_entry = add_field(
            "Due date (YYYY-MM-DD, optional)",
            task[4] or "" if editing else ""
        )

        #Category
        category_entry = add_field(
            "Category",
            task[5] or "" if editing else "Personal"
        )


        #Save Task
        def save_task():

            name = name_entry.get().strip()

            description = description_entry.get().strip()

            priority = priority_var.get()

            due_date = due_entry.get().strip()

            category = category_entry.get().strip()

            #Required field validation
            if not name:

                messagebox.showwarning(
                    "Missing Information",
                    "Please enter a task name.",
                    parent=window
                )

                return

            #Date validation
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

            #Save to database
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

        #Save button is outside save task function
        save_button = tk.Button(
            window,
            text="Save Task",
            command=save_task,
            bg=TEAL,
            fg=WHITE,
            activebackground=TEAL_LIGHT,
            activeforeground=WHITE,
            relief="flat",
            padx=18,
            pady=9,
            cursor="hand2"
        )

        save_button.pack(
            anchor="e",
            padx=25,
            pady=20
        )

        #Center form over main application
        window.update_idletasks()

        parent_window = self.winfo_toplevel()

        x = parent_window.winfo_rootx()
        y = parent_window.winfo_rooty()

        parent_width = parent_window.winfo_width()
        parent_height = parent_window.winfo_height()

        window_width = 420
        window_height = 460

        position_x = x + (parent_width - window_width) // 2
        position_y = y + (parent_height - window_height) // 2

        window.geometry(
            f"{window_width}x{window_height}+{position_x}+{position_y}"
        )

        window.grab_set()

        name_entry.focus_set()

    
    # Get selected task
    def get_selected_task(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showinfo(
                "Select a Task",
                "Please select a task first."
            )

            return None

        task_id = int(selected[0])

        try:

            task = task_backend.get_task_by_id(task_id)

            if task is None:

                messagebox.showerror(
                    "Task Not Found",
                    "This task could not be found."
                )

                return None

            return task

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )

            return None

    #Edit task
    def edit_selected_task(self):

        task = self.get_selected_task()

        if task is not None:

            self.open_task_form(task)

    #Mark task complete
    def complete_selected_task(self):

        task = self.get_selected_task()

        if task is None:
            return

        if task[6]:

            messagebox.showinfo(
                "Already Completed",
                "This task is already completed."
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

    #Mark task pending
    def uncomplete_selected_task(self):

        task = self.get_selected_task()

        if task is None:
            return

        try:

            task_backend.uncomplete_task(task[0])

            self.refresh_tasks()

        except Exception as error:

            messagebox.showerror(
                "Could Not Update Task",
                str(error)
            )

    #Delete task
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
