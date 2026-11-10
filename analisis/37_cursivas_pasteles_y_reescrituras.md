# 37. Cursivas aymaras, pasteles hechos y reescrituras de Codex

10 de noviembre de 2026, por la tarde. El autor tomó tres decisiones sobre los pendientes:

- cursiva para las voces aymaras;
- escribir el artículo como si los pasteles ya estuvieran hechos e incorporados;
- incorporar las mejores sugerencias de estilo de la auditoría de Codex (`analisis/34`), siempre que sean coherentes con el texto.

Lo de la carpeta de Drive lo resuelve el autor.

## 1. Cursivas

Van en cursiva, fuera de las citas, las voces aymaras que nombran cosas, oficios e instituciones del mundo andino que el artículo estudia: *ayllu*, *chujlla*, *apacheta*, *huaca*, *yatiri*, *achachi*, *pututu* y *Jilakata*, también en plural. Las palabras del vocabulario de Bertonio ya iban en cursiva.

- **Dentro de un título que ya va en cursiva**, la voz pasa a redonda: «*Umbral de la* apacheta», «*Cráneo/nido: sección de la* chujlla *de los Huanca*», «*El centinela de la resistencia: los tres vigías del* ayllu *vacío*».
- **El título del artículo** lleva «el *ayllu*», y el inglés, «The *Ayllu*».
- **Dentro de las citas** no se toca nada. Tampoco en las palabras clave, que son datos para los catálogos.
- **Siguen en redonda los préstamos de uso general** en el castellano andino: puna, pirca, chácara, yunga, callapo, coca. Si el autor los quiere en cursiva, es un cambio de pocos minutos.

`AGENTS.md` recoge el criterio en la regla 4.

## 2. Los pasteles, como hechos

El texto habla ahora de los pasteles y no de sus esquemas:

- **§1.** Termina con «los seis pasteles de la serie, que reproducimos como figuras 1 a 6». Sale la frase «Se trata de una investigación en desarrollo» (S08 de Codex).
- **§2.**
  - Dice que los pasteles «están más cerca de la ilustración que del hallazgo, porque no aportan datos nuevos sobre la novela, aunque obligan a decidir lo que el texto deja abierto» (S06). Antes se leía «descubrir, no descubren nada».
  - El análisis de cada pastel «anota, además de lo que muestra, lo que hizo la mano».
  - El plano (3) es «lo que el pastel obliga a decidir».
- **Figuras 1, 2, 3 y 6.** En el plano (3), «el esquema» pasa a «el pastel». El plano (2) ya describía en presente lo que hace la mano con la materia y no cambia.
- **§8.** «Los pasteles obligan a decidir...».
- **Pies de las figuras 1 a 6.** «Pastel al óleo sobre papel, [medidas, año]. Fuente: elaboración propia.». Hay que completar las medidas y el año cuando lleguen los escaneos.
- **Declaración de IA.** El alcance dice ahora «el diseño de los esquemas de encaje con que se compusieron los pasteles de las figuras 1 a 6, el trazado de los diagramas (figuras 7 y 8)». Se mantiene la ayuda de la IA en los esquemas porque los pasteles salen de ellos. Antes, `articulo/figuras/LEEME.md` proponía quitar esa mención al cambiar las figuras; ahora dice que se quite solo si los pasteles se hicieron por otro camino.

**Hasta que lleguen los escaneos**, las figuras 1 a 6 siguen mostrando los esquemas, y sus pies dicen «[medidas, año]». El artículo no se envía antes de cambiarlas. Si los pasteles no llegan a tiempo, hay que volver a la versión del commit f784ab3. Lo dicen la lista de envío (paso 4), la guía de los pasteles, `articulo/figuras/LEEME.md` y `AGENTS.md`.

Los planos (2) y (3) describen el pastel tal como lo planearon los esquemas. Si el pastel terminado hace otra cosa, hay que escribir lo que hizo. Solo eso puede presentarse como hallazgo.

## 3. Reescrituras de Codex

### Incorporadas

| N.º | Dónde | Cambio |
|---|---|---|
| E01 | §1 | «la mecánica material del despojo, es decir, los objetos y los gestos con que se pierde la tierra», sin los dos puntos ni la serie de tres |
| E04 | §3 | «Para el narrador, «las chujllas no tienen cuartos ni mucho menos» (Botelho Gosálvez, 1982 [1945]: 30)», sin el anuncio que repetía la cita y con la referencia completa al empezar el párrafo |
| E05 | §5 | «Del otro lado, las manos del puneño pierden su oficio, y en los Yungas a Paulo le advierten: «Sabrás arar...»». Los dos puntos introducen ahora la voz y no una revelación |
| E06 | §2 | «Lo que la novela pone frente a frente son, entonces, dos manos con dos agarres, la que ara y la que firma», sin el «más que X, Y» |
| E08 | §3 | «Leídas con estos autores, las dependencias de los Huanca forman una casa comprimida donde el narrador solo ve una madriguera». Ya no atribuye a los autores lo que «vería» cualquiera de ellos |
| E11 | §4 | «de modo que, al menos aquí, el despojo tiene más que ver con la casta que con el tamaño». Un solo caso no refuta a Alexander |
| E19 | §4 y Figura 2 | Se explican «infolio» («un libro de gran formato y otro pequeño») y «alzado» («que es la vista de frente»). «calota» ya se había explicado |
| E20 | §4 | Las dos oraciones cortas se juntan en una |
| E22 | Abstract | «the dry-stone wall» |
| S04 | §6 | «La sequía, que en la novela precede al éxodo, se cuenta con...», para avisar del salto atrás |
| S06 y S08 | §1 y §2 | En el apartado 2 |
| S09 | Cuadro 1 | «Agua (145, 152-153), cascotes (144), montón (154)» |
| R15 | §1 | «(Kolář, cit. en Fuão, 2011: 43)», como las demás citas indirectas |

Ya se habían aplicado antes E13, E16, E17, E21, S02, S03, S07, R01, R13, R14 y R16 (`analisis/36`).

### Descartadas

- **E02.** Quedó resuelta con la cita completa de Fuão p. 53.
- **E03.** Los dos puntos introducen una cita, como es normal.
- **E07, E09, E10, E12, E14 y E15.** Son cierres interpretativos del autor. Las propuestas de Codex los aplanaban: «la autoridad decide cuáles de esos escritos reconoce», «el esquema permite comparar», «la novela conserva también los padecimientos...». La etimología de *domesticar* (E12) es correcta.
- **S05.** Mover la frase sobre la cola de la Figura 3 no mejora el plano (3).
- **R10, R11 y R12.** Son notas de procedencia que el artículo no necesita, porque los pies y la bibliografía ya identifican las fuentes.
- **R17.** «Reduplican» traduce bien «reduplicam».

## 4. Verificación

- Las 286 citas conservan su fuente y su página. Las únicas diferencias son de forma:
  - «las chujllas no tienen cuartos...» va ahora en minúscula y con la referencia completa;
  - la cita de Kolář lleva «cit. en».
- La cursiva no entra en ninguna cita ni en la bibliografía.
- **Extensión:** 75.409 caracteres y 12.784 palabras, 38 páginas.
