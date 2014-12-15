# ==============================================================================
"""SameGame : Untitled Project"""
# ==============================================================================
__author__  = "Seurin Mathieu and Rhouzlane Elias"
__version__ = "2.0"
__date__    = "2014-14-12"
# ==============================================================================
#!/bin/python3

from data import cache
from data.master import Master
from data import constants as c
from data import home, menu, party

def main():
    
    master = Master() #Controleur du programme
    #Initialisation du cache avec récupération des ressources
    cache.init_cache() 
    state_dict = {c.HOME : home.Home(),
                  c.MAIN_MENU : menu.Main(),
                  c.SELECT_MODE : menu.ModeSelection(),
                  c.SELECT_CHAR : menu.CharacterSelection(),
                  c.ARCADE : party.Arcade()}
    #initalise les écrans du jeu et définit l'écran principal
    master.setup_state(state_dict, c.HOME)
    master.main_loop() #lancement du jeu et de la boucle principale
    master.exit() #sortie du jeu

if __name__=='__main__':
    main()
