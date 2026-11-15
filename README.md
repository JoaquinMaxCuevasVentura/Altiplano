# Altiplano: «Cosecha de piedras», un artículo sobre la novela de Raúl Botelho Gosálvez

**«Cosecha de piedras: el *ayllu*, el Estado y la mina. Dibujando *Altiplano* de Raúl Botelho Gosálvez»**, de Joaquin Max Cuevas Ventura. Lee la novela *Altiplano* (1945; citada por la 7.ª ed., La Paz, Juventud, 1982) desde la arquitectura y el dibujo, siguiendo sus piedras.

El artículo nació para el dossier «Narrativas, lenguajes y representaciones: memoria y ficción a través de las Humanidades» de *Estudios Bolivianos* N.º 43 (IEB, FHCE, UMSA), cuyo plazo venció el 25 de septiembre de 2026. Desde el 2 de noviembre no responde a ninguna convocatoria ni tiene límite de extensión. La primera revista candidata es *Atenea*.

- **Si trabajas con un asistente de IA** (Codex u otro), sus instrucciones están en `AGENTS.md`.
- **Si buscas una versión anterior** o quieres ver cómo cambió el proyecto, está en `archivo_del_proyecto/`.

## Estado (14 de noviembre de 2026)

| Dato | Valor |
|---|---|
| Texto | Versión final reescrita el 2 de noviembre (`analisis/33`), corregida el 10 de noviembre tras el cotejo con las fuentes (`analisis/35` a `37`) y auditada el 14 (`analisis/38`). El autor la reescribirá con su voz |
| Extensión | 76.939 caracteres con espacios y 13.039 palabras, con notas y bibliografía; 40 páginas en Word. Para *Atenea* habría que quitar unas 4.500 palabras |
| Resúmenes | 122 palabras en español y 118 en inglés; cinco palabras clave en cada lengua |
| Citas de la novela | 145 entre comillas y 4 en bloque, cotejadas el 10 de noviembre con la edición digital de la UMSA. Falta el cotejo con el libro impreso |
| Citas de las demás fuentes | Cotejadas el 10 de noviembre con las 25 fuentes que reunió el autor |
| Bibliografía | 37 obras |
| Figuras | Ocho. El texto describe las seis primeras como pasteles hechos, pero todavía se ven sus esquemas de encaje, y los pies esperan medidas y año. **El artículo no se envía hasta cambiarlas por los escaneos.** La 7 y la 8 son diagramas |
| Imágenes | Siete de dominio público, en serie aparte: d'Orbigny, Squier (dos), Guaman Poma (tres) y la Library of Congress. Las de Guaman Poma no alcanzan para imprimir |

**Lo que falta, en orden,** está en `entregables/02_lista_de_envio.md`. En resumen: que el autor reescriba el texto con su voz, hacer y escanear los pasteles, cotejar la novela con el impreso, pedir las imágenes de Guaman Poma en alta resolución, cotejar «Father Electricity», elegir revista y adaptar el formato.

## Qué sostiene el artículo

- **Punto de partida.** La crítica ya mostró, con Cornejo Polar, que el narrador indigenista vuelve naturaleza la historia india.
- **Qué estudia.** Lo que la novela registra sin que su narrador lo advierta: los objetos y los gestos con que se pierde la tierra.
- **Qué sostiene.** La novela marca la posesión con piedras (el mojón, la pirca, el montón), cuenta cómo se pierde frente a papeles y máquinas, calla lo que los aymaras hicieron con la escritura (los títulos coloniales, los tinterillos aliados, la escuela de Warisata) y recuerda solo una parte de lo ocurrido.
- **Con qué lee.** El vocabulario aymara de Bertonio, la historia andina (Rivera Cusicanqui, Barnadas, Choque Canqui, Zavaleta, Duviols, Dean), la crítica de Cornejo Polar, Churata como contemporáneo, y autores de arquitectura y dibujo (Frampton, Pallasmaa, Cárcamo Pino, Alexander, Fuão, Monteys y Fuertes, Lundberg, Seguí, Ingold).
- **Cómo dibuja.** Seis pasteles al óleo, examinados cada uno en tres planos: lo que dice el texto, lo que hace la mano y lo que el dibujo obliga a decidir.

## Dónde está cada cosa

| Ruta | Qué es |
|---|---|
| `articulo/articulo_cosecha_de_piedras.md` | El texto fuente del artículo |
| `articulo/articulo_cosecha_de_piedras.docx` | El Word: carta, márgenes de 2,5 cm, Times New Roman 12, interlineado 1,5 |
| `articulo/articulo_cosecha_de_piedras_cambios.docx` | El Word con los cambios marcados respecto de la versión anterior al 2 de noviembre (commit 6f9bed8), para aceptarlos o rechazarlos uno por uno |
| `articulo/figuras/` | Las ocho figuras, las siete imágenes de dominio público y su `LEEME.md` |
| `articulo/generar_docx.py`, `articulo/generar_figuras.py` | Los generadores del Word y de las figuras |
| `articulo/plantilla_estudios_bolivianos.docx` | La plantilla de estilos. El generador ya no la reescribe en cada uso |
| `articulo/articulo_altiplano.md` y `.docx` | La versión 3, «Topografías de la carne y el barro en *Altiplano*», de septiembre. Es una alternativa sin figuras y no se actualiza |
| `entregables/` | Los archivos finales, con su `LEEME.md`: el artículo en Word y PDF (01), la lista de envío (02), la guía de los seis pasteles (03), el fichero de pasajes (04), las revistas candidatas (05), el atlas de Are.na (06) y las fuentes para cotejar (07) |
| `analisis/` | El registro de cada etapa, del 01 al 38, cada uno con su fecha. No se reescribe |
| `analisis/esquemas/` | Los esquemas y las notaciones de las figuras, con sus generadores |
| `taxonomia/` | La taxonomía visual del 18 de octubre: 51 imágenes de dominio público en cuatro tableros |
| `reports/` y `research_notes/` | El informe de convocatorias del 10 de octubre y sus notas |
| `archivo_del_proyecto/` | El archivo del desarrollo: las versiones anteriores de cada material, el inventario, la línea de tiempo y lo que falta |

**Ramas relacionadas, sin unir:**

- `claude/eager-bohr-mx9420`: los registros de arquitectura del altiplano, 95 láminas reunidas el 10 y el 11 de noviembre. De allí salieron las imágenes 1 y 3 del artículo.
- `codex/analisis-churata` y `codex/auditoria-version-final`: los dos informes de Codex, que ya están en `analisis/32` y `analisis/34`.

Las ramas `claude/fervent-lovelace-exgqzl` y `claude/zen-cannon-kqblsc` son de otro proyecto, la tipografía *Contenida*.

## Análisis y protocolo

| Archivo | Contenido |
|---|---|
| `analisis/01_convocatoria_estudios_bolivianos_43.md` | Convocatoria: ejes (el principal es «discurso, poder y representaciones sociales»), normas, riesgos y correo de envío |
| `analisis/02_codigo_genetico_carcamo_pino.md` | El «código genético» de Cárcamo Pino: conceptos, métodos, estilo y recetario de emulación |
| `analisis/03_marco_cruzado.md` | Lundberg, Martin, Vázquez Ramos *et al.* y la novela (primera ronda) |
| `analisis/04_verificaciones_y_pendientes.md` | Qué hacer y verificar antes de enviar |
| `analisis/05_guia_de_dibujo.md` | Guía de la exploración gráfica en tres escenas (versión 3; la reemplaza `05b`) |
| `analisis/05b_guia_seis_pasteles.md` | **Guía de los seis pasteles** del artículo definitivo: composición, paleta, técnica y registro de cada pieza. Al día el 11 de octubre, con la numeración del artículo (Castillete = 4, Pelvis = 5, Centinela = 6) |
| `analisis/06_fichero_de_pasajes.md` | Las citas de la novela ordenadas por página (para cotejar con el impreso), erratas de la transcripción, cautelas de lectura y tropos del narrador. Regenerado el 11 de octubre con las 153 citas de entonces. La versión al día es `entregables/04_fichero_de_pasajes.md` |
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
| `analisis/32_churata.md` | Informe parcial de Codex del 2 de noviembre sobre lo que Churata podía aportar. Traído el 14 de noviembre de la rama `codex/analisis-churata`, como registro |
| `analisis/33_version_final_sin_patrones_de_ia.md` | La versión final del 2 de noviembre. Qué dicen las fuentes sobre los patrones de escritura de la IA y cuánto aparecían en el texto anterior; lo que se recuperó de lo quitado por extensión, con la fuente y el registro de cada cita; lo que aportó Gamaliel Churata; la verificación de cada cita con su página. |
| `analisis/34_auditoria_de_la_version_final.md` | Auditoría de Codex del 2 de noviembre: escritura, estructura, citas y referencias de la versión final, con 64 hallazgos. Traída de la rama `codex/auditoria-version-final` como registro. Lo que se aplicó de ella está en `36` y `37` |
| `analisis/35_cotejo_con_las_fuentes.md` | Cotejo del 10 de noviembre con las 25 fuentes que el autor reunió en una carpeta privada: todas las citas existen en su fuente. Resuelve la mayor parte de las dudas de la auditoría de Codex y propone unas pocas correcciones de página y de forma, que se aplicaron ese mismo día (`36`) |
| `analisis/36_tipos_de_cita_y_correcciones.md` | Las correcciones del cotejo aplicadas el 10 de noviembre y la variación de los tipos de cita: cuánto citaba el artículo y cómo, el criterio (cita textual cuando importan las palabras, paráfrasis para lo demás, referencias narrativas y tres citas en bloque nuevas), la lista de cambios y su verificación |
| `analisis/37_cursivas_pasteles_y_reescrituras.md` | Decisiones del autor del 10 de noviembre: cursiva para las voces aymaras, el texto escrito como si los pasteles estuvieran hechos (los pies esperan medidas y año, y las figuras, los escaneos) y las reescrituras de Codex que se incorporaron y las que no, con el porqué |
| `analisis/38_auditoria_del_proyecto.md` | Auditoría del 14 de noviembre: las decisiones tomadas hasta entonces, lo que se corrigió en el artículo, en los documentos finales y en los generadores, las dos imágenes que entraron de los registros de arquitectura y lo que queda como propuesta para el autor |
| `analisis/39_archivo_del_proyecto.md` | El archivo del proyecto, del 15 de noviembre: de dónde se reconstruyó cada cosa, cómo se ordenó, qué quedó fuera y cómo se rehace y se comprueba |
| `reports/Convocatorias abiertas para el artículo.md` | Revistas y convocatorias abiertas al 10 de octubre de 2026 para enviar el artículo, con los veredictos de extensión recalculados el 11 de octubre para la versión final: diez candidatas ordenadas (primera, *Atenea*), ficha de cada una, plazos, extensión, cobros, filiación, política de IA y plan de la semana. Los sitios oficiales estaban bloqueados: todo dato sale de extractos del buscador y hay que confirmarlo en la página de cada revista (notas en `research_notes/`) |
| `analisis/esquemas/fig1…fig6` | Los esquemas de encaje anteriores de los seis pasteles, con la numeración de la serie. Se conservan, pero desde el 1 de octubre las Figuras 1 a 6 salen de las notaciones de `diagramas/` (`23`) |
| `analisis/esquemas/guias/` | Seis guías de composición sin texto, a 1536 × 1024 o 1024 × 1536, para usar con los prompts de `17`, la máscara opcional de la Figura 5 y dos guías de los diagramas (Figuras 7 y 8; la 8, vertical) para los prompts de `20` y `21`, y sus entradas con rótulos, máscaras y mapas de zonas para los de `22`. Se regeneran con `generar_guias.py` (las de los diagramas, después de `generar_diagramas.js`) |
| `analisis/esquemas/diagramas/` | Las ocho figuras del artículo trazadas como notaciones (SVG con la letra incrustada): los esquemas de encaje de las Figuras 1 a 6 y los diagramas de las 7 y 8. Su generador, `generar_diagramas.js`, y la letra Nothing You Could Do (OFL) con su licencia |
| `analisis/esquemas/escena1…escena3` | Inventarios de las tres escenas de la versión 3 |
| `analisis/referencias_visuales/` | Las cuatro imágenes de referencia de la primera ronda. **No son las figuras del artículo** |

## Regenerar el Word y las figuras

```bash
pip install pypandoc_binary python-docx pillow
python3 articulo/generar_docx.py                                # artículo definitivo (no toca lo que no cambia)
python3 articulo/generar_docx.py articulo/articulo_altiplano.md  # versión 3
node analisis/esquemas/diagramas/generar_diagramas.js           # notaciones de las figuras 1 a 8
python3 articulo/generar_figuras.py                             # necesita Chromium (variable CHROME)
python3 entregables/generar_entregables.py                      # archivos finales: copia el artículo, hace su PDF y los Word
```
