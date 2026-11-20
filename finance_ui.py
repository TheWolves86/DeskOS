
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from features import finance as backend


BG = "#F4F6F3"
WHITE = "#FFFFFF"
TEXT = "#183B37"
MUTED = "#82918B"
ACCENT = "#268477"
BORDER = "#E3EAE5"


class FinanceScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)

        self.search_var = tk.StringVar()
        self.filter_var = tk.StringVar(value="All")
        self.setup_styles()
        self.build_header()
        self.build_summary()
        self.build_toolbar()
        self.build_table()
        self.refresh_data()

    #setups the styles
    def setup_styles(self):
        style = ttk.Style()

        style.configure(
            "Finance.Treeview",
            background=WHITE,
            foreground=TEXT,
            fieldbackground=WHITE,
            rowheight=39,
            borderwidth=0,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Finance.Treeview.Heading",
            background="#EAF0EC",
            foreground=TEXT,
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padding=10
        )

        style.map(
            "Finance.Treeview",
            background=[("selected", "#D5E9E2")],
            foreground=[("selected", TEXT)]
        )

    #heading
    def build_header(self):
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=30, pady=(25, 18))

        tk.Label(
            header,
            text="Finance",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 25, "bold")
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Track your income, expenses and balance.",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(4, 0))

    # Summary cards
    def build_summary(self):
        container = tk.Frame(self, bg=BG)
        container.pack(fill="x", padx=30, pady=(0, 20))

        for i in range(3):
            container.grid_columnconfigure(i, weight=1, uniform="cards")

        self.balance_label = self.create_card(
            container, 0, "Total Balance", "₹0.00", TEXT
        )
        self.income_label = self.create_card(
            container, 1, "Total Income", "₹0.00", "#26845D"
        )
        self.expense_label = self.create_card(
            container, 2, "Total Expenses", "₹0.00", "#C45B52"
        )

    def create_card(self, parent, column, title, value, color):
        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=(0 if column == 0 else 6, 0 if column == 2 else 6)
        )

        tk.Frame(card, bg=color, height=4).pack(fill="x")

        body = tk.Frame(card, bg=WHITE, padx=17, pady=14)
        body.pack(fill="both", expand=True)

        tk.Label(
            body,
            text=title.upper(),
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w")

        label = tk.Label(
            body,
            text=value,
            bg=WHITE,
            fg=color,
            font=("Segoe UI", 21, "bold")
        )
        label.pack(anchor="w", pady=(8, 0))

        return label

    #search and transaction controls
    def build_toolbar(self):
        toolbar = tk.Frame(self, bg=BG)
        toolbar.pack(fill="x", padx=30, pady=(0, 15))

        search_frame = tk.Frame(
            toolbar,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        search_frame.pack(side="left", fill="x", expand=True)

        tk.Label(
            search_frame,
            text="⌕",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 16)
        ).pack(side="left", padx=(11, 3))

        ttk.Entry(
            search_frame,
            textvariable=self.search_var
        ).pack(side="left", fill="x", expand=True, ipady=7, padx=7)

        self.search_var.trace_add(
            "write",
            lambda *args: self.refresh_table()
        )

        ttk.Combobox(
            toolbar,
            textvariable=self.filter_var,
            values=["All", "Income", "Expense"],
            state="readonly",
            width=12
        ).pack(side="left", padx=10, ipady=5)

        self.filter_var.trace_add(
            "write",
            lambda *args: self.refresh_table()
        )

        tk.Button(
            toolbar,
            text="+  Add Transaction",
            command=self.open_form,
            bg=ACCENT,
            fg=WHITE,
            activebackground="#1D6E63",
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            padx=17,
            pady=10,
            cursor="hand2"
        ).pack(side="right")

    #transaction table
    def build_table(self):
        container = tk.Frame(
            self,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        container.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 15)
        )

        heading = tk.Frame(container, bg=WHITE)
        heading.pack(fill="x", padx=18, pady=15)

        tk.Label(
            heading,
            text="Transactions",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 13, "bold")
        ).pack(side="left")

        self.count_label = tk.Label(
            heading,
            text="0 transactions",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9)
        )
        self.count_label.pack(side="right")

        tk.Frame(container, bg=BORDER, height=1).pack(fill="x")

        table_area = tk.Frame(container, bg=WHITE)
        table_area.pack(fill="both", expand=True, padx=12, pady=12)

        columns = ("id", "date", "description", "type", "category", "amount")

        self.tree = ttk.Treeview(
            table_area,
            columns=columns,
            show="headings",
            style="Finance.Treeview",
            selectmode="browse"
        )

        headings = {
            "id": "ID",
            "date": "DATE",
            "description": "DESCRIPTION",
            "type": "TYPE",
            "category": "CATEGORY",
            "amount": "AMOUNT"
        }

        for column, title in headings.items():
            self.tree.heading(column, text=title)

        self.tree.column("id", width=45, anchor="center", stretch=False)
        self.tree.column("date", width=105, anchor="center")
        self.tree.column("description", width=200)
        self.tree.column("type", width=90, anchor="center")
        self.tree.column("category", width=110, anchor="center")
        self.tree.column("amount", width=120, anchor="e")

        self.tree.tag_configure("income", foreground="#26845D")
        self.tree.tag_configure("expense", foreground="#C45B52")

        scrollbar = ttk.Scrollbar(
            table_area,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind(
            "<Double-1>",
            lambda event: self.edit_transaction()
        )

        #Table actions
        actions = tk.Frame(self, bg=BG)
        actions.pack(fill="x", padx=30, pady=(0, 20))

        self.action_button(
            actions, "Edit", self.edit_transaction
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            actions,
            text="Delete",
            command=self.delete_transaction,
            bg="#FCECEB",
            fg="#B64A43",
            activebackground="#F5D8D5",
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            font=("Segoe UI", 9, "bold")
        ).pack(side="left")

        self.action_button(
            actions, "↻ Refresh", self.refresh_data
        ).pack(side="right")

    def action_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=WHITE,
            fg=TEXT,
            activebackground="#EAF0EC",
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            font=("Segoe UI", 9, "bold")
        )

    #Update summary cards
    def refresh_data(self):
        try:
            transactions = backend.get_transactions()

            income = sum(
                float(row[1]) for row in transactions
                if row[3] == "income"
            )

            expenses = sum(
                float(row[1]) for row in transactions
                if row[3] == "expense"
            )

            balance = backend.get_balance()

            self.balance_label.config(text=f"₹{balance:,.2f}")
            self.income_label.config(text=f"₹{income:,.2f}")
            self.expense_label.config(text=f"₹{expenses:,.2f}")

            self.refresh_table()

        except Exception as error:
            messagebox.showerror("Finance Error", str(error))

    #refresh transaction list
    def refresh_table(self):
        if not hasattr(self, "tree"):
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            transactions = backend.get_transactions()
        except Exception as error:
            messagebox.showerror("Database Error", str(error))
            return

        query = self.search_var.get().strip().lower()
        selected_filter = self.filter_var.get().lower()

        visible = 0

        for row in sorted(
            transactions,
            key=lambda item: item[5] or "",
            reverse=True
        ):
            transaction_id, amount, description, kind, category, transaction_date = row

            description = description or ""
            category = category or ""
            kind = kind or ""
            transaction_date = transaction_date or ""

            if selected_filter != "all" and kind.lower() != selected_filter:
                continue

            searchable = (
                f"{description} {category} {kind} {transaction_date}"
            ).lower()

            if query and query not in searchable:
                continue

            self.tree.insert(
                "",
                "end",
                iid=str(transaction_id),
                values=(
                    transaction_id,
                    transaction_date,
                    description,
                    kind.title(),
                    category,
                    f"₹{float(amount):,.2f}"
                ),
                tags=(kind.lower(),)
            )

            visible += 1

        self.count_label.config(text=f"{visible} transactions")

    #Add or edit transaction
    def open_form(self, transaction=None):
        editing = transaction is not None

        window = tk.Toplevel(self)
        window.title("Edit Transaction" if editing else "New Transaction")
        window.geometry("440x520")
        window.resizable(False, False)
        window.configure(bg=BG)
        window.transient(self.winfo_toplevel())

        tk.Label(
            window,
            text="Edit Transaction" if editing else "New Transaction",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 21, "bold")
        ).pack(anchor="w", padx=28, pady=(24, 4))

        tk.Label(
            window,
            text="Enter the transaction details below.",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=28, pady=(0, 15))

        form = tk.Frame(window, bg=BG)
        form.pack(fill="both", expand=True, padx=28)

        def make_field(label, value=""):
            tk.Label(
                form,
                text=label,
                bg=BG,
                fg=TEXT,
                font=("Segoe UI", 9, "bold")
            ).pack(anchor="w", pady=(9, 5))

            entry = ttk.Entry(form)
            entry.pack(fill="x", ipady=5)
            entry.insert(0, str(value or ""))
            return entry

        amount_entry = make_field(
            "Amount (₹)",
            transaction[1] if editing else ""
        )

        description_entry = make_field(
            "Description",
            transaction[2] if editing else ""
        )

        tk.Label(
            form,
            text="Transaction Type",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=(12, 5))

        type_var = tk.StringVar(
            value=transaction[3].title() if editing else "Expense"
        )

        ttk.Combobox(
            form,
            textvariable=type_var,
            values=["Income", "Expense"],
            state="readonly"
        ).pack(fill="x", ipady=4)

        category_entry = make_field(
            "Category",
            transaction[4] if editing else ""
        )

        date_entry = make_field(
            "Date (YYYY-MM-DD)",
            transaction[5] if editing else date.today().isoformat()
        )

        def save():
            amount_text = amount_entry.get().strip()
            description = description_entry.get().strip()
            category = category_entry.get().strip()
            transaction_date = date_entry.get().strip()
            kind = type_var.get().lower()

            try:
                amount = float(amount_text)
                if amount <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Invalid Amount",
                    "Enter an amount greater than zero.",
                    parent=window
                )
                return

            if not description or not category:
                messagebox.showwarning(
                    "Missing Information",
                    "Description and category are required.",
                    parent=window
                )
                return

            try:
                date.fromisoformat(transaction_date)
            except ValueError:
                messagebox.showerror(
                    "Invalid Date",
                    "Use YYYY-MM-DD for the date.",
                    parent=window
                )
                return

            try:
                if editing:
                    backend.update_transaction(
                        transaction[0],
                        amount,
                        description,
                        kind,
                        category,
                        transaction_date
                    )
                else:
                    backend.add_transaction(
                        amount,
                        description,
                        kind,
                        category,
                        transaction_date
                    )

                window.destroy()
                self.refresh_data()

            except Exception as error:
                messagebox.showerror(
                    "Save Failed",
                    str(error),
                    parent=window
                )

        buttons = tk.Frame(window, bg=BG)
        buttons.pack(fill="x", padx=28, pady=20)

        tk.Button(
            buttons,
            text="Cancel",
            command=window.destroy,
            bg="#E9EFEC",
            fg=TEXT,
            relief="flat",
            padx=17,
            pady=9,
            cursor="hand2"
        ).pack(side="left")

        tk.Button(
            buttons,
            text="Save Transaction",
            command=save,
            bg=ACCENT,
            fg=WHITE,
            activebackground="#1D6E63",
            relief="flat",
            padx=17,
            pady=9,
            cursor="hand2"
        ).pack(side="right")

        window.update_idletasks()

        parent = self.winfo_toplevel()
        x = parent.winfo_rootx() + (parent.winfo_width() - 440) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - 520) // 2

        window.geometry(f"+{x}+{y}")
        window.grab_set()
        amount_entry.focus_set()

    #Get selected transaction
    def get_selected_transaction(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showinfo(
                "Select Transaction",
                "Please select a transaction first."
            )
            return None

        transaction_id = int(selected[0])

        return next(
            (
                row for row in backend.get_transactions()
                if row[0] == transaction_id
            ),
            None
        )

    #edit selected transaction
    def edit_transaction(self):
        transaction = self.get_selected_transaction()

        if transaction is not None:
            self.open_form(transaction)

    #Delete selected transaction
    def delete_transaction(self):
        transaction = self.get_selected_transaction()

        if transaction is None:
            return

        confirm = messagebox.askyesno(
            "Delete Transaction",
            f"Delete '{transaction[2]}'?"
        )

        if not confirm:
            return

        try:
            backend.delete_transaction(transaction[0])
            self.refresh_data()
        except Exception as error:
            messagebox.showerror("Delete Failed", str(error))

