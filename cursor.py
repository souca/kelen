import pygame as pg


class Cursor:
    def __init__(self, g):
        self.g = g 

        self.image = pg.Surface((7,12)).convert()
        self.image.set_colorkey((255,0,255))
        self.image.fill((255,0,255))
        self.iro = (240,240,240)
        pg.draw.polygon(self.image,self.iro,[[0,0],[0,12],[7,12],[0,0]])
        self.rect = pg.Rect(0,0,40,40)
        self.rect.center = (40, 40)
        self.estado = pg.mouse.get_pressed()

    def update(self):
        ...

    def draw(self):
        self.g.screen.blit(self.image, self.rect)