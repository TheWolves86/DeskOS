import tkinter as tk
from tkinter import ttk, messagebox
from features import search as backend


WHITE = "#FFFFFF"
TEAL = "#268477"
DARK = "#123B38"
TEXT = "#243532"
MUTED = "#7B8985"
BORDER = "#E3EAE6"


class SearchScreen(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=24)

        self.results = []

        self.setup_styles()
        self.build_ui()

    def setup_styles(self):
        style = ttk.Style()

        style.configure(
            "Search.Treeview",
            background=WHITE,
            foreground=TEXT,
            fieldbackground=WHITE,
            rowheight=42,
            font=("Segoe UI", 10),
            borderwidth=0
        )

        style.configure(
            "Search.Treeview.Heading",
            background="#EDF2EF",
            foreground=DARK,
            font=("Segoe UI", 9, "bold"),
            relief="flat"
        )

        style.map(
            "Search.Treeview",
            background=[("selected", "#DCEDE8")],
            foreground=[("selected", DARK)]
        )

    def build_ui(self):
        ttk.Label(
            self,
            text="Global Search",
            font=("Segoe UI", 23, "bold"),
            foreground=DARK
        ).pack(anchor="w")

        ttk.Label(
            self,
            text="Find anything across your DeskOS workspace.",
            font=("Segoe UI", 10),
            foreground=MUTED
        ).pack(anchor="w", pady=(4, 20))

        search_card = tk.Frame(
            self,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        search_card.pack(fill="x", pady=(0, 18))

        search_row = tk.Frame(search_card, bg=WHITE)
        search_row.pack(fill="x", padx=18, pady=18)

        self.query_var = tk.StringVar()

        self.search_entry = ttk.Entry(
            search_row,
            textvariable=self.query_var,
            font=("Segoe UI", 12)
        )
        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=7
        )
        self.search_entry.bind(
            "<Return>",
            lambda event: self.search()
        )

        tk.Button(
            search_row,
            text="Search",
            command=self.search,
            bg=TEAL,
            fg="white",
            activebackground=DARK,
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=22,
            pady=10,
            cursor="hand2"
        ).pack(side="left", padx=(12, 0))

        self.filter_var = tk.StringVar(value="All")

        filter_row = tk.Frame(search_card, bg=WHITE)
        filter_row.pack(fill="x", padx=18, pady=(0, 14))

        ttk.Label(
            filter_row,
            text="Filter:",
            background=WHITE,
            foreground=MUTED
        ).pack(side="left", padx=(0, 10))

        self.filter_box = ttk.Combobox(
            filter_row,
            textvariable=self.filter_var,
            values=[
                "All",
                "Tasks",
                "Habits",
                "Finance",
                "Notes",
                "Journal"
            ],
            state="readonly",
            width=15
        )
        self.filter_box.pack(side="left")
        self.filter_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.display_results()
        )

        results_header = tk.Frame(self, bg="#F4F6F3")
        results_header.pack(fill="x", pady=(0, 10))

        ttk.Label(
            results_header,
            text="Search Results",
            font=("Segoe UI", 13, "bold"),
            foreground=DARK
        ).pack(side="left")

        self.count_label = ttk.Label(
            results_header,
            text="0 results",
            foreground=MUTED
        )
        self.count_label.pack(side="right")

        table_frame = tk.Frame(
            self,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        table_frame.pack(fill="both", expand=True)

        columns = ("type", "title", "details")

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Search.Treeview"
        )

        self.tree.heading("type", text="TYPE")
        self.tree.heading("title", text="TITLE")
        self.tree.heading("details", text="DETAILS")

        self.tree.column("type", width=110)
        self.tree.column("title", width=220)
        self.tree.column("details", width=350)

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        scrollbar.pack(side="right", fill="y", pady=8)

        self.empty_label = ttk.Label(
            self,
            text="Enter something above to search your workspace.",
            foreground=MUTED,
            font=("Segoe UI", 10)
        )
        self.empty_label.pack(pady=12)

    def search(self):
        query = self.query_var.get().strip()

        if not query:
            messagebox.showwarning(
                "Empty search",
                "Enter something to search for."
            )
            return

        try:
            self.results = backend.global_search(query)
            self.display_results()

        except Exception as error:
            messagebox.showerror("Search error", str(error))

    def display_results(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        selected_filter = self.filter_var.get()

        names = {
            "task": "Tasks",
            "habit": "Habits",
            "finance": "Finance",
            "note": "Notes",
            "journal": "Journal"
        }

        count = 0

        for result_type, row in self.results:
            display_type = names.get(result_type, result_type.title())

            if selected_filter != "All" and display_type != selected_filter:
                continue

            title = ""
            details = ""

            if result_type == "task":
                title = row[1]
                details = f"{row[5]} • {row[3]} priority"

            elif result_type == "habit":
                title = row[1]
                details = f"Category: {row[3]}"

            elif result_type == "finance":
                title = row[2]
                details = f"{row[3]} • {row[4]}"

            elif result_type == "note":
                title = row[1]
                details = f"Category: {row[3]}"

            elif result_type == "journal":
                title = row[1]
                details = f"Date: {row[3]}"

            self.tree.insert(
                "",
                "end",
                values=(display_type, title, details)
            )

            count += 1

        self.count_label.config(
            text=f"{count} result{'s' if count != 1 else ''}"
        )

        if count == 0:
            self.empty_label.config(text="No matching results found.")
        else:
            self.empty_label.config(text="")
