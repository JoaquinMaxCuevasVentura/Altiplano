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

## 10. Uso de IA

Claude (Anthropic) redactó los textos de `chhaxwa/` y este registro, leyó las fuentes, hizo la investigación, calculó las medidas y escribió el código de Blender y del documento. Los renders son elaboración propia con asistencia de IA. Ninguna imagen viene de un generador de imágenes. El artículo no cambia y su declaración de IA sigue siendo cierta.
