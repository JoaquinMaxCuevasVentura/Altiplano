# Figuras del artículo

El artículo definitivo (`../articulo_cosecha_de_piedras.md`) lleva seis figuras. Son los **esquemas de encaje** de los seis pasteles: fijan las coordenadas que da el texto (con su página) y las decisiones del dibujo (punto de vista, escala, operación de cada zona). Se elaboraron con asistencia de IA y así lo dicen el pie de cada figura y la declaración de IA.

La numeración sigue el orden de aparición en el artículo, que no coincide con la de la serie original:

| Figura del artículo | Pastel | Esquema de origen |
|---|---|---|
| `figura_1.png` | Cráneo/nido | `analisis/esquemas/fig1_craneo_nido.svg` |
| `figura_2.png` | Signo Escalonado frente al mapa | `analisis/esquemas/fig2_signo_mapa.svg` |
| `figura_3.png` | Umbral de la apacheta | `analisis/esquemas/fig3_apacheta.svg` |
| `figura_4.png` | El castillete y la caída al plano 450 | `analisis/esquemas/fig6_castillete.svg` |
| `figura_5.png` | Pelvis telúrica / Pachamama sorda | `analisis/esquemas/fig4_pelvis.svg` |
| `figura_6.png` | El centinela de la resistencia | `analisis/esquemas/fig5_centinela.svg` |

Para regenerarlas después de editar un SVG: `python3 articulo/generar_figuras.py`.

El 30 de septiembre de 2026 se corrigió el esquema de la Figura 2. El cerro ya no es una pirámide simétrica: el Signo Escalonado se traza encima y no encaja en la pendiente, como dice el texto.

Para explorar cada pastel con GPT Image 2 hay seis guías sin texto en `analisis/esquemas/guias/`. Los prompts están en `analisis/17_estilo_y_prompts_gpt_image.md`. Esas imágenes no se publican: las figuras finales serán los escaneos de los pasteles.

## Si quieres publicar las fotografías de los pasteles

1. Escanea o fotografía cada pastel con luz rasante suave y sin reflejos (de 2.000 a 3.000 px de lado mayor) y guárdalo aquí con el nombre de su figura, por ejemplo `figura_4.jpg`.
2. En el `.md`, cambia la ruta de la imagen (`figuras/figura_4.png` → `figuras/figura_4.jpg`) y el pie. Modelo: `**Figura 4.** *El castillete y la caída al plano 450*. Pastel al óleo sobre ⟦soporte⟧, ⟦medidas⟧, ⟦año⟧. Fuente: elaboración propia.`
3. Revisa el plano (2) *Operación* y el plano (3) *Contraste* de esa figura: hoy describen el procedimiento del esquema y lo que obliga a decidir frente al texto. Si el pastel terminado hizo otra cosa, escribe lo que hizo. Solo eso puede presentarse como hallazgo: el artículo advierte que las decisiones del esquema «no cuentan como hallazgos».
4. Si ya no queda ningún esquema, reescribe las frases que hablan de ellos: en la sección 1 («de los que se reproduce el esquema de encaje, el trazado que fija la composición (figuras 1-6)»), en la 2 («Los esquemas de encaje que aquí se reproducen…») y en las conclusiones («Los esquemas obligan a decidir…»). Quita además de la declaración de IA «, y la codificación vectorial de los esquemas de encaje de las figuras 1 a 6»; la enumeración terminará en «la redacción de borradores». Si solo sustituyes algunas figuras, ajusta los números.
   - Si antes de los pasteles generaste imágenes exploratorias con GPT Image 2, la declaración tiene que decirlo:
     - en b), agrega «y la generación de imágenes exploratorias, previas a los pasteles y no reproducidas»;
     - en a), agrega GPT Image 2 (OpenAI).
   - Mide casi lo mismo que lo que sale (`analisis/17_estilo_y_prompts_gpt_image.md`, §17.7).
5. No vuelvas a correr `generar_figuras.py` sobre un número que ya sea fotografía.
6. Regenera el Word (`python3 articulo/generar_docx.py`) y comprueba que la extensión siga entre 47.500 y 49.500 caracteres. Hoy el margen es de 28 caracteres: lo que añadas tendrás que recortarlo en otra parte.
