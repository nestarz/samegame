# ==============================================================================
"""SameGame: Untitled Project"""
# ==============================================================================
__author__ = "Seurin Mathieu and Rhouzlane Elias"
__version__ = "2.1"
__date__ = "2014-14-12"
# ==============================================================================
#!/bin/python3

from samegame.master import Master
from samegame import constants as c
from samegame.states import home, menu, game


def main():
    master = Master()
    state_dict = {c.HOME: home.Home(),
                  c.MAIN_MENU: menu.Main(),
                  c.SELECT_MODE: menu.ModeSelection(),
                  c.SELECT_LEVEL: menu.LevelSelection(),
                  c.ARCADE: game.Arcade()}
    master.setup_state(state_dict, c.HOME)
    master.main_loop()
    master.exit()

if __name__ == '__main__':
    main()
