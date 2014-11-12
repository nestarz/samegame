#!/bin/python3

#GAME CONFIG
NAME = "SAMEGAME"
AUTHOR = "Mathieu Seurin & Elias Rhouzlane"
SCREEN_HEIGHT = 574
SCREEN_WIDTH = 1024
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)

#STATES NAME
HOME = "home"
ARCADE = "arcade"
VERSUS = "versus"
SELECT_MODE = "mode_selection"
SELECT_CHAR = "character_selection"
MAIN_MENU = "main_menu"

#COLOR RGB
GREEN_RGB = (60, 191, 63)
YELLOW_RGB = (255, 215, 0)
RED_RGB = (255, 0, 0)
BLACK_RGB = (0, 0, 0)
WHITE_RGB = (255, 255, 255)
ORANGE_RGB = (255, 69, 0)
GREY_RGB = (170,170,170)
PINK_RGB = (240,240,240)
BLUE_RGB = (66,169,188)
PURPLE_RGB = (156,82,181)
MAROON_RGB = (118,93,48)

#STYLES
BTN = {
    "default": {
        "default": {
            "color": (255, 255, 255)
        },
        "hover": {
            "color": (253, 84, 72)
        },
        "size": 18,
        "font": 'joystix',
        "AA":1
    },
    "menu": {
        "default": {
            "color": (255, 255, 255)
        },
        "hover": {
            "color": (253, 84, 72)
        },
        "size": 27,
        "font": 'joystix',
        "AA":1,
        "bold":0
    }
}

#DIRECTIONS
STATIC = (0,0)
UP = (0,-1)
DOWN = (0,1)
RIGHT = (1,0)
LEFT = (-1,0)
UPRIGHT = (1,-1)
UPLEFT = (-1,-1)
DOWNRIGHT = (1,1)
DOWNLEFT = (-1,1)

