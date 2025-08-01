import tkinter as tk
from tkinter import ttk, StringVar, messagebox
from db.orm import credit
from datetime import datetime
from template import Frame, date_entry
from variables import ROW_COUNT, FONT


class CreditFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(style="G.TFrame", padding=1)

    def tk_vars(self):
        self.table_columns = ("ID", "Provider", "Initial Amount", "Current Amount")
        self.table_columns_width = (5, 300, 100, 100)
        self.table_columns_align = ("e", "w", "e", "e")
        self.provider = StringVar()
        self.initial_amount = StringVar()
        self.id = StringVar()
        self.provider_2 = StringVar()
        self.payment = StringVar()

    def main(self):
        ttk.Label(self.add_frame, text="Provider:").grid(row=self.i, column=0, sticky="e", pady=10)
        ttk.Label(self.add_frame, text="Amount:").grid(row=self.i, column=0, sticky="e", pady=10)
        ttk.Label(self.add_frame, text="Date:").grid(row=self.i, column=0, sticky="e", pady=10)
        self.i = 0
        ttk.Entry(self.add_frame, textvariable=self.provider).grid(row=self.i, column=1, sticky="ew")
        ttk.Entry(self.add_frame, textvariable=self.initial_amount).grid(row=self.i, column=1, sticky="ew")
        date_frame = ttk.Frame(self.add_frame)
        date_frame.grid(row=self.i, column=1, sticky="w")
        date_entry(self, date_frame)
        ttk.Button(
            self.add_frame, text="Add Credit", style="Confirm.TButton", command=self.save_credit
        ).grid(
            row=self.i, column=0, columnspan=2, sticky="ew", ipady=10
        )

        self.list_table = ttk.Treeview(self.list_frame, show="headings", selectmode="browse", columns=self.table_columns, height=ROW_COUNT)
        for col_name, col_width, col_align in zip(self.table_columns, self.table_columns_width, self.table_columns_align):
            self.list_table.heading(col_name, text=col_name)
            self.list_table.column(col_name, width=col_width, anchor=col_align)
        self.list_table.place(relx=0, rely=0, relwidth=1.0, relheight=0.93)
        page_no_frame = ttk.Frame(self.list_frame)
        page_no_frame.place(relx=0, rely=0.93, relwidth=1.0, relheight=0.07)
        tk.Button(
            page_no_frame, text="<<", height=1, font=FONT, command=lambda: self.change_page(-1)
        ).place(relx=0, rely=0, relwidth=0.4, relheight=1.0)
        self.page_no_label = ttk.Label(page_no_frame, text="00/00", justify="center", font=FONT, anchor="center")
        self.page_no_label.place(relx=0.4, rely=0, relwidth=0.2, relheight=1.0)
        tk.Button(
            page_no_frame, text=">>", height=1, font=FONT, command=lambda: self.change_page(1)
        ).place(relx=0.6, rely=0, relwidth=0.4, relheight=1.0)

        self.i = 0
        ttk.Label(self.detail_frame, text="ID:").grid(row=self.i, column=0, sticky="e", pady=10)
        ttk.Label(self.detail_frame, text="Provider:").grid(row=self.i, column=0, sticky="e", pady=10)
        ttk.Label(self.detail_frame, text="Paid Amount:").grid(row=self.i, column=0, sticky="e", pady=10)
        ttk.Label(self.detail_frame, text="Date:").grid(row=self.i, column=0, sticky="e", pady=10)
        self.i = 0
        ttk.Entry(self.detail_frame, textvariable=self.id, state="readonly").grid(row=self.i, column=1, sticky="ew")
        ttk.Entry(self.detail_frame, textvariable=self.provider_2, state="readonly").grid(row=self.i, column=1, sticky="ew")
        ttk.Entry(self.detail_frame, textvariable=self.payment).grid(row=self.i, column=1, sticky="ew")
        date_frame_2 = ttk.Frame(self.detail_frame)
        date_frame_2.grid(row=self.i, column=1, sticky="w")
        date_entry(self, date_frame_2)
        ttk.Button(
            self.detail_frame, text="Pay Credit", style="Confirm.TButton", command=self.update_credit
        ).grid(
            row=self.i, column=0, columnspan=2, sticky="ew", ipady=10
        )
        ttk.Button(
            self.detail_frame, text="Delete Credit", style="Delete.TButton", command=self.delete_credit
        ).grid(
            row=self.i, column=0, columnspan=2, sticky="ew", ipady=10
        )

    def events(self):
        self.list_table.bind("<Double-Button-1>", self.select_credit)

    def save_credit(self):
        provider = self.provider.get()
        initial_amount = self.initial_amount.get()
        year = self.year.get()
        month = self.month.get()
        day = self.day.get()
        hour = self.hour.get() or 0
        minute = self.minute.get() or 0
        if not (provider and initial_amount and year and month and day):
            messagebox.showwarning("Missing Values", "Values are Missing!")
            return None
        try:
            float(initial_amount)
            int(year)
            int(month)
            int(day)
            int(hour)
            int(minute)
        except ValueError:
            messagebox.showwarning("Wrong Type", "String used instead of numbers!")
            return None
        date = datetime(year, month, day, hour, minute)
        credit.create(provider, initial_amount, date)
        self.refresh()

    def update_credit(self):
        id = self.id.get()
        amount = self.payment.get()
        year = self.year.get()
        month = self.month.get()
        day = self.day.get()
        hour = self.hour.get() or 0
        minute = self.minute.get() or 0
        if not (id and amount and year and month and day):
            messagebox.showwarning("Missing Values", "Values are Missing!")
            return None
        try:
            float(amount)
            int(year)
            int(month)
            int(day)
            int(hour)
            int(minute)
        except ValueError:
            messagebox.showwarning("Wrong Type", "String used instead of numbers!")
            return None
        date = datetime(year, month, day, hour, minute)
        credit.update(id, amount, date)
        self.refresh()

    def delete_credit(self):
        credit_id = self.id.get()
        if not credit_id:
            return None
        confirmation = messagebox.askyesno("Are you sure?", f"Do you want to delete credit of ID.{credit_id}?")
        if not confirmation:
            return None
        credit.delete(credit_id)
        self.refresh()

    def select_credit(self, *args):
        selected_credit = self.list_table.selection()
        if not selected_credit:
            return None
        credit_id = self.list_table.item(selected_credit[0]).get("values", [None])[0]
        c = credit.get_by_id(credit_id)
        self.id.set(c.id)
        self.provider_2.set(c.provider)
        self.payment.set("")
        date = datetime.now()
        self.year.set(date.year)
        self.month.set(date.month)
        self.day.set(date.day)
        self.hour.set(date.hour)
        self.minute.set(date.minute)
        self.detail_frame.tkraise()

    def update_table(self):
        credits, credit_count = credit.get_paginated(self.page_no, show_cleared=True)
        self.total_pages = (credit_count - 1) // ROW_COUNT + 1
        self.page_no_label.config(text=f"{self.page_no}/{self.total_pages}")
        self.list_table.delete(*self.list_table.get_children())
        for row in credits:
            self.list_table.insert(
                '', tk.END,
                values=(row.id, row.provider, row.initial_amount, row.current_amount)
            )

    def change_page(self, i: int):
        next_page_no = self.page_no + i
        if next_page_no in range(1, self.total_pages + 1):
            self.page_no = next_page_no
            self.update_table()

    def refresh(self):
        self.add_frame.tkraise()
        self.provider.set("")
        self.initial_amount.set("")

        self.provider_2.set("")
        self.payment.set("")

        current_time = datetime.now()
        self.year.set(current_time.year)
        self.month.set(current_time.month)
        self.day.set(current_time.day)
        self.hour.set(current_time.hour)
        self.minute.set(current_time.minute)

        self.page_no = 1
        self.update_table()
