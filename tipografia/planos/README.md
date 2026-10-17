# Los planos de la anatomía base

Once láminas A3 que dibujan la concepción formal de *Contenida* con la precisión de un plano de arquitectura: cotas, ejes, niveles, cortes, detalles y cajetín. A la derecha de cada lámina, **el porqué de cada decisión de anatomía tipográfica**: contraste, ojo, apertura, terminales, remates, hombro, sobrepaso… Cada decisión tiene un número en un rombo, que aparece también en el dibujo, en el lugar de la letra donde ocurre. Su razón se da en tres niveles:

- **concepto:** las decisiones de la obra, D1 … D16 (`../01_la_obra_decision_por_decision.md`);
- **retórica:** la figura que la sostiene;
- **poética:** el verso del poema con que rima, sin tocarlo.

**Es la concepción formal, no la letra.** La mano calca el esqueleto del pie aplicando estas reglas (Acción 3), repuja (Acción 4) y sigue con los estados. Lo que la placa contradiga se anota en el laboratorio de discrepancias (`../05_migracion_digital.md`, §5.6). No se corrige la placa para que se parezca al plano. Como toda la simulación, es la propuesta de la máquina: **no entra en la caja ni en la fuente.**

**Descarga:** [`contenida_planos.pdf`](contenida_planos.pdf), once páginas A3 apaisadas. Impresas al 100 %, las vistas a 1:1 se pueden medir con regla.

## Las láminas

| Lámina | Qué dibuja | Escalas | Decisiones |
|---|---|---|---|
| [P-00](png/P-00_indice.png) | Índice, convenciones y el cuadro de las 24 decisiones anatómicas | — | lo hallado y lo reconstruido; las tres reglas de la gravedad |
| [P-01](png/P-01_celda.png) | La celda y las cuatro líneas, en la placa de 150 mm | 1:1 · 1:3 | el cuerpo (la celda de la cabeza); el ancho (monoespaciada); las líneas (nombres de vasija); la altura de x (1,71) |
| [P-02](png/P-02_canal.png) | El canal y la chapa: el radio mínimo, lo que no se hace, los cortes A–A y B–B, la intemperie | 2:1 · 5:1 | contraste: ninguno; la curva mínima; remates: ninguno; el desagüe; el relieve |
| [P-03](png/P-03_o_cuenca.png) | **o · la cuenca**, con la pared, el desagüe y cómo se construye | 1:1 · 2:1 · 4:1 · 1:2 | el ojo, arriba; la panza, abajo; el sobrepaso; la apertura; el eje |
| [P-04](png/P-04_l_fuste.png) | **l · el fuste**, con el quiebre y el asiento | 1:1 · 2:1 · 1:2 | el asta en tres planos; arriba, un corte; abajo, el asiento |
| [P-05](png/P-05_n_hombro.png) | **n · el hombro**, con la familia de arcos y el encuentro tangente | 1:1 · 2:1 · 1:2 | la superelipse; el arranque tangente; la altura del arranque; la bajada |
| [P-06](png/P-06_a_gancho_y_gota.png) | **a · el gancho y la gota**, con la construcción de la gota | 1:1 · 5:1 · 1:2 | el gancho a 105°; la gota; el ojo que se abre; la a de dos pisos |
| [P-07](png/P-07_partes.png) | El cuadro de las doce partes, como el cuadro de aberturas de un plano | 1:4 | las cinco reglas de la derivación |
| [P-08](png/P-08_detalles.png) | Detalles: punto, tilde, onda, sifón, alivio y la celda de la cifra | 2:1 · 1:2 | seis decisiones de detalle |
| [P-09](png/P-09_dobles_opuestos.png) | Los dobles opuestos: ? ¿ · 6 9 · « », cada par con su comparación | 1:2 | ninguno es el reflejo del otro |
| [P-10](png/P-10_caja.png) | El plan general de la caja de 8 × 7 | 1:5 | solo caja baja; 56 celdas; el orden; el ¶; la puerta |

## Cómo se leen

- **Unidades:** milímetros de la placa y, entre paréntesis, unidades de la fuente (UPM). La celda mide 136,7 mm de alto, que son 1000 UPM. Los niveles se miden desde el fondo, que es el ±0, como el piso terminado de un plano.
- **Líneas:** contorno continuo para lo hallado y a puntos, en violeta, para lo reconstruido; eje de trazo y punto; líneas de la gramática a trazos; construcción y comparación en gris.
- **Rellenos:** el cuerpo de la letra, rayado a 45° como el metal en corte; la base blanda del repujado, punteada.
- **Símbolos:** la llamada de vista o detalle (número arriba, lámina abajo), el nivel, la escala gráfica y, en lugar del norte, **la gravedad**: solo gotea lo que mira abajo.

## Lo que los planos encontraron

Medir es también discutir. Al acotar sobre el cuerpo, y no sobre las reglas, aparecieron dos cosas:

1. **La gota de la a deja 2,2 mm libres, no 3,5.** La regla pide 0,4 canal entre la gota y la cuenca, pero lo mide desde la gota sin estirar; estirada 1,15 por su peso, quedan 2,2 mm. Está acotado en P-06 y anotado en `../03c_gramatica.md`, §7. La placa dirá si alcanza.
2. **El quiebre se describía mal.** Cada plano del asta se aparta 1,6° del eje: entre el primero y el segundo hay 3,2°, y entre el segundo y el tercero, 1,6°. Se corrigió la descripción en `gramatica.py` y en `03c`; la forma no cambió.

## Archivos

| Archivo | Qué es |
|---|---|
| `generar_planos.py` | Arma las once láminas, el PDF, las vistas previas y los DXF |
| `geometria.py` | Corre la gramática y anota lo que se acota: contornos, ejes, nodos, marcas, alivios, el testigo del pie y los puntos de construcción de los cuatro generadores |
| `dibujo.py` | El dibujo técnico: la hoja A3, los tipos de línea, las cotas, los niveles, la llamada, la gravedad, el cajetín y la columna del porqué |
| `por_que.py` | **El porqué de cada lámina**, separado del dibujo para corregirlo sin tocar el código |
| `svg/` | Las once láminas en SVG, en milímetros |
| `png/` | Vistas previas, a 110 ppp |
| `dxf/` | Para CAD, en milímetros reales, con el origen en el fondo y el borde izquierdo de la celda (como en la fuente). Capas: CONTORNO, RECONSTRUIDO, EJE, LINEAS, CELDA, PLACA, NODOS, ALIVIOS, COTAS y TEXTO. Están la celda (P-01), los cuatro generadores (P-03 a P-06) y la caja completa (P-10) |
| `contenida_planos.pdf` | Las once láminas, una por página, en A3 |

Para rehacerlos (unos treinta segundos):

```bash
pip install ezdxf pymupdf shapely opencv-python-headless scipy pillow fonttools brotli
python3 tipografia/planos/generar_planos.py
```

Con `--cache RUTA.json` la geometría se guarda la primera vez y se lee las siguientes. Con `--solo P-03` se rehace una lámina. El PDF necesita Chromium o Chrome.

## Herramientas que se miraron

Antes de dibujar se buscó si ya existía una herramienta para esto:

| Herramienta | Qué es | Por qué no, o para cuándo |
|---|---|---|
| [Prototypo](https://github.com/byte-foundry/prototypo) | Diseño paramétrico de tipografías en el navegador | Su motor lleva años sin cambios, y sus parámetros son los de una romana (remates, contraste), no los de esta obra |
| [Metapolator](https://github.com/metapolator/metapolator) | Interpolación paramétrica sobre METAFONT (GPLv3) | Interpola pesos y estilos: aquí los estilos son estados hechos a mano, y no se interpola nada (`05`, §5.7) |
| [Metaflop](https://github.com/metaflop/metaflop) | Fuentes paramétricas en el navegador, con METAFONT | Igual que Prototypo: sus parámetros son los de otra anatomía |
| METAFONT (Knuth) y MetaPost | Describir la letra como el recorrido del centro de una pluma | Es la idea más cercana a la gramática: un eje y un trazo de ancho fijo, como el punzón. Se tomó la idea, no la herramienta |
| [Fontra](https://github.com/fontra/fontra) | Editor de fuentes libre, activo, en el navegador (GPLv3) | **Para la etapa digital**, si se migra: abre UFO y sirve para revisar los contornos vectorizados de los calcos (`05`, §5.6) |
| [drawbot-skia](https://github.com/justvanrossum/drawbot-skia) | Dibujo con Python a PDF y SVG | Habría servido para las láminas; se prefirió SVG directo para no sumar dependencias |
| [ezdxf](https://github.com/mozman/ezdxf) | Lee y escribe DXF desde Python, con cotas | **Se usa** para los DXF |

Ninguna herramienta trae las reglas de esta obra: el desagüe, la gota a plomada, la superelipse de la chapa, el alivio del aluminio. Por eso los planos salen de la gramática misma.

Hecho con asistencia de IA: la máquina dibujó los planos y redactó los textos desde los documentos del proyecto.
