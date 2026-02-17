import pygame as pg
import numpy as np
from itertools import product
from random import randint 


class Board:
    def __init__(self, g):
        self.borde = pg.Vector2(40,40)
        self.size = pg.Vector2(560,560) #g.size - 2*self.borde

        self.iros = ["#ff0088","#006aff"]
        self.current_iro = 0

        self.surf = pg.Surface(self.size, pg.SRCALPHA)
        self.surf.fill("#e3f0f3")
        self.rect = self.surf.get_rect()

        self.n = 7 # numero de tiles
        self.t = min(self.surf.get_size())/self.n # tamaño del tile
        # todo: ojo aqui-> ok si W==H, en rectángulos no sé!

        self.tiles = self.create_tiles()
        # por ahora: tiles = {'surf':, 'rect':, 'other_info_TBD':}
        # el rect va colocado con respecto al origen de board.rect

        self.tile_mouse_hovering = None 

        # estado: dos elementos, trenza uno y trenza dos.
        #         dentro, (iro, path in narco)
        self.estado = [[[0,0] for tile in self.tiles],
                       [[0,0] for tile in self.tiles]]

        # ========================================
        self.puntos = {'oo': pg.Vector2(0.5,0.5),
                       'ee': pg.Vector2(1.0,0.5),
                       'ww': pg.Vector2(0.0,0.5),
                       'nn': pg.Vector2(0.5,0.0),
                       'ss': pg.Vector2(0.5,1.0)}
        self.narco = { 0: [],
                       1: ['ee','oo','nn'],
                       2: ['ee','oo','ss'],
                       3: ['ww','oo','nn'],
                       4: ['ww','oo','ss'],
                       5: ['ee','ww'],
                       6: ['nn','ss']}
        # ========================================

        # g de game o de global
        self.g = g

    def create_tiles(self):
        # Inicialización de los tiles:
        # -para cada punto de la malla 2D
        # -generamos una surface blanca con máscara transparente
        # -generamos un rect del mismo tamaño colocado en el punto correpondiente del tablero
        # todo: alerta cuadrado
        _tiles = []
        for x in product(range(self.n), repeat=2):
            _surf = pg.Surface((self.t, self.t), pg.SRCALPHA)
            _surf.set_colorkey("#ff00ff")
            _surf.fill("#ffffff")
            _rect = _surf.get_rect(topleft=(pg.Vector2(x)*self.t))
            _tiles.append({'surf': _surf, 'rect': _rect})
        return _tiles

    def update(self):
        
        _mpos = self.g.cursor.pos-self.borde

        # acciones de ratón contra tiles
        if self.rect.collidepoint(_mpos):

            _ab = tuple(map(int,_mpos/self.t)) 
            _idx = _ab[0]*self.n+_ab[1]

            if self.g.input.acciones['cd']:
                self.estado[0][_idx][1] = 0
            
            if self.g.input.acciones['cd_mod']:
                self.estado[1][_idx][1] = 0

            if self.g.input.acciones['ci']:
                self.estado[0][_idx][0] = self.current_iro
                self.estado[0][_idx][1] = (self.estado[0][_idx][1]+1)%len(self.narco)

            if self.g.input.acciones['ci_mod']:
                self.estado[1][_idx][0] = self.current_iro
                self.estado[1][_idx][1] = (self.estado[1][_idx][1]+1)%len(self.narco)

            if self.g.input.acciones['swap_over_under']:
                self.estado[0][_idx], self.estado[1][_idx] = self.estado[1][_idx], self.estado[0][_idx]

        if self.g.input.acciones['change_iro']:
            self.current_iro = 0 if self.current_iro == 1 else 1

        if self.g.input.acciones['debug']:
            print(self.estado[0])
            print(self.estado[1])
            print()

    def draw(self):
        
        for k,tile in enumerate(self.tiles):

            # inicializar el dibujo del tile
            tile['surf'].fill("#ffffff")

            # todo: we can do better here -----------------------------------------------------
            # pintamos trenza 1
            if _ptos := [self.puntos[x]*self.t for x in self.narco[self.estado[0][k][1]]]:
                _iro = self.iros[self.estado[0][k][0]]
                pg.draw.circle(tile['surf'], "#000000", 0.5*pg.Vector2(self.t, self.t), 23)
                pg.draw.circle(tile['surf'], _iro, 0.5*pg.Vector2(self.t, self.t), 21)
                pg.draw.lines(tile['surf'], "#000000", False, _ptos, 48)
                pg.draw.lines(tile['surf'], _iro, False, _ptos, 44)

            # pintamos trenza 2
            if _ptos := [self.puntos[x]*self.t for x in self.narco[self.estado[1][k][1]]]:
                _iro = self.iros[self.estado[1][k][0]]
                pg.draw.circle(tile['surf'], "#000000", 0.5*pg.Vector2(self.t, self.t), 23)
                pg.draw.circle(tile['surf'], _iro, 0.5*pg.Vector2(self.t, self.t), 21)
                pg.draw.lines(tile['surf'], "#000000", False, _ptos, 48)
                pg.draw.lines(tile['surf'], _iro, False, _ptos, 44)
            # ---------------------------------------------------------------------------------

            # imprimimos la tile en el board
            self.surf.blit(tile['surf'],tile['rect'])

        # imprimimos el board en la screen
        self.g.screen.blit(self.surf, self.borde)

        _iro = "#5ff0f2"
        for i in range(self.n):
            pg.draw.line(self.surf, _iro, (i*self.t,0), (i*self.t,self.size[1]))
        for j in range(self.n):
            pg.draw.line(self.surf, _iro, (0,j*self.t), (self.size[0],j*self.t))

        if self.tile_mouse_hovering is not None:
            _tile = self.tiles[self.tile_mouse_hovering]['rect']
            pg.draw.rect(self.surf,"#42aaff", _tile, 2)

        self.g.screen.blit(self.surf, self.borde)       
