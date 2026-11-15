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

## Si quieres publicar las fotografías de los pasteles

1. Escanea o fotografía cada pastel con luz rasante suave y sin reflejos (de 2.000 a 3.000 px de lado mayor) y guárdalo aquí con el nombre de su figura, por ejemplo `figura_4.jpg`.
2. En el `.md`, cambia la ruta de la imagen (`figuras/figura_4.png` → `figuras/figura_4.jpg`) y el pie. Modelo: `**Figura 4.** *El castillete y la caída al plano 450*. Pastel al óleo sobre ⟦soporte⟧, ⟦medidas⟧, ⟦año⟧. Fuente: elaboración propia.`
3. Revisa el plano (2) *Operación* y el plano (3) *Hallazgo* de esa figura: hoy describen el procedimiento y lo que muestra el esquema. Si el pastel terminado hizo otra cosa, escribe lo que hizo.
4. Si ya no queda ningún esquema en el artículo, quita de la declaración de IA «la elaboración de los esquemas de encaje reproducidos en las figuras 1 a 6».
5. No vuelvas a correr `generar_figuras.py` sobre un número que ya sea fotografía.
6. Regenera el Word (`python3 articulo/generar_docx.py`) y comprueba que la extensión siga entre 47.500 y 49.500 caracteres.
