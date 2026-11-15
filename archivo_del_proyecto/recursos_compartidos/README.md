# Recursos compartidos

Lo que usan varias versiones o varias líneas. Sigue en su lugar, sin copiar: moverlo rompería los generadores. Cuando una versión anterior necesita un recurso que cambió, su copia está en la carpeta de esa versión.

| Recurso | Dónde está | Quién lo usa |
|---|---|---|
| La plantilla de estilos del Word | [`articulo/plantilla_estudios_bolivianos.docx`](../../articulo/plantilla_estudios_bolivianos.docx) | `articulo/generar_docx.py` y `entregables/generar_entregables.py`: todos los Word del proyecto |
| El generador del Word del artículo | [`articulo/generar_docx.py`](../../articulo/generar_docx.py) | El artículo y, a través suyo, los entregables |
| El generador de los entregables | [`entregables/generar_entregables.py`](../../entregables/generar_entregables.py) | Los Word y el PDF de `entregables/` |
| El generador de las notaciones | [`analisis/esquemas/diagramas/generar_diagramas.js`](../../analisis/esquemas/diagramas/generar_diagramas.js) | Las notaciones SVG de las figuras 1 a 8 |
| La letra de las notaciones y su licencia | [`analisis/esquemas/diagramas/fuentes/`](../../analisis/esquemas/diagramas/fuentes/) | `generar_diagramas.js`: los rótulos de las ocho figuras |
| El generador de las figuras | [`articulo/generar_figuras.py`](../../articulo/generar_figuras.py) | Los PNG de `articulo/figuras/`, que piden el artículo y los entregables |
| El generador de las guías | [`analisis/esquemas/guias/generar_guias.py`](../../analisis/esquemas/guias/generar_guias.py) | Las guías y máscaras de `analisis/esquemas/guias/` |
| Las figuras y las imágenes del artículo | [`articulo/figuras/`](../../articulo/figuras/) | El artículo en `.md`, sus Word y el PDF de `entregables/` |
| Las imágenes de la taxonomía | [`taxonomia/imagenes/`](../../taxonomia/imagenes/) | Los cuatro tableros y el catálogo; cinco de las imágenes del artículo salieron de aquí (`articulo/figuras/LEEME.md`) |
| El generador de los tableros | [`taxonomia/generar_tableros.py`](../../taxonomia/generar_tableros.py) | Los tableros y `taxonomia/catalogo.md` |
| Las cuatro referencias visuales | [`analisis/referencias_visuales/`](../../analisis/referencias_visuales/) | `analisis/03`, `05`, `05b` y `17`: referencias de estilo, no figuras del artículo |

Para regenerar los archivos: la sección «Cómo regenerar los archivos» de [`AGENTS.md`](../../AGENTS.md). Hacen falta `pypandoc_binary`, `python-docx` y `pillow`; LibreOffice para el PDF, y Chromium y Node para las figuras y los tableros.
