#!/bin/python3

import pygame as pg
from . import setup
from . import state

class Master(setup.Window):
    def __init__(self):
        setup.Window.__init__(self)
        self.done = False                       #etat du programme
        self.clock = pg.time.Clock()            #horloge du programme
        self.fps = 30                           #frequence d'update
        self.current_time = 0.0                 #valeur du chronometre
        self.state = state.State()              #Debug
        #TODO : hierarchiser les etats

    def update(self):
        """Met a jour le programme"""
        self.current_time = pg.time.get_ticks() #maj du chronometre
        if self.state.quit:         #check si le prog doit se terminer
            self.done = True        #le prog est termine
        elif self.state.done:       #check si l'etat doit terminer
            self.flip_state()       #changement d'etat
        self.state.update()         #maj de l'etat

    def main(self):
        """Boucle principale du programme"""
        while not self.done:
            self.update()               #maj du prog
            pg.display.update()         #maj de la fenetre
            self.clock.tick(self.fps)   #si self.fps non depasse, attend

    def flip_state(self):
        """Change l'etat du programme"""
        pass
        #TODO : Changement d'etat
