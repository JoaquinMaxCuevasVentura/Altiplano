# 2. Contenedor: traducir la obra en estructuras

El 27 de septiembre de 2026 pediste una tipografía hecha con traducciones formales de *Contener una ruina: acciones para desenterrar una voz* (Rebeca Paz con CreaciónxAcuerpamiento, Artefacto Tatuajes, Sopocachi, La Paz, 22 de agosto de 2026) y del poema que escribiste después. Dejaste abierta una duda: si desarrollar conceptos que definan estructuras en lugar de definir formas.

**Resultado.** Hay una fuente que funciona, Contenedor 0.100, variable, con cinco ejes, cuatro versiones de cada letra y tres juegos estilísticos. Ninguna letra se dibujó a mano: todas se deducen de las reglas de este documento, escritas como programa en `fuente/`.

**Sobre los libros.** Anunciaste seis libros técnicos, pero llegó uno solo: Kimberly Elam, *Typographic Contrast, Color, & Composition: A Graphic Design Project Guide* (2009). Lo que viene de Elam lleva página: el folio impreso, que en el PDF es el número de página menos cuatro. Lo que viene de otras fuentes técnicas va marcado como conocimiento general, sin página, porque no lo cotejé con los libros que no llegaron.

## 2.1. ¿Estructuras o formas?

**Recomendación: estructuras primero y la forma como prueba.** Tres razones:

1. **La obra es una cadena de traducciones en la que ninguna forma sobrevive.** Piedra borrada, fotografía, dibujo, escaneo, repujado, cuerpo, video, charco, pared. Lo que pasa de un eslabón al siguiente es una estructura: una distribución de placas sobre un cuerpo, una retícula, un bucle. Una tipografía de formas fijas contradiría esa lógica. Una tipografía de reglas deja que cada vuelta salga distinta.
2. **La forma de base es prestada a propósito.** El esqueleto de las letras es la matriz de 5 × 7 de las impresoras de matriz y las pantallas de caracteres: la letra con que las máquinas imprimían registros, inventarios y fichas. Todos los archivos funcionan así. Esa forma anónima es la piedra; lo que la fuente le agrega es la opinión sobre ella. No se salvó la piedra, solo la opinión sobre ella.
3. **Las herramientas técnicas ya son estructuras.** Un eje variable es una regla de transformación; una función OpenType es una regla de sustitución. Permiten diseñar comportamientos y no solo figuras (conocimiento general).

**El límite.** Una estructura sin prueba formal termina en una letra genérica. Por eso cada regla tiene que cumplir dos condiciones: salir de algo verificable en la obra o en el poema, y pasar una prueba de lectura. Elam pone esa condición a su propio ejercicio: cada número debe ser legible (p. 2). La prueba también puede fallar a propósito: con la boca tapada el texto se lee; con los ojos tapados, no (§ 2.3).

## 2.2. Las traducciones

| En la obra o en el poema | Estructura tipográfica | Dónde está en la fuente | Apoyo técnico |
|---|---|---|---|
| La piscina vacía. «Quedó el contenedor / de lo que ya no está» | La celda es el contenedor: todas las letras ocupan lo mismo, seis azulejos. La i deja vacía casi toda la suya | Monoespaciada, 600 unidades de ancho | Elam, contraste de escala (p. 26) |
| La retícula de azulejos de la piscina | Retícula de 5 columnas y 9 filas: altura de x de 5 filas, mayúsculas de 7, descendentes de 2. El azulejo mide 100 unidades | `glifos.py` | Matriz de 5 × 7 (conocimiento general) |
| Las placas repujadas, sueltas, con piel a la vista entre una y otra | Cada azulejo lleno es una placa. Entre placa y placa queda piel | Parámetro `PIEL`; eje `wght`: Piel (100), Seca (400), Piedra (900) | Elam, contraste de peso (p. 34) |
| «Ningún contenedor aguanta lo que contiene» | Ninguna contraforma se cierra: la piel comunica todo hueco con el exterior | Consecuencia de la regla anterior | En un esténcil, los puentes existen para que la contraforma no se caiga (conocimiento general) |
| El monolito de pie y el vaso acostado | Ancho de la letra: de la tensión vertical de la estela a la horizontal del agua | Eje `wdth`: Monolito (60) a Piscina (150) | Elam, contraste de ancho: el tipo comprimido tiene una fuerte tensión vertical (p. 52) |
| La placa que refleja; el vaso de la piscina | Figura y fondo dentro de la placa: la placa se vacía hasta volverse contenedor | Eje `VASO` (0 a 100) | Elam, contraformas llenas o borradas (p. 11) y el aforismo de Lao-Tse sobre la vasija, citado de Emil Ruder (p. 16) |
| «Tocas el agua y la diosa se deforma». La imagen rebotaba en la bandeja y llegaba temblando a la pared | Cada fila de placas se corre por su cuenta, según una onda con otra fase en cada vuelta | Eje `AGUA` (0 a 100) | Elam: la inclinación se mide contra la línea de base (p. 48) |
| «Moverse como se mueve la piedra, / es decir, apenas, es decir, temblor» | Cada placa se desplaza y gira un poco. Las que tienen un solo vecino (los terminales) se desprenden primero y giran más | Eje `TEMB` (0 a 100) | Elam, contraste de remate (p. 57): donde otras letras tienen serifas, estas tienen terminales sueltos |
| Las baldosas oscuras desprendidas en el fondo, que se leen como peces | Todo punto es un pez: puntos, tildes, diéresis y el punto de la i son azulejos desprendidos, girados 45°. La coma es un pez con cola | Carácter `*` en la retícula; `ACENTOS` | Regla propia |
| «Termina y empieza, / termina y empieza». «Cada vuelta pasa por el agua / y el agua no repite, / la misma diosa dos veces / y ninguna igual» | Cuatro vueltas de cada carácter, con otra mano y otro temblor. La siguiente vuelta depende de la letra anterior, así que la misma palabra repetida casi nunca cae igual | Función `calt`, activa por defecto: «vuelve sin que la llames» | Alternativas contextuales de OpenType (conocimiento general) |
| Bandas del mismo material sobre los ojos y la boca. «A la boca la taparon, a las manos no, / No tiene lengua pero igual dice» | Una banda cruza la parte baja de la altura de x (boca) o la alta (ojos). Con la boca tapada el texto se lee; con los ojos tapados, mucho menos | `ss01` Boca tapada, `ss02` Ojos tapados | Elam: la superposición como señal de profundidad (pp. 5 y 39) y el cierre, que completa lo recortado (p. 13) |
| «La tierra se dio de beber a sí misma». La challa invertida | Donde se juntan tres trazos, la placa se achica: una trampa de tinta. A tamaños chicos la tinta llena el hueco | Parámetro `ARTICULACION` | Elam cierra con la tapa de una guía telefónica (p. 64); la letra de las guías de AT&T, Bell Centennial de Matthew Carter (1978), es el ejemplo clásico de trampas de tinta (conocimiento general) |
| A la piscina le devolvieron su agua, convertida en luz | Cada letra retiene el agua que puede (§ 2.4) y esa agua se dibuja con líneas horizontales, la convención del agua en un corte de arquitectura | `ss03` Agua devuelta, en verde donde el programa sabe de color (tablas COLR y CPAL) | Elam, sistema de color por volúmenes (p. 7) |
| «Al final del ciclo, / de la boca sale un signo / hecho con las manos» | El calderón (¶), que cierra el párrafo, es el signo escalonado. Otros tres ornamentos: pez ◆, placa repujada ■, disco de agua ● | `SIGNOS["¶"]`, `ORNAMENTOS` | Posnansky, *El signo escalonado* (1913) |
| «Quedó el contenedor / de lo que ya no está» | El glifo que aparece cuando falta un carácter (`.notdef`) es una piscina vacía, con las esquinas rectas | `elementos_notdef()` | Regla propia |
| «Desenterrar una voz / es desenterrar la mano del que la escribió» | La mano: cada placa tiene las esquinas irregulares (hasta un 20 % de la semiplaca), un giro de hasta 3,2° y una colocación imperfecta. Cambia en cada vuelta | Parámetros `MANO`, `GIRO_MANO`, `COLOCACION` | Regla propia |
| «Nos fuimos con las manos secas» | La instancia por defecto se llama Seca: sin agua y sin temblor | Instancia `Seca` | Regla propia |

Dos reglas más no tienen verso propio pero sostienen el sistema:

- **El cero guarda un pez.** Es el contenedor de lo que ya no está y todavía conserva un signo. De paso se distingue de la O.
- **La contraforma primero.** En el grabado de punzones, la contraforma se abría antes que la letra, con un contrapunzón (Fred Smeijers, *Counterpunch*, 1996; conocimiento general). Aquí pasa algo parecido: las letras se diseñaron como vasos, y `vasos.py` mide lo que cada una contiene.

## 2.3. El color

Elam propone tres colores medidos por el volumen que ocupan (p. 7): uno dominante, uno subordinado y un acento que ocupa muy poco y que debe tocar su complemento para vibrar.

- **Dominante:** el blanco del azulejo.
- **Subordinado:** el grafito.
- **Acento:** el verde del agua del dibujo, `#4C8C3A`. Es el color que la fuente trae en su paleta.
- **Complemento:** el complemento del verde es el rojo del asperón colorado, la piedra que ya no está. En el muestrario aparece una sola vez, tocando el verde, en la franja de la paleta.

## 2.4. Qué letras contienen

`vasos.py` echa agua sobre cada letra de la retícula. El agua baja o se corre hacia los lados y nunca sube. Donde no puede escapar, queda. El número es la cantidad de azulejos que retiene.

| Caso | Letras (azulejos de agua) |
|---|---|
| **Vaso cerrado:** la contraforma no toca el exterior de la retícula | a 3 · b 9 · d 9 · e 3 · g 9 · o 9 · p 9 · q 9 · A 6 · B 12 · D 15 · O 15 · P 6 · Q 13 · R 6 · 0 15 · 4 3 · 6 6 · 8 12 · 9 6 |
| **Piscina abierta:** retiene agua con la boca al cielo | j 2 · k 3 · r 1 · t 2 · u 12 · v 10 · w 10 · x 4 · y 12 · C 3 · G 7 · H 9 · J 2 · K 6 · M 4 · N 9 · U 18 · V 16 · W 15 · X 7 · Y 7 · 5 3 |
| **Piscina volcada:** retendría agua dada vuelta | h 12 · k 3 · m 8 · n 12 · w 1 · x 4 · A 9 · C 3 · G 3 · H 9 · K 6 · M 13 · N 9 · Q 1 · R 6 · W 1 · X 7 · 2 3 |

Tres lecturas:

- La **u** es la piscina y la **n** es la piscina volcada: la misma forma, antes y después de derramarse.
- Las letras más cerradas (O, D y el cero, 15 azulejos cada una) son las que más contienen. El cero además guarda un pez.
- Ninguna de estas contraformas se cierra de verdad, porque entre placa y placa queda piel.

La tabla completa se regenera con `python3 fuente/vasos.py`.

## 2.5. Lo que Elam aporta y lo que no

Elam no enseña a diseñar tipografías: enseña a componer con familias clásicas ya hechas. Lo que se traslada al diseño de una fuente son cuatro cosas:

| Pasaje | Página | Cómo entra |
|---|---|---|
| Los siete contrastes: figura y fondo, escala, peso, espacio, inclinación, ancho y remate | pp. 1, 16, 26, 34, 39, 48, 52, 57 | Cada contraste se vuelve una estructura de la misma fuente (§ 2.2) |
| El color por volúmenes y el acento que toca su complemento | p. 7 | La paleta (§ 2.3) |
| Las contraformas llenas o borradas; el recorte y el cierre | pp. 11 y 13 | El eje Vaso; las bandas que tapan y dejan leer |
| El método: pocas reglas y un ejercicio engañosamente simple que da resultados muy variados | pp. 1 y 2 | La decisión de trabajar con reglas y no con dibujos |

## 2.6. Lo que falta

- **Los otros cinco libros.** Vuelve a subirlos. Con ellos se pueden revisar las proporciones, el espaciado y la construcción de las curvas, que hoy resuelve la retícula de 5 × 7.
- **El nombre.** Contenedor es provisional. Otras opciones que salen del poema: *Presente continuo*, *Apenas*, *Vaso*. Conviene no llamarla Kochamama ni Qucha: el poema dice que ponerle nombre es otra manera de enterrar.
- **La retícula.** La de 5 × 7 se lee bien desde unos 13 píxeles, pero sus curvas son toscas. Una retícula más fina (por ejemplo, 7 × 9) daría una versión para texto largo, con las mismas reglas.
- **Una versión proporcional.** La monoespaciada es una decisión conceptual (la celda es el contenedor). Una compañera proporcional se deduciría de las mismas reglas.
- **Pruebas impresas.** Las trampas de tinta y la piel solo se comprueban en papel, con la impresión que vayas a usar (risografía, láser o una máquina de escribir con la tinta corrida, como la de tu poema).
- **Una traducción física.** Como ninguna contraforma se cierra, cada letra funciona como esténcil. Se puede cortar en aluminio, que es el material de las placas.
- **La licencia.** Está «por definir». Si quieres que circule, la SIL Open Font License es la opción habitual.
- **Dos detalles del poema.** En la versión que enviaste dice «ningùn», con acento grave; en el muestrario puse «ningún». «Es lo que hacemos con todo, no?» va sin signo de apertura y lo dejé así, por si es deliberado.
