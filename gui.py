import pygame as pg


class Gui:
    def __init__(self, g):
        self.g = g

        self.surf = pg.Surface((40,560), pg.SRCALPHA)
        self.surf.set_colorkey("#ff00ff")
        self.surf.fill("#edf1ef")
        self.rect = self.surf.get_rect().move(620,40)
    
    def update(self):
        ...

    def draw(self):

        self.surf.fill("#edf1ef")
        pg.draw.circle(self.surf, self.g.board.iros[0], (20,20), 10, 0)
        pg.draw.circle(self.surf, self.g.board.iros[1] , (20,50), 10, 0)

        _current_iro = self.g.board.iros[self.g.board.current_iro]
        _y = 20 if _current_iro == self.g.board.iros[0] else 50
        pg.draw.circle(self.surf, _current_iro, (20,_y), 14, 2)
        self.g.screen.blit(self.surf, self.rect)

        

