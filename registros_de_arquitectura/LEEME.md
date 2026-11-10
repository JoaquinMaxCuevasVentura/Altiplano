# Registros de arquitectura del altiplano

61 láminas de dominio público con dibujos de arquitectura del altiplano boliviano y de la cuenca del lago Titicaca, publicadas entre 1847 y 1914. Cada una lleva su fuente, su página y un comentario que dice por qué entra. 10 de noviembre de 2026.

Es solo una recopilación. No toca el artículo ni sus figuras.

## La lámina de referencia

El pedido parte de una imagen que el autor guardó de la cuenta *vernacularology*: «Bohío», de F. Leon, 1995, tinta sobre Mylar, publicada según esa cuenta en *Black and White: Journal of Architecture and Ideas*, vol. 0, n.º 3, «Mile Zero». La imagen no está en el repositorio porque no es de uso libre.

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
| **La medida** | Planta, corte o alzado en proyección recta, con escala o cotas | 26 |
| **El material** | Que el dibujo distinga pieza por pieza de qué está hecho el edificio | 25 |
| **El tipo común** | Un edificio corriente y sin autor, no un monumento | 17 |
| **La leyenda** | Letras, números o nombres que explican las partes dentro de la misma lámina | 22 |
| **El objeto solo** | El edificio aislado y de frente, sin escena ni paisaje | 30 |

Dos láminas no cumplen ninguno y entran como contraste; su comentario lo dice.

Ninguna lámina cumple los cinco caminos. Las más cercanas a la referencia son estas:

- **N.º 28,** el pórtico de Tiwanaku de d'Orbigny (1847): dos alzados de frente, sin paisaje y con escala.
- **N.º 8,** la tumba aymara de Carangas, también de d'Orbigny: planta y corte con escala.
- **N.º 51,** una lámina de Bandelier (1910) con los muros de Pilco-Kayma en alzado y cada piedra dibujada.
- **N.º 2,** la casa de un agricultor cerca de Tiwanaku, de Inwards (1884): la única casa dibujada por sí misma.

## Qué hay

| Archivo | Qué es |
|---|---|
| `imagenes/` | Las 61 láminas, a 1.300 px de lado como máximo. El nombre empieza con el número del catálogo |
| `catalogo.json` | La fuente de datos: la ficha de cada lámina, las familias y los caminos. Se edita a mano |
| `catalogo.md` | La misma ficha en tablas legibles, con el comentario de cada lámina. La escribe el generador: no se edita |
| `hoja_1_casa.jpg` a `hoja_6_pueblo.jpg` | Una hoja de contactos por familia, para ver las láminas juntas |
| `generar_hojas.py` | Rehace las hojas y `catalogo.md` |
| `recursos_por_conseguir.md` | La lista de lo que apareció en la búsqueda y no se pudo abrir, con su enlace, lo que pasó y qué buscar en cada sitio |

## Las seis familias

| Familia | Láminas | Qué reúne |
|---|---|---|
| La casa común | 7 | Chozas, casas de pueblo y tambos. Todas son vistas |
| La torre funeraria | 11 | La chullpa aymara y las tumbas de cista, con tres plantas y cortes |
| Tiwanaku en planta y en perfil | 9 | Planos de conjunto, plantas piedra por piedra y un perfil |
| Tiwanaku: portadas y piedra labrada | 11 | La portada monolítica en alzado y en vista, y los bloques dibujados como piezas |
| Las islas del lago | 21 | La arquitectura inca de las islas del Sol y de la Luna |
| El pueblo y la iglesia | 2 | La entrada de la iglesia de Tiwanaku y el santuario de Copacabana |

## Lo que muestra la recopilación

Son observaciones sobre lo que se encontró, no sobre la historia del dibujo.

1. **La casa común del altiplano no tiene levantamiento en estas fuentes.**
   - Las siete láminas de casas son vistas de viajeros.
   - Las plantas, los cortes y los alzados existen desde 1847, pero se hicieron para tumbas, templos y palacios.
   - El equivalente altiplánico del bohío, una casa de adobe, piedra o champa con techo de paja dibujada en alzado y con sus materiales nombrados, no apareció en ninguna fuente de dominio público.
2. **La chullpa es el tipo mejor medido.** Tiene planta y corte en d'Orbigny (n.º 8) y en Squier (n.os 10, 11 y 12).
3. **Los dos interiores.** Solo dos láminas muestran un edificio por dentro: la choza de Uchusuma (n.º 5) y las cámaras del palacio de la isla del Sol (n.º 42). En la primera se ven los palos del techo y la paja.
4. **La piedra que cambia de edificio.** Inwards dibuja la casa del n.º 2 para mostrar que sus pilares, su escalera y su portada salieron de las ruinas. Wiener dibuja la entrada de la iglesia de Tiwanaku con dos monolitos antiguos a los lados (n.º 60).
5. **El mismo edificio, dibujado tres veces.** El palacio de la isla del Sol aparece en vista en d'Orbigny (n.º 39), en planta en Squier (n.os 43 y 44) y en detalle en Bandelier (n.os 50 a 54). Sirve para comparar qué registra cada manera de dibujar.

## Una nota sobre el nombre

El pedido habla de culturas «mesoamericanas» de Bolivia. Mesoamérica es el área de México y Centroamérica. Las culturas del altiplano boliviano (aymara, uru-chipaya, tiwanaku, inca) pertenecen al área andina, y con ese nombre se buscó.

## Fuentes y derechos

| Fuente | Láminas | Derechos |
|---|---|---|
| E. G. Squier, *Peru: Incidents of Travel and Exploration in the Land of the Incas*, 1877. Internet Archive, escaneo del Getty Research Institute | 21 | `NOT_IN_COPYRIGHT` en los metadatos del ejemplar |
| A. F. Bandelier, *The Islands of Titicaca and Koati*, 1910. Internet Archive, escaneo del Getty Research Institute | 12 | `NOT_IN_COPYRIGHT` en los metadatos del ejemplar |
| Alcide d'Orbigny, *Voyage dans l'Amérique méridionale*, atlas de la parte histórica, 1847. Internet Archive, escaneo de Smithsonian Libraries para la Biodiversity Heritage Library | 8 | «Not in copyright», según la ficha |
| Richard Inwards, *The Temple of the Andes*, 1884. Internet Archive, escaneo del Getty Research Institute | 8 | `NOT_IN_COPYRIGHT` en los metadatos del ejemplar |
| Charles Wiener, *Pérou et Bolivie*, 1880. Internet Archive, escaneo de la Universidad de Carolina del Norte | 7 | Dominio público por fecha: el autor murió en 1913. La ficha no trae declaración |
| Arthur Posnansky, *Guía general ilustrada…*, La Paz, 1912. Internet Archive, escaneo de la Universidad de Carolina del Norte | 1 | Dominio público por fecha: el autor murió en 1946. La ficha no trae declaración |
| E. W. Middendorf, *Peru*, t. III, 1895. Internet Archive, escaneo de la Universidad de Toronto | 1 | Dominio público por fecha: el autor murió en 1908. La ficha no trae declaración |
| Arthur Posnansky, *Una metrópoli prehistórica en la América del Sud*, t. I, Berlín, 1914. Internet Archive, escaneo de Wellcome Collection | 3 | **Por confirmar.** La obra es de 1914 y el autor murió en 1946, pero la ficha de Wellcome dice que el ejemplar podría tener derechos |

- **Las páginas.** Las de Squier, Wiener y Middendorf son las páginas impresas. Las de Bandelier salen de su lista de láminas. En Inwards, el número es el de la lámina.
- **Lo que no se pudo leer.** Tres láminas de d'Orbigny y una de Posnansky no dejan leer su número o su título en el escaneo. La ficha lo dice y da el enlace a la hoja.
- **Los títulos de Inwards.** Sus láminas no llevan título impreso. La ficha cita la frase con que el propio autor las describe en el texto.
- **Lo que se tocó.** Cada lámina es un recorte de la página escaneada. Las que venían de costado se giraron. A las tres de Posnansky de 1914 se les subió el contraste, porque el escaneo es oscuro.

## Lo que se buscó y no entró

**Libros revisados sin dibujos de arquitectura que sirvan:**

- David Forbes, *On the Aymara Indians of Bolivia and Peru*, 1870: retratos y objetos.
- Arthur Chervin, *Anthropologie bolivienne*, 1907: fotografías antropométricas.
- Créqui-Montfort y Sénéchal de la Grange, *Rapport sur une mission scientifique en Amérique du Sud*, 1904: mapas.
- A. F. Bandelier, *The Ruins at Tiahuanaco*, 1911: el escaneo disponible no conserva las láminas.
- Francis de Castelnau, *Antiquités des Incas*, 1854: la lámina de Tiwanaku es de iconografía, y el escaneo está muy lavado.
- Posnansky (1912) y Middendorf (1895) traen sobre todo fotografías. De cada uno entró una sola lámina.

**Con derechos o con derechos dudosos.** Sirven para consultar; no se copiaron al repositorio.

- *Handbook of South American Indians*, vol. 2, Smithsonian, 1946 ([Internet Archive](https://archive.org/details/bulletin14321946smit)). Son fotografías cedidas por Alfred Métraux y Harry Tschopik:
  - lámina 101, chullpas en territorio aymara ([hoja n716](https://archive.org/details/bulletin14321946smit/page/n716/mode/1up));
  - lámina 114, el techado de una casa chipaya en Carangas ([hoja n737](https://archive.org/details/bulletin14321946smit/page/n737/mode/1up));
  - las láminas vecinas (hojas n719 y n736) muestran casas, pero no se cotejaron sus pies.
- Alfred Métraux, *Les Indiens Uro-Čipaya de Carangas*, 1935 ([Internet Archive](https://archive.org/details/les-indiens-uro-cypaya-de-carangas-1935)). El autor murió en 1963. No se revisó.
- Arthur Posnansky, *Antropología y sociología de las razas interandinas*, 1938 ([Internet Archive](https://archive.org/details/antropologia-y-sociologia-de-las-razas-interandinas-y-de-las-regiones-adyacentes)). No se revisó.
- Weston La Barre, *The Aymara Indians of the Lake Titicaca Plateau*, 1948, y Harry Tschopik, *The Aymara of Chucuito*, 1951. No se revisaron.

**ResearchGate y revistas académicas.** ResearchGate rechaza las consultas automáticas, así que sus figuras no se revisaron una por una. Las figuras de estos trabajos son de sus autores, salvo que la revista diga otra cosa.

- [«Comparación del sistema constructivo de Putucos con otros sistemas constructivos en tierra»](https://www.researchgate.net/publication/319967004_Comparacion_del_sistema_constructivo_de_Putucos_con_otros_sistemas_constructivos_en_tierra_Comparison_of_the_construction_system_of_Putucos_with_other_construction_systems_in_earth).
- [«Prototype of a Putuco-Type Vernacular House Based on Ch'ampa…»](https://www.researchgate.net/publication/383319494_Prototype_of_a_Putuco-Type_Vernacular_House_Based_on_Ch'ampa_to_Improve_Thermal_Comfort_in_a_Cold_and_Dry_Climate_in_Southern_Peru), de 2024.
- [«Arquitectura de los pueblos milenarios del altiplano: una configuración femenina y masculina, Jaqi Andino»](https://www.researchgate.net/publication/355992328_arquitectura_de_los_pueblos_milenarios_del_altiplano_una_configuracion_femenina_y_masculina_Jaqi_Andino). Según su resumen, levanta 15 viviendas del altiplano boliviano y peruano.
- [«Características de la arquitectura vernácula en zonas altoandinas de Perú»](https://www.researchgate.net/publication/362614435_Caracteristicas_de_la_arquitectura_vernacula_en_zonas_altoandinas_de_Peru_Una_contribucion_al_estudio_del_mundo_rural).
- Sergio Alfaro Malatesta, Beatriz Yuste Miguel y Massimo Palme, [«Los cielos de paja y barro aligerado: respuesta adaptativa al clima extremo en contexto andino»](https://publicaciones.ucuenca.edu.ec/ojs/index.php/maskana/article/view/4900), *Maskana*, 14 (2), 2023. Licencia CC BY-NC-SA 4.0.
- Risto Kesseli y Martti Pärssinen, [«Identidad étnica y muerte: torres funerarias (chullpas) como símbolos de poder étnico en el altiplano boliviano de Pakasa»](https://journals.openedition.org/bifea/4936), *Bulletin de l'IFEA*, 34 (3), 2005. En la parte revisada trae mapas y fotografías, sin plantas.
- Un artículo de *Andean Past* sobre el putuku y un trabajo sobre la casa uru chipaya en el repositorio CORE aparecieron en la búsqueda, pero sus servidores no dejaron leerlos.
- Dos obras impresas que estos trabajos citan como fuente de planos: Marussi Castellán, *Arquitectura vernacular: los putucos de Puno* (Universidad Ricardo Palma, 1999), y Šolc, *Casa aymara en Enquelga* (1975).

**Repositorios que no respondieron desde el entorno de trabajo:**

- Gallica, HathiTrust, Europeana y el sitio de la Biodiversity Heritage Library dieron el error 403. De la BHL se usó la copia que está en Internet Archive.
- La New York Public Library no conectó.
- Wikimedia Commons limita las consultas. Solo se pudieron listar categorías.
- La Library of Congress respondió. No se buscó en ella porque su fondo de Bolivia es de fotografías.

## Lo que falta o decides tú

1. **Las familias y los caminos** son una propuesta. Se cambian en `catalogo.json`.
2. **Las tres láminas de Posnansky de 1914** (n.os 25, 26 y 27) tienen los derechos por confirmar. Hasta entonces, no conviene publicarlas.
3. **El lado peruano del lago.** Entraron nueve láminas de Puno, de la puna de Tacna y de Tacora, que hoy está en Chile, porque son el mismo altiplano. La ficha lo dice en el lugar. Si la serie debe ser solo de Bolivia, salen los n.os 1, 4, 5, 6, 10, 11, 14, 15 y 16; el n.º 12 no nombra su sitio.
4. **Las cuatro que se repiten.** Los n.os 1, 3, 11 y 20 ya están en la taxonomía visual (`taxonomia/`, n.os 2, 11, 32 y 31). Aquí van recortadas de nuevo y más grandes.
5. **Fuentes que faltan:**
   - Stübel y Uhle, *Die Ruinenstaette von Tiahuanaco*, 1892, con los levantamientos más exactos de Tiwanaku. No apareció en Internet Archive.
   - Los dibujos de Léonce Angrand de 1848, en la Biblioteca Nacional de Francia.
   - El álbum de la misión francesa de 1903 en Tiwanaku, que está en Wikimedia Commons.
   - Las casas chipayas de Métraux, cuando se aclaren sus derechos.
6. **El dibujo que no existe.** Si la casa común del altiplano no tiene un alzado como el del bohío, hacerlo es trabajo de dibujo y no de archivo. Las láminas de la primera familia y las fotografías de 1946 son el material de partida.
7. **Si alguna lámina pasa al artículo,** vale la regla de `AGENTS.md`: necesita un pasaje que la pida, y la declaración de uso de IA tiene que nombrar esta búsqueda, que se hizo con Claude.

## Cómo regenerar

```bash
python3 registros_de_arquitectura/generar_hojas.py   # las seis hojas de contactos y catalogo.md
```

Necesita Pillow.

Para añadir una lámina:

1. Ponla en `imagenes/`, a 1.300 px de lado como máximo.
2. Añade su ficha a `catalogo.json`, con la fuente, el enlace a la página, los derechos, la familia, los caminos y el comentario.
3. Regenera.
