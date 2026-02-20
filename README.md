
# Kēlen

Hace mucho tiempo, caí en una web que hablaba del [Kēlen](https://www.terjemar.net/kelen/lajathin.php), un lenguaje inventado por Lydia Sotomayor, que tenía un curioso sistema de escritura ceremonial compuesto de lazos. 

Hiciera unos cuantos sketches en Processing para pintarlos y exportarlos, y echara bastante tiempo, pero ninguno trascendió.

Vuelvo con nuevos vigores a probar ideas. 

***

<p align="center">
<img src="https://github.com/souca/kelen/blob/main/screenshots/kelen_v2.png" width="676" height="630" />
</p>
***

Podemos dibujar las dos trenzas en el tablero.
- `clic` sobre un tile rota los posibles caminos de la trenza 1
- `[shift]+clic` para la trenza 2
El color del trazo lo define el `current_iro`, que se cambia con `espacio`.
- `s` cambia el over-under
- `w` activa un anchor point
- `p` modo debug (whatever that is)

if self.g.input.acciones['anchor']:
    anchor = self.find_anchor_near_mouse(_idx, _mpos)

    if anchor is None:
        return

    # Toggle anchor actual
    ap = self.tiles[_idx]['anchor_points']
    ap[anchor] = not ap[anchor]

    # Toggle anchor opuesto en el vecino
    vecino_idx = self.neighbor_index(_idx, anchor)
    if vecino_idx is None:
        return

    ap_vecino = self.tiles[vecino_idx]['anchor_points']
    ap_vecino[OPPOSITE[anchor]] = not ap_vecino[OPPOSITE[anchor]]

    ***


0 = 1 << 0
N = 1 << 1
S = 1 << 2
W = 1 << 3
E = 1 << 4

# tile con todos las anclas apagadas
anchor_points = 0b00000

# tile con el ancla W encendida
anchor_points = W

# tile con el ancla W y S encendida
anchor_points = W | S

# tile con todas las anclas encendidas
anchor_points = 0 | W | E | N | S

# comprobación de si E está activo
anchor_points & E

# activar el ancla E
anchor_points |= E

# desactivar el ancla W
anchor_points &= ~W

# flipar el ancla S
anchor_points ^= S

# con este mapa
ANCHOR_BIT = {'n': N, 'w': W, 'e': E, 'o': O, 's': S}
# podemos hacer
tile.anchor_points ^= ANCHOR_BIT[anchor]

***

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