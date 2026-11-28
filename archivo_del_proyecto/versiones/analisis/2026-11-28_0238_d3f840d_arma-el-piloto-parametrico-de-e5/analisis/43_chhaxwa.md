# 43. *Chhaxwa*

27 de noviembre de 2026. El autor aprobó el título propuesto en `analisis/42` (§8), ***Chhaxwa*. Cinco pruebas de construcción a partir de *Altiplano***, y pidió rehacer el proyecto paralelo a partir de ese replanteamiento, olvidando lo que hizo GPT. Durante el trabajo añadió dos pedidos:

- investigar antes de modelar en Blender, en GitHub y en lo que haga falta para lograr materiales procedurales e iluminación realistas, y modelar las pruebas de forma hiperrealista;
- explorar formas en cada una de las cinco pruebas, con cinco referencias que adjuntó;
- armar el documento del proyecto con la influencia del diseño editorial de *Obra gruesa*, en Typst o en SILE.

## 1. Lo que se hizo

Una carpeta nueva, `chhaxwa/`, en la rama del artículo:

| Archivo | Qué es |
|---|---|
| `LEEME.md` | El proyecto: qué es, su estado, las cinco pruebas, las reglas, las referencias, lo que no se usa y la declaración de IA |
| `01_la_cosecha.md` a `05_el_fogon.md` | Una prueba por archivo: el pasaje, la técnica con su fuente, la regla, los pasos, las medidas con su origen, qué se mide, los precedentes, qué se pierde al cambiar de escala y los cuidados |
| `ficha_de_registro.md` | La ficha que se llena cada vez que se hace una prueba, y cómo se fotografía |
| `fuentes.md` | Las fuentes de las técnicas con sus páginas, las referencias del método y cómo se hicieron los cálculos |
| `investigacion_blender.md` | La investigación previa al modelado, lo que se probó y lo que se propone |
| `exploracion_formal.md` | Las cinco referencias leídas como operaciones formales y las quince formas |
| `blender/` | El código: materiales, generadores y estudio (`comun.py`), las quince maquetas (`formas.py`), el render (`renderizar.py`) y el prototipo en el paisaje |
| `renders/` | Los renders de las quince maquetas de forma y del prototipo |
| `documento/` | El documento del proyecto en Typst (`chhaxwa.typ`), su PDF y el guion que lo compila |

**No se usó nada de la rama `proyecto/la-tierra-que-queda`:** ni su modelo, ni sus imágenes, ni sus guiones, ni sus dibujos de detalle. Esa rama queda como registro. La prueba 2 parte ahora de una frase del artículo y no de la idea de GPT que `analisis/42` (§5) quería conservar.

## 2. Las medidas

- **La casa de la prueba 5** sale de la tabla 1 de Šolc (2011 [1975]: 93-94). Se tomó la mediana de los 17 dormitorios de adobe con techo a dos aguas: 5,75 × 3,30 m y 2,1 m de alto. Con todas las casas de adobe a dos aguas (67) da 5,70 × 3,27 m. Los muros son de 2 m, la medida de la novela (p. 30).
- **El techo** tiene una pendiente de unos 45°. Sale de las fajas de 2,5 m, que se apoyan en el muro y se doblan 20 cm sobre el caballete (Šolc, 2011 [1975]: 105 y 107), y coincide con las fotos de la armadura (ibid.: figs. 20 y 21). El caballete queda a unos 3,6 m del piso.
- **El sol.** Se calculó su posición en La Paz para el 21 de junio, el 20 de marzo y el 21 de diciembre con las fórmulas de la NOAA (prueba 5). En junio, el sol pasa por el noreste hacia las 10 de la mañana, a 35° de altura, y en diciembre no pasa nunca por el noreste. Un agujero de 15 cm en un muro de 40 cm solo deja pasar el sol cuando este está a menos de unos 20° de su eje, así que la dirección del *t'uju* elige la fecha y la hora en que entra el sol.
- **Lo que no tiene fuente** se marcó como decisión del proyecto en cada tabla. Entre otras cosas, la medida de la puerta, la del *t'uju*, la del bloque de champa y las medidas de la pirca de la prueba 2.

## 3. Una precisión a `analisis/41`

El hallazgo F5 comparó la cumbrera del modelo de GPT, de 4,21 m, con los dos metros que da la novela. Con los datos de Šolc, una *chujlla* con muros de 2 m y techo de *p'ira* tiene el caballete a unos 3,6 m. La altura de la cumbrera, por sí sola, no contradice la novela. Lo que sí la contradice en ese modelo son los aleros a 3,09 y 4,09 m, que doblan la altura de los muros, y la cubierta de tierra en lugar de paja. F5 se sostiene por esas dos razones.

## 4. Las láminas que se dejaron

El primer plan, que venía de `analisis/42` (§6), era dibujar las pruebas en láminas A3 con axonometrías de proceso trazadas en SVG por un guion propio. Las seis láminas se hicieron, pero los dibujos tenían errores en el orden de las caras y mucho espacio vacío. Cuando el autor pidió modelar en Blender se dejaron, porque Blender puede dar las mismas axonometrías en línea a partir del modelo, con Freestyle, que se probó y funciona. Las láminas no entran al repositorio; quedan en la carpeta de trabajo de la sesión y el archivo del proyecto las registra como material descartado.

## 5. La investigación sobre Blender

Está en `chhaxwa/investigacion_blender.md`. En resumen:

- **Proyectos de código abierto:** Infinigen, para materiales procedurales escritos como código; BlenderProc, como modelo de trabajo con guiones; Bullet Constraints Builder, para derrumbes de mampostería; Meshroom, para escanear material real, y AgX, para el color. Los generadores de pircas y de techos de paja que mejor resuelven son pagados y no se usan.
- **Luz:** el cielo de dispersión múltiple de Blender 5.0, con la altitud del altiplano y el sol de la tabla de la prueba 5. Se comprobó con un render de prueba que el giro del sol en Blender es el acimut de la tabla.
- **Materiales:** colores dentro de los albedos físicos y texturas escaneadas libres de Poly Haven. Lo más fiel sería escanear el material real del lugar.
- **Lo probado:** Blender 5.0.1 como módulo de Python, Cycles en la CPU, el eliminador de ruido, AgX y Freestyle. Un prototipo de pirca en el altiplano tardó 4 minutos y 18 segundos. La simulación de un montón con cuerpos rígidos funciona pero todavía no da datos confiables: hay que calibrarla.

**Una regla en tensión.** La regla 3 del proyecto dice que el modelo en el computador solo mide y planifica. Los renders hiperrealistas la cambian y pueden pasar por fotos. Se propone tratarlos como predicciones, rotulados siempre como renders, y compararlos con las fotos de las maquetas cuando existan. Lo decide el autor.

## 6. La exploración formal

Está en `chhaxwa/exploracion_formal.md`. Las cinco referencias se leyeron como cinco operaciones: la masa sobre lo liviano, la masa ahuecada, el montón como apoyo, la proporción y las capas, el óculo y el pozo. Cada una se ató a una técnica o un dato del altiplano. De ahí salen quince formas, tres por prueba, modeladas como maquetas de estudio a 1:5, 1:10 o 1:20, con una figura de madera para la escala. Una de las referencias parece ser una pieza de granito de Smiljan Radić y Marcela Correa; *Obra gruesa* cuenta que cortaron «a mitad el granito de 19 toneladas» para *El Niño Escondido en un Pez* (Radić, 2017: 230-231). El autor puede confirmarlo. Las otras dos referencias sin autor nombrado hay que acreditarlas antes de mostrar.

## 7. El documento

Se eligió Typst antes que SILE porque se instala como paquete de Python (`pip install typst`) y no necesita compilar nada. Las dos son libres. De *Obra gruesa* se tomaron seis rasgos, mirando de nuevo las páginas del extracto: la grotesca pequeña, los números de página enormes en negrita, los títulos verticales, las fichas negras con texto blanco y puntos guía, la página gris de entrada y la segunda voz en gris. En el libro esa voz es el inglés. Aquí es la novela, para que el pasaje de cada prueba corra al lado de su técnica. La página es de 23 × 24 cm y cada prueba es un par de páginas enfrentadas. La letra es Inter, una grotesca libre; la del libro no se identificó.

## 8. Verificación

- **Citas.** Todas las citas nuevas se cotejaron en su página: la novela (pp. 8, 9, 10, 30, 31, 32, 41, 72, 79, 154, 155 y 156), Šolc (pp. 93-94, 102, 105-111), Squier (pp. 255, 313 y 391-393), Yampara Blanco (p. 13), Suárez Jordán (p. 130), Vitulas-Quille y Reynoso-Machaca (pp. 5, 9-11), Bertonio (pp. 77, 132, 246, 276 y 330) y *Obra gruesa* (pp. 24, 78, 190, 204, 214, 216, 226 y 230-231). Las traducciones de Squier y de Vitulas-Quille y Reynoso-Machaca son nuestras.
- **Fuentes de la web.** La investigación sobre Blender se hizo con búsquedas del 27 de noviembre. Los datos de los proyectos y de los artículos vienen de sus páginas de presentación y de los resúmenes de las búsquedas, no de una lectura completa. El catálogo de Poly Haven se consultó directamente en su API.
- **Lo que no se usó.** Ningún archivo de la rama de GPT, ninguna imagen de las referencias y ninguna imagen hecha con IA.

## 9. Lo que decide el autor

- Si se reescribe la regla 3 para admitir renders como predicciones.
- Cuáles de las quince formas se desarrollan, y en qué orden se hacen las pruebas. Se propone empezar por la 2.
- La autoría de las referencias R1 y R5, y si R4 es *El Niño Escondido en un Pez*.
- Si se pide permiso a `studio_cifuentes_ethz`.
- Si los dos metros de la novela son los muros, como se leyó aquí, o la altura total de la *chujlla* (prueba 5).

## 10. Más tarde, el mismo día: la elección del autor y las piezas

El autor miró las quince formas y eligió dos, recomponiéndolas:

- **E1. La montaña habitada** (prueba 1): el cono de piedra de 1B, más chato, con la entrada forrada de queñua de 1C.
- **E2. El corral techado** (prueba 2): el cerramiento de 2C con el techo de ichu de 5C o, como sugirió, el de 4C. Se modelaron las dos versiones y el autor elige.

Para las pruebas 3, 4 y 5 pidió más opciones en diagrama, para recomponerlas él. Se hicieron 27 piezas en diagrama (modelos de masas blancos, con contornos y una figura de 1,65 m), en `chhaxwa/renders/piezas/`, con `chhaxwa/blender/piezas.py`: ocho para el dintel, diez para la *p'ira* y nueve para el fogón. A ellas se suma la serie del tiempo, que muestra E2 en cuatro estados, del techo nuevo a la pirca caída. Mandó en tres tandas quince referencias más y sus fotos de los adobitos de la Huaca Pucllana. Las piezas que salen de ellas y la descripción de cada referencia están en `chhaxwa/exploracion_formal.md` (§6 y §7).

Dos cautelas:

- **Los adobitos de la Huaca Pucllana** son una técnica de la costa, de la cultura Lima, y no del altiplano. Para que entren con la regla 1 hace falta una fuente publicada, con su página. Las fotos son del autor y no se suben al repositorio sin que él lo pida.
- **Las quince formas de la exploración** quedan como registro, renderizadas a media resolución. Solo E1 y E2 están a resolución completa.

El documento en Typst suma las formas elegidas, la serie del tiempo y tres páginas de piezas, y pasa a 22 páginas.

## 11. Uso de IA

Claude (Anthropic) redactó los textos de `chhaxwa/` y este registro, leyó las fuentes, hizo la investigación, calculó las medidas y escribió el código de Blender y del documento. Los renders son elaboración propia con asistencia de IA. Ninguna imagen viene de un generador de imágenes. El artículo no cambia y su declaración de IA sigue siendo cierta.

## 12. Más tarde, el mismo día: las cinco exploraciones

El autor cerró la exploración con cinco obras y pidió rehacer el documento alrededor de ellas. En el camino tomó estas decisiones:

- **E1 y E2** quedan como estaban. E2 lleva el techo de cono.
- **La tercera** iba a ser una A de piedra amontonada con tierra apisonada entre los dos muros, sobre una base de pirca, a partir de la referencia R6. Se modeló y el autor la descartó. La reemplaza *La torre de champa*, su interpretación de R8 con los materiales del proyecto: hiladas de champa, una V volada entre dos apoyos que son una pirca y un montón, lajas pasantes y un techo de un agua de fajas de *p'ira* atado a piedras hincadas en el muro, la segunda *chhaxwa* de Bertonio.
- **La chullpa (E4)** lleva la base de piedra, y no de madera, y una pirámide de adobitos de pie, como se le propuso.
- **La casa (E5)** lleva una bóveda de adobe por aproximación de hiladas. Primero se modeló con cúpula, y el autor aclaró que en su referencia (R16) es una bóveda.

**Las fuentes nuevas.** Se buscaron y se cotejaron en su página:

- en Squier (1877), las chullpas de Palca (pp. 243-244), de Acora (pp. 352-354) y la cornisa de las casas de champa del Ramis (pp. 391-392). Dan la cámara cubierta por hiladas voladas, la plataforma de piedra, la boca al este de dieciocho pulgadas, la cornisa de ichu prensado y la altura de 16 pies que tiene E4;
- para el aparejo de librero de la Huaca Pucllana, la ponencia de Agüero Benites y otros (2015: 3 y 6), que es la fuente que faltaba para los adobitos (§10). Allí también se recuerda que en la sierra se construía casi solo con piedra, y E4 lo dice.

En Squier (1877: 352) aparece además Hatuncolla, el señorío del lago Umayo al que pertenecían las chullpas de Sillustani. Es el mismo nombre que el *ayllu* de la novela, Jatun-Kolla. No se usa en el proyecto. Queda anotado por si el autor lo quiere.

**Lo que se hizo:**

| Archivo | Qué es |
|---|---|
| `chhaxwa/exploraciones.md` | Las cinco exploraciones, con sus medidas y su origen, la tabla que las cruza con las pruebas y lo que decide el autor |
| `chhaxwa/blender/formas.py` | E3, E4 y E5 (y `comun.py`, con los adobes como instancias y la hilada que se corta en los vanos) |
| `chhaxwa/blender/diagramas.py` | Un corte de cada exploración y las cinco a la misma escala, en masas con contornos |
| `chhaxwa/renders/render_forma_E3.jpg` a `E5.jpg` y `renders/diagramas/` | Los renders a resolución completa y los seis diagramas |
| `chhaxwa/documento/` | El documento rehecho, en 22 páginas |

**Las medidas.** Las que no tienen fuente están marcadas como proyecto en `exploraciones.md`. Dos tienen consecuencias que el autor debe ver:

- la torre de champa tiene de 4,2 a 5,4 m, y hay que probar primero si se sostiene;
- la casa de la bóveda llega a 2,6 m, más que los dos metros de la novela, porque una bóveda volada sobre 3,30 m necesita casi dos metros de alto.

**Una imagen de exploración.** El autor preguntó qué opinaba de una imagen de una cúpula de anillos de tierra sobre una base de piedra redonda, con ichu arriba. Se le respondió que tiene fuentes (el putuco y la cámara de la chullpa de Palca), pero que repite la figura de E1, que el ichu tapa la salida del humo y que la piedra es de río y no de cosecha. Se le propuso usarla para repensar E1 o dejarla fuera. Si la imagen viene de un generador, no entra al documento (regla 5). Lo decide el autor.

**Verificación.** Las citas nuevas de la novela (pp. 30, 32, 154, 155 y 156), de Squier y de Agüero Benites y otros se cotejaron en su texto. El documento se compiló sin errores y se revisó página por página. Los diagramas se pasaron a 64 colores.

**Pendiente.** El autor sugirió QCAD para los dibujos de detalle. QCAD no está en los paquetes de este entorno. Su formato es DXF, que puede escribir la biblioteca libre `ezdxf` desde Python, así que se propone dibujar los detalles en DXF, editables en QCAD.

**Uso de IA.** Claude (Anthropic) buscó y cotejó las fuentes nuevas, redactó `exploraciones.md` y los textos del documento, y escribió el código de los modelos, de los diagramas y del documento. Las formas y las decisiones son del autor. Ninguna imagen del proyecto viene de un generador de imágenes.

## 13. Más tarde, el mismo día: una candidata, la casa redonda

El autor volvió a preguntar qué opinaba de la imagen de la cúpula de tierra sobre una base de piedra (§12). Se le respondió con cuatro correcciones, y pidió hacerlas y analizar a cuál de las cinco exploraciones podría reemplazar.

**Lo que se hizo.** La forma E6 en `chhaxwa/blender/formas.py`, su render (`renders/render_forma_E6.jpg`) y su corte (`renders/diagramas/diagrama_x6.png`), y la sección «Una candidata: la casa redonda» en `chhaxwa/exploraciones.md`. Las correcciones:

- la piedra de la cosecha en lugar de la de río;
- un dintel de laja sobre la puerta;
- el óculo abierto bajo un sombrero de ichu;
- la tierra revocada en anillos que escurren el agua;
- el *t'uju* al noreste.

Al modelarla apareció una sexta: una cúpula por aproximación de hiladas se cierra en cono, así que la forma baja de la imagen solo puede ser un relleno de tierra sobre una cámara volada.

**Una fuente que cambia el análisis.** Yampara Blanco describe el *muruqu uta*, la casa redonda de todos los días, con la puerta al este, el fogón y el *t'uju* al noreste (2019: 13), y la pareja que forma con la casa cuadrada o rectangular, el *taru uta* (ibid.: 9). La candidata es esa casa redonda. El putuco, en cambio, suele ser cuadrado (Vitulas-Quille y Reynoso-Machaca, 2025: 5). Las citas se cotejaron en su página.

**El análisis.** Se propone que reemplace a E2, el corral techado. Las razones:

- comparte con E2 la pirca redonda de doble cara;
- con E5 forma la pareja de casas que describe Yampara Blanco;
- E1, que lleva el título, queda intacta.

Reemplazar a E1 o a E5 también es posible, con lo que pierde cada caso (`exploraciones.md`). El documento no se cambió: se rehace cuando el autor elija.

**Uso de IA.** Claude (Anthropic) modeló la candidata, buscó y cotejó la fuente de la casa redonda y redactó el análisis. La imagen del autor no se subió al repositorio.

## 14. Más tarde, el mismo día: la casa redonda como E3 y la *pirwa* como E6

El autor decidió que la casa redonda reemplazara a la torre de champa (E3), y no a E2 como se le proponía. Se le advirtió que la torre traía tres cosas que ninguna otra obra tenía, y pidió pasárselas a la casa:

- **el umbral:** se entra por un paso de piedra con jambas de 60 cm y tres hiladas que vuelan 10 cm hasta cerrarse a 96 cm, la regla de la prueba 3, y el pasaje del «dintel de Jatun-Kolla» (p. 155) pasa a esta casa;
- **la *p'ira*:** la tierra se cubre con seis cursos de fajas de 0,7 m traslapadas como tejuelas, que además resuelven el agua de la lluvia;
- **la *chhaxwa*:** los palos del sombrero de ichu se atan a tres piedras hincadas en el collar del óculo, y unas lajas hincadas sirven de escalones.

Después preguntó si convenía mejorar la torre para que ocupara otro lugar y, si aportaba, incluirla como sexta exploración. Se juzgó que sí, si tenía un uso. Yampara Blanco describe las *pirwas* de la vivienda aymara como «silos aéreos de granos, quinua y papas deshidratadas», con una boca arriba para cargar y otra abajo para sacar (2019: 14), y la novela termina con un «pronóstico de abundancia, de trojes altos y almiares llenos» (p. 157). La torre volvió como E6, *La pirwa*:

- se bajó a 3,6 y 4,6 m;
- las lajas pasantes se ordenaron en una escalera hasta una boca de carga;
- en la clave de la V se puso una trampa para sacar lo guardado. Que esa boca esté abajo y no a un costado es decisión del proyecto.

Las citas de Yampara Blanco (pp. 9, 13 y 14) y de la novela (pp. 16, 155 y 157) se cotejaron en su texto.

**La serie queda de seis.** Va de una cosecha a otra: el montón de piedras (E1), la pirca (E2), la casa redonda (E3), la tumba (E4), la casa rectangular (E5) y el troje (E6). E3 y E5 forman la pareja de casas de Yampara Blanco, y E6 es una de sus *pirwas*. E3 es la única obra que usa las cinco pruebas.

**Lo que cambió en los archivos:**

- `formas.py`: E3 es la casa redonda y E6 la *pirwa*, y la candidata E6 desaparece;
- `diagramas.py`: tiene los cortes de las seis y la serie de seis a la misma escala;
- `exploraciones.md` se rehízo para las seis;
- el documento pasa a veinticuatro páginas, con la tabla de seis filas y un par de páginas para E6;
- los renders y los cortes de E3 y E6 se reemplazaron, y los de la torre y de la candidata quedan en la historia de la rama.

**Uso de IA.** Claude (Anthropic) modeló los cambios, buscó y cotejó las fuentes de la *pirwa* y redactó los textos. Las decisiones son del autor.

## 15. Más tarde, el mismo día: los pasajes desde el artículo, la *p'ira* de E2 y E5 a dos metros

El autor pidió tres cambios.

**Los pasajes, desde el artículo.** Se leyó el artículo «Cosecha de piedras» para elegir el pasaje de cada exploración entre los que el artículo ya lee en términos de construcción:

| | Pasajes de la novela | Lo que el artículo lee en ellos |
|---|---|---|
| E1 | La «montaña de piedras» (p. 9) | El montón como arquitectura mínima |
| E2 | Las pircas «derruidas» y los techos «desfondados» (p. 79); las pircas «compuestas» (p. 156) | Reparar el techo y el lindero |
| E3 | El «portal de su chujlla» (p. 34); el «dintel de Jatun-Kolla» (p. 155) | El umbral de la casa y del *ayllu* |
| E4 | Las piedras amontonadas sobre el cadáver (p. 35); el «informe montón» de la mina (p. 154) | Habitar y enterrar casi no se distinguen |
| E5 | Las *chujllas* «rectangulares y chatas» (p. 30); las herramientas colgadas (p. 31) | La casa como caja de herramientas, cerca del *taru uta* |
| E6 | Los «trojes altos» y la «atalaya de la esperanza» (p. 157) | La casa como recipiente que guarda la cosecha, y la memoria del retorno |

Leídas de a pares repiten la tesis del artículo:

- E1 y E4 son el montón en que se habita y el montón en que se entierra;
- E3 y E5 son las dos casas;
- E2 y E6 son el lindero y el troje.

Los pasajes se cotejaron en el texto de la novela. Las lecturas son del artículo, y asignarlas a las obras es una propuesta.

**La *p'ira* bajo el ichu de E2.** Al modelarla apareció un error del modelo anterior. Los ocho palos estaban dentro del corral y terminaban a 2,3 m, mientras el cono, a ese radio, estaba a 3,8 m, así que el techo quedaba en el aire. Para poner pares y *p'ira* los palos pasaron a la pirca, donde miden 1,7 m. En la entrada hay dos palos que bajan hasta el suelo. Sobre los palos van un anillo atado, dieciséis pares, las fajas de *p'ira* y el ichu. La franja de cielo de 90 cm se mantiene.

**E5 a dos metros.** El bloque baja de 2,6 a 2 m, los de la novela (p. 30). Para que la bóveda quepa, arranca a 35 cm, la altura de los camastros, y cada hilada vuela de 11 a 13 cm desde el principio, de modo que la clave queda a 1,9 m. La sección se vuelve apuntada, como la cámara de la chullpa de Acora (Squier, 1877: 353). Un vuelo de 13 cm es un tercio del largo del adobe, y hay que probar que se sostiene.

**Uso de IA.** Claude (Anthropic) leyó el artículo, propuso los pasajes, cotejó las citas y cambió los modelos, los cortes, los textos y el documento.

## 16. 28 de noviembre: las láminas de detalle, sin figuras y con grosores

El autor propuso QCAD (Community Edition, GPLv3) para los dibujos de detalle, porque trabaja sobre DXF. QCAD no se puede instalar en este entorno, así que las láminas se dibujan con código, con la biblioteca ezdxf, y se guardan en DXF, que QCAD abre y edita. El guion es `chhaxwa/detalles/dibujar_detalles.py`. Cada lámina es un A3 apaisado a una sola escala, dibujado en metros reales; E1 va a 1:25 y las demás a 1:20.

| Lámina | Qué muestra |
|---|---|
| 1. E1 | Corte por la boca: la cámara volada, el dintel de lajas y la caja de queñua |
| 2. E2 | Corte por la pirca y el alero: las caras, el relleno, el palo, el anillo, el par, la *p'ira* y el ichu |
| 3. E3 | Corte de oeste a este por el paso: la pirca, la cúpula de champa, el relleno, las fajas traslapadas y el sombrero |
| 4. E4 | Corte por la boca: las pilas, la cama de lajas, la cámara de adobitos y su dintel; el aparejo de librero y la cornisa |
| 5. E5 | Corte de través por el fogón: el bloque, la bóveda volada, el relleno y la clave abierta |
| 6. E6 | Corte a lo largo: los apoyos, la V, el piso, la trampa y lo guardado; la *chhaxwa* en un corte de través |

**Dos pedidos a mitad del trabajo.** El autor pidió quitar las figuras humanas, que se veían mal, de las láminas y de los modelos, y cuidar los grosores de línea, porque las primeras vistas tenían un solo grosor.

- **Las figuras.** `blender/comun.py` tiene ahora `FIGURAS = False`, que apaga la figura de madera en todos los modelos. Se rehicieron sin figuras los quince renders de forma, los siete de las exploraciones, las 31 piezas y los siete diagramas. Se corrigieron los pies y los textos que nombraban la figura de 1,65 m. Las láminas no llevan figuras.
- **Los grosores.** Las capas siguen la jerarquía del dibujo de arquitectura. Lo cortado lleva un contorno de 0,50 mm, y sus juntas, de 0,18 mm. El suelo va a 0,70 mm, lo que se ve más allá del corte va en gris a 0,18 mm y lo oculto, en trazos. Los sombreados van en gris a 0,09 mm, uno por material, y las cotas y las guías, en gris oscuro a 0,13 mm. El contorno grueso sale de unir las piezas cortadas con shapely, de modo que las juntas interiores quedan finas. Los patrones son de la lista de AutoCAD, que QCAD también trae. Las primeras vistas salían con un solo grosor por otra causa. El motor de matplotlib de ezdxf toma los milímetros como si fueran puntos, y hubo que multiplicarlos por 2,835. El DXF no cambia por eso.

**Lo que las láminas resolvieron.** Dibujar a escala obligó a decidir cosas que los modelos dejaban abiertas. Quedan marcadas como decisiones del proyecto en las láminas y en `chhaxwa/exploraciones.md`:

- E1 lleva un dintel de lajas sobre el paso, entre la cámara y la caja de queñua.
- En E2, el anillo va sobre los palos y recibe los pares, justo bajo la *p'ira*.
- En E4, la cámara se forra de adobitos, y el dintel de la boca va de la cámara a la cara.
- En E5, el camastro es un banco de adobe de 0,70 × 0,35 m contra el muro sur.
- E6 lleva un piso de palos de queñua de muro a muro sobre la V, con la trampa bajo un hueco.

**Tres correcciones.** Las láminas mostraron tres medidas mal escritas.

- Los palos de E2 miden 1,4 m, y no 1,7 como dice el §15. Se ajustaron el modelo y el diagrama para que el anillo cargue los pares.
- La última hilada de la bóveda de E5 deja una rendija de 43 cm, y no de 30. Las lajas la cierran a 1,86 m.
- El paso de E3 mide 96 cm hasta lo alto de la hilada que lo cierra, como pide la regla de la prueba 3. Al centro, en cambio, quedan 84 cm libres, porque las dos mitades de esa hilada se tocan por abajo.

Se corrigieron `exploraciones.md` y el documento.

**El documento.** Las seis láminas entran en el documento en una serie aparte, L1 a L6, para no mover la numeración de las figuras. Tiene ahora treinta páginas. Las láminas también están juntas en `chhaxwa/detalles/laminas_de_detalle.pdf`, en A3, para imprimirlas.

**Las exploraciones paramétricas.** El autor preguntó por herramientas para explorar las seis obras de forma paramétrica y generativa mientras se dibujan los detalles. La propuesta, que el autor tiene que aprobar antes de hacerla:

- **Aquí:** Python con bpy, que ya modela las maquetas y puede armar Geometry Nodes desde código, y build123d, que se instala con pip y exporta a STEP y DXF. ezdxf sigue para las láminas.
- **En el escritorio del autor:** Sverchok y Tissue en Blender, y FreeCAD, que se usan con su interfaz gráfica.
- **Las variantes:** cada exploración se vuelve una función cuyos parámetros son las reglas de construcción, como el vuelo por hilada, el arranque, la piedra de una cosecha o el largo de las fajas. Cada variante se dibuja con una marca que dice si cumple esas reglas.
- **El piloto:** E5, porque tiene un límite de la novela, los dos metros, y una regla que probar, el vuelo de 13 cm.

**Uso de IA.** Claude (Anthropic) escribió el guion de las láminas y su dibujo, el interruptor de las figuras, las correcciones y este registro, y rehízo las imágenes y el documento.

## 17. Más tarde, el mismo día: el piloto paramétrico en E5 y la bóveda verdadera

El autor aprobó el piloto de exploración paramétrica en E5. Está en `chhaxwa/parametrico/`, con su `LEEME.md`.

**Hiladas voladas.** `boveda_e5.py` vuelve la bóveda una función de sus reglas. Cambian el arranque, el vuelo de la primera hilada y el de la última, en 825 variantes, y lo demás queda como en `exploraciones.md`. Cada variante tiene que cumplir tres reglas:

- **A.** La clave, con sus lajas, no pasa de 2 m (p. 30).
- **C.** El relleno carga las colas y deja 30 cm de parapeto.
- **K.** La rendija la cierra una laja.

Como lo que vuela el adobe lo mide la prueba 3, se probaron tres escenarios. Si vuela 12 cm, cumplen 18 variantes; si vuela un tercio de su largo, 42, y si vuela 15 cm, 120. Por debajo de unos 11 cm ninguna cabe en dos metros. En cada escenario se eligió la de más ancho para estar sentado:

- con un tercio, es la E5 que ya estaba, en el borde de la regla C;
- con 15 cm, la bóveda arranca a 60 cm y gasta 112 adobes y 1,8 m³ de relleno menos.

En ninguna variante con hiladas voladas se está de pie en más de 44 cm de ancho.

**La bóveda verdadera.** A mitad del trabajo el autor preguntó si E5 podía tener una bóveda convencional, y después mandó la foto de un arco de adobe de dovelas, cada adobe con la junta hacia el centro. La foto no se sube al repositorio. `boveda_e5_verdadera.py` prueba 258 bóvedas de medio punto, catenarias y rebajadas, con anillos de 10, 20 o 40 cm según cómo se ponga el adobe. Como una bóveda verdadera empuja, la regla del vuelo se cambia por dos de equilibrio:

- **E.** Tiene que caber una línea de presiones dentro del anillo, buscada entre todos los empujes y alturas de la clave.
- **S.** La resultante de media casa tiene que caer dentro de la base del muro.

Cumplen 145. Con dovelas de canto, de 20 cm, como las de la foto, las elegidas dejan de 0,93 a 1,20 m de ancho para estar de pie, contra 0,43 m de E5, y gastan de 558 a 718 adobes, contra 728. La cuenta es plana, con pesos supuestos sin medir, y no mide la resistencia del adobe ni el deslizamiento de las juntas. Que la catenaria pueda levantarse sin cimbra, como las bóvedas nubias, no está cotejado en las fuentes del proyecto; el medio punto y la rebajada piden cimbra.

**Los nodos.** `boveda_e5_nodos.py` arma la bóveda en Geometry Nodes, con los parámetros como controles y un interruptor entre hiladas voladas y bóveda verdadera de dovelas trabadas. Guarda `e5_parametrica.blend` y un render de cuatro variantes. Al compararlos apareció una diferencia de redondeo. Para E5 la cuenta de hiladas da justo 12,5: Python redondeaba al par (12) y Blender hacia arriba (13). Ahora los dos toman el entero de abajo en el empate, que es lo que ya daba E5. El guion comprueba que los nodos dan las mismas hiladas y la misma clave que el cálculo.

**El documento.** Suma cinco figuras en una serie aparte, P1 a P5: el campo, la matriz, las elegidas, la comparación con la bóveda verdadera y el render de los nodos. Tiene ahora treinta y cuatro páginas.

**Lo que decide el autor.**

- Si E5 sigue con hiladas voladas o pasa a una bóveda verdadera. Eso cambiaría la técnica que la ata a la prueba 3 y a la chullpa de Acora, y pediría una prueba del arco y, salvo en la catenaria, cimbra. Mientras tanto, el modelo y la lámina de E5 no cambian.
- Si el piloto sigue con las otras cinco exploraciones.

**Uso de IA.** Claude (Anthropic) propuso el piloto, escribió los guiones, los nodos y las láminas, hizo las cuentas y redactó estos textos.
