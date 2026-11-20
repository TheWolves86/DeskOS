import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from features import journal as backend

BG = "#F4F6F3"
WHITE = "#FFFFFF"
TEAL = "#268477"
DARK = "#123B38"
TEXT = "#243532"
MUTED = "#7B8985"
BORDER = "#E3EAE6"


class JournalScreen(ttk.Frame):
    #initializez the main screen
    def __init__(self, parent):
        super().__init__(parent, padding=24)

        self.selected_id = None
        self.entries = []

        self.setup_styles()
        self.build_ui()
        self.refresh_entries()

    #setups the styleee
    def setup_styles(self):
        style = ttk.Style()

        style.configure(
            "Journal.Treeview",
            background=WHITE,
            foreground=TEXT,
            fieldbackground=WHITE,
            rowheight=40,
            font=("Segoe UI", 10),
            borderwidth=0
        )

        style.configure(
            "Journal.Treeview.Heading",
            background="#EDF2EF",
            foreground=DARK,
            font=("Segoe UI", 9, "bold"),
            relief="flat"
        )

        style.map(
            "Journal.Treeview",
            background=[("selected", "#DCEDE8")],
            foreground=[("selected", DARK)]
        )

    #idk why i am commeting but yeah it build the ui
    def build_ui(self):
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0, 20))

        ttk.Label(
            header,
            text="Journal",
            font=("Segoe UI", 23, "bold"),
            foreground=DARK
        ).pack(side="left")

        ttk.Label(
            header,
            text="A private space for your daily thoughts.",
            font=("Segoe UI", 10),
            foreground=MUTED
        ).pack(side="left", padx=16, pady=(9, 0))

        tk.Button(
            header,
            text="+  New Entry",
            command=self.new_entry,
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

        body = ttk.Frame(self)
        body.pack(fill="both", expand=True)

        #Entry list
        left = tk.Frame(
            body,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))

        ttk.Label(
            left,
            text="Your Entries",
            font=("Segoe UI", 13, "bold"),
            foreground=DARK,
            background=WHITE
        ).pack(anchor="w", padx=16, pady=(16, 12))

        filter_frame = tk.Frame(left, bg=WHITE)
        filter_frame.pack(fill="x", padx=16, pady=(0, 12))

        self.date_filter = tk.StringVar()

        ttk.Entry(
            filter_frame,
            textvariable=self.date_filter
        ).pack(side="left", fill="x", expand=True)

        tk.Button(
            filter_frame,
            text="Filter",
            command=self.refresh_entries,
            bg="#E7F1ED",
            fg=DARK,
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2"
        ).pack(side="left", padx=(8, 0))

        tk.Button(
            left,
            text="Show All Entries",
            command=self.clear_filter,
            bg=WHITE,
            fg=TEAL,
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2"
        ).pack(anchor="w", padx=16, pady=(0, 10))

        columns = ("title", "date")

        self.tree = ttk.Treeview(
            left,
            columns=columns,
            show="headings",
            style="Journal.Treeview"
        )

        self.tree.heading("title", text="ENTRY")
        self.tree.heading("date", text="DATE")

        self.tree.column("title", width=190, anchor="w")
        self.tree.column("date", width=110, anchor="w")

        self.tree.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 12)
        )

        self.tree.bind("<<TreeviewSelect>>", self.select_entry)

        #Journal editor
        right = tk.Frame(
            body,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        right.pack(side="right", fill="both", expand=True)

        editor_header = tk.Frame(right, bg=WHITE)
        editor_header.pack(fill="x", padx=20, pady=(18, 16))

        ttk.Label(
            editor_header,
            text="Journal Editor",
            font=("Segoe UI", 13, "bold"),
            foreground=DARK,
            background=WHITE
        ).pack(side="left")

        self.status_label = ttk.Label(
            editor_header,
            text="New entry",
            foreground=MUTED,
            background=WHITE,
            font=("Segoe UI", 9)
        )
        self.status_label.pack(side="right")

        ttk.Label(
            right,
            text="TITLE",
            background=WHITE,
            foreground=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", padx=20)

        self.title_var = tk.StringVar()

        ttk.Entry(
            right,
            textvariable=self.title_var,
            font=("Segoe UI", 12)
        ).pack(fill="x", padx=20, pady=(5, 14))

        ttk.Label(
            right,
            text="DATE (YYYY-MM-DD)",
            background=WHITE,
            foreground=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", padx=20)

        self.date_var = tk.StringVar(value=date.today().isoformat())

        ttk.Entry(
            right,
            textvariable=self.date_var
        ).pack(fill="x", padx=20, pady=(5, 14))

        ttk.Label(
            right,
            text="YOUR THOUGHTS",
            background=WHITE,
            foreground=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", padx=20)

        content_frame = tk.Frame(right, bg=WHITE)
        content_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(5, 12)
        )

        self.content_text = tk.Text(
            content_frame,
            wrap="word",
            font=("Segoe UI", 10),
            bg="#FAFCFA",
            fg=TEXT,
            insertbackground=TEAL,
            relief="flat",
            padx=12,
            pady=12,
            undo=True
        )
        self.content_text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            content_frame,
            orient="vertical",
            command=self.content_text.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.content_text.configure(
            yscrollcommand=scrollbar.set
        )

        #Actions
        actions = tk.Frame(right, bg=WHITE)
        actions.pack(fill="x", padx=20, pady=(0, 18))

        tk.Button(
            actions,
            text="Save Entry",
            command=self.save_entry,
            bg=TEAL,
            fg="white",
            activebackground=DARK,
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=9,
            cursor="hand2"
        ).pack(side="left")

        tk.Button(
            actions,
            text="Delete",
            command=self.delete_entry,
            bg="#FCEBE9",
            fg="#B64D45",
            activebackground="#F5D8D5",
            relief="flat",
            font=("Segoe UI", 10),
            padx=16,
            pady=9,
            cursor="hand2"
        ).pack(side="right")

    #Refreshes the entries
    def refresh_entries(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.entries = backend.get_journal_entries()

        filter_date = self.date_filter.get().strip()

        filtered = self.entries

        if filter_date:
            filtered = [
                entry for entry in self.entries
                if str(entry[3]) == filter_date
            ]

        filtered = sorted(
            filtered,
            key=lambda entry: str(entry[3]),
            reverse=True
        )

        for entry in filtered:
            self.tree.insert(
                "",
                "end",
                iid=str(entry[0]),
                values=(entry[1], entry[3])
            )

    #Clears the filer tab
    def clear_filter(self):
        self.date_filter.set("")
        self.refresh_entries()

    #opens a new form for entry
    def new_entry(self):
        self.selected_id = None

        self.title_var.set("")
        self.date_var.set(date.today().isoformat())
        self.content_text.delete("1.0", "end")

        self.status_label.config(text="New entry")

        for item in self.tree.selection():
            self.tree.selection_remove(item)

    #selects a entry so we can perform crud
    def select_entry(self, event=None):
        selection = self.tree.selection()

        if not selection:
            return

        entry_id = int(selection[0])

        for entry in self.entries:
            if entry[0] == entry_id:
                self.selected_id = entry_id

                self.title_var.set(entry[1] or "")
                self.content_text.delete("1.0", "end")
                self.content_text.insert("1.0", entry[2] or "")
                self.date_var.set(entry[3] or "")

                self.status_label.config(text="Editing entry")
                break

    #Saves the entry
    def save_entry(self):
        title = self.title_var.get().strip()
        content = self.content_text.get("1.0", "end-1c").strip()
        entry_date = self.date_var.get().strip()

        if not title or not content or not entry_date:
            messagebox.showwarning(
                "Missing information",
                "Please fill in the title, date and content."
            )
            return

        try:
            date.fromisoformat(entry_date)

            if self.selected_id is None:
                backend.add_journal_entry(
                    title,
                    content,
                    entry_date
                )
            else:
                backend.update_journal_entry(
                    self.selected_id,
                    title,
                    content,
                    entry_date
                )

            self.refresh_entries()
            self.new_entry()

            messagebox.showinfo(
                "Saved",
                "Your journal entry has been saved."
            )

        except ValueError:
            messagebox.showerror(
                "Invalid date",
                "Use YYYY-MM-DD format for the date."
            )

        except Exception as error:
            messagebox.showerror("Error", str(error))

    #Deletes a entry
    def delete_entry(self):
        if self.selected_id is None:
            messagebox.showwarning(
                "No entry selected",
                "Select an entry to delete."
            )
            return

        confirm = messagebox.askyesno(
            "Delete entry",
            "Are you sure you want to delete this journal entry?"
        )

        if not confirm:
            return

        try:
            backend.delete_journal_entry(self.selected_id)
            self.new_entry()
            self.refresh_entries()

        except Exception as error:
            messagebox.showerror("Error", str(error))
