
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from features import habits as backend

BG = "#F4F6F3"
WHITE = "#FFFFFF"
TEXT = "#183B37"
MUTED = "#82918B"
ACCENT = "#268477"
BORDER = "#E3EAE5"


class HabitsScreen(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=BG)

        self.search_var = tk.StringVar()
        self.filter_var = tk.StringVar(value="Active")

        self.setup_styles()
        self.build_header()
        self.build_summary()
        self.build_toolbar()
        self.build_table()
        self.build_actions()
        self.refresh_habits()

    #Setup all the styless
    def setup_styles(self):
        style = ttk.Style()

        style.configure(
            "Habits.Treeview",
            background=WHITE,
            foreground=TEXT,
            fieldbackground=WHITE,
            rowheight=40,
            borderwidth=0,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Habits.Treeview.Heading",
            background="#EAF0EC",
            foreground=TEXT,
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padding=10
        )

        style.map(
            "Habits.Treeview",
            background=[("selected", "#D5E9E2")],
            foreground=[("selected", TEXT)]
        )

    #Builds the header ig
    def build_header(self):
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=30, pady=(25, 18))

        tk.Label(
            header,
            text="Habits",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 25, "bold")
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Build consistency, one day at a time.",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(4, 0))

    #Summary cards
    def build_summary(self):
        frame = tk.Frame(self, bg=BG)
        frame.pack(fill="x", padx=30, pady=(0, 18))

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        self.active_label = self.create_card(
            frame, 0, "Active Habits", "0", ACCENT
        )

        self.completed_label = self.create_card(
            frame, 1, "Completed Today", "0 / 0", "#3B9B72"
        )

    def create_card(self, parent, column, title, value, color):
        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=(0 if column == 0 else 6, 0 if column == 1 else 6)
        )

        tk.Frame(card, bg=color, height=4).pack(fill="x")

        body = tk.Frame(card, bg=WHITE, padx=17, pady=13)
        body.pack(fill="both", expand=True)

        tk.Label(
            body,
            text=title.upper(),
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w")

        label = tk.Label(
            body,
            text=value,
            bg=WHITE,
            fg=color,
            font=("Segoe UI", 21, "bold")
        )
        label.pack(anchor="w", pady=(7, 0))

        return label

    #Search and filters
    def build_toolbar(self):
        toolbar = tk.Frame(self, bg=BG)
        toolbar.pack(fill="x", padx=30, pady=(0, 15))

        search_frame = tk.Frame(
            toolbar,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        search_frame.pack(side="left", fill="x", expand=True)

        tk.Label(
            search_frame,
            text="⌕",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 16)
        ).pack(side="left", padx=(11, 3))

        ttk.Entry(
            search_frame,
            textvariable=self.search_var
        ).pack(side="left", fill="x", expand=True, ipady=7, padx=7)

        self.search_var.trace_add(
            "write",
            lambda *args: self.refresh_habits()
        )

        ttk.Combobox(
            toolbar,
            textvariable=self.filter_var,
            values=["All", "Active", "Archived"],
            state="readonly",
            width=12
        ).pack(side="left", padx=10, ipady=5)

        self.filter_var.trace_add(
            "write",
            lambda *args: self.refresh_habits()
        )

        tk.Button(
            toolbar,
            text="+  Add Habit",
            command=self.open_habit_form,
            bg=ACCENT,
            fg=WHITE,
            activebackground="#1D6E63",
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            padx=17,
            pady=10,
            cursor="hand2"
        ).pack(side="right")

    #Habit's table
    def build_table(self):
        container = tk.Frame(
            self,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        container.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 15)
        )

        heading = tk.Frame(container, bg=WHITE)
        heading.pack(fill="x", padx=18, pady=15)

        tk.Label(
            heading,
            text="Your Habits",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 13, "bold")
        ).pack(side="left")

        self.count_label = tk.Label(
            heading,
            text="0 habits",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9)
        )
        self.count_label.pack(side="right")

        tk.Frame(container, bg=BORDER, height=1).pack(fill="x")

        area = tk.Frame(container, bg=WHITE)
        area.pack(fill="both", expand=True, padx=12, pady=12)

        columns = ("id", "habit", "category", "status", "streak")

        self.table = ttk.Treeview(
            area,
            columns=columns,
            show="headings",
            style="Habits.Treeview",
            selectmode="browse"
        )

        headings = {
            "id": "ID",
            "habit": "HABIT",
            "category": "CATEGORY",
            "status": "TODAY",
            "streak": "STREAK"
        }

        for column, title in headings.items():
            self.table.heading(column, text=title)

        self.table.column("id", width=45, anchor="center", stretch=False)
        self.table.column("habit", width=220)
        self.table.column("category", width=130, anchor="center")
        self.table.column("status", width=120, anchor="center")
        self.table.column("streak", width=100, anchor="center")

        self.table.tag_configure("done", foreground="#26845D")
        self.table.tag_configure("pending", foreground=TEXT)
        self.table.tag_configure("archived", foreground=MUTED)

        scrollbar = ttk.Scrollbar(
            area,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.table.bind(
            "<Double-1>",
            lambda event: self.edit_selected_habit()
        )

    #Actions
    def build_actions(self):
        footer = tk.Frame(self, bg=BG)
        footer.pack(fill="x", padx=30, pady=(0, 20))

        self.action_button(
            footer, "✓  Mark Done", self.complete_selected_habit
        ).pack(side="left", padx=(0, 7))

        self.action_button(
            footer, "↺  Mark Undone", self.undo_selected_habit
        ).pack(side="left", padx=7)

        self.action_button(
            footer, "Edit", self.edit_selected_habit
        ).pack(side="left", padx=7)

        self.action_button(
            footer, "History", self.show_history
        ).pack(side="left", padx=7)

        tk.Button(
            footer,
            text="Delete",
            command=self.delete_selected_habit,
            bg="#FCECEB",
            fg="#B64A43",
            activebackground="#F5D8D5",
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            font=("Segoe UI", 9, "bold")
        ).pack(side="left", padx=7)

    def action_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=WHITE,
            fg=TEXT,
            activebackground="#EAF0EC",
            relief="flat",
            bd=0,
            padx=13,
            pady=8,
            cursor="hand2",
            font=("Segoe UI", 9, "bold")
        )

    #Refreshes habit information
    def refresh_habits(self):
        if not hasattr(self, "table"):
            return

        for item in self.table.get_children():
            self.table.delete(item)

        try:
            habits = backend.get_habits()
        except Exception as error:
            messagebox.showerror("Database Error", str(error))
            return

        query = self.search_var.get().strip().lower()
        selected_filter = self.filter_var.get()

        active_count = 0
        completed_count = 0
        visible_count = 0

        for habit in habits:
            habit_id, name, description, category, created_at, active = habit

            is_active = bool(active)
            is_done = backend.is_habit_done_today(habit_id)

            if is_active:
                active_count += 1
                if is_done:
                    completed_count += 1

            searchable = (
                f"{name or ''} {description or ''} {category or ''}"
            ).lower()

            if query and query not in searchable:
                continue

            if selected_filter == "Active" and not is_active:
                continue

            if selected_filter == "Archived" and is_active:
                continue

            streak = backend.get_habit_streak(habit_id)

            status = "Done" if is_done else "Not Done"

            if not is_active:
                tag = "archived"
                status = "Archived"
            else:
                tag = "done" if is_done else "pending"

            self.table.insert(
                "",
                "end",
                iid=str(habit_id),
                values=(
                    habit_id,
                    name,
                    category or "General",
                    status,
                    f"{streak} days"
                ),
                tags=(tag,)
            )

            visible_count += 1

        self.active_label.config(text=str(active_count))
        self.completed_label.config(
            text=f"{completed_count} / {active_count}"
        )
        self.count_label.config(text=f"{visible_count} habits")

    #Add or edit a habit
    def open_habit_form(self, habit=None):
        editing = habit is not None

        window = tk.Toplevel(self)
        window.title("Edit Habit" if editing else "New Habit")
        window.geometry("440x450")
        window.resizable(False, False)
        window.configure(bg=BG)
        window.transient(self.winfo_toplevel())

        tk.Label(
            window,
            text="Edit Habit" if editing else "Create a Habit",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 21, "bold")
        ).pack(anchor="w", padx=28, pady=(24, 4))

        tk.Label(
            window,
            text="Make a small commitment to yourself.",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=28, pady=(0, 15))

        form = tk.Frame(window, bg=BG)
        form.pack(fill="both", expand=True, padx=28)

        def make_field(label, value=""):
            tk.Label(
                form,
                text=label,
                bg=BG,
                fg=TEXT,
                font=("Segoe UI", 9, "bold")
            ).pack(anchor="w", pady=(9, 5))

            entry = ttk.Entry(form)
            entry.pack(fill="x", ipady=5)
            entry.insert(0, str(value or ""))
            return entry

        name_entry = make_field(
            "Habit name *",
            habit[1] if editing else ""
        )

        description_entry = make_field(
            "Description",
            habit[2] if editing else ""
        )

        category_entry = make_field(
            "Category",
            habit[3] if editing else "Personal"
        )

        active_var = tk.IntVar(value=habit[5] if editing else 1)

        tk.Checkbutton(
            form,
            text="Active habit",
            variable=active_var,
            bg=BG,
            fg=TEXT,
            activebackground=BG,
            selectcolor=WHITE,
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=13)

        def save():
            name = name_entry.get().strip()
            description = description_entry.get().strip()
            category = category_entry.get().strip()

            if not name:
                messagebox.showwarning(
                    "Missing Name",
                    "Please enter a habit name.",
                    parent=window
                )
                return

            try:
                if editing:
                    backend.update_habit(
                        habit[0],
                        name,
                        description,
                        category,
                        active_var.get()
                    )
                else:
                    backend.add_habit(
                        name,
                        description,
                        category,
                        date.today().isoformat(),
                        active_var.get()
                    )

                window.destroy()
                self.refresh_habits()

            except Exception as error:
                messagebox.showerror(
                    "Save Failed",
                    str(error),
                    parent=window
                )

        buttons = tk.Frame(window, bg=BG)
        buttons.pack(fill="x", padx=28, pady=20)

        tk.Button(
            buttons,
            text="Cancel",
            command=window.destroy,
            bg="#E9EFEC",
            fg=TEXT,
            relief="flat",
            padx=16,
            pady=9,
            cursor="hand2"
        ).pack(side="left")

        tk.Button(
            buttons,
            text="Save Habit",
            command=save,
            bg=ACCENT,
            fg=WHITE,
            activebackground="#1D6E63",
            relief="flat",
            padx=18,
            pady=9,
            cursor="hand2"
        ).pack(side="right")

        window.update_idletasks()

        parent = self.winfo_toplevel()
        x = parent.winfo_rootx() + (parent.winfo_width() - 440) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - 450) // 2

        window.geometry(f"+{x}+{y}")
        window.grab_set()
        name_entry.focus_set()

    #Get selected habit
    def get_selected_habit(self):
        selected = self.table.selection()

        if not selected:
            messagebox.showinfo(
                "Select a Habit",
                "Please select a habit first."
            )
            return None

        habit_id = int(selected[0])

        try:
            return next(
                (habit for habit in backend.get_habits()
                 if habit[0] == habit_id),
                None
            )
        except Exception as error:
            messagebox.showerror("Database Error", str(error))
            return None

    #edits selected habit
    def edit_selected_habit(self):
        habit = self.get_selected_habit()
        if habit is not None:
            self.open_habit_form(habit)

    #Mark's habit complete
    def complete_selected_habit(self):
        habit = self.get_selected_habit()

        if habit is None:
            return

        if not habit[5]:
            messagebox.showinfo(
                "Archived Habit",
                "Activate this habit before marking it done."
            )
            return

        try:
            backend.mark_habit_done_today(habit[0])
            self.refresh_habits()
        except Exception as error:
            messagebox.showerror("Update Failed", str(error))

    #Undos today's completion
    def undo_selected_habit(self):
        habit = self.get_selected_habit()

        if habit is None:
            return

        try:
            backend.mark_habit_undone_today(habit[0])
            self.refresh_habits()
        except Exception as error:
            messagebox.showerror("Update Failed", str(error))

    # Delete selected habit
    def delete_selected_habit(self):
        habit = self.get_selected_habit()

        if habit is None:
            return

        confirm = messagebox.askyesno(
            "Delete Habit",
            f"Delete '{habit[1]}'? This cannot be undone."
        )

        if not confirm:
            return

        try:
            backend.delete_habit(habit[0])
            self.refresh_habits()
        except Exception as error:
            messagebox.showerror("Delete Failed", str(error))

    # View habit history
    def show_history(self):
        habit = self.get_selected_habit()

        if habit is None:
            return

        try:
            history = backend.get_habit_history(habit[0])
        except Exception as error:
            messagebox.showerror("History Error", str(error))
            return

        window = tk.Toplevel(self)
        window.title("Habit History")
        window.geometry("420x430")
        window.configure(bg=BG)
        window.transient(self.winfo_toplevel())

        tk.Label(
            window,
            text=habit[1],
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w", padx=22, pady=(22, 4))

        tk.Label(
            window,
            text="Your recorded progress",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=22, pady=(0, 15))

        table = ttk.Treeview(
            window,
            columns=("date", "status"),
            show="headings",
            style="Habits.Treeview"
        )

        table.heading("date", text="DATE")
        table.heading("status", text="STATUS")

        table.column("date", width=180, anchor="center")
        table.column("status", width=150, anchor="center")

        table.pack(fill="both", expand=True, padx=22, pady=(0, 22))

        for log_date, completed in sorted(
            history,
            key=lambda item: item[0],
            reverse=True
        ):
            table.insert(
                "",
                "end",
                values=(
                    log_date,
                    "Done" if completed else "Not Done"
                )
            )
