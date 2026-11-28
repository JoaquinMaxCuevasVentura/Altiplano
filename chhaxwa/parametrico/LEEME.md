# Exploración paramétrica: el piloto en las seis

El autor pidió explorar las seis exploraciones de forma paramétrica y generativa mientras se dibujan los detalles, y empezar por E5, la casa de la bóveda. Aquí la bóveda se vuelve una función de sus reglas de construcción: el guion genera cientos de variantes, revisa cuáles se pueden construir en la casa de la novela y elige las mejores. El 28 de noviembre, con E5 resuelta, el piloto pasó a las otras cinco (más abajo). El resultado y lo que queda por decidir están en `../exploraciones.md` y en el documento (páginas de la serie P).

## E5: las dos familias

**Hiladas voladas** (`boveda_e5.py`). Es la bóveda de E5 tal como está modelada: cada hilada vuela un poco más que la de abajo. Cambian el arranque, el vuelo de la primera hilada y el de la última, en 825 variantes. Cada una tiene que cumplir tres reglas:

- **A.** La clave, con sus lajas, no pasa de 2 m, la altura de las casas de la novela (p. 30).
- **C.** El relleno carga las colas de todas las hiladas menos la última y deja un parapeto de 30 cm (proyecto).
- **K.** La rendija de la clave no pasa de 50 cm, para que una laja de 75 cm apoye 12 cm de cada lado (proyecto).

Lo que vuela el adobe sin caerse lo mide la prueba 3. Mientras no se sepa, se prueban tres escenarios: 12 cm, un tercio del largo del adobe (13,3 cm) y 15 cm.

**Bóveda verdadera** (`boveda_e5_verdadera.py`). El autor la pidió para compararla, con la foto de un arco de adobe de dovelas, cada adobe con la junta hacia el centro (la foto no está en el repositorio). Después la descartó, y E5 sigue volando hiladas, como las otras obras. Hay tres tipos: de medio punto, catenaria y rebajada. El anillo mide 10, 20 o 40 cm según cómo se ponga el adobe de 40 × 20 × 10 cm, y en total son 258 variantes. Una bóveda verdadera empuja hacia los lados, así que la regla de vuelo se cambia por una de equilibrio:

- **E.** Tiene que caber una línea de presiones, el camino de los empujes, dentro del espesor del anillo.
- **S.** La resultante de media casa tiene que caer dentro de la base del muro.

La cuenta es plana, por metro de bóveda, con el relleno de tierra cargando los riñones. Mide solo el equilibrio: no la resistencia del adobe ni el deslizamiento de las juntas. Los pesos son supuestos del proyecto, sin medir: adobe 18, tierra 16 y piedra 20 kN/m³.

## Las otras cinco

Cada exploración tiene su guion, con sus parámetros, sus reglas y su corte, y todos usan `piloto.py`, que escribe la tabla, dibuja el campo y arma la lámina con la matriz de cortes. Las reglas que dependen de cuánto vuela una pieza se prueban con los tres escenarios de E5, ahora como fracción del largo de la pieza: 0,30, un tercio y 0,375. Una regla marcada «proyecto» es una decisión sin fuente, que el autor puede cambiar.

| Exploración | Guion | Qué cambia | Las reglas |
|---|---|---|---|
| E1. La montaña | `montana_e1.py` | El radio al pie del cono, el de la cámara y el vuelo de cada hilada: 324 variantes | **T**, el talud no pasa de 40°, el que supone la prueba 1; **C**, detrás de cada piedra que vuela quedan sus 40 cm de cola. Lleva un collar de 40 cm alrededor del óculo |
| E2. El corral | `corral_e2.py` | El diámetro del corral, el alto del cono y cómo se apoyan las fajas: dieciséis pares con correas o sin ellas, o 32 pares; 189 | **P**, la pendiente es de 45° o más, la de la prueba 4; **S**, la faja cruza 70 cm o menos entre apoyos, como en el techo de Šolc (prueba 4) |
| E3. La casa redonda | `cupula_e3.py` | El radio del cuarto, el alto de la pirca y cómo vuela la cúpula: 360 | **K**, la pirca es al menos tan alta como el paso de 96 cm de la prueba 3 y su laja; **C**, el relleno cubre la cola de cada hilada |
| E4. La chullpa | `chullpa_e4.py` | El vuelo de la cámara, el retiro de la pirámide y la pieza del forro: 140 | **C**, la cola del forro cabe en el relleno; **T**, sobre la laja de cierre queda una hilada; **R**, la hilada no se retira más de 7 cm, la mitad del fondo del adobito (proyecto) |
| E6. La *pirwa* | `pirwa_e6.py` | El vuelo de la V y el alto del depósito: 100 | **P**, la clave queda a 1,70 m o más, para estar de pie bajo la trampa (proyecto); **E**, el lado alto no pasa de 4,6 m, el que aceptó el autor |

El 28 de noviembre se aplicaron los resultados: E1 pasó a la variante elegida, E2 lleva correas, la cúpula de E3 vuela de 8 a 12 cm y la cámara de E4, 4 cm. En cada guion, `ACTUAL` es la variante de ahora y `ANTES`, la de antes del piloto.

En los campos, el gris mide lo que cada exploración gasta o da: la piedra del cono, la queñua del techo, el área de pie, el volumen de la cámara o lo que se guarda. En blanco quedan las variantes que fallan una regla, con su letra, y con una V las que cumplen la forma pero piden que la pieza vuele más de un tercio de su largo.

Algunas medidas son supuestos que una prueba va a medir: los 0,44 m³ de piedra por parcela y el talud de 40° de la prueba 1, la pendiente de 45° de la prueba 4 y lo que vuela cada pieza en la prueba 3. Cuando las pruebas den sus números, basta cambiar la constante en el guion y volver a correrlo.

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
| `piloto.py` | Las piezas comunes de las otras cinco: la tabla, el campo y la lámina-matriz |
| `montana_e1.py`, `corral_e2.py`, `cupula_e3.py`, `chullpa_e4.py`, `pirwa_e6.py` | Los guiones de E1, E2, E3, E4 y E6 |
| `todas.py` | Corre los cinco guiones, uno tras otro |
| `e1_variantes.csv` … `e6_variantes.csv` | Las variantes de cada una, con sus medidas y las reglas que cumplen |
| `e1_campo.png` … `e6_campo.png` | P6, P8, P10, P12 y P14: el campo de cada una |
| `e1_matriz.dxf` … `e6_matriz.dxf`, y sus `.png` | P7, P9, P11, P13 y P15: la matriz de cortes de cada una, a 1:100 (E2, a 1:200) |

## Cómo se rehace

Desde la raíz del repositorio:

```bash
python3 chhaxwa/parametrico/boveda_e5.py                      # pip install ezdxf shapely matplotlib
venv_bpy/bin/python chhaxwa/parametrico/boveda_e5_nodos.py    # pip install bpy==5.0.1, Python 3.11
python3 chhaxwa/parametrico/todas.py                          # E1, E2, E3, E4 y E6; o cada guion por separado
```

Las láminas usan las capas y los grosores de `../detalles/dibujar_detalles.py`, y un DXF que no cambia no se reescribe. El número de hiladas sale de la misma cuenta que en `../blender/formas.py`. En el empate, cuando la cuenta da justo media hilada, se toma el entero de abajo, como con los 12,5 de E5.
