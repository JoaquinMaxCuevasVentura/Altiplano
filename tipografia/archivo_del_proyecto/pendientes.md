# Pendientes, ausencias y dudas

Lo que falta en el archivo y por qué, lo que se registra sin copiarlo y lo que solo tú puedes confirmar. Cada fila tiene su número en `inventario.csv`. [Volver al índice](README.md).

## Lo que no se archiva por decisión o por las reglas del proyecto

| Id | Qué | Por qué no está aquí |
|---|---|---|
| `N-001` | La foto del pie de la lámina | De ella salen los testigos de simulacion/testigos/. «La foto no se sube al repositorio: solo letras sueltas» (extraer_testigos.py; 07_posnansky.md, §3). |
| `N-004` | video_ui/ | No se suben, como el video. La conversación vio 8 de estas imágenes; tampoco se copian. |
| `N-005` | 83b7a8a6-Check_out_the_full_projects_on_my_page..mp4 | No se sube: «se cita, no se sube». Se tomó el método, no la interfaz. |
| `N-006` | Las imágenes del atlas | Veinticuatro imágenes de dominio público. «imagenes/ sigue fuera del repositorio (06, §6.4)». No están en este contenedor; se rehacen con taxonomia/descargar_imagenes.py. |
| `N-008` | El reel del repujado y su video | La referencia para la simulación del repujado. No está en este contenedor y no se sube: «se cita, no se sube». |
| `N-011` | Cinco imágenes de referencia editorial (primera tanda) | El guion, un cuadernillo de HEAD Genève, las páginas de los noventa, el catálogo de cine y el libro coreano, según el encargo editorial. No están en este contenedor y no se suben (06, §6.4). |
| `N-012` | Cinco imágenes de referencia editorial (segunda tanda) | El libro con forma de guion, «PAST (in)tense / future (im)PERFECT», el catálogo de un festival de cine, un libro coreano sobre la vida en Japón y una doble página de «EUROPE ©2020» de Dora Lazarevic. No se suben (06, §6.4: las referencias se citan). La conversación las vio el 19.10 y guarda copias reducidas; tampoco se copian. |
| `N-016` | «Contenedor»: posible antecedente, de otra conversación | Se presenta como «Tipografía · prototipo 0.100 · 144 caracteres · 5 ejes» a partir de Contener una ruina. Es anterior a esta conversación, que empieza el 29.09: no se archiva hasta que confirmes si es parte del proyecto. |
| `N-017` | «Vasijas»: posible antecedente, de otra conversación | Se presenta como «Contener una ruina · tipografía · segundo intento» (seis páginas: agua, cadena, espalda, placa, ruina). Anterior a esta conversación: no se archiva hasta que lo confirmes. |

## Lo que no está o no se pudo recuperar

| Id | Qué | Qué pasó |
|---|---|---|
| `N-002` | Las versiones 1 a 3 del artefacto «Gramática de Contenida» | No se pudieron leer: se archivan la versión 4 (del registro de la conversación), la 5 y la 6 (la vigente). |
| `N-007` | La primera versión del artefacto «El repujado de Contenida» | El resumen de la conversación la nombra «v2»: la anterior no se pudo leer. |
| `N-009` | El armado intermedio del libro (.cache/) | libro.html, el texto del informe en JSON y las vistas de las páginas. Se rehace con armar.py: «Todo lo que se arma va a .cache/, que no entra en el repositorio» (README del libro). |
| `N-010` | Las dependencias de Node del libro (node_modules/) | Vivliostyle CLI 11.3.3 y lo que necesita. Se reinstalan con «npm ci» desde package-lock.json, que es vigente. |
| `N-013` | Los estados intermedios hechos con ediciones por guion | Muchos cambios se hicieron con guiones de Python o sed, no escribiendo el archivo entero: de esos queda el resultado (en git), no cada paso. Lo mismo con la edición de editorial/libro.py del 19.10 (su base es anterior a este registro). |
| `N-014` | El entorno de la sesión | Las herramientas con que se armó, se probó y se rehízo todo: no son material del proyecto. |
| `N-015` | Archivos generados e ignorados | Los ignora .gitignore; se rehacen con sus generadores (informe/armar.py, digital/poliza.py). |
| `N-021` | El registro de la conversación del 29.09 al 18.10 | No está en este contenedor. Quedan los commits, los documentos y el resumen con que sigue la conversación (19.10.2026), del que salen los pedidos sin fecha de la línea de tiempo. |
| `N-034` | Los dos zips de entregables (documentos e imágenes) | Se armaron con armar_entregables.sh y se enviaron en la conversación (uno de 32 MB). No están en este contenedor; su contenido sale del repositorio de entonces (commit sin confirmar). |
| `N-035` | Herramientas de trabajo de contenedores anteriores | Se perdieron con sus contenedores. Del encargo queda la página publicada (en versiones/editorial/). |

## Lo que se registra sin copiarlo

- **Los archivos de la raíz del repositorio** (`README.md` y `.gitignore`) cambiaron 15 veces con commits de *Contenida*, pero mezclan los dos proyectos: no se copian. Cada fila dice cómo recuperarlos con `git show`.
- **10 duplicados exactos** de materiales que ya están archivados o vigentes: se anotan con el número del original. `C-025` (captura vista en la conversación: hoja1.png), `C-031` (captura vista en la conversación: hoja3.png), `C-037` (captura vista en la conversación: hoja4.png), `C-048` (captura vista en la conversación: hoja_movil.png), `C-068` (Captura de prueba: figura_informe.png), `C-070` (captura vista en la conversación: hoja_informe.png)….
- **La caché de Python que se subió por error** el 30.09 y se borró en `deb0435`: se anota, no se copia.
- **La lámina enderezada y el pie aparte** (8.11.2026), las dos imágenes en que se volvieron a medir las proporciones: no se suben, como la foto del pie (07, §3). Quedan sus medidas (`esquemas/celda_medida.json` y `razon_medida.json`) y P-11A, la lámina con capturas, que se arma desde ellas con `planos/proporciones_sobre_la_lamina.py` y queda en `planos/privado/`, fuera del repositorio.

## Dudas que solo puedes resolver tú

1. **«Contenedor» y «Vasijas».** Son dos artefactos de claude.ai del 27 y el 28 de septiembre, anteriores a esta conversación. Por su texto parecen el primer y el segundo intento de esta tipografía. ¿Son parte del proyecto? Si lo son, entran como antecedentes.
2. **¿Hay algún entregable aprobado?** Ningún registro lo dice, así que nada figura como «entregable aprobado». Lo vigente es el estado actual de la rama.
3. **¿Se usó el encargo para GPT Astra 6?** Figura como «alternativa» porque no consta.
4. **¿Se borra el duplicado del artefacto del repujado** (`Y3FyvuU5q3hZjo9TW8qKor`)? Sigue publicado, con la celda de 0,84.
5. **¿Cuándo se escribieron los textos de partida** (el poema, el pie de la lámina)? El archivo solo tiene la fecha del commit en que entraron.
6. **¿Mide 0,90 la retícula de la cabeza en el impreso?** La celda sale de la lámina enderezada (8.11.2026); falta medirla con regla.

## Lo que el archivo deduce y conviene revisar

- **El `app.js` de la versión 4 en línea** se toma del commit `1eaf342` porque mide lo mismo (21 438 bytes); no se comparó su contenido.
- **Las fechas de las versiones en línea** salen de su identificador de versión, que es una marca de tiempo: con la versión 5 coincide con la publicación registrada (03:20 UTC del 30.10.2026).
- **Los generadores marcados «deducido»** en el inventario no los nombra el propio generador ni su README.
- **Lo que se retiró en `3f66520`** figura como «estado sin confirmar»: el commit dice que piel, copia y azulejo «quedan en pausa», no que se descarten.
- **Los pedidos sin fecha** de la línea de tiempo se unen a un commit por su tema y su orden.
