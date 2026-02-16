import pygame as pg
import numpy as np
from itertools import product


class Board:
    def __init__(self, g):
        self.w, self.h = g.size
        self.borde = pg.Vector2(40,40)
        self.grid = pg.Surface(g.size-2*self.borde)
        self.grid.fill("#e3f0f3")
        self.rect = self.grid.get_rect(topleft=self.borde)

        self.n = 7 # numero de tiles
        self.t = min(self.grid.get_size())/self.n # tamaño del tile
        # todo: ojo aqui-> ok si W==H, en rectángulos no sé!

        self.tiles = self.create_tiles()

        self.g = g

    def update(self):
        ...

    def draw(self):
        
        self.draw_grid()

        # draw embelishments: selected and hover
        for k,tile in enumerate(self.tiles):

            if tile['is_selected']:
                # pg.draw.rect(self.g.screen, "#ecadee", tile['rect'].move(self.borde))
                xy0 = self.borde + pg.Vector2()
                xy1 = self.borde + pg.Vector2(self.t,self.t)
                # pg.draw.circle(tile['surf'], "#ff1231", (self.t,self.t), 10)
                pg.draw.rect(tile['surf'], "#44bb44", tile['rect'].move(self.borde),0)

            self.g.screen.blit(tile['surf'],tile['rect'])

            if k == self.g.cursor.hover_on_tile:
                pg.draw.rect(self.g.screen, "#ffccff", tile['rect'].move(self.borde), 2)

    def ord(self, k):
        # todo: pode ser static
        _i = k//self.n 
        _j = k%self.n 
        return (_i,_j)

    @staticmethod
    def create_transparent_surface(size, colorkey="#ff00ff"):
        _surf = pg.Surface((size,size))
        _surf.set_colorkey(colorkey)
        _surf.fill(colorkey)
        return _surf

    def create_tiles(self):

        return [{"rect": pg.Rect(*self.t*pg.Vector2(x), self.t, self.t),
                 "surf": self.create_transparent_surface(self.t),
                 "is_selected": False}
                for x in (product(range(self.n), repeat=2))]
    
    def draw_grid(self):

        _iro = "#5ff0f2"
        for i in range(self.n):
            pg.draw.line(self.grid, _iro, (i*self.t,0), (i*self.t,self.h))
        for j in range(self.n):
            pg.draw.line(self.grid, _iro, (0,j*self.t), (self.w,j*self.t))

        self.g.screen.blit(self.grid, self.borde)

        # ==================================
        self.puntos = {'oo': pg.P(0.5,0.5),
                       'ee': pg.P(1.0,0.5),
                       'ww': pg.P(0.0,0.5),
                       'nn': pg.P(0.5,0.0),
                  'ss': pg.P(0.5,1.0)}
        self.narco = {0: ['ee','oo','nn']}
        # ==================================