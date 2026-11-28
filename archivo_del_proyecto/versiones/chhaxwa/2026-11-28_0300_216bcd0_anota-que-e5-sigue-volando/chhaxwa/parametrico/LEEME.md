# Exploración paramétrica: el piloto en E5

El autor pidió explorar las seis exploraciones de forma paramétrica y generativa mientras se dibujan los detalles, y empezar por E5, la casa de la bóveda. Aquí la bóveda se vuelve una función de sus reglas de construcción: el guion genera cientos de variantes, revisa cuáles se pueden construir en la casa de la novela y elige las mejores. El resultado y lo que queda por decidir están en `../exploraciones.md` y en el documento (páginas de la serie P).

## Las dos familias

**Hiladas voladas** (`boveda_e5.py`). Es la bóveda de E5 tal como está modelada: cada hilada vuela un poco más que la de abajo. Cambian el arranque, el vuelo de la primera hilada y el de la última, en 825 variantes. Cada una tiene que cumplir tres reglas:

- **A.** La clave, con sus lajas, no pasa de 2 m, la altura de las casas de la novela (p. 30).
- **C.** El relleno carga las colas de todas las hiladas menos la última y deja un parapeto de 30 cm (proyecto).
- **K.** La rendija de la clave no pasa de 50 cm, para que una laja de 75 cm apoye 12 cm de cada lado (proyecto).

Lo que vuela el adobe sin caerse lo mide la prueba 3. Mientras no se sepa, se prueban tres escenarios: 12 cm, un tercio del largo del adobe (13,3 cm) y 15 cm.

**Bóveda verdadera** (`boveda_e5_verdadera.py`). El autor la pidió para compararla, con la foto de un arco de adobe de dovelas, cada adobe con la junta hacia el centro (la foto no está en el repositorio). Después la descartó, y E5 sigue volando hiladas, como las otras obras. Hay tres tipos: de medio punto, catenaria y rebajada. El anillo mide 10, 20 o 40 cm según cómo se ponga el adobe de 40 × 20 × 10 cm, y en total son 258 variantes. Una bóveda verdadera empuja hacia los lados, así que la regla de vuelo se cambia por una de equilibrio:

- **E.** Tiene que caber una línea de presiones, el camino de los empujes, dentro del espesor del anillo.
- **S.** La resultante de media casa tiene que caer dentro de la base del muro.

La cuenta es plana, por metro de bóveda, con el relleno de tierra cargando los riñones. Mide solo el equilibrio: no la resistencia del adobe ni el deslizamiento de las juntas. Los pesos son supuestos del proyecto, sin medir: adobe 18, tierra 16 y piedra 20 kN/m³.

## Los archivos

| Archivo | Qué es |
|---|---|
| `boveda_e5.py` | El guion: las hiladas voladas, los escenarios, el campo y las láminas P2 y P3. Al final llama a `boveda_e5_verdadera.py` |
| `boveda_e5_verdadera.py` | La bóveda verdadera, la línea de presiones y la lámina P4 |
| `boveda_e5_nodos.py` | Arma la bóveda en Geometry Nodes, comprueba que da lo mismo que el cálculo y guarda el `.blend` |
| `e5_variantes.csv`, `e5_variantes_verdaderas.csv` | Todas las variantes con sus medidas y las reglas que cumplen |
| `e5_campo.png` | P1: el campo de las 825 variantes de hiladas voladas |
| `e5_matriz.dxf` y `.png` | P2: veinticuatro variantes a 1:100 |
| `e5_elegidas.dxf` y `.png` | P3: la mejor de cada escenario, a 1:50 |
| `e5_verdaderas.dxf` y `.png` | P4: la E5 actual y la mejor bóveda verdadera de cada tipo, con su línea de presiones, a 1:50 |
| `e5_parametrica.blend` | El grupo de nodos «Bóveda de E5» y cuatro objetos que lo usan. Se abre en Blender, se elige un objeto y se mueven los controles del modificador |
| `e5_nodos.jpg` | P5: render de los cuatro objetos. Es un render de Blender, no una foto |

## Cómo se rehace

Desde la raíz del repositorio:

```bash
python3 chhaxwa/parametrico/boveda_e5.py                      # pip install ezdxf shapely matplotlib
venv_bpy/bin/python chhaxwa/parametrico/boveda_e5_nodos.py    # pip install bpy==5.0.1, Python 3.11
```

Las láminas usan las capas y los grosores de `../detalles/dibujar_detalles.py`, y un DXF que no cambia no se reescribe. El número de hiladas sale de la misma cuenta que en `../blender/formas.py`. En el empate, cuando la cuenta da justo media hilada, se toma el entero de abajo, como con los 12,5 de E5.
