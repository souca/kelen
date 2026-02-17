import pygame as pg


class Gui:
    def __init__(self, g):
        self.g = g

        _font_path = 'assets/fonts/cambria.ttf'
        self.fonts = {26: pg.font.Font(_font_path, 26),
                      18: pg.font.Font(_font_path, 18)}

        # Control bar
        _surf = pg.Surface((40,560), pg.SRCALPHA)
        _surf.set_colorkey("#ff00ff")
        _surf.fill("#edf1ef")
        _rect = _surf.get_rect().move(620,40)
        self.control_bar = {'surf': _surf, 'rect': _rect}

        # Info icon
        _surf = self.fonts[18].render('(i)', True, "#84acff")
        _rect = _surf.get_rect(midtop=(640,10))
        self.info_icon = {'surf': _surf, 'rect': _rect}
        # Info window
        _surf = self.fonts[26].render(':: Nudos ::', True, "#84acff")
        _rect = _surf.get_rect(midtop=(340,6))
        self.info_window = {'surf': _surf, 'rect': _rect}
        
    
    def update(self):
        ...

    def draw(self):

        self.control_bar['surf'].fill("#edf1ef")
        pg.draw.circle(self.control_bar['surf'], self.g.board.iros[0], (20,20), 10, 0)
        pg.draw.circle(self.control_bar['surf'], self.g.board.iros[1], (20,50), 10, 0)

        _current_iro = self.g.board.iros[self.g.board.current_iro]
        _y = 20 if _current_iro == self.g.board.iros[0] else 50
        pg.draw.circle(self.control_bar['surf'], _current_iro, (20,_y), 14, 2)
        self.g.screen.blit(self.control_bar['surf'], self.control_bar['rect'])

        self.g.screen.blit(self.info_icon['surf'], self.info_icon['rect'])
        self.g.screen.blit(self.info_window['surf'], self.info_window['rect'])

        

