# ==============================================================================
"""SameGame : Untitled Project"""
# ==============================================================================
__author__  = "Seurin Mathieu and Rhouzlane Elias"
__version__ = "1.0"
__date__    = "2014-22-11"
# ==============================================================================
#!/bin/python3

import sys
import pygame

from data.master import Master

def main():
    master = Master()
    master.main()

if __name__=='__main__':
    main()
    pygame.quit()
    sys.exit()
