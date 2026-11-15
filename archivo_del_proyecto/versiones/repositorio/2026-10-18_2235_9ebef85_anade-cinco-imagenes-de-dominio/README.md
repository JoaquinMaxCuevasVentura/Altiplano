# Altiplano: «Cosecha de piedras», un artículo sobre la novela de Raúl Botelho Gosálvez

Artículo, análisis de fuentes y protocolo gráfico. Nació para el dossier «Narrativas, lenguajes y representaciones: memoria y ficción a través de las Humanidades» de *Estudios Bolivianos* N.º 43 (IEB, FHCE, UMSA), cuyo plazo venció el 25 de septiembre de 2026. **Ahora busca revista:** la primera candidata es *Atenea* (`reports/Convocatorias abiertas para el artículo.md`).

**Si trabajas con un asistente de IA (Codex u otro):** sus instrucciones están en `AGENTS.md`.

## Entregables (al 18 de octubre de 2026)

**Los archivos finales están en `entregables/`**, con su `LEEME.md`: el artículo en Word y en PDF, y cinco documentos en Markdown y en Word para enviarlo. Son versiones limpias, sin el historial de trabajo.

| Entregable | Archivo final | Estado |
|---|---|---|
| **El artículo** | `entregables/01_articulo_cosecha_de_piedras.docx` y `.pdf` (fuente: `articulo/articulo_cosecha_de_piedras.md`) | Versión final del 10 de octubre, con la cita de «Pyramid of Bones» cotejada el 11 con el librillo japonés de *Virtue* y, desde el 18, cinco imágenes de dominio público: 65.722 caracteres, 10.946 palabras, 33 páginas en Word; 153 citas de la novela verificadas; 34 entradas de bibliografía |
| **La lista de envío** | `entregables/02_lista_de_envio` | Lo hecho y lo que falta, en orden: epígrafe, declaración de IA, pasteles, cotejo, datos por confirmar, revista, versión anónima y envío. Sale de `analisis/04_verificaciones_y_pendientes.md` |
| **La guía de los seis pasteles** | `entregables/03_guia_de_los_seis_pasteles` | Versión final de `analisis/05b_guia_seis_pasteles.md`, con sus citas de la novela comprobadas otra vez |
| **El fichero de pasajes** | `entregables/04_fichero_de_pasajes` | Versión final de `analisis/06_fichero_de_pasajes.md`: las 153 citas y las 2 en bloque, por página, para cotejarlas con el impreso |
| **Las revistas candidatas** | `entregables/05_revistas_candidatas` | Resumen final de `reports/Convocatorias abiertas para el artículo.md`: diez revistas, recortes, barreras y qué hacer antes de enviar |
| **El atlas de Are.na** | 11 canales privados de la cuenta joaquin-cuevas; resumen en `entregables/06_atlas_de_arena`; registro en `analisis/29_atlas_arena.md` | 38 bloques; el canal de pasteles espera tus escaneos |
| **La taxonomía visual** | `taxonomia/` y su `LEEME.md`; registro en `analisis/30_taxonomia_visual.md` | 51 imágenes de dominio público (Guaman Poma, Squier, el Public Domain Image Archive y la Library of Congress) clasificadas por material y gesto, en cuatro tableros: el árbol, las fases de la novela, el mapa de fechas y el relato del argumento. Hecha el 18 de octubre. Los tableros no entran al artículo; seis de sus imágenes, sí, como imágenes 1-5 |
| **Las ocho figuras** | `articulo/figuras/` y su `LEEME.md` | Seis esquemas de encaje y dos diagramas, trazados como notaciones el 1 de octubre |
| **Las cinco imágenes de dominio público** | `articulo/figuras/imagen_1.jpg` a `imagen_5.jpg`; selección y razones en `analisis/31_proyecto_de_imagenes_de_dominio_publico.md` | Serie aparte de las figuras, añadida el 18 de octubre: tres dibujos de Guaman Poma (el escribano; la tejedora y el contador con su khipu; agosto), la Puerta del Sol de Squier y la mina Siglo XX (Library of Congress). Las de Guaman Poma no alcanzan para imprimir: hay que pedirlas a la Biblioteca Real de Dinamarca |
| **El Word con cambios marcados** | `articulo/articulo_cosecha_de_piedras_cambios.docx` | 20 cambios respecto de la versión anterior a las imágenes (commit 541ae4b): las cinco imágenes con sus frases y pies, tres *ibid.* que pasan a la cita completa, la bibliografía y la declaración de IA. Rehecho el 18 de octubre |
| **Los generadores** | `articulo/generar_docx.py`, `articulo/generar_figuras.py` y `entregables/generar_entregables.py` | Funcionan. Los Word que hacen pasan la validación de esquema |
| *La versión 3 (alternativa)* | `articulo/articulo_altiplano.md` y `.docx` | Archivada desde el 25 de septiembre; no se actualiza |

Los análisis `01` a `31` y el informe de `reports/` son el registro de cada etapa, cada uno con su fecha: no se reescriben cuando el artículo cambia. Lo vigente está en `entregables/`.

## Artículo definitivo

**«Cosecha de piedras: el ayllu, el Estado y la mina. Dibujando *Altiplano* de Raúl Botelho Gosálvez»**
*Harvest of Stones: The Ayllu, the State and the Mine. Drawing Raúl Botelho Gosálvez's* Altiplano
Joaquin Max Cuevas Ventura

Lee *Altiplano* (1945; citado por la 7.ª ed., La Paz, Juventud, 1982) desde la arquitectura y el dibujo, siguiendo sus piedras. Está escrito en lenguaje llano y abre con un epígrafe aymara: el lema del Taller de Historia Oral Andina, tomado de Silvia Rivera Cusicanqui.

- **Punto de partida.** La crítica ya mostró, con Cornejo Polar, que el narrador indigenista vuelve naturaleza la historia india.
- **Qué estudia el artículo.** Lo que la novela registra a espaldas de su narrador: la mecánica material del despojo.
- **Qué sostiene:**
  - La novela inscribe la posesión en la piedra (mojón, pirca, montón) y narra su captura por papeles y máquinas.
  - Calla el uso indio de la letra: los títulos coloniales, los tinterillos aliados y la escuela de Warisata.
  - Hace de la memoria una reparación selectiva del lugar.

- **Marco:**
  - **Fuentes andinas:** léxico aymara colonial (Bertonio), el *huanca* (Duviols), historiografía andina (Rivera Cusicanqui, Barnadas, Choque Canqui), las dos concepciones del espacio de Zavaleta, la heterogeneidad de Cornejo Polar y dos textos de *Susto al susto* (2025): el *qalachuyma*, el «corazón de piedra», en un relato de Alison Spedding, y la cura del susto como retorno «al territorio y a la memoria», de Malena y Gabriel Rodríguez. Con ellos se lee la «piedra bezoar» que vendía el yatiri de la novela, la *jayintilla* de Bertonio.
  - **Arquitectura y dibujo:** la crítica histórica del espacio (Vázquez Ramos *et al.* y Hall), la tectónica (Frampton), el manuaje y los agarres de la mano (Cárcamo Pino), la arquitectura como verbo y la casa como cuerpo (Pallasmaa, que además trae la frase de Bachelard sobre la vista y la mano), el método de Lundberg, el dibujo según Seguí e Ingold y, desde el 10 de octubre, *A Pattern Language* de Alexander: la chujlla de una habitación como casa comprimida y la propiedad como control y reparación (`analisis/25_alexander_lenguaje_de_patrones.md`). También, desde el mismo día, la collage: Fuão (*A collage como trajetória amorosa*) da una teoría del ensamblaje y de las operaciones de la mano (recorte, fragmento, encuentro, cola), y Monteys y Fuertes (*Casa collage*) piensan la casa como gente, objetos y usos, por agregación y con el hogar al centro (`analisis/26_fuao_y_monteys_collage.md`). En la revisión final entran cruces con la cultura popular, como los que hace Cárcamo Pino en su escritura, pero con los del autor: tres canciones de The Voidz, dos por su título («All Wordz Are Made Up», con el antecedente de *manuaje* en Randall McLeod, y «Pyramid of Bones») y dos pasajes de las letras que aportó el autor («Pyramid of Bones» y «Father Electricity»). La novela da además el apodo del Alcalde: «el lobo» (`analisis/27_auditoria_otra_ia_collage_titulos_y_the_voidz.md`).
  - **De la versión 2 queda** Bacon, a través de Martin.
  - **Cinco libros:** Frampton, Dean, Garrington, Scott y Le Guin.
- **Respuesta al arbitraje.** El artículo incorpora la respuesta a las cinco objeciones del arbitraje simulado (`analisis/08_respuesta_al_arbitraje.md`).
- **Recursos de Cárcamo Pino y lenguaje llano.** Adopta varios recursos de su escritura: el epígrafe (con un lema aymara en lugar del Saramago que él cita), una nota aclaratoria, los juegos de palabras, las analogías físicas (entre ellas, el esgrafiado para el método y la pirca de doble cara para la memoria) y la mirada sobre los gestos de la mano. No adopta su fórmula estructural ni sus latinismos (`analisis/09_recursos_de_carcamo_y_lenguaje_llano.md`; las analogías, en `analisis/11_analogias_fisicas.md`).
- **Ocho figuras.** Las seis primeras se examinan en tres planos: texto, operación y *contraste*. Van con el Cuadro 1 completo.
  - Las figuras son los **esquemas de encaje** de cada pastel, trazados desde el 1 de octubre como notaciones, en el mismo lenguaje de los diagramas (`analisis/23_esquemas_de_encaje_como_notaciones.md`). Se elaboraron con asistencia de IA y así lo declaran el pie y la declaración de IA.
  - Se numeran por orden de aparición: Castillete = 4, Pelvis = 5, Centinela = 6.
  - La 7 y la 8 son **diagramas** trazados como notaciones (línea fina, órbitas, materia y escritura pegada a la línea): la memoria del retorno (§7) y los tres montones, piedra, papel y máquina, sobre un eje vertical con las páginas de la novela (conclusiones). También se declaran como hechos con asistencia de IA (`analisis/19_esquemas_a_mano_y_diagramas.md`).
- **Cinco imágenes de dominio público.** Van en serie aparte («Imagen 1-5»), cada una junto al pasaje que la pide. No ilustran la novela: muestran lo que calla o aquello con lo que contrasta.
  - Lo que calla: el escribano andino de Guaman Poma (§2) y el hilo que sirve para registrar, la tejedora y el khipu (§4).
  - Con qué contrasta: la Puerta del Sol de Squier, con el anciano que el viajero volvió «parte integrante de los monumentos» (§3); la mina Siglo XX (§5); el arado de pie de agosto, hecho para el cuerpo (§7).
  - La selección y sus razones están en `analisis/31_proyecto_de_imagenes_de_dominio_publico.md`.

| Archivo | Contenido |
|---|---|
| `articulo/articulo_cosecha_de_piedras.md` | Texto fuente (Markdown) |
| `articulo/articulo_cosecha_de_piedras.docx` | Versión Word con las normas: carta, márgenes de 2,5 cm, Times New Roman 12, interlineado 1,5 |
| `articulo/articulo_cosecha_de_piedras_cambios.docx` | El artículo con los cambios del 18 de octubre (las cinco imágenes de dominio público, sus frases y pies, los *ibid.* ajustados, la bibliografía y la declaración de IA) marcados respecto de la versión anterior (commit 541ae4b), para aceptarlos o rechazarlos uno por uno en Word. Los cambios de la revisión final del 10 de octubre se marcaban respecto del commit 45624ba; esa versión del archivo sigue en el historial |
| `articulo/figuras/` | Las ocho figuras (seis esquemas de encaje y dos diagramas), las cinco imágenes de dominio público y cómo sustituir los esquemas por los escaneos de los pasteles (`LEEME.md`) |
| `articulo/generar_docx.py` | Regenera el `.docx` e informa la extensión y las palabras de los resúmenes |
| `articulo/generar_figuras.py` | Regenera las ocho figuras a partir de las notaciones SVG (o solo las que se le indiquen) |
| `articulo/plantilla_estudios_bolivianos.docx` | Plantilla de estilos que usa el generador |
| `articulo/articulo_altiplano.md` y `.docx` | Versión 3, «Topografías de la carne y el barro en *Altiplano*»: alternativa sin figuras. Su referencia a Barnadas (1977) es errónea (`analisis/04_verificaciones_y_pendientes.md`, §4.7) |

**Estado:**

- **Extensión:** 65.722 caracteres con espacios, bibliografía y notas incluidas; unas 10.900 palabras; el Word tiene 33 páginas. Ya no va a *Estudios Bolivianos* y no hay límite fijo: cada revista pone el suyo (`reports/Convocatorias abiertas para el artículo.md`; qué revistas lo admiten tal cual y cuánto pide recortar cada una, en su apartado «Cuánto hay que cortar», recalculado el 11 de octubre).
- **Resúmenes:** resumen de 99 palabras y abstract de 90.
- **Palabras clave:** cinco en cada lengua (norma 4d).
- **Autoría y declaraciones:**
  - Autoría y nota 1 completas (80 palabras; límite, 100).
  - Investigación «en desarrollo».
  - Conflicto de intereses y declaración de IA, en las declaraciones finales.
- **Citas de la novela:** las 153 entre comillas y las dos en bloque se comprobaron automáticamente contra la transcripción; existen literalmente y están en la página indicada. Las cadenas de «ibid.», revisadas. El fichero `analisis/06_fichero_de_pasajes.md` las ordena por página para el cotejo con el impreso.
- **Citas de las demás fuentes:** se cotejaron con el texto de cada una.
- **Faltan:**
  - leer el texto en voz alta y hacerlo propio;
  - confirmar el epígrafe;
  - hacer y escanear los pasteles: serán las figuras (las imágenes de GPT Image 2 son solo exploración; `analisis/17_estilo_y_prompts_gpt_image.md`);
  - revisar los dos diagramas, rótulos y páginas, y decidir si entran (`analisis/19_esquemas_a_mano_y_diagramas.md`);
  - cotejar las citas con el impreso (`analisis/06_fichero_de_pasajes.md`);
  - cotejar el pasaje de «Father Electricity» con la letra oficial de *Tyranny* (el de «Pyramid of Bones» ya se cotejó con el librillo japonés de *Virtue*);
  - elegir revista y adaptar el formato y la extensión (para *Atenea*, unas 1.800 palabras menos);
  - preparar una versión anonimizada si la revista la pide;
  - enviar.

  Véase `entregables/02_lista_de_envio.md`.

## Análisis y protocolo

| Archivo | Contenido |
|---|---|
| `analisis/01_convocatoria_estudios_bolivianos_43.md` | Convocatoria: ejes (el principal es «discurso, poder y representaciones sociales»), normas, riesgos y correo de envío |
| `analisis/02_codigo_genetico_carcamo_pino.md` | El «código genético» de Cárcamo Pino: conceptos, métodos, estilo y recetario de emulación |
| `analisis/03_marco_cruzado.md` | Lundberg, Martin, Vázquez Ramos *et al.* y la novela (primera ronda) |
| `analisis/04_verificaciones_y_pendientes.md` | Qué hacer y verificar antes de enviar |
| `analisis/05_guia_de_dibujo.md` | Guía de la exploración gráfica en tres escenas (versión 3; la reemplaza `05b`) |
| `analisis/05b_guia_seis_pasteles.md` | **Guía de los seis pasteles** del artículo definitivo: composición, paleta, técnica y registro de cada pieza. Al día el 11 de octubre, con la numeración del artículo (Castillete = 4, Pelvis = 5, Centinela = 6) |
| `analisis/06_fichero_de_pasajes.md` | Las citas de la novela ordenadas por página (para cotejar con el impreso), erratas de la transcripción, cautelas de lectura y tropos del narrador. Regenerado el 11 de octubre con las 153 citas del artículo final y las dos en bloque |
| `analisis/07_cinco_libros.md` | Análisis de Scott, Dean, Frampton, Garrington y Le Guin: pasajes con página, función y límite de cada uno, y dónde entra cada uno en el artículo definitivo |
| `analisis/08_respuesta_al_arbitraje.md` | **Respuesta al arbitraje**: las cinco objeciones, las diez fuentes de los dos bloques (Bertonio, Duviols, Barnadas, Rivera Cusicanqui, Zavaleta; Cornejo Polar, Barnadas y Coy, Ingold, Seguí), pasajes con página, qué entró en el artículo definitivo, qué se quitó y qué quedó en reserva |
| `analisis/09_recursos_de_carcamo_y_lenguaje_llano.md` | Qué recursos de Cárcamo Pino entraron, cuáles no y por qué; el epígrafe y las opciones descartadas; criterios de la versión en lenguaje llano; autores que salieron |
| `analisis/10_pallasmaa_y_dos_tesis.md` | Pallasmaa (*La imagen corpórea*), la tesis de Aljohani, *Narrative Structures* y el libro de Potteiger y Purinton, analizado y descartado: qué dicen de verdad, con página; qué entró en el artículo y qué no, y por qué |
| `analisis/11_analogias_fisicas.md` | Analogías físicas: cómo las usa Cárcamo Pino, criterios para este artículo, los cuatro borradores evaluados (pirca y ripio, válvula, bomba de pistón, cántaro y arco), las dos que entraron (esgrafiado y pirca de doble cara) y cómo hacer otras |
| `analisis/12_taller_cine_experimental.md` | El taller de Byron Davies sobre cine experimental: qué ya está en el artículo, la corrección que sugirió (el alma «cerrada» y el rostro «hierático» de la Figura 1), lo que no entra y por qué, y lecturas en reserva (tres textos de Davies) |
| `analisis/13_metaforas_populares_y_titulo.md` | Metáforas populares para simplificar el texto (piedra, papel o tijera; la casita de la Alasita; el Tío de la mina; *uta*, techo y casa), con la frase lista y su costo en caracteres, y cinco opciones de subtítulo más simples |
| `analisis/14_evaluacion_propuesta_otra_ia.md` | Evaluación de una propuesta hecha con otra IA: títulos con «manuaje» y «grafuaje» (no), «piedra, papel y máquina» (sí), cuatro metáforas verificadas (los pururaucas entran con Dean; la sopa de piedra y la casa sobre la roca, no) y el «corazón de piedra» de la novela (p. 80) |
| `analisis/15_spedding_susto_al_susto.md` | La fuente del «corazón de piedra»: Alison Spedding, «Piedras en el camino», en *Susto al susto* (2025). Cita verificada en el escaneo (p. XV), correcciones al análisis de otra IA, lo que entró (§7) y lo que queda en reserva (las piedras *awicha* de los cimientos). El libro completo muestra que es un relato (véase 16) |
| `analisis/16_susto_al_susto_libro_completo.md` | *Susto al susto* completo: la «piedra bezoar» de la novela (p. 66) es la *jayintilla* de Bertonio (p. 361), y el éxodo y el retorno se leen como un susto (§§6-7). También: el texto de Spedding es ficción, qué dice el colofón, los diez recortes, lo que queda en reserva de cada sección y lo que no se usa |
| `analisis/17_estilo_y_prompts_gpt_image.md` | Tu estilo leído en nueve pasteles, la paleta matérica (el color por el material y sus propiedades físicas, con página de la novela) y los seis prompts para explorar las obras con GPT Image 2, con qué evitar, qué mirar y qué cambia en el artículo cuando entren los escaneos. Los prompts se ajustaron tras la evaluación de `18` |
| `analisis/18_estilo_y_articulo_evaluacion.md` | ¿Tu estilo suma al artículo o es un pretexto? Lo que suma (la materia, las operaciones, la piedra con cuerpo, el vano), lo que resta (el ensueño sin tiempo, la escala incierta, el agua donde la novela no la pone), la prueba del plano (3) y la propuesta de usar tu estilo como la capa que se raspa |
| `analisis/19_esquemas_a_mano_y_diagramas.md` | Tus cinco esquemas a mano leídos de cerca, dónde hace falta un diagrama y dónde no, las Figuras 7 y 8 (qué muestran, qué deciden, cómo entraron en el artículo), la herramienta de boceto y qué cambia si las redibujas a mano (los prompts para explorarlas están en `20`) |
| `analisis/20_prompts_diagramas_estilo_referencias.md` | Prompts para llevar los diagramas al estilo de tus cinco referencias con GPT Image 2: el lenguaje de las referencias rasgo por rasgo, los materiales por lo que son (tierra siena, alquitrán, pan de oro, papel, grafito, hoja de plata), dos guías sin texto, dos variantes por figura, correcciones cortas y qué mirar |
| `analisis/21_diagramas_como_notaciones.md` | Por qué los diagramas estaban «cuadrados», las cinco referencias releídas como diagramas teóricos (la nueva, la 24, anota los fragmentos de una fuente en órbita), las Figuras 7 y 8 rehechas como notaciones (la mirada que es también el tiempo; el eje de páginas de la 9 a la 154), su relación con el manuaje, prompts para explorarlas y materiales para redibujarlas a mano |
| `analisis/22_prompts_para_mejorar_las_notaciones.md` | Prompts para meter las Figuras 7 y 8 en GPT Image 2 y mejorarlas, solo para explorar: las entradas con rótulos en los tamaños del modelo, tres maneras (toda la hoja, todo menos los rótulos, zona por zona, con máscaras), un bloque de mejora, cuatro variantes para pensar, qué mirar y la declaración de IA |
| `analisis/23_esquemas_de_encaje_como_notaciones.md` | Las Figuras 1 a 6 rehechas como notaciones, en el lenguaje de las 7 y 8: el aparato común (las cuatro funciones del Cuadro 1 como signos, el asterisco para lo que decide el dibujo, las mayúsculas para lo que hace la mano), qué afirma y qué decide cada figura, las 74 citas comprobadas, los tres datos de los esquemas anteriores que no pasaron y qué cambió en el artículo |
| `analisis/24_otro_epigrafe.md` | Otro epígrafe para el artículo final: por qué el lema del Taller de Historia Oral Andina sigue siendo el más coherente con el dossier, tres alternativas verificadas (Bertonio, los montones de la p. 220; el capataz de la mina, p. 142; Le Guin, p. 6), qué cambia en §7 y cómo cuadra la extensión |
| `analisis/25_alexander_lenguaje_de_patrones.md` | *A Pattern Language* (Alexander, Ishikawa y Silverstein, 1977) frente al artículo: dónde lo fortalece (la chujlla como casa comprimida, las tres chujllas alrededor del patio, la comida y el fuego, la propiedad como control y reparación, el umbral, las cosas de la vida), dónde hay que discutirlo (el arquetipo, el papeleo por tamaño, la estaca y el papel), cómo ir más allá (los patrones del ayllu desde Bertonio y la novela; un grado de apoyo para cada figura), qué cambió en el artículo, siete textos listos, patrones por verificar en el impreso y las citas con su original inglés |
| `analisis/26_fuao_y_monteys_collage.md` | Fuão, *A collage como trajetória amorosa* (2011), y Monteys y Fuertes, *Casa collage* (2001), frente al artículo: cómo se paginaron, lo que comparten (operaciones de la mano y casa como gente y objetos), dónde fortalecen cada sección, dónde discutirlos, cómo ir más allá (una columna de enseres en el Cuadro 1, un diagrama de la casa dispersa, una notación de «modo de empleo»), textos listos y las citas con su original |
| `analisis/27_auditoria_otra_ia_collage_titulos_y_the_voidz.md` | Auditoría de las propuestas de otra IA: qué se sostiene del análisis de *Casa collage* y Fuão (páginas corridas, citas cosidas, errores sobre la novela), por qué conviene mantener el título, qué se pudo verificar de The Voidz (álbumes y pistas sí; de trece versos que propuso la otra IA, solo dos están en las letras), qué pasajes de las letras entraron y por qué, qué dice de verdad Cárcamo Pino, lo que entró y la revisión final del artículo. Desde el 11 de octubre, el cotejo con el librillo japonés de *Virtue* (§27.12): la letra es oficial, y el pasaje de «Pyramid of Bones» cambia de corte de verso, no de palabras |
| `analisis/28_prompt_atlas_arena.md` | Prompt revisado para armar un atlas privado en Are.na: los datos reales del proyecto, las 32 obras que ya están citadas, los huecos por prioridad (crítica sobre la novela, vecinas del concurso de 1940, Warisata, facsímiles, datos de catálogo), canales por material del argumento (piedra, papel, máquina) y sin canal de «paisaje», reglas del conector, de verificación y de representación, y lo que hay que decidir antes de usarlo. No se creó nada en Are.na |
| `analisis/29_atlas_arena.md` | Registro del atlas de Are.na, hecho el 10 y el 11 de octubre: once canales privados (la matriz, nueve por material o tema y uno vacío para los escaneos de los pasteles) y 38 bloques con su ficha; los identificadores de cada canal y bloque; qué herramientas fallaron (el buscador de Are.na pide Premium, un TIFF de Commons, la ficha de la BnF) y cómo se resolvió; los canales ajenos revisados (no se conectó nada); qué huecos cubre cada hallazgo; lo que tienes que mirar o decidir; y cinco propuestas para el artículo, ninguna aplicada (la primera, mencionar el concurso de 1940 en §1) |
| `analisis/30_taxonomia_visual.md` | Registro de la taxonomía visual, hecha el 18 de octubre. Las fuentes de las 51 imágenes de dominio público (Guaman Poma en la Det Kgl. Bibliotek, Squier en Internet Archive, el Public Domain Image Archive y la Library of Congress), lo que falló (Wikimedia Commons bloqueado) y los derechos de la LoC, confirmados esa tarde y los cuatro tableros de `taxonomia/` |
| `analisis/31_proyecto_de_imagenes_de_dominio_publico.md` | Propuesta del 18 de octubre: siete imágenes de dominio público de la taxonomía como serie aparte, cada una después de un pasaje del artículo, con su pie y su frase de enlace; las Figuras 1-8 no cambian. Incluye la revisión de las 51 imágenes. Una nota fechada cuenta cómo se aplicó: entraron cinco, por qué quedaron fuera las pilastras y la apacheta, y el hallazgo de Squier sobre el anciano de la Puerta del Sol |
| `reports/Convocatorias abiertas para el artículo.md` | Revistas y convocatorias abiertas al 10 de octubre de 2026 para enviar el artículo, con los veredictos de extensión recalculados el 11 de octubre para la versión final: diez candidatas ordenadas (primera, *Atenea*), ficha de cada una, plazos, extensión, cobros, filiación, política de IA y plan de la semana. Los sitios oficiales estaban bloqueados: todo dato sale de extractos del buscador y hay que confirmarlo en la página de cada revista (notas en `research_notes/`) |
| `analisis/esquemas/fig1…fig6` | Los esquemas de encaje anteriores de los seis pasteles, con la numeración de la serie. Se conservan, pero desde el 1 de octubre las Figuras 1 a 6 salen de las notaciones de `diagramas/` (`23`) |
| `analisis/esquemas/guias/` | Seis guías de composición sin texto, a 1536 × 1024 o 1024 × 1536, para usar con los prompts de `17`, la máscara opcional de la Figura 5 y dos guías de los diagramas (Figuras 7 y 8; la 8, vertical) para los prompts de `20` y `21`, y sus entradas con rótulos, máscaras y mapas de zonas para los de `22`. Se regeneran con `generar_guias.py` (las de los diagramas, después de `generar_diagramas.js`) |
| `analisis/esquemas/diagramas/` | Las ocho figuras del artículo trazadas como notaciones (SVG con la letra incrustada): los esquemas de encaje de las Figuras 1 a 6 y los diagramas de las 7 y 8. Su generador, `generar_diagramas.js`, y la letra Nothing You Could Do (OFL) con su licencia |
| `analisis/esquemas/escena1…escena3` | Inventarios de las tres escenas de la versión 3 |
| `analisis/referencias_visuales/` | Las cuatro imágenes de referencia de la primera ronda. **No son las figuras del artículo** |

## Regenerar el Word y las figuras

```bash
pip install pypandoc_binary python-docx pillow
python3 articulo/generar_docx.py                                # artículo definitivo
python3 articulo/generar_docx.py articulo/articulo_altiplano.md  # versión 3
node analisis/esquemas/diagramas/generar_diagramas.js           # notaciones de las figuras 1 a 8
python3 articulo/generar_figuras.py                             # necesita Chromium (variable CHROME)
python3 entregables/generar_entregables.py                      # archivos finales: copia el artículo, hace su PDF y los Word
```
