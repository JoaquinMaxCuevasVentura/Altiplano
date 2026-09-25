# Altiplano: artículo para *Estudios Bolivianos* N.º 43 (2026)

Borrador de artículo, análisis de fuentes y protocolo de exploración gráfica para el dossier «Narrativas, lenguajes y representaciones: memoria y ficción a través de las Humanidades» (IEB, FHCE, UMSA). **Plazo de envío: 25 de septiembre de 2026, a ieb.fhce@umsa.bo.**

## Artículo (versión 3, tras la depuración y cinco libros nuevos)

**«Topografías de la carne y el barro en *Altiplano*»**
*Topographies of Flesh and Mud in* Altiplano

Pregunta cómo construye *Altiplano* (1945; citado por la 7.ª ed., La Paz, Juventud, 1982) las posibilidades de habitar, permanecer y retirarse mediante las relaciones entre cuerpos, materiales, trabajo y autoridad. Sigue a tres familias —los Villca en la aldea de Umacachi, los Huanca en los Yungas, Juan Condori en la mina— y el retorno al ayllu. Sostiene que la novela produce el desamparo alterando el acceso a la tierra, el refugio, las herramientas, el salario y el desplazamiento, dentro y fuera de la comunidad, y que el retorno repone la pertenencia con más trabajo corporal y un recuerdo seleccionado.

- Lee la novela en tres planos (historia, narrador, investigador) y critica la voz narrativa: animalización, paternalismo, asimetrías de género, sexualización telúrica.
- Usa las referencias con funciones distintas: Vázquez Ramos *et al.* (historicidad del concepto de espacio) con una sola distinción de Lefebvre; Cárcamo Pino (manuaje; herramientas y escritorio en un mismo repertorio) y Pareyson; Martin (preguntas comparativas sobre la casa y el ascensor); Lundberg (cuatro operaciones, más el retorno al pasaje).
- Suma cinco libros, cada uno en la escena que lo necesita: Scott (legibilidad: Kero-Pata, el tinterillo, las huellas de la mina), Dean (los mojones como memoria de la posesión; la Pachamama), Frampton (masa apilada y armazón: la chujlla y la cosecha de piedras), Garrington (la galería medida con el cuerpo) y Le Guin (la novela como bolsa frente a la flecha de la mina).
- La exploración gráfica al pastel al óleo está en curso: el artículo presenta sus tres escenas y sus criterios de registro, no resultados, y no anuncia figuras que no existen.

| Archivo | Contenido |
|---|---|
| `articulo/articulo_altiplano.md` | Texto fuente (Markdown) |
| `articulo/articulo_altiplano.docx` | Versión Word con las normas: carta, márgenes de 2,5 cm, Times New Roman 12, interlineado 1,5 |
| `articulo/figuras/` | Aquí irán los pasteles cuando estén hechos y registrados (instrucciones en `LEEME.md`) |
| `articulo/generar_docx.py` | Regenera el `.docx` e informa la extensión y las palabras de los resúmenes |
| `articulo/plantilla_estudios_bolivianos.docx` | Plantilla de estilos que usa el generador |

**Estado:**

- 41.760 caracteres con espacios (el rango permitido es de 20.000 a 50.000); resumen de 99 palabras; abstract de 96.
- Se comprobaron automáticamente las 144 citas de la novela contra la transcripción: cada una existe literalmente y está en la página indicada. También se revisaron a mano los datos parafraseados y las citas de los cinco libros nuevos, con su página.
- **Faltan:** leer y hacer propio el texto; verificar a Arriarán (2021: 29-31); los datos de autoría; el ajuste de la declaración de IA; el cotejo con el impreso. Véase `analisis/04_verificaciones_y_pendientes.md`.

La versión anterior («La cosecha de piedras: dibujar el habitar en *Altiplano* de Botelho Gosálvez», con seis figuras previstas) queda en el historial de git.

## Análisis y protocolo

| Archivo | Contenido |
|---|---|
| `analisis/01_convocatoria_estudios_bolivianos_43.md` | Convocatoria: ejes (el principal es «discurso, poder y representaciones sociales»), normas, riesgos y correo de envío |
| `analisis/02_codigo_genetico_carcamo_pino.md` | El «código genético» de Cárcamo Pino: conceptos, métodos, estilo y recetario de emulación |
| `analisis/03_marco_cruzado.md` | Lundberg, Martin, Vázquez Ramos *et al.* y la novela (primera ronda). Una nota inicial indica qué conserva y qué retira la versión 3 |
| `analisis/04_verificaciones_y_pendientes.md` | Qué hacer y verificar antes de enviar |
| `analisis/05_guia_de_dibujo.md` | **Guía de la exploración gráfica**: tres escenas, ciclo de trabajo, plantilla de registro, criterios para elegir dos o tres figuras, pie modelo e inserción |
| `analisis/06_fichero_de_pasajes.md` | Las 144 citas de la novela ordenadas por página (para cotejar con el impreso), erratas de la transcripción, cautelas de lectura y tropos del narrador |
| `analisis/07_cinco_libros.md` | **Análisis de Scott, Dean, Frampton, Garrington y Le Guin**: pasajes con página, función y límite de cada uno en el artículo, y qué propuestas no se adoptaron y por qué |
| `analisis/esquemas/escena1…escena3` | Inventarios de las tres escenas (SVG): lo que da el texto y lo que el dibujo debe decidir. No son bocetos de las figuras |
| `analisis/esquemas/fig1…fig6` | Esquemas de la versión anterior, como material de reserva |
| `analisis/referencias_visuales/` | Las cuatro imágenes de referencia de la primera ronda. **No son las figuras del artículo** |

## Regenerar el Word

```bash
pip install pypandoc_binary python-docx
python3 articulo/generar_docx.py
```
