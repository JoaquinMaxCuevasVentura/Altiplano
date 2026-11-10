# 34. Registros de arquitectura del altiplano

10 de noviembre de 2026. Es una recopilación de imágenes: el artículo no se cambió.

## El pedido

El autor envió una captura de un dibujo, «Bohío», de F. Leon (1995, tinta sobre Mylar), y pidió:

- analizarla con detalle;
- buscar registros de arquitectura de ese tipo para las culturas del altiplano boliviano, en repositorios de imágenes de uso libre y en libros de Internet Archive;
- incluir ResearchGate y páginas parecidas;
- comentar por qué se elige cada imagen, partiendo de la lectura de la referencia;
- mantener la arquitectura como tema principal.

## Lo que se hizo

1. **La lectura de la referencia.** El dibujo es un alzado de frente de una casa campesina, con el material dibujado pieza por pieza, una escala gráfica y una leyenda con los nombres locales de los materiales. De ahí salieron cinco criterios, llamados caminos: la medida, el material, el tipo común, la leyenda y el objeto solo. Están explicados en `registros_de_arquitectura/LEEME.md`.
2. **La búsqueda.** Se revisaron catorce libros en Internet Archive, hoja por hoja o por su lista de láminas. Entraron láminas de ocho.
3. **La selección.** Quedaron 61 láminas en seis familias. Cada ficha de `registros_de_arquitectura/catalogo.json` lleva la fuente, el enlace a la hoja del escaneo, los derechos, los caminos y el comentario.
4. **Las hojas de contactos.** Una por familia, hechas con `generar_hojas.py`.

## Cómo se comprobó cada dato

- **Los títulos** se leyeron en el pie de cada grabado o en la lista de láminas del libro.
- **Las páginas** de Squier coinciden con su lista de ilustraciones y con las que ya daba la taxonomía visual. Las de Wiener se dedujeron de dos cabeceras leídas en el escaneo (la hoja 470 es la p. 437 y la hoja 474 es la p. 441). La de Middendorf se leyó en la cabecera.
- **Las láminas de Bandelier** se numeraron siguiendo el orden de su lista, que coincide con el contenido de cada hoja.
- **Las láminas de Inwards** no llevan título. Se cotejaron con el texto del autor.

## Dos errores que se corrigieron antes de guardar

El cotejo con el texto de Inwards cambió dos fichas que se habían descrito solo mirando el dibujo:

1. **La lámina X** parecía la restitución de un edificio antiguo. El autor dice que es la casa de un agricultor indígena acomodado, hecha con piedras sacadas de las ruinas. Pasó a la familia de la casa común (n.º 2).
2. **La lámina XVI** parecía un bloque labrado de Tiwanaku. El autor dice que son piezas egipcias, puestas para comparar. Se quitó.

Sirve de aviso para las fichas que no se pudieron cotejar con un texto: describen lo que se ve y nada más.

## Lo que no se encontró

Ninguna fuente de dominio público trae un levantamiento de la casa común del altiplano. Las siete láminas de casas son vistas. Las plantas, los cortes y los alzados se hicieron para tumbas, templos y palacios.

## Lo que falló

- Gallica, HathiTrust, Europeana y el sitio de la Biodiversity Heritage Library dieron el error 403.
- Wikimedia Commons limitó las consultas.
- ResearchGate rechaza las consultas automáticas. Sus trabajos se localizaron con un buscador y van como referencias en el `LEEME.md`, sin copiar figuras.
- El escaneo de Wiener de la Universidad de Carolina del Norte no entregó su texto. Los pies de sus grabados se leyeron con un OCR propio (Tesseract).

## Lo que queda para el autor

Está en la sección «Lo que falta o decides tú» de `registros_de_arquitectura/LEEME.md`. Lo principal:

- confirmar los derechos de las tres láminas de Posnansky de 1914;
- decidir si se queda el lado peruano del lago;
- las fuentes que faltan (Stübel y Uhle, Angrand, Métraux).
