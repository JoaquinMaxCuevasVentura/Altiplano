# Lista de envío

**«Cosecha de piedras: el ayllu, el Estado y la mina. Dibujando *Altiplano* de Raúl Botelho Gosálvez»**, de Joaquin Max Cuevas Ventura.

Estado al 11 de octubre de 2026. Aquí está lo que ya se hizo y lo que te toca hacer antes de enviar el artículo, en orden.

## El artículo hoy

| Dato | Valor |
|---|---|
| Extensión | 61.705 caracteres con espacios y 10.286 palabras, con notas y bibliografía. En Word, 29 páginas (tamaño carta, Times New Roman 12, interlineado 1,5) |
| Resúmenes | 99 palabras en español y 90 en inglés |
| Palabras clave | Botelho Gosálvez; ayllu; despojo; manuaje; dibujo como investigación. En inglés: Botelho Gosálvez; ayllu; dispossession; manuage; drawing as research |
| Títulos | 16 palabras en español y 15 en inglés. Si la revista pide 12 como máximo: «Cosecha de piedras: el ayllu, el Estado y la mina en *Altiplano*» |
| Figuras | Ocho. Las figuras 1 a 6 son los esquemas de encaje de los seis pasteles; la 7 y la 8, diagramas. Va además el Cuadro 1 |
| Citas de la novela | 153 entre comillas y 2 en bloque. Todas se comprobaron contra la transcripción: existen tal cual y están en la página indicada |
| Bibliografía | 32 obras |
| Destino | Sin elegir. La primera candidata es *Atenea* (véase `05_revistas_candidatas`) |

## Lo que ya está hecho

- [x] Texto final revisado, sin marcas pendientes ni erratas a la vista.
- [x] Línea de autoría y nota 1, de 80 palabras.
- [x] Resumen, abstract, palabras clave y títulos en las dos lenguas.
- [x] Declaración de conflicto de intereses y declaración de uso de IA.
- [x] Citas de la novela comprobadas contra la transcripción, una por una. Cadenas de *ibid.* revisadas.
- [x] Citas de las demás fuentes cotejadas con el texto de cada una, con su página.
- [x] El pasaje de «Pyramid of Bones» sigue la letra oficial, la del librillo de la edición japonesa de *Virtue*.
- [x] Word regenerado con la versión final.

## Lo que te toca, en orden

### 1. Leer el artículo en voz alta y hacerlo tuyo

Cambia lo que no suene a ti. Antes de firmar, decide si sostienes cada interpretación. Las que más conviene mirar:

- la escuela de Warisata, que la novela calla (sección 2);
- los tinterillos, que en la historia también asesoraron a las comunidades (sección 4);
- los vigías leídos como mojones, con el *achachi* y la *saywa* de Bertonio (Figura 6);
- la apacheta sin montón (Figura 3);
- los dos agarres de la mano y la huella dactilar «como un sello» (secciones 2 y 5);
- las dos analogías: el esgrafiado (sección 1) y la pirca de doble cara (sección 7);
- el cierre de la Figura 1: el narrador declara cerrada el alma de los comunarios y los ve como estatuas;
- el *qalachuyma*, que el artículo presenta como parte de un relato de Spedding (sección 7);
- los cruces con la cultura popular: el apodo «el lobo» del Alcalde y las tres canciones de The Voidz (secciones 2, 3, 4 y 7).

Si cambias algo, regenera el Word con `python3 articulo/generar_docx.py` y después los entregables con `python3 entregables/generar_entregables.py`.

### 2. Confirmar el epígrafe

Hoy el artículo abre con el lema del Taller de Historia Oral Andina: «Mirando al pasado para caminar por el presente y el futuro (*qhip nayr uñtasis sarnaqapxañani*)» (Rivera Cusicanqui, 2010 [1984]: 17). Habla de la memoria, da la primera palabra a una voz aymara colectiva y prepara la crítica de la sección 7.

Si prefieres que el epígrafe nombre la piedra o la cosecha, hay tres alternativas ya comprobadas en su fuente:

| Opción | Texto | Qué hace | Cuidado |
|---|---|---|---|
| A. Bertonio | «Montón de papa cubierto de ichu. *Qäna* vel *phina*. Montón de piedras como las que suele haber por las chácaras. *Qala chaxwa*, *pünqu*, *qutu*» (Bertonio, 2011 [1612]: 220) | Junta el montón de la cosecha y el de las piedras: la «cosecha de piedras» dicha en aymara | Habla un vocabulario jesuita, no un aymara. Esta entrada escribe *chaxwa*; la de la sección 1, *chhaxwa*: se respeta cada una |
| B. El capataz de la mina | «Aquí cosecharás miles de cargas de estaño... Las papas de estaño las siembra el diablo ¿sabes?» (Botelho Gosálvez, 1982 [1945]: 142) | La cosecha del título vuelta mina | Da la primera palabra a quien se burla de Condori. La primera frase ya está en la sección 5 |
| C. Le Guin | «[…] antes de la herramienta que expulsa energía hacia fuera, creamos la herramienta que lleva energía a casa» (Le Guin, 2021 [1986]: 6) | Anuncia la oposición entre el arma y el recipiente de las conclusiones | Es una voz ajena a los Andes, ya citada dos veces, y no nombra la piedra |

Si cambias el epígrafe, cambia también una frase de la sección 7. Donde dice «Es lo contrario del lema del epígrafe: los comunarios de la novela no caminan mirando al pasado; lo esconden en un foso», puede decir: «Al revés del lema del Taller de Historia Oral Andina (Rivera Cusicanqui, 2010 [1984]: 17), los comunarios no caminan mirando al pasado: lo esconden en un foso».

### 3. Revisar la declaración de uso de IA

Así figura hoy en el artículo:

> a\) *Herramientas*: Claude (Anthropic) y ChatGPT (OpenAI), asistentes de IA generativa. b) *Alcance*: se emplearon en la exploración bibliográfica, la transcripción y paginación de fuentes digitalizadas, la localización y el cotejo de citas con su página, el contraste de pasajes de la novela, la revisión conceptual y la redacción de borradores, y el diseño y trazado de los esquemas de encaje (figuras 1-6) y de los diagramas (figuras 7 y 8). c) *Rol*: el autor concibió la hipótesis original, diseñó la metodología de lectura tectónica, seleccionó las fuentes, decidió las interpretaciones, dirigió y revisó la redacción y es autor exclusivo de los pasteles al óleo que sustentan la investigación; asume la plena responsabilidad intelectual por la versión final del manuscrito.

- **Describe lo que se hizo.** El alcance incluye la redacción de borradores y el trazado de las ocho figuras porque así se preparó el texto.
- **Si reescribes el artículo con tus palabras** antes de enviarlo, puedes decirlo en el rol.
- **Cuando entren los escaneos de los pasteles,** quita del alcance «el diseño y trazado de los esquemas de encaje (figuras 1-6)». Si las exploraciones con GPT Image 2 influyeron en los pasteles, dilo.
- **Si redibujas a mano los diagramas 7 y 8,** quítalos también del alcance y cambia sus pies.
- **Lee la política de IA de la revista elegida.** Al menos una de primera línea, la *Revista Hispánica Moderna*, prohíbe redactar con IA generativa.

### 4. Hacer los pasteles y cambiar las figuras

La guía está en `03_guia_de_los_seis_pasteles`. Cuando tengas los escaneos:

- reemplaza los esquemas de las figuras 1 a 6 (la guía explica cómo, paso a paso);
- escribe en cada pie el soporte, las medidas y el año, en lugar de «Esquema de encaje del pastel al óleo. Fuente: elaboración propia con asistencia de IA»;
- reescribe el plano (3), *Contraste*, de cada figura con lo que hizo el pastel;
- ajusta la declaración de IA (paso 3).

Revisa también las notaciones de las figuras 1 a 6 (rótulos y decisiones marcadas con asterisco) y los diagramas 7 y 8 (rótulos y páginas). Decide si los diagramas entran.

### 5. Cotejar las citas con el libro impreso

Usa `04_fichero_de_pasajes`: trae las citas de la novela por página, con una casilla para marcar. Empieza por las pp. 88-107, donde la transcripción repite texto y alguna cita puede estar corrida una página.

Coteja también tres citas tomadas de fuentes escaneadas:

- Barnadas (1978 [1975]: 84), cuyo OCR estaba muy dañado;
- Zavaleta Mercado (1986: 21, n. 1);
- Cornejo Polar, si decides citar la 1.ª edición (véase el paso 6).

### 6. Revisar los datos que no se pudieron comprobar del todo

| Fuente | Qué falta |
|---|---|
| Cárcamo Pino (2019) | El artículo pone «Cham: Springer», que publicó las actas de EGA 2018. Cárcamo Pino (2025b) las cita como «Alicante: EGA, 2019». Elige una forma |
| Frampton (1995) | Confirmar en la portada el editor (John Cava) y la ciudad |
| Le Guin (2021 [1986]) | Completar la dirección exacta del texto en es.theanarchistlibrary.org |
| Alexander *et al.* (1977) | Las páginas citadas (xiii, xliii, 395, 405, 610-611, 621 y 1166) salen del OCR del libro. Cotejarlas con el impreso. Si consigues la edición castellana (Gustavo Gili), conviene citarla |
| Martin (2014: 85) y Scott (2020 [1998]: 3) | Paginaciones reconstruidas. Cotejar con el impreso si puedes |
| Spedding (2025) | Confirmar en el libro el año, el ISBN y las páginas de la sección (XIII-XXIII) |
| Rodríguez y Rodríguez (2025) | Confirmar la última página del capítulo (61) |
| Cornejo Polar (2003 [1994]: 41, 180) | Se cita la 2.ª edición (2003). Si prefieres la 1.ª (Horizonte, 1994), comprobar las páginas |
| Bertonio (2011 [1612]) | Se cita la transcripción digital. Si un evaluador lo pide, cotejar con el facsímil de 1612 |

### 7. Cotejar «Father Electricity»

El pasaje de la sección 7 («I do not want to see the whole mess / I wish I could live in retrospect») sale de la letra que aportaste. Es de *Tyranny* (2014), y el librillo de *Virtue* no lo trae.

- Cotéjalo con la letra oficial: el librillo de *Tyranny* o un servicio de *streaming* con letras con licencia.
- Si cambia algo (palabras, corte de verso, mayúsculas), dale al artículo la forma de esa fuente y di de dónde sale en la bibliografía, como ya se hizo con *Virtue*.
- Mientras tanto, si la revista pregunta, la cita es de la grabación y la transcripción es tuya.

### 8. Elegir la revista

Usa `05_revistas_candidatas`. Antes de decidir, abre la página oficial de cada revista y confirma la recepción, la extensión, el trato de las figuras, los cobros y la política de IA. Esos datos salen de extractos del buscador, no de una lectura directa.

### 9. Adaptar el texto a la revista

- **Formato y citas.** El Word sigue hoy la plantilla de *Estudios Bolivianos*. Según la revista, hará falta APA 7, MLA o Chicago.
- **Extensión.** Para *Atenea* (8.500 palabras con resumen y referencias) hay que quitar unas 1.800.
  - La palanca principal son los pies de figura analíticos y el Cuadro 1, unas 1.850 palabras: acórtalos o pasa parte de su análisis al texto.
  - Después vienen los cruces más alejados de la novela (Alexander en la sección 3, la casa difusa de la sección 5, las canciones) y los pasajes de trama que no llevan cita.
  - El marco teórico y la bibliografía deben quedar completos. Si una obra deja de citarse, sácala de la bibliografía.
- **La frase «Se trata de una investigación en desarrollo»** (final de la sección 1) respondía a una norma de *Estudios Bolivianos*. Decide si la mantienes.
- **Las figuras, aparte.** *Atenea* las pide en JPG o TIF, a 300 ppp o más y con 12 cm de ancho como mínimo, con su pie y su fuente.
- **Filiación.** No tienes una institucional. La salida habitual es «Investigador independiente, La Paz (Bolivia)». Si la revista pide filiación, pregúntale si la acepta.
- **ORCID.** Créalo antes del primer envío: es gratis y muchas plataformas lo exigen.

### 10. Preparar la versión anónima, si la piden

Para el arbitraje a doble ciego:

- quita tu nombre y la nota 1;
- deja «El autor» en las declaraciones, porque no identifica a nadie;
- borra tu nombre de las propiedades del archivo (en Word: Archivo → Información → Inspeccionar documento).

### 11. Enviar

Envía a una sola revista por vez: casi todas lo exigen. Anota la fecha de envío para reclamar respuesta según el plazo que declare la revista.

## Datos de autoría

| Dónde | Qué dice |
|---|---|
| Línea de autoría | Joaquin Max Cuevas Ventura |
| Nota 1 (80 palabras) | Licenciatura en Arquitectura (UMSA); técnico superior en Diseño Gráfico (Instituto Técnico Atenea); estudios de posgrado en Gestión BIM (Universidad Católica Boliviana); coordinación de Arquicinema (FAADU-UMSA); ocupación actual; áreas de trabajo; correo electrónico; La Paz, Bolivia |
| Final de la sección 1 | «Se trata de una investigación en desarrollo» |
| Conflicto de intereses | «El autor declara no tener conflictos de intereses» |

La nota no trae adscripción institucional ni publicaciones. Si tienes alguna, cabe. *Kipus* pide, además, una nota biobibliográfica de 100 a 150 palabras.

## Mejoras opcionales

No hacen falta para enviar. Cada una tiene su fuente:

1. **El concurso de 1940 (sección 1).** La nota «Al lector» de la edición citada dice que la novela se escribió «entre junio y agosto de 1940» para el Concurso de Novelas Latinoamericanas de la Unión Panamericana; que el jurado boliviano no la mencionó y envió la novela de Augusto Céspedes, *Metal del diablo*; y que ganó *El mundo es ancho y ajeno*, de Ciro Alegría, «cuyo argumento tiene un sorprendente parecido al de “Altiplano”» (Botelho Gosálvez, 1982 [1945]: 4). Una frase situaría la novela en su tiempo.
2. **Crítica previa por leer.** La tesis de Jacqueline M. O'Sullivan sobre Botelho Gosálvez (Universidad de Texas en El Paso, 1951), el estudio de Rodolfo A. Borello sobre *Raza de bronce* (1985) y Arriarán (2021: 29-31). Solo entran si los lees.
3. **Las fechas del autor.** Si la revista las pide: Raúl Botelho Gosálvez (La Paz, 1917-2004), según la ficha de autoridad de la Biblioteca Nacional de Francia.

## Lista final para marcar

- [ ] Artículo leído en voz alta y hecho propio
- [ ] Epígrafe confirmado o cambiado
- [ ] Declaración de IA revisada
- [ ] Pasteles hechos y escaneados; figuras, pies, plano (3) y declaración ajustados
- [ ] Notaciones de las figuras 1 a 6 y diagramas 7 y 8 revisados
- [ ] Citas de la novela cotejadas con el impreso
- [ ] Datos por confirmar revisados
- [ ] «Father Electricity» cotejado con la letra oficial
- [ ] Revista elegida y sus normas leídas en su web
- [ ] Texto adaptado: formato, citas, extensión y figuras aparte
- [ ] ORCID creado y filiación decidida
- [ ] Versión anónima, si la piden
- [ ] Envío, a una sola revista
