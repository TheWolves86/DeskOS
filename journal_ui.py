
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from features import journal as journal_backend


class JournalScreen(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.bg_color = "#F5F4EF"
        self.teal = "#075753"
        self.dark_text = "#173C3A"
        self.muted_text = "#71817D"

        self.selected_entry_id = None

        self.setup_styles()
        self.create_layout()
        self.refresh_entries()

    #Styles
    def setup_styles(self):

        style = ttk.Style()

        style.configure(
            "Journal.TFrame",
            background=self.bg_color
        )

        style.configure(
            "Journal.Treeview",
            background="white",
            foreground=self.dark_text,
            fieldbackground="white",
            rowheight=38,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Journal.Treeview.Heading",
            background="#E9EFEC",
            foreground=self.dark_text,
            font=("Segoe UI", 10, "bold"),
            relief="flat"
        )

        style.map(
            "Journal.Treeview",
            background=[("selected", "#D5E9E4")],
            foreground=[("selected", self.dark_text)]
        )

    #Main Layout
    def create_layout(self):

        self.configure(style="Journal.TFrame")

        # Header
        header = tk.Frame(self, bg=self.bg_color)
        header.pack(fill="x", padx=30, pady=(25, 15))

        tk.Label(
            header,
            text="Journal",
            bg=self.bg_color,
            fg=self.dark_text,
            font=("Segoe UI", 24, "bold")
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Reflect on your day and preserve your memories.",
            bg=self.bg_color,
            fg=self.muted_text,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(4, 0))

        # Main content
        content = tk.Frame(self, bg=self.bg_color)
        content.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(10, 25)
        )

        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=2)
        content.rowconfigure(0, weight=1)

        self.create_entries_list(content)
        self.create_editor(content)

    #Entries List
    def create_entries_list(self, parent):

        left = tk.Frame(
            parent,
            bg="white",
            highlightbackground="#E5E9E6",
            highlightthickness=1
        )

        left.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10)
        )
        left.columnconfigure(0, weight=1)
        left.rowconfigure(3, weight=1)

        # Heading
        heading = tk.Frame(left, bg="white")
        heading.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 10))

        tk.Label(
            heading,
            text="My Entries",
            bg="white",
            fg=self.dark_text,
            font=("Segoe UI", 14, "bold")
        ).pack(side="left")

        tk.Button(
            heading,
            text="+ New",
            command=self.new_entry,
            bg=self.teal,
            fg="white",
            activebackground="#167E75",
            activeforeground="white",
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2"
        ).pack(side="right")

        # Date filter
        filter_frame = tk.Frame(left, bg="white")
        filter_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 10))

        self.filter_date_var = tk.StringVar(value="")

        ttk.Entry(
            filter_frame,
            textvariable=self.filter_date_var,
            font=("Segoe UI", 10)
        ).pack(
            side="left",
            fill="x",
            expand=True,
            ipady=6
        )

        tk.Button(
            filter_frame,
            text="Filter",
            command=self.filter_by_date,
            bg="#E5EFEB",
            fg=self.dark_text,
            relief="flat",
            padx=10,
            pady=6,
            cursor="hand2"
        ).pack(side="left", padx=(6, 0))

        tk.Button(
            left,
            text="Show All Entries",
            command=self.refresh_entries,
            bg="#E9EFEC",
            fg=self.dark_text,
            relief="flat",
            padx=10,
            pady=6,
            cursor="hand2"
        ).grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 10))

        # Table
        table_frame = tk.Frame(left, bg="white")
        table_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0, 10))

        self.tree = ttk.Treeview(
            table_frame,
            columns=("id", "title", "date"),
            show="headings",
            style="Journal.Treeview",
            height=5
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("date", text="Date")

        self.tree.column("id", width=35, anchor="center")
        self.tree.column("title", width=140)
        self.tree.column("date", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(side="right", fill="y")

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_entry
        )

        # Delete button
        tk.Button(
            left,
            text="Delete Selected Entry",
            command=self.delete_entry,
            bg="#F8E7E5",
            fg="#B64C43",
            relief="flat",
            padx=10,
            pady=8,
            cursor="hand2"
        ).grid(row=4, column=0, sticky="ew", padx=15, pady=(0, 15))

    #Journal Editor
    def create_editor(self, parent):

        right = tk.Frame(
            parent,
            bg="white",
            highlightbackground="#E5E9E6",
            highlightthickness=1
        )

        right.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        tk.Label(
            right,
            text="Journal Editor",
            bg="white",
            fg=self.dark_text,
            font=("Segoe UI", 14, "bold")
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(18, 15))

        form = tk.Frame(right, bg="white")
        form.grid(row=1, column=0, sticky="nsew", padx=20)

        # Title
        tk.Label(
            form,
            text="Entry Title",
            bg="white",
            fg=self.dark_text,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=(0, 5))

        self.title_var = tk.StringVar()

        ttk.Entry(
            form,
            textvariable=self.title_var,
            font=("Segoe UI", 11)
        ).pack(fill="x", ipady=7, pady=(0, 15))

        # Date
        tk.Label(
            form,
            text="Date (YYYY-MM-DD)",
            bg="white",
            fg=self.dark_text,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=(0, 5))

        self.date_var = tk.StringVar(
            value=date.today().isoformat()
        )

        ttk.Entry(
            form,
            textvariable=self.date_var,
            font=("Segoe UI", 10)
        ).pack(fill="x", ipady=6, pady=(0, 15))

        # Content
        tk.Label(
            form,
            text="Your Thoughts",
            bg="white",
            fg=self.dark_text,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=(0, 5))

        text_frame = tk.Frame(form, bg="white")
        text_frame.pack(fill="both", expand=True)

        self.content_text = tk.Text(
            text_frame,
            wrap="word",
            height=8,
            font=("Segoe UI", 10),
            bg="#FCFCFA",
            fg=self.dark_text,
            relief="flat",
            padx=12,
            pady=12,
            undo=True
        )

        content_scrollbar = ttk.Scrollbar(
            text_frame,
            orient="vertical",
            command=self.content_text.yview
        )

        self.content_text.configure(
            yscrollcommand=content_scrollbar.set
        )

        self.content_text.pack(
            side="left",
            fill="both",
            expand=True
        )

        content_scrollbar.pack(
            side="right",
            fill="y"
        )

        # Save button
        tk.Button(
            right,
            text="Save Entry",
            command=self.save_entry,
            bg=self.teal,
            fg="white",
            activebackground="#167E75",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=9,
            cursor="hand2"
        ).grid(row=2, column=0, sticky="e", padx=20, pady=(10, 18))

        right.columnconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)

    #Refresh Entries
    def refresh_entries(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        entries = journal_backend.get_journal_entries()

        for entry in entries:

            self.tree.insert(
                "",
                "end",
                values=(
                    entry[0],
                    entry[1] or "",
                    entry[3] or ""
                )
            )

    #Filter By Date
    def filter_by_date(self):

        selected_date = self.filter_date_var.get().strip()

        try:
            date.fromisoformat(selected_date)
        except ValueError:
            messagebox.showerror(
                "Invalid Date",
                "Enter a valid date in YYYY-MM-DD format."
            )
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        entries = journal_backend.get_journal_entries_for_date(
            selected_date
        )

        for entry in entries:

            self.tree.insert(
                "",
                "end",
                values=(
                    entry[0],
                    entry[1] or "",
                    entry[3] or ""
                )
            )

    #Select Entry
    def select_entry(self, event=None):

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(
            selected[0],
            "values"
        )

        entry_id = int(values[0])

        entry = next(
            (
                row for row in journal_backend.get_journal_entries()
                if row[0] == entry_id
            ),
            None
        )

        if entry is None:
            return

        self.selected_entry_id = entry[0]

        self.title_var.set(entry[1] or "")
        self.date_var.set(entry[3] or "")

        self.content_text.delete("1.0", "end")
        self.content_text.insert("1.0", entry[2] or "")

    #New Entry
    def new_entry(self):

        self.selected_entry_id = None

        for item in self.tree.selection():
            self.tree.selection_remove(item)

        self.title_var.set("")
        self.date_var.set(date.today().isoformat())

        self.content_text.delete("1.0", "end")

    #Save Entry
    def save_entry(self):

        title = self.title_var.get().strip()
        content = self.content_text.get(
            "1.0",
            "end-1c"
        ).strip()

        entry_date = self.date_var.get().strip()

        if not title:
            messagebox.showwarning(
                "Missing Title",
                "Please enter a title."
            )
            return

        if not content:
            messagebox.showwarning(
                "Missing Content",
                "Please write something in your journal."
            )
            return

        try:
            date.fromisoformat(entry_date)
        except ValueError:
            messagebox.showerror(
                "Invalid Date",
                "Use a valid date in YYYY-MM-DD format."
            )
            return

        if self.selected_entry_id is None:

            journal_backend.add_journal_entry(
                title,
                content,
                entry_date
            )

        else:

            journal_backend.update_journal_entry(
                self.selected_entry_id,
                title,
                content,
                entry_date
            )

        messagebox.showinfo(
            "Saved",
            "Your journal entry has been saved."
        )

        self.new_entry()
        self.refresh_entries()

    #Delete Entry
    def delete_entry(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select an entry to delete."
            )
            return

        values = self.tree.item(
            selected[0],
            "values"
        )

        entry_id = int(values[0])

        confirm = messagebox.askyesno(
            "Delete Entry",
            "Are you sure you want to delete this journal entry?"
        )

        if not confirm:
            return

        journal_backend.delete_journal_entry(entry_id)

        self.new_entry()
        self.refresh_entries()

        messagebox.showinfo(
            "Deleted",
            "Journal entry deleted successfully."
        )
