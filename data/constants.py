#!/bin/python3

#GAME CONFIG
NAME = "SAMEGAME"
AUTHOR = "Mathieu Seurin & Rhouzlane Elias"
SCREEN_HEIGHT = 574
SCREEN_WIDTH = 1024
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)

#STATES NAME
HOME = "home"
PARTY = "party"
MAIN_MENU = "main_menu"

#COLOR RGB
GREEN_RGB = (0, 255, 0)
YELLOW_RGB = (255, 215, 0)
RED_RGB = (255, 0, 0)
BLACK_RGB = (0, 0, 0)
WHITE_RGB = (255, 255, 255)
ORANGE_RGB = (255, 69, 0)

#STYLES
BUTTON_STYLE = {
    "default": {
        "default": {
            "textcolor": (255, 255, 255)
        },
        "hover": {
            "textcolor": (253, 84, 72)
        },
        "fontsize": 18,
        "fontname": 'joystix'
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

#TEXT EFFECTS
EFFECT = {
    'blink': {
        'name': 'blink',
        'delay': 15
    },
    'fadein200': {
        'name': 'fadein',
        'delay': 200
    },
    'fadein100': {
        'name': 'fadein',
        'delay': 100
    },
    'fadein50': {
        'name': 'fadein',
        'delay': 50
    },
    'fadein10': {
        'name': 'fadein',
        'delay': 10
    },
    'moveup50': {
        'name': 'move',
        'delay': 50,
        'direction': UP
    },
    'wait50': {
        'name': 'wait',
        'delay': 50
    },
    'shake50': {
        'name': 'shake',
        'delay': 50
    }
}
