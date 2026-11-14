
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from features import notes as notes_backend


class NotesScreen(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.bg_color = "#F5F4EF"
        self.teal = "#075753"
        self.dark_text = "#173C3A"
        self.muted_text = "#71817D"

        self.selected_note_id = None

        self.setup_styles()
        self.create_layout()
        self.refresh_notes()

    # -----------------------------
    # Styles
    # -----------------------------

    def setup_styles(self):

        style = ttk.Style()

        style.configure(
            "Notes.TFrame",
            background=self.bg_color
        )

        style.configure(
            "Notes.Treeview",
            background="white",
            foreground=self.dark_text,
            fieldbackground="white",
            rowheight=38,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Notes.Treeview.Heading",
            background="#E9EFEC",
            foreground=self.dark_text,
            font=("Segoe UI", 10, "bold"),
            relief="flat"
        )

        style.map(
            "Notes.Treeview",
            background=[("selected", "#D5E9E4")],
            foreground=[("selected", self.dark_text)]
        )

    # -----------------------------
    # Main Layout
    # -----------------------------

    def create_layout(self):

        self.configure(style="Notes.TFrame")

        # Header
        header = tk.Frame(self, bg=self.bg_color)
        header.pack(fill="x", padx=30, pady=(25, 15))

        tk.Label(
            header,
            text="Notes",
            bg=self.bg_color,
            fg=self.dark_text,
            font=("Segoe UI", 24, "bold")
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Capture your thoughts and keep everything organized.",
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

        self.create_notes_list(content)
        self.create_editor(content)

    # -----------------------------
    # Notes List
    # -----------------------------

    def create_notes_list(self, parent):

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

        # List heading
        heading = tk.Frame(left, bg="white")
        heading.pack(fill="x", padx=15, pady=(15, 10))

        tk.Label(
            heading,
            text="Your Notes",
            bg="white",
            fg=self.dark_text,
            font=("Segoe UI", 14, "bold")
        ).pack(side="left")

        tk.Button(
            heading,
            text="+ New",
            command=self.new_note,
            bg=self.teal,
            fg="white",
            activebackground="#167E75",
            activeforeground="white",
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2"
        ).pack(side="right")

        # Search
        self.search_var = tk.StringVar()

        search = ttk.Entry(
            left,
            textvariable=self.search_var,
            font=("Segoe UI", 10)
        )

        search.pack(
            fill="x",
            padx=15,
            pady=(0, 10),
            ipady=6
        )

        self.search_var.trace_add(
            "write",
            lambda *args: self.refresh_notes()
        )

        # Category filter
        self.category_var = tk.StringVar(value="All")

        self.category_box = ttk.Combobox(
            left,
            textvariable=self.category_var,
            values=["All"],
            state="readonly",
            font=("Segoe UI", 10)
        )

        self.category_box.pack(
            fill="x",
            padx=15,
            pady=(0, 12),
            ipady=4
        )

        self.category_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.refresh_notes()
        )

        # Notes table
        table_frame = tk.Frame(left, bg="white")
        table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=("id", "title", "category", "date"),
            show="headings",
            style="Notes.Treeview"
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("category", text="Category")
        self.tree.heading("date", text="Date")

        self.tree.column("id", width=35, anchor="center")
        self.tree.column("title", width=120)
        self.tree.column("category", width=85)
        self.tree.column("date", width=90, anchor="center")

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
            self.select_note
        )

        # Delete button
        tk.Button(
            left,
            text="Delete Selected Note",
            command=self.delete_note,
            bg="#F8E7E5",
            fg="#B64C43",
            relief="flat",
            padx=10,
            pady=8,
            cursor="hand2"
        ).pack(fill="x", padx=15, pady=(0, 15))

    # -----------------------------
    # Note Editor
    # -----------------------------

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

        # Editor heading
        tk.Label(
            right,
            text="Note Editor",
            bg="white",
            fg=self.dark_text,
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", padx=20, pady=(18, 15))

        form = tk.Frame(right, bg="white")
        form.pack(fill="both", expand=True, padx=20)

        # Title
        tk.Label(
            form,
            text="Title",
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

        # Category
        tk.Label(
            form,
            text="Category",
            bg="white",
            fg=self.dark_text,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=(0, 5))

        self.editor_category_var = tk.StringVar()

        ttk.Entry(
            form,
            textvariable=self.editor_category_var,
            font=("Segoe UI", 10)
        ).pack(fill="x", ipady=6, pady=(0, 15))

        # Content
        tk.Label(
            form,
            text="Content",
            bg="white",
            fg=self.dark_text,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=(0, 5))

        text_frame = tk.Frame(form, bg="white")
        text_frame.pack(fill="both", expand=True)

        self.content_text = tk.Text(
            text_frame,
            wrap="word",
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
            text="Save Note",
            command=self.save_note,
            bg=self.teal,
            fg="white",
            activebackground="#167E75",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=9,
            cursor="hand2"
        ).pack(anchor="e", padx=20, pady=18)

    # -----------------------------
    # Refresh Notes
    # -----------------------------

    def refresh_notes(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        all_notes = notes_backend.get_notes()

        # Update category choices
        categories = sorted({
            row[3] for row in all_notes if row[3]
        })

        self.category_box["values"] = ["All"] + categories

        selected_category = self.category_var.get()

        if selected_category not in ["All"] + categories:
            self.category_var.set("All")
            selected_category = "All"

        search_text = self.search_var.get().strip().lower()

        for note in sorted(
            all_notes,
            key=lambda row: row[4] or "",
            reverse=True
        ):

            note_id = note[0]
            title = note[1] or ""
            content = note[2] or ""
            category = note[3] or ""
            created_at = note[4] or ""

            # Category filter
            if selected_category != "All":
                if category != selected_category:
                    continue

            # Search filter
            searchable = (
                title + " " + content + " " + category
            ).lower()

            if search_text not in searchable:
                continue

            self.tree.insert(
                "",
                "end",
                values=(
                    note_id,
                    title,
                    category,
                    created_at
                )
            )

    # -----------------------------
    # Select Note
    # -----------------------------

    def select_note(self, event=None):

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(
            selected[0],
            "values"
        )

        note_id = int(values[0])

        note = next(
            (
                row for row in notes_backend.get_notes()
                if row[0] == note_id
            ),
            None
        )

        if note is None:
            return

        self.selected_note_id = note[0]

        self.title_var.set(note[1] or "")
        self.editor_category_var.set(note[3] or "")

        self.content_text.delete("1.0", "end")
        self.content_text.insert("1.0", note[2] or "")

    # -----------------------------
    # New Note
    # -----------------------------

    def new_note(self):

        self.selected_note_id = None

        # Remove table selection
        for item in self.tree.selection():
            self.tree.selection_remove(item)

        self.title_var.set("")
        self.editor_category_var.set("")

        self.content_text.delete("1.0", "end")

    # -----------------------------
    # Save Note
    # -----------------------------

    def save_note(self):

        title = self.title_var.get().strip()
        category = self.editor_category_var.get().strip()
        content = self.content_text.get(
            "1.0",
            "end-1c"
        ).strip()

        # Validate title
        if not title:
            messagebox.showwarning(
                "Missing Title",
                "Please enter a title for your note."
            )
            return

        # Validate content
        if not content:
            messagebox.showwarning(
                "Missing Content",
                "Please write something in your note."
            )
            return

        if not category:
            category = "General"

        if self.selected_note_id is None:

            # Add new note
            notes_backend.add_note(
                title,
                content,
                category,
                date.today().isoformat()
            )

        else:

            # Update existing note
            notes_backend.update_note(
                self.selected_note_id,
                title,
                content,
                category
            )

        messagebox.showinfo(
            "Saved",
            "Your note has been saved successfully."
        )

        self.new_note()
        self.refresh_notes()

    # -----------------------------
    # Delete Note
    # -----------------------------

    def delete_note(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a note to delete."
            )
            return

        values = self.tree.item(
            selected[0],
            "values"
        )

        note_id = int(values[0])

        confirm = messagebox.askyesno(
            "Delete Note",
            "Are you sure you want to delete this note?"
        )

        if not confirm:
            return

        notes_backend.delete_note(note_id)

        self.new_note()
        self.refresh_notes()

        messagebox.showinfo(
            "Deleted",
            "The note has been deleted."
        )
