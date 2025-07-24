import tkinter as tk
from tkinter import ttk, StringVar, BooleanVar, messagebox
from db.orm import play_time
from datetime import datetime
from template import Frame, date_entry
from variables import ROW_COUNT


class DeviceFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(style="G.TFrame", padding=1)

    def tk_vars(self):
        self.table_columns = ("Name", "Status", "Start Time", "Max Time")
        self.table_columns_width = (300, 70, 100, 100)
        self.table_columns_align = ("w", "e", "e", "e")
        self.name = StringVar()
        self.old_name = StringVar()
        self.new_name = StringVar()
        self.is_running = BooleanVar()
        self.max_time = StringVar()

    def main(self):
        ttk.Label(self.add_frame, text="Name:").grid(row=0, column=0, sticky="e", pady=10)
        ttk.Entry(self.add_frame, textvariable=self.name).grid(row=0, column=1, sticky="ew")
        ttk.Button(
            self.add_frame, text="Add Device", style="Confirm.TButton", command=self.save_device
        ).grid(
            row=1, column=0, columnspan=2, sticky="ew", ipady=10
        )

        self.list_table = ttk.Treeview(self.list_frame, show="headings", selectmode="browse", columns=self.table_columns, height=ROW_COUNT)
        for col_name, col_width, col_align in zip(self.table_columns, self.table_columns_width, self.table_columns_align):
            self.list_table.heading(col_name, text=col_name)
            self.list_table.column(col_name, width=col_width, anchor=col_align)
        self.list_table.place(relx=0, rely=0, relwidth=1.0, relheight=0.93)

        ttk.Label(self.detail_frame, text="Name:").grid(row=self.i, column=0, sticky="e", pady=10)
        ttk.Label(self.detail_frame, text="New Name:").grid(row=self.i, column=0, sticky="e", pady=10)
        ttk.Label(self.detail_frame, text="Status:").grid(row=self.i, column=0, sticky="e", pady=10)
        ttk.Label(self.detail_frame, text="Start Time:").grid(row=self.i, column=0, sticky="e", pady=10)
        ttk.Label(self.detail_frame, text="Max Time:").grid(row=self.i, column=0, sticky="e", pady=10)
        self.i = 0
        ttk.Entry(self.detail_frame, textvariable=self.old_name, state="readonly").grid(row=self.i, column=1, sticky="ew")
        ttk.Entry(self.detail_frame, textvariable=self.new_name).grid(row=self.i, column=1, sticky="ew")
        ttk.Checkbutton(self.detail_frame, variable=self.is_running).grid(row=self.i, column=1, sticky="ew")
        date_frame_2 = ttk.Frame(self.detail_frame)
        date_frame_2.grid(row=self.i, column=1, sticky="w")
        date_entry(self, date_frame_2)
        ttk.Entry(self.detail_frame, textvariable=self.max_time).grid(row=self.i, column=1, sticky="ew")
        ttk.Button(
            self.detail_frame, text="Update Expense", style="Confirm.TButton", command=self.update_device
        ).grid(
            row=self.i, column=0, columnspan=2, sticky="ew", ipady=10
        )
        ttk.Button(
            self.detail_frame, text="Delete Expense", style="Delete.TButton", command=self.delete_device
        ).grid(
            row=self.i, column=0, columnspan=2, sticky="ew", ipady=10
        )

    def events(self):
        self.list_table.bind("<Double-Button-1>", self.select_device)

    def save_device(self):
        name = self.name.get()
        if not name:
            messagebox.showwarning("Missing Values", "Values are Missing!")
            return None
        play_time.create(name, False, datetime.now(), 0)
        self.refresh()

    def update_device(self):
        name = self.old_name.get()
        new_name = self.new_name.get()
        is_running = self.is_running.get()
        year = self.year.get()
        month = self.month.get()
        day = self.day.get()
        hour = self.hour.get()
        minute = self.minute.get()
        max_time = self.max_time.get()
        if not (name and year and month and day):
            messagebox.showwarning("Missing Values", "Values are Missing!")
            return None
        try:
            int(year)
            int(month)
            int(day)
            int(hour)
            int(minute)
            int(max_time)
        except ValueError:
            messagebox.showwarning("Wrong Type", "String used instead of numbers!")
            return None
        start_time = datetime(year, month, day, hour, minute)
        play_time.edit(name, is_running, start_time, max_time, new_name)
        self.refresh()

    def delete_device(self):
        name = self.old_name.get()
        if not name:
            return None
        confirmation = messagebox.askyesno("Are you sure?", f"Do you want to delete device: {name}?")
        if not confirmation:
            return None
        play_time.delete(name)
        self.refresh()

    def select_device(self, *args):
        selected_device = self.list_table.selection()
        if not selected_device:
            return None
        device_name = self.list_table.item(selected_device[0], ).get("values", [None])[0]
        d = play_time.get_by_name(device_name)
        self.old_name.set(d.name)
        self.is_running.set(d.is_running)
        self.year.set(d.start_time.year)
        self.month.set(d.start_time.month)
        self.day.set(d.start_time.day)
        self.hour.set(d.start_time.hour)
        self.minute.set(d.start_time.minute)
        self.max_time.set(d.max_time)
        self.detail_frame.tkraise()

    def update_table(self):
        devices = play_time.get_all()
        self.list_table.delete(*self.list_table.get_children())
        for row in devices:
            self.list_table.insert(
                '', tk.END,
                values=(row.name, row.is_running, row.start_time, row.max_time)
            )

    def refresh(self):
        self.add_frame.tkraise()
        self.name.set("")
        self.new_name.set("")

        self.page_no = 1
        self.update_table()
