import tkinter as tk
from tkinter import ttk
from tasks_ui import TasksScreen
from habits_ui import HabitsScreen
from finance_ui import FinanceScreen
from notes_ui import NotesScreen
from journal_ui import JournalScreen
from dashboard_ui import DashboardScreen

#creates the main window for our application
root = tk.Tk()

#set the title of the application
root.title("DeskOS")

#set the starting window size ig
root.geometry("900x600")

#set the minimum window size
root.minsize(800, 500)

#Main layout
sidebar = tk.Frame(root, bg="#075753", width=200)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

content = tk.Frame(root, bg="#F5F4EF")
content.pack(side="left", fill="both", expand=True)

#App name
logo = tk.Label(
    sidebar,
    text="🍃 DeskOS",
    bg="#075753",
    fg="white",
    font=("Segoe UI", 18, "bold"),
    anchor="w",
    padx=20,
    pady=25
)
logo.pack(fill="x")

#Stores the name of all the available pages
pages = [
    "Dashboard",
    "Tasks",
    "Habits",
    "Finance",
    "Notes",
    "Journal",
    "Search"
]

#displays the screen selected by the user
def show_page(page_name):
    for widget in content.winfo_children():
        widget.destroy()

    if page_name == "Dashboard":
        screen = DashboardScreen(content)
        screen.pack(fill="both", expand=True)

    elif page_name == "Tasks":
        screen = TasksScreen(content)
        screen.pack(fill="both", expand=True)

    elif page_name == "Habits":
        screen = HabitsScreen(content)
        screen.pack(fill="both", expand=True)

    elif page_name == "Finance":
        screen = FinanceScreen(content)
        screen.pack(fill="both", expand=True)

    elif page_name == "Notes":
        screen = NotesScreen(content)
        screen.pack(fill="both", expand=True)

    elif page_name == "Journal":
        screen = JournalScreen(content)
        screen.pack(fill="both", expand=True)

    else:
        heading = tk.Label(
            content,
            text=page_name,
            bg="#F5F4EF",
            fg="#173C3A",
            font=("Segoe UI", 24, "bold")
        )
        heading.pack(anchor="w", padx=30, pady=30)


#loops through every page in pages list
for page in pages:
    button = tk.Button(
        sidebar,
        text=page,
        command = lambda name=page: show_page(name),
        bg="#075753",
        fg="white",
        activebackground="#167E75",
        activeforeground="white",
        relief="flat",
        bd=0,
        font=("Segoe UI", 11),
        anchor="w",
        padx=22,
        pady=12,
        cursor="hand2"
    )
    button.pack(fill="x")

show_page("Dashboard")

#keeps the application running
root.mainloop()

#