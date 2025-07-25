import tkinter as tk
from tkinter import ttk, IntVar


class Frame(ttk.Frame):
    def __init__(self, master: tk.Tk | ttk.Frame):
        super().__init__(master)
        self._i: int = 0
        self.page_no: int = 1
        self.total_pages: int = 1
        self.prev_frame: ttk.Frame = None
        self.year = IntVar()
        self.month = IntVar()
        self.day = IntVar()
        self.hour = IntVar()
        self.minute = IntVar()
        self.tk_vars()
        self.add_frame = ttk.Frame(self)
        self.add_frame.columnconfigure(1, weight=1)
        self.add_frame.place(relx=0, rely=0, relwidth=0.3, relheight=1.0)
        self.detail_frame = ttk.Frame(self)
        self.detail_frame.columnconfigure(1, weight=1)
        self.detail_frame.place(relx=0, rely=0, relwidth=0.3, relheight=1.0)
        self.list_frame = ttk.Frame(self)
        self.list_frame.place(relx=0.3, rely=0, relwidth=0.7, relheight=1.0)
        self.main()
        self.events()
        self.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)

    @property
    def i(self) -> int:
        self._i += 1
        return self._i - 1

    @i.setter
    def i(self, x) -> None:
        self._i = x

    def tk_vars(self) -> None:
        pass

    def main(self) -> None:
        pass

    def events(self) -> None:
        pass

    def refresh(self) -> None:
        pass

    def set_active(self) -> None:
        self.tkraise()
        self.refresh()


class DateClass:
    def __init__(self):
        self.year = IntVar()
        self.month = IntVar()
        self.day = IntVar()
        self.hour = IntVar()
        self.minute = IntVar()


def date_entry(cls, frame: ttk.Frame):
    frame.columnconfigure((0, 2, 4, 6, 8), weight=1)
    ttk.Spinbox(frame, textvariable=cls.year, from_=2000, to=2999, justify="right", width=22).grid(row=0, column=0, sticky="ew")
    ttk.Label(frame, text="/").grid(row=0, column=1)
    ttk.Spinbox(frame, textvariable=cls.month, from_=1, to=12, justify="center").grid(row=0, column=2)
    ttk.Label(frame, text="/").grid(row=0, column=3)
    ttk.Spinbox(frame, textvariable=cls.day, from_=1, to=32).grid(row=0, column=4)
    ttk.Label(frame, text="  ").grid(row=0, column=5)
    ttk.Spinbox(frame, textvariable=cls.hour, from_=0, to=23, justify="right").grid(row=0, column=6)
    ttk.Label(frame, text=":").grid(row=0, column=7)
    ttk.Spinbox(frame, textvariable=cls.minute, from_=0, to=59).grid(row=0, column=8)
