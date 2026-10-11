# 29. El atlas de Are.na: registro

**Fechas:** 10 y 11 de octubre.

**De dónde sale.** Aprobaste la propuesta de `28` («1. Yes 2. Empty for my scans»): once canales privados, y el de pasteles vacío para tus escaneos. Este registro dice qué se creó, cómo se hizo, qué falló y qué falta. El artículo no se tocó.

**En una línea:** 11 canales privados y 38 bloques (24 enlaces, 10 textos y 4 imágenes). No se conectó nada de otras personas, y el canal de pasteles está vacío.

## 29.1. La arquitectura

- **La cuenta:** joaquin-cuevas (id 631536), plan gratuito.
- **La matriz:** `altiplano` (id 5846731). Conecta los diez canales y tiene tres bloques de texto: «Cómo se lee este atlas», «El artículo: título, tesis e índice» y «Ya citado (no se busca de nuevo)».
- **Todo es privado.** Se comprobó canal por canal el 11 de octubre.

| Canal | ID | Bloques | Rima con |
|---|---|---|---|
| `altiplano` (matriz) | 5846731 | 3, más los 10 canales | Todo el artículo |
| `altiplano · la novela y su autor` | 5846732 | 6 | §1 |
| `altiplano · piedra` | 5846733 | 5 | §1, §3, §7; figuras 1-3 y 8 |
| `altiplano · papel` | 5846734 | 3 | §2, §4 |
| `altiplano · máquina` | 5846735 | 4 | §5; figuras 3 y 4 |
| `altiplano · cuerpo y memoria` | 5846736 | 3 | §6, §7; figuras 5-7 |
| `altiplano · dibujo` | 5846737 | 4 | §2, §8; figura 8 |
| `altiplano · crítica` | 5846738 | 4 | §1, §8 |
| `altiplano · vecinas` | 5846739 | 4 | §1 |
| `altiplano · cruces` | 5846740 | 2 | §2-§4, §7 |
| `altiplano · pasteles` | 5846741 | 0 | Figuras 1-8: tus escaneos |

**Cada bloque lleva su ficha:**

- qué es;
- la licencia;
- por qué está aquí;
- qué se toma;
- cómo se verificó;
- qué falta.

Los títulos siguen la forma «§ · autor · obra · año». En los metadatos van la sección, la licencia y el estado («verificado con el buscador», «no leído», «pendiente»).

## 29.2. Cómo se usó Are.na y qué falló

**Herramientas usadas:** `getCurrentUser`, `getUserContents`, `getChannel`, `channelDigest`, `getChannelContents`, `getBlock`, `getBlockConnections`, `createChannel`, `createConnection`, `createBlock` (de uno en uno), `updateBlock` y `deleteConnection`.

**No se usaron:**

- `searchAndConnect`, porque conecta resultados sin revisarlos;
- `batchCreateBlocks`, porque ya había dado `403`;
- los comentarios.

**Lo que falló y cómo se resolvió:**

| Problema | Qué pasó | Solución |
|---|---|---|
| El buscador de Are.na | `search` responde `403`: pide una suscripción Premium | Se buscó con el buscador web, y los canales ajenos se revisaron por su nombre |
| Un TIFF de Commons | Las miniaturas de la foto de la apacheta (1904-1905) no llegaron a Are.na: quedaban como enlace con captura | Se enlazó la página del archivo en Commons. Los dos intentos fallidos (51249996 y 51250013) se retiraron |
| La ficha de la BnF | Are.na no pudo abrir el catálogo, y el bloque quedó «fallido» y sin ficha (51249971) | Se rehízo como bloque de texto (51251693) y el fallido salió del canal. Sigue en tu cuenta, suelto: puedes borrarlo |
| `deleteConnection` | Devuelve un error de formato aunque funcione | Cada retiro se confirmó con el recuento del canal |
| Las listas en Markdown | Sin una línea en blanco antes, Are.na las muestra como texto con saltos | Se corrigió en 51249978 y 51249981 |
| La red del entorno | Casi todos los sitios están bloqueados: Commons, archive.org, doi.org, la web de Are.na y su servidor de imágenes | Solo funcionaron el buscador y el conector. Ninguna página se abrió desde aquí, y cada ficha dice cómo se verificó |
| El conector | Se desconectó una vez durante la revisión | Se reconectó y la revisión siguió |
| Un bloque de prueba | 51250020 | Se retiró; lo confirma el recuento |

**Las capturas no se revisaron.** Are.na guarda una captura de cada enlace, pero no pude verlas. Algunas pesan muy poco y podrían mostrar una página de bloqueo o de cookies en lugar de la ficha:

- Qobuz (36 KB);
- el catálogo de la UNSAM (93 KB);
- la Biblioteca Virtual Miguel de Cervantes (95 KB);
- RIBApix (95 KB).

El enlace funciona igual, pero conviene mirarlas.

**Lo que dice cada enlace al abrirse.** Are.na lee el título de la página. En casi todos los enlaces coincide con la ficha. Hay una excepción: el DOI de *Atenea* (51249977) abre una página titulada «Fernando Alegría» (ver §29.6).

## 29.3. Los bloques, canal por canal

### `altiplano` (matriz)

| ID | Tipo | Bloque | Nota |
|---|---|---|---|
| 51249964 | Texto | Cómo se lee este atlas | Actualizado el 11 de octubre: la regla de «cruces» y quién redactó las fichas |
| 51249963 | Texto | El artículo: título, tesis e índice | — |
| 51249959 | Texto | Ya citado (no se busca de nuevo) | Las 32 obras de la bibliografía |

### `la novela y su autor`

| ID | Tipo | Bloque | Nota |
|---|---|---|---|
| 51251693 | Texto | BnF · Raúl Botelho Gosálvez (1917-2004) · ficha de autoridad | Reemplaza al enlace fallido |
| 51249975 | Enlace | Wikipedia · Raúl Botelho Gosálvez | Fuente secundaria |
| 51249977 | Enlace | *Atenea*, n.º 214 · nota sobre el premio de Ciro Alegría | **Ojo:** el DOI abre «Fernando Alegría». Hay que leerlo antes de usarlo |
| 51249978 | Enlace | *La República* (2024) · «La vuelta al mundo de Ciro Alegría» | Lista corregida |
| 51249980 | Enlace | Montero (2024) · el catálogo de la Editorial Ayacucho | Ahí habría que buscar *Altiplano* |
| 51249981 | Texto | *Altiplano. Novela india* (Ayacucho) · solo PDF | Ficha ampliada: una nota preliminar fecharía la escritura en 1940 |

### `piedra`

| ID | Tipo | Bloque | Nota |
|---|---|---|---|
| 51249998 | Imagen | Squier · la Puerta del Sol de Tiwanaku · 1877 | Licencia por confirmar |
| 51250016 | Enlace | ESO / Max Alexander · apacheta cerca de ALMA (Atacama) | Es de Chile, no de Bolivia |
| 51250017 | Enlace | Bertonio · *Arte de la lengua aymara* · 1612 | Internet Archive |
| 51250018 | Enlace | Bertonio · *Vocabulario de la lengua aymara* · 1612 | Ficha de Estudios Indianos |
| 51250026 | Enlace | Expedición Nordenskiöld · apacheta entre Pelechuco y Queara · 1904-1905 | Página de Commons: el TIFF no pasó |

### `papel`

| ID | Tipo | Bloque |
|---|---|---|
| 51250029 | Enlace | *Correo del Sur* (2019) · «Los papeles de Santos Marka T'ula» |
| 51250030 | Enlace | *Correo del Sur* (2015) · las fotos de Warisata de Carlos Salazar Mostajo (MUSEF) |
| 51250031 | Texto | THOA · *El indio Santos Marka T'ula* · 1984 |

### `máquina`

| ID | Tipo | Bloque |
|---|---|---|
| 51250034 | Imagen | Establecimiento minero de Catavi · 1930 |
| 51250035 | Imagen | Castillete de la mina Viscachani |
| 51250037 | Enlace | *The Americas* · la masacre de Catavi de 1942 |
| 51250038 | Enlace | Commons · categoría «Mines in Bolivia» (índice) |

### `cuerpo y memoria`

| ID | Tipo | Bloque | Nota |
|---|---|---|---|
| 51250041 | Enlace | Stephenson (2002) · el THOA como contraesfera pública indígena | *Latin American Research Review* |
| 51250043 | Enlace | Oyarzo Varela (2022) · el THOA y Rivera Cusicanqui, 1983-1984 | Se añadió el título exacto |
| 51250044 | Enlace | *Oral History Review* · el THOA, parte 1 | — |

### `dibujo`

| ID | Tipo | Bloque | Nota |
|---|---|---|---|
| 51250051 | Imagen | Canaletto · *Capriccio* con el Rialto de Palladio · años 1750 | Dominio público |
| 51250052 | Enlace | RIBA · guía sobre Lubetkin y Tecton | — |
| 51250126 | Enlace | Gordon Cullen · mural de la salud del Finsbury Health Centre · foto de 1938 | Imagen con licencia (RIBApix): solo enlace |
| 51250139 | Enlace | Jiří Kolář · *Charitas* (rollage) · 1964 | Obra protegida (Kunsthalle Praha): solo enlace |

### `crítica`

| ID | Tipo | Bloque | Nota |
|---|---|---|---|
| 51250143 | Enlace | O'Sullivan (1951) · *Humanitarianism in the works of Raúl Botelho Gosálvez* | Tesis de la UTEP; no leída |
| 51250152 | Enlace | Choque Canqui y Ticona Alejo (1996) · *Jesús de Machaqa: la marka rebelde* | No leído |
| 51250155 | Enlace | Borello (1985) · «Arguedas: "Raza de bronce"» | No leído |
| 51250163 | Texto | Pistas pendientes de la crítica | Arriarán, Barnadas, Salazar de la Torre y las reseñas |

### `vecinas`

| ID | Tipo | Bloque |
|---|---|---|
| 51250175 | Enlace | Céspedes · *Metal del diablo* · 1946 (catálogo de la UNQ) |
| 51250179 | Enlace | Arguedas · *Raza de bronce* · 1919 (Wikipedia) |
| 51250189 | Texto | Alegría · *El mundo es ancho y ajeno* · 1941 |
| 51250206 | Texto | Botelho · *Borrachera verde* (1937) y *Coca* (1941) |

### `cruces`

| ID | Tipo | Bloque | Nota |
|---|---|---|---|
| 51250211 | Enlace | The Voidz en Qobuz | Servicio con licencia. La web oficial (thevoidz.com) no se pudo comprobar. El enlace de Deezer que tenía apuntado no entró: no se pudo saber de quién era la página |
| 51250213 | Texto | Pasajes de The Voidz pendientes de cotejo | Sin letras: solo dónde están |

### `pasteles`

Está vacío: es para tus escaneos y tus procesos. Su regla pide soporte, medidas y año, y que lo hecho con IA vaya rotulado.

## 29.4. Lo conectado de otras personas

**Nada.** Estos son los canales revisados, en la fase 0 (10 de octubre) y en la revisión final (11 de octubre):

| Canal | Dueño | Qué tiene | Decisión |
|---|---|---|---|
| `indigenismo` | Another Person | Pueblos indígenas en general (IA, vivienda en EE. UU.) | No se conecta |
| `andes` | miela salgado | 13 bloques de pensamiento andino, sobre todo de Ecuador. Uno, «El pensamiento andino y la construcción de países plurinacionales y sociedades interculturales» (26095588), enlaza un artículo de ALAI sobre los estados-nación de Abya-Yala | No se conectó: es general y no toca la tierra ni la piedra del altiplano aymara. La decisión es tuya |
| `aymara` | A LUBOYERA | Un solo bloque: la foto de una bolsa de envío | No se conecta |
| `vernacular-architecture` | Émile Foucher | Arquitectura de Montreal | No se conecta |
| `bolivia` | — | Privado | — |
| `latin-american-literature`, `collage-theory` | — | No existen | — |
| Los once canales de *Contenida* | Tú | Otro proyecto | No se tocaron |

## 29.5. Qué huecos de `28` cubre cada hallazgo

| Hueco | Qué se encontró | Qué falta |
|---|---|---|
| 1. Crítica sobre *Altiplano* | La tesis de O'Sullivan (1951). El estudio de Borello sobre *Raza de bronce* (1985). Jesús de Machaqa contado desde las comunidades por historiadores aymaras (Choque Canqui y Ticona, 1996) | Ningún estudio de *Altiplano* leído. Arriarán (2021: 29-31), sin leer. Salazar de la Torre, sin encontrar. Reseñas de 1945-1946, ninguna. La pista de Barnadas queda descartada (`04`, §4.7) |
| 2. Las vecinas del concurso | *El mundo es ancho y ajeno* y su juicio por tierras; *Metal del diablo*; *Raza de bronce*; *Borrachera verde* y *Coca* | Leer al menos el juicio de Alegría. Ubicar las primeras ediciones de Botelho |
| 3. Warisata | La muestra de fotos de Salazar Mostajo (MUSEF, 2015). La nota de 1982 que el artículo ya cita | Dónde están las fotos y con qué derechos. Estudios sobre la escuela-ayllu |
| 4. Las cosas que lee el artículo | Apachetas (Nordenskiöld, 1904-1905; ESO), el castillete de Viscachani, Catavi en 1930, el índice de minas de Commons y Tiwanaku (Squier) | Pircas, mojones y chujllas; aserraderos y cocales de los Yungas. La foto FSA/OWI de una mina de Patiño (LC-USE6-D-000116): solo apareció en una ficha didáctica, no en la Biblioteca del Congreso, así que no entró |
| 5. Facsímiles coloniales | El *Arte* de Bertonio (Internet Archive) y la ficha del *Vocabulario* (Estudios Indianos) | Un facsímil del *Vocabulario*. Según el catálogo Zenon, la edición de 1956 tuvo una reimpresión de CERES en 1984 |
| Dibujo y método | Canaletto, la guía de RIBA, el mural de Cullen y Kolář | El esgrafiado en pastel al óleo: no se buscó en esta pasada |
| Cuerpo y memoria | Tres textos sobre el THOA | Las sequías del altiplano: no se buscó en esta pasada |
| Cruces | Qobuz y los pasajes por cotejar | La letra oficial |

## 29.6. Lo que tienes que mirar o decidir

1. **Las capturas** de Qobuz, la UNSAM, la Biblioteca Virtual Miguel de Cervantes y RIBApix (§29.2).
2. **El texto de *Atenea*, n.º 214.** El DOI abre una página titulada «Fernando Alegría». Puede que el texto sea del escritor chileno, o sobre él, y que solo mencione el premio de Ciro Alegría. Si vas a enviar el artículo a *Atenea*, conviene leerlo.
3. **El bloque 26095588 de `andes`.** Mi propuesta es no conectarlo.
4. **El bloque fallido 51249971.** Ya no está en ningún canal. Puedes borrarlo desde tu cuenta.
5. **Lo que hay que leer antes de citar:**
   - O'Sullivan (1951);
   - Borello (1985);
   - Choque Canqui y Ticona (1996);
   - Arriarán (2021: 29-31);
   - el juicio de *El mundo es ancho y ajeno*.
6. **Las licencias** de las imágenes de Commons (Squier, Catavi, Viscachani, Canaletto y Nordenskiöld) y de la foto del ESO.
7. **Los dos pasajes de The Voidz**, que hay que cotejar con la letra oficial (`27`, §27.11).
8. **Tus pasteles**, que van al canal `pasteles`, con soporte, medidas y año.

## 29.7. Propuestas para el artículo

**Ninguna entró: el artículo no se tocó.** Son opciones, cada una con su fuente:

1. **El concurso de 1940 (§1).** El artículo no lo menciona. La nota «Al lector» de la edición que cita el artículo dice tres cosas:
   - que la novela se escribió «entre junio y agosto de 1940» para el concurso de la Unión Panamericana y Farrar & Rinehart;
   - que el jurado boliviano no la mencionó y envió *Metal del diablo*, de Augusto Céspedes;
   - que ganó *El mundo es ancho y ajeno*, «cuyo argumento tiene un sorprendente parecido al de "Altiplano"» (Botelho Gosálvez, 1982 [1945]: 4).

   Una frase en §1 situaría la novela en su tiempo con una fuente que el artículo ya usa. Si se confirma la nota preliminar de la edición de Ayacucho (bloque 51249981), sería mejor citar esa, que es de 1945.
2. **El otro juicio por tierras (§4).** *El mundo es ancho y ajeno* también cuenta un despojo por vía judicial. Si lees ese juicio, una nota al pie podría decir que la trampa de papeles era el asunto de las dos novelas del concurso. Sin leerlo, no.
3. **La historia contada desde la marka (§4 u §8).** Choque Canqui y Ticona (1996) cuentan desde las comunidades un conflicto con el pueblo vecino: el de Jesús de Machaqa en 1921. Sería un contrapeso al narrador, en la línea de Rivera Cusicanqui. Solo después de leerlo.
4. **La rollage (§1, en nota).** Fuão cuenta que Kolář bautizó la rollage, «o ato de desfiar a imagem em tiras», por las persianas de las tiendas (Fuão, 2011: 44). Podría acompañar la cita de Kolář que ya está en §1. Es prescindible.
5. **Las fechas del autor (§1).** Si la revista las pide: «(La Paz, 1917-2004)», según la ficha de autoridad de la BnF.

## 29.8. Fuentes principales

- [Ficha de autoridad de la BnF](https://catalogue.bnf.fr/ark:/12148/cb12175725j)
- [O'Sullivan (1951), UTEP](https://scholarworks.utep.edu/dissertations/AAIEP00079)
- [Choque Canqui y Ticona (1996), catálogo de la UNSAM](https://buscador.unsam.edu.ar/Record/19722)
- [Borello (1985), Biblioteca Virtual Miguel de Cervantes](https://cervantesvirtual.com/portales/sergio_ramirez/obra/arguedas-raza-de-bronce/)
- [*Metal del diablo*, catálogo de la UNQ](https://biblio.unq.edu.ar/qfind/Record/23565/Details)
- [*Raza de bronce*, Wikipedia](https://en.wikipedia.org/wiki/Raza_de_Bronce)
- [Carlos Ramos Núñez, «La justicia en "El mundo es ancho y ajeno"», *LP Derecho*](https://lpderecho.pe/justicia-mundo-ancho-ajeno-carlos-ramos-nunez/)
- [Gordon Cullen, mural de la salud (RIBApix)](https://www.architecture.com/image-library/RIBApix/licensed-image/poster/finsbury-health-centre-pine-street-london-the-health-mural-by-gordon-cullen-by-entrance-to-the-solar/posterid/RIBA3100-38.html)
- [Jiří Kolář, *Charitas* (Kunsthalle Praha)](https://emuseum.kunsthallepraha.org/en/objects/details/1304)
- [The Voidz en Qobuz](https://www.qobuz.com/us-en/interpreter/the-voidz/2411330)
- Las demás fuentes de la fase 0 están en `28`, §28.4.
