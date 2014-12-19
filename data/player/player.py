import pygame as pg
from .. import cache
from .. import constants as c
from ..graphics.sprites import Panel, BoardGFX, BlockGFX, CursorGFX, InformationGFX
from ..gamecore import GameCore, Cursor
from ..player.player_tools import *

class Player:

    def __init__(self, index):
        assert index in [0,1]
        self.index = index
        self.actions = {}
        self.alive = True
        self.up_timer = 0
        self.pause_timer = 0
        self.input_timer = 0
        self.score = 0

    def setup_game(self, board, panel):
        self.board = board
        self.cursor = self.board.cursor
        self.controls = c.CONTROLS[self.index]
        self.name = c.PLAYER_NAME[self.index]
        self.key = Keys(c.CONTROLS[self.index])
        self.board_group = pg.sprite.LayeredDirty()
        self.block_group = pg.sprite.LayeredDirty()
        self.cursor_group = pg.sprite.LayeredDirty()
        self.information_group = pg.sprite.LayeredDirty()
        self.all_groups = (self.board_group,
                            self.cursor_group,
                            self.block_group,
                            self.cursor_group,
                            self.information_group)
        self.setup_board(panel)
        self.setup_blocks()
        self.setup_cursor()
        self.setup_information()
        self.setup_input()

    def setup_board(self, panel):

        # Create graphic board thanks to logic board
        # Then add this board to LayeredDirty group
        self.board_gfx = BoardGFX(self.board, self.index, panel)
        self.board_gfx.setup_effect('fadein', 1500)
        self.board_gfx.add(self.board_group)

    def setup_blocks(self):

        # Create block for each filled case in logic board
        # Then add them to LayeredDirty group
        board = self.board
        for row in reversed(range(board.num_row)):
            for col in range(board.num_col):
                if board.board[row][col].color:
                    block = BlockGFX(board.board[row][col], self)
                    block.add(self.block_group)
                    self.board_gfx.array[block.pos[0]][block.pos[1]] = block

    def setup_cursor(self):

        # Create cursor from logic cursor taken from board
        # Then add it to his own LayeredDirty group
        self.cursor_gfx = CursorGFX(self.cursor, self.board_gfx)
        self.cursor_gfx.add(self.cursor_group)

    def add_information(self, information):

        # Create interface for logic information object parameter
        info_gfx = InformationGFX(information)
        info_gfx.add(self.information_group)

    def setup_information(self):

        # -- Create useful information boxes for player --
        # Each Information object are taken from player_tools.py
        # They get a reference from whole player in order
        # to do easy update
        self.add_information(NameInformation(self))
        self.add_information(ModeInformation(self))
        self.add_information(UpInformation(self))
        self.add_information(PauseInformation(self))
        self.add_information(ScoreInformation(self))

    def setup_input(self):
        self.actions[self.key.UP] = lambda: self.cursor.move_up()
        self.actions[self.key.DOWN] = lambda: self.cursor.move_down()
        self.actions[self.key.RIGHT] = lambda: self.cursor.move_right()
        self.actions[self.key.LEFT] = lambda: self.cursor.move_left()
        self.actions[self.key.SWAP] = lambda: self.swap()
        self.actions[self.key.GENERATE] = lambda: self.up_row()

    def check_input(self, keys, elapsed):
        """ Check for user events """

        # Check 70ms after last key press if self.actions keys
        # are pressed then launches the corresponding action
        if self.input_timer > 300:
            for index, function in self.actions.items():
                if keys[index]:
                    function()
                    self.input_timer = 0
        self.input_timer += elapsed

    def swap(self):

        # Order to logic board to swap case focused by cursor (internal process)
        case1, case2 = self.board.swap()
        case1.on_swap = True
        case2.on_swap = True

    def up_row(self):

        # Check if top row is empty, if True, player loses the game
        game_over = not self.board.top_row_empty()

        if game_over and self.alive:
            self.add_information(GameOverInformation(self))
            self.alive = False
        else:
            self.board.up()
            self.cursor.move_up()
            cases = self.board.generate_hidden()
            for case in cases:
                block = BlockGFX(case, self)
                block.add(self.block_group)
                self.board_gfx.array[case.pos[0]][case.pos[1]] = block

    @property
    def new_row_timer(self):
        return int((self.board.speed + self.pause_timer - self.up_timer)/600)

    def game_event(self, elapsed, destroy):
        if destroy:
            self.pause_timer += destroy*1000 #x blocks = x secondes
            self.score += destroy #x blocks = x points
        if self.pause_timer > 0:
            self.pause_timer -= elapsed
        elif self.up_timer > self.board.speed:
            self.up_row()
            self.up_timer = 0
        else:
            self.up_timer += elapsed
            self.pause_timer = 0

    def update(self, panel, keys, elapsed):
        if self.alive:
            self.check_input(keys, elapsed)
        self.board.gravity()
        destroyed, nb_destroyed = self.board.check_destroy()
        self.board_group.update(elapsed, panel)
        self.information_group.update(elapsed, self)
        self.block_group.update(elapsed, self, destroyed)
        self.cursor_group.update(elapsed, self)
        if self.alive:
            self.game_event(elapsed, nb_destroyed)
        self.board.destroy_block()
        self.board.gravity()
        return self.all_groups
