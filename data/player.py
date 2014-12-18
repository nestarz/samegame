import pygame as pg
from . import cache
from . import constants as c
from .graphics.sprites import Panel, BlockGFX, CursorGFX, InfoGFX
from .gamecore import GameCore, Cursor

class Player:

    def __init__(self, index):
        self.index = index
        self.controls = c.CONTROLS[index]
        self.hidden_timer = 0

    def setup_game(self, board, board_gfx, keys):
        self.board = board
        self.cursor = self.board.cursor
        self.keys = keys
        self.board_gfx = board_gfx
        self.pause = 0
        self.blocks_gfx = pg.sprite.LayeredDirty()
        self.cursor_gfx = pg.sprite.LayeredDirty()
        self.info_gfx = pg.sprite.LayeredDirty()
        self.info = {}
        cursor = CursorGFX(self.cursor, board_gfx)
        cursor.add(self.cursor_gfx)
        self.alive = True
        self.score = 0
        self.setup_board()
        self.setup_blocks()
        self.setup_input()

    def setup_board(self, board):

        # Create graphic board thanks to logic board
        board = BoardGFX(board)
        board.setup_effect('fadein', 1500)
        board.add(self.boards_group)

    def setup_blocks(self):
        board = self.board
        for row in reversed(range(board.num_row)):
            for col in range(board.num_col):
                if board.board[row][col].color:
                    block = BlockGFX(board.board[row][col], self)
                    block.add(self.blocks_gfx)

    def setup_input(self, actions):
        actions[key.UP] = lambda: cursor.move_up()
        actions[key.DOWN] = lambda: cursor.move_down()
        actions[key.RIGHT] = lambda: cursor.move_right()
        actions[key.LEFT] = lambda: cursor.move_left()
        actions[key.SWAP] = lambda: self.swap()
        actions[key.GENERATE] = lambda: board.geneate()
        return actions

    def check_input(self):
        self.actions[key.UP] = lambda: cursor.move_up()
        self.actions[key.DOWN] = lambda: cursor.move_down()
        self.actions[key.RIGHT] = lambda: cursor.move_right()
        self.actions[key.LEFT] = lambda: cursor.move_left()

    def add_information(self, name, info=''):
        self.info_list[name] = InfoGFX(name, info)
        self.info_list[name].add(self.info_group)

    def update_information(self, name, info=''):
        self.info_list[name].update_information(info)

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

    def calc_new_row_timer(self):
        return int((self.game.speed + self.pause - self.hidden_timer)/600)

    def game_event(self, elapsed, player, board, destroy):
        if destroy:
            self.pause += destroy*1000 #x blocks = x secondes
            self.score += destroy #x blocks = x points

        info_p = "Pause={}s".format(str(int((self.pause)/600)))
        info_r = "Up in {:.0f}s".format(self.calc_new_row_timer())

        self.update_information('pause', info_p)
        self.update_information('new_row', info_r)

        if self.pause > 0:
            self.pause -= elapsed
        elif self.hidden_timer > self.game.speed:
            self.up_row()
            self.hidden_timer = 0
        else:
            self.hidden_timer += elapsed
            self.pause = 0

    def update(self, window, keys, elapsed):
        self.board.gravity()
        self.board.check_destroy()
        self.blocks_gfx.update(elapsed, board)
        self.cursor_gfx.update(elapsed, board)
        self.info_gfx.update(elapsed)
        self.rects += self.cursor_gfx.draw(window)
        self.rects += self.blocks_gfx.draw(window)
        self.rects += self.info_gfx.draw(window)
        destroy = self.board.destroy_block()
        self.board.gravity()
        self.game_event(elapsed, player, board, destroy)
