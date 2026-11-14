
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from features import finance as finance_backend


#Finance Screen
class FinanceScreen(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.configure(style="Finance.TFrame")

        self.bg_color = "#F5F4EF"
        self.card_color = "#FFFFFF"
        self.teal = "#075753"
        self.dark_text = "#173C3A"
        self.muted_text = "#71817D"

        self.current_filter = "All"
        self.setup_styles()
        self.canvas = tk.Canvas(
            self,
            bg=self.bg_color,
            highlightthickness=0
        )
        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.page = ttk.Frame(self.canvas, style="Finance.TFrame")
        self.page_window = self.canvas.create_window(
            (0, 0),
            window=self.page,
            anchor="nw"
        )
        self.page.bind("<Configure>", self.update_scroll_region)
        self.canvas.bind("<Configure>", self.resize_page)

        self.create_layout()
        self.bind_mousewheel(self.page)
        self.refresh_data()

    #Styles
    def setup_styles(self):
        style = ttk.Style()

        style.configure(
            "Finance.TFrame",
            background=self.bg_color
        )

        style.configure(
            "Finance.Treeview",
            background="white",
            foreground=self.dark_text,
            rowheight=35,
            fieldbackground="white",
            font=("Segoe UI", 10)
        )

        style.configure(
            "Finance.Treeview.Heading",
            background="#E9EFEC",
            foreground=self.dark_text,
            font=("Segoe UI", 10, "bold"),
            relief="flat"
        )

        style.map(
            "Finance.Treeview",
            background=[("selected", "#D5E9E4")],
            foreground=[("selected", self.dark_text)]
        )

    def update_scroll_region(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def resize_page(self, event):
        self.canvas.itemconfigure(self.page_window, width=event.width)

    def bind_mousewheel(self, widget):
        if not isinstance(widget, (ttk.Combobox, ttk.Treeview)):
            widget.bind("<MouseWheel>", self.on_mousewheel, add="+")
            widget.bind("<Button-4>", self.on_mousewheel, add="+")
            widget.bind("<Button-5>", self.on_mousewheel, add="+")

        for child in widget.winfo_children():
            self.bind_mousewheel(child)

    def on_mousewheel(self, event):
        if getattr(event, "num", None) == 4:
            units = -1
        elif getattr(event, "num", None) == 5:
            units = 1
        else:
            units = -int(event.delta / 120)
            if units == 0:
                units = -1 if event.delta > 0 else 1

        self.canvas.yview_scroll(units, "units")
        return "break"

    #Main Layout
    def create_layout(self):

        self.configure(style="Finance.TFrame")

        #Main heading
        header = tk.Frame(self.page, bg=self.bg_color)
        header.pack(fill="x", padx=30, pady=(25, 15))

        tk.Label(
            header,
            text="Finance",
            bg=self.bg_color,
            fg=self.dark_text,
            font=("Segoe UI", 24, "bold")
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Keep track of your income and expenses.",
            bg=self.bg_color,
            fg=self.muted_text,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(4, 0))

        # Summary cards
        self.create_summary_cards(self.page)

        # Transaction section
        self.create_transaction_section(self.page)

    #Summary Cards
    def create_summary_cards(self, parent):

        cards_frame = tk.Frame(parent, bg=self.bg_color)
        cards_frame.pack(fill="x", padx=30, pady=10)

        cards_frame.columnconfigure(0, weight=1)
        cards_frame.columnconfigure(1, weight=1)
        cards_frame.columnconfigure(2, weight=1)

        self.balance_label = self.create_summary_card(
            cards_frame, 0, "Total Balance", self.dark_text
        )
        self.income_label = self.create_summary_card(
            cards_frame, 1, "Total Income", "#16845B"
        )
        self.expense_label = self.create_summary_card(
            cards_frame, 2, "Total Expenses", "#C45B52"
        )

    def create_summary_card(self, parent, column, title, value_color):
        card = tk.Frame(
            parent,
            bg="white",
            highlightbackground="#E5E9E6",
            highlightthickness=1
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=6,
            pady=5
        )

        tk.Label(
            card,
            text=title,
            bg="white",
            fg=self.muted_text,
            font=("Segoe UI", 10)
        ).pack(anchor="w", padx=16, pady=(14, 5))

        value_label = tk.Label(
            card,
            text="₹0.00",
            bg="white",
            fg=value_color,
            font=("Segoe UI", 19, "bold")
        )
        value_label.pack(anchor="w", padx=16, pady=(0, 14))
        return value_label

    #Transaction Section
    def create_transaction_section(self, parent):

        section = tk.Frame(parent, bg=self.bg_color)
        section.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(15, 25)
        )

        # Section heading
        top_bar = tk.Frame(section, bg=self.bg_color)
        top_bar.pack(fill="x", pady=(0, 12))

        tk.Label(
            top_bar,
            text="Transactions",
            bg=self.bg_color,
            fg=self.dark_text,
            font=("Segoe UI", 15, "bold")
        ).pack(side="left")

        entry_form = tk.Frame(
            section,
            bg="white",
            highlightbackground="#E5E9E6",
            highlightthickness=1
        )
        entry_form.pack(fill="x", pady=(0, 12))

        for column in range(3):
            entry_form.columnconfigure(column, weight=1)

        self.entry_amount_var = tk.StringVar()
        self.entry_description_var = tk.StringVar()
        self.entry_type_var = tk.StringVar(value="Expense")
        self.entry_category_var = tk.StringVar()
        self.entry_date_var = tk.StringVar(value=date.today().isoformat())

        self.add_inline_field(
            entry_form, "Amount (₹)", self.entry_amount_var, 12, 0, 0
        )
        self.add_inline_field(
            entry_form, "Description", self.entry_description_var, 22, 0, 1
        )
        tk.Label(
            entry_form,
            text="Type",
            bg="white",
            fg=self.dark_text,
            font=("Segoe UI", 9, "bold")
        ).grid(row=0, column=2, sticky="w", padx=(8, 12), pady=(8, 2))
        ttk.Combobox(
            entry_form,
            textvariable=self.entry_type_var,
            values=["Income", "Expense"],
            state="readonly",
            width=12,
            font=("Segoe UI", 10)
        ).grid(row=1, column=2, sticky="ew", padx=(8, 12), pady=(0, 8))

        self.add_inline_field(
            entry_form, "Category", self.entry_category_var, 18, 1, 0
        )
        self.add_inline_field(
            entry_form, "Date (YYYY-MM-DD)", self.entry_date_var, 14, 1, 1
        )
        tk.Button(
            entry_form,
            text="Save Transaction",
            command=self.save_inline_transaction,
            bg=self.teal,
            fg="white",
            activebackground="#167E75",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=6,
            cursor="hand2"
        ).grid(row=3, column=2, sticky="ew", padx=(8, 12), pady=(4, 8))

        # Search and filters
        toolbar = tk.Frame(section, bg=self.bg_color)
        toolbar.pack(fill="x", pady=(0, 12))

        self.search_var = tk.StringVar()

        search_entry = ttk.Entry(
            toolbar,
            textvariable=self.search_var,
            font=("Segoe UI", 10)
        )
        search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=6
        )

        search_entry.insert(0, "")

        self.search_var.trace_add(
            "write",
            lambda *args: self.refresh_table()
        )

        self.filter_var = tk.StringVar(value="All")

        filter_box = ttk.Combobox(
            toolbar,
            textvariable=self.filter_var,
            values=["All", "Income", "Expense"],
            state="readonly",
            width=12,
            font=("Segoe UI", 10)
        )
        filter_box.pack(side="left", padx=(10, 0), ipady=4)

        filter_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.refresh_table()
        )

        # Table container
        table_frame = tk.Frame(
            section,
            bg="white",
            highlightbackground="#E5E9E6",
            highlightthickness=1
        )
        table_frame.pack(fill="both", expand=True)

        columns = (
            "id",
            "date",
            "description",
            "type",
            "category",
            "amount"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Finance.Treeview"
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("date", text="Date")
        self.tree.heading("description", text="Description")
        self.tree.heading("type", text="Type")
        self.tree.heading("category", text="Category")
        self.tree.heading("amount", text="Amount")

        self.tree.column("id", width=45, anchor="center")
        self.tree.column("date", width=100, anchor="center")
        self.tree.column("description", width=180)
        self.tree.column("type", width=85, anchor="center")
        self.tree.column("category", width=110, anchor="center")
        self.tree.column("amount", width=110, anchor="e")

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
            expand=True,
            padx=(8, 0),
            pady=8
        )

        scrollbar.pack(
            side="right",
            fill="y",
            pady=8,
            padx=(0, 8)
        )

        self.tree.tag_configure(
            "income",
            foreground="#16845B"
        )

        self.tree.tag_configure(
            "expense",
            foreground="#C45B52"
        )

        # Action buttons
        actions = tk.Frame(section, bg=self.bg_color)
        actions.pack(fill="x", pady=(12, 0))

        tk.Button(
            actions,
            text="Edit",
            command=self.edit_transaction,
            bg="#E5EFEB",
            fg=self.dark_text,
            relief="flat",
            padx=16,
            pady=7,
            cursor="hand2"
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            actions,
            text="Delete",
            command=self.delete_transaction,
            bg="#F8E7E5",
            fg="#B64C43",
            relief="flat",
            padx=16,
            pady=7,
            cursor="hand2"
        ).pack(side="left")

        tk.Button(
            actions,
            text="Refresh",
            command=self.refresh_data,
            bg="#E9EFEC",
            fg=self.dark_text,
            relief="flat",
            padx=16,
            pady=7,
            cursor="hand2"
        ).pack(side="right")

    #Refresh Data
    def refresh_data(self):

        transactions = finance_backend.get_transactions()
        total_income = sum(
            row[1] for row in transactions if row[3] == "income"
        )
        total_expense = sum(
            row[1] for row in transactions if row[3] == "expense"
        )
        balance = finance_backend.get_balance()
        self.balance_label.config(
            text=f"₹{balance:,.2f}"
        )

        self.income_label.config(
            text=f"₹{total_income:,.2f}"
        )

        self.expense_label.config(
            text=f"₹{total_expense:,.2f}"
        )

        self.refresh_table()

    #Refresh Table
    def refresh_table(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        transactions = finance_backend.get_transactions()
        selected_filter = self.filter_var.get().lower()
        search_text = self.search_var.get().strip().lower()

        for row in sorted(
            transactions,
            key=lambda item: item[5] or "",
            reverse=True
        ):

            transaction_id = row[0]
            amount = row[1]
            description = row[2] or ""
            transaction_type = row[3] or ""
            category = row[4] or ""
            transaction_date = row[5] or ""

            # Apply type filter
            if selected_filter != "all":
                if transaction_type.lower() != selected_filter:
                    continue

            # Apply search
            searchable_text = (
                description + " " +
                category + " " +
                transaction_type + " " +
                transaction_date
            ).lower()

            if search_text not in searchable_text:
                continue

            tag = transaction_type.lower()
            self.tree.insert(
                "",
                "end",
                values=(
                    transaction_id,
                    transaction_date,
                    description,
                    transaction_type.title(),
                    category,
                    f"₹{amount:,.2f}"
                ),
                tags=(tag,)
            )


    def add_inline_field(self, parent, label, variable, width, row, column):
        tk.Label(
            parent,
            text=label,
            bg="white",
            fg=self.dark_text,
            font=("Segoe UI", 9, "bold")
        ).grid(
            row=row * 2,
            column=column,
            sticky="w",
            padx=(8, 12),
            pady=(8, 2)
        )
        ttk.Entry(
            parent,
            textvariable=variable,
            width=width,
            font=("Segoe UI", 10)
        ).grid(
            row=row * 2 + 1,
            column=column,
            sticky="ew",
            padx=(8, 12),
            pady=(0, 8)
        )

    def save_inline_transaction(self):
        values = self.validate_transaction(
            self.entry_amount_var.get(),
            self.entry_description_var.get(),
            self.entry_type_var.get(),
            self.entry_category_var.get(),
            self.entry_date_var.get()
        )
        if values is None:
            return

        finance_backend.add_transaction(*values)
        self.entry_amount_var.set("")
        self.entry_description_var.set("")
        self.entry_type_var.set("Expense")
        self.entry_category_var.set("")
        self.entry_date_var.set(date.today().isoformat())
        self.refresh_data()

    #Edit Transaction
    def edit_transaction(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a transaction to edit."
            )
            return

        values = self.tree.item(selected[0], "values")
        transaction_id = int(values[0])
        transaction = next(
            (
                row for row in finance_backend.get_transactions()
                if row[0] == transaction_id
            ),
            None
        )

        if transaction is None:
            messagebox.showerror(
                "Error",
                "Transaction not found."
            )
            return

        self.open_transaction_form(transaction)

    #Transaction Form
    def open_transaction_form(self, transaction=None):
        is_editing = transaction is not None
        window = tk.Toplevel(self)
        window.title(
            "Edit Transaction" if is_editing else "Add Transaction"
        )
        window.geometry("420x470")
        window.resizable(False, False)
        window.configure(bg=self.bg_color)
        window.transient(self.winfo_toplevel())
        window.grab_set()

        heading = (
            "Edit Transaction" if is_editing
            else "Add Transaction"
        )

        tk.Label(
            window,
            text=heading,
            bg=self.bg_color,
            fg=self.dark_text,
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=25, pady=(22, 18))

        form = tk.Frame(window, bg=self.bg_color)
        form.pack(fill="both", expand=True, padx=25)

        # Form variables
        amount_var = tk.StringVar(
            value=str(transaction[1]) if is_editing else ""
        )
        description_var = tk.StringVar(
            value=transaction[2] if is_editing else ""
        )
        type_var = tk.StringVar(
            value=transaction[3].title() if is_editing else "Expense"
        )
        category_var = tk.StringVar(
            value=transaction[4] if is_editing else ""
        )
        date_var = tk.StringVar(
            value=transaction[5] if is_editing else date.today().isoformat()
        )

        # Amount
        self.add_form_label(form, "Amount (₹)")

        ttk.Entry(
            form,
            textvariable=amount_var,
            font=("Segoe UI", 10)
        ).pack(fill="x", ipady=6, pady=(0, 12))

        # Description
        self.add_form_label(form, "Description")

        ttk.Entry(
            form,
            textvariable=description_var,
            font=("Segoe UI", 10)
        ).pack(fill="x", ipady=6, pady=(0, 12))

        # Type
        self.add_form_label(form, "Transaction Type")

        ttk.Combobox(
            form,
            textvariable=type_var,
            values=["Income", "Expense"],
            state="readonly",
            font=("Segoe UI", 10)
        ).pack(fill="x", ipady=4, pady=(0, 12))

        # Category
        self.add_form_label(form, "Category")

        ttk.Entry(
            form,
            textvariable=category_var,
            font=("Segoe UI", 10)
        ).pack(fill="x", ipady=6, pady=(0, 12))

        # Date
        self.add_form_label(form, "Date (YYYY-MM-DD)")

        ttk.Entry(
            form,
            textvariable=date_var,
            font=("Segoe UI", 10)
        ).pack(fill="x", ipady=6, pady=(0, 18))

        # Save function
        def save_transaction():

            values = self.validate_transaction(
                amount_var.get(),
                description_var.get(),
                type_var.get(),
                category_var.get(),
                date_var.get(),
                parent=window
            )
            if values is None:
                return

            # Save to database
            if is_editing:

                finance_backend.update_transaction(
                    transaction[0],
                    *values
                )

            else:

                finance_backend.add_transaction(*values)

            window.destroy()
            self.refresh_data()

        # Buttons
        buttons = tk.Frame(window, bg=self.bg_color)
        buttons.pack(fill="x", padx=25, pady=(5, 22))

        tk.Button(
            buttons,
            text="Cancel",
            command=window.destroy,
            bg="#E9EFEC",
            fg=self.dark_text,
            relief="flat",
            padx=18,
            pady=8,
            cursor="hand2"
        ).pack(side="left")

        tk.Button(
            buttons,
            text="Save Transaction",
            command=save_transaction,
            bg=self.teal,
            fg="white",
            activebackground="#167E75",
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=8,
            cursor="hand2"
        ).pack(side="right")

    def validate_transaction(
        self,
        amount_text,
        description,
        transaction_type,
        category,
        transaction_date,
        parent=None
    ):
        amount_text = amount_text.strip()
        description = description.strip()
        transaction_type = transaction_type.strip().lower()
        category = category.strip()
        transaction_date = transaction_date.strip()

        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Amount",
                "Enter an amount greater than zero.",
                parent=parent or self
            )
            return None

        if not description:
            messagebox.showerror(
                "Missing Description",
                "Please enter a description.",
                parent=parent or self
            )
            return None

        if not category:
            messagebox.showerror(
                "Missing Category",
                "Please enter a category.",
                parent=parent or self
            )
            return None

        if transaction_type not in ("income", "expense"):
            messagebox.showerror(
                "Invalid Type",
                "Choose Income or Expense.",
                parent=parent or self
            )
            return None

        try:
            date.fromisoformat(transaction_date)
        except ValueError:
            messagebox.showerror(
                "Invalid Date",
                "Use a valid date in YYYY-MM-DD format.",
                parent=parent or self
            )
            return None

        return amount, description, transaction_type, category, transaction_date

    #Form Label Helper
    def add_form_label(self, parent, text):

        tk.Label(
            parent,
            text=text,
            bg=self.bg_color,
            fg=self.dark_text,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=(0, 5))

    #Delete Transaction
    def delete_transaction(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a transaction to delete."
            )
            return

        values = self.tree.item(selected[0], "values")
        transaction_id = int(values[0])

        confirm = messagebox.askyesno(
            "Delete Transaction",
            "Are you sure you want to delete this transaction?"
        )

        if not confirm:
            return

        finance_backend.delete_transaction(transaction_id)
        self.refresh_data()
