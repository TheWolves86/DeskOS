
import tkinter as tk
from tkinter import ttk
from features.dashboard import get_dashboard_summary


BG = "#F4F6F3"
WHITE = "#FFFFFF"
TEXT = "#183B37"
MUTED = "#82918B"
ACCENT = "#268477"
BORDER = "#E3EAE5"


class DashboardScreen(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=BG)

        self.create_header()
        self.load_dashboard()

    #Page's heading
    def create_header(self):
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=30, pady=(25, 22))

        heading = tk.Frame(header, bg=BG)
        heading.pack(side="left")

        tk.Label(
            heading,
            text="Good to see you.",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 24, "bold")
        ).pack(anchor="w")

        tk.Label(
            heading,
            text="Here's what's happening in your workspace.",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(4, 0))

        tk.Button(
            header,
            text="↻  Refresh",
            command=self.load_dashboard,
            bg=ACCENT,
            fg=WHITE,
            activebackground="#1D6E63",
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            padx=17,
            pady=9,
            cursor="hand2"
        ).pack(side="right", anchor="center")

    #Reusable summary card
    def create_card(self, parent, title, value, subtitle, accent):
        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        tk.Frame(
            card,
            bg=accent,
            height=4
        ).pack(fill="x")

        body = tk.Frame(card, bg=WHITE, padx=17, pady=15)
        body.pack(fill="both", expand=True)

        tk.Label(
            body,
            text=title.upper(),
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w")

        tk.Label(
            body,
            text=value,
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w", pady=(9, 3))

        tk.Label(
            body,
            text=subtitle,
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w")

        return card

    #section panel
    def create_panel(self, parent, title, subtitle):
        panel = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        heading = tk.Frame(panel, bg=WHITE)
        heading.pack(fill="x", padx=19, pady=(17, 14))

        tk.Label(
            heading,
            text=title,
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w")

        tk.Label(
            heading,
            text=subtitle,
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(3, 0))

        tk.Frame(panel, bg=BORDER, height=1).pack(fill="x")

        return panel

    #Load dashboard information from the existinnnggg backend
    def load_dashboard(self):
        if hasattr(self, "dashboard_content"):
            self.dashboard_content.destroy()

        data = get_dashboard_summary()

        tasks = data["tasks"]
        habits = data["habits"]
        finance = data["finance"]
        content = data["content"]

        self.dashboard_content = tk.Frame(self, bg=BG)
        self.dashboard_content.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )

        #Summary cards ig
        cards_frame = tk.Frame(self.dashboard_content, bg=BG)
        cards_frame.pack(fill="x", pady=(0, 20))

        for column in range(4):
            cards_frame.grid_columnconfigure(
                column,
                weight=1,
                uniform="dashboard_cards"
            )

        cards = [
            (
                "Pending Tasks",
                str(tasks["pending"]),
                "Tasks still to complete",
                "#D49A45"
            ),
            (
                "Completed Tasks",
                str(tasks["completed"]),
                "Tasks finished",
                "#3B9B72"
            ),
            (
                "Active Habits",
                str(habits["active"]),
                "Habits you're tracking",
                "#268477"
            ),
            (
                "Total Balance",
                f"₹{finance['balance']:,.2f}",
                "Current financial balance",
                "#6488B5"
            )
        ]

        for column, card_data in enumerate(cards):
            card = self.create_card(cards_frame, *card_data)
            card.grid(
                row=0,
                column=column,
                sticky="nsew",
                padx=(0 if column == 0 else 6, 0 if column == 3 else 6)
            )

        #Upcoming tasks and recent notes
        sections = tk.Frame(self.dashboard_content, bg=BG)
        sections.pack(fill="both", expand=True)

        sections.grid_columnconfigure(0, weight=1, uniform="panels")
        sections.grid_columnconfigure(1, weight=1, uniform="panels")
        sections.grid_rowconfigure(0, weight=1)

        tasks_panel = self.create_panel(
            sections,
            "Upcoming Tasks",
            "Keep an eye on what's coming next"
        )
        tasks_panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )

        notes_panel = self.create_panel(
            sections,
            "Recent Notes",
            "Your recently created notes"
        )
        notes_panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8, 0)
        )

        self.display_tasks(tasks_panel, data["upcoming_tasks"])
        self.display_notes(notes_panel, data["recent_notes"])

        #Small footer
        footer = tk.Frame(self.dashboard_content, bg=BG)
        footer.pack(fill="x", pady=(17, 0))

        stats = [
            ("HABITS TODAY", f"{habits['completed_today']} / {habits['active']}"),
            ("TOTAL NOTES", str(content["total_notes"])),
            ("JOURNAL ENTRIES", str(content["total_journal"]))
        ]

        for label, value in stats:
            item = tk.Frame(footer, bg=BG)
            item.pack(side="left", padx=(0, 35))

            tk.Label(
                item,
                text=label,
                bg=BG,
                fg=MUTED,
                font=("Segoe UI", 8, "bold")
            ).pack(anchor="w")

            tk.Label(
                item,
                text=value,
                bg=BG,
                fg=TEXT,
                font=("Segoe UI", 11, "bold")
            ).pack(anchor="w", pady=(3, 0))

    #Displays upcoming tasks
    def display_tasks(self, parent, tasks):
        body = tk.Frame(parent, bg=WHITE, padx=15, pady=12)
        body.pack(fill="both", expand=True)

        if not tasks:
            tk.Label(
                body,
                text="You're all caught up!",
                bg=WHITE,
                fg=TEXT,
                font=("Segoe UI", 11, "bold")
            ).pack(anchor="w", pady=(10, 3))

            tk.Label(
                body,
                text="No upcoming tasks to display.",
                bg=WHITE,
                fg=MUTED,
                font=("Segoe UI", 9)
            ).pack(anchor="w")

            return

        for task in tasks:
            row = tk.Frame(
                body,
                bg="#F7F9F7",
                padx=12,
                pady=11
            )
            row.pack(fill="x", pady=4)

            tk.Frame(
                row,
                bg=ACCENT,
                width=3
            ).pack(side="left", fill="y", padx=(0, 10))

            details = tk.Frame(row, bg="#F7F9F7")
            details.pack(side="left", fill="x", expand=True)

            tk.Label(
                details,
                text=str(task[1]),
                bg="#F7F9F7",
                fg=TEXT,
                font=("Segoe UI", 10, "bold"),
                anchor="w",
                wraplength=300
            ).pack(anchor="w")

            tk.Label(
                details,
                text=f"Due date: {task[4]}",
                bg="#F7F9F7",
                fg=MUTED,
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(3, 0))

    #Displays the recently created notes
    def display_notes(self, parent, notes):
        body = tk.Frame(parent, bg=WHITE, padx=15, pady=12)
        body.pack(fill="both", expand=True)

        if not notes:
            tk.Label(
                body,
                text="No notes yet.",
                bg=WHITE,
                fg=TEXT,
                font=("Segoe UI", 11, "bold")
            ).pack(anchor="w", pady=(10, 3))

            tk.Label(
                body,
                text="Your recent notes will appear here.",
                bg=WHITE,
                fg=MUTED,
                font=("Segoe UI", 9)
            ).pack(anchor="w")

            return

        for note in notes:
            row = tk.Frame(
                body,
                bg="#F7F9F7",
                padx=12,
                pady=11
            )
            row.pack(fill="x", pady=4)

            tk.Frame(
                row,
                bg="#6488B5",
                width=3
            ).pack(side="left", fill="y", padx=(0, 10))

            details = tk.Frame(row, bg="#F7F9F7")
            details.pack(side="left", fill="x", expand=True)

            tk.Label(
                details,
                text=str(note[1]),
                bg="#F7F9F7",
                fg=TEXT,
                font=("Segoe UI", 10, "bold"),
                anchor="w",
                wraplength=300
            ).pack(anchor="w")

            tk.Label(
                details,
                text=f"Category: {note[3]}",
                bg="#F7F9F7",
                fg=MUTED,
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(3, 0))
