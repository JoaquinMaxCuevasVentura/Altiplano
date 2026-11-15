# 4. Pendientes y verificaciones antes del envío

**Estado del artículo** «La cosecha de piedras: dibujar el habitar en *Altiplano* de Botelho Gosálvez»:

- 48.220 caracteres con espacios, bibliografía incluida (límite: 50.000).
- Resumen de 99 palabras y abstract de 97 (límite: 100).
- Texto, cuadro, citas y bibliografía completos.
- **Faltan los seis pasteles.** El artículo presenta su protocolo y formula el tercer plano de cada figura como hipótesis.

## 4.1. Qué te toca hacer, en orden

1. **Dibujar los seis pasteles** con `05_guia_de_dibujo.md`. Si no llegas al plazo, lee la §5.7 de la guía.
2. **Insertar las figuras** y completar sus pies (guía, §5.6).
3. **Reescribir el plano (3)** de cada figura: de «Contraste (hipótesis)» a «Hallazgo» (guía, §5.5). Ajusta también:
   - en la sección 1: «los seis pasteles están en ejecución, y aquí se presentan su protocolo y las hipótesis…»;
   - en la sección 2, al final: «formulado como hipótesis mientras los pasteles se completan»;
   - en la sección 8, segundo párrafo: «En esta fase, más preguntas que respuestas…» y «Las seis hipótesis serán confirmadas o corregidas…»;
   - en el resumen, si quieres, «propone» por «realiza».
4. **Completar la autoría** (§4.2).
5. **Ajustar la declaración de IA** (§4.5).
6. **Cotejar las citas de la novela con el impreso**, empezando por las pp. 88-107 (`06_fichero_de_pasajes.md`, §6.1 y §6.4).
7. **Revisar los datos marcados B y C** (§4.3).
8. **Regenerar el Word**: `python3 articulo/generar_docx.py`. Debe informar menos de 50.000 caracteres.
9. **Enviar** a ieb.fhce@umsa.bo (§4.6). **El plazo vence el 25 de septiembre de 2026.**

## 4.2. Marcadores ⟦…⟧ del artículo

| Dónde | Qué completar |
|---|---|
| Línea de autoría | Nombre y apellidos |
| Nota 1 | Formación y grado, adscripción, publicaciones principales, correo, ciudad y país (máximo 100 palabras) |
| Figuras 1-6 | Sustituir `⟦Figura N: pastel al óleo en ejecución⟧` por la imagen; completar `⟦soporte, medidas, año⟧` |
| Conflicto de intereses | «El autor» o «La autora» |
| Declaración de IA | Versión o modelo; «autor» o «autora» |

## 4.3. Verificación de fuentes

Estado de cada dato:

- **A**: leído en un documento adjunto.
- **B**: tomado de una fuente citada por un documento adjunto (se cita como «cit. en»). Basta para el artículo; consulta el original solo si quieres citarlo directamente.
- **C**: dato bibliográfico o de conocimiento general que no pude comprobar aquí.

| # | Dato | Estado | Acción |
|---|---|---|---|
| 1 | 162 citas de *Altiplano* | A (transcripción) | Cotejar con el impreso, sobre todo las pp. 88-107 |
| 2 | Citas de Cárcamo Pino (2025a, 2025b) | A | — |
| 3 | Cárcamo Pino (2019: 1412) y Salazar Sánchez y Cárcamo Pino (2021: 1482) | B, vía 2025b: 244-245 | — |
| 4 | Editorial de Cárcamo Pino (2019) | C | El artículo pone «Cham: Springer»; Cárcamo Pino (2025b) la cita como «Alicante: EGA, 2019». Confirmar cuál corresponde al volumen *Graphic Imprints* |
| 5 | Pareyson (2002: 18) | B, vía 2025b: 246, n. 12 | Cárcamo Pino titula la obra en castellano; el artículo da el título italiano con fecha original de 1954. Confirmar |
| 6 | Corona Martínez (2009 [1990]: 50) | B, vía 2025a: 12 | Confirmar ciudad (Buenos Aires) de la editorial Nobuko |
| 7 | Citas de Vázquez Ramos *et al.* (2023) | A (traducción propia del portugués) | — |
| 8 | Hall (1973: 133) | B, vía Vázquez Ramos *et al.*: 3 | Es una retraducción desde el portugués. Si tienes la edición española (IEAL, 1973), cita su redacción literal |
| 9 | Alberti (2011: 147), Schmarsow (1994: 286), Worringer (1953: 56), Lefebvre (1991: 38-39) | B, vía Vázquez Ramos *et al.* | Worringer tiene edición española (FCE): si la consultas, usa su redacción |
| 10 | Citas de Lundberg (2019) | A | — |
| 11 | Citas de Martin (2014) y sus páginas | A* | Paginación reconstruida y validada. Cotejar dos o tres páginas con el libro impreso si puedes |
| 12 | Shonfield (2000: 173), Bachelard (1994: 6, 102), Freud (2003: 124), Vidler (1992: 32), Colomina (1992: 95; 1994: 276), Deleuze (2003: 100), Foucault (1986: 25, 27) | B, vía las notas de Martin | — |
| 13 | Páginas del capítulo de Colomina (1992) en *Sexuality and Space* | C | Añadir el rango de páginas en la bibliografía |
| 14 | Traductor de Deleuze (2003) | C | Las notas de Martin dicen «David W. Smith»; el traductor es Daniel W. Smith, como pone el artículo. Confirmar |
| 15 | Loos (1972 [1910]), el túmulo en el bosque | C | Paráfrasis del ensayo «Arquitectura» (1910). Confirmar edición y traductores de Gustavo Gili; añadir página si citas literalmente |
| 16 | Etimologías: *texto* < *textus*; *urdir*; *domesticar* < *domus*; *histérico* < *hystéra* | C | Son estándar; conviene cotejarlas en el DLE o en Corominas por si un árbitro lo pide |

## 4.4. Presupuesto de extensión

- Ahora: 48.220 caracteres, con los marcadores de figura.
- La nota de autor añadirá unos 500.
- Sustituir los seis marcadores por imágenes restará unos 250.
- Si al reescribir las hipótesis como hallazgos crece el texto, compensa recortando en el mismo apartado.

## 4.5. Declaración de uso de IA (punto 8 de las normas)

Es obligatoria, y su omisión implica el rechazo. El artículo trae esta redacción, que debes ajustar a lo que hayas hecho de verdad:

> a) *Herramientas*: Claude (Anthropic), asistente de inteligencia artificial generativa, ⟦indicar versión o modelo⟧. b) *Alcance*: lectura asistida de las fuentes, localización y verificación de pasajes con su página, análisis estilístico de textos de referencia, propuesta de estructura, redacción de un borrador completo y diseño del protocolo de dibujo. c) *Rol*: el autor ⟦o la autora⟧ formuló el problema, el esquema del artículo y las cautelas críticas; es autor ⟦o autora⟧ de los dibujos; revisó y reescribió el borrador, verificó las citas contra los originales y es responsable de la versión final.

Cuanto más reescribas con tu voz, más tuyo será el texto y más fácil será defenderlo en el arbitraje.

## 4.6. Correo de envío (modelo)

> Adjunto el artículo «La cosecha de piedras: dibujar el habitar en *Altiplano* de Botelho Gosálvez» para su consideración en el dossier «Narrativas, lenguajes y representaciones: memoria y ficción a través de las Humanidades» del número 43 de *Estudios Bolivianos*. Se trata de una investigación en desarrollo, original e inédita, que no ha sido enviada a otra revista. El texto incluye la declaración sobre el uso de herramientas de inteligencia artificial que exige el punto 8 de las normas.

Pregunta a los editores si quieren, para el doble ciego, un archivo anonimizado y una portada aparte.

## 4.7. Limitación del entorno de trabajo

La política de red del entorno donde se preparó el borrador bloqueó la lectura directa de en.wikipedia.org, abebooks.com, idoc.pub, scribd.com, biblioteca.clacso.edu.ar, archive.org, redalyc.org, researchgate.net y academia.edu, entre otros. Por eso los datos marcados con C no se pudieron comprobar en línea.

Para ampliar el acceso en futuras sesiones, abre el menú del entorno de la nube (barra de título de la sesión) y elige *Edit* → *Network access*. Los niveles de acceso se describen en https://code.claude.com/docs/en/claude-code-on-the-web.

## 4.8. Lista final de envío

- [ ] Seis pasteles realizados, escaneados e insertados (§4.1, pasos 1-2)
- [ ] Plano (3) de cada figura reescrito como hallazgo, y frases de estado actualizadas (§4.1, paso 3)
- [ ] Marcadores ⟦…⟧ completados (§4.2)
- [ ] Citas cotejadas con el impreso (`06_fichero_de_pasajes.md`)
- [ ] Datos B y C revisados (§4.3)
- [ ] Declaración de IA ajustada (§4.5)
- [ ] `.docx` regenerado con menos de 50.000 caracteres y resúmenes de 100 palabras como máximo
- [ ] Versión anonimizada, si la piden
- [ ] Correo a ieb.fhce@umsa.bo hasta el 25 de septiembre de 2026
