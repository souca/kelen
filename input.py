import sys
import pygame as pg


class InputManager:

    def __init__(self, g):

        self.g = g
        self.acciones = {'ci_down': False,
                         'cd_down': False,
                         'ci_up': False,
                         'cd_up': False,
                         'ci_mod': False,
                         'cd_mod': False,
                         'ci_hold': False,
                         'cd_hold': False,
                         'ci_hold_mod': False,
                         'cd_hold_mod': False,
                         'change_iro': False,
                         'swap_over_under': False,
                         'debug': False,
                         'anchor': False,
                         'rotate': False,
                         'toggle_grid': False}

    def update(self):

        self.acciones = {k: False for k in self.acciones}

        _shift = pg.key.get_mods() & pg.KMOD_SHIFT

        mouse_buttons = pg.mouse.get_pressed()
        self.acciones['ci_hold'] = mouse_buttons[0]
        self.acciones['cd_hold'] = mouse_buttons[2]
        self.acciones['ci_mod_hold'] = mouse_buttons[0] & _shift
        self.acciones['cd_mod_hold'] = mouse_buttons[2] & _shift


        for event in pg.event.get():
            self.check_exit(event)

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # clic izquierdo
                        self.acciones['ci_mod' if _shift else 'ci_down' ] = True
                elif event.button == 3: # clic derecho
                        self.acciones['cd_mod' if _shift else 'cd_down' ] = True

            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.acciones['ci_up'] = True
                elif event.button == 3:
                    self.acciones['cd_up'] = True

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                      self.acciones['change_iro'] = True
                if event.key == pg.K_p: 
                     self.acciones['debug'] = True
                if event.key == pg.K_s: 
                     self.acciones['swap_over_under'] = True
                if event.key == pg.K_w:
                     self.acciones['anchor'] = True
                if event.key == pg.K_r:
                     self.acciones['rotate'] = True
                if event.key == pg.K_g:
                     self.acciones['toggle_grid'] = True

    @staticmethod
    def check_exit(event):
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            sys.exit()
        