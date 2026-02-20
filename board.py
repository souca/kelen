import pygame as pg
import numpy as np
from itertools import product
from random import randint 
from tile import Tile


class Board:
    def __init__(self, g):
        # g de game o de global
        self.g = g

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
        self.vecinos = self.calculate_tiles_vecinos(self.n)
        # por ahora: tiles = {'surf':, 'rect':, 'anchor_points':, 'other_info_TBD':}
        # ...'anchor_points': {'o': False, 'e': False, 'n': False, 's': False, 'w': False }
        # ..................: direccion: activacion 
        # ..................: a cambiar por un bytestring
        # anchor_points = 0b0000
        # el rect va colocado con respecto al origen de board.rect

        self.tile_mouse_hovering = None 
        self.tile_mouse_hovering_neighbours = []

        self.anchors_visited_during_drag = set()

        # estado: dos elementos, trenza uno y trenza dos.
        #         dentro, (iro, path in narco)
        self.estado = [[[0,0] for tile in self.tiles],
                       [[0,0] for tile in self.tiles]]

        self.rotate = False
        self.draw_grid = True

        # ========================================
        # todo: ugly and bad naming
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
        self.nadir = {'ee':'ww',
                      'ww':'ee',
                      'nn': 'ss',
                      'ss':'nn'}
        # ========================================

    def create_tiles(self):
        # Inicialización de los tiles:
        # -para cada punto de la malla 2D
        # -generamos una surface blanca con máscara transparente
        # -generamos un rect del mismo tamaño colocado en el punto correpondiente del tablero
        # todo: alerta cuadrado
        # _ap = {'oo': False, 'ee': False, 'nn': False, 'ss': False, 'ww': False}
        # _tiles = []
        # for xy in product(range(self.n), repeat=2):
            # _surf = pg.Surface((self.t, self.t), pg.SRCALPHA)
            # _surf.set_colorkey("#ff00ff")
            # _surf.fill("#ffffff")
            # _rect = _surf.get_rect(topleft=(pg.Vector2(xy)*self.t))
            # _tiles.append({'surf': _surf, 'rect': _rect, 'anchor_points': _ap.copy()})
            # _tiles.append(Tile(self.g, self.n, self.size, xy))
        return [Tile(self.g, idx, self.n, self.size, xy)
                for idx,xy in enumerate(product(range(self.n), repeat=2))]


    @staticmethod
    def calculate_tiles_vecinos(n):
        # asumimos tablero cuadrado
        # devolvemos [()], el orden va implícito
        vecinos = [] 
        for idx in range(n*n):
            y,x = divmod(idx,n)
            gr = []
            if x > 0:
                gr.append(idx-1)
            if x < n-1:
                gr.append(idx+1)
            if y > 0:
                gr.append(idx-n)
            if y < n-1:
                gr.append(idx+n)

            vecinos.append(tuple(gr))
        return vecinos

    def update(self):
        
        _mpos = self.g.cursor.pos-self.borde

        # acciones de ratón contra tiles
        self.tile_mouse_hovering = None
        if self.rect.collidepoint(_mpos):

            _ab = tuple(map(int,_mpos/self.t)) 
            _idx = _ab[0]*self.n+_ab[1]
            self.tile_mouse_hovering = _idx
            self.tile_mouse_hovering_neighbours = self.vecinos[_idx]

            if self.g.cursor.dragging:
                # -mientras el cursor esté siendo clicado, las anclas por las que pase se
                # les cambiará el estado. 
                # -distancia^2 de 100 puesta a mano, pero habría que hacerla dependiente de self.t
                # -anchors_visited_during_drag es un set que contiene las anclas por las que se pasó
                # en la sesión de arrastre. Cuando se suelte el botón, se resetea.
                
                _vecino_lookup = {'w': -self.n, 'e': self.n, 'n': -1, 's': 1, 'o': 0}

                for _anchor,_ap in Tile.anchor_coordinates.items():
                    _xy = self.tiles[_idx].rect.topleft + self.t*_ap
                    if _mpos.distance_squared_to(_xy) < 100 and (_idx,_anchor) not in self.anchors_visited_during_drag:
                        self.tiles[_idx].anchors ^= Tile.bit_anchor[_anchor]
                        self.anchors_visited_during_drag.add((_idx,_anchor))

                        # aqui vamos a ver si hay que actualizar el path en este tile
                        
                        # el estado de un ancla W tiene que estar sincronizado con el 
                        # ancla E del vecino a la izquierda en la malla de tiles. 
                        # `vecino_lookup` da el cambio de indice para obtener cambio de índice
                        # para caer en el vecino en funcion del ancla original
                        # `nadir` da el ancla opuesta dentro de un tile: w->e n->s etc
                        _idx_vecino = _idx + _vecino_lookup[_anchor]
                        _anchor_vecino = Tile.nadir[_anchor]
                        if _idx_vecino in self.vecinos[_idx] and (_idx_vecino,_anchor_vecino) not in self.anchors_visited_during_drag:
                            self.tiles[_idx_vecino].anchors ^= Tile.bit_anchor[_anchor_vecino]
                            self.anchors_visited_during_drag.add((_idx_vecino,_anchor_vecino))

            if self.g.input.acciones['ci_up']:
                # reiniciamos las anclas visitadas en una sesión de arrastre
                self.anchors_visited_during_drag.clear()
                

            # if self.g.input.acciones['cd']:
            #     self.estado[0][_idx][1] = 0
            
            # if self.g.input.acciones['cd_mod']:
            #     self.estado[1][_idx][1] = 0

            # if self.g.input.acciones['ci']:
            #     self.estado[0][_idx][0] = self.current_iro
            #     self.estado[0][_idx][1] = (self.estado[0][_idx][1]+1)%len(self.narco)

            # if self.g.input.acciones['ci_mod']:
            #     self.estado[1][_idx][0] = self.current_iro
            #     self.estado[1][_idx][1] = (self.estado[1][_idx][1]+1)%len(self.narco)

            if self.g.input.acciones['swap_over_under']:
                self.estado[0][_idx], self.estado[1][_idx] = self.estado[1][_idx], self.estado[0][_idx]

            # check if mouse is close to anchor point 
            # todo: esto puede ir con bitmasks para hacerlo mucho más bonito
            # todo: esto pide a gritos separarlo en pequeños métodos
            # if self.g.input.acciones['anchor']:
            #     _ap = self.tiles[_idx]['anchor_points']
            #     _lookup = {'ee': self.n, 'ww': -self.n, 'nn': -1, 'ss': +1}
            #     if (anchor := self.get_anchor_point(_idx, _mpos)) is not None:
            #         _ap[anchor] = not _ap[anchor]
                    # vecinos 
                    # _idx_vecino = _idx + _lookup.get(anchor, 0)
                    # _y, _x = divmod(_idx_vecino, self.n) # notice we're brushing the 'oo' away
                    # _y0, _x0 = divmod(_idx, self.n)
                    # manhattan = abs(_y0-_y) + abs(_x0-_x) # keep it simple
                    # if 0<=_x<self.n and 0<=_y<self.n and manhattan == 1:
                    #     _ap_vecino = self.tiles[_idx_vecino]['anchor_points']
                    #     _nadir = self.nadir[anchor]
                    #     _ap_vecino[_nadir] = not _ap_vecino[_nadir]

                    # _idx_vecino = _idx + _lookup.get(anchor, 0)
                    # if (anchor_vecino := self.get_anchor_vecino_point(_idx_vecino)) is not None:
                    #     _ap_vecino = self.tiles[_idx_vecino]['anchor_points'][anchor_vecino]
                    #     _ap_vecino = not _ap_vecino

                
                    # si en esta interacción hubo un cambio (un nuevo anchor point),
                    # comprobaremos si los anchors del tile forman un path. 
                    # Si lo forman, le ponemos el estado correspondiente al tile! 
                    #
                    # ahora lo hacemos para _tile, pero también habrá que hacerlo para el vecino!
                    # 
                    # la complicacion de que tenemos que aceptar para el camino vertical|horizontal
                    # los conjuntos de anchors con y sin el centro! 
                    # _activos = tuple(k for k,v in _ap.items() if v)
                    # if _este_estado := [ k for k,v in self.narco.items() if set(_activos)==set(v)]:
                    #     self.estado[0][_idx][1] = _este_estado[0]
                    # elif set(_activos) == set(['ee','oo','ww']):
                    #     self.estado[0][_idx][1] = 5
                    # elif set(_activos) == set(['nn','oo','ss']):
                    #     self.estado[0][_idx][1] = 6
                    # else: 
                    #     self.estado[0][_idx][1] = 0
                
        if self.g.input.acciones['change_iro']:
            self.current_iro = 0 if self.current_iro == 1 else 1

        if any(self.g.input.acciones.values()):
            self.surf_rotate = pg.transform.rotate(self.surf, 45)

        if self.g.input.acciones['rotate']:
            self.rotate = not self.rotate
        
        if self.g.input.acciones['toggle_grid']:
            self.draw_grid = not self.draw_grid

    # def get_anchor_vecino_point(self, _idx_vecino, anchor):
    #     _y, _x = divmod(_idx_vecino, self.n) # notice we're brushing the 'oo' away
    #     _y0, _x0 = divmod(_idx, self.n)
    #     manhattan = abs(_y0-_y) + abs(_x0-_x) # keep it simple
    #     if 0<=_x<self.n and 0<=_y<self.n and manhattan == 1:
    #         _ap_vecino = self.tiles[_idx_vecino]['anchor_points']
    #         _nadir = self.nadir[anchor]
    #         return _nadir
    #     return None
            # _ap_vecino[_nadir] = not _ap_vecino[_nadir]

    # def get_anchor_point(self, _idx, _mpos):
    #     '''
    #     returns an anchor point from the hovered tile close to the cursor,
    #     or None
    #     '''
    #     _oo = self.tiles[_idx].rect.topleft
    #     for pp in self.tiles[_idx]['anchor_points']:
    #         _xy = self.puntos[pp] * self.t + _oo
    #         if _mpos.distance_squared_to(_xy) < 100:
    #             return pp
    #     return None

    def draw(self):

        for k,tile in enumerate(self.tiles):

            tile.draw()
        
            # inicializar el dibujo del tile
            # tile.surf.fill("#ffffff")

            # todo: we can do better here -----------------------------------------------------
            # pintamos trenza 1
            # if _ptos := [self.puntos[x]*self.t for x in self.narco[self.estado[0][k][1]]]:
            #     _iro = self.iros[self.estado[0][k][0]]
            #     pg.draw.circle(tile.surf, "#000000", 0.5*pg.Vector2(self.t, self.t), 23)
            #     pg.draw.circle(tile.surf, _iro, 0.5*pg.Vector2(self.t, self.t), 21)
            #     pg.draw.lines(tile.surf, "#000000", False, _ptos, 48)
            #     pg.draw.lines(tile.surf, _iro, False, _ptos, 44)

            # pintamos trenza 2
            # if _ptos := [self.puntos[x]*self.t for x in self.narco[self.estado[1][k][1]]]:
            #     _iro = self.iros[self.estado[1][k][0]]
            #     pg.draw.circle(tile.surf, "#000000", 0.5*pg.Vector2(self.t, self.t), 23)
            #     pg.draw.circle(tile.surf, _iro, 0.5*pg.Vector2(self.t, self.t), 21)
            #     pg.draw.lines(tile.surf, "#000000", False, _ptos, 48)
            #     pg.draw.lines(tile.surf, _iro, False, _ptos, 44)
            # ---------------------------------------------------------------------------------

            # imprimimos la tile en el board
            self.surf.blit(tile.surf,tile.rect)

        # draw anchor points
        for tile in self.tiles:
            if (tile.idx == self.tile_mouse_hovering or 
                tile.idx in self.tile_mouse_hovering_neighbours):
                # pg.draw.rect(self.surf, "#d5a34222", tile.rect)
                for anchor in Tile.bit_anchor:
                    _pto = Tile.anchor_coordinates[anchor]*self.t + tile.rect.topleft
                    # _iro = "#ffcb22" if tile.anchors&Tile.bit_anchor[anchor] else "#5522ff"
                    if tile.anchors&Tile.bit_anchor[anchor]:
                        pg.draw.circle(self.surf, "#ffcb22", tuple(map(int,_pto)), 7)
                    pg.draw.circle(self.surf, "#5522ff", tuple(map(int,_pto)), 5, 1)



        # imprimimos el board en la screen
        self.g.screen.blit(self.surf, self.borde)

        # grid lines
        if self.draw_grid:
            _iro = "#5ff0f2"
            for i in range(self.n):
                pg.draw.line(self.surf, _iro, (i*self.t,0), (i*self.t,self.size[1]))
            for j in range(self.n):
                pg.draw.line(self.surf, _iro, (0,j*self.t), (self.size[0],j*self.t))

        # hover related decorations
        # if self.tile_mouse_hovering is not None:
        #     # outline
        #     _tile = self.tiles[self.tile_mouse_hovering]
        #     pg.draw.rect(self.surf,"#42aaff", _tile['rect'], 1)

        #     # also its neighbourgs
        #     vecinos = [-1,+1,-self.n,+self.n]
        #     _idxs = [self.tile_mouse_hovering + v for v in vecinos]
        #     _y0,_x0 = divmod(self.tile_mouse_hovering, self.n)
        #     for _id in _idxs:
        #         _y,_x = divmod(_id, self.n)
        #         manhattan = abs(_y0-_y) + abs(_x0-_x) # keep it simple
        #         if 0<=_x<self.n and 0<=_y<self.n and manhattan == 1:
        #             _tile_v = self.tiles[_id]
        #             pg.draw.rect(self.surf,"#ffc342", _tile_v['rect'], 1)

        #     # anchor points
        #     _oo = _tile['rect'].topleft
        #     for k,v in _tile['anchor_points'].items():
        #         _iro = "#42aaff" if not v else "#ffdc42"
        #         _size = 2 if not v else 4
        #         pg.draw.circle(self.surf, _iro, self.t*self.puntos[k]+_oo, _size)
        #         # pg.draw.circle(self.surf, "#42aaff", self.t*v+_oo, 2)

        if not self.rotate:
            self.g.screen.blit(self.surf, self.borde)       
        else:
            _rect_rotate = self.surf_rotate.get_rect(center=self.surf.get_rect().center).move(self.borde)
            self.g.screen.blit(self.surf_rotate, _rect_rotate)       
