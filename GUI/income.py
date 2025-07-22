from template import Frame


class IncomeFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(style="G.TFrame", padding=1)
