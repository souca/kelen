
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
