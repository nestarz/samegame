#!/bin/python3
# -*- coding: utf-8 -*-

import pygame as pg
from samegame.graphics.gfx import SuperSurface
from samegame.graphics.general_sprites import Sprite
from samegame.tools import render_text
from samegame import constants as c


class InformationGFX(Sprite):

    def __init__(self, information_obj):
        pg.sprite.DirtySprite.__init__(self)
        player = information_obj.player
        self.information_obj = information_obj
        self.index = player.index
        self.height = sum([spr.rect.h for spr in player.information_group])
        self.style = information_obj.style
        self.text = information_obj.text
        self.size = information_obj.size
        ref = render_text(self.text, self.size, style=self.style)
        SuperSurface.__init__(self, ref)
        self.position_information(player.board_gfx)

    def position_information(self, board_gfx):
        RECT_PLAYER_1 = board_gfx.rect.right + 10
        RECT_PLAYER_2 = board_gfx.rect.left - self.rect.w - 10
        self.rect.x = RECT_PLAYER_2 if self.index else RECT_PLAYER_1
        self.rect.y = board_gfx.rect.top + self.rect.h + self.height + 10

    def change_text(self, text):
        if self.text != text:
            self.image = render_text(text, self.size, style=self.style)
            self.rect.size = self.image.get_rect().size
            self.text = text

    def update(self, elapsed, player):
        self.information_obj.update()
        self.change_text(self.information_obj.text)
        self.position_information(player.board_gfx)
        self.dirty = 1
        Sprite.update(self, elapsed)


class CursorGFX(Sprite):
    SIZE = (43*2+1, 42+2)

    def __init__(self, cursor, board_gfx):

        # call DirtySprite initializer
        pg.sprite.DirtySprite.__init__(self)

        # Create SuperSurface with CursorGFX size
        ref = pg.Surface(CursorGFX.SIZE, pg.HWSURFACE | pg.SRCALPHA)
        SuperSurface.__init__(self, ref)

        # Draw a rect with white 5px border size (not filled)
        pg.draw.rect(self.image, (255, 255, 255), self.rect, 5)
        self.image = self.image.convert()

        # Reference to logic cursor
        self.cursor = cursor

        # Deep copy cursor position
        # Its not a reference to cursor positon, in order to handle move
        self.pos_row = cursor.pos_row
        self.pos_col = cursor.pos_col

        # Positionning cursor relative to board
        self.position(board_gfx)

    def position(self, surface):
        """ Positioning cursor relative to a surface """

        # Cursor will be positioned to focus a block
        self.rect.bottom = surface.rect.bottom - (self.cursor.pos_row*43 + 2)
        self.rect.x = 2 + surface.rect.x + self.cursor.pos_col*43

    def move(self):

        # Create cursor shortcut
        cursor = self.cursor

        # If cursor is moving on the vertical axis
        if cursor.pos_col-self.pos_col != 0:
            self.rect.move_ip(43*(cursor.pos_col-self.pos_col), 0)
            #self.setup_effect('move', 50, (43*(cursor.pos_col-self.pos_col), 0), 1)

        # If cursor is moving on the vertical axis
        if cursor.pos_row-self.pos_row != 0:
            self.rect.move_ip(0, -43*(cursor.pos_row-self.pos_row))
            #self.setup_effect('move', 50, (0, -43*(cursor.pos_row-self.pos_row)), 1)

        # Update gfx cursor position to correspond
        # with logic cursor position in the logic board
        self.pos_row, self.pos_col = cursor.pos_row, cursor.pos_col

    def update(self, elapsed, player):
        Sprite.update(self, elapsed)
        self.move()
        if not player.alive:
            self.image.set_alpha(70)
        self.dirty = 1


class BlockGFX(Sprite):
    """ Bloc de couleur """

    W, H = 38, 38
    size = (W, H)

    def __init__(self, case, player):
        pg.sprite.DirtySprite.__init__(self)
        ref = pg.Surface(BlockGFX.size, pg.HWSURFACE | pg.SRCALPHA)
        SuperSurface.__init__(self, ref)
        self.player = player
        self.image.fill(c.COLORS_DICT[case.color] + (245,))
        self.image = self.image.convert()
        self.board_gfx = player.board_gfx
        self.cell = case
        self.pos = case.pos
        self.set_position(player.board_gfx)
        self.time_stacker = 0
        self.alive = True
        self.cell.dying = False
        self.dying_time = 0
        self.frozen = False

    def set_position(self, surface):
        """ Positioning block relative to a surface """

        # Blocks will be positioned in the bottom of the surface
        self.rect.bottom = surface.rect.bottom - (self.pos[0]*43 + 5)
        self.rect.x = 5 + surface.rect.x + self.pos[1]*43

    def color_update(self):

        # If player is not alive, we set a transparency effect on the block
        if not self.player.alive:
            self.image.set_alpha(70)
        # Else if block is alive and not dying
        elif self.alive and not self.cell.dying:
            # If case is in the hidden row, we set a special alpha on the block
            if self.cell.pos[0] == 0:
                self.image.set_alpha(110)
            else:
                self.image.set_alpha(255)

    def is_block_dying(self, dying_cases):

        # For each list of dying cases coordinates
        # check if case position of the block is inside
        # If true, we apply a blink effect on the block
        # and init a dying timer (timer done will kill the block)
        # Then we freeze all blocks in the same column of the dying case
        # for the same duration of dying (for readability purpose)
        for line in dying_cases:
            if self.cell.pos in line:

                # Dying constants (from constants.py)
                BLINK_DURATION = c.BLINK_DURATION
                DYING_TIMER = c.DYING_TIMER

                # Apply blink effect with a duration
                self.setup_effect('blink', BLINK_DURATION)

                # Set the dying timer
                self.dying_timer = DYING_TIMER

                # Freeze all cases in the same col as dying case (dying case included)
                self.board_gfx.freeze_col(self.cell.pos[1], self.dying_timer)

                # Yes, the case is dying
                return True

        # No, the case is not about to be destroyed, it is not dying
        return False

    def move(self):

        # Create shortcut
        cell = self.cell

        # If case is moving on the vertical axis
        if cell.pos[1]-self.pos[1] != 0:
            #self.rect.move_ip(43*(case.pos[1]-self.pos[1]), 0)
            self.setup_effect('move', 70, (43*(cell.pos[1]-self.pos[1]), 0), 1)

        # If case is moving on the vertical axis
        if cell.pos[0]-self.pos[0] != 0:
            #self.rect.move_ip(0, -43*(case.pos[0]-self.pos[0]))
            self.setup_effect('move', 70, (0, -43*(cell.pos[0]-self.pos[0])), 1)

        # Update block position to correspond
        # with case position in the logic board
        self.pos = cell.pos

    def update(self, elapsed, player, dying_blocks):

        # Update block color relative to game state
        self.color_update()

        # Must respect some rules to move:
        # - Block must be alive and not dying (for blink effect)
        # - Block must (not be frozen or must be on swap)
        #   OR (must be dying and frozen)
        # If dying, we update timer until fixed duration (blink effect duration)
        # then we kill the block, it will not be updated after this
        if self.alive and not self.cell.dying:

            # Check if block is in dying blocks (get from logic board process)
            # Note : dying blocks is a list of coordinate list (2 dimensions)
            self.cell.dying = self.is_block_dying(dying_blocks)

            # If case is swapping, or if case is
            # not frozen, we try to move the block (if needed)
            # We do the same if block is dying AND frozen (for gravity purpose)
            if self.cell.on_swap or not self.cell.frozen:
                self.move()
            elif self.cell.dying and self.cell.frozen:
                self.move()

        elif self.dying_timer < 0:

            # Kill the sprite, will ne longer be updated
            # It remove itself from groups
            self.kill()

            # The case is no more dying nor alive (it is dead)
            self.cell.dying = False
            self.alive = False

        elif self.cell.dying:

            # If case is still in the process of
            # dying, we decrease the dying timer
            self.dying_timer -= elapsed

        # Update the sprite (apply effects if needed)
        Sprite.update(self, elapsed)


class BoardGFX(Sprite):

    # Padding inside board
    PADDING_X = 5
    PADDING_Y = 5

    # Color of our board
    COLOR = (0, 0, 0, 250)

    # Image of our board
    IMG_FILENAME = c.BOARD_GFX_NAME

    def __init__(self, board, index, panel):

        # Board have an index which allow us to place our board on panel
        self.index = index

        # Calcul board size based on block size and board dimensions
        w = BoardGFX.PADDING_X + (BoardGFX.PADDING_X + BlockGFX.W) * board.num_col
        h = BoardGFX.PADDING_Y + (BoardGFX.PADDING_Y + BlockGFX.H) * board.num_row

        # Get image of board
        # ref = cache.get_image(BoardGFX.IMG_FILENAME[self.index])
        ref = pg.Surface((w, h), pg.HWSURFACE | pg.SRCALPHA)

        # Create surface that will welcome our board
        pg.sprite.DirtySprite.__init__(self) # TODO Shouldn't you call the Sprite __init__? Weird stuff here
        SuperSurface.__init__(self, ref)

        # Crow image to BoardGFX size
        # self.rect.size = w, h

        # Poisiton board
        self.position(panel)

        # Fill our board image with board color
        self.image.fill(BoardGFX.COLOR)

        # Reference to logic board for mapping cases
        self.board = board

        # Dict that contain frozen blocks by col
        self.frozen_cells = {}

        # Dict that contain freeze timer by col
        self.freeze_timer = {}

    def __iter__(self):
        # Allow to iter in BoardGFX and his blocks (BlockGFX)
        return self.array.__iter__()

    def position(self, panel):
        # Position board
        self.rect.bottom = panel.rect.bottom
        RECT_PLAYER_1 = panel.rect.left + 10
        RECT_PLAYER_2 = panel.rect.right - self.rect.w - 10
        self.rect.x = RECT_PLAYER_2 if self.index else RECT_PLAYER_1

    def get_frozen_col(self, col):
        # Return the blocks in a frozen col
        return self.frozen_blocks.get(col, [])

    def freeze_col(self, col, duration):
        # Each case of a col will be frozen during "duration" ms
        self.frozen_cells[col] = []
        for line in self.board:
            # If case is not empty, then I freeze the block and add a timer
            if line[col]:
                line[col].frozen = True
                self.freeze_timer[col] = duration
                self.frozen_cells[col].append(line[col])

    def defreeze_col(self, col):
        # Each case in the col will be defreeze except if the case is dying
        for case in self.frozen_cells[col]:
            if not case.dying:
                case.frozen = False

    def freeze_update(self, elapsed):
        # Each existing timer will be update
        # if timer done => defreeze the col
        for col, timer in self.freeze_timer.items():
            if timer < 0:
                self.freeze_timer[col] = 0
                self.defreeze_col(col)
            else:
                self.freeze_timer[col] -= elapsed

    def update(self, elapsed, panel):
        # Position board
        self.position(panel)
        # Update the sprite (apply effects if needed)
        Sprite.update(self, elapsed)
        # Update blocks state by col
        self.freeze_update(elapsed)
