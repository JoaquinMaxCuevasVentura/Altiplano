# Instrucciones para agentes de IA

Este archivo es para cualquier asistente que trabaje en el repositorio, como Codex u otros. Léelo entero antes de cambiar nada.

## El proyecto

- **El artículo.** «Cosecha de piedras: el ayllu, el Estado y la mina. Dibujando *Altiplano* de Raúl Botelho Gosálvez», de Joaquin Max Cuevas Ventura. Lee la novela *Altiplano* (1945) desde la arquitectura y el dibujo.
- **Su estado** (11 de octubre de 2026):
  - versión final de 61.705 caracteres y 10.286 palabras, 29 páginas en Word;
  - 153 citas de la novela entre comillas y 2 en bloque;
  - 32 obras en la bibliografía.
- **El destino.** Sin elegir. La primera candidata es la revista *Atenea*, que pide recortar unas 1.800 palabras.
- **El autor decide.** Las interpretaciones, el título, el epígrafe, la tesis y la revista son suyos. Propón, explica y espera su respuesta; no cambies nada de eso por tu cuenta.
- **Lo que falta, en orden:** `entregables/02_lista_de_envio.md`.

## Dónde está cada cosa

| Ruta | Qué es | ¿Se edita? |
|---|---|---|
| `articulo/articulo_cosecha_de_piedras.md` | El texto fuente del artículo | Sí, solo con cambios aprobados por el autor |
| `articulo/articulo_cosecha_de_piedras.docx` | El Word, generado desde el `.md` | No a mano: se regenera |
| `articulo/articulo_cosecha_de_piedras_cambios.docx` | El Word con los cambios marcados respecto del commit 45624ba | No a mano |
| `articulo/figuras/` | Las ocho figuras y su `LEEME.md` | Sí, siguiendo el `LEEME.md` |
| `entregables/` | Los archivos finales: el artículo en Word y PDF y cinco documentos (`.md` y `.docx`) | Los `.md`, sí; los `.docx` y el `.pdf` se regeneran |
| `analisis/01_…` a `analisis/30_…` | El registro de cada etapa, con su fecha | **No se reescribe.** Solo se añaden notas o secciones fechadas |
| `taxonomia/` | La taxonomía visual: 51 imágenes de dominio público, su catálogo y tres tableros | `catalogo.json` y `LEEME.md`, sí; los tableros y `catalogo.md` se regeneran con `generar_tableros.py` |
| `reports/` y `research_notes/` | El informe de convocatorias y sus notas: registro | Igual que `analisis/` |
| `README.md` | El índice del repositorio | Sí, cuando cambie algo de lo que describe |

La rama del artículo es `claude/altiplano-botelho-article-jm2nlr`, que es la rama por defecto. Las ramas `claude/fervent-lovelace-exgqzl` y `claude/zen-cannon-kqblsc` son de otros proyectos: no las toques.

## Reglas de contenido

1. **No inventes citas, páginas, fuentes ni hallazgos.** Cada cita tiene que existir tal cual en su fuente y en la página indicada. Si no puedes comprobarla, no la añadas: déjala como pendiente y dilo.
2. **Las fuentes no están en el repositorio.** Faltan la transcripción paginada de la novela y los OCR de los libros, y el repositorio es público, así que no los subas. Sin ellas no se pueden volver a comprobar las citas. No cambies una cita salvo que el autor te dé la fuente.
3. **Las letras de canciones no se copian enteras.** Se citan uno o dos versos con su referencia. La de «Pyramid of Bones» sigue el librillo de la edición japonesa de *Virtue*. La de «Father Electricity» está pendiente de cotejo.
4. **Lenguaje llano, en español.**
   - Frases cortas; los términos técnicos se explican.
   - Comillas latinas «», y “ ” dentro de ellas.
   - Coma decimal y punto en los millares (61.705).
5. **Formato de las citas.** Autor y año con página: «(Botelho Gosálvez, 1982 [1945]: 96)», y luego «(ibid.: 102)». Las omisiones dentro de una cita van como «[...]». Mantén las cadenas de *ibid.* correctas si mueves texto.
6. **Las figuras.** La numeración es la del artículo: el Castillete es la 4, la Pelvis la 5 y el Centinela la 6. Las figuras 1 a 6 son esquemas que se reemplazarán por los escaneos de los pasteles del autor. Las imágenes hechas con generadores de IA son solo exploración y no se publican.
7. **La declaración de uso de IA.** Está al final del artículo y tiene que decir la verdad. Si redactas o corriges texto del artículo, avísale al autor y propón añadir la herramienta que usaste a la declaración.
8. **Datos personales.** El repositorio es público. No añadas datos personales del autor más allá de los que ya figuran en el artículo.

## Cómo regenerar los archivos

```bash
pip install pypandoc_binary python-docx pillow
python3 articulo/generar_docx.py                        # el Word del artículo; informa caracteres y palabras
git checkout -- articulo/plantilla_estudios_bolivianos.docx   # el generador reescribe la plantilla: devuélvela
python3 entregables/generar_entregables.py              # copia el artículo, hace su PDF (necesita LibreOffice) y los Word de entregables/
node analisis/esquemas/diagramas/generar_diagramas.js   # las notaciones SVG de las figuras 1 a 8
python3 articulo/generar_figuras.py                     # los PNG de las figuras (necesita Chromium; variable CHROME)
python3 taxonomia/generar_tableros.py                   # los tableros de la taxonomía visual y su catálogo (Chromium)
```

Cada vez que cambie el artículo:

- regenera los dos Word y el PDF con los comandos de arriba;
- pon al día las cifras de extensión (caracteres, palabras, páginas) donde aparecen: `README.md`, `entregables/LEEME.md`, `entregables/02_lista_de_envio.md` y `entregables/05_revistas_candidatas.md`;
- si cambia una cita de la novela, pon al día también la tabla de `entregables/04_fichero_de_pasajes.md`.

## Antes de proponer cambios

- [ ] `git diff --check`: sin espacios sobrantes.
- [ ] El Word regenerado y la extensión informada por `generar_docx.py`.
- [ ] La plantilla devuelta a su estado (`git status` no la muestra).
- [ ] Sin archivos de paso: `__pycache__`, PDF de prueba, fotos o letras completas.
- [ ] Ninguna cita, página ni fuente nueva sin comprobar.

## Ramas y commits

- **No escribas directamente en `claude/altiplano-botelho-article-jm2nlr`.** Trabaja en una rama propia y propone los cambios con un *pull request* hacia esa rama. Así el autor los revisa antes de unirlos, y no chocan con otros asistentes que trabajan en el mismo proyecto.
- **Commits en español,** con un título que diga qué cambia, como los del historial: `Coteja «Pyramid of Bones» con el librillo japonés de Virtue`. En el cuerpo, explica qué cambió y por qué.
