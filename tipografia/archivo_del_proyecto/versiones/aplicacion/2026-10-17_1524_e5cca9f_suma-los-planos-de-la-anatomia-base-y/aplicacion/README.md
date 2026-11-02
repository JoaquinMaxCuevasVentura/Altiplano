# Las decisiones de la letra

Una sola pantalla para discutir la anatomía base de *Contenida* (`../03c_gramatica.md`).

- **A la izquierda, el plano del signo elegido:** la celda con sus cuatro líneas y sus niveles en unidades de la fuente, el cuerpo, los ejes, los nodos, los alivios y las partes. Debajo, sus medidas en milímetros de la placa y en UPM.
- **A la derecha, nueve decisiones de anatomía.** Cada una lleva su porqué y el rombo de su plano (`../planos/`). Al moverla, los 55 signos se rehacen.
- **Abajo, la caja de 8 × 7,** para elegir el signo.

Como el resto de la simulación, es la propuesta de la máquina: **no entra en la caja ni en la fuente.** La letra de la caja la calca la mano desde el pie (`../04_taller_analogico.md`, acciones 3 y 4).

## Por qué es más simple que antes

La aplicación de septiembre tenía cuatro vistas, seis simuladores, veinte parámetros y versiones guardadas. Simulaba los estados (calco, placa, cinta, frotado, agua, voz) que ahora hace la mano. Quedó lo que corresponde a la concepción formal:

| Antes | Ahora |
|---|---|
| Cuatro vistas: caja, signo, texto y estados | Una mesa: el plano del signo, sus decisiones y la caja |
| Seis simuladores (`simuladores.js`) | Ninguno: los estados los hace la mano |
| Veinte parámetros, en tres grupos | Nueve decisiones que la mano puede discutir; lo que fija el material, en una lista aparte |
| El signo sin medidas de la fuente | Las cotas en mm y en UPM, los niveles (el fondo es ±0) y los lados de la celda |
| Clipper desde un CDN | `clipper.js`, en la carpeta: abre sin conexión |

## Las nueve decisiones

| Decisión | Parámetro | De la obra | Plano |
|---|---|---|---|
| La altura de x | `razon_x` | 1,71 de las ascendentes (la foto del pie) | P-01 · 4 |
| El contraste: ninguno | `canal` | 8,9 mm: la media entre el grueso y el fino de la o del pie | P-02 · 1 |
| La panza: el fondo plano | `trapecio` | 0,70 del ancho mayor | P-03 · 2 |
| La panza: la pared | `pared` | 0,55 | P-03 · 2 |
| El hombro: la tensión | `hombro` | superelipse, n = 3 | P-05 · 1 |
| El hombro: dónde arranca | `hombro_caida` | 0,40, a ojo: falta medirlo | P-05 · 3 |
| El asta: el quiebre | `quiebre` | 1,6° por plano | P-04 · 1 |
| Los remates: la intemperie | `intemperie` | 0,12 canal | P-02 · 3 |
| El terminal: la gota | `gota_masa` | 1,25 canal | P-06 · 2 |

**Lo que no se mueve** lo fija el material o una regla: el radio de la chapa (0,6 canal), el desagüe (3 mm, el surco del punzón), el alivio, el asiento, los tres planos, el gancho a 105°, la caída y el cuello de la gota, el sifón y la cinta.

## Cómo se abre

- **Sin servidor:** abre `index.html` en el navegador. Las fuentes las toma de `../laminas/fuentes/`; si el navegador no las carga desde el disco, usa las del sistema, y la página funciona igual.
- **Con servidor,** desde `tipografia/`:

  ```bash
  cd tipografia && python3 -m http.server 8000
  # y abre http://localhost:8000/aplicacion/
  ```

Los ajustes quedan guardados en ese navegador, nada más.

## De la página a Python

1. Mueve las decisiones.
2. Descarga `parametros.json`. Solo van los ajustes; el resto sigue saliendo del pie y de la obra.
3. Corre:

   ```bash
   python3 tipografia/simulacion/gramatica.py --parametros parametros.json
   ```

El botón *El plano en SVG* descarga el plano del signo a escala: 4 px del lienzo son 1 mm de la placa.

**La gramática de la página es la de Python.** `gramatica.js` es `simulacion/gramatica.py` portada a JavaScript, con el mismo azar de las recetas. Con los mismos ajustes, los contornos de los 55 signos coinciden con los de Python: la diferencia es de 0,16 % del área en la mediana, y de 0,8 % en el peor caso (los paréntesis).

## Archivos

| Archivo | Qué es |
|---|---|
| `index.html` | La página |
| `app.js` | La mesa: el plano, las decisiones, la caja y las salidas |
| `gramatica.js` | La gramática: achatar el pie, medirlo, el esqueleto, los parámetros, el taller, las 55 recetas y el cuerpo |
| `clipper.js` | Clipper 6.4.2 (Angus Johnson; traducción a JavaScript de Timo), para unir y engrosar polígonos. Licencia Boost 1.0, en la cabecera del archivo |
| `datos.js` | Generado: los 30 testigos del pie, sus medidas, la razón de la foto, la caja, las recetas, los parámetros y el azar de cada receta |
| `exportar.py` | Regenera `datos.js`. Con `--prueba RUTA` escribe también los cuerpos de Python, para comparar |

Si cambia el pie o la gramática en Python:

```bash
python3 tipografia/aplicacion/exportar.py
```

Hecho con asistencia de IA.
