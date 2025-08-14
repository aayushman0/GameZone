from tkinter import ttk, StringVar, messagebox
from db.orm import play_time
from datetime import datetime, timedelta
from template import Frame, DateClass, date_entry


class TimerFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(style="G.TFrame", padding=1)
        self.update_devices()

    def tk_vars(self):
        self.names = [StringVar(), StringVar(), StringVar(), StringVar()]
        self.dates = [DateClass(), DateClass(), DateClass(), DateClass()]
        self.max_time = [StringVar(), StringVar(), StringVar(), StringVar()]
        self.counter_type = [StringVar(), StringVar(), StringVar(), StringVar()]
        self.counter = [StringVar(), StringVar(), StringVar(), StringVar()]

    def main(self):
        timer_frame = [None, None, None, None]
        button_funcs = [self.button_1, self.button_2, self.button_3, self.button_4]
        for i in range(4):
            timer_frame[i] = ttk.Frame(self)
            timer_frame[i].configure(style="G.TFrame", padding=1)
            timer_frame[i].place(relx=i / 4, rely=0, relheight=1.0, relwidth=1 / 4)
            ttk.Label(timer_frame[i], textvariable=self.names[i], anchor="center").place(relx=0, rely=0, relwidth=1.0, relheight=0.25)
            date_frame = ttk.Frame(timer_frame[i])
            date_frame.place(relx=0, rely=0.25, relwidth=1.0, relheight=0.25)
            date_entry(self.dates[i], date_frame)
            button_frame = ttk.Frame(timer_frame[i])
            button_frame.columnconfigure(3, weight=1)
            button_frame.place(relx=0, rely=0.5, relwidth=1.0, relheight=0.25)
            ttk.Label(button_frame, text="Minutes:").grid(row=0, column=0, sticky="ew")
            ttk.Entry(button_frame, textvariable=self.max_time[i], width=10).grid(row=0, column=1, sticky="ew")
            ttk.Button(
                button_frame, text="Start / Stop", style="Confirm.TButton", command=button_funcs[i]
            ).grid(row=0, column=2, sticky="e")
            counter_frame = ttk.Frame(timer_frame[i])
            counter_frame.place(relx=0, rely=0.75, relwidth=1.0, relheight=0.25)
            ttk.Label(counter_frame, textvariable=self.counter_type[i]).place(relx=0, rely=0, relwidth=0.4, relheight=1.0)
            ttk.Label(counter_frame, textvariable=self.counter[i], anchor="center").place(relx=0.4, rely=0, relwidth=0.6, relheight=1.0)

    def button_1(self):
        self.button(0)

    def button_2(self):
        self.button(1)

    def button_3(self):
        self.button(2)

    def button_4(self):
        self.button(3)

    def button(self, i: int):
        year = self.dates[i].year.get()
        month = self.dates[i].month.get()
        day = self.dates[i].day.get()
        hour = self.dates[i].hour.get() or 0
        minute = self.dates[i].minute.get() or 0
        max_time = self.max_time[i].get() or 0
        if not (year and month and day):
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
        date = datetime(year, month, day, hour, minute)
        device = self.devices[i]
        play_time.edit(device.name, not device.is_running, date, max_time)
        self.update_devices()

    def update_devices(self):
        self.devices = play_time.get_all()[:4]

    def refresh(self):
        current_time = datetime.now()
        for i, device in enumerate(self.devices):
            self.names[i].set(device.name)
            self.dates[i].year.set(current_time.year)
            self.dates[i].month.set(current_time.month)
            self.dates[i].day.set(current_time.day)
            self.dates[i].hour.set(current_time.hour)
            self.dates[i].minute.set(current_time.minute)
            self.max_time[i].set("")

    def refresh_time(self):
        current_time = datetime.now()
        for i, device in enumerate(self.devices):
            if not device.is_running:
                self.counter_type[i].set("")
                self.counter[i].set("")
                continue
            if device.max_time:
                self.counter_type[i].set("Remaining Time:")
                final_time = device.start_time + timedelta(minutes=device.max_time)
                display_time: timedelta = final_time - current_time
            else:
                self.counter_type[i].set("Time Elapsed:")
                display_time: timedelta = current_time - device.start_time
            total_seconds = int(max(display_time.total_seconds(), 0))
            timer = f"{total_seconds//3600}:{(total_seconds//60) % 60}:{total_seconds % 60}"
            self.counter[i].set(timer)
        self.after(1000, self.refresh_time)
