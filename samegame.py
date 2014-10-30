# ==============================================================================
"""SameGame : Untitled Project"""
# ==============================================================================
__author__  = "Seurin Mathieu and Rhouzlane Elias"
__version__ = "1.0"
__date__    = "2014-22-11"
# ==============================================================================
#!/bin/python3

from data import cache
from data.master import Master
from data import constants as c
from data import home, menu, party, gamecore

def main():
    master = Master()
    cache.init_cache()
    state_dict = {c.HOME : home.Home(),
                  c.ARCADE : party.Party(),
                  c.MAIN_MENU: menu.MainMenu()}
    master.setup_state(state_dict, c.HOME)
    master.main_loop()
    master.exit()

if __name__=='__main__':
    main()



