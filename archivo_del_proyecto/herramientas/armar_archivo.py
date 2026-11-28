#!/usr/bin/env python3
"""Arma archivo_del_proyecto/: el archivo del desarrollo del artículo «Cosecha de piedras».

Saca de git cada versión anterior de cada archivo y la deja en versiones/<línea>/<versión>/ con su ruta original,
junto a las imágenes que sus páginas piden. Suma lo que quedó de la conversación y no entró en git, registra las
ramas relacionadas y lo que está en línea, y escribe el inventario, las fichas, la línea de tiempo, los pendientes
y la guía. Los originales no se tocan.

Se corre desde la raíz del repositorio, en la rama del artículo:
    python3 archivo_del_proyecto/herramientas/armar_archivo.py [--scratch CARPETA]
La parte de git se rehace en cualquier copia del repositorio que tenga las ramas (git fetch origin). La de la
conversación necesita la carpeta de trabajo de la sesión; sin --scratch, se conservan las copias ya archivadas,
con los datos de conversacion.json. Para comprobar el archivo ya armado: verificar_archivo.py.
"""

import argparse
import csv
import datetime as dt
import functools
import hashlib
import html
import json
import posixpath
import re
import shutil
import subprocess
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote

ARCHIVO = "archivo_del_proyecto"
RAMA = "claude/altiplano-botelho-article-jm2nlr"
UTC = dt.timezone.utc

# Ramas del mismo proyecto que no están unidas a la del artículo. De las dos de Codex se trajo su único archivo.
OTRAS_RAMAS = [
    ("codex/analisis-churata", "757013a",
     "Rama de Codex con el informe sobre Churata. Su archivo se trajo a la rama del artículo el 14 de noviembre (commit 93a80af)."),
    ("codex/auditoria-version-final", "a244367",
     "Rama de Codex con la auditoría de la versión final. Su archivo se trajo a la rama del artículo el 10 de noviembre (commit 0a2c4ba)."),
]
# Ramas relacionadas: trabajos que salen de esta rama y no están unidos. Se registran archivo por archivo, no se copian.
# (rama, último commit, línea de trabajo, qué decir en la ficha)
RELACIONADAS = [
    ("claude/eager-bohr-mx9420", "41afd36", "registros",
     "El artículo tomó de ella dos imágenes ({analisis38})."),
    ("proyecto/la-tierra-que-queda", "d2591eb", "tierra",
     "La hizo GPT en paralelo al artículo y tiene abierto el pull request en borrador n.º 1. La auditoría está en {analisis41}."),
]
# Notas para archivos de las ramas relacionadas, cuando un registro del proyecto dice algo de ellos.
NOTAS_RELACIONADAS = [
    (r"^proyectos/la-tierra-que-queda/Serie_seleccionada/El_claro_de_la_piedra\.png$",
     "Render directo de Blender: conserva sus metadatos (analisis/41, §5)."),
    (r"^proyectos/la-tierra-que-queda/Serie_seleccionada/.+\.png$",
     "Sin metadatos de Blender. Según analisis/41 (F3 y F10), todo indica que es una versión tratada con GPT Image o un recorte ampliado de una: solo exploración (regla 6 de AGENTS.md)."),
    (r"^proyectos/la-tierra-que-queda/guiones_recuperados/(altiplano-serie-selection/lamina|anteproyecto/nudos)\.py$",
     "Corre con lo que hay en la rama, cambiando su ruta de salida (analisis/41, §5)."),
    (r"^proyectos/la-tierra-que-queda/guiones_recuperados/.+\.py$",
     "No corre: depende del .blend o de archivos de la sesión de GPT que se perdieron (analisis/41, F1)."),
]

LINEAS = {   # el orden es el del índice
    "articulo": ("El artículo", "El texto fuente del artículo, sus Word, el Word con los cambios marcados, la plantilla de estilos y el generador.", "articulo/"),
    "figuras": ("Las figuras y las imágenes del artículo", "Las ocho figuras, las imágenes de dominio público de la serie aparte, su guía y el generador de los PNG.", "articulo/figuras/"),
    "esquemas": ("Los esquemas, las notaciones y las guías", "Los esquemas de encaje, las notaciones SVG de las figuras, las guías y máscaras para explorar los pasteles, y las cuatro referencias visuales de la primera ronda.", "analisis/esquemas/"),
    "analisis": ("El registro de análisis", "Los documentos numerados de analisis/: cada etapa del proyecto, con su fecha.", "analisis/"),
    "entregables": ("Los entregables", "El artículo en Word y PDF y los documentos que lo acompañan, con su generador.", "entregables/"),
    "taxonomia": ("La taxonomía visual", "Las 51 imágenes de dominio público, su catálogo y los tableros.", "taxonomia/"),
    "convocatorias": ("El informe de convocatorias", "El informe de convocatorias abiertas y las notas de la búsqueda.", "reports/"),
    "chhaxwa": ("Chhaxwa. Cinco pruebas de construcción", "El proyecto paralelo que reemplaza a La tierra que queda: las cinco pruebas, la exploración formal, los modelos de Blender y sus renders.", "chhaxwa/"),
    "repositorio": ("El índice y las reglas del repositorio", "README.md y AGENTS.md.", ""),
    "comprobaciones": ("Las comprobaciones de la conversación", "Guiones, listas de citas y vistas de página con que se comprobó el artículo. Nunca entraron en git.", None),
    "tierra": ("La tierra que queda (rama de GPT, sin unir)", "Tres estudios de arquitectura que GPT hizo en paralelo a partir del artículo, con lo que pudo recuperar de ellos.", None),
    "registros": ("Los registros de arquitectura (rama relacionada, sin unir)", "El catálogo de láminas de arquitectura del altiplano, hecho en otra conversación sobre una rama que sale de esta.", None),
}

ESTADOS = ("versión anterior", "alternativa", "prueba o experimento", "versión vigente", "entregable aprobado",
           "material descartado", "estado sin confirmar")

# Estado de lo que un commit introdujo y otro retiró, cuando el registro lo dice. Clave: el commit que lo introdujo.
DESCARTES = {
    "28707a8": ("material descartado",
                "«Revierte 28707a8 a pedido del autor: el artículo vuelve a la versión con la casa como cuerpo de Pallasmaa» (mensaje del commit 7f00348)."),
}
# Estado de las rutas que un commit retiró sin reemplazarlas en el mismo lugar. Clave: (commit que retira, patrón de la ruta).
RETIROS = [
    ("b557ff6", r"/(vendor/|fuentes/(Caveat|OFL-Caveat))", "material descartado",
     "«Generador nuevo sin rough.js, con la letra Nothing You Could Do (OFL)» (mensaje del commit b557ff6)."),
    ("8996cfb", r"^articulo/figuras/figura_\d_", "versión anterior",
     "Las cuatro imágenes de la primera ronda pasaron a analisis/referencias_visuales/ (commit 8996cfb). «El usuario aclaró que estas imágenes eran solo referencias» (analisis/03)."),
    ("8996cfb", r"piedras_puestas_en_el_agua", "versión anterior",
     "Primer borrador, con su primer título. Lo reemplazó la reescritura del commit 8996cfb, que cambia el nombre del archivo."),
    ("b4af793", r"articulo_cosecha_de_piedras\.", "versión anterior",
     "«Sustituye «La cosecha de piedras» por «Topografías de la carne y el barro en Altiplano»» (mensaje del commit b4af793). El título volvió en el commit b3edfd9."),
    ("0767d19", r"_revisado\.", "versión anterior",
     "«Adopta la versión revisada como artículo definitivo» (asunto del commit 0767d19): el contenido pasó a articulo_cosecha_de_piedras."),
]

GENERADORES = [   # (patrón de la ruta, generador)
    (r"^articulo/articulo_.+_cambios\.docx$", "comparación en LibreOffice de dos Word del artículo (no hay guion en el repositorio)"),
    (r"^articulo/articulo_.+\.docx$", "articulo/generar_docx.py, desde el .md del mismo nombre"),
    (r"^articulo/plantilla_estudios_bolivianos\.docx$", "articulo/generar_docx.py --plantilla"),
    (r"^articulo/figuras/figura_\d\.png$", "articulo/generar_figuras.py, desde analisis/esquemas/"),
    (r"^analisis/esquemas/diagramas/.+\.svg$", "analisis/esquemas/diagramas/generar_diagramas.js"),
    (r"^analisis/esquemas/guias/.+\.(svg|png)$", "analisis/esquemas/guias/generar_guias.py"),
    (r"^entregables/01_.+\.docx$", "entregables/generar_entregables.py: copia de articulo/articulo_cosecha_de_piedras.docx"),
    (r"^entregables/01_.+\.pdf$", "entregables/generar_entregables.py (LibreOffice, desde el Word)"),
    (r"^entregables/.+\.docx$", "entregables/generar_entregables.py, desde el .md del mismo nombre"),
    (r"^taxonomia/(tablero_.+|catalogo\.md)$", "taxonomia/generar_tableros.py, desde catalogo.json"),
    (r"^registros_de_arquitectura/(hoja_.+|catalogo\.md)$", "registros_de_arquitectura/generar_hojas.py, desde catalogo.json"),
    (r"^chhaxwa/renders/render_forma_", "chhaxwa/blender/renderizar.py (Blender 5.0.1)"),
    (r"^chhaxwa/renders/render_prototipo_", "chhaxwa/blender/prototipo_pirca_paisaje.py (Blender 5.0.1)"),
    (r"^chhaxwa/renders/piezas/", "chhaxwa/blender/piezas.py (Blender 5.0.1) y aligerar_piezas.py"),
    (r"^chhaxwa/renders/diagramas/", "chhaxwa/blender/diagramas.py (Blender 5.0.1) y aligerar_piezas.py"),
    (r"^chhaxwa/detalles/(detalle_E\d\.(dxf|png)|laminas_de_detalle\.pdf)$", "chhaxwa/detalles/dibujar_detalles.py (ezdxf, shapely y matplotlib)"),
    (r"^chhaxwa/documento/chhaxwa\.pdf$", "chhaxwa/documento/compilar.py (Typst), desde chhaxwa.typ"),
]

COLUMNAS = ["id", "nombre", "descripcion", "categoria", "linea", "version_o_etapa", "estado", "formato", "copia",
            "ruta_original", "ruta_archivada", "rama", "commit", "fecha", "que_representa_la_fecha", "en_versiones",
            "relacion", "fuente_o_generador", "sha256", "bytes", "blob_git", "observaciones"]

QUE_FECHA = {
    "git": "fecha del commit (UTC) en que este contenido entra en git; no es la fecha de creación de la obra ni, necesariamente, la del archivo",
    "scratch": "última modificación del archivo en la carpeta de trabajo de la sesión (UTC)",
    "registro": "fecha que da el registro del proyecto para ese material",
}

# ------------------------------------------------------------------------------------------------ la conversación
# Lo que quedó en la carpeta de trabajo de la sesión y no entró en git. Rutas relativas a esa carpeta.
CONVERSACION = [
    dict(linea="articulo", nombre="borrador-por-partes-de-la-version-final", estado="versión anterior",
         titulo="Borrador por partes de la versión final",
         que="El borrador de la reescritura del 2 de noviembre, en cuatro partes, antes de unirlas en el artículo. El archivo unido (articulo_final.md) es idéntico al artículo del commit 3eb412c y no se copia.",
         respaldo="`analisis/33_version_final_sin_patrones_de_ia.md` cuenta la reescritura. Que estas cuatro partes sean su borrador se deduce de su fecha y de su contenido.",
         archivos=["final_md/parte1.md", "final_md/parte2.md", "final_md/parte3.md", "final_md/parte4.md",
                   "final_md/articulo_final.md", "final_md/anterior.docx", "final_md/nuevo.docx", "final_md/cambios.docx",
                   "v_3eb412c.md", "v_6f9bed8.md"]),
    dict(linea="articulo", nombre="word-con-los-cambios-del-10-de-noviembre", estado="alternativa",
         titulo="Word con los cambios del 10 de noviembre",
         que="Un Word con solo los cambios de la mañana del 10 de noviembre marcados (251), comparado con el artículo del commit 0a2c4ba. Se le envió al autor en la conversación. Es otra comparación que la del Word de cambios del repositorio, que parte del commit 6f9bed8.",
         respaldo="`analisis/36_tipos_de_cita_y_correcciones.md` describe los cambios que marca. El envío consta en la conversación (10 de noviembre, 09:26 UTC).",
         archivos=["cambios/cambios_del_10_de_noviembre.docx", "cambios/v6f9.docx", "cambios/v0a2.docx", "cambios/head_cambios.docx"]),
    dict(linea="articulo", nombre="articulo-antes-de-las-cursivas", estado="versión anterior",
         titulo="El artículo antes de las cursivas",
         que="El texto del artículo guardado justo antes de pasar a cursiva las voces aymaras, entre los commits f784ab3 y 7b44456.",
         respaldo="`analisis/37_cursivas_pasteles_y_reescrituras.md`, apartado 1. Que sea el estado previo se deduce de su nombre y de su fecha.",
         archivos=["lista/antes_cursivas.md"]),
    dict(linea="articulo", nombre="word-con-los-cambios-de-cursivas-pasteles-y-codex", estado="alternativa",
         titulo="Word con los cambios de cursivas, pasteles y Codex",
         que="Un Word con los cambios de la tarde del 10 de noviembre marcados (74), comparado con el artículo del commit f784ab3. Se le envió al autor en la conversación.",
         respaldo="`analisis/37_cursivas_pasteles_y_reescrituras.md`. El envío consta en la conversación (10 de noviembre, 09:59 UTC).",
         archivos=["cambios/cambios_cursivas_pasteles_codex.docx", "cambios/vf784.docx"]),
    dict(linea="articulo", nombre="word-con-los-cambios-del-15-de-noviembre", estado="alternativa",
         titulo="Word con los cambios del 15 de noviembre",
         que="Un Word con solo los cambios de la versión casi final marcados (56), comparado con el artículo del commit 3d57d31. Se le envió al autor en la conversación.",
         respaldo="`analisis/40_version_casi_final.md` describe los cambios que marca.",
         archivos=["cambios15/cambios_del_15_de_noviembre.docx", "cambios15/v3d57.docx", "antes_casa.md"]),
    dict(linea="figuras", nombre="paginas-de-origen-de-las-imagenes-1-y-3", estado="prueba o experimento",
         titulo="Páginas de origen de las imágenes 1 y 3",
         que="Las páginas completas de Internet Archive de donde salen la Imagen 1 (d'Orbigny, 1847) y la Imagen 3 (Squier, 1877), sus recortes y dos hojas de contacto con que se eligieron. Son de dominio público.",
         respaldo="`analisis/38_auditoria_del_proyecto.md` dice de qué libro y página sale cada imagen. Los recortes se hicieron con órdenes sueltas en la conversación, sin guion.",
         archivos=["ia/tumba_full.jpg", "ia/tumba_crop.jpg", "ia/dorm_full.jpg", "ia/dorm_crop.jpg", "ia/paginas.jpg", "ia/crops.jpg"]),
    dict(linea="comprobaciones", nombre="guion-para-leer-los-libros-de-churata", estado="prueba o experimento",
         titulo="Guion para leer los libros de Churata",
         que="El guion que separó por secciones los dos libros de Churata que el autor adjuntó. Los libros tienen derechos y no se archivan.",
         respaldo="`analisis/32_churata.md` y `analisis/33_version_final_sin_patrones_de_ia.md`.",
         archivos=["churata_scripts/secciones.py"]),
    dict(linea="comprobaciones", nombre="guiones-y-vistas-de-la-version-final", estado="prueba o experimento",
         titulo="Guiones y vistas de la versión final",
         que="Los guiones que midieron los patrones de redacción y compararon las citas antes y después de la reescritura del 2 de noviembre, las dos listas de citas, el guion que arma el Word de cambios y cuatro vistas de página.",
         respaldo="`analisis/33_version_final_sin_patrones_de_ia.md` nombra el guion `patrones` como «fuera del repositorio».",
         archivos=["final_scripts/patrones.py", "final_scripts/citas.py", "final_scripts/comparar.py",
                   "final_scripts/citas_antes.json", "final_scripts/citas_despues.json",
                   "final_render/a.png", "final_render/b.png", "final_render/c.png", "final_render/d.png"]),
    dict(linea="comprobaciones", nombre="vistas-de-la-lista-de-fuentes", estado="prueba o experimento",
         titulo="Vistas de la lista de fuentes",
         que="Un PDF de prueba de `entregables/07_fuentes_para_cotejar` y sus cuatro páginas en imagen, con el guion que las sacó.",
         respaldo="El commit 1d06a39 añade la lista. Que estas vistas sean su prueba se deduce de su nombre y de su fecha.",
         archivos=["lista/paginas.py", "lista/07_fuentes_para_cotejar.pdf", "lista/p-1.jpg", "lista/p-2.jpg", "lista/p-3.jpg", "lista/p-4.jpg"]),
    dict(linea="comprobaciones", nombre="guiones-del-cotejo-con-las-fuentes", estado="prueba o experimento",
         titulo="Guiones del cotejo con las fuentes",
         que="Los guiones con que se cotejaron las citas con las 25 fuentes el 10 de noviembre, la lista de citas de ese día y las tablas que relacionan cada página del PDF con su número impreso. Las fuentes no se archivan.",
         respaldo="`analisis/35_cotejo_con_las_fuentes.md`.",
         archivos=["lista/pagemap.py", "lista/cotejo.py", "lista/ver.py", "lista/build_map.py", "lista/buscar.py", "lista/citas_hoy.json",
                   "lista/map_04_alexander.json", "lista/map_05_barnadas.json", "lista/map_06_bertonio.json",
                   "lista/map_07_carcamo2025a.json", "lista/map_08_carcamo2025b.json", "lista/map_09_cornejo.json",
                   "lista/map_10_lundberg.json", "lista/map_11_rivera.json", "lista/map_12_scott.json",
                   "lista/map_13_zavaleta.json", "lista/map_17_leguin.json", "lista/map_18_dean.json",
                   "lista/map_19_duviols.json", "lista/map_20_garrington.json", "lista/map_21_ingold.json",
                   "lista/map_23_pallasmaa.json", "lista/map_24_segui.json", "lista/map_25_vazquez.json"]),
    dict(linea="comprobaciones", nombre="guiones-de-los-tipos-de-cita-y-las-correcciones", estado="prueba o experimento",
         titulo="Guiones de los tipos de cita y las correcciones",
         que="El guion que cuenta los tipos de cita, el que relaciona cada cita con su fuente y su página, el que aplicó las correcciones del cotejo, las listas de citas de antes y de después, y el guion que ordena las marcas del Word de cambios.",
         respaldo="`analisis/36_tipos_de_cita_y_correcciones.md`.",
         archivos=["lista/tipos.py", "lista/citas2.py", "lista/editar.py", "lista/antes.json", "lista/despues.json", "lista/orden_rpr.py"]),
    dict(linea="comprobaciones", nombre="guiones-de-las-cursivas-y-las-reescrituras", estado="prueba o experimento",
         titulo="Guiones de las cursivas y las reescrituras",
         que="El guion que puso las cursivas, el que aplicó las reescrituras de Codex y los pasteles hechos, y las listas de citas de antes y de después.",
         respaldo="`analisis/37_cursivas_pasteles_y_reescrituras.md`.",
         archivos=["lista/cursivas.py", "lista/editar2.py", "lista/antes2.json", "lista/despues2.json"]),
    dict(linea="comprobaciones", nombre="guiones-de-la-version-casi-final", estado="prueba o experimento",
         titulo="Guiones de la versión casi final",
         que="El guion que incorporó a Suárez Jordán y a Yampara Blanco, el de la pasada de pulido, las listas de citas de antes y de después y el guion de las citas con los dos autores nuevos.",
         respaldo="`analisis/40_version_casi_final.md`.",
         archivos=["lista/citas3.py", "lista/editar3.py", "lista/editar4.py", "lista/antes5.json", "lista/despues5.json", "lista/despues6.json"]),
    dict(linea="comprobaciones", nombre="vistas-y-listas-de-la-auditoria-del-proyecto", estado="prueba o experimento",
         titulo="Vistas y listas de la auditoría del proyecto",
         que="Las páginas del PDF del artículo en imagen, como se miraron en la auditoría del 14 de noviembre (versión del commit 7b44456), y las listas de citas de antes y de después de sus cambios.",
         respaldo="`analisis/38_auditoria_del_proyecto.md`.",
         archivos=["lista/antes3.json", "lista/despues3.json", "lista/despues4.json"] + [f"aud/pg-{i:02d}.jpg" for i in range(1, 60)]),
]

# Lo que no se archiva o no está. (nombre, descripción, categoría, línea, estado, dónde está, observaciones)
NO_ARCHIVADO = [
    ("Las 25 fuentes del cotejo", "Los libros y artículos que cita el artículo, en PDF, imagen o Word, reunidos por el autor el 10 de noviembre",
     "fuente bibliográfica", "analisis", "", "carpeta privada del Drive del autor (`Altiplano-fuentes`)",
     "No se archivan: tienen derechos de autor y el repositorio es público (regla 2 de AGENTS.md). Qué páginas se usaron de cada una: entregables/07_fuentes_para_cotejar.md y analisis/35."),
    ("Los textos extraídos de las fuentes", "El texto de cada fuente, por página, sacado para cotejar las citas",
     "fuente bibliográfica", "comprobaciones", "", "carpeta de trabajo de la sesión (fuentes_txt/, img/)",
     "No se archivan: son copias de obras con derechos. Se pierden cuando se cierre la sesión. Se rehacen con las fuentes y los guiones del cotejo."),
    ("Los dos libros de Churata", "Textos esenciales y El pez de oro, en Word, adjuntados por el autor el 2 de noviembre",
     "fuente bibliográfica", "analisis", "", "adjuntos de la conversación",
     "No se archivan: tienen derechos de autor. Lo que se usó de ellos está en analisis/32 y analisis/33."),
    ("Las fuentes de la carpeta de los registros de arquitectura", "Los PDF de vivienda, chullpas y Tiwanaku que el autor reunió para los registros; de ellos se leyeron cinco para el artículo el 15 de noviembre",
     "fuente bibliográfica", "analisis", "", "carpeta del Drive del autor (la de los registros de arquitectura)",
     "No se archivan: casi todos tienen derechos de autor. Qué se leyó y qué entró en el artículo: analisis/40."),
    ("Las transcripciones y el OCR de septiembre y octubre", "Las transcripciones con que se comprobaron las citas por primera vez",
     "fuente bibliográfica", "analisis", "", "",
     "No recuperable: «nunca entraron al repositorio y […] se perdieron cuando se reinició el entorno de trabajo» (entregables/07). Las citas se cotejaron otra vez el 10 de noviembre."),
    ("El registro de la conversación", "El registro de la sesión donde se hizo el proyecto, desde el 18 de octubre",
     "documentación", "repositorio", "", "contenedor de la sesión",
     "No se archiva: contiene datos privados del autor, el enlace de su carpeta y fragmentos de obras con derechos. La parte anterior al 18 de octubre solo quedó resumida. Lo que importa de ella está en analisis/ y en los mensajes de los commits."),
    ("El artículo de RAEL sobre el estilo de escritura de GPT", "Alonso Simón et al., en la Revista Electrónica de Lingüística Aplicada, 23(1): el PDF que se leyó al investigar los patrones de redacción",
     "fuente bibliográfica", "analisis", "", "carpeta de trabajo de la sesión (ia_estilo_rael/)",
     "No se archiva: es una obra de terceros, de acceso abierto y en línea. analisis/33 da su referencia y dice qué se tomó de esa lectura."),
    ("El texto de Squier en Internet Archive", "El texto completo de Peru: Incidents of Travel and Exploration in the Land of the Incas (1877)",
     "fuente bibliográfica", "figuras", "", "https://archive.org/details/gri_peruincident00squi",
     "No se archiva: es de dominio público y está en línea. Se leyeron las pp. 255-256 (analisis/38)."),
    ("Los pasteles del autor", "Los seis pasteles al óleo de las figuras 1 a 6 y sus escaneos",
     "obra", "figuras", "", "",
     "Todavía no existen en el repositorio. El texto los describe como hechos desde el 10 de noviembre y sus pies dicen «[medidas, año]» (analisis/37). El artículo no se envía antes de cambiar las figuras."),
    ("Las imágenes de exploración hechas con generadores de IA", "Las pruebas de estilo hechas con GPT Image a partir de los prompts de analisis/17, 20 y 22",
     "prueba", "esquemas", "estado sin confirmar", "",
     "No están en el repositorio ni en la conversación que se conserva. «Las imágenes de GPT Image 2 son solo exploración» (analisis/04); no se publican (regla 6 de AGENTS.md). No consta si el autor las guarda."),
    ("Las cinco referencias de estilo del 30 de septiembre", "Arco sobre el agua, portada en la niebla, monolito nocturno y dos losas perforadas",
     "recurso: referencia de estilo", "esquemas", "estado sin confirmar", "",
     "analisis/17 las describe como «las cinco que enviaste hoy». No están en el repositorio; las cuatro de la primera ronda sí (analisis/referencias_visuales/)."),
    ("Las fotos del librillo de Virtue y las letras completas", "Las fotos del librillo japonés con que se cotejó «Pyramid of Bones»",
     "fuente bibliográfica", "analisis", "", "",
     "No se archivan: «Las fotos no se suben al repositorio y las letras no se copian completas» (analisis/27)."),
    ("Lo que se perdió de La tierra que queda", "El archivo de Blender de la revisión final (seis escenas), sus siete renders y dos comparaciones, el dossier de cinco páginas en Typst, la lámina A3 en PDF y el ZIP para Windows",
     "resultado exportado", "tierra", "", "",
     "Quedaron en el espacio de trabajo de la conversación con GPT, al que el autor no tiene acceso (analisis/41, F1 y F2). Si el enlace de descarga de esa conversación todavía funciona, el ZIP va a la carpeta privada de Drive."),
    ("Las cinco maquetas que nombran los guiones de GPT", "Las maquetas que los guiones de La tierra que queda atribuyen al autor como base del estudio 02",
     "recurso: referencia visual", "tierra", "estado sin confirmar", "",
     "Según analisis/42 (§1), todo indica que son las cinco maquetas de studio_cifuentes_ethz que el autor le pasó a GPT como inspiración, y no obra suya."),
    ("Las capturas de studio_cifuentes_ethz", "Diecisiete capturas de la publicación «HS26 – Atlas Works – 50% Stone and 50% Earth», que inspiraron el proyecto paralelo",
     "recurso: referencia visual", "tierra", "", "adjuntos de esta conversación (27 de noviembre)",
     "No se archivan: son obra de terceros. analisis/42 dice qué se tomó de ellas."),
    ("El PDF de Obra gruesa, de Smiljan Radić", "El extracto del libro (Ediciones Puro Chile, 2017) del que salen los precedentes del proyecto paralelo",
     "fuente bibliográfica", "tierra", "", "conversación con GPT y adjuntos de esta conversación (27 de noviembre)",
     "No se archiva: tiene todos los derechos reservados. analisis/42 cita sus páginas."),
    ("Las cinco referencias de la exploración formal", "Dos maquetas de studio_cifuentes_ethz, una pirámide truncada sobre caballetes, un granito partido y forrado de madera y un cono sobre palos",
     "recurso: referencia visual", "chhaxwa", "", "adjuntos de esta conversación (27 de noviembre)",
     "No se archivan: son obra de terceros. chhaxwa/exploracion_formal.md las describe y dice qué se tomó de cada una."),
    ("El primer intento de láminas en SVG", "Seis láminas A3 con axonometrías de proceso trazadas en SVG con un guion propio",
     "prueba", "chhaxwa", "material descartado", "carpeta de trabajo de la sesión (laminas_svg/)",
     "Se dejó cuando el autor pidió modelar en Blender: los dibujos tenían errores de orden de las caras (analisis/43). Las axonometrías de proceso saldrán de los modelos de Blender."),
    ("La A de piedra y tierra", "Una exploración de Chhaxwa: dos muros de piedra amontonada con tierra apisonada entre ellos, sobre una base de pirca",
     "prueba", "chhaxwa", "material descartado", "carpeta de trabajo de la sesión (rapidas/)",
     "Se modeló y el autor la descartó; la reemplaza la torre de champa (analisis/43, §12). Solo hubo renders rápidos."),
    ("Las referencias de las exploraciones E3 y E5", "Una torre de tablas sobre dos apoyos de piedra (R8) y un bloque en talud con una ranura y una bóveda (R16), y la imagen de una cúpula de tierra que mandó el autor, de la que sale la casa redonda (E3)",
     "recurso: referencia visual", "chhaxwa", "", "adjuntos de esta conversación (27 de noviembre)",
     "No se archivan: son obra de terceros o de origen sin confirmar. chhaxwa/exploracion_formal.md y exploraciones.md las describen."),
    ("Blender como módulo de Python", "bpy 5.0.1, instalado en un entorno virtual de la sesión",
     "herramienta: generador o guion", "chhaxwa", "", "carpeta de trabajo de la sesión (venv_bpy/)",
     "No se archiva: se instala con pip install bpy==5.0.1 (chhaxwa/LEEME.md)."),
    ("Los identificadores de los archivos de Drive", "La lista de los 25 archivos con su identificador en Drive",
     "datos", "comprobaciones", "", "carpeta de trabajo de la sesión (lista/ids.txt)",
     "No se archiva: el enlace de la carpeta del autor no entra en el repositorio."),
]

# Lo que está en línea y no se copia. Los datos son los de analisis/29.
EN_LINEA = [(n, i, b) for n, i, b in [
    ("altiplano (matriz)", "5846731", "3 bloques y los 10 canales"), ("altiplano · la novela y su autor", "5846732", "6 bloques"),
    ("altiplano · piedra", "5846733", "5 bloques"), ("altiplano · papel", "5846734", "3 bloques"),
    ("altiplano · máquina", "5846735", "4 bloques"), ("altiplano · cuerpo y memoria", "5846736", "3 bloques"),
    ("altiplano · dibujo", "5846737", "4 bloques"), ("altiplano · crítica", "5846738", "4 bloques"),
    ("altiplano · vecinas", "5846739", "4 bloques"), ("altiplano · cruces", "5846740", "2 bloques"),
    ("altiplano · pasteles", "5846741", "vacío: espera los escaneos del autor")]]


# ------------------------------------------------------------------------------------------------ git
def git(*args, binario=False, comprobar=True):
    r = subprocess.run(["git", "-c", "core.quotepath=false", *args], capture_output=True, check=comprobar)
    return r.stdout if binario else r.stdout.decode("utf8")


@functools.lru_cache(None)
def arbol(commit):
    d = {}
    for ent in git("ls-tree", "-r", "-z", commit, binario=True).decode("utf8").split("\0"):
        if ent:
            meta, ruta = ent.split("\t", 1)
            _, tipo, blob = meta.split()
            if tipo == "blob":
                d[ruta] = blob
    return d


@functools.lru_cache(None)
def contenido(blob):
    return git("cat-file", "blob", blob, binario=True)


def cambios(commit):
    partes = git("diff-tree", "-r", "-z", "--no-commit-id", "-M", "--root", commit, binario=True).decode("utf8").split("\0")
    res, i = [], 0
    while i < len(partes):
        meta = partes[i]
        i += 1
        if not meta.startswith(":"):
            continue
        _, _, ba, bb, est = meta[1:].split(" ")
        if est[0] in "RC":
            viejo, nuevo = partes[i], partes[i + 1]
            i += 2
        else:
            viejo = nuevo = partes[i]
            i += 1
        res.append({"est": est[0], "viejo": viejo, "nuevo": nuevo, "ba": ba, "bb": bb})
    return res


def lista_commits(rango):
    salida = git("log", "--reverse", "--format=%H%x1f%aI%x1f%s%x1f%b%x1e", rango)
    lista = []
    for reg in salida.split("\x1e"):
        reg = reg.strip("\n")
        if not reg:
            continue
        h, fecha, asunto, cuerpo = reg.split("\x1f")
        cuerpo = "\n".join(l for l in cuerpo.strip().splitlines()
                           if not l.startswith(("Co-Authored-By:", "Claude-Session:", "https://claude.ai/"))).strip()
        lista.append({"h": h, "c": h[:7], "fecha": dt.datetime.fromisoformat(fecha).astimezone(UTC),
                      "asunto": asunto, "cuerpo": sin_correos(cuerpo)})
    return lista


# ------------------------------------------------------------------------------------------------ utilidades
def sha256(b):
    return hashlib.sha256(b).hexdigest()


def blob_git(b):
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def sin_correos(t):
    return re.sub(r"\s*<?[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}>?", "", t)


def slug(t, largo=32):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    out = ""
    for p in re.findall(r"[a-z0-9]+", t):
        if len(out) + len(p) + 1 > largo:
            break
        out = f"{out}-{p}" if out else p
    return out


def fecha_txt(f):
    return f.strftime("%Y-%m-%d %H:%M") + " UTC"


def enlace(texto, destino):
    return f"[{texto}]({quote(destino, safe='/#.-_~')})"


def linea_de(ruta):
    if ruta.startswith(ARCHIVO + "/"):
        return None
    if ruta.startswith("articulo/figuras/") or ruta == "articulo/generar_figuras.py":
        return "figuras"
    if ruta.startswith("articulo/"):
        return "articulo"
    if ruta.startswith(("analisis/esquemas/", "analisis/referencias_visuales/")):
        return "esquemas"
    if ruta.startswith("analisis/"):
        return "analisis"
    if ruta.startswith("entregables/"):
        return "entregables"
    if ruta.startswith("taxonomia/"):
        return "taxonomia"
    if ruta.startswith(("reports/", "research_notes/")):
        return "convocatorias"
    if ruta.startswith("registros_de_arquitectura/"):
        return "registros"
    if ruta.startswith("proyectos/la-tierra-que-queda/"):
        return "tierra"
    if ruta.startswith("chhaxwa/"):
        return "chhaxwa"
    return "repositorio"


def formato(ruta):
    ext = posixpath.splitext(ruta)[1].lower().lstrip(".")
    return ext.upper() if ext else "—"


def generador(ruta):
    for patron, gen in GENERADORES:
        if re.search(patron, ruta):
            return gen
    if ruta.endswith(".md"):
        return "redactado (sin generador)"
    return ""


def categoria(ruta):
    n, ext, base = ruta.lower(), posixpath.splitext(ruta.lower())[1], posixpath.basename(ruta.lower())
    if ext in (".ttf", ".otf", ".woff2"):
        return "recurso: fuente tipográfica"
    if base.startswith(("ofl-", "license")):
        return "recurso: licencia"
    if "/vendor/" in n:
        return "recurso: biblioteca de terceros"
    if base == "plantilla_estudios_bolivianos.docx":
        return "recurso: plantilla de estilos"
    if n.startswith("analisis/referencias_visuales/") or re.match(r"articulo/figuras/figura_\d_", n):
        return "recurso: referencia visual"
    if re.match(r"(articulo/figuras/imagen_|taxonomia/imagenes/|registros_de_arquitectura/imagenes/)", n):
        return "recurso: imagen de terceros"
    if ext in (".py", ".js"):
        return "herramienta: generador o guion"
    if ext == ".json":
        return "datos"
    if ext == ".md":
        if re.match(r"articulo/articulo_", n) or (n.startswith("entregables/") and base != "leeme.md"):
            return "fuente editable"
        if generador(ruta).startswith(("taxonomia/", "registros_")):
            return "resultado exportado"
        return "documentación"
    if ext == ".svg":
        return "fuente editable" if not generador(ruta) else "resultado exportado"
    if ext in (".docx", ".pdf", ".png", ".jpg", ".jpeg"):
        return "resultado exportado"
    return "otro"


def descripcion(ruta, datos):
    base, ext = posixpath.basename(ruta), posixpath.splitext(ruta)[1].lower()
    t = None
    if ext in (".md", ".py", ".js", ".svg"):
        try:
            texto = datos.decode("utf8")
        except UnicodeDecodeError:
            texto = ""
        if ext == ".md":
            m = re.search(r"^#\s+(.+)$", texto, re.M)
            t = m and m.group(1)
        elif ext == ".py":
            m = re.search(r'^(?:#.*\n|\s*\n)*[rRuUbB]*("""|\'\'\')\s*(.+?)\s*(?:\n|\1)', texto)
            t = m and m.group(2)
        elif ext == ".js":
            m = re.search(r"/\*+\s*(.+?)\s*(?:\n|\*/)", texto) or re.search(r"^//\s*(.+)$", texto, re.M)
            t = m and m.group(1)
        elif ext == ".svg":
            m = re.search(r"<title>(.*?)</title>", texto, re.S)
            t = m and html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
    if not t:
        reglas = [
            (r"^articulo/articulo_.+_cambios\.docx$", "El artículo en Word, con los cambios marcados"),
            (r"^articulo/articulo_.+\.docx$", "El artículo en Word"),
            (r"^articulo/plantilla_", "La plantilla de estilos del Word"),
            (r"^articulo/figuras/figura_(\d)\.png$", "Figura {0} del artículo"),
            (r"^articulo/figuras/imagen_(\d)\.jpg$", "Imagen {0} de la serie de dominio público"),
            (r"^articulo/figuras/figura_\d_|^analisis/referencias_visuales/", "Referencia visual de la primera ronda"),
            (r"^analisis/esquemas/guias/mascara", "Máscara para explorar una figura con un generador de imágenes"),
            (r"^analisis/esquemas/guias/", "Guía de composición para explorar una figura"),
            (r"^analisis/esquemas/diagramas/fuentes/|/vendor/", "Recurso del generador de diagramas"),
            (r"^analisis/esquemas/", "Esquema o notación de una figura"),
            (r"^entregables/01_.+\.pdf$", "El artículo en PDF"),
            (r"^entregables/01_.+\.docx$", "El artículo en Word (copia del de articulo/)"),
            (r"^entregables/.+\.docx$", "Entregable en Word"),
            (r"^taxonomia/imagenes/", "Imagen de la taxonomía visual"),
            (r"^taxonomia/tablero_", "Tablero de la taxonomía visual"),
            (r"^registros_de_arquitectura/imagenes/", "Lámina de los registros de arquitectura"),
            (r"^proyectos/la-tierra-que-queda/Serie_seleccionada/", "Imagen de la serie de La tierra que queda"),
            (r"^proyectos/la-tierra-que-queda/guiones_recuperados/", "Guion recuperado de La tierra que queda"),
            (r"^proyectos/la-tierra-que-queda/comprobaciones/", "Comprobación de la geometría de la chujlla de La tierra que queda"),
            (r"^registros_de_arquitectura/hoja_", "Hoja de contacto de los registros de arquitectura"),
            (r"^chhaxwa/renders/render_forma_E(\d)\w*\.jpg$", "Render de la exploración E{0} de Chhaxwa (no es una foto)"),
            (r"^chhaxwa/renders/render_forma_(\w+)\.jpg$", "Render de la maqueta de forma {0} de Chhaxwa (no es una foto)"),
            (r"^chhaxwa/renders/diagramas/diagrama_x(\d)\.png$", "Corte en diagrama de la exploración E{0} de Chhaxwa"),
            (r"^chhaxwa/renders/diagramas/diagrama_serie\.png$", "Las seis exploraciones de Chhaxwa a la misma escala, en diagrama"),
            (r"^chhaxwa/detalles/detalle_E(\d)\.dxf$", "Lámina de detalle de la exploración E{0} de Chhaxwa, en DXF"),
            (r"^chhaxwa/detalles/detalle_E(\d)\.png$", "Vista en grises de la lámina de detalle de la exploración E{0} de Chhaxwa"),
            (r"^chhaxwa/detalles/laminas_de_detalle\.pdf$", "Las seis láminas de detalle de Chhaxwa, en A3"),
            (r"^chhaxwa/renders/render_prototipo_", "Render de prueba de Chhaxwa: una pirca en el altiplano (no es una foto)"),
        ]
        for patron, texto in reglas:
            m = re.search(patron, ruta)
            if m:
                t = texto.format(*m.groups()) if m.groups() else texto
                break
    t = re.sub(r"\s+", " ", sin_correos(t or base)).strip()
    return t[:170]


DESCRIPCIONES_CONVERSACION = [
    (r"final_md/parte(\d)\.md$", "Borrador de la versión final del 2 de noviembre, parte {0} de 4"),
    (r"final_md/articulo_final\.md$|^v_3eb412c\.md$", "El artículo del 2 de noviembre, copia de trabajo"),
    (r"^v_6f9bed8\.md$", "El artículo anterior a la versión final, copia de trabajo"),
    (r"antes_cursivas\.md$", "El artículo del 10 de noviembre, antes de las cursivas"),
    (r"cambios_del_10_de_noviembre\.docx$", "Word con los cambios del 10 de noviembre marcados, respecto del commit 0a2c4ba"),
    (r"cambios_cursivas_pasteles_codex\.docx$", "Word con los cambios de cursivas, pasteles y Codex marcados, respecto del commit f784ab3"),
    (r"cambios_del_15_de_noviembre\.docx$", "Word con los cambios del 15 de noviembre marcados, respecto del commit 3d57d31"),
    (r"\.docx$", "Word del artículo, copia de trabajo para comparar"),
    (r"aud/pg-(\d+)\.jpg$", "Vista de la página {0} del PDF del artículo, en la auditoría"),
    (r"final_render/", "Vista de página de la versión final, para revisarla"),
    (r"lista/p-(\d)\.jpg$", "Vista de la página {0} de la lista de fuentes"),
    (r"07_fuentes_para_cotejar\.pdf$", "PDF de prueba de la lista de fuentes"),
    (r"map_\d+_(\w+)\.json$", "Tabla de páginas de la fuente «{0}»: página del archivo y número impreso"),
    (r"(citas\w*|antes\d?|despues\d?)\.json$", "Lista de las citas del artículo, con su fuente y su página"),
    (r"final_scripts/comparar\.py$", "Arma con LibreOffice un Word con los cambios marcados entre dos Word"),
    (r"lista/paginas\.py$", "Reúne las páginas que el artículo cita de cada obra, para la lista de fuentes"),
    (r"lista/pagemap\.py$", "Busca en cada página de una fuente su número impreso"),
    (r"lista/build_map\.py$", "Arma la tabla que relaciona cada página del archivo con su número impreso"),
    (r"lista/ver\.py$", "Muestra una frase en la página de una fuente, para leerla en su contexto"),
    (r"lista/buscar\.py$", "Busca una frase en el texto de una fuente y dice en qué página está"),
    (r"lista/editar\.py$", "Aplica al artículo las correcciones del cotejo y las variaciones de los tipos de cita"),
    (r"lista/editar3\.py$", "Incorpora al artículo a Suárez Jordán (1990) y a Yampara Blanco (2019)"),
    (r"lista/editar4\.py$", "Aplica al artículo la pasada de pulido de la versión casi final"),
    (r"^antes_casa\.md$", "El artículo antes de la versión casi final, copia de trabajo"),
    (r"lista/editar2\.py$", "Aplica al artículo las reescrituras de Codex y la escritura con los pasteles hechos"),
    (r"lista/orden_rpr\.py$", "Ordena las marcas de cambio del Word para que pase la validación"),
    (r"ia/tumba_full\.jpg$", "Página completa del atlas de d'Orbigny (1847) en Internet Archive"),
    (r"ia/tumba_crop\.jpg$", "Recorte de la lámina de d'Orbigny, antes de reducirlo para la Imagen 1"),
    (r"ia/dorm_full\.jpg$", "Página 256 completa de Squier (1877) en Internet Archive"),
    (r"ia/dorm_crop\.jpg$", "Recorte del grabado de Squier para la Imagen 3"),
    (r"ia/(paginas|crops)\.jpg$", "Hoja de contacto para elegir las imágenes 1 y 3"),
]


def descripcion_conversacion(rel, datos):
    for patron, texto in DESCRIPCIONES_CONVERSACION:
        m = re.search(patron, rel)
        if m:
            return texto.format(*m.groups())
    return descripcion(rel, datos or b"")


IMAGEN_MD = re.compile(r"""!\[[^\]]*\]\(\s*(?:<([^>]+)>|([^)\s]+))|<img[^>]+src\s*=\s*["']([^"']+)["']""")
REF_SVG = re.compile(r"""(?:\bsrc|\bhref|xlink:href)\s*=\s*["']([^"']+)["']|url\(\s*["']?([^"')]+)["']?\s*\)""")


def referencias(ruta, datos):
    """Las imágenes y los recursos que una página pide con una ruta relativa."""
    ext = posixpath.splitext(ruta)[1].lower()
    if ext not in (".md", ".svg", ".html"):
        return
    try:
        texto = datos.decode("utf8")
    except UnicodeDecodeError:
        return
    vistos = set()
    for m in (IMAGEN_MD if ext == ".md" else REF_SVG).finditer(texto):
        r = next((g for g in m.groups() if g), "").strip()
        if not r or r.startswith(("http:", "https:", "data:", "mailto:", "//", "#", "javascript:")):
            continue
        r = html.unescape(r.split("#")[0].split("?")[0])
        if r and r not in vistos:
            vistos.add(r)
            yield r


# ------------------------------------------------------------------------------------------------ el archivo
class Archivo:
    def __init__(self, raiz, scratch):
        self.raiz, self.destino, self.scratch = raiz, raiz / ARCHIVO, scratch
        self.filas, self.versiones = [], []
        self.cuenta = defaultdict(int)
        self.archivados = {}        # (ruta, blob) -> fila con copia
        self.por_blob = {}          # blob -> fila con copia (para los duplicados)
        self.pesos = defaultdict(int)

    # -- filas y copias
    def fila(self, prefijo, **k):
        self.cuenta[prefijo] += 1
        f = {c: "" for c in COLUMNAS}
        f["id"] = f"{prefijo}-{self.cuenta[prefijo]:04d}"
        f.update({c: ("" if v is None else v) for c, v in k.items()})
        self.filas.append(f)
        return f

    def copiar(self, datos, rel, clase):
        p = self.destino / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(datos)
        self.pesos[clase] += len(datos)
        return f"{ARCHIVO}/{rel}"

    # -- git
    def desde_git(self):
        todos = lista_commits("HEAD")
        self.cambios = {c["h"]: cambios(c["h"]) for c in todos}
        self.commits = [c for c in todos if any(linea_de(x["nuevo"]) for x in self.cambios[c["h"]])]
        for c in self.commits:
            c["rama"] = RAMA
        self.cabeza = self.commits[-1]
        self.VIG = {r: b for r, b in arbol(self.cabeza["h"]).items() if linea_de(r)}
        self.vig_por_blob = {}
        for r, b in sorted(self.VIG.items()):
            self.vig_por_blob.setdefault(b, r)
        # en qué commits está cada (ruta, contenido)
        self.presencia = defaultdict(list)
        for c in self.commits:
            for r, b in arbol(c["h"]).items():
                if linea_de(r):
                    self.presencia[(r, b)].append(c["c"])
        # las ramas de Codex entran en la misma línea de tiempo
        extra = []
        for rama, punta, nota in OTRAS_RAMAS:
            if subprocess.run(["git", "cat-file", "-e", punta], capture_output=True).returncode:
                sys.exit(f"Falta el commit {punta} de la rama {rama}: git fetch origin {rama}")
            for c in lista_commits(f"HEAD..{punta}"):
                c["rama"], c["nota_rama"] = rama, nota
                self.cambios[c["h"]] = cambios(c["h"])
                extra.append(c)
        self.fila_vigente = {}
        orden = sorted(self.commits + extra, key=lambda c: (c["fecha"], c["rama"] != RAMA))
        self.todos = orden
        retiro = {}                # ruta -> commit que la retiró por última vez
        for c in self.commits:
            for x in self.cambios[c["h"]]:
                if x["est"] in "DR":
                    retiro[x["viejo"]] = c["c"]
        self.retiro = retiro
        for c in orden:
            por_linea = defaultdict(list)
            for x in self.cambios[c["h"]]:
                for l in {linea_de(x["nuevo"]), linea_de(x["viejo"])} - {None}:
                    por_linea[l].append(x)
            for l in sorted(por_linea, key=list(LINEAS).index):
                self.version_git(l, c, por_linea[l])
        self.vigentes_en_su_lugar()

    def estado_historico(self, ruta, c):
        if c["c"] in DESCARTES:
            return DESCARTES[c["c"]]
        if ruta not in self.VIG and ruta in self.retiro:
            for commit, patron, estado, nota in RETIROS:
                if commit == self.retiro[ruta] and re.search(patron, ruta):
                    return estado, nota
            return "estado sin confirmar", f"La ruta se retiró en el commit {self.retiro[ruta]} y su mensaje no dice por qué."
        return "versión anterior", "La reemplazó un commit posterior."

    def version_git(self, l, c, xs):
        carpeta = f"{c['fecha']:%Y-%m-%d_%H%M}_{c['c']}_{slug(c['asunto'])}"
        rel = f"versiones/{l}/{carpeta}"
        v = dict(linea=l, origen="git", c=c, carpeta=carpeta, rel=rel, fecha=c["fecha"], titulo=c["asunto"],
                 aqui=[], vigentes=[], repetidos=[], duplicados=[], deps=[], rotos=[],
                 anadidos=[], modificados=[], retirados=[], renombrados=[])
        principal = c["rama"] == RAMA
        for x in sorted(xs, key=lambda x: x["nuevo"]):
            ruta = x["nuevo"]
            if x["est"] == "D":
                v["retirados"].append(x["viejo"])
                continue
            if x["est"] == "R":
                v["renombrados"].append((x["viejo"], ruta))
                if linea_de(ruta) != l:        # salió de esta línea hacia otra
                    continue
                if linea_de(x["viejo"]) != l:
                    v["anadidos"].append(ruta)
            elif x["est"] == "A":
                v["anadidos"].append(ruta)
            else:
                v["modificados"].append(ruta)
            blob = x["bb"]
            if self.VIG.get(ruta) == blob:                      # sigue vigente en su lugar
                v["vigentes"].append(ruta)
                if not principal:
                    f = self.fila("R", nombre=posixpath.basename(ruta), descripcion=descripcion(ruta, contenido(blob)),
                                  categoria=categoria(ruta), linea=l, version_o_etapa=carpeta, estado="versión vigente",
                                  formato=formato(ruta), copia="no se copia: duplicado exacto del vigente",
                                  ruta_original=ruta, ruta_archivada=ruta, rama=c["rama"], commit=c["c"],
                                  fecha=fecha_txt(c["fecha"]), que_representa_la_fecha=QUE_FECHA["git"],
                                  fuente_o_generador=generador(ruta), sha256=sha256(contenido(blob)),
                                  bytes=len(contenido(blob)), blob_git=blob,
                                  observaciones=f"Aquí apareció por primera vez este contenido. {c['nota_rama']}")
                    v["duplicados"].append(f)
                continue
            if (ruta, blob) in self.archivados:                 # mismo contenido en la misma ruta: ya está
                v["repetidos"].append((ruta, self.archivados[(ruta, blob)]))
                continue
            datos = contenido(blob)
            estado, nota = self.estado_historico(ruta, c)
            comun = dict(nombre=posixpath.basename(ruta), descripcion=descripcion(ruta, datos), categoria=categoria(ruta),
                         linea=l, version_o_etapa=carpeta, estado=estado, formato=formato(ruta), ruta_original=ruta,
                         rama=c["rama"], commit=c["c"], fecha=fecha_txt(c["fecha"]), que_representa_la_fecha=QUE_FECHA["git"],
                         en_versiones=" ".join(self.presencia.get((ruta, blob), [])), fuente_o_generador=generador(ruta),
                         sha256=sha256(datos), bytes=len(datos), blob_git=blob)
            gemelo = self.por_blob.get(blob)
            if gemelo or blob in self.vig_por_blob:             # mismo contenido en otra ruta: no se copia otra vez
                donde = gemelo["ruta_archivada"] if gemelo else self.vig_por_blob[blob]
                quien = gemelo["id"] if gemelo else f"el vigente {self.vig_por_blob[blob]}"
                f = self.fila("H", **comun, copia=f"no se copia: duplicado exacto de {quien}", ruta_archivada=donde,
                              relacion=f"mismo contenido que {quien}", observaciones=nota)
                v["duplicados"].append(f)
                self.archivados[(ruta, blob)] = f
                continue
            f = self.fila("H", **comun, copia="copia exacta desde git",
                          ruta_archivada=self.copiar(datos, f"{rel}/{ruta}", "git"), observaciones=nota)
            self.archivados[(ruta, blob)] = f
            self.por_blob[blob] = f
            v["aqui"].append(f)
        # las imágenes y los recursos que piden las páginas copiadas
        presentes = {f["ruta_original"] for f in v["aqui"]}
        for f in list(v["aqui"]):
            for r in referencias(f["ruta_original"], contenido(f["blob_git"])):
                dep = posixpath.normpath(posixpath.join(posixpath.dirname(f["ruta_original"]), r))
                blob = arbol(c["h"]).get(dep)
                if dep.startswith("..") or not blob:
                    v["rotos"].append((f["ruta_original"], r))
                    continue
                if dep in presentes:
                    continue
                presentes.add(dep)
                datos = contenido(blob)
                d = self.fila("D", nombre=posixpath.basename(dep), descripcion=descripcion(dep, datos),
                              categoria=categoria(dep), linea=l, version_o_etapa=carpeta, formato=formato(dep),
                              copia="copia funcional: lo pide una página de esta carpeta", ruta_original=dep,
                              ruta_archivada=self.copiar(datos, f"{rel}/{dep}", "dependencias"), rama=c["rama"], commit=c["c"],
                              fecha=fecha_txt(c["fecha"]), que_representa_la_fecha="fecha del commit (UTC) de la versión que lo pide",
                              relacion=f"lo pide {f['id']} ({f['ruta_original']})", fuente_o_generador=generador(dep),
                              sha256=sha256(datos), bytes=len(datos), blob_git=blob,
                              observaciones="Es el archivo tal como estaba en ese commit. Su propia historia está en su línea.")
                v["deps"].append(d)
        # la línea completa en ese commit
        if principal:
            en_linea = [(r, b) for r, b in arbol(c["h"]).items() if linea_de(r) == l]
            v["total"] = len(en_linea)
            v["total_vigentes"] = sum(1 for r, b in en_linea if self.VIG.get(r) == b)
            v["total_aqui"] = sum(1 for r, b in en_linea if any(f["ruta_original"] == r and f["blob_git"] == b for f in v["aqui"]))
        self.versiones.append(v)

    def vigentes_en_su_lugar(self):
        primera = {}
        for c in self.commits:
            for x in self.cambios[c["h"]]:
                if x["est"] != "D":
                    primera.setdefault((x["nuevo"], x["bb"]), c)
        for ruta, blob in sorted(self.VIG.items()):
            datos = (self.raiz / ruta).read_bytes()
            c = primera[(ruta, blob)]
            estado, obs = "versión vigente", "Estado actual de la rama. No consta una aprobación como entregable."
            if blob_git(datos) != blob:
                obs = "ATENCIÓN: el archivo de la carpeta de trabajo no coincide con el de la rama."
            if ruta.startswith("articulo/articulo_altiplano."):
                estado, obs = "alternativa", "«La versión 3 […] Es una alternativa sin figuras y no se actualiza» (README.md). Sigue en su lugar."
            if ruta.startswith("analisis/referencias_visuales/"):
                obs = "«El usuario aclaró que estas imágenes eran solo referencias» (analisis/03). No son figuras del artículo."
            f = self.fila("V", nombre=posixpath.basename(ruta), descripcion=descripcion(ruta, datos), categoria=categoria(ruta),
                          linea=linea_de(ruta), version_o_etapa=f"vigente ({self.cabeza['c']})", estado=estado,
                          formato=formato(ruta), copia="en su lugar (no se copia)", ruta_original=ruta, ruta_archivada=ruta,
                          rama=RAMA, commit=c["c"], fecha=fecha_txt(c["fecha"]), que_representa_la_fecha=QUE_FECHA["git"],
                          en_versiones=" ".join(self.presencia[(ruta, blob)]), fuente_o_generador=generador(ruta),
                          sha256=sha256(datos), bytes=len(datos), blob_git=blob, observaciones=obs)
            self.fila_vigente[ruta] = f
        for f in self.filas:        # las filas de otras ramas apuntan a su vigente
            if f["id"].startswith("R-") and f["ruta_original"] in self.fila_vigente:
                v = self.fila_vigente[f["ruta_original"]]
                f["relacion"] = f"mismo contenido que {v['id']}"
                v["relacion"] = f"apareció antes en la rama {f['rama']} ({f['commit']}, {f['fecha']})"

    # -- las ramas relacionadas
    def ramas_relacionadas(self):
        for rama, punta, linea, nota in RELACIONADAS:
            self.rama_relacionada(rama, punta, linea, nota)

    def rama_relacionada(self, rama, punta, linea, nota):
        if subprocess.run(["git", "cat-file", "-e", punta], capture_output=True).returncode:
            sys.exit(f"Falta el commit {punta} de la rama {rama}: git fetch origin {rama}")
        base = git("merge-base", "HEAD", punta).strip()
        for c in lista_commits(f"{base}..{punta}"):
            carpeta = f"{c['fecha']:%Y-%m-%d_%H%M}_{c['c']}_{slug(c['asunto'])}"
            c["rama"], c["base"], c["nota_relacionada"] = rama, base[:7], nota
            v = dict(linea=linea, origen="relacionada", c=c, carpeta=carpeta, rel=f"versiones/{linea}/{carpeta}",
                     fecha=c["fecha"], titulo=c["asunto"], aqui=[], vigentes=[], repetidos=[], duplicados=[], deps=[],
                     rotos=[], anadidos=[], modificados=[], retirados=[], renombrados=[], en_rama=[])
            for x in sorted(cambios(c["h"]), key=lambda x: x["nuevo"]):
                if x["est"] == "D":
                    v["retirados"].append(x["viejo"])
                    continue
                (v["anadidos"] if x["est"] == "A" else v["modificados"]).append(x["nuevo"])
                datos = contenido(x["bb"])
                es_ultima = arbol(punta).get(x["nuevo"]) == x["bb"]
                f = self.fila("R", nombre=posixpath.basename(x["nuevo"]), descripcion=descripcion(x["nuevo"], datos),
                              categoria=categoria(x["nuevo"]), linea=linea, version_o_etapa=carpeta,
                              estado="estado sin confirmar", formato=formato(x["nuevo"]),
                              copia="en su rama (no se copia)", ruta_original=x["nuevo"], ruta_archivada="",
                              rama=rama, commit=c["c"], fecha=fecha_txt(c["fecha"]), que_representa_la_fecha=QUE_FECHA["git"],
                              fuente_o_generador=generador(x["nuevo"]), sha256=sha256(datos), bytes=len(datos), blob_git=x["bb"],
                              observaciones=("Es el estado más reciente de su rama. " if es_ultima else "Lo reemplazó un commit posterior de su rama. ")
                              + f"La rama no está unida a la del artículo y no consta una decisión de unirla. Se recupera con: git show {c['c']}:\"{x['nuevo']}\""
                              + next((" " + t for patron, t in NOTAS_RELACIONADAS if re.search(patron, x["nuevo"])), ""))
                v["en_rama"].append(f)
            self.versiones.append(v)

    # -- la conversación
    def desde_conversacion(self, previos):
        manifiesto_ruta = self.destino / "herramientas" / "conversacion.json"
        manifiesto = json.loads(manifiesto_ruta.read_text("utf8")) if manifiesto_ruta.exists() else {}
        nuevo = {}
        for g in CONVERSACION:
            piezas = []
            for rel in g["archivos"]:
                if self.scratch and (self.scratch / rel).exists():
                    p = self.scratch / rel
                    datos = p.read_bytes()
                    fecha = dt.datetime.fromtimestamp(p.stat().st_mtime, UTC).strftime("%Y-%m-%d %H:%M")
                elif rel in manifiesto:
                    fecha, datos = manifiesto[rel]["fecha"], previos.get(rel)
                    if datos is None:           # un duplicado que no se copió: su contenido está en git
                        datos = contenido(manifiesto[rel]["blob_git"])
                else:
                    continue
                previo = manifiesto.get(rel, {}) if not (self.scratch and (self.scratch / rel).exists()) else {}
                nuevo[rel] = {"fecha": previo.get("fecha", fecha), "sha256": previo.get("sha256") or sha256(datos),
                              "bytes": previo.get("bytes") or len(datos), "blob_git": previo.get("blob_git") or blob_git(datos)}
                piezas.append((rel, fecha, datos))
            if not piezas:
                continue
            primera = min(f for _, f, _ in piezas)
            fecha = dt.datetime.strptime(primera, "%Y-%m-%d %H:%M").replace(tzinfo=UTC)
            carpeta = f"{fecha:%Y-%m-%d_%H%M}_conversacion_{g['nombre']}"
            v = dict(linea=g["linea"], origen="conversacion", carpeta=carpeta, rel=f"versiones/{g['linea']}/{carpeta}",
                     fecha=fecha, titulo=g["titulo"], g=g, aqui=[], duplicados=[], vigentes=[], repetidos=[], deps=[], rotos=[],
                     anadidos=[], modificados=[], retirados=[], renombrados=[])
            for rel, f_txt, datos in piezas:
                m = nuevo[rel]
                comun = dict(nombre=posixpath.basename(rel), descripcion=descripcion_conversacion(rel, datos),
                             categoria="prueba o comprobación" if g["linea"] == "comprobaciones" and not rel.endswith(".py")
                             else categoria(rel), linea=g["linea"], version_o_etapa=carpeta, formato=formato(rel),
                             ruta_original=f"<carpeta de trabajo de la sesión>/{rel}", rama="", commit="",
                             fecha=f_txt + " UTC", que_representa_la_fecha=QUE_FECHA["scratch"],
                             sha256=m["sha256"], bytes=m["bytes"], blob_git=m["blob_git"])
                gemelo = self.por_blob.get(m["blob_git"])
                if gemelo or m["blob_git"] in self.vig_por_blob:
                    quien = gemelo["id"] if gemelo else self.fila_vigente[self.vig_por_blob[m["blob_git"]]]["id"]
                    donde = gemelo["ruta_archivada"] if gemelo else self.vig_por_blob[m["blob_git"]]
                    f = self.fila("C", **comun, estado="", copia=f"no se copia: duplicado exacto de {quien}",
                                  ruta_archivada=donde, relacion=f"mismo contenido que {quien}",
                                  observaciones="Copia de trabajo de un archivo que ya está en git.")
                    v["duplicados"].append(f)
                    continue
                f = self.fila("C", **comun, estado=g["estado"], copia="copia exacta desde la carpeta de trabajo de la sesión",
                              ruta_archivada=self.copiar(datos, f"{v['rel']}/{rel}", "conversacion"),
                              observaciones="No entró en git como estaba.")
                v["aqui"].append(f)
            self.versiones.append(v)
        if nuevo:
            manifiesto_ruta.write_text(json.dumps(nuevo, ensure_ascii=False, indent=1, sort_keys=True) + "\n", "utf8")

    def lo_demas(self):
        for nombre, ident, bloques in EN_LINEA:
            self.fila("L", nombre=nombre, descripcion=f"Canal privado del atlas de Are.na ({bloques})", categoria="atlas en línea",
                      linea="entregables", version_o_etapa="2026-10-10 y 2026-10-11", estado="estado sin confirmar", formato="canal de Are.na",
                      copia="en línea (no se copia)", ruta_original=f"Are.na, canal {ident}", fecha="2026-10-11",
                      que_representa_la_fecha=QUE_FECHA["registro"], relacion="lo describen analisis/29_atlas_arena.md y entregables/06_atlas_de_arena.md",
                      observaciones="Los datos son los de analisis/29. Al armar el archivo no se volvió a abrir el canal: su estado actual no está comprobado.")
        for nombre, desc, cat, linea, estado, donde, obs in NO_ARCHIVADO:
            self.fila("N", nombre=nombre, descripcion=desc, categoria=cat, linea=linea, estado=estado,
                      copia="no se archiva" if donde else "ausente", ruta_original=donde, observaciones=obs)

    # -- estados de las versiones y vecinos
    def ordenar(self):
        self.versiones.sort(key=lambda v: (list(LINEAS).index(v["linea"]), v["fecha"], v["origen"] != "git"))
        por_linea = defaultdict(list)
        for v in self.versiones:
            por_linea[v["linea"]].append(v)
        for l, vs in por_linea.items():
            ultima_git = [v for v in vs if v["origen"] == "git" and v["c"]["rama"] == RAMA]
            for i, v in enumerate(vs):
                v["anterior"] = vs[i - 1] if i else None
                v["siguiente"] = vs[i + 1] if i + 1 < len(vs) else None
                if v["origen"] == "conversacion":
                    v["estado"] = v["g"]["estado"]
                elif v["origen"] == "relacionada":
                    v["estado"] = "estado sin confirmar"
                elif v["c"]["rama"] != RAMA:
                    v["estado"] = "versión vigente" if v["vigentes"] and not v["aqui"] else "estado sin confirmar"
                elif ultima_git and v is ultima_git[-1]:
                    v["estado"] = "versión vigente"
                elif v["c"]["c"] in DESCARTES:
                    v["estado"] = DESCARTES[v["c"]["c"]][0]
                else:
                    v["estado"] = "versión anterior"
        self.por_linea = por_linea

    # -- escritura
    def escribir(self):
        self.ordenar()
        for v in self.versiones:
            self.ficha(v)
        for l, vs in self.por_linea.items():
            self.indice_de_linea(l, vs)
        self.indice_de_versiones()
        self.inventario()
        self.linea_de_tiempo()
        self.pendientes()
        self.recursos()
        self.guia()

    def escribir_md(self, rel, lineas):
        p = self.destino / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("\n".join(lineas).rstrip("\n") + "\n", "utf8")

    def vigente_de(self, l):
        destino = LINEAS[l][2]
        return None if destino is None else (destino or "./")

    def ficha(self, v):
        l, arriba = v["linea"], "../../../../"
        L = [f"# {LINEAS[l][0]} · {fecha_txt(v['fecha'])}", "", f"**{v['titulo']}**", "", "| | |", "|---|---|",
             f"| Línea | {enlace(LINEAS[l][0], '../README.md')} |"]
        if v["origen"] == "conversacion":
            L += ["| Origen | la conversación del proyecto; no está en git |",
                  f"| Fecha | {fecha_txt(v['fecha'])}: la del archivo más antiguo de la carpeta de trabajo, no la de creación de lo que contiene |"]
        else:
            L += [f"| Origen | commit `{v['c']['c']}` de la rama `{v['c']['rama']}` |",
                  f"| Fecha | {fecha_txt(v['fecha'])}: la del commit, no la de creación de lo que contiene |"]
        L.append(f"| Estado de la versión | {v['estado']} |")
        if self.vigente_de(l) is not None:
            L.append(f"| Lo vigente | {enlace('`' + (LINEAS[l][2] or 'README.md y AGENTS.md') + '`', arriba + LINEAS[l][2])} |")
        for rotulo, otro in (("La versión anterior", v["anterior"]), ("La versión siguiente", v["siguiente"])):
            if otro:
                L.append(f"| {rotulo} | {enlace(otro['carpeta'], '../' + otro['carpeta'] + '/ficha.md')} |")
        L += ["", "## Qué contiene esta carpeta", ""]
        if v["origen"] == "conversacion":
            L += [v["g"]["que"], ""]
        if v["aqui"]:
            uno = len(v["aqui"]) == 1
            if v["origen"] == "conversacion":
                que = "archivo de la conversación" if uno else "archivos de la conversación"
            else:
                que = "archivo de esta versión que ya no es el vigente" if uno else "archivos de esta versión que ya no son los vigentes"
            L.append(f"- **{len(v['aqui'])} {que},** con su ruta original: " + ", ".join(
                enlace(f"`{f['ruta_original'].split('>/')[-1]}`", f["ruta_archivada"][len(ARCHIVO) + 1 + len(v['rel']) + 1:]) for f in v["aqui"]) + ".")
        if v["deps"]:
            L.append(f"- **{len(v['deps'])} {'copia' if len(v['deps']) == 1 else 'copias'} de imágenes o recursos** que piden esas páginas, tal como estaban en ese commit, para que se vean como entonces.")
        if v["duplicados"]:
            L.append(f"- **{len(v['duplicados'])} que no se {'copia' if len(v['duplicados']) == 1 else 'copian'}** porque su contenido ya está guardado en otra parte: " + "; ".join(
                f"`{f['ruta_original'].split('>/')[-1]}` ({f['relacion']}: " + enlace("ver", arriba + f["ruta_archivada"]) + ")" for f in v["duplicados"]) + ".")
        if v["repetidos"]:
            L.append(f"- **{len(v['repetidos'])} que {'vuelve' if len(v['repetidos']) == 1 else 'vuelven'} a un contenido anterior,** ya archivado: " + "; ".join(
                f"`{r}` (" + enlace(f["id"], arriba + f["ruta_archivada"]) + ")" for r, f in v["repetidos"]) + ".")
        if v["vigentes"] and (v["origen"] != "git" or v["c"]["rama"] == RAMA):
            L.append(f"- **{len(v['vigentes'])} que {'sigue vigente' if len(v['vigentes']) == 1 else 'siguen vigentes'} en su lugar,** sin cambios desde este commit: " + ", ".join(
                enlace(f"`{r}`", arriba + r) for r in v["vigentes"]) + ".")
        if v.get("en_rama"):
            L.append(f"- **Nada copiado.** Los {len(v['en_rama'])} archivos de este commit siguen en su rama y están en `inventario.csv` (columna `version_o_etapa`). "
                     f"Para ver uno: `git show {v['c']['c']}:<ruta>`.")
        if not (v["aqui"] or v["deps"] or v["duplicados"] or v["repetidos"] or v["vigentes"] or v.get("en_rama")):
            L.append("- Solo esta ficha: el commit retiró archivos de la línea y no dejó otros.")
        if v["rotos"]:
            L.append(f"- **{len(v['rotos'])} {'ruta de imagen que no existía' if len(v['rotos']) == 1 else 'rutas de imagen que no existían'} en ese commit** (suelen ser ejemplos dentro del texto): " + ", ".join(f"`{r}` en `{o}`" for o, r in v["rotos"]) + ".")
        if "total" in v:
            otras = v["total"] - v["total_aqui"] - v["total_vigentes"]
            L += ["", "## La versión completa", "",
                  f"En este commit, la línea tenía {v['total']} archivos: {v['total_aqui']} están en esta carpeta, {otras} en carpetas de otras versiones "
                  f"y {v['total_vigentes']} siguen vigentes en su lugar. Para ver cuáles, filtra `inventario.csv` por la columna `en_versiones` con `{v['c']['c']}`. "
                  f"Para tenerla entera: `git worktree add ../altiplano_{v['c']['c']} {v['c']['c']}`."]
        if v["origen"] != "conversacion":
            L += ["", "## Qué cambió respecto de la anterior", ""]
            for rotulo, lista in (("Añadidos", v["anadidos"]), ("Modificados", v["modificados"]), ("Retirados", v["retirados"])):
                if lista:
                    muestra = ", ".join(f"`{r}`" for r in lista[:40]) + (f" y {len(lista) - 40} más" if len(lista) > 40 else "")
                    L.append(f"- **{rotulo} ({len(lista)}):** {muestra}.")
            for viejo, nuevo in v["renombrados"]:
                L.append(f"- **Cambió de lugar o de nombre:** `{viejo}` pasó a `{nuevo}`.")
            idas = v["retirados"] + [viejo for viejo, _ in v["renombrados"]]
            for nota in sorted({n for commit, patron, _, n in RETIROS if commit == v["c"]["c"] and any(re.search(patron, r) for r in idas)}):
                L.append(f"- **Sobre lo retirado:** {nota}")
            notas = sorted({f["observaciones"] for f in v["aqui"] + v["duplicados"] if f["estado"] in ("material descartado", "estado sin confirmar") and f["id"].startswith("H-")})
            for n in notas:
                L.append(f"- **Sobre su estado:** {n}")
        L += ["", "## Lo que lo respalda", ""]
        if v["origen"] == "conversacion":
            L += [v["g"]["respaldo"]]
        else:
            L += [f"El mensaje del commit `{v['c']['c']}`:", "", f"> {v['c']['asunto']}"]
            if v["c"]["cuerpo"]:
                L += [">"] + [f"> {x}".rstrip() for x in v["c"]["cuerpo"].splitlines()]
            registros = sorted({x["nuevo"] for x in self.cambios.get(v["c"]["h"], []) if re.match(r"analisis/\d+\w*_", x["nuevo"]) and x["est"] != "D" and x["nuevo"] in self.VIG})
            if registros:
                L += ["", "El registro del proyecto que ese commit escribió o puso al día: " + ", ".join(enlace(f"`{r}`", arriba + r) for r in registros) + "."]
            if v["c"].get("nota_rama"):
                L += ["", v["c"]["nota_rama"]]
            if v["origen"] == "relacionada":
                L += ["", f"Esta rama sale del commit `{v['c']['base']}` de la rama del artículo y no está unida. " + v["c"]["nota_relacionada"].format(
                      analisis38=enlace("`analisis/38_auditoria_del_proyecto.md`", arriba + "analisis/38_auditoria_del_proyecto.md"),
                      analisis41=enlace("`analisis/41_auditoria_de_la_tierra_que_queda.md`", arriba + "analisis/41_auditoria_de_la_tierra_que_queda.md"))]
        self.escribir_md(f"{v['rel']}/ficha.md", L)

    def origen_txt(self, v):
        if v["origen"] == "conversacion":
            return "conversación"
        return f"`{v['c']['c']}`" + ("" if v["c"]["rama"] == RAMA else f" (rama `{v['c']['rama']}`)")

    def indice_de_linea(self, l, vs):
        L = [f"# {LINEAS[l][0]}", "", LINEAS[l][1], ""]
        if self.vigente_de(l) is not None:
            L += [f"Lo vigente está en su lugar: {enlace('`' + (LINEAS[l][2] or 'la raíz del repositorio') + '`', '../../../' + LINEAS[l][2])}. "
                  "Cada carpeta guarda lo que en esa versión era distinto de lo vigente.", ""]
        L += ["| Fecha (UTC) | Origen | Versión | Estado | Archivos en la carpeta |", "|---|---|---|---|---|"]
        for v in vs:
            L.append(f"| {v['fecha']:%Y-%m-%d %H:%M} | {self.origen_txt(v)} | {enlace(v['titulo'], v['carpeta'] + '/ficha.md')} | {v['estado']} | {len(v['aqui']) + len(v['deps'])} |")
        self.escribir_md(f"versiones/{l}/README.md", L)

    def indice_de_versiones(self):
        L = ["# Las versiones, por línea de trabajo", "",
             "Cada línea reúne los archivos que cambian juntos. Dentro, una carpeta por versión, con su ficha.", "",
             "| Línea | Qué reúne | Versiones |", "|---|---|---|"]
        for l in LINEAS:
            if l in self.por_linea:
                L.append(f"| {enlace(LINEAS[l][0], l + '/README.md')} | {LINEAS[l][1]} | {len(self.por_linea[l])} |")
        self.escribir_md("versiones/README.md", L)

    def inventario(self):
        orden = {p: i for i, p in enumerate("VHDCRLN")}
        self.filas.sort(key=lambda f: (orden[f["id"][0]], f["id"]))
        with open(self.destino / "inventario.csv", "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.DictWriter(fh, COLUMNAS, lineterminator="\n")
            w.writeheader()
            w.writerows(self.filas)

    def linea_de_tiempo(self):
        L = ["# Línea de tiempo", "",
             "Todo lo que tiene fecha, en orden. Las fechas de los commits dicen cuándo entró cada contenido en git, en hora universal (UTC). "
             "No son las fechas de creación de las obras: la novela es de 1945, y los pasteles del autor todavía no tienen fecha en el proyecto.", "",
             "| Fecha (UTC) | Origen | Qué | Líneas que toca |", "|---|---|---|---|"]
        grupos = defaultdict(list)
        for v in self.versiones:
            clave = (v["fecha"], v["c"]["c"] if v["origen"] != "conversacion" else v["carpeta"])
            grupos[clave].append(v)
        for (fecha, _), vs in sorted(grupos.items(), key=lambda kv: kv[0]):
            v = vs[0]
            lineas = ", ".join(enlace(LINEAS[x["linea"]][0], f"versiones/{x['linea']}/{x['carpeta']}/ficha.md") for x in vs)
            L.append(f"| {fecha:%Y-%m-%d %H:%M} | {self.origen_txt(v)} | {v['titulo']} | {lineas} |")
        L += ["", "## Lo que tiene fecha y no es un commit", "",
              "- **10 y 11 de octubre de 2026:** el atlas de Are.na, once canales privados en línea (`analisis/29_atlas_arena.md`).",
              "- **10 de noviembre de 2026:** el autor reúne las 25 fuentes en una carpeta privada de su Drive (`analisis/35_cotejo_con_las_fuentes.md`).",
              "- **18 de octubre de 2026:** desde esta fecha se conserva el registro de la conversación. De lo anterior quedó un resumen."]
        self.escribir_md("linea_de_tiempo.md", L)

    def pendientes(self):
        L = ["# Pendientes del archivo", "",
             "Lo que el proyecto menciona y no está, lo que existe y no se archiva, y las dudas que el registro no resuelve. "
             "Los pendientes del artículo están en `entregables/02_lista_de_envio.md`; aquí van solo los del archivo.", "",
             "## Lo que no se archiva o no está", "", "| N.º | Qué | Dónde está | Por qué |", "|---|---|---|---|"]
        for f in self.filas:
            if f["id"].startswith("N-"):
                L.append(f"| {f['id']} | **{f['nombre']}.** {f['descripcion']} | {f['ruta_original'] or 'No está'} | {f['observaciones']} |")
        L += ["", "## Lo que está en línea y no se copia", "",
              "Los once canales del atlas de Are.na (`L-0001` a `L-0011` del inventario) son privados y están en la cuenta del autor. "
              "El archivo guarda su descripción (`analisis/29_atlas_arena.md` y `entregables/06_atlas_de_arena.md`), no su contenido. "
              "Al armar el archivo no se volvieron a abrir.", "",
              "## Dudas que el registro no resuelve", "",
              "- **Ningún material consta como entregable aprobado.** El autor aprobó correcciones y tomó decisiones que están en `analisis/` "
              "(el título, el epígrafe, las cursivas, escribir con los pasteles hechos), pero no hay un registro donde dé por definitivo un archivo. "
              "Además, `AGENTS.md` dice que reescribirá el artículo con su voz. Por eso lo más reciente figura como «versión vigente».",
              "- **La rama `claude/eager-bohr-mx9420`** (los registros de arquitectura) no está unida. Si se une, su `analisis/34_registros_de_arquitectura.md` "
              "choca en número con el `34` de esta rama. Unirla o no es decisión del autor.",
              "- **La rama `proyecto/la-tierra-que-queda`** (el proyecto paralelo de GPT) no está unida y tiene un *pull request* en borrador. "
              "Qué hacer con ella y con sus imágenes, que según `analisis/41` están tratadas con GPT Image, es decisión del autor.",
              "- **Las ramas de Codex** (`codex/analisis-churata` y `codex/auditoria-version-final`) ya entregaron su único archivo a la rama del artículo. "
              "No consta si el autor quiere conservarlas o borrarlas.",
              "- **La conversación anterior al 18 de octubre** solo quedó resumida. Sus archivos de trabajo (transcripciones, OCR, pruebas) no se pueden recuperar. "
              "Lo que produjo sí está en git, commit por commit.",
              "- **Las fechas de la carpeta de trabajo** son las de la última modificación de cada archivo, y pueden ser posteriores a su primera escritura.",
              "- **Las imágenes de exploración hechas con IA** y las cinco referencias de estilo del 30 de septiembre no están en ningún registro que se conserve. "
              "Si el autor las guarda y quiere archivarlas, hay que decidir antes si pueden estar en un repositorio público."]
        rotos = [(v, o, r) for v in self.versiones for o, r in v["rotos"]]
        if rotos:
            L += ["", "## Rutas de imagen que no existían en su versión", "",
                  "Estas páginas nombran una imagen que no existía en su commit. Casi todas son ejemplos dentro del texto, como `figura_N.jpg`. Se copian tal cual, sin corregir.", ""]
            for v, o, r in rotos:
                L.append(f"- `{o}` pide `{r}` ({enlace(v['carpeta'], 'versiones/' + v['linea'] + '/' + v['carpeta'] + '/ficha.md')}).")
        self.escribir_md("pendientes.md", L)

    def recursos(self):
        L = ["# Recursos compartidos", "",
             "Lo que usan varias versiones o varias líneas. Sigue en su lugar, sin copiar: moverlo rompería los generadores. "
             "Cuando una versión anterior necesita un recurso que cambió, su copia está en la carpeta de esa versión.", "",
             "| Recurso | Dónde está | Quién lo usa |", "|---|---|---|"]
        tabla = [
            ("La plantilla de estilos del Word", "articulo/plantilla_estudios_bolivianos.docx", "`articulo/generar_docx.py` y `entregables/generar_entregables.py`: todos los Word del proyecto"),
            ("El generador del Word del artículo", "articulo/generar_docx.py", "El artículo y, a través suyo, los entregables"),
            ("El generador de los entregables", "entregables/generar_entregables.py", "Los Word y el PDF de `entregables/`"),
            ("El generador de las notaciones", "analisis/esquemas/diagramas/generar_diagramas.js", "Las notaciones SVG de las figuras 1 a 8"),
            ("La letra de las notaciones y su licencia", "analisis/esquemas/diagramas/fuentes/", "`generar_diagramas.js`: los rótulos de las ocho figuras"),
            ("El generador de las figuras", "articulo/generar_figuras.py", "Los PNG de `articulo/figuras/`, que piden el artículo y los entregables"),
            ("El generador de las guías", "analisis/esquemas/guias/generar_guias.py", "Las guías y máscaras de `analisis/esquemas/guias/`"),
            ("Las figuras y las imágenes del artículo", "articulo/figuras/", "El artículo en `.md`, sus Word y el PDF de `entregables/`"),
            ("Las imágenes de la taxonomía", "taxonomia/imagenes/", "Los cuatro tableros y el catálogo; cinco de las imágenes del artículo salieron de aquí (`articulo/figuras/LEEME.md`)"),
            ("El generador de los tableros", "taxonomia/generar_tableros.py", "Los tableros y `taxonomia/catalogo.md`"),
            ("Las cuatro referencias visuales", "analisis/referencias_visuales/", "`analisis/03`, `05`, `05b` y `17`: referencias de estilo, no figuras del artículo"),
        ]
        for nombre, ruta, uso in tabla:
            if (self.raiz / ruta).exists():
                L.append(f"| {nombre} | {enlace('`' + ruta + '`', '../../' + ruta)} | {uso} |")
        L += ["", "Para regenerar los archivos: la sección «Cómo regenerar los archivos» de " + enlace("`AGENTS.md`", "../../AGENTS.md") + ". "
              "Hacen falta `pypandoc_binary`, `python-docx` y `pillow`; LibreOffice para el PDF, y Chromium y Node para las figuras y los tableros."]
        self.escribir_md("recursos_compartidos/README.md", L)

    def guia(self):
        n = lambda p: sum(1 for f in self.filas if f["id"].startswith(p))
        copiadas = lambda p: sum(1 for f in self.filas if f["id"].startswith(p) and f["copia"].startswith("copia"))
        mb = lambda k: f"{self.pesos[k] / 1e6:.0f}".replace(".", ",")
        primero, ultimo = self.commits[0], self.cabeza
        L = ["# Archivo del proyecto «Cosecha de piedras»", "",
             "Este archivo ordena lo que se produjo al desarrollar el artículo «Cosecha de piedras: el *ayllu*, el Estado y la mina. Dibujando *Altiplano* de Raúl Botelho Gosálvez». "
             "Reúne lo que quedó registrado en la rama del artículo, en las ramas relacionadas y en la conversación donde se hizo. "
             "Sirve para ver qué se hizo, cómo cambió y recuperar cualquier versión anterior sin confundirla con la vigente.", "",
             "No es una versión nueva del proyecto ni una selección: guarda también los borradores, las pruebas y lo descartado. Los originales siguen en su lugar, sin cambios.", "",
             "## Qué abarca", "",
             f"- **La rama del artículo,** `{RAMA}`: {len(self.commits)} commits, del {primero['fecha']:%d.%m.%Y} al {ultimo['fecha']:%d.%m.%Y} (de `{primero['c']}` a `{ultimo['c']}`).",
             f"- **De git:** {n('H-')} versiones anteriores de archivos ({copiadas('H-')} copiadas tal cual y {n('H-') - copiadas('H-')} que repiten un contenido ya guardado) y los {n('V-')} archivos vigentes, registrados en su lugar.",
             f"- **De la conversación:** {n('C-')} piezas de la carpeta de trabajo ({copiadas('C-')} copiadas): borradores, dos Word de cambios que se enviaron al autor, guiones de comprobación y vistas de página.",
             f"- **Copias funcionales:** {n('D-')} imágenes copiadas junto a las páginas que las piden, para que se vean como entonces.",
             f"- **Otras ramas:** {n('R-')} registros. Las dos ramas de Codex entregaron su archivo a la rama del artículo. La de los registros de arquitectura (`{RELACIONADAS[0][0]}`) y la de *La tierra que queda* (`{RELACIONADAS[1][0]}`), que hizo GPT, son otros trabajos que salen de esta rama; se registran y no se copian.",
             f"- **En línea:** {n('L-')} canales del atlas de Are.na, descritos y no copiados.",
             f"- **Lo que falta:** {n('N-')} registros de lo que no se archiva o no está, con el motivo. Están en [pendientes.md](pendientes.md).",
             f"- **Peso de lo copiado:** {mb('git')} MB de git, {mb('dependencias')} MB de copias funcionales y {mb('conversacion')} MB de la conversación. "
             "Lo que viene de git no agranda el repositorio, porque git guarda una sola vez cada contenido.",
             "- **Fuera del archivo:** las ramas `claude/fervent-lovelace-exgqzl` y `claude/zen-cannon-kqblsc` son de otro proyecto (la tipografía *Contenida*) y no se tocan.", "",
             "## Cómo está ordenado", "", "```",
             "archivo_del_proyecto/",
             "├── README.md               esta guía",
             "├── inventario.csv          un registro por material, con su procedencia",
             "├── linea_de_tiempo.md      todo lo que tiene fecha, en orden",
             "├── pendientes.md           lo que falta, lo que no se copia y las dudas",
             "├── verificacion.md         lo que se comprobó y cómo",
             "├── versiones/              las versiones, por línea de trabajo",
             "│   └── <línea>/",
             "│       ├── README.md       sus versiones, en orden",
             "│       └── AAAA-MM-DD_HHMM_<origen>_<nombre>/",
             "│           ├── ficha.md    qué es, qué cambió y qué lo respalda",
             "│           └── …           los archivos, con su ruta original desde la raíz",
             "├── recursos_compartidos/   lo que usan varias versiones (sigue en su lugar)",
             "└── herramientas/           el guion que armó el archivo y el que lo verifica",
             "```", "",
             "- [inventario.csv](inventario.csv) · [linea_de_tiempo.md](linea_de_tiempo.md) · [pendientes.md](pendientes.md) · [verificacion.md](verificacion.md) · "
             "[versiones/](versiones/README.md) · [recursos_compartidos/](recursos_compartidos/README.md) · [herramientas/](herramientas/)", "",
             "## Las líneas de trabajo", "", "| Línea | Versiones | Lo vigente, en su lugar |", "|---|---|---|"]
        for l in LINEAS:
            vs = self.por_linea.get(l)
            if not vs:
                continue
            cuenta = defaultdict(int)
            for v in vs:
                cuenta["de git" if v["origen"] == "git" else "de la conversación" if v["origen"] == "conversacion" else "de la rama relacionada"] += 1
            donde = "no está en esta rama" if self.vigente_de(l) is None else enlace("`" + (LINEAS[l][2] or "README.md y AGENTS.md") + "`", "../" + LINEAS[l][2])
            if l == "comprobaciones":
                donde = "no entraron en git"
            L.append(f"| {enlace(LINEAS[l][0], 'versiones/' + l + '/README.md')} | {', '.join(f'{k} {t}' for t, k in cuenta.items())} | {donde} |")
        L += ["", "## Cómo se lee", "", "### Las carpetas de versión", "",
              "Se llaman `AAAA-MM-DD_HHMM_<origen>_<nombre>`: la fecha y la hora (UTC), el origen (el commit o `conversacion`) y unas palabras del commit o de lo que es. "
              "No hay números de versión, porque el proyecto no los usó de forma continua y el archivo no los inventa. "
              "Los documentos hablan de una «versión 3» y de una «versión final»; cuando lo hacen, la ficha cita el documento.", "",
              "Cada carpeta guarda **lo que en esa versión era distinto de lo vigente**: lo que cambió en ese commit y ya no está así. "
              "Lo que no cambió está en una carpeta anterior o sigue vigente en su lugar. La ficha dice cuántos archivos tenía la línea completa, y el inventario dice cuáles (columna `en_versiones`). "
              "Debajo de cada carpeta, los archivos conservan su ruta desde la raíz del repositorio, para que sus enlaces funcionen. "
              "Por eso el artículo en `.md` lleva al lado sus figuras tal como eran en ese commit.", "",
              "### Los estados", "", "Cada material lleva uno, y solo cuando hay un registro que lo sostenga:", "",
              "- **Versión vigente:** el estado actual de la rama. Es lo más reciente, no lo aprobado.",
              "- **Versión anterior:** la reemplazó un commit posterior, o es un estado intermedio que dejó la conversación antes del commit.",
              "- **Alternativa:** otro camino para lo mismo. Son `articulo/articulo_altiplano` (la «versión 3», que el README conserva como alternativa) y los dos Word de cambios que parten de otra versión.",
              "- **Prueba o experimento:** lo que sirvió para comprobar: guiones, listas de citas y vistas de página.",
              "- **Material descartado:** lo que un commit sacó del proyecto y su mensaje lo dice. Son la cita de Potteiger y Purinton, revertida a pedido del autor, y los recursos del primer generador de diagramas.",
              "- **Estado sin confirmar:** lo que el registro no permite clasificar, como la rama sin unir y los canales en línea que no se volvieron a abrir.",
              "- **Entregable aprobado:** ninguno. En los registros no consta que el autor haya dado por definitivo un archivo ([pendientes.md](pendientes.md)).", "",
              "Las fuentes de terceros que no se archivan no llevan estado, porque no son material del proyecto.", "",
              "### Las fechas", "", "Cada fecha dice qué representa, en la columna `que_representa_la_fecha`:", "",
              "- **La de un commit** es cuándo entró ese contenido en git. No es la fecha en que se creó la obra, ni necesariamente la del archivo.",
              "- **La de la conversación** es la última modificación del archivo en la carpeta de trabajo de la sesión.",
              "- **La del registro** es la que da un documento del proyecto, como las del atlas de Are.na.", "",
              "Los pies de las figuras 1 a 6 dicen «[medidas, año]»: los pasteles todavía no tienen fecha en el proyecto, y el archivo no les pone una.", "",
              "### Los números del inventario", "", "| Prefijo | Qué es |", "|---|---|",
              "| `V-` | Archivo vigente, registrado en su lugar. No se copia |",
              "| `H-` | Versión anterior sacada de git. Copia exacta, o referencia a otra copia si el contenido se repite |",
              "| `D-` | Copia funcional: una imagen que pide una página archivada |",
              "| `C-` | Pieza de la conversación que no entró en git como estaba |",
              "| `R-` | Archivo de otra rama. No se copia: se dice cómo recuperarlo |",
              "| `L-` | Material en línea. No se copia |",
              "| `N-` | Lo que no se archiva o no está |", "",
              "### Copias y duplicados", "",
              "Los duplicados se detectan por contenido: el SHA-256 y el identificador de git de cada archivo están en el inventario. "
              "Si un contenido ya está guardado, no se copia otra vez: su fila dice de cuál es duplicado y dónde está. "
              "Pasa con el Word de `entregables/01`, que es copia del de `articulo/`, y con los archivos que solo cambiaron de nombre. "
              "Un duplicado no es lo mismo que otra exportación: dos Word generados del mismo texto en fechas distintas pueden diferir, y entonces se guardan los dos.", "",
              "### Lo documentado y lo deducido", "",
              "Las fichas citan el mensaje del commit y el documento de `analisis/` que respalda cada versión. Eso es lo documentado. "
              "La línea de trabajo de cada archivo, el estado «versión anterior» de lo reemplazado y la relación entre un borrador de la conversación y su commit son deducciones del orden y de las fechas, y las fichas lo dicen. "
              "Las decisiones del autor que constan están en `analisis/`; el archivo no le atribuye otras.", "",
              "## La versión vigente", "",
              f"Es el estado de la rama en el commit `{ultimo['c']}` ({ultimo['fecha']:%d.%m.%Y}): el artículo en " + enlace("`articulo/articulo_cosecha_de_piedras.md`", "../articulo/articulo_cosecha_de_piedras.md")
              + ", sus Word y los archivos de " + enlace("`entregables/`", "../entregables/") + ". Qué es cada cosa: el " + enlace("`README.md`", "../README.md")
              + " de la raíz. Lo que falta para enviar el artículo: " + enlace("`entregables/02_lista_de_envio.md`", "../entregables/02_lista_de_envio.md") + ".", "",
              "## Cómo recuperar una versión", "",
              "- **Un archivo:** ábrelo en su carpeta de `versiones/`, o búscalo en `inventario.csv` por su ruta original.",
              "- **Un archivo, desde git:** `git show <commit>:<ruta>`, con el commit y la ruta del inventario.",
              "- **El proyecto entero como estaba:** `git worktree add ../altiplano_<commit> <commit>`. Cuando termines, `git worktree remove ../altiplano_<commit>`.",
              "- **Volver a una versión:** copia el archivo a su lugar en una rama nueva y propón el cambio. No lo hagas sobre la rama del artículo sin que el autor lo pida.", "",
              "## Verificación", "",
              "[verificacion.md](verificacion.md) dice qué se comprobó: que cada copia coincide con su origen en git, que el inventario ubica todo lo recuperado, que los enlaces funcionan y que los originales no cambiaron. "
              "Se rehace con `python3 archivo_del_proyecto/herramientas/verificar_archivo.py`.", "",
              "El archivo se arma con `python3 archivo_del_proyecto/herramientas/armar_archivo.py`. No se edita a mano: si el proyecto cambia, se corre otra vez."]
        self.escribir_md("README.md", L)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--scratch", type=Path, help="la carpeta de trabajo de la sesión, para lo que no entró en git")
    args = ap.parse_args()
    raiz = Path(git("rev-parse", "--show-toplevel").strip())
    destino = raiz / ARCHIVO
    # lo que ya se archivó de la conversación se conserva si no se da la carpeta de trabajo
    previos = {}
    manifiesto = destino / "herramientas" / "conversacion.json"
    if manifiesto.exists() and not args.scratch:
        for carpeta in destino.glob("versiones/*/*_conversacion_*"):
            for p in carpeta.rglob("*"):
                if p.is_file() and p.name != "ficha.md":
                    previos[p.relative_to(carpeta).as_posix()] = p.read_bytes()
    for nombre in ("versiones", "recursos_compartidos"):
        shutil.rmtree(destino / nombre, ignore_errors=True)
    a = Archivo(raiz, args.scratch)
    a.desde_git()
    a.ramas_relacionadas()
    a.desde_conversacion(previos)
    a.lo_demas()
    a.escribir()
    print(f"{len(a.filas)} registros; {len(a.versiones)} versiones en {len(a.por_linea)} líneas")
    for k in ("V", "H", "D", "C", "R", "L", "N"):
        print(f"  {k}-: {a.cuenta[k]}")
    print("  peso copiado (MB):", {k: round(v / 1e6, 1) for k, v in a.pesos.items()})


if __name__ == "__main__":
    main()
