import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("DeskOS")
root.geometry("900x600")
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


pages = [
    "Dashboard",
    "Tasks",
    "Habits",
    "Finance",
    "Notes",
    "Journal",
    "Search"
]

def show_page(page_name):
    for widget in content.winfo_children():
        widget.destroy()

    heading = tk.Label(
        content,
        text=page_name,
        bg="#F5F4EF",
        fg="#173C3A",
        font=("Segoe UI", 24, "bold"),
    )
    heading.pack(anchor="w", padx=30, pady=30)

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

root.mainloop()