#!/bin/python3

from tkinter import *

class Window(Tk):
    def __init__(self):
        """
        Définit une Window
        """

        Tk.__init__(self)
        self.title("Spiro")
        self.resizable(width=False, height=False)

    def run(self):
        """
        Lance le jeu
        """
        self.mainloop()
