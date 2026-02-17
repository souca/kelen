import sys
import pygame as pg
from input import InputManager
from board import Board
from cursor import Cursor
from gui import Gui

"""
-toggle grid lines
-fix corners in tile centers
-dynamic color change
-maybe more dynamic changes in other parameters
-export config in file
-import config from file (python now allows drag and drop)
-improved gui
-simulation help
-show rotated
-ease fill tiles
-clic in path points!!!
"""

class Game:

    def __init__(self):

        self.size = pg.Vector2(680,640)
        pg.init()

        pg.display.set_caption('JARL')
        self.screen = pg.display.set_mode(self.size)

        self.clock = pg.time.Clock()
        self.input = InputManager(self)
        self.board = Board(self)
        self.cursor = Cursor(self)
        self.gui = Gui(self)

        self.bg = {'surf': pg.Surface(self.size)}
        self.bg['surf'].fill("#94dbb4")
        self.bg |= {'rect': self.bg['surf'].get_rect(topleft=(0,0))}


    def run(self):
        while True:
            self.update()
            self.draw()

    def update(self):

        self.cursor.update()
        self.input.update()
        self.gui.update()
        self.board.update()

        pg.display.update()
        self.clock.tick(60)

    def draw(self):

        self.screen.blit(self.bg['surf'], self.bg['rect'])
        self.board.draw() 
        self.gui.draw()
        self.cursor.draw()

Game().run()
