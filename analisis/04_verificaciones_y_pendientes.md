# 4. Pendientes y verificaciones antes del envío

> **Versión revisada.** Hay un borrador que responde a las cinco objeciones del arbitraje con diez fuentes nuevas: `articulo/articulo_cosecha_de_piedras_revisado.md` (49.207 caracteres). Este documento sigue describiendo el artículo definitivo. Qué cambia en el borrador, con qué fuentes y qué te toca decidir: `08_respuesta_al_arbitraje.md`.

**Estado del artículo definitivo**, «La cosecha de piedras: dibujar el habitar en *Altiplano* de Botelho Gosálvez». Es la versión 2 completa, reforzada con cinco libros (Scott, Dean, Frampton, Garrington y Le Guin; véase `07_cinco_libros.md`), con la escena del tinterillo y con compresión sintáctica de la trama.

- **Extensión.** 48.989 caracteres con espacios, bibliografía incluida. El rango pedido es de 47.500 a 49.500; el límite de la revista, 50.000.
- **Resúmenes y títulos.** Resumen de 95 palabras y abstract de 93 (límite: 100). Títulos de 12 y 10 palabras.
- **Citas de la novela.** Las 147 citas se comprobaron contra la transcripción: todas existen literalmente y están en la página indicada. También las del Cuadro 1. Se revisaron a mano los datos parafraseados.
- **Correcciones.** Esa revisión corrigió tres datos de la versión 2:
  - la «encerrona» es la casa municipal, no la plaza;
  - el vecindario agradece la carne, no «felicita»;
  - el contratista del aserradero termina contratando a Paulo.
- **Cadenas de «ibid.».** Todas remiten a la obra correcta.
- **Citas de los cinco libros.** Se cotejaron con sus originales, con la página (§4.3).
- **Figuras.** Seis, numeradas por orden de aparición: Castillete = 4, Pelvis = 5, Centinela = 6. Son los esquemas de encaje de los pasteles, hechos con asistencia de IA y declarados así (§4.4).

## 4.1. Qué te toca hacer, en orden

1. **Leer el artículo entero y hacerlo tuyo.** Reescribe con tu voz lo que no reconozcas como propio y decide cada interpretación antes de firmar.
2. **Decidir las figuras** (§4.4): esquemas de encaje, como ahora, o fotografías de los pasteles (`articulo/figuras/LEEME.md`).
3. **Elegir el estado de la investigación.** Al final de la sección 1 hay un marcador: «Se trata de una investigación ⟦en desarrollo / concluida⟧». Las normas piden aclararlo al inicio.
4. **Completar la autoría** (§4.2).
5. **Ajustar la declaración de IA** (§4.5).
6. **Cotejar las citas de la novela con el impreso**, empezando por las pp. 88-107 (`06_fichero_de_pasajes.md`, §§6.1 y 6.4).
7. **Revisar los datos marcados B y C** (§4.3).
8. **Regenerar el Word** con `python3 articulo/generar_docx.py` y comprobar que la extensión siga entre 47.500 y 49.500 (§4.6).
9. **Enviar** a ieb.fhce@umsa.bo (modelo de correo en `01_convocatoria_estudios_bolivianos_43.md`, §1.6). **El plazo venció el 25 de septiembre de 2026**: si aún no enviaste, conviene escribir a la revista antes de mandar el archivo.

## 4.2. Marcadores ⟦…⟧ del artículo

| Dónde | Qué completar |
|---|---|
| Línea de autoría | Nombre y apellidos |
| Nota 1 | Formación y grado, adscripción, publicaciones principales, correo, ciudad y país (máximo 100 palabras) |
| Final de la sección 1 | «en desarrollo» o «concluida» |
| Conflicto de intereses | «El autor» o «La autora» |
| Declaración de IA | Versión de ChatGPT y de Claude; los dos ⟦ajustar⟧ del alcance; «autor» o «autora» |

## 4.3. Verificación de fuentes

Estado de cada dato:

- **A**: leído en un documento adjunto.
- **B**: tomado de una fuente citada por un documento adjunto (se cita como «cit. en»). Basta para el artículo; consulta el original solo si quieres citarlo directamente.
- **C**: dato bibliográfico o de conocimiento general que no pude comprobar aquí.

| # | Dato | Estado | Acción |
|---|---|---|---|
| 1 | 147 citas de *Altiplano* y los datos parafraseados | A (transcripción) | Cotejar con el impreso, sobre todo las pp. 88-107 |
| 2 | Citas de Cárcamo Pino (2025a: 8, 12; 2025b: 244, 245, 246, 259) | A | — |
| 3 | Definición de manuaje, Cárcamo Pino (2019: 1412) | B, vía 2025b: 244 | — |
| 4 | Editorial de Cárcamo Pino (2019) | C | El artículo pone «Cham: Springer», que publicó las actas de EGA 2018. Cárcamo Pino (2025b) las cita como «Alicante: EGA, 2019». Confirmar cuál prefieres |
| 5 | Pareyson (2002: 18) | B, vía 2025b: 246 | Cárcamo Pino cita una edición española de 2002; la bibliografía da el título italiano. Confirmar la edición |
| 6 | Vázquez Ramos *et al.* (2023: 3-8, 13) y las citas que recogen (Alberti, Schmarsow, Worringer, Hall, Lefebvre) | A / B | Traducción propia del portugués. Lefebvre, p. 38, como lo citan ellos |
| 7 | Lundberg (2019: 3, 15, 18, 21) | A | — |
| 8 | Martin (2014: 7, 13, 25, 63, 64, 66, 71, 84, 85, 88, 99, 137, 138) y lo que cita (Shonfield, Bachelard, Colomina, Freud, Vidler, Deleuze, Foucault) | A* / B | Paginación de Martin reconstruida y validada; cotejar dos o tres páginas con el impreso si puedes |
| 9 | Loos (1972 [1910]) | C | El túmulo del bosque, sin página. Añade la página de la edición de Gustavo Gili si la tienes |
| 10 | Scott (2020 [1998]: 3, 35-36) | A (texto) con páginas del índice analítico | El archivo no trae números de página: cotejar las dos páginas con el impreso |
| 11 | Dean (2010: 5, 44, 68, 202 n. 86) | A | Páginas reconstruidas con los encabezados del archivo y comprobadas con el índice. La n. 86 dice que «Wank'a» y sus variantes «Huanca» o «Guanca» se usaban como nombre de varón entre los incas |
| 12 | Frampton (1995: 5) | A (escaneo de la introducción) | Confirmar en la portada el editor (John Cava) y la ciudad de la bibliografía |
| 13 | Garrington (2013: 2, 16) | A | Paginación comprobada con el índice |
| 14 | Le Guin (2021 [1986]: 8, 10, 11) | A (PDF de la traducción de Nedev y Pérez de Lama) | Completar la URL exacta en es.theanarchistlibrary.org |

## 4.4. Las figuras: qué dice el artículo y qué no

- **Qué afirma.** El artículo presenta seis pasteles al óleo como instrumentos de lectura y los analiza en tres planos:
  - (1) el texto;
  - (2) la operación del pastel;
  - (3) el hallazgo que surge al contrastarlos.

  Las figuras reproducen el **esquema de encaje** de cada pastel. El pie lo dice («Esquema de encaje del pastel al óleo. Fuente: elaboración propia con asistencia de IA»), y la declaración de IA precisa que Claude elaboró esos esquemas.
- **Qué no afirma.** No dice si los pasteles están terminados o en curso, ni describe resultados de piezas que no se muestran. Cada *Hallazgo* se apoya en el texto de la novela, con su página, y puede verificarse en el esquema.
- **Si tienes fotografías de los pasteles**, puedes sustituir los esquemas: pasos en `articulo/figuras/LEEME.md`. En ese caso:
  - escribe en el pie los datos reales de cada pieza (soporte, medidas, año);
  - revisa los planos (2) y (3) con lo que hizo cada pastel;
  - ajusta la declaración de IA.

## 4.5. Declaración de uso de IA (punto 8 de las normas)

Es obligatoria, y su omisión implica el rechazo. El artículo trae esta redacción, que debes ajustar a lo que hiciste de verdad:

> a) *Herramientas*: ChatGPT (OpenAI), ⟦versión⟧, y Claude (Anthropic), ⟦versión⟧, asistentes de inteligencia artificial generativa.
>
> b) *Alcance*: ChatGPT se empleó en la revisión conceptual del proyecto, el contraste de pasajes, la organización del argumento y el apoyo a la redacción ⟦ajustar⟧; Claude, en la lectura asistida de las fuentes, la localización y verificación de citas con su página, la redacción de borradores, el diseño del protocolo de dibujo y la elaboración de los esquemas de encaje reproducidos en las figuras 1 a 6 ⟦ajustar⟧.
>
> c) *Rol*: el autor ⟦o la autora⟧ formuló el problema, el esquema del artículo y las cautelas críticas; decidió las interpretaciones; es autor ⟦o autora⟧ de los pasteles al óleo; revisó y reescribió los borradores, verificó las citas contra los originales y responde por la versión final.

Dos advertencias:

- El uso de ChatGPT no debe describirse como simple corrección ortográfica.
- Si no llegas a verificar las citas contra el impreso, no digas que lo hiciste. Escribe, en cambio, «contra la transcripción de la edición citada».

## 4.6. Extensión

- **Ahora:** 48.989 caracteres, con los marcadores de autoría todavía sin completar.
- **Nota de autor y nombre:** caben unos 650 caracteres de nota (unas 95 palabras) sin pasar de 49.500.
- **Si te pasas:**
  - acorta la nota de autor;
  - o resume en el texto un pasaje de trama que no lleve cita.

  El marco teórico, el Cuadro 1 y la bibliografía deben quedar completos.
- **Comprobación:** `python3 articulo/generar_docx.py` informa la extensión exacta.

## 4.7. Antecedentes críticos: un riesgo de arbitraje

El artículo definitivo no discute la crítica previa sobre *Altiplano*. La versión 3 citaba a Arriarán (2021: 29-31) y a Barnadas (1977). Las normas piden una «revisión de la literatura», y un evaluador puede echarla de menos.

- **La versión revisada** cita la crítica del narrador indigenista de Cornejo Polar (2003 [1994]: 180) y se sitúa frente a ella (`08_respuesta_al_arbitraje.md`, §8.1).
- **La referencia a Barnadas (1977) de la versión 3 no debe usarse.** El tomo que enviaste (Barnadas y Coy, *Realidad sociohistórica y expresión literaria en Bolivia*, 1977) incluye *Altiplano* en su corpus (p. 36), pero no la analiza. Su contratapa enumera los ocho estudios publicados, y el de Botelho es sobre *Coca*. El folleto «Raúl Botelho Gosálvez: Altiplano» no consta.

- **Si puedes leer las pp. 29-31 de Arriarán**, un párrafo breve al final de la sección 1 bastaría (unos 400 caracteres; hay margen si la nota de autor es corta).
- **Si no las verificas, no lo añadas.** Lo que la versión 3 decía de Arriarán procede de la depuración y no pude comprobarlo: el sitio donde está el libro no era accesible desde este entorno.
- **La entrada bibliográfica** está en `articulo/articulo_altiplano.md`.

## 4.8. Limitación del entorno de trabajo

La política de red del entorno donde se preparó el borrador bloqueó varios sitios: el libro de Arriarán (samuelarriaranhome.wpcomstaging.com), el registro de Google Books de Barnadas, en.wikipedia.org, archive.org, researchgate.net y academia.edu, entre otros. Por eso los datos marcados con C no se pudieron comprobar en línea.

Para ampliar el acceso en futuras sesiones, abre el menú del entorno de la nube (barra de título de la sesión) y elige *Edit* → *Network access*. Los niveles de acceso se describen en https://code.claude.com/docs/en/claude-code-on-the-web.

## 4.9. Lista final de envío

- [ ] Artículo leído y reescrito con voz propia; interpretaciones decididas
- [ ] Figuras decididas: esquemas o fotografías, con su pie (§4.4)
- [ ] Estado de la investigación elegido en la sección 1
- [ ] Marcadores ⟦…⟧ completados (§4.2)
- [ ] Declaración de IA ajustada (§4.5)
- [ ] Citas cotejadas con el impreso (`06_fichero_de_pasajes.md`)
- [ ] Datos B y C revisados (§4.3)
- [ ] `.docx` regenerado: entre 47.500 y 49.500 caracteres y resúmenes de 100 palabras como máximo
- [ ] Versión anonimizada, si la piden
- [ ] Correo a ieb.fhce@umsa.bo hasta el 25 de septiembre de 2026
