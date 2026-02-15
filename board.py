import pygame as pg
import numpy as np


class Board:
    def __init__(self, g):
        self.w, self.h = g.size

        self.borde = [40,40]
        self.grid = pg.Surface((self.w-2*self.borde[0],
                               self.h-2*self.borde[1]))

        self.n = 7 # numero de tiles
        self.t = min(self.grid.get_size())/self.n # tamaño del tile
        # ojo aqui: ok si W==H, en rectángulos no sé!

        self.g = g

    def update(self):
        ...

    def draw(self):
        
        self.draw_grid()

    
    def draw_grid(self):

        _iro = "#5ff0f2"
        for i in range(self.n):
            pg.draw.line(self.grid, _iro, (i*self.t,0), (i*self.t,self.h))
        for j in range(self.n):
            pg.draw.line(self.grid, _iro, (0,j*self.t), (self.w,j*self.t))

        self.g.screen.blit(self.grid, self.borde)