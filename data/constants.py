#!/bin/python3
from pygame import locals as pg

# GAME CONFIG
NAME = "SAMEGAME"
AUTHOR = "Mathieu Seurin & Elias Rhouzlane"
SCREEN_HEIGHT = 574
SCREEN_WIDTH = 1024
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# STATES NAME
HOME = "home"
ARCADE = "arcade"
VERSUS = "versus"
SELECT_MODE = "mode_selection"
SELECT_CHAR = "character_selection"
MAIN_MENU = "main_menu"

# COLOR RGB
GREEN_RGB = (60, 191, 63)
YELLOW_RGB = (255, 215, 0)
RED_RGB = (255, 0, 0)
BLACK_RGB = (0, 0, 0)
WHITE_RGB = (255, 255, 255)
ORANGE_RGB = (255, 69, 0)
GREY_RGB = (170, 170, 170)
PINK_RGB = (240, 240, 240)
BLUE_RGB = (66, 169, 188)
PURPLE_RGB = (156, 82, 181)
MAROON_RGB = (118, 93, 48)
COLORS_DICT = {
    "blue": BLUE_RGB,
    "green": GREEN_RGB,
    "orange": ORANGE_RGB,
    "grey": GREY_RGB,
    "purple": PURPLE_RGB,
    "yellow": YELLOW_RGB,
    "pink": PINK_RGB,
    "maroon": MAROON_RGB,
    "white": WHITE_RGB,
    "red": RED_RGB,
    "black": BLACK_RGB
}
# CONTROLS
PLAYER1_CONTROLS = {
    'UP': pg.K_UP,
    'DOWN': pg.K_DOWN,
    'LEFT': pg.K_LEFT,
    'RIGHT': pg.K_RIGHT,
    'SWAP': pg.K_RETURN,
    'GENERATE': pg.K_m
}

PLAYER2_CONTROLS = {
    'UP': pg.K_w,
    'DOWN': pg.K_s,
    'LEFT': pg.K_a,
    'RIGHT': pg.K_d,
    'SWAP': pg.K_SPACE,
    'GENERATE': pg.K_r
}
CONTROLS = [PLAYER1_CONTROLS, PLAYER2_CONTROLS]
# STYLES
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
        "AA": 1,
        "bold": 0
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
        "AA": 1,
        "bold": 0
    }
}

# DIRECTIONS
STATIC = (0, 0)
UP = (0, -1)
DOWN = (0, 1)
RIGHT = (1, 0)
LEFT = (-1, 0)
UPRIGHT = (1, -1)
UPLEFT = (-1, -1)
DOWNRIGHT = (1, 1)
DOWNLEFT = (-1, 1)
