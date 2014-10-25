#!/bin/python3

#GAME CONFIG
NAME = "SAMEGAME"
SCREEN_HEIGHT = 574
SCREEN_WIDTH = 1024
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)

#STATES NAME
HOME_SCREEN = "home screen"
PARTY = "party"

GREEN_RGB = (0, 255, 0)
YELLOW_RGB = (255, 215, 0)
RED_RGB = (255, 0, 0)
BLACK_RGB = (0, 0, 0)
ORANGE_RGB = (255, 69, 0)

BUTTON_STYLE = {
    "default": {
        "default": {
            "text_color": (255, 255, 255)
        },
        "hover": {
            "text_color": (253, 84, 72)
        },
        "fontsize": 26,
        "fontname": 'joystix'
    }
}
