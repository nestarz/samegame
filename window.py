#!/bin/python3

import tkinter as tk
from lib import game_frame as GAME

FPS = 30

class Window(tk.Tk):
    def __init__(self):
        """
        Définit une Window
        """

        tk.Tk.__init__(self)
        self.title("samegame")
        self.resizable(width=False, height=False)
        self.game = GAME.TkSameGameFrame()
        self.__do_run = True

    @property
    def do_run(self):
        return self.__do_run

    @do_run.setter
    def do_run(self, value=True):
        self.__do_run = value

    def run(self):
        """
        Lance le jeu
        """
        self.game.run()
        self.mainloop()
        while self.__do_run:
            self.after(FPS)
            self.do_run = False
        self.destroy()
