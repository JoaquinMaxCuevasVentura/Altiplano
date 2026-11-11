# Registros de arquitectura del altiplano

95 láminas con dibujos de arquitectura del altiplano boliviano y de la cuenca del lago Titicaca, de 1847 a 2025. Cada una lleva su fuente, su página y un comentario que dice por qué entra.

Se hizo en dos tandas:

- **10 de noviembre de 2026:** 61 láminas de dominio público, tomadas de libros de Internet Archive.
- **11 de noviembre de 2026:** 34 láminas más, sacadas de los 53 PDF y las 12 imágenes que el autor reunió en su Drive a partir de `recursos_por_conseguir.md`. Por decisión suya, esta tanda incluye obras con derechos.

Es solo una recopilación. No toca el artículo ni sus figuras.

> **Aviso sobre los derechos.** Este repositorio es público. Dieciséis láminas vienen de estudios con derechos de autor o con licencias que ponen condiciones, y otras ocho tienen los derechos por confirmar. Están aquí para estudio, cada una con su cita. Ninguna debe pasar al artículo ni a otra publicación sin permiso. El detalle está en «Fuentes y derechos».

## La lámina de referencia

El pedido parte de una imagen que el autor guardó de la cuenta *vernacularology*: «Bohío», de F. Leon, 1995, tinta sobre Mylar, publicada según esa cuenta en *Black and White: Journal of Architecture and Ideas*, vol. 0, n.º 3, «Mile Zero». Esa imagen no está en el repositorio.

Lo que se ve en ella:

- **Un alzado de frente.** La casa está en proyección recta, sin perspectiva. No hay suelo, cielo, vecinos ni gente.
- **El techo manda.** Ocupa más de la mitad de la altura. Las hojas de palma del alero y de la cumbrera están dibujadas una por una, y el resto del techo es un punteado denso.
- **La pared, tabla por tabla.** Es una fila de piezas verticales con dos largueros horizontales y una puerta al centro.
- **Una leyenda al pie.** Una línea manuscrita dice que es un bohío típico de la provincia de Pinar del Río y enumera los materiales con su nombre local. Se alcanzan a leer *penca*, *yagua* y *cuje*.
- **Una escala gráfica** debajo de la casa.
- **Un tipo y no un edificio.** La casa no tiene dueño ni dirección: representa a todas las de su clase.
- **Tinta y un solo color.** Todo lo que se sabe del material se dice con línea, punto y rayado.

Es un levantamiento de arquitecto aplicado a una casa campesina. El dibujo le da a la casa común el trato que la disciplina reserva para los monumentos.

## Cinco caminos para leer el pedido

De esa lectura salen cinco criterios. Cada lámina del catálogo dice por cuáles entra.

| Camino | Qué pide | Láminas |
|---|---|---|
| **La medida** | Planta, corte o alzado en proyección recta, con escala o cotas | 48 |
| **El material** | Que el dibujo distinga pieza por pieza de qué está hecho el edificio | 38 |
| **El tipo común** | Un edificio corriente y sin autor, no un monumento | 35 |
| **La leyenda** | Letras, números o nombres que explican las partes dentro de la misma lámina | 42 |
| **El objeto solo** | El edificio aislado y de frente, sin escena ni paisaje | 50 |

Dos láminas no cumplen ninguno y entran como contraste; su comentario lo dice.

Las más cercanas a la referencia:

- **N.º 8,** el putuku de champa de Chávez (1998): una casa sola, casi de frente, con cada bloque dibujado y un hombre al lado. Es el bohío del altiplano.
- **N.os 9 y 10,** la planta, los cortes y el corte con materiales de un putuco de Taraco (2025): tienen cotas, escala y los materiales nombrados.
- **N.º 17,** la planta de una casa en Jalsuri (2019), con cada recinto rotulado en aymara.
- **N.º 59,** la Puerta del Sol de Angrand (1848): un alzado a la aguada, de frente, con escala y sin paisaje.
- **N.º 64,** la misma portada en Stübel y Uhle (1892), acotada a escala 1:15.
- **N.º 48,** el pórtico de d'Orbigny (1847), con sus dos caras en alzado.

## Qué hay

| Archivo | Qué es |
|---|---|
| `imagenes/` | Las 95 láminas, a 1.300 px de lado como máximo. El nombre empieza con el número del catálogo |
| `catalogo.json` | La fuente de datos: la ficha de cada lámina, las familias y los caminos. Se edita a mano |
| `catalogo.md` | La misma ficha en tablas legibles, con el comentario de cada lámina. La escribe el generador: no se edita |
| `hoja_1_casa.jpg` a `hoja_7_pueblo.jpg` | Una hoja de contactos por familia. Las láminas con derechos van marcadas |
| `generar_hojas.py` | Rehace las hojas y `catalogo.md` |
| `recursos_por_conseguir.md` | Lo que no se pudo abrir en la primera tanda y en qué quedó después de la carpeta del autor |

## Las siete familias

| Familia | Láminas | Qué reúne |
|---|---|---|
| La casa común | 7 | Chozas, casas de pueblo y tambos vistos por viajeros del siglo XIX. Todas son vistas |
| La casa medida | 16 | Plantas, cortes y alzados de la casa aymara, del putuco y de dos pueblos, en estudios de 1935 a 2025 |
| La torre funeraria | 13 | La chullpa aymara y las tumbas de cista, con cuatro plantas y cortes |
| Tiwanaku en planta y en perfil | 11 | Planos de conjunto, plantas piedra por piedra y un perfil |
| Tiwanaku: portadas y piedra labrada | 24 | La portada monolítica en alzado y en vista, y los bloques dibujados como piezas |
| Las islas y la orilla del lago | 22 | La arquitectura inca de las islas del Sol y de la Luna y de Copacabana |
| El pueblo y la iglesia | 2 | La entrada de la iglesia de Tiwanaku y el santuario de Copacabana |

## Lo que muestra la recopilación

Son observaciones sobre lo que se encontró, no sobre la historia del dibujo.

1. **La casa común tardó un siglo en ser medida.**
   - En los libros del siglo XIX, las casas son vistas de viajeros (n.os 1 a 7). Las plantas y los cortes se reservaban para tumbas, templos y palacios.
   - Los levantamientos de la casa aparecen después: el pueblo de Chipaya en 1935 (n.º 23), Enquelga en 1975 (n.º 22), la vivienda aymara en 1990 (n.os 14 a 16) y los putucos desde 1998 (n.os 8 a 13).
   - Por eso casi todo lo que hay de la casa medida tiene derechos, y lo que está libre es de monumentos.
2. **El putuco es la casa mejor dibujada.** Tiene vista de frente (n.º 8), planta y cortes (n.º 9), corte con materiales (n.º 10), planta de conjunto (n.º 11) y dos perspectivas rotuladas (n.os 12 y 13).
3. **Sigue faltando el alzado con leyenda.** Ningún dibujo junta, como el bohío, el alzado de frente, la escala y la lista de materiales con su nombre local. El n.º 8 tiene lo primero; el n.º 10, los materiales en inglés; el n.º 17, los nombres en aymara sobre una planta. Reunirlos es trabajo de dibujo.
4. **La Puerta del Sol, dibujada por cuatro manos.** D'Orbigny (n.º 48, 1847), Angrand (n.º 59, 1848), Wiener (n.os 52 y 53, 1880) y Stübel y Uhle (n.os 64 y 65, 1892) dibujan la misma pieza. Sirve para comparar qué registra cada manera: la aguada, el grabado, la vista y el alzado acotado.
5. **La piedra como pieza suelta.** Inwards (n.os 55 a 58), Angrand (n.os 61 a 63) y Stübel y Uhle (n.os 68 a 71) dibujan los bloques de Tiwanaku uno por uno, en isométrica o en alzado y planta. Es el mismo trato que el bohío da a cada tabla.
6. **Los dos interiores.** Solo dos láminas muestran un edificio por dentro: la choza de Uchusuma (n.º 5) y las cámaras del palacio de la isla del Sol (n.º 75).
7. **La piedra que cambia de edificio.** Inwards dibuja la casa del n.º 2 para mostrar que sus pilares, su escalera y su portada salieron de las ruinas. Wiener dibuja la entrada de la iglesia de Tiwanaku con dos monolitos antiguos a los lados (n.º 94).

## Una nota sobre el nombre

El pedido habla de culturas «mesoamericanas» de Bolivia. Mesoamérica es el área de México y Centroamérica. Las culturas del altiplano boliviano (aymara, uru-chipaya, tiwanaku, inca) pertenecen al área andina, y con ese nombre se buscó.

## Fuentes y derechos

Cada ficha del catálogo lleva su estado. Son cinco.

| Estado | Láminas | Qué significa |
|---|---|---|
| Comprobado | 50 | La institución que guarda el ejemplar dice que está en dominio público |
| Por fecha | 21 | El autor murió hace más de setenta años, pero la ficha del escaneo no trae declaración |
| Por confirmar | 8 | Hay un motivo concreto de duda. No conviene publicarlas |
| Licencia abierta | 2 | Se pueden reproducir citando al autor y sin uso comercial |
| Con derechos | 14 | Solo para estudio. Reproducirlas fuera de aquí pide permiso |

**Primera tanda, de Internet Archive:**

| Fuente | Láminas | Estado |
|---|---|---|
| E. G. Squier, *Peru: Incidents of Travel and Exploration in the Land of the Incas*, 1877. Escaneo del Getty Research Institute | 21 | Comprobado: `NOT_IN_COPYRIGHT` |
| A. F. Bandelier, *The Islands of Titicaca and Koati*, 1910. Escaneo del Getty Research Institute | 12 | Comprobado: `NOT_IN_COPYRIGHT` |
| Alcide d'Orbigny, *Voyage dans l'Amérique méridionale*, atlas de la parte histórica, 1847. Escaneo de Smithsonian Libraries | 8 | Comprobado: «Not in copyright» |
| Richard Inwards, *The Temple of the Andes*, 1884. Escaneo del Getty Research Institute | 8 | Comprobado: `NOT_IN_COPYRIGHT` |
| Charles Wiener, *Pérou et Bolivie*, 1880. Escaneo de la Universidad de Carolina del Norte | 9 | Por fecha: el autor murió en 1913 |
| Arthur Posnansky, *Guía general ilustrada…*, La Paz, 1912 | 1 | Por fecha: el autor murió en 1946 |
| E. W. Middendorf, *Peru*, t. III, 1895 | 1 | Por fecha: el autor murió en 1908 |
| Arthur Posnansky, *Una metrópoli prehistórica en la América del Sud*, 1914. Escaneo de Wellcome Collection | 3 | **Por confirmar:** la ficha de Wellcome dice que el ejemplar podría tener derechos |

Dos de las nueve láminas de Wiener (n.os 35 y 93) son hojas que el autor ubicó y leyó.

**Segunda tanda, de la carpeta del autor:**

| Fuente | Láminas | Estado |
|---|---|---|
| Alphons Stübel y Max Uhle, *Die Ruinenstätte von Tiahuanaco*, 1892. Digitalización de la Universidad de Heidelberg | 10 | Por fecha: Stübel murió en 1904 y Uhle en 1944. Las condiciones de Heidelberg no se pudieron leer |
| Léonce Angrand, dibujos de 1848, publicados por Heiko Prümers en *Beiträge zur Allgemeinen und Vergleichenden Archäologie*, 13, 1993 | 5 | **Por confirmar:** los dibujos son de 1848 y Angrand murió en 1886, pero la reproducción viene de un artículo de 1993. Los originales están en la Biblioteca Nacional de Francia |
| Édouard Riou, grabado de *Le Tour du monde*, t. 6, 1862. Wikimedia Commons | 1 | Comprobado: dominio público, según la ficha |
| Yasmani Vitulas-Quille y Karina Reynoso-Machaca, capítulo de IntechOpen, 2025 | 4 | Con derechos. La licencia no consta en el PDF |
| Marina Suárez Jordán, *Ciudad y Territorio*, 85, 1990 | 3 | Con derechos |
| Heber Chui Betancur y otros, *Cuadernos de Vivienda y Urbanismo*, 15, 2022 | 2 | Con derechos. Licencia sin comprobar |
| Sergio J. Chávez, *Andean Past*, 5, 1998 | 1 | Con derechos |
| Andrea Gamio Felipa, *Anales de Edificación*, 3 (2), 2017. El dibujo es de Marussi (1999) | 1 | Con derechos |
| Pacha Yapucha Yampara Blanco, *Revista Nodo*, 14 (27), 2019 | 1 | Con derechos. Licencia sin comprobar |
| Václav Šolc, *Annals of the Náprstek Museum*, 8, 1975 | 1 | Con derechos |
| Alfred Métraux, *Journal de la Société des Américanistes*, 27 (1), 1935 | 1 | Con derechos: el autor murió en 1963 |
| Diego González Carrasco, tesis de la Universidad de Sheffield, 2016 | 1 | Licencia abierta: CC BY-NC-ND 2.5 |
| Sergio Alfaro Malatesta y otros, *Maskana*, 14 (2), 2023. El croquis es de Contreras Álvarez (1974) | 1 | Licencia abierta: CC BY-NC-SA 4.0 |

Notas:

- **Varias de esas revistas publican hoy con licencias Creative Commons.** No se comprobó la de cada artículo, así que la ficha dice «con derechos» mientras no conste otra cosa. Vale la pena mirarlo: algunas pasarían a «licencia abierta».
- **Los PDF completos no están en el repositorio.** Siguen en el Drive del autor. Aquí solo va el recorte de cada figura.
- **Las páginas.** Las de Squier, Wiener y Middendorf son las páginas impresas. Las de Bandelier salen de su lista de láminas. En Inwards y en Stübel y Uhle, el número es el de la lámina. En Angrand, el número es el de la figura del artículo de Prümers.
- **Lo que no se pudo leer.** Tres láminas de d'Orbigny y una de Posnansky no dejan leer su número o su título en el escaneo. La ficha lo dice.
- **Los títulos de Inwards.** Sus láminas no llevan título impreso. La ficha cita la frase con que el propio autor las describe en el texto.
- **Lo que se tocó.** Cada lámina es un recorte de la página. Las que venían de costado se giraron. A las tres de Posnansky de 1914 se les subió el contraste.

## Lo que falta o decides tú

1. **Las láminas con derechos en un repositorio público.** Entraron porque lo pediste. Si prefieres que no estén a la vista, se pueden quitar de esta rama antes de unirla, y dejar solo sus fichas con el enlace a la fuente.
2. **Las ocho por confirmar:** las tres de Posnansky de 1914 (n.os 43, 44 y 45) y las cinco de Angrand (n.os 59 a 63).
3. **Las licencias sin comprobar.** IntechOpen, *Cuadernos de Vivienda y Urbanismo*, *Revista Nodo*, *Anales de Edificación*, *Andean Past* y *Ciudad y Territorio* dicen la licencia en la página de cada artículo.
4. **Lo que no es de Bolivia.** Catorce láminas son del lado peruano del lago y cuatro del altiplano chileno. La ficha lo dice en el lugar. Si la serie debe ser solo boliviana, salen los n.os 1, 4, 5, 6, 9 a 13, 18 a 22, 26, 27, 30, 31, 32 y 35. Los n.os 8, 28 y 36 no nombran su sitio.
5. **Las cuatro que se repiten.** Los n.os 1, 3, 27 y 38 ya están en la taxonomía visual (`taxonomia/`, n.os 2, 11, 32 y 31).
6. **Las familias y los caminos** son una propuesta. Se cambian en `catalogo.json`.
7. **Lo que queda por revisar de tu carpeta** está en `recursos_por_conseguir.md`.
8. **El dibujo que no existe.** El alzado de una casa del altiplano con su escala y su lista de materiales en aymara está por hacer. Los n.os 8, 9, 10 y 17 dan casi todos los datos.
9. **Si alguna lámina pasa al artículo,** vale la regla de `AGENTS.md`: necesita un pasaje que la pida y un dominio público comprobado, y la declaración de uso de IA tiene que nombrar esta búsqueda, que se hizo con Claude.

## Cómo regenerar

```bash
python3 registros_de_arquitectura/generar_hojas.py   # las siete hojas de contactos y catalogo.md
```

Necesita Pillow.

Para añadir una lámina:

1. Ponla en `imagenes/`, a 1.300 px de lado como máximo.
2. Añade su ficha a `catalogo.json`, con la fuente, el enlace, los derechos y su estado, la familia, los caminos y el comentario.
3. Regenera.
