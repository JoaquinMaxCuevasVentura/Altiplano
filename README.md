# Altiplano: artículo para *Estudios Bolivianos* N.º 43 (2026)

Borrador de artículo y análisis de fuentes para el dossier «Narrativas, lenguajes y representaciones: memoria y ficción a través de las Humanidades» (IEB, FHCE, UMSA). **Plazo de envío: 25 de septiembre de 2026, a ieb.fhce@umsa.bo.**

## Artículo

**«Piedras puestas en el agua. Notas para redibujar *Altiplano* de Botelho Gosálvez»**
*Stones Set in Water: Notes for Redrawing Botelho Gosálvez's* Altiplano

Relee la novela *Altiplano* (1945) de Raúl Botelho Gosálvez desde la arquitectura. Usa cuatro dibujos al pastel al óleo como dispositivo de investigación mediante un *redibujo cruzado*: el método de cuatro pasos de Simon Lundberg injertado en la reescritura de referencias cruzadas de Mauricio Cárcamo Pino. Lo apoyan Richard Martin (la arquitectura en la ficción), Vázquez Ramos *et al.* (la historicidad del espacio), Lefebvre, Rivera Cusicanqui (lo *ch'ixi*) y las categorías aymaras *urqu/uma/taypi*.

| Archivo | Contenido |
|---|---|
| `articulo/articulo_piedras_puestas_en_el_agua.md` | Texto fuente (Markdown) |
| `articulo/articulo_piedras_puestas_en_el_agua.docx` | Versión Word con las normas: carta, márgenes 2,5 cm, Times New Roman 12, interlineado 1,5 |
| `articulo/figuras/` | Los cuatro pasteles (Figuras 1-4) |
| `articulo/generar_docx.py` | Regenera el `.docx` desde el Markdown e informa extensión y palabras de los resúmenes |
| `articulo/plantilla_estudios_bolivianos.docx` | Plantilla de estilos que usa el generador |

Estado: unos 40.400 caracteres con espacios (el rango permitido es 20.000-50.000); resumen de 99 palabras; abstract de 93. **Faltan:** los datos de autoría, las páginas de la novela, las fichas de los dibujos y el ajuste de la declaración de IA. Véase `analisis/04_verificaciones_y_pendientes.md`.

## Análisis

| Archivo | Contenido |
|---|---|
| `analisis/01_convocatoria_estudios_bolivianos_43.md` | Convocatoria: ejes, encaje, lista de normas, riesgos y correo de envío |
| `analisis/02_codigo_genetico_carcamo_pino.md` | El «código genético» de Cárcamo Pino: conceptos, métodos, estilo, plantillas y recetario de emulación |
| `analisis/03_marco_cruzado.md` | Lundberg, Martin (citas con página), Vázquez Ramos *et al.*, *Altiplano* (datos y onomástica), lectura de los dibujos y mapa de cruces |
| `analisis/04_verificaciones_y_pendientes.md` | Qué verificar y completar antes de enviar |

## Regenerar el Word

```bash
pip install pypandoc_binary python-docx
python3 articulo/generar_docx.py
```
