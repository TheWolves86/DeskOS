import tkinter as tk
from tkinter import ttk
from datetime import date

from tasks_ui import TasksScreen
from habits_ui import HabitsScreen
from finance_ui import FinanceScreen
from notes_ui import NotesScreen
from journal_ui import JournalScreen
from dashboard_ui import DashboardScreen
from global_search_ui import SearchScreen


BG = "#F4F6F3"
SIDEBAR = "#123B38"
SIDEBAR_HOVER = "#1D514B"
ACCENT = "#268477"
WHITE = "#FFFFFF"
TEXT = "#183B37"
MUTED = "#82918B"
BORDER = "#E3EAE5"


class DeskOS:

    def __init__(self, root):
        self.root = root
        self.current_page = None
        self.nav_buttons = {}

        self.setup_window()
        self.setup_styles()
        self.create_layout()
        self.show_page("Dashboard")

    #Configure the main windowwwww
    def setup_window(self):
        self.root.title("DeskOS")
        self.root.geometry("1150x720")
        self.root.minsize(900, 600)
        self.root.configure(bg=BG)

        self.root.option_add("*Font", ("Segoe UI", 10))

    #Set styles for tkinter widgetss
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=WHITE,
            foreground=TEXT,
            fieldbackground=WHITE,
            rowheight=36,
            borderwidth=0,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#EAF0EC",
            foreground=TEXT,
            font=("Segoe UI", 10, "bold"),
            relief="flat"
        )

        style.map(
            "Treeview",
            background=[("selected", "#D5E9E2")],
            foreground=[("selected", TEXT)]
        )

        style.configure(
            "TEntry",
            padding=8
        )

        style.configure(
            "TCombobox",
            padding=7
        )

    # Build the sidebar and main content area
    def create_layout(self):
        self.sidebar = tk.Frame(
            self.root,
            bg=SIDEBAR,
            width=225
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.main_area = tk.Frame(
            self.root,
            bg=BG
        )
        self.main_area.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.create_sidebar()
        self.create_topbar()

        self.page_container = tk.Frame(
            self.main_area,
            bg=BG
        )
        self.page_container.pack(
            fill="both",
            expand=True
        )

    # Create the application branding and navigation
    def create_sidebar(self):
        brand = tk.Frame(self.sidebar, bg=SIDEBAR)
        brand.pack(fill="x", padx=22, pady=(28, 35))

        tk.Label(
            brand,
            text="DeskOS",
            bg=SIDEBAR,
            fg=WHITE,
            font=("Segoe UI", 23, "bold")
        ).pack(anchor="w")

        tk.Label(
            brand,
            text="YOUR PERSONAL WORKSPACE",
            bg=SIDEBAR,
            fg="#A7C5BB",
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", pady=(4, 0))

        tk.Label(
            self.sidebar,
            text="WORKSPACE",
            bg=SIDEBAR,
            fg="#8EAAA1",
            font=("Segoe UI", 8, "bold"),
            anchor="w"
        ).pack(fill="x", padx=24, pady=(0, 10))

        pages = [
            ("Dashboard", "⌂"),
            ("Tasks", "✓"),
            ("Habits", "◷"),
            ("Finance", "₹"),
            ("Notes", "▤"),
            ("Journal", "✎"),
            ("Search", "⌕")
        ]

        for page, symbol in pages:
            button = tk.Button(
                self.sidebar,
                text=f"   {symbol}     {page}",
                command=lambda name=page: self.show_page(name),
                bg=SIDEBAR,
                fg="#D5E4DF",
                activebackground=SIDEBAR_HOVER,
                activeforeground=WHITE,
                relief="flat",
                bd=0,
                font=("Segoe UI", 11),
                anchor="w",
                padx=15,
                pady=13,
                cursor="hand2"
            )
            button.pack(fill="x", padx=12, pady=2)
            self.nav_buttons[page] = button

        footer = tk.Frame(self.sidebar, bg=SIDEBAR)
        footer.pack(side="bottom", fill="x", padx=22, pady=22)

        tk.Frame(
            footer,
            bg="#42645E",
            height=1
        ).pack(fill="x", pady=(0, 13))

        tk.Label(
            footer,
            text="LOCAL WORKSPACE",
            bg=SIDEBAR,
            fg="#A7C5BB",
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w")

        tk.Label(
            footer,
            text="Your data stays on this device.",
            bg=SIDEBAR,
            fg="#D5E4DF",
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(5, 0))

    #Creates the top information bar
    def create_topbar(self):
        topbar = tk.Frame(
            self.main_area,
            bg=WHITE,
            height=58,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        tk.Label(
            topbar,
            text="PERSONAL PRODUCTIVITY",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9, "bold")
        ).pack(side="left", padx=28)

        tk.Label(
            topbar,
            text=date.today().strftime("%A, %d %B %Y"),
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 9)
        ).pack(side="right", padx=28)

    #Opens the selected screen and highlight its navigation button
    def show_page(self, page_name):
        self.current_page = page_name

        for widget in self.page_container.winfo_children():
            widget.destroy()

        for name, button in self.nav_buttons.items():
            if name == page_name:
                button.configure(
                    bg=ACCENT,
                    fg=WHITE,
                    font=("Segoe UI", 11, "bold")
                )
            else:
                button.configure(
                    bg=SIDEBAR,
                    fg="#D5E4DF",
                    font=("Segoe UI", 11)
                )

        screens = {
            "Dashboard": DashboardScreen,
            "Tasks": TasksScreen,
            "Habits": HabitsScreen,
            "Finance": FinanceScreen,
            "Notes": NotesScreen,
            "Journal": JournalScreen,
            "Search": SearchScreen
        }

        screen_class = screens.get(page_name)

        if screen_class:
            self.page_canvas = tk.Canvas(
                self.page_container,
                bg=BG,
                highlightthickness=0
            )
            scrollbar = ttk.Scrollbar(
                self.page_container,
                orient="vertical",
                command=self.page_canvas.yview
            )
            self.page_canvas.configure(yscrollcommand=scrollbar.set)

            scrollbar.pack(side="right", fill="y")
            self.page_canvas.pack(side="left", fill="both", expand=True)

            page_content = tk.Frame(self.page_canvas, bg=BG)
            self.page_window = self.page_canvas.create_window(
                (0, 0),
                window=page_content,
                anchor="nw"
            )
            page_content.bind(
                "<Configure>",
                lambda event: self.page_canvas.configure(
                    scrollregion=self.page_canvas.bbox("all")
                )
            )
            self.page_canvas.bind(
                "<Configure>",
                lambda event: self.page_canvas.itemconfigure(
                    self.page_window,
                    width=event.width
                )
            )

            screen = screen_class(page_content)
            screen.pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = DeskOS(root)
    root.mainloop()
