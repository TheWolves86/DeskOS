from tkinter import *
from tkinter import ttk

root = Tk()
root.title("DeskOS")
root.geometry("800x600")
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Welcome to DeskOS").grid(column=0, row=1)
ttk.Label(frm, text="DeskOS").grid(column=0, row=0)
ttk.Button(frm, text="Say Hello", command=lambda: print("Hello World")).grid(column=5, row=2)
ttk.Button(frm, text="Exit DeskOS", command=root.destroy).grid(column=1, row=0)
root.mainloop()
