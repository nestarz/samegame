#!/bin/python3

import pygame as pg
from . import cache
from . import constants as c
from . import tools as t
from .gamecore import GameCore, Cursor
from time import sleep

class Player():
  INDEX = 0
  def __init__(self):
    Player.INDEX += 1

  def setup_game(self, board, keys):
    self.board = board
    self.cursor = self.board.cursor
    self.keys = keys


class Party(t.Screen):
    def __init__(self):
        super().__init__()
        self.timer = 0


class Arcade(Party):
    def __init__(self):
        super().__init__()
        self.name = 'arcade'
        self.next = 'home'
        self.players = [Player(), Player()]
        self.img_boards = list()
        self.allow_input = [False for player in self.players]
        self.allow_input_timer = self.allow_swap_timer = [0 for player in self.players]

    def start(self, screen):
      """ Création des plateaux de jeu, des touches et attribution des plateaux de jeu aux joueurs """
      nb_color = 6
      nb_col = 7
      self.case_w, self.case_h = 38,38
      self.margin_x, self.margin_y = 5, 5
      self.game = GameCore(1,nb_color,10,nb_col,len(self.players))
      for i, player in enumerate(self.players):
        player.setup_game(self.game.all_board[i], c.CONTROLS[i])
      super().start(screen)

    def setup_images(self, screen):
        HEIGHT = screen.get_rect().h
        WIDTH = screen.get_rect().w

        panel = pg.Surface((WIDTH-150,HEIGHT-110), pg.SRCALPHA)
        panel = t.Panel(panel, screen, (0,0,0,210), True)
        panel.rect.midbottom = screen.get_rect().midbottom
        self.images.append(panel)
        margin_x = 30
        for i, player in enumerate(self.players):
          board = pg.Surface((self.margin_x+(self.case_w+self.margin_x)*player.board.num_col
            ,self.margin_y + (self.case_h+self.margin_y)*player.board.num_row+10), pg.SRCALPHA)
          board = t.Panel(board, panel.surface,  (255,255,255,30), True)
          board.rect.y = (panel.rect.h - board.rect.h)
          board.rect.x = (panel.rect.w - board.rect.w) + margin_x if i > 0 else margin_x
          margin_x = - margin_x
          self.images.append(board)
          self.img_boards.append(board)

    def check_for_input(self, keys):
        for i, player in enumerate(self.players):
          self.allow_input_timer[i] += self.elapsed
          self.allow_swap_timer[i] += self.elapsed
          if self.allow_input[i]:
              if keys[player.keys['UP']]:
                  player.cursor.move_up()
              elif keys[player.keys['DOWN']]:
                  player.cursor.move_down()
              elif keys[player.keys['RIGHT']]:
                  player.cursor.move_right()
              elif keys[player.keys['LEFT']]:
                  player.cursor.move_left()
              elif keys[player.keys['SWAP']]:
                  player.board.swap()
              elif keys[pg.K_ESCAPE]:
                  self.set_done(self.next)
          self.allow_input[i] = False

          no_key_pressed = (not keys[player.keys['DOWN']]
              and not keys[player.keys['UP']]
              and not keys[player.keys['RIGHT']]
              and not keys[player.keys['LEFT']]
              and not keys[player.keys['SWAP']]
              and not keys[pg.K_ESCAPE])

          key_pressed_and_timer_exceed = \
          ((self.allow_input_timer[i] > .1 and keys[player.keys['DOWN']])
              or (self.allow_input_timer[i] > .1 and keys[player.keys['UP']])
              or (self.allow_input_timer[i] > .1 and keys[player.keys['LEFT']])
              or (self.allow_swap_timer[i] > .5 and keys[player.keys['SWAP']])
              or (self.allow_input_timer[i] > .1 and keys[player.keys['RIGHT']]))

          if (key_pressed_and_timer_exceed):
                  self.allow_input[i] = True
                  self.allow_input_timer[i] = 0
                  self.allow_swap_timer[i] = 0
          elif no_key_pressed:
                  self.allow_input[i] = True
                  self.allow_input_timer[i] = -.4
                  self.allow_swap_timer[i] = -.4

    def set_done(self, next):
        super().set_done(next)
        self.to_set_done = True
        self.to_set_done_timer = 0.5
        self.bg.setup_effect('fadeout', 2)

    def update(self, window, keys, elapsed):
        super().update(window, keys, elapsed)
        self.timer += 1
        img = t.Image(t.text_to_surface(' {:04d} '.format(self.timer), 'joystix', 22, c.WHITE_RGB), window)
        start_img = pg.Surface(img.surface.get_size(), pg.SRCALPHA)
        start_img.fill((0,0,0,150))
        start_img.blit(img.surface, img.rect)
        start_img = t.Image(start_img, window)
        start_img.rect.right = window.get_rect().right
        start_img.rect.x = start_img.rect.x - 80
        start_img.rect.y = start_img.rect.y + 80
        window.blit(start_img.surface, start_img.rect)
        margin_x = 0
        for i, player in enumerate(self.players):
          board = player.board
          cursor = player.cursor
          for row in reversed(range(board.num_row)):
              for col in range(board.num_col):
                  if not board.board[row][col] is False:
                      pg.draw.rect(self.img_boards[i].surface,
                                       c.COLORS_DICT[board.board[row][col]]+(235,),
                                       [margin_x + (5+38)*col+5,
                                        (5+38)*(board.num_row-row)-30-5,
                                        38,
                                        38])
                  else:
                      pg.draw.rect(self.img_boards[i].surface,
                                       (255,255,255,50),
                                       [margin_x + (5+38)*col+5,
                                        (5+38)*(board.num_row-row)-30-5,
                                        38, 38])
          pg.draw.rect(self.img_boards[i].surface,
                             (255,255,255),
                             [margin_x +(5+38)*player.cursor.pos_col+5,
                             (5+38)*(board.num_row-cursor.pos_row)-30-5,
                             38*2+5, 38],5)
          board.gravity()
          destroy = board.destroy_block()
          board.gravity()
          if destroy: #debug only
            print(destroy)
            print(board)
