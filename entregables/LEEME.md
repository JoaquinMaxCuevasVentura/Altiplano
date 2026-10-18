# Entregables finales de «Cosecha de piedras»

**«Cosecha de piedras: el ayllu, el Estado y la mina. Dibujando *Altiplano* de Raúl Botelho Gosálvez»**, de Joaquin Max Cuevas Ventura. Versión final del 11 de octubre de 2026, con cinco imágenes de dominio público añadidas el 18 de octubre.

Esta carpeta reúne los archivos finales del proyecto: el artículo y los cinco documentos que acompañan su envío. Cada documento va en Markdown (`.md`), para leerlo aquí, y en Word (`.docx`), para imprimirlo o editarlo. El artículo va en Word y en PDF.

| N.º | Archivo | Qué es | Para qué sirve |
|---|---|---|---|
| 01 | `01_articulo_cosecha_de_piedras.docx` y `.pdf` | El artículo final: 65.722 caracteres y 10.946 palabras, 33 páginas, 8 figuras, 5 imágenes de dominio público, el Cuadro 1 y 34 obras en la bibliografía | Leerlo, hacerlo tuyo y adaptarlo a la revista que elijas |
| 02 | `02_lista_de_envio` | Lo que está hecho y lo que falta, en orden, con el epígrafe, la declaración de IA, los datos por confirmar y la lista para marcar | Saber qué hacer antes de enviar |
| 03 | `03_guia_de_los_seis_pasteles` | Materiales, técnicas, el ciclo de trabajo y una ficha por figura | Hacer los pasteles que reemplazarán a los esquemas de las figuras 1 a 6 |
| 04 | `04_fichero_de_pasajes` | Las citas de la novela por página, con una casilla para marcar, y las cautelas de lectura | Cotejar las citas con el libro impreso |
| 05 | `05_revistas_candidatas` | Diez revistas ordenadas, lo que pide cada una, cuánto hay que recortar y qué hacer antes de enviar | Elegir adónde enviar el artículo |
| 06 | `06_atlas_de_arena` | Qué hay en los once canales privados de Are.na y qué falta | Volver a las fuentes visuales y a las pistas de lectura |

## Por dónde empezar

1. Lee el artículo (01) en voz alta.
2. Sigue la lista de envío (02). Te manda, en su momento, a la guía de los pasteles (03), al fichero de pasajes (04) y a las revistas (05).
3. Cuando tengas los escaneos de los pasteles, súbelos también al atlas (06).

## Lo que no está en esta carpeta

- **Las figuras y las imágenes sueltas.** Están en `articulo/figuras/`: ocho PNG, los esquemas de encaje de las figuras 1 a 6 y los diagramas 7 y 8, y cinco JPG, las imágenes de dominio público 1 a 5. Algunas revistas, como *Atenea*, las piden aparte. Las tres de Guaman Poma no alcanzan para imprimir: hay que pedirlas en alta resolución (lista de envío, paso 5). Los pasos para cambiarlas por los escaneos de los pasteles están en la guía (03, sección 6) y en `articulo/figuras/LEEME.md`.
- **El Word con cambios marcados.** Está en `articulo/articulo_cosecha_de_piedras_cambios.docx`, por si quieres revisar uno por uno los cambios de la última revisión: las cinco imágenes, sus frases y sus pies.
- **El registro de trabajo.** Los análisis de `analisis/` (del 01 al 31) y el informe completo de convocatorias, en `reports/`. De ahí salen estos documentos; no hace falta leerlos para enviar.

## Cómo rehacer los archivos

Si cambias el artículo o uno de estos documentos, desde la raíz del repositorio:

```bash
python3 articulo/generar_docx.py           # el Word del artículo
python3 entregables/generar_entregables.py # copia el artículo, hace su PDF y los Word de esta carpeta
```

El segundo necesita LibreOffice para el PDF.
