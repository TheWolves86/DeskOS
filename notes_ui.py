
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from features import notes as backend


BG = "#F4F6F3"
WHITE = "#FFFFFF"
TEAL = "#268477"
DARK = "#123B38"
TEXT = "#243532"
MUTED = "#7B8985"
BORDER = "#E3EAE6"


class NotesScreen(ttk.Frame):
    #Initializez the app
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(style="App.TFrame")

        self.selected_id = None
        self.notes = []

        self.setup_styles()
        self.build_ui()
        self.refresh_notes()

    #Setups the stylee
    def setup_styles(self):
        style = ttk.Style()

        style.configure(
            "Notes.Treeview",
            background=WHITE,
            foreground=TEXT,
            fieldbackground=WHITE,
            rowheight=38,
            font=("Segoe UI", 10),
            borderwidth=0
        )

        style.configure(
            "Notes.Treeview.Heading",
            background="#EDF2EF",
            foreground=DARK,
            font=("Segoe UI", 9, "bold"),
            relief="flat"
        )

        style.map(
            "Notes.Treeview",
            background=[("selected", "#DCEDE8")],
            foreground=[("selected", DARK)]
        )

    #it says that it build the ui
    def build_ui(self):
        self.configure(padding=24)

        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0, 20))

        ttk.Label(
            header,
            text="Notes",
            font=("Segoe UI", 23, "bold"),
            foreground=DARK
        ).pack(side="left")

        ttk.Label(
            header,
            text="Capture your thoughts and ideas.",
            font=("Segoe UI", 10),
            foreground=MUTED
        ).pack(side="left", padx=16, pady=(9, 0))

        self.new_button = tk.Button(
            header,
            text="+  New Note",
            command=self.new_note,
            bg=TEAL,
            fg="white",
            activebackground=DARK,
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=18,
            pady=9,
            cursor="hand2"
        )
        self.new_button.pack(side="right")

        body = ttk.Frame(self)
        body.pack(fill="both", expand=True)

        #Notes list
        left = tk.Frame(
            body,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))

        ttk.Label(
            left,
            text="Your Notes",
            font=("Segoe UI", 13, "bold"),
            foreground=DARK,
            background=WHITE
        ).pack(anchor="w", padx=16, pady=(16, 10))

        self.search_var = tk.StringVar()
        search = ttk.Entry(left, textvariable=self.search_var)
        search.pack(fill="x", padx=16, pady=(0, 10))
        search.insert(0, "")

        self.search_var.trace_add(
            "write",
            lambda *_: self.refresh_notes()
        )

        self.category_filter = tk.StringVar(value="All")

        self.category_box = ttk.Combobox(
            left,
            textvariable=self.category_filter,
            state="readonly",
            values=["All"],
        )
        self.category_box.pack(fill="x", padx=16, pady=(0, 12))
        self.category_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.refresh_notes()
        )

        columns = ("title", "category", "date")

        self.tree = ttk.Treeview(
            left,
            columns=columns,
            show="headings",
            style="Notes.Treeview"
        )

        self.tree.heading("title", text="TITLE")
        self.tree.heading("category", text="CATEGORY")
        self.tree.heading("date", text="DATE")

        self.tree.column("title", width=150, anchor="w")
        self.tree.column("category", width=90, anchor="w")
        self.tree.column("date", width=95, anchor="w")

        self.tree.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 12)
        )

        self.tree.bind("<<TreeviewSelect>>", self.select_note)

        #Editor
        right = tk.Frame(
            body,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        right.pack(side="right", fill="both", expand=True)

        editor_header = tk.Frame(right, bg=WHITE)
        editor_header.pack(fill="x", padx=20, pady=(18, 12))

        ttk.Label(
            editor_header,
            text="Note Editor",
            font=("Segoe UI", 13, "bold"),
            foreground=DARK,
            background=WHITE
        ).pack(side="left")

        self.status_label = ttk.Label(
            editor_header,
            text="New note",
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
            text="CATEGORY",
            background=WHITE,
            foreground=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", padx=20)

        self.category_var = tk.StringVar(value="General")

        ttk.Entry(
            right,
            textvariable=self.category_var
        ).pack(fill="x", padx=20, pady=(5, 14))

        ttk.Label(
            right,
            text="CONTENT",
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

        #Editor's actions
        actions = tk.Frame(right, bg=WHITE)
        actions.pack(fill="x", padx=20, pady=(0, 18))

        tk.Button(
            actions,
            text="Save Note",
            command=self.save_note,
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
            command=self.delete_note,
            bg="#FCEBE9",
            fg="#B64D45",
            activebackground="#F5D8D5",
            relief="flat",
            font=("Segoe UI", 10),
            padx=16,
            pady=9,
            cursor="hand2"
        ).pack(side="right")

    #refreshes the notes
    def refresh_notes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.notes = backend.get_notes()

        categories = sorted({
            str(note[3]) for note in self.notes
            if note[3]
        })

        values = ["All"] + categories
        self.category_box["values"] = values

        if self.category_filter.get() not in values:
            self.category_filter.set("All")

        query = self.search_var.get().lower().strip()
        selected_category = self.category_filter.get()

        filtered = []

        for note in self.notes:
            note_id, title, content, category, created_at = note

            if query and query not in (
                str(title) + " " +
                str(content) + " " +
                str(category)
            ).lower():
                continue

            if selected_category != "All":
                if category != selected_category:
                    continue

            filtered.append(note)

        filtered.sort(
            key=lambda note: str(note[4]),
            reverse=True
        )

        for note in filtered:
            self.tree.insert(
                "",
                "end",
                iid=str(note[0]),
                values=(
                    note[1],
                    note[3],
                    note[4]
                )
            )

    #form for a new note
    def new_note(self):
        self.selected_id = None

        self.title_var.set("")
        self.category_var.set("General")
        self.content_text.delete("1.0", "end")

        self.status_label.config(text="New note")

        for item in self.tree.selection():
            self.tree.selection_remove(item)

    #selects a note so we can perform a specific function
    def select_note(self, event=None):
        selection = self.tree.selection()

        if not selection:
            return

        note_id = int(selection[0])

        for note in self.notes:
            if note[0] == note_id:
                self.selected_id = note_id

                self.title_var.set(note[1] or "")
                self.category_var.set(note[3] or "General")

                self.content_text.delete("1.0", "end")
                self.content_text.insert("1.0", note[2] or "")

                self.status_label.config(text="Editing note")
                break

    #Saves the note
    def save_note(self):
        title = self.title_var.get().strip()
        content = self.content_text.get("1.0", "end-1c").strip()
        category = self.category_var.get().strip() or "General"

        if not title:
            messagebox.showwarning(
                "Missing title",
                "Please enter a title for your note."
            )
            return

        if not content:
            messagebox.showwarning(
                "Empty note",
                "Please write something before saving."
            )
            return

        try:
            if self.selected_id is None:
                backend.add_note(
                    title,
                    content,
                    category,
                    date.today().isoformat()
                )
            else:
                backend.update_note(
                    self.selected_id,
                    title,
                    content,
                    category
                )

            self.refresh_notes()
            self.new_note()

            messagebox.showinfo(
                "Saved",
                "Your note has been saved."
            )

        except Exception as error:
            messagebox.showerror("Error", str(error))

    #deletes a note
    def delete_note(self):
        if self.selected_id is None:
            messagebox.showwarning(
                "No note selected",
                "Select a note to delete."
            )
            return

        confirm = messagebox.askyesno(
            "Delete note",
            "Are you sure you want to delete this note?"
        )

        if not confirm:
            return

        try:
            backend.delete_note(self.selected_id)
            self.new_note()
            self.refresh_notes()

        except Exception as error:
            messagebox.showerror("Error", str(error))
