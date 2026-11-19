
import tkinter as tk
from tkinter import ttk
from features.search import global_search


class SearchScreen(tk.Frame):

    #Initializez the screeen
    def __init__(self, parent):
        super().__init__(parent, bg="#F5F4EF")

        self.create_header()
        self.create_search_bar()
        self.create_results_table()

    #Creates the page's headingg
    def create_header(self):
        tk.Label(
            self,
            text="Global Search",
            bg="#F5F4EF",
            fg="#173C3A",
            font=("Segoe UI", 25, "bold")
        ).pack(anchor="w", padx=30, pady=(25, 15))

    #Creates the search input and button
    def create_search_bar(self):
        search_frame = tk.Frame(self, bg="#F5F4EF")
        search_frame.pack(fill="x", padx=30, pady=10)

        self.search_entry = tk.Entry(
            search_frame,
            font=("Segoe UI", 12),
            relief="flat",
            bd=0
        )
        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=10,
            padx=(0, 10)
        )

        self.search_entry.bind("<Return>", self.run_search)

        tk.Button(
            search_frame,
            text="Search",
            command=self.run_search,
            bg="#075753",
            fg="white",
            relief="flat",
            padx=20,
            pady=9,
            cursor="hand2"
        ).pack(side="left")

        tk.Button(
            search_frame,
            text="Clear",
            command=self.clear_search,
            bg="#DDE7E3",
            fg="#173C3A",
            relief="flat",
            padx=15,
            pady=9,
            cursor="hand2"
        ).pack(side="left", padx=(8, 0))

    #Creates the tableee
    def create_results_table(self):
        table_frame = tk.Frame(self, bg="white")
        table_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=15
        )

        columns = ("type", "name", "category", "details")

        self.results_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.results_table.heading("type", text="Type")
        self.results_table.heading("name", text="Name")
        self.results_table.heading("category", text="Category")
        self.results_table.heading("details", text="Details")

        self.results_table.column("type", width=100)
        self.results_table.column("name", width=180)
        self.results_table.column("category", width=120)
        self.results_table.column("details", width=250)

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.results_table.yview
        )

        self.results_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.results_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.status_label = tk.Label(
            self,
            text="Enter something to search across DeskOS.",
            bg="#F5F4EF",
            fg="#657572",
            font=("Segoe UI", 10)
        )
        self.status_label.pack(anchor="w", padx=30, pady=(0, 15))

    #Run the global search and display result
    def run_search(self, event=None):
        query = self.search_entry.get().strip()

        if not query:
            self.status_label.config(text="Please enter something to search.")
            return

        for item in self.results_table.get_children():
            self.results_table.delete(item)

        results = global_search(query)

        for result_type, row in results:

            if result_type == "task":
                name = row[1]
                category = row[5]
                details = f"Priority: {row[3]} | Due: {row[4]}"

            elif result_type == "habit":
                name = row[1]
                category = row[3]
                details = "Active" if row[5] else "Inactive"

            elif result_type == "finance":
                name = row[2]
                category = row[4]
                details = f"{row[3].title()} | ₹{row[1]:,.2f} | {row[5]}"

            elif result_type == "note":
                name = row[1]
                category = row[3]
                details = f"Created: {row[4]}"

            elif result_type == "journal":
                name = row[1]
                category = "Journal"
                details = f"Date: {row[3]}"

            self.results_table.insert(
                "",
                "end",
                values=(
                    result_type.title(),
                    name,
                    category,
                    details
                )
            )

        self.status_label.config(
            text=f"Found {len(results)} result(s) for '{query}'."
        )

    #Clear the search
    def clear_search(self):
        self.search_entry.delete(0, tk.END)

        for item in self.results_table.get_children():
            self.results_table.delete(item)

        self.status_label.config(
            text="Enter something to search across DeskOS."
        )
