import tkinter as tk

class TkSameGameFrame(tk.Frame):
    def run (self):
        self.init_widget()
        self.display_intro()

    def init_widget(self):
        # widget inits
        self.canvas = tk.Canvas(
            self,
            width=800,
            height=450,
        )
        self.canvas.pack()

    def display_intro(self):
        self.set_display('intro')
        #self.start_music()

    def set_display(self, sname):
        self.bg = tk.PhotoImage(file="data/images/{}.gif".format(sname))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg)
