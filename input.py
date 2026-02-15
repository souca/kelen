import sys
import pygame as pg


class InputManager:

    def __init__(self, g):
        self.g = g



    def __str__(self):
        ...
    
    def update(self):

        for event in pg.event.get():
            self.check_exit(event)

    @staticmethod
    def check_exit(event):
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            sys.exit()
        