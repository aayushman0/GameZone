import tkinter as tk
from tkinter import ttk, StringVar, messagebox
from db.orm import income
from datetime import datetime
from template import Frame, date_entry
from variables import ROW_COUNT, FONT


class IncomeFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(style="G.TFrame", padding=1)

    def tk_vars(self):
        self.table_columns = ("ID", "Name", "Price", "Date")
        self.table_columns_width = (5, 300, 100, 100)
        self.table_columns_align = ("e", "w", "e", "e")
        self.add_table_columns = ("Name", "Price")
        self.add_table_columns_width = (250, 50)
        self.add_table_columns_align = ("w", "e")
        self.customer_name = StringVar()
        self.name = StringVar()
        self.price = StringVar()
        self.income_list = list()
        self.discount = StringVar()
        self.final_price = StringVar()
        self.id = StringVar()
        self.customer_name_2 = StringVar()
        self.name_2 = StringVar()
        self.price_2 = StringVar()
        self.income_list_2 = list()
        self.discount_2 = StringVar()
        self.final_price_2 = StringVar()

    def main(self):
        ttk.Label(self.add_frame, text="Customer:").grid(row=self.i, column=0, sticky="e", pady=5)
        ttk.Label(self.add_frame, text="Name:").grid(row=self.i, column=0, sticky="e", pady=5)
        ttk.Label(self.add_frame, text="Price:").grid(row=self.i, column=0, sticky="e", pady=5)
        self.i = self.i + 2
        ttk.Label(self.add_frame, text="Discount:").grid(row=self.i, column=0, sticky="e", pady=5)
        ttk.Label(self.add_frame, text="Net Total:").grid(row=self.i, column=0, sticky="e", pady=5)
        ttk.Label(self.add_frame, text="Date:").grid(row=self.i, column=0, sticky="e", pady=5)
        self.i = 0
        ttk.Entry(self.add_frame, textvariable=self.customer_name).grid(row=self.i, column=1, sticky="ew")
        ttk.Entry(self.add_frame, textvariable=self.name).grid(row=self.i, column=1, sticky="ew")
        ttk.Entry(self.add_frame, textvariable=self.price).grid(row=self.i, column=1, sticky="ew")
        ttk.Button(
            self.add_frame, text="Add to List", style="Confirm.TButton", command=self.add_to_list
        ).grid(
            row=self.i, column=1, sticky="ew", ipady=10
        )
        self.add_table = ttk.Treeview(self.add_frame, show="headings", selectmode="browse", columns=self.add_table_columns, height=5)
        for col_name, col_width, col_align in zip(self.add_table_columns, self.add_table_columns_width, self.add_table_columns_align):
            self.add_table.heading(col_name, text=col_name)
            self.add_table.column(col_name, width=col_width, anchor=col_align)
        self.add_table.grid(row=self.i, column=0, columnspan=2, sticky="ew")
        ttk.Entry(self.add_frame, textvariable=self.discount).grid(row=self.i, column=1, sticky="ew")
        ttk.Entry(self.add_frame, textvariable=self.final_price).grid(row=self.i, column=1, sticky="ew")
        date_frame = ttk.Frame(self.add_frame)
        date_frame.grid(row=self.i, column=1, sticky="ew")
        date_entry(self, date_frame)
        ttk.Button(
            self.add_frame, text="Add Income", style="Confirm.TButton", command=self.save_income
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
        ttk.Label(self.detail_frame, text="ID:").grid(row=self.i, column=0, sticky="e", pady=5)
        ttk.Label(self.detail_frame, text="Customer:").grid(row=self.i, column=0, sticky="e", pady=5)
        ttk.Label(self.detail_frame, text="Name:").grid(row=self.i, column=0, sticky="e", pady=5)
        ttk.Label(self.detail_frame, text="Price:").grid(row=self.i, column=0, sticky="e", pady=5)
        self.i = self.i + 2
        ttk.Label(self.detail_frame, text="Discount:").grid(row=self.i, column=0, sticky="e", pady=5)
        ttk.Label(self.detail_frame, text="Net Total:").grid(row=self.i, column=0, sticky="e", pady=5)
        ttk.Label(self.detail_frame, text="Date:").grid(row=self.i, column=0, sticky="e", pady=5)
        self.i = 0
        ttk.Entry(self.detail_frame, textvariable=self.id, state="readonly").grid(row=self.i, column=1, sticky="ew")
        ttk.Entry(self.detail_frame, textvariable=self.customer_name_2).grid(row=self.i, column=1, sticky="ew")
        ttk.Entry(self.detail_frame, textvariable=self.name_2).grid(row=self.i, column=1, sticky="ew")
        ttk.Entry(self.detail_frame, textvariable=self.price_2).grid(row=self.i, column=1, sticky="ew")
        ttk.Button(
            self.detail_frame, text="Add to List", style="Confirm.TButton", command=self.add_to_list_2
        ).grid(
            row=self.i, column=1, sticky="ew", ipady=10
        )
        self.add_table_2 = ttk.Treeview(self.detail_frame, show="headings", selectmode="browse", columns=self.add_table_columns, height=5)
        for col_name, col_width, col_align in zip(self.add_table_columns, self.add_table_columns_width, self.add_table_columns_align):
            self.add_table_2.heading(col_name, text=col_name)
            self.add_table_2.column(col_name, width=col_width, anchor=col_align)
        self.add_table_2.grid(row=self.i, column=0, columnspan=2, sticky="ew")
        ttk.Entry(self.detail_frame, textvariable=self.discount_2).grid(row=self.i, column=1, sticky="ew")
        ttk.Entry(self.detail_frame, textvariable=self.final_price_2).grid(row=self.i, column=1, sticky="ew")
        date_frame_2 = ttk.Frame(self.detail_frame)
        date_frame_2.grid(row=self.i, column=1, sticky="ew")
        date_entry(self, date_frame_2)
        ttk.Button(
            self.detail_frame, text="Update Income", style="Confirm.TButton", command=self.update_income
        ).grid(
            row=self.i, column=0, columnspan=2, sticky="ew", ipady=10
        )
        ttk.Button(
            self.detail_frame, text="Delete Income", style="Delete.TButton", command=self.delete_income
        ).grid(
            row=self.i, column=0, columnspan=2, sticky="ew", ipady=10
        )

    def events(self):
        self.add_table.bind("<Double-Button-1>", self.remove_from_add_table)
        self.add_table_2.bind("<Double-Button-1>", self.remove_from_add_table_2)
        self.discount.trace_add("write", self.update_net_total)
        self.discount_2.trace_add("write", self.update_net_total_2)
        self.list_table.bind("<Double-Button-1>", self.select_income)

    def add_to_list(self):
        name = self.name.get()
        price = self.price.get()
        if not (name and price):
            messagebox.showwarning("Missing Values", "Values are Missing!")
            return None
        try:
            float(price)
        except ValueError:
            messagebox.showwarning("Wrong Type", "String used instead of numbers!")
            return None
        self.income_list.append((name, float(price)))
        self.name.set("")
        self.price.set("")
        self.update_add_table()

    def add_to_list_2(self):
        name = self.name_2.get()
        price = self.price_2.get()
        if not (name and price):
            messagebox.showwarning("Missing Values", "Values are Missing!")
            return None
        try:
            float(price)
        except ValueError:
            messagebox.showwarning("Wrong Type", "String used instead of numbers!")
            return None
        self.income_list_2.append((name, float(price)))
        self.name_2.set("")
        self.price_2.set("")
        self.update_add_table_2()

    def update_add_table(self):
        self.add_table.delete(*self.add_table.get_children())
        for name, price in self.income_list:
            self.add_table.insert(
                '', tk.END,
                values=(name, price)
            )
        self.update_net_total()

    def update_add_table_2(self):
        self.add_table_2.delete(*self.add_table_2.get_children())
        for name, price in self.income_list_2:
            self.add_table_2.insert(
                '', tk.END,
                values=(name, price)
            )
        self.update_net_total_2()

    def remove_from_add_table(self, *args):
        selected_item = self.add_table.selection()
        if not selected_item:
            return None
        selected_item = selected_item[0]
        selected_tuple = self.add_table.item(selected_item).get("values", [None, 0])
        selected_tuple = (selected_tuple[0], float(selected_tuple[1]))
        if selected_tuple not in self.income_list:
            return None
        self.income_list.remove(selected_tuple)
        self.add_table.delete(selected_item)
        self.update_net_total()

    def remove_from_add_table_2(self, *args):
        selected_item = self.add_table_2.selection()
        if not selected_item:
            return None
        selected_item = selected_item[0]
        selected_tuple = self.add_table_2.item(selected_item).get("values", [None, 0])
        selected_tuple = (selected_tuple[0], float(selected_tuple[1]))
        if selected_tuple not in self.income_list_2:
            return None
        self.income_list_2.remove(selected_tuple)
        self.add_table_2.delete(selected_item)
        self.update_net_total_2()

    def update_net_total(self, *args):
        total = sum(price for _, price in self.income_list)
        try:
            discount = float(self.discount.get() or 0)
        except ValueError:
            discount = 0
        self.final_price.set(max((total - discount), 0))

    def update_net_total_2(self, *args):
        total = sum(price for _, price in self.income_list_2)
        try:
            discount = float(self.discount_2.get() or 0)
        except ValueError:
            discount = 0
        self.final_price_2.set(max((total - discount), 0))

    def save_income(self):
        customer_name = self.customer_name.get()
        income_list = self.income_list
        discount = self.discount.get()
        price = self.final_price.get()
        year = self.year.get()
        month = self.month.get()
        day = self.day.get()
        hour = self.hour.get()
        minute = self.minute.get()
        if not (income_list and price and year and month and day and hour and minute):
            messagebox.showwarning("Missing Values", "Values are Missing!")
            return None
        date = datetime(year, month, day, hour, minute)
        income_string = "||".join(f"{n}::{p}" for n, p in income_list)
        income.create(customer_name, income_string, discount, price, date)
        self.refresh()

    def update_income(self):
        id = self.id.get()
        customer_name = self.customer_name_2.get()
        income_list = self.income_list_2
        discount = self.discount_2.get()
        price = self.final_price_2.get()
        year = self.year.get()
        month = self.month.get()
        day = self.day.get()
        hour = self.hour.get()
        minute = self.minute.get()
        if not (income_list and price and year and month and day and hour and minute):
            messagebox.showwarning("Missing Values", "Values are Missing!")
            return None
        date = datetime(year, month, day, hour, minute)
        income_string = "||".join(f"{n}::{p}" for n, p in income_list)
        income.edit(id, customer_name, income_string, discount, price, date)
        self.refresh()

    def delete_income(self):
        income_id = self.id.get()
        if not income_id:
            return None
        confirmation = messagebox.askyesno("Are you sure?", f"Do you want to delete income of ID.{income_id}?")
        if not confirmation:
            return None
        income.del_res(income_id)
        self.refresh()

    def select_income(self, *args):
        selected_income = self.list_table.selection()
        if not selected_income:
            return None
        income_id = self.list_table.item(selected_income[0]).get("values", [None])[0]
        i = income.get_by_id(income_id)
        self.id.set(i.id)
        self.customer_name_2.set(i.customer_name)
        self.name_2.set("")
        self.price_2.set("")
        self.income_list_2 = []
        for single_entry in i.income_list.split("||"):
            n, p = single_entry.split("::")
            self.income_list_2.append((n, float(p)))
        self.discount_2.set(i.discount)
        self.final_price_2.set(i.price)
        self.year.set(i.date.year)
        self.month.set(i.date.month)
        self.day.set(i.date.day)
        self.hour.set(i.date.hour)
        self.minute.set(i.date.minute)
        self.update_add_table_2()
        self.detail_frame.tkraise()

    def update_table(self):
        incomes, income_count = income.get_paginated(self.page_no)
        self.total_pages = income_count // ROW_COUNT + 1
        self.page_no_label.config(text=f"{self.page_no}/{self.total_pages}")
        self.list_table.delete(*self.list_table.get_children())
        for row in incomes:
            income_list = row.income_list.split("||")
            income_name = ", ".join(i.split("::")[0] for i in income_list)
            self.list_table.insert(
                '', tk.END,
                values=(row.id, income_name, row.price, row.date)
            )

    def change_page(self, i: int):
        next_page_no = self.page_no + i
        if next_page_no in range(1, self.total_pages + 1):
            self.page_no = next_page_no
            self.update_table()

    def refresh(self):
        self.add_frame.tkraise()
        self.customer_name.set("")
        self.name.set("")
        self.price.set("")
        self.income_list = []
        self.discount.set("")
        self.final_price.set("")

        self.customer_name_2.set("")
        self.name_2.set("")
        self.price_2.set("")
        self.income_list_2 = []
        self.discount_2.set("")
        self.final_price_2.set("")

        current_time = datetime.now()
        self.year.set(current_time.year)
        self.month.set(current_time.month)
        self.day.set(current_time.day)
        self.hour.set(current_time.hour)
        self.minute.set(current_time.minute)

        self.page_no = 1
        self.update_table()
        self.update_add_table()
        self.update_add_table_2()
