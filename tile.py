import pygame as pg


class Tile:

    anchor_coordinates = {'o': pg.Vector2(0.5,0.5),
                          'n': pg.Vector2(0.5,0.0),
                          's': pg.Vector2(0.5,1.0),
                          'e': pg.Vector2(1.0,0.5),
                          'w': pg.Vector2(0.0,0.5)}
    bit_anchor = {'o':1<<0, 'n':1<<1, 's':1<<2, 'e':1<<3, 'w':1<<4}
    nadir = {'w':'e', 'e':'w', 'n':'s', 's':'n', 'o': None}

    def __init__(self, g, idx, number_of_tiles, board_size, topleft):
        '''
        number_of_tiles:int >>  número de tiles en un eje (asumimos tablero cuadrado)
        board_size:Vector2 >> tamaño del tablero 
        topleft:[] >> posicion de la esquina NW del tile en coordenadas del tablero (no?)
        '''

        self.g = g
        
        self.idx = idx
        self.size = min(board_size)/number_of_tiles
        self.surf = pg.Surface((self.size, self.size), pg.SRCALPHA)
        self.surf.set_colorkey("#ff00ff")
        self.surf.fill("#ffffff")
        self.rect = self.surf.get_rect(topleft=(pg.Vector2(topleft)*self.size))
        self.anchors = 0b00000 

    @staticmethod
    def random_iro():
        from random import randint
        return (randint(0,255), randint(0,255), randint(0,255))

    def draw(self):

        N = Tile.bit_anchor['n']
        S = Tile.bit_anchor['s']
        W = Tile.bit_anchor['w']
        E = Tile.bit_anchor['e']
        O = Tile.bit_anchor['o']

        {
            (N|O|S): self.vertical,
            (E|O|W): self.horizontal,
            (N|S): self.vertical,
            (E|W): self.horizontal,
            (O): self.center_point,
            (E): self.east_point,
            (W): self.west_point,
            (N|O|W): self.corner_now,
            (N|O|E): self.corner_noe,
            (S|O|W): self.corner_sow,
            (S|O|E): self.corner_soe,
            (N|O|W|E|S): self.cross,
            (N|W|E|S): self.cross,
        }.get(self.anchors, self.empty)()


    def empty(self):
        self.surf.fill("#ffffff")

    def cross(self):
        _iro = self.g.board.iros[0]
        _ptos = (Tile.anchor_coordinates['n']*self.size,
                 Tile.anchor_coordinates['s']*self.size)
        pg.draw.lines(self.surf, _iro, False, _ptos, 48)
        _ptos = (Tile.anchor_coordinates['w']*self.size,
                 Tile.anchor_coordinates['e']*self.size)
        pg.draw.lines(self.surf, _iro, False, _ptos, 48)

    def vertical(self):
        _iro = self.g.board.iros[0]
        _ptos = (Tile.anchor_coordinates['n']*self.size,
                 Tile.anchor_coordinates['s']*self.size)
        pg.draw.lines(self.surf, _iro, False, _ptos, 48)

    def horizontal(self):
        _iro = self.g.board.iros[0]
        _ptos = (Tile.anchor_coordinates['w']*self.size,
                 Tile.anchor_coordinates['e']*self.size)
        pg.draw.lines(self.surf, _iro, False, _ptos, 48)
    
    def east_point(self):
        ...

    def west_point(self):
        ...

    def corner_now(self):
        _iro = self.g.board.iros[0]
        _ptos = (Tile.anchor_coordinates['n']*self.size,
                 Tile.anchor_coordinates['o']*self.size,
                 Tile.anchor_coordinates['w']*self.size)
        pg.draw.lines(self.surf, _iro, False, _ptos, 48)
        pg.draw.circle(self.surf, _iro, _ptos[1], 24)

    def corner_noe(self):
        _iro = self.g.board.iros[0]
        _ptos = (Tile.anchor_coordinates['n']*self.size,
                 Tile.anchor_coordinates['o']*self.size,
                 Tile.anchor_coordinates['e']*self.size)
        pg.draw.lines(self.surf, _iro, False, _ptos, 48)
        pg.draw.circle(self.surf, _iro, _ptos[1], 24)

    def corner_sow(self):
        _iro = self.g.board.iros[0]
        _ptos = (Tile.anchor_coordinates['s']*self.size,
                 Tile.anchor_coordinates['o']*self.size,
                 Tile.anchor_coordinates['w']*self.size)
        pg.draw.lines(self.surf, _iro, False, _ptos, 48)
        pg.draw.circle(self.surf, _iro, _ptos[1], 24)
        
    def corner_soe(self):
        _iro = self.g.board.iros[0]
        _ptos = (Tile.anchor_coordinates['s']*self.size,
                 Tile.anchor_coordinates['o']*self.size,
                 Tile.anchor_coordinates['e']*self.size)
        pg.draw.lines(self.surf, _iro, False, _ptos, 48)
        pg.draw.circle(self.surf, _iro, _ptos[1], 24)
        
    def center_point(self):
        _iro = self.g.board.iros[0]
        _pto = Tile.anchor_coordinates['o']*self.size
        pg.draw.circle(self.surf, _iro, _pto, 30)
