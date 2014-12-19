#!/bin/python3
from pygame import locals as pg

# GAME CONFIG
NAME = "SAMEGAME"
AUTHOR = "Mathieu Seurin", "Elias Rhouzlane"
SCREEN_HEIGHT = 574
SCREEN_WIDTH = 1024
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# TIME CONSTANTS
BG_FADE_TIME = 800
BLINK_DURATION = 140
DYING_TIMER = 1700

# CONTROLS
PLAYER1_CONTROLS = {
    'UP': pg.K_w,
    'DOWN': pg.K_s,
    'LEFT': pg.K_a,
    'RIGHT': pg.K_d,
    'SWAP': pg.K_SPACE,
    'GENERATE': pg.K_r
}
PLAYER2_CONTROLS = {
    'UP': pg.K_UP,
    'DOWN': pg.K_DOWN,
    'LEFT': pg.K_LEFT,
    'RIGHT': pg.K_RIGHT,
    'SWAP': pg.K_RETURN,
    'GENERATE': pg.K_RSHIFT
}
CONTROLS = {0: PLAYER1_CONTROLS, 1: PLAYER2_CONTROLS}

# STATES NAME (SAME AS STATES'S BACKGROUND FILENAME)
HOME = "home"
ARCADE = "arcade"
VERSUS = "versus"
SELECT_MODE = "mode_selection"
SELECT_LEVEL = "level_selection"
SELECT_CHAR = "character_selection"
MAIN_MENU = "main_menu"

# STATES DESCRIPTION
MAIN_MENU_DESCRIPTION = "Main Menu"
SELECT_MODE_DESCRIPTION = "Select your mode"
SELECT_LEVEL_DESCRIPTION = "Choose your skill"
SELECT_CHAR_DESCRIPTION = "Choose your hero"

# GFX_NAME
LOGOGFXNAME = 'logo'
BOARD_GFX_NAME = {0: 'board1', 1: 'board2'}

## TEXT
SUBLOGO_TEXT = "Mathieu Seurin & Rhouzlane Elias"
START_TEXT = 'Press Start Button'
# BTN TEXT
BTN_TEXT_CONTINUE = "Continue"
BTN_TEXT_NEWGAME = "New Game"
BTN_TEXT_LOADGAME = "Load Game"
BTN_TEXT_BACK = "Back"
BTN_TEXT_QUIT = "Quit"
BTN_TEXT_EASY = "Easy"
BTN_TEXT_NORMAL = "Normal"
BTN_TEXT_HARD = "Hard"
BTN_TEXT_INFERNO = "Inferno"
BTN_TEXT_DEV = "Developper"
BTN_TEXT_1P = "1Player"
BTN_TEXT_2P = "2Player"

#PARTY TEXT
PLAYER_NAME = {0: "P1", 1: "P2"}
SPEED = {1:11000, 2:8000, 3:7000, 4:5000}
MODE_NAME_TUPLE = (
    (SPEED[1], BTN_TEXT_EASY),
    (SPEED[2], BTN_TEXT_NORMAL),
    (SPEED[3], BTN_TEXT_HARD),
    (SPEED[4], BTN_TEXT_INFERNO),
)
MODE_NAME_DICT = {s:btn for s,btn in MODE_NAME_TUPLE}

# FONT
FONT1 = 'joystix'
FONT2 = 'larabiefont'

# COLOR RGB
GREEN_RGB = (60, 191, 63)
YELLOW_RGB = (255, 215, 0)
RED_RGB = (255, 0, 0)
BLACK_RGB = (0, 0, 0)
WHITE_RGB = (255, 255, 255)
ORANGE_RGB = (253, 84, 72)
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

# STYLES
DEFAULT_BTN_STYLE = {
    "color1": (255, 255, 255),
    "color2": (253, 84, 72),
    "size": 18,
    "font": 'joystix',
    "AA": 1,
    "bold": 0
}
MENU_BTN_STYLE = {
    "color1": (255, 255, 255),
    "color2": (253, 84, 72),
    "size": 27,
    "font": 'joystix',
    "AA": 1,
    "bold": 0
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
