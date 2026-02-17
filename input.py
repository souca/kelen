import sys
import pygame as pg


class InputManager:

    def __init__(self, g):

        self.g = g
        self.acciones = {'ci': False,
                         'cd': False,
                         'ci_mod': False,
                         'cd_mod': False,
                         'change_iro': False,
                         'debug': False}

    def __str__(self):
        ...
    
    def update(self):

        self.acciones = {k: False for k in self.acciones}

        for event in pg.event.get():
            self.check_exit(event)

            if event.type == pg.MOUSEBUTTONDOWN:
                _shift = pg.key.get_mods() & pg.KMOD_SHIFT
                if event.button == 1:  # clic izquierdo
                        self.acciones['ci_mod' if _shift else 'ci' ] = True
                elif event.button == 3: # clic derecho
                        self.acciones['cd_mod' if _shift else 'cd' ] = True

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                      self.acciones['change_iro'] = True
                if event.key == pg.K_p: 
                     self.acciones['debug'] = True


    @staticmethod
    def check_exit(event):
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            sys.exit()
        