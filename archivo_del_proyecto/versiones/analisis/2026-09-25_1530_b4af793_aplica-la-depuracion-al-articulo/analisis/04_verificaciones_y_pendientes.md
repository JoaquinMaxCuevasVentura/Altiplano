# 4. Pendientes y verificaciones antes del envío

**Estado del artículo** «Topografías de la carne y el barro en *Altiplano*» (versión 3, que aplica la depuración recibida):

- 35.843 caracteres con espacios, bibliografía incluida (límite: 50.000; la depuración estimaba entre 31.000 y 35.000).
- Resumen de 99 palabras y abstract de 96 (límite: 100). Títulos de 9 y 7 palabras.
- 135 citas de la novela comprobadas contra la transcripción: todas existen literalmente y están en la página indicada. También se revisaron a mano los datos parafraseados (cifras, orden de los hechos, quién dice qué).
- Sin figuras. La exploración gráfica está en curso y el artículo solo presenta sus unidades y criterios (`05_guia_de_dibujo.md`).

## 4.1. Qué te toca hacer, en orden

1. **Leer el artículo entero y hacerlo tuyo.** La depuración lo pide expresamente: la revisión y la decisión autoral sobre las interpretaciones deben hacerse antes de firmar y enviar. Reescribe con tu voz lo que no reconozcas como propio.
2. **Verificar a Arriarán (2021: 29-31)** (§4.4). Es el único antecedente crítico que el artículo discute, y lo que dice de él procede de la depuración.
3. **Completar la autoría** (§4.2).
4. **Ajustar la declaración de IA** (§4.5).
5. **Cotejar las citas de la novela con el impreso**, empezando por las pp. 88-107 (`06_fichero_de_pasajes.md`, §6.1 y §6.4).
6. **Revisar los datos marcados B y C** (§4.3).
7. **Decidir qué hacer con las figuras** (`05_guia_de_dibujo.md`, §5.9).
8. **Regenerar el Word**: `python3 articulo/generar_docx.py`.
9. **Enviar** a ieb.fhce@umsa.bo (modelo de correo en `01_convocatoria_estudios_bolivianos_43.md`, §1.6). **El plazo vence hoy, 25 de septiembre de 2026.**

## 4.2. Marcadores ⟦…⟧ del artículo

| Dónde | Qué completar |
|---|---|
| Línea de autoría | Nombre y apellidos |
| Nota 1 | Formación y grado, adscripción, publicaciones principales, correo, ciudad y país (máximo 100 palabras) |
| Conflicto de intereses | «El autor» o «La autora» |
| Declaración de IA | Versión de ChatGPT y de Claude; los dos ⟦ajustar⟧ del alcance; «autor» o «autora» |

## 4.3. Verificación de fuentes

Estado de cada dato:

- **A**: leído en un documento adjunto.
- **B**: tomado de una fuente citada por un documento adjunto (se cita como «cit. en»). Basta para el artículo; consulta el original solo si quieres citarlo directamente.
- **C**: dato bibliográfico o de conocimiento general que no pude comprobar aquí.

| # | Dato | Estado | Acción |
|---|---|---|---|
| 1 | 135 citas de *Altiplano* y los datos parafraseados | A (transcripción) | Cotejar con el impreso, sobre todo las pp. 88-107 |
| 2 | Citas de Cárcamo Pino (2025a: 12; 2025b: 244, 246) | A | — |
| 3 | Definición de manuaje, Cárcamo Pino (2019: 1412) | B, vía 2025b: 244 | — |
| 4 | Editorial de Cárcamo Pino (2019) | C | El artículo pone «Cham: Springer», que publicó las actas de EGA 2018 (*Graphic Imprints*). Cárcamo Pino (2025b) las cita como «Alicante: EGA, 2019». Confirmar cuál prefieres |
| 5 | Pareyson (2002: 18) | B, vía 2025b: 246, n. 12 | Cárcamo Pino cita «*Estética: teoria de la formatividad*, vol. 1, Milán: Bompiani, 2002». El artículo da el título italiano, *Estetica. Teoria della formatività*, con fecha original de 1954. Confirmar la edición |
| 6 | Citas de Vázquez Ramos *et al.* (2023: 4) | A (traducción propia del portugués) | — |
| 7 | Lefebvre (1991: 38) | B, vía Vázquez Ramos *et al.*: 13 | Vázquez Ramos *et al.* citan solo la p. 38 |
| 8 | Citas de Lundberg (2019: 3, 21) | A | — |
| 9 | Citas de Martin (2014: 7, 63, 64, 69) | A* | Paginación reconstruida y validada. Cotejar dos o tres páginas con el libro impreso si puedes |
| 10 | Shonfield (2000: 173), Bachelard (1994: 6), Lynch en Rodley (2005: 10) | B, vía las notas de Martin | — |
| 11 | Arriarán (2021: 29-31) | C: procede de la depuración | Ver §4.4 |
| 12 | Barnadas (1977) | C | No consultado; el artículo lo dice. Confirmar ciudad (Cochabamba) y si hay coautor en la portada |

## 4.4. Arriarán y Barnadas

El artículo dice que Arriarán (2021: 29-31):

1. examina en *Altiplano* la oposición entre comunidad y afuera;
2. cuestiona el regreso al pasado como solución esencialista;
3. resume la muerte de Juan Condori como un accidente.

Las tres afirmaciones proceden de la depuración, que declara haber consultado esas páginas. **No pude comprobarlas**: el sitio donde está el libro no era accesible desde este entorno. Lee las pp. 29-31 antes de enviar. Si alguna afirmación no se sostiene, corrige el cuarto párrafo de la sección 1. Si Arriarán menciona el disparo, elimina la frase sobre el accidente.

Barnadas (1977) tiene 25 páginas y está registrado como «Raúl Botelho Gosálvez: *Altiplano*: esquema metodológico de aproximación a la narrativa boliviana», Los Amigos del Libro. El artículo dice que no se ha consultado y promete su lectura para la versión final.

## 4.5. Declaración de uso de IA (punto 8 de las normas)

Es obligatoria, y su omisión implica el rechazo. El artículo trae esta redacción, que debes ajustar a lo que hayas hecho de verdad:

> a) *Herramientas*: ChatGPT (OpenAI), ⟦versión⟧, y Claude (Anthropic), ⟦versión⟧, asistentes de inteligencia artificial generativa. b) *Alcance*: ChatGPT se empleó en la revisión conceptual del proyecto, el contraste de pasajes, la organización del argumento y el apoyo a la redacción ⟦ajustar⟧; Claude, en la lectura asistida de las fuentes, la localización y verificación de citas con su página y la redacción de borradores a partir de esa revisión ⟦ajustar⟧. c) *Rol*: el autor ⟦o la autora⟧ formuló el problema y las cautelas críticas, decidió las interpretaciones, revisó y reescribió los borradores, verificó las citas contra los originales, es autor ⟦o autora⟧ de la exploración gráfica y responde por la versión final.

La depuración advierte que el uso de ChatGPT no debe describirse como simple corrección ortográfica. Si no llegas a verificar las citas contra el impreso, no digas que lo hiciste: escribe «contra la transcripción de la edición citada».

## 4.6. Presupuesto de extensión

- Ahora: 35.843 caracteres.
- La nota de autor añadirá unos 500.
- Cada figura, con su pie y su párrafo de resultados, sumará entre 800 y 1.200.
- Con tres figuras el artículo quedaría cerca de 39.000, dentro del límite de 50.000.

## 4.7. Limitación del entorno de trabajo

La política de red del entorno donde se preparó el borrador bloqueó la lectura directa del libro de Arriarán (samuelarriaranhome.wpcomstaging.com), del registro de Google Books de Barnadas y de otros sitios (en.wikipedia.org, archive.org, researchgate.net, academia.edu, entre ellos). Por eso los datos marcados con C no se pudieron comprobar en línea.

Para ampliar el acceso en futuras sesiones, abre el menú del entorno de la nube (barra de título de la sesión) y elige *Edit* → *Network access*. Los niveles de acceso se describen en https://code.claude.com/docs/en/claude-code-on-the-web.

## 4.8. Lista final de envío

- [ ] Artículo leído y reescrito con voz propia; interpretaciones decididas (§4.1, paso 1)
- [ ] Arriarán (2021: 29-31) verificado (§4.4)
- [ ] Marcadores ⟦…⟧ completados (§4.2)
- [ ] Declaración de IA ajustada (§4.5)
- [ ] Citas cotejadas con el impreso (`06_fichero_de_pasajes.md`)
- [ ] Datos B y C revisados (§4.3)
- [ ] Decisión sobre las figuras (`05_guia_de_dibujo.md`, §5.9)
- [ ] `.docx` regenerado con menos de 50.000 caracteres y resúmenes de 100 palabras como máximo
- [ ] Versión anonimizada, si la piden
- [ ] Correo a ieb.fhce@umsa.bo hasta el 25 de septiembre de 2026
