# Altiplano: artículo para *Estudios Bolivianos* N.º 43 (2026)

Artículo, análisis de fuentes y protocolo gráfico para el dossier «Narrativas, lenguajes y representaciones: memoria y ficción a través de las Humanidades» (IEB, FHCE, UMSA). **Plazo de envío: 25 de septiembre de 2026, a ieb.fhce@umsa.bo.**

## Artículo definitivo

**«La cosecha de piedras: dibujar el habitar en *Altiplano* de Botelho Gosálvez»**
*The Harvest of Stones: Drawing Dwelling in Botelho Gosálvez's* Altiplano

Relee *Altiplano* (1945; citado por la 7.ª ed., La Paz, Juventud, 1982) desde su «cosecha de piedras»: el montón es la arquitectura mínima de la novela (pirca, casa, tumba, escombro). Sostiene que la novela piensa el habitar como manipulación de la piedra, el despojo como su captura por una red de personas, papeles y máquinas, y la memoria como reparación selectiva del lugar; y que su narrador, al denunciar, también petrifica a quienes describe.

- **Base:** la versión 2 completa, con toda su constelación teórica: Loos (el túmulo), Colomina (el intruso, el umbral), Freud y Vidler (del pesebre a la tumba), Bacon y Deleuze (la carne, la jaula, la catástrofe), Worringer (la petrificación), Bachelard (la casa y el nido), Alberti, Schmarsow, Hall, Lefebvre, Foucault, Cárcamo Pino, Corona Martínez, Pareyson, Lundberg y Martin.
- **Cinco libros injertados:**
  - Frampton: estereotomía y tectónica en el túmulo, la chujlla y los callapos.
  - Dean: la *wank'a* frente a la petrificación de Worringer, en el apellido Huanca; la Pachamama.
  - Garrington: la prosa háptica y la huella dactilar.
  - Scott: la legibilidad estatal en el radio urbano y en el tinterillo.
  - Le Guin: la ficción del arma (la mina) y la del recipiente (el ayllu).
- **La escena del tinterillo completa**, con el manuaje burocrático del infolio.
- **Corrección filológica de la p. 132:** la hija de Paulo «había sido desflorada por el patrón»; luego la desesperación la «obligó a venderse».
- **Seis figuras** analizadas en tres planos (texto, operación, hallazgo) y el Cuadro 1 completo. Las figuras son los **esquemas de encaje** de cada pastel, hechos con asistencia de IA y declarados como tales en el pie y en la declaración de IA. Numeradas por orden de aparición: Castillete = 4, Pelvis = 5, Centinela = 6.

| Archivo | Contenido |
|---|---|
| `articulo/articulo_cosecha_de_piedras.md` | Texto fuente (Markdown) |
| `articulo/articulo_cosecha_de_piedras.docx` | Versión Word con las normas: carta, márgenes de 2,5 cm, Times New Roman 12, interlineado 1,5 |
| `articulo/figuras/` | Las seis figuras y cómo sustituirlas por fotografías de los pasteles (`LEEME.md`) |
| `articulo/generar_docx.py` | Regenera el `.docx` e informa la extensión y las palabras de los resúmenes |
| `articulo/generar_figuras.py` | Regenera las figuras a partir de los esquemas SVG |
| `articulo/plantilla_estudios_bolivianos.docx` | Plantilla de estilos que usa el generador |
| `articulo/articulo_altiplano.md` y `.docx` | Versión 3, «Topografías de la carne y el barro en *Altiplano*»: alternativa sin figuras, con antecedentes críticos (Arriarán, Barnadas) |

**Estado:**

- 48.989 caracteres con espacios, bibliografía incluida. El rango pedido es de 47.500 a 49.500; el límite de la revista, 50.000.
- Resumen de 95 palabras; abstract de 93.
- La nota de autor puede ocupar unos 650 caracteres (unas 95 palabras) sin salir del rango.
- Las 147 citas de la novela se comprobaron automáticamente contra la transcripción: existen literalmente y están en la página indicada. Los datos parafraseados se revisaron a mano.
- Las citas de los cinco libros se cotejaron con sus originales.
- **Faltan:**
  - leer y hacer propio el texto;
  - elegir si la investigación está «en desarrollo» o «concluida» (marcador al final de la sección 1);
  - los datos de autoría;
  - ajustar la declaración de IA;
  - decidir si las figuras son los esquemas o las fotografías de los pasteles;
  - cotejar las citas con el impreso.

  Véase `analisis/04_verificaciones_y_pendientes.md`.

## Análisis y protocolo

| Archivo | Contenido |
|---|---|
| `analisis/01_convocatoria_estudios_bolivianos_43.md` | Convocatoria: ejes (el principal es «discurso, poder y representaciones sociales»), normas, riesgos y correo de envío |
| `analisis/02_codigo_genetico_carcamo_pino.md` | El «código genético» de Cárcamo Pino: conceptos, métodos, estilo y recetario de emulación |
| `analisis/03_marco_cruzado.md` | Lundberg, Martin, Vázquez Ramos *et al.* y la novela (primera ronda) |
| `analisis/04_verificaciones_y_pendientes.md` | Qué hacer y verificar antes de enviar |
| `analisis/05_guia_de_dibujo.md` | Guía de la exploración gráfica en tres escenas (versión 3) |
| `analisis/05b_guia_seis_pasteles.md` | **Guía de los seis pasteles** del artículo definitivo: composición, paleta, técnica y registro de cada pieza |
| `analisis/06_fichero_de_pasajes.md` | Las 147 citas de la novela ordenadas por página (para cotejar con el impreso), erratas de la transcripción, cautelas de lectura y tropos del narrador |
| `analisis/07_cinco_libros.md` | Análisis de Scott, Dean, Frampton, Garrington y Le Guin: pasajes con página, función y límite de cada uno, y dónde entra cada uno en el artículo definitivo |
| `analisis/esquemas/fig1…fig6` | Esquemas de encaje de los seis pasteles (fuente de `articulo/figuras/`; la numeración de los archivos es la de la serie) |
| `analisis/esquemas/escena1…escena3` | Inventarios de las tres escenas de la versión 3 |
| `analisis/referencias_visuales/` | Las cuatro imágenes de referencia de la primera ronda. **No son las figuras del artículo** |

## Regenerar el Word y las figuras

```bash
pip install pypandoc_binary python-docx pillow
python3 articulo/generar_docx.py                                # artículo definitivo
python3 articulo/generar_docx.py articulo/articulo_altiplano.md  # versión 3
python3 articulo/generar_figuras.py                             # necesita Chromium (variable CHROME)
```
