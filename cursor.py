import pygame as pg


class Cursor:
    def __init__(self, g):
        self.g = g 

        pg.mouse.set_visible(False)
        self.image = pg.Surface((7,12)).convert()
        self.image.set_colorkey("#ff00ff")
        self.image.fill("#ff00ff")
        self.iro = "#046834"
        pg.draw.polygon(self.image,self.iro,[[0,0],[0,12],[7,12],[0,0]])
        self.rect = pg.Rect(0,0,40,40)
        self.rect.center = (40,40)

        self.pos = pg.Vector2()
        self.grid = None
        self.estado = None

        self.dragging = False
        

    def update(self):
        self.pos.update(pg.mouse.get_pos())
        self.rect.topleft = self.pos 


        # self.pos_in_board = self.pos - self.g.board.borde
        # _x = None 
        # _y = None

        # self.estado = pg.mouse.get_just_pressed()
        # _jarl = self.pos_in_board/self.g.board.t
        # ab = tuple(map(int,_jarl.xy))
        # indice = ab[0] * self.g.board.n + ab[1] # asi o al reves ¿?
        # self.hover_on_tile = indice
        # if not self.g.board.rect.collidepoint(self.pos):
        #     self.hover_on_tile = None

        # if self.estado[0]:
        #     self.g.board.tiles[indice]['is_selected'] = not self.g.board.tiles[indice]['is_selected']

        if self.g.input.acciones['ci_down']:
            self.dragging = True 
        elif self.g.input.acciones['ci_up']:
            self.dragging = False


    def draw(self):
        self.g.screen.blit(self.image, self.rect)