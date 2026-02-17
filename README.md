
# Kēlen

Hace mucho tiempo, caí en una web que hablaba del [Kēlen](https://www.terjemar.net/kelen/lajathin.php), un lenguaje inventado por Lydia Sotomayor, que tenía un curioso sistema de escritura ceremonial compuesto de lazos. 

Hiciera unos cuantos sketches en Processing para pintarlos y exportarlos, y echara bastante tiempo, pero ninguno trascendió.

Vuelvo con nuevos vigores a probar ideas. 



### dump

formato de `estado`:
|· · ·|  >  |· N ·|
|· · ·|  >  |W O E|
|· · ·|  >  |· S ·|
 i) mapa {N -> [(0.5,0.0)*F]} 
ii) "1EON,2NOS" 



class InputManager:

    def __init__(self):
        self.acciones = {'left': [pg.K_a, pg.K_LEFT],
                         'right': [pg.K_d, pg.K_RIGHT],
                         'jump': [pg.K_w, pg.K_UP]}

        self.key_press = {accion: False for accion in self.acciones}
        self.key_down = {accion: False for accion in self.acciones}
        self.key_up = {accion: False for accion in self.acciones}

    def __str__(self):
        o = f'PRESS: {self.key_press}\nDOWN:  {self.key_down}\nUP:    {self.key_up}\n'
        return o

    def update(self):

        for accion in self.key_down:
            self.key_down[accion] = False
        for accion in self.key_up:
            self.key_up[accion] = False

        _pressed = pg.key.get_pressed()
        for accion, keys in self.acciones.items():
            self.key_press[accion] = any(_pressed[key] for key in keys)

        for event in pg.event.get():
            self.check_exit(event)

            if event.type == pg.KEYDOWN:
                for accion, keys in self.acciones.items():
                    if event.key in keys:
                        self.key_down[accion] = True

            if event.type == pg.KEYUP:
                for accion, keys in self.acciones.items():
                    if event.key in keys:
                        self.key_up[accion] = True


            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # clic izquierdo
                    if pg.key.get_mods() & pg.KMOD_SHIFT:
                        self.acciones['ci_mod'] = True
                    else:
                        self.acciones['ci'] = True
                if event.button == 2:  # clic derecho
                    if pg.key.get_mods() & pg.KMOD_SHIFT:
                        self.acciones['cd_mod'] = True
                    else:
                        self.acciones['cd'] = True


       #         dentro, (iro, path in narco)
        self.estado = [[(0,0) for tile in self.tiles],
                       [(0,0) for tile in self.tiles]]