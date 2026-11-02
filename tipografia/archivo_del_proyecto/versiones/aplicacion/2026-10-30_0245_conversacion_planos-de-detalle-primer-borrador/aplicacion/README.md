# Las decisiones de la letra

Una mesa para discutir la anatomía base de *Contenida* (`../03c_gramatica.md`), dibujada con las convenciones de sus planos (`../planos/`).

- **A la izquierda, el plano del signo elegido:** la celda con sus cuatro líneas y sus niveles en unidades de la fuente, el cuerpo, los ejes, los nodos, los alivios y las partes. Debajo, sus medidas en milímetros de la placa y en UPM.
- **A la derecha, siete planos de detalle, uno por parte de la anatomía.** Cada decisión se mueve en su propio dibujo: se toma el asa (el círculo) y se arrastra. Con el teclado, las flechas la mueven de a un paso (con Mayús, de a diez), Inicio y Fin la llevan a los extremos, y Supr o Esc la devuelven a la obra. Al soltar, los 55 signos se rehacen.
- **Abajo, la caja de 8 × 7,** para elegir el signo.

Como el resto de la simulación, es la propuesta de la máquina: **no entra en la caja ni en la fuente.** La letra de la caja la calca la mano desde el pie (`../04_taller_analogico.md`, acciones 3 y 4).

## Una interfaz hecha para esta letra

No es un panel de deslizadores. En *Contenida*, la anatomía se discute en planos: niveles, cortes, cotas, ejes y la gravedad en lugar del norte. Por eso las decisiones se mueven ahí, cada una con el gesto de su dibujo:

- el nivel del borde sube y baja;
- el corte del canal se ensancha;
- la pared de la cuenca se tira de su tirador;
- el asta se quiebra;
- el hombro se tensa;
- la gota se estira hacia abajo, por su peso;
- el radio del desgaste se acota desde su centro.

Cada dibujo usa las fórmulas de la gramática (`gramatica.js`), así que lo que se mueve en él es lo que cambia en la letra.

La convención es la de la caja:

- **En gris metal,** la letra como queda.
- **Encima, su eje o su contorno:** en tinta y continuo, la obra; en violeta y a puntos, lo que se aparta de ella, como lo reconstruido.
- **El asa:** queda en tinta mientras la decisión es la de la obra, y se llena de violeta cuando se aparta.

La idea de hacer el control a la medida del proyecto viene de un reel de Aimeric sobre *Ultravaria*, una tipografía paramétrica de veinte ejes con una interfaz inventada para ella. **Se toma el método, no la interfaz:** el video se cita, no se sube.

## Los siete dibujos

| Dibujo | Plano | Qué se ve | Qué se mueve | La decisión y la obra |
|---|---|---|---|---|
| La celda y sus niveles | P-01 · 4 | La n y la l a su altura, las líneas de la celda y sus niveles en UPM | El nivel del borde, arriba y abajo | `razon_x`: 1,71 de las ascendentes (la foto del pie) |
| El canal | P-02 · 1 | El corte A–A del aluminio y una tira en planta, a 1,9 | El borde del surco, hacia los lados | `canal`: 8,9 mm, la media entre el grueso y el fino de la o del pie |
| La cuenca | P-03 · 2 | La o a su tamaño, con su eje, el desagüe y el nivel del fondo | La esquina del fondo, hacia los lados; el tirador de la pared, arriba y abajo | `trapecio`: 0,70 del ancho mayor · `pared`: 0,55 |
| El fuste | P-04 · 1 | La l en tres planos, con su corte y su asiento; los desvíos, × 10 como en el plano | El quiebre del primer plano | `quiebre`: 1,6° por plano |
| El hombro | P-05 · 1 · 3 | La n a 1,1, con los arcos de n = 2 y n = 5 en gris | El punto del arco a 45°; el arranque, en la pata | `hombro`: n = 3 · `hombro_caida`: 0,40, a ojo (falta medirlo) |
| La gota | P-06 · 2 | El gancho de la a, su gota y la gravedad | El fondo de la gota, hacia abajo | `gota_masa`: 1,25 canal |
| La intemperie | P-02 · 3 | La punta del fuste, × 8, con su línea de corte | El centro del radio, en diagonal | `intemperie`: 0,12 canal |

**Lo que no se mueve** lo fija el material o una regla, y va en una lista aparte:

- el radio de la chapa (0,6 canal);
- el desagüe (3 mm, el surco del punzón);
- el alivio y el asiento;
- los tres planos;
- el gancho a 105°;
- la caída y el cuello de la gota;
- el sifón y la cinta.

## Por qué es más simple que la de septiembre

La aplicación de septiembre simulaba los estados (calco, placa, cinta, frotado, agua, voz) que ahora hace la mano. Quedó lo que corresponde a la concepción formal:

| Septiembre | Ahora |
|---|---|
| Cuatro vistas: caja, signo, texto y estados | Una mesa: el plano del signo, siete planos de detalle y la caja |
| Seis simuladores (`simuladores.js`) | Ninguno: los estados los hace la mano |
| Veinte parámetros en tres grupos, con deslizadores | Nueve decisiones, cada una en el dibujo de su parte; lo que fija el material, en una lista aparte |
| El signo sin medidas de la fuente | Las cotas en mm y en UPM, los niveles (el fondo es ±0) y los lados de la celda |
| Clipper desde un CDN | `clipper.js`, en la carpeta: abre sin conexión |

## Cómo se abre

- **En línea:** el artefacto de Claude [«Gramática de Contenida»](https://claude.ai/artifact/MD4hC81MMftYgHHB1RT9bL), privado (se comparte desde su menú). Es la misma página, pero ahí:
  - las fuentes vienen de Google Fonts y Clipper, de jsDelivr;
  - las descargas pasan por el visor, que pide confirmación.
- **Sin servidor:** abre `index.html` en el navegador. Las fuentes las toma de `../laminas/fuentes/`; si el navegador no las carga desde el disco, usa las del sistema, y la página funciona igual.
- **Con servidor,** desde `tipografia/`:

  ```bash
  cd tipografia && python3 -m http.server 8000
  # y abre http://localhost:8000/aplicacion/
  ```

Los ajustes quedan guardados solo en ese navegador.

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
| `app.js` | La mesa: el plano, los siete dibujos con sus asas, la caja y las salidas |
| `gramatica.js` | La gramática: achatar el pie, medirlo, el esqueleto, los parámetros, el taller, las 55 recetas y el cuerpo |
| `clipper.js` | Clipper 6.4.2 (Angus Johnson; traducción a JavaScript de Timo), para unir y engrosar polígonos. Licencia Boost 1.0, en la cabecera del archivo |
| `datos.js` | Generado: los 30 testigos del pie, sus medidas, la razón de la foto, la caja, las recetas, los parámetros y el azar de cada receta |
| `exportar.py` | Regenera `datos.js`. Con `--prueba RUTA` escribe también los cuerpos de Python, para comparar |

Si cambia el pie o la gramática en Python:

```bash
python3 tipografia/aplicacion/exportar.py
```

Hecho con asistencia de IA.
