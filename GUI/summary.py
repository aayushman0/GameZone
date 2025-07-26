from tkinter import ttk, StringVar
from db.orm import summary
from datetime import date
from template import Frame, date_entry


class SummaryFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(style="G.TFrame", padding=1)

    def tk_vars(self):
        self.total_expense = StringVar()
        self.total_income = StringVar()
        self.remaining_credit = StringVar()
        self.current_capital = StringVar()

    def main(self):
        ttk.Label(self.add_frame, text="Date:").grid(row=self.i, column=0, sticky="e", pady=10)
        self.i
        ttk.Label(self.list_frame, text="Total Expense:").grid(row=self.i, column=0, sticky="e", pady=10)
        ttk.Label(self.list_frame, text="Total Income:").grid(row=self.i, column=0, sticky="e", pady=10)
        self.i
        ttk.Label(self.list_frame, text="Remaining Credit:").grid(row=self.i, column=0, sticky="e", pady=10)
        ttk.Label(self.list_frame, text="Current Capital:").grid(row=self.i, column=0, sticky="e", pady=10)
        self.i = 0
        date_frame = ttk.Frame(self.add_frame)
        date_frame.grid(row=self.i, column=1, sticky="ew", pady=10)
        date_entry(self, date_frame)
        ttk.Button(
            self.add_frame, text="Filter", style="Confirm.TButton", command=self.update_total
        ).grid(
            row=self.i, column=1, sticky="ew", ipady=10, padx=(20, 50)
        )
        ttk.Entry(self.list_frame, textvariable=self.total_expense, state="readonly").grid(row=self.i, column=1, sticky="ew")
        ttk.Entry(self.list_frame, textvariable=self.total_income, state="readonly").grid(row=self.i, column=1, sticky="ew")
        ttk.Separator(self.list_frame).grid(row=self.i, column=0, columnspan=2, sticky="ew", pady=10)
        ttk.Entry(self.list_frame, textvariable=self.remaining_credit, state="readonly").grid(row=self.i, column=1, sticky="ew")
        ttk.Entry(self.list_frame, textvariable=self.current_capital, state="readonly").grid(row=self.i, column=1, sticky="ew")

    def update_total(self):
        year = self.year.get()
        month = self.month.get()
        day = self.day.get()
        if not (year or month or day):
            return None
        filter_date = date(year, month, day)
        self.total_expense.set(summary.total_expense(filter_date, filter_date))
        self.total_income.set(summary.total_income(filter_date, filter_date))

    def refresh(self):
        self.add_frame.tkraise()
        current_time = date.today()
        self.year.set(current_time.year)
        self.month.set(current_time.month)
        self.day.set(current_time.day)
        self.total_expense.set(summary.total_expense())
        self.total_income.set(summary.total_income())
        self.remaining_credit.set(summary.remaining_credit())
        self.current_capital.set(summary.current_capital())
