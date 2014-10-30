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
MAIN_MENU = "main_menu"

#COLOR RGB
GREEN_RGB = (0, 255, 0)
YELLOW_RGB = (255, 215, 0)
RED_RGB = (255, 0, 0)
BLACK_RGB = (0, 0, 0)
WHITE_RGB = (255, 255, 255)
ORANGE_RGB = (255, 69, 0)
GREY_RGB = (240,240,240)
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
        "size": 33,
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

#TEXT EFFECTS
EFFECT = {
    'blink': {
        'name': 'blink',
        'delay': 15
    },
    'fadein200': {
        'name': 'fadein',
        'delay': 200,
        'set_alpha':False
    },
    'fadein100': {
        'name': 'fadein',
        'delay': 100,
        'set_alpha':False
    },
    'fadein50': {
        'name': 'fadein',
        'delay': 50,
        'set_alpha':False
    },
    'fadein10': {
        'name': 'fadein',
        'delay': 10,
        'set_alpha':False
    },
    'moveup50': {
        'name': 'move',
        'delay': 50,
        'direction': UP
    },
    'moveup25': {
        'name': 'move',
        'delay': 25,
        'direction': UP
    },
    'wait35': {
        'name': 'wait',
        'delay': 35
    },
    'wait25': {
        'name': 'wait',
        'delay': 25
    },
    'shake50': {
        'name': 'shake',
        'delay': 50
    }
}
