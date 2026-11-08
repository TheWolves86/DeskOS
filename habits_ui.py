
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from features import habits as habit_backend


# ==========================================
# DESKOS COLOURS
# ==========================================

BG = "#F5F4EF"
TEAL = "#075753"
TEAL_LIGHT = "#167E75"
TEXT = "#173C3A"
MUTED = "#71807A"
WHITE = "#FFFFFF"


# ==========================================
# HABITS SCREEN
# ==========================================

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

    # ======================================
    # STYLES
    # ======================================

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

        style.configure(
            "HabitsTitle.TLabel",
            background=BG,
            foreground=TEXT,
            font=("Segoe UI", 24, "bold")
        )

        style.configure(
            "Habits.Treeview",
            font=("Segoe UI", 10),
            rowheight=38,
            background=WHITE,
            fieldbackground=WHITE
        )

        style.configure(
            "Habits.Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )

    # ======================================
    # HEADER
    # ======================================

    def build_header(self):

        header = ttk.Frame(
            self,
            style="Habits.TFrame",
            padding=(25, 25, 25, 12)
        )

        header.pack(fill="x")

        title = ttk.Label(
            header,
            text="Habits",
            style="HabitsTitle.TLabel"
        )

        title.pack(anchor="w")

        subtitle = ttk.Label(
            header,
            text="Build consistency, one day at a time.",
            style="Habits.TLabel"
        )

        subtitle.pack(anchor="w", pady=(4, 0))

    # ======================================
    # SUMMARY
    # ======================================

    def build_summary(self):

        summary = ttk.Frame(
            self,
            style="Habits.TFrame",
            padding=(25, 10)
        )

        summary.pack(fill="x")

        self.active_label = ttk.Label(
            summary,
            text="Active Habits: 0",
            style="Habits.TLabel"
        )

        self.active_label.pack(side="left")

        self.completed_label = ttk.Label(
            summary,
            text="Completed Today: 0/0",
            style="Habits.TLabel"
        )

        self.completed_label.pack(side="right")

    # ======================================
    # TOOLBAR
    # ======================================

    def build_toolbar(self):

        toolbar = ttk.Frame(
            self,
            style="Habits.TFrame",
            padding=(25, 10)
        )

        toolbar.pack(fill="x")

        # Search

        self.search_entry = ttk.Entry(
            toolbar,
            textvariable=self.search_var
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.refresh_habits()
        )

        # Filters

        filters = ttk.Combobox(
            toolbar,
            textvariable=self.filter_var,
            values=["All", "Active", "Archived"],
            state="readonly",
            width=12
        )

        filters.pack(side="left", padx=8)

        filters.bind(
            "<<ComboboxSelected>>",
            lambda event: self.refresh_habits()
        )

        # Add habit button

        add_button = tk.Button(
            toolbar,
            text="+ Add Habit",
            command=self.open_habit_form,
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

    # ======================================
    # HABIT TABLE
    # ======================================

    def build_habit_table(self):

        table_frame = ttk.Frame(
            self,
            style="Habits.TFrame",
            padding=(25, 5, 25, 10)
        )

        table_frame.pack(
            fill="both",
            expand=True
        )

        columns = (
            "id",
            "habit",
            "category",
            "status",
            "streak"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Habits.Treeview",
            selectmode="browse"
        )

        self.table.heading("id", text="ID")
        self.table.heading("habit", text="Habit")
        self.table.heading("category", text="Category")
        self.table.heading("status", text="Today's Status")
        self.table.heading("streak", text="Streak")

        self.table.column(
            "id",
            width=45,
            anchor="center"
        )

        self.table.column(
            "habit",
            width=230
        )

        self.table.column(
            "category",
            width=130
        )

        self.table.column(
            "status",
            width=130,
            anchor="center"
        )

        self.table.column(
            "streak",
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
            lambda event: self.edit_selected_habit()
        )

    # ======================================
    # BOTTOM BUTTONS
    # ======================================

    def build_bottom_bar(self):

        bottom = ttk.Frame(
            self,
            style="Habits.TFrame",
            padding=(25, 10, 25, 20)
        )

        bottom.pack(fill="x")

        ttk.Button(
            bottom,
            text="Mark Done",
            command=self.complete_selected_habit
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            bottom,
            text="Mark Undone",
            command=self.undo_selected_habit
        ).pack(side="left", padx=8)

        ttk.Button(
            bottom,
            text="Edit",
            command=self.edit_selected_habit
        ).pack(side="left", padx=8)

        ttk.Button(
            bottom,
            text="History",
            command=self.show_history
        ).pack(side="left", padx=8)

        ttk.Button(
            bottom,
            text="Delete",
            command=self.delete_selected_habit
        ).pack(side="left", padx=8)

        self.count_label = ttk.Label(
            bottom,
            text="0 habits",
            style="Habits.TLabel"
        )

        self.count_label.pack(side="right")

    # ======================================
    # REFRESH HABITS
    # ======================================

    def refresh_habits(self):

        for item in self.table.get_children():
            self.table.delete(item)

        try:
            habits = habit_backend.get_habits()

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                f"Could not load habits:\n{error}"
            )

            return

        search_text = self.search_var.get().strip().lower()
        selected_filter = self.filter_var.get()

        active_count = 0
        completed_count = 0
        visible_count = 0

        for habit in habits:

            (
                habit_id,
                name,
                description,
                category,
                created_at,
                active
            ) = habit

            # Count active habits

            if active:
                active_count += 1

                if habit_backend.is_habit_done_today(habit_id):
                    completed_count += 1

            # Apply search

            searchable_text = (
                f"{name or ''} "
                f"{description or ''} "
                f"{category or ''}"
            ).lower()

            if search_text and search_text not in searchable_text:
                continue

            # Apply active/archive filter

            if selected_filter == "Active" and not active:
                continue

            if selected_filter == "Archived" and active:
                continue

            # Today's completion status

            is_done = habit_backend.is_habit_done_today(habit_id)

            status = "Done" if is_done else "Not Done"

            # Calculate streak

            streak = habit_backend.get_habit_streak(habit_id)

            # Insert into table

            self.table.insert(
                "",
                "end",
                iid=str(habit_id),
                values=(
                    habit_id,
                    name,
                    category,
                    status,
                    f"{streak} days"
                )
            )

            visible_count += 1

        # Update summary

        self.active_label.configure(
            text=f"Active Habits: {active_count}"
        )

        self.completed_label.configure(
            text=f"Completed Today: {completed_count}/{active_count}"
        )

        self.count_label.configure(
            text=f"{visible_count} habits"
        )

    # ======================================
    # ADD / EDIT HABIT FORM
    # ======================================

    def open_habit_form(self, habit=None):

        editing = habit is not None

        window = tk.Toplevel(self)

        window.title(
            "Edit Habit" if editing else "Add Habit"
        )

        window.geometry("420x390")
        window.resizable(False, False)
        window.configure(bg=BG)

        window.transient(self.winfo_toplevel())

        # Heading

        tk.Label(
            window,
            text="Edit Habit" if editing else "Add New Habit",
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

        # Reusable field creator

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

        # Habit name

        name_entry = add_field(
            "Habit name *",
            habit[1] if editing else ""
        )

        # Description

        description_entry = add_field(
            "Description",
            (habit[2] or "") if editing else ""
        )

        # Category

        category_entry = add_field(
            "Category",
            (habit[3] or "") if editing else "Personal"
        )

        # Active status

        active_var = tk.IntVar(
            value=habit[5] if editing else 1
        )

        tk.Checkbutton(
            form,
            text="Active habit",
            variable=active_var,
            bg=BG,
            fg=TEXT,
            activebackground=BG,
            selectcolor=WHITE
        ).pack(
            anchor="w",
            pady=12
        )

        # ==================================
        # SAVE HABIT
        # ==================================

        def save_habit():

            name = name_entry.get().strip()

            description = description_entry.get().strip()

            category = category_entry.get().strip()

            active = active_var.get()

            if not name:

                messagebox.showwarning(
                    "Missing Information",
                    "Please enter a habit name.",
                    parent=window
                )

                return

            try:

                if editing:

                    habit_backend.update_habit(
                        habit[0],
                        name,
                        description,
                        category,
                        active
                    )

                else:

                    habit_backend.add_habit(
                        name,
                        description,
                        category,
                        date.today().isoformat(),
                        active
                    )

                window.destroy()

                self.refresh_habits()

            except Exception as error:

                messagebox.showerror(
                    "Could Not Save",
                    str(error),
                    parent=window
                )

        # Save button

        tk.Button(
            window,
            text="Save Habit",
            command=save_habit,
            bg=TEAL,
            fg=WHITE,
            activebackground=TEAL_LIGHT,
            activeforeground=WHITE,
            relief="flat",
            padx=18,
            pady=9,
            cursor="hand2"
        ).pack(
            anchor="e",
            padx=25,
            pady=15
        )

        # Center the form

        window.update_idletasks()

        parent_window = self.winfo_toplevel()

        x = parent_window.winfo_rootx()
        y = parent_window.winfo_rooty()

        parent_width = parent_window.winfo_width()
        parent_height = parent_window.winfo_height()

        window_width = 420
        window_height = 390

        position_x = x + (parent_width - window_width) // 2
        position_y = y + (parent_height - window_height) // 2

        window.geometry(
            f"{window_width}x{window_height}+{position_x}+{position_y}"
        )

        window.grab_set()

        name_entry.focus_set()

    # ======================================
    # GET SELECTED HABIT
    # ======================================

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

            for habit in habit_backend.get_habits():

                if habit[0] == habit_id:
                    return habit

            messagebox.showerror(
                "Habit Not Found",
                "This habit could not be found."
            )

            return None

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )

            return None

    # ======================================
    # EDIT HABIT
    # ======================================

    def edit_selected_habit(self):

        habit = self.get_selected_habit()

        if habit is not None:

            self.open_habit_form(habit)

    # ======================================
    # MARK HABIT DONE
    # ======================================

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

            habit_backend.mark_habit_done_today(habit[0])

            self.refresh_habits()

        except Exception as error:

            messagebox.showerror(
                "Could Not Complete Habit",
                str(error)
            )

    # ======================================
    # MARK HABIT UNDONE
    # ======================================

    def undo_selected_habit(self):

        habit = self.get_selected_habit()

        if habit is None:
            return

        try:

            habit_backend.mark_habit_undone_today(habit[0])

            self.refresh_habits()

        except Exception as error:

            messagebox.showerror(
                "Could Not Update Habit",
                str(error)
            )

    # ======================================
    # DELETE HABIT
    # ======================================

    def delete_selected_habit(self):

        habit = self.get_selected_habit()

        if habit is None:
            return

        confirm = messagebox.askyesno(
            "Delete Habit",
            f"Delete '{habit[1]}'?\nThis cannot be undone."
        )

        if not confirm:
            return

        try:

            habit_backend.delete_habit(habit[0])

            self.refresh_habits()

        except Exception as error:

            messagebox.showerror(
                "Could Not Delete Habit",
                str(error)
            )

    # ======================================
    # HABIT HISTORY
    # ======================================

    def show_history(self):

        habit = self.get_selected_habit()

        if habit is None:
            return

        try:

            history = habit_backend.get_habit_history(habit[0])

        except Exception as error:

            messagebox.showerror(
                "History Error",
                str(error)
            )

            return

        window = tk.Toplevel(self)

        window.title("Habit History")
        window.geometry("350x400")
        window.configure(bg=BG)

        tk.Label(
            window,
            text=habit[1],
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 18, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=20
        )

        table = ttk.Treeview(
            window,
            columns=("date", "status"),
            show="headings"
        )

        table.heading("date", text="Date")
        table.heading("status", text="Status")

        table.column("date", width=150)
        table.column("status", width=120)

        table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        # Sort newest dates first

        history = sorted(
            history,
            key=lambda log: log[0],
            reverse=True
        )

        for log_date, completed in history:

            status = "Done" if completed else "Not Done"

            table.insert(
                "",
                "end",
                values=(log_date, status)
            )
