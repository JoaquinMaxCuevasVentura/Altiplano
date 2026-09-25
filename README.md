# Altiplano: artículo para *Estudios Bolivianos* N.º 43 (2026)

Borrador de artículo, análisis de fuentes y protocolo de dibujo para el dossier «Narrativas, lenguajes y representaciones: memoria y ficción a través de las Humanidades» (IEB, FHCE, UMSA). **Plazo de envío: 25 de septiembre de 2026, a ieb.fhce@umsa.bo.**

## Artículo (versión 2)

**«La cosecha de piedras: dibujar el habitar en *Altiplano* de Botelho Gosálvez»**
*The Harvest of Stones: Drawing Dwelling in Botelho Gosálvez's* Altiplano

Relee *Altiplano* (1945; citado por la 7.ª ed., La Paz, Juventud, 1982) a partir de la «cosecha de piedras» de la p. 9. Sigue el montón de piedras —pirca, casa, tumba, escombro— por el ayllu, la aldea de Umacachi, los Yungas y la mina «Pensylvania», hasta el retorno. Los materiales teóricos intervienen en el examen de los pasajes:

- la crítica histórica del espacio de Vázquez Ramos *et al.*, con Hall, Alberti, Schmarsow, Worringer y Lefebvre;
- el manuaje y la formatividad de Cárcamo Pino y Pareyson;
- la lectura arquitectónica de la ficción de Martin: Bachelard, Freud, Loos, Bacon y Deleuze, Foucault;
- las cuatro operaciones de Lundberg, adaptadas a la lectura.

Propone seis pasteles al óleo, cada uno examinado en tres planos: texto, operación del pastel y contraste. Critica la voz del narrador (animalización, sexualización, petrificación) y evita la oposición entre la mano y el papel.

| Archivo | Contenido |
|---|---|
| `articulo/articulo_cosecha_de_piedras.md` | Texto fuente (Markdown) |
| `articulo/articulo_cosecha_de_piedras.docx` | Versión Word con las normas: carta, márgenes de 2,5 cm, Times New Roman 12, interlineado 1,5 |
| `articulo/figuras/` | Aquí van los seis pasteles cuando estén escaneados (`figura_1.jpg` … `figura_6.jpg`) |
| `articulo/generar_docx.py` | Regenera el `.docx` e informa la extensión y las palabras de los resúmenes |
| `articulo/plantilla_estudios_bolivianos.docx` | Plantilla de estilos que usa el generador |

**Estado:**

- 48.271 caracteres con espacios (el rango permitido es de 20.000 a 50.000); resumen de 99 palabras; abstract de 97.
- Se comprobaron automáticamente las 162 citas de la novela contra la transcripción: cada una existe literalmente y está en la página indicada.
- **Faltan:** los seis pasteles, que todavía no están hechos (las figuras van como marcadores ⟦…⟧); los datos de autoría; y el ajuste de la declaración de IA. Véase `analisis/04_verificaciones_y_pendientes.md`.

## Análisis y protocolo

| Archivo | Contenido |
|---|---|
| `analisis/01_convocatoria_estudios_bolivianos_43.md` | Convocatoria: ejes, encaje, lista de normas, riesgos y correo de envío |
| `analisis/02_codigo_genetico_carcamo_pino.md` | El «código genético» de Cárcamo Pino: conceptos, métodos, estilo y recetario de emulación |
| `analisis/03_marco_cruzado.md` | Lundberg, Martin, Vázquez Ramos *et al.* y la novela (primera ronda, con correcciones) |
| `analisis/04_verificaciones_y_pendientes.md` | Qué hacer y verificar antes de enviar |
| `analisis/05_guia_de_dibujo.md` | **Guía para realizar los seis pasteles**: materiales, técnicas, fichas por figura, paletas tomadas de la novela y cómo reescribir hipótesis como hallazgos |
| `analisis/06_fichero_de_pasajes.md` | Las 162 citas de la novela ordenadas por página (para cotejar con el impreso), erratas de la transcripción y tropos del narrador |
| `analisis/esquemas/` | Seis esquemas de encaje (SVG), uno por figura |
| `analisis/referencias_visuales/` | Las cuatro imágenes de referencia de la primera ronda. **No son las figuras del artículo** |

## Regenerar el Word

```bash
pip install pypandoc_binary python-docx
python3 articulo/generar_docx.py
```
