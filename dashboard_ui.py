import tkinter as tk
from tkinter import ttk
from datetime import date
from features.dashboard import get_dashboard_summary

class DashboardScreen(tk.Frame):
    def __init___(self,parent):
        super().__init__(parent, bg="#F5F4EF")
        self.create_header()
        self.load_dashboard()

    def create_header(self):
        header = tk.Frame(self, bg="#F5F4EF")
        header.pack(fill="x", padx=30, pady=(25, 15))

        title = tk.Label(
            header,
            text="Dashboard",
            bg="#F5F4EF",
            fg="#173C3A",
            font=("Segoe UI", 25, "bold")
        )
        title.pack(side="left")

        refresh_button = tk.Button(
            header,
            text = "↻ Refresh",
            command=self.load_dashboard,
            bg="#075753",
            fg="white",
            activebackground="#167E75",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=7,
            cursor="hand2"
        )
        refresh_button.pack(side="right")

    def create_card(self, parent, title, value, color="#075753"):
        card = tk.Frame(
            parent,
            bg="white",
            padx=15,
            pady=12,
            highlightbackground="#E1E5E1",
            higlightthickness=1
        )

        tk.Label(
            card,
            text=title,
            bg="white",
            fg="#657752",
            font=("Segoe UI", 10)
        ).pack(anchor="w")

        tk.Label(
            card,
            text=value,
            bg="white",
            fg=color,
            font=("Segoe UI", 19, "bold"),
        ).pack(anchor="w", pady=(5, 0))

        return card

    def load_dashboard(self):
        if hasattr(self, "dashboard_content"):
            self.dashboard_content.destroy()

        data = get_dashboard_summary()

        self.dashboard_content = tk.Frame(
            self,
            bg="#F5F4EF"
        )
        self.dashboard_content.pack(
            fill = "both",
            expand = True,
            padx = 30,
            pady=(0, 20)
        )

        tasks = data["tasks"]
        habits = data["habits"]
        finance = data["finance"]
        content = data["content"]

        cards_frame = tk.Frame(
            self.dashboard_content,
            bg="#F5F4EF"
        )
        cards_frame.pack(fill="x", pady=(0, 20))

        cards_frame.grid_columnconfigure(
            (0, 1, 2, 3),
            weight = 1,
            uniform="cards"
        )

        cards = [
            ("Pending Tasks", tasks["pending"], "#B7791F"),
            ("Completed Tasks", tasks["completed"], "#16845B"),
            ("Active Habits", habits["active"], "#075753"),
            ("Total Balance", f"₹{finance['balance']:,.2f}", "#075753")
        ]

        for column, (title, value, color) in enumerate(cards):
            card = self.create_card(
                cards_frame,
                title,
                str(value),
                color
            )
            card.grid(
                row=0,
                column=column,
                sticky="nsew",
                padx=4
            )

        sections = tk.Frame(
            self.dashboard_content,
            bg="#F5F4EF"
        )
        sections.pack(fill="both", expand=True)

        sections.grid_columnconfigure(
            (0, 1),
            weight=1,
            uniform="sections"
        )
        sections.grid_rowconfigure(0, weight=1)

        self.create_upcoming_tasks(
            sections,
            data["upcoming_tasks"]
        )

        self.create_recent_notes(
            sections,
            data["recent_notes"]
        )

        info = tk.Label(
            self.dashboard_content,
            text=(
                f"Habits completed today: "
                f"{habits['completed_today']} / {habits['active']}     "
                f"Notes: {content['total_notes']}     "
                f"Journal entries: {content['total_journal']}"
            ),
            bg="#F5F4EF",
            fg="#657572",
            font=("Segoe UI", 9)
        )
        info.pack(anchor="w", pady=(12, 0))

    def create_upcoming_tasks(self, parent, tasks):
        panel = tk.Frame(
            parent,
            bg="white",
            padx=15,
            pady=15,
            highlightbackground="#E1E5E1",
            highlightthickness=1
        )
        panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 6)
        )
        tk.Label(
            panel,
            text="Upcoming Tasks",
            bg="white",
            fg="#173C3A",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(0, 12))

        if not tasks:
            tk.Label(
                panel,
                text="No upcoming tasks.You are all caught up!",
                bg="white",
                fg="#657572",
                font=("Segoe UI", 10),
                wraplength=250
            ).pack(anchor="w", pady=10)
            return

        for task in tasks:
            task_name = task[1]
            due_date = task[4]

            row = tk.Frame(panel, bg="#F5F4EF", padx=10, pady=8)
            row.pack(fill="x", pady = 3)

            tk.Label(
                row,
                text=task_name,
                bg="#F5F4EF",
                fg="#173C3A",
                font=("Segoe UI", 10, "bold"),
                wraplength=220
            ).pack(anchor="w")

            tk.Label(
                row,
                text=f"Due: {due_date}",
                bg="#F5F4EF",
                fg="#657572",
                font=("Segoe UI", 9)
            ).pack(anchor="w")

    def create_recent_notes(self, parent, notes):
        panel = tk.Frame(
            parent,
            bg="white",
            padx=15,
            pady=15,
            highlightbackground="#E1E5E1",
            higlightthickness=1
        )
        panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(6, 0)
        )
        tk.Label(
            panel,
            text="Recent Notes",
            bg="white",
            fg="#173C3A",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(0, 12))

        if not notes:
            tk.Label(
                panel,
                text="No notes created yet.",
                bg="white",
                fg="#657572",
                font=("Segoe UI", 10)
            ).pack(anchor="w", pady=10)
            return

        for note in notes:
            note_title = note[1]
            note_category = note[3]

            row = tk.Frame(panel, bg="#F5F4EF", padx=10, pady=8)
            row.pack(fill="x", pady=3)

            tk.Label(
                row,
                text=note_title,
                bg="#F5F4EF",
                fg="#173C3A",
                font=("Segoe UI", 10, "bold"),
                wraplength=220
            ).pack(anchor="w")

            tk.Label(
                row,
                text=f"Category: {note_category}",
                bg="#F5F4EF",
                fg="#657572",
                font=("Segoe UI", 9)
            ).pack(anchor="w")