# *Chhaxwa*. Cinco pruebas de construcción a partir de *Altiplano*

En el vocabulario aymara que Ludovico Bertonio publicó en 1612, *chhaxwa* nombra dos piedras. Una es la de los montones que se hacen al limpiar la chacra, las piedras «que amontonan limpiando las chácaras». La otra es la piedra «hincada en la pared para atar en ella los palos del techo» (Bertonio, 2011 [1612]: 330). Este proyecto va de una a otra. Empieza en un terreno que se despiedra y termina bajo el techo de una casa.

Es una serie de pruebas de construcción con piedra, tierra y paja del altiplano. Cada una parte de un pasaje de la novela *Altiplano* (1945), de Raúl Botelho Gosálvez, y de una técnica andina descrita en una fuente, y busca la forma que esa técnica permite. Lo que se quiere es explorar técnicas y materiales del altiplano y, con ellos, formas poéticas en arquitectura.

El proyecto es de Joaquin Max Cuevas Ventura. Va aparte de su artículo «Cosecha de piedras: el *ayllu*, el Estado y la mina», que lee la misma novela desde el dibujo, y no lo cambia. Es especulativo, porque Jatun-Kolla, el *ayllu* de la novela, no existe; las técnicas y los materiales, en cambio, son reales.

## Estado (27 de noviembre de 2026)

**Planteado y modelado, sin construir.** Las cinco pruebas están descritas, sus quince formas y las seis exploraciones que eligió el autor están modeladas en Blender, pero todavía no se ha hecho ninguna maqueta. Los renders muestran lo que se espera. No son registros de lo que pasó ni fotos de maquetas, y no deben presentarse así.

Las medidas de cada prueba llevan su origen. Las que vienen de una fuente tienen autor y página; las que salen de una cuenta dicen cómo se hizo, y las demás son decisiones del proyecto, que se comprueban o se cambian al construir.

## Las cinco pruebas

| N.º | Prueba | Pasaje de la novela | Técnica | Escala | Archivo |
|---|---|---|---|---|---|
| 1 | La cosecha | La «cosecha de piedras» (p. 9) y el «informe montón» de la mina (p. 154) | Despedregar y amontonar | Tamaño natural | `01_la_cosecha.md` |
| 2 | El relleno | Las pircas «compuestas» al volver (p. 156) y la «piedrecilla menuda» (p. 8) | La pirca de doble cara | 1:5 | `02_el_relleno.md` |
| 3 | El dintel | Los comunarios se arrodillan «en el dintel de Jatun-Kolla» (p. 155) | El arco por aproximación de hiladas | Tamaño natural | `03_el_dintel.md` |
| 4 | La *p'ira* | Los techos de paja (pp. 10 y 41) y los techos «desfondados» (p. 79) | La *p'ira* y la armadura atada | Tamaño natural | `04_la_pira.md` |
| 5 | El fogón | Las *chujllas* «rectangulares y chatas» (p. 30) y Paulo en cuclillas junto al fuego (p. 32) | La casa de Enquelga y el *t'uju* | 1:10 | `05_el_fogon.md` |

Las páginas son de la novela, citada por su séptima edición (Botelho Gosálvez, 1982 [1945]).

Las pruebas se encadenan. La piedra menuda que separa la prueba 1 es el relleno de la 2. La *p'ira* de la 4 cubre los montones de la 1 y la maqueta de la 5. Por eso se propone empezar por la 2, que pone a prueba una frase del artículo y es la más fácil de construir, y seguir con la 4 y la 5, que comparten el techo. El orden lo decide el autor.

## Las reglas

1. **Una técnica documentada por prueba,** con su fuente y su página. Donde la fuente no alcanza, la prueba lo dice.
2. **Un pasaje de la novela que la pida,** también con su página.
3. **Trabajo de riesgo.** Alan Chandler, siguiendo a David Pye, llama así al trabajo en que «el resultado de cada operación durante el proceso es determinado por el trabajador a medida que trabaja» (Chandler, 2017: 216). Las maquetas se hacen con el material real, a tamaño natural o a escala 1:5 o 1:10. Un modelo en el computador sirve para medir y planificar, pero lo que se muestra es la maqueta.
4. **La forma sale de la técnica.** En el altiplano, el arco se hace volando las hiladas y el techo es de paja y barro, así que el proyecto no trae formas de otra parte.
5. **Nada de imágenes hechas con IA.** Se muestran las fotos de las maquetas, sin retoques, y los dibujos de su proceso.
6. **Lo ritual se documenta y no se escenifica.** Las fuentes describen la *ch'alla* de la armadura, los amuletos que se cuelgan de ella y los ritos de la jornada del putuco. Las pruebas los nombran donde corresponde, con su fuente, pero no los repiten ni los convierten en imagen. Son de quienes construyen su casa.
7. **Las manos se registran.** Cuántas personas, cuánto tiempo y quién hizo qué. En Enquelga, el techo de una casa lo levantaron seis hombres y tres mujeres (Šolc, 2011 [1975]: 106), y el putuco se levanta en una sola jornada con ayuda de vecinos y parientes (Vitulas-Quille y Reynoso-Machaca, 2025: 9-10). La manera de hacer también es parte de la forma.

Cada prueba se anota en la ficha de `ficha_de_registro.md`. Al pasar de una escala a otra, la ficha pide anotar qué se retuvo y qué se descartó, que es la pregunta de Chandler: hay que «decidir qué retenemos y qué descartamos en ese proceso de traducción» (Chandler, 2017: 214).

## La exploración formal y los modelos

Además de medir una técnica, cada prueba explora formas. `exploracion_formal.md` lee las cinco referencias que reunió el autor como operaciones formales y propone tres formas por prueba, quince en total, cada una salida de la técnica de su prueba. Las quince están modeladas en Blender como maquetas de estudio y sus imágenes están en `renders/`.

`investigacion_blender.md` reúne la investigación previa al modelado (proyectos de código abierto, materiales procedurales, la luz del altiplano y la simulación), lo que se probó y lo que se propone. El código está en `blender/`:

- `comun.py`, con los materiales procedurales, los generadores de piedra, tierra, paja y madera, el estudio de fotografía y el sol de La Paz;
- `formas.py`, con las quince maquetas y las seis exploraciones;
- `piezas.py`, con las piezas en diagrama para recomponer; `diagramas.py`, con el corte de cada exploración y las cinco a la misma escala, y `aligerar_piezas.py`, que aligera los PNG de los dos;
- `renderizar.py`, que las renderiza;
- `prototipo_pirca_paisaje.py`, la primera prueba del flujo, con una pirca en el altiplano.

Se necesita Blender como módulo de Python, instalado con `pip install bpy==5.0.1` en Python 3.11. Desde la raíz del repositorio, `venv_bpy/bin/python chhaxwa/blender/renderizar.py todas` rehace las quince imágenes.

**Las seis exploraciones.** De las quince formas, de 27 piezas en diagrama, de dieciséis referencias y de una imagen del autor salieron seis obras que juntan las técnicas de las pruebas: E1, *La montaña habitada*; E2, *El corral techado*; E3, *La casa redonda*; E4, *La chullpa*; E5, *La casa de la bóveda*, y E6, *La pirwa*, un troje alto. Están en `exploraciones.md`, con sus medidas, sus fuentes y una tabla que cruza cada obra con las cinco pruebas. Cómo se llegó a ellas está en `exploracion_formal.md` (§6 a §9).

**Los renders son predicciones, no fotos.** Cada archivo se llama `render_…`, y su pie tiene que decirlo. Cuando se construya una maqueta, su foto se pone junto al render, tomada desde el mismo punto de vista. La regla 3 todavía dice que el modelo en el computador solo mide y planifica. `investigacion_blender.md` (§1) propone reescribirla, y lo decide el autor.

## El documento

`documento/chhaxwa.pdf` reúne el proyecto en veinticuatro páginas de 23 × 24 cm: la tabla de las exploraciones y las pruebas con las seis obras a la misma escala, un par de páginas por exploración, con su texto, su corte y su render, una página por prueba con sus tres formas, el proceso, las referencias, el prototipo y las fuentes. El diseño toma rasgos del de *Obra gruesa*, a pedido del autor: una grotesca pequeña, los números de página muy grandes, los títulos de las pruebas en vertical, las fichas negras con texto blanco, una página gris de entrada y una segunda voz en gris, que en el libro de Radić es el inglés y aquí es la novela. Cada exploración ocupa dos páginas enfrentadas, el texto y el corte a la izquierda y el render a la derecha.

Se compone en Typst (`documento/chhaxwa.typ`), con la letra Inter, que es libre. Para rehacerlo: `pip install typst` y, desde la raíz, `python3 chhaxwa/documento/compilar.py`.

## Las referencias

Dos referencias dan el método, y ninguna de las dos da las formas.

- **Las maquetas de `studio_cifuentes_ethz`,** de la publicación «HS26 – Atlas Works – 50% Stone and 50% Earth» (2026), que llevaron al autor a empezar el proyecto. De ellas vienen tres ideas: una proporción de materiales como regla, la maqueta de material real como instrumento de investigación y el dibujo del proceso en axonometrías sucesivas. Sus arcos de medio punto, su bóveda de arista y sus pilares troncocónicos son de otra tradición y no se usan. Sus imágenes no están en el repositorio, porque son obra de terceros. Antes de mostrarlas junto a las maquetas de este proyecto convendría pedir permiso.
- ***Obra gruesa*, de Smiljan Radić (2017).** Sobre todo la *Ampliación para la Casa del Carbonero*, que toma la hornilla del carbonero, cubierta «con barro y paja, apisonándolos con un palo corto, hasta formar una cúpula», y la convierte en una esfera de barro de 3,20 m que, dice Radić, «no sirve para nada» (Radić, 2017: 24). Cada prueba nombra el pasaje del libro que le sirve. El libro tiene todos los derechos reservados y no está en el repositorio.

## Lo que no se usa

GPT hizo en paralelo un proyecto a partir del mismo artículo, *La tierra que queda*, que está en la rama `proyecto/la-tierra-que-queda`. El autor pidió rehacerlo desde cero, y *Chhaxwa* no usa nada de él, ni el modelo, ni las imágenes, ni los guiones. Esa rama queda como registro; su auditoría está en `analisis/41` y el replanteamiento que dio origen a este proyecto, en `analisis/42`. El registro de este proyecto es `analisis/43`.

## Las fuentes

Las fuentes de las técnicas, con las páginas que usa cada prueba, están en `fuentes.md`. Ninguna está en el repositorio, que es público: el autor las guarda en una carpeta privada. Todas las citas de esta carpeta se cotejaron en su página el 27 de noviembre de 2026. Las traducciones del inglés de Squier y de Vitulas-Quille y Reynoso-Machaca son nuestras.

## Uso de inteligencia artificial

El autor eligió el título, las referencias, el propósito del proyecto y las seis exploraciones. Claude (Anthropic), un asistente de IA generativa, redactó con sus indicaciones los textos de esta carpeta, leyó y cotejó las fuentes, hizo la investigación sobre Blender, calculó las medidas y la tabla del sol y escribió el código que modela y renderiza las maquetas y el que compone el documento. Los renders son, por eso, elaboración propia con asistencia de IA. Los calcula Blender a partir de geometría, materiales y luz escritos en código, y no hay en el proyecto ninguna imagen hecha con un generador de imágenes. Las maquetas, sus fotos y las decisiones que quedan abiertas son del autor.
