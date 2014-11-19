#!/bin/python3
# -*- coding: utf-8 -*-
# ======================================================================
# ======================================================================

"""SameGame : Untitled Project"""

__author__ = 'Seurin Mathieu and Rhouzlane Elias'
__version__ = '1.0'
__date__ = '2014-22-11'

# ======================================================================

from data import cache
from data.master import Master
from data import constants as c
from data import home, menu, party


def main():
    master = Master()
    cache.init_cache()
    state_dict = {
        c.HOME: home.Home(),
        c.MAIN_MENU: menu.Main(),
        c.SELECT_MODE: menu.ModeSelection(),
        c.SELECT_CHAR: menu.CharacterSelection(),
        c.ARCADE: party.Arcade(),
        }
    master.setup_state(state_dict, c.ARCADE)
    master.main_loop()
    master.exit()


if __name__ == '__main__':
    main()



