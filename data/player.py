import pygame as pg
from . import cache
from . import constants as c
from .graphics.sprites import Panel, BoardGFX, BlockGFX, CursorGFX, InfoGFX
from .gamecore import GameCore, Cursor

class Keys:
    def __init__(self, controls):
        self.UP = controls['UP']
        self.DOWN = controls['DOWN']
        self.RIGHT = controls['RIGHT']
        self.LEFT = controls['LEFT']
        self.SWAP = controls['SWAP']
        self.GENERATE = controls['GENERATE']

class Player:

    def __init__(self, index):
        self.index = index
        self.controls = c.CONTROLS[index]
        self.hidden_timer = 0

    def setup_game(self, board):
        self.alive = True
        self.actions = {}
        self.info_dict = {}
        self.pause = 0
        self.score = 0
        self.board = board
        self.cursor = self.board.cursor
        self.key = Keys(c.CONTROLS[self.index])
        self.board_group = pg.sprite.LayeredDirty()
        self.block_group = pg.sprite.LayeredDirty()
        self.cursor_group = pg.sprite.LayeredDirty()
        self.info_group = pg.sprite.LayeredDirty()
        self.setup_board()
        self.setup_blocks()
        self.setup_cursor()
        self.setup_input()

    def setup_board(self):

        # Create graphic board thanks to logic board
        self.board_gfx = BoardGFX(self.board)
        self.board_gfx.setup_effect('fadein', 1500)
        self.board_gfx.add(self.board_group)

    def setup_blocks(self):
        board = self.board
        for row in reversed(range(board.num_row)):
            for col in range(board.num_col):
                if board.board[row][col].color:
                    block = BlockGFX(board.board[row][col], self)
                    block.add(self.block_group)

    def setup_cursor(self):
        self.cursor_gfx = CursorGFX(self.cursor, self.board_gfx)
        self.cursor_gfx.add(self.cursor_group)

    def add_information(self, name, info=''):
        self.info_dict[name] = InfoGFX(name, info)
        self.info_dict[name].add(self.info_group)

    def update_information(self, name, info=''):
        self.info_dict[name].update_information(info)

    def setup_information(self):
        info_p = "{}: {}".format(self.index, c.PLAYER_NAME[self.index])
        info_s = "{}".format(c.MODE_NAME[self.speed])
        self.add_information('nom', info_p)
        self.add_information('mode', info_s)
        self.add_information('new_row')
        self.add_information('pause')
        self.add_information('score')

    def setup_input(self):
        self.actions[self.key.UP] = lambda: cursor.move_up()
        self.actions[self.key.DOWN] = lambda: cursor.move_down()
        self.actions[self.key.RIGHT] = lambda: cursor.move_right()
        self.actions[self.key.LEFT] = lambda: cursor.move_left()
        self.actions[self.key.SWAP] = lambda: self.swap()
        self.actions[self.key.GENERATE] = lambda: board.geneate()

    def check_input(self):
        pass

    def swap(self):
        case1, case2 = self.board.swap()

    def up_row(self, player, board):
        if board.top_row_empty():
            board.up()
            player.cursor.move_up()
            cases = board.generate_hidden()
            for c in cases:
                block = BlockGFX(c, player)
                block.add(player.blocks_gfx)
        else:
            player.alive = False
            self.info_list.add_information('alive', 'Game Over')

    @property
    def new_row_timer(self):
        return int((self.board.speed + self.pause - self.hidden_timer)/600)

    def game_event(self, elapsed, destroy):
        if destroy:
            self.pause += destroy*1000 #x blocks = x secondes
            self.score += destroy #x blocks = x points

        info_p = "Pause={}s".format(str(int((self.pause)/600)))
        info_r = "Up in {:.0f}s".format(self.new_row_timer)

        self.update_information('pause', info_p)
        self.update_information('new_row', info_r)

        if self.pause > 0:
            self.pause -= elapsed
        elif self.hidden_timer > self.board.speed:
            self.up_row()
            self.hidden_timer = 0
        else:
            self.hidden_timer += elapsed
            self.pause = 0

    def update(self, window, keys, elapsed):

        self.board.gravity()
        self.board.check_destroy()

        self.block_group.update(elapsed, self.board)
        self.cursor_group.update(elapsed, self.board)
        self.info_group.update(elapsed)

        rects = []
        rects += self.cursor_group.draw(window)
        rects += self.block_group.draw(window)
        rects += self.info_group.draw(window)

        destroy = self.board.destroy_block()
        self.board.gravity()

        self.game_event(elapsed, destroy)

        return self.rects
