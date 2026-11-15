# 28. Prompt para el atlas de Are.na (revisado)

**Fecha:** 10 de octubre.

**De dónde sale.** Es tu borrador de prompt, ajustado a lo que el proyecto ya tiene. No se creó nada en Are.na: tu prompt pide confirmar antes, y la revisión se hizo solo con lecturas.

## 28.1. Qué cambié y por qué

**Datos del proyecto:**

- **Los huecos del proyecto, rellenados.** Tesis, secciones, figuras, edición, destino, extensión y norma de citas salen del artículo final. El prompt ya no depende de que pegues nada.
- **Lo que ya tienes.** La lista de las 32 obras citadas entra en el prompt, para que el atlas no las busque de nuevo y se concentre en lo que falta.
- **Lo que falta.** Es una lista concreta, por prioridad, tomada de los pendientes del proyecto:
  - la crítica sobre la novela;
  - las novelas del concurso de 1940;
  - Warisata;
  - facsímiles coloniales;
  - datos de catálogo sin cerrar (`04`, §4.3);
  - la letra oficial de las dos canciones citadas.
- **La fecha de muerte del autor.** Tu borrador decía 2002. El análisis 03 registra «La Paz, 1917-2004», con varias fuentes biográficas que coinciden (por extractos del buscador). El prompt pide verificarla antes de escribirla en una ficha. La regla de derechos no cambia: la novela no es de dominio público.

**Los canales:**

- **Siguen el argumento.** En lugar de canales genéricos («contexto», «paisaje»), hay uno por material del argumento: piedra (el ayllu), papel (la aldea y el Estado) y máquina (los Yungas y la mina). Se suman cuerpo y memoria, el dibujo como método, la crítica, las vecinas y los cruces con la cultura popular. Cada canal dice con qué sección y figura rima.
- **No hay canal de «paisaje».** El artículo critica al narrador porque «vuelve paisaje una posesión» (§8). Un canal de fotos del altiplano repetiría esa mirada. Las imágenes entran por lo que muestran del trabajo y de la posesión (mojones, pircas, apachetas, chujllas, castilletes), siempre con autor, fecha y lugar.
- **No hay canal de «fuentes» con citas.** Las 153 citas de la novela ya están verificadas en el artículo, y copiarlas a otro lugar abre la puerta a errores. Una cita nueva entra solo con su fuente abierta y su página, en el canal temático que le toca.

**El conector y tu cuenta:**

- **Tu cuenta.** Es del plan gratuito (*tier* «free») y ya tiene 11 canales privados de otro proyecto, *Contenida*. Ninguno es de *Altiplano*, así que no hay nada que duplicar. El prompt prohíbe tocar o conectar ese atlas sin tu permiso, aunque «contenida · la ruina» también registra Tiwanaku.
- **Los canales privados funcionan en tu plan:** los once de *Contenida* lo son. El prompt pide crear primero la matriz y comprobar con `getChannel` que quedó `private` antes de seguir.
- **`searchAndConnect` queda prohibido.** Conecta hasta 20 resultados sin revisarlos. `batchCreateBlocks` sigue prohibido, porque ya te dio `403`.
- **Campos útiles del conector.** `createBlock` acepta `alt_text`, `original_source_url`, `original_source_title` y `metadata`. El prompt pide texto alternativo en cada imagen y, si conviene, metadatos de sección, licencia y estado.
- **`channelDigest`** resume un canal sin traerlo entero. Sirve para revisar canales ajenos o grandes.

**Verificación:**

- **Desde este entorno no se abre la web.** Probé veinte direcciones de la lista de búsqueda (Commons, Internet Archive, HathiTrust, BDH, Library of Congress, SciELO, Redalyc, DOAJ, doi.org, Persée, are.na, la Biblioteca Virtual de la UMSA, Open Library y otras) y ninguna abrió. Solo funciona el buscador. El conector de Are.na sí funciona, porque va por otro camino.
- **Cómo se verifica entonces.** El prompt pide anotar en cada ficha *cómo* se verificó cada dirección: abierta, extracto del buscador o estado del bloque en Are.na. Lo que no se pudo abrir no se da por verificado.
- **Lo que aprendimos con las letras de The Voidz.** La otra IA inventó once de trece versos. Por eso ninguna cita entra de memoria ni tomada de otra IA, y las letras no se suben: solo enlaces oficiales.

**Representación:**

- **Las reglas del artículo.** El narrador animaliza, petrifica y sexualiza a los comunarios, y la serie no dibuja el linchamiento ni «el alma» que el narrador declara cerrada. El atlas sigue el mismo límite:
  - ninguna imagen de violencia;
  - ninguna imagen que haga de las personas paisaje o material;
  - nada que ilustre a las mujeres que la novela deja sin nombre.

**El artículo y los pasteles:**

- **El artículo no se toca.** Lo que el atlas encuentre y deba entrar se propone en el registro, con fuente y página, y tú decides.
- **Los pasteles.** Las figuras del artículo serán los escaneos de tus pasteles. Las imágenes de GPT no se suben. El prompt pregunta si quieres un canal privado para tus pasteles.

## 28.2. Lo que tienes que decidir antes de usarlo

1. **Dónde correrlo.**
   - **En esta sesión.** Are.na funciona, pero las direcciones solo se pueden verificar con el buscador y con el estado del bloque.
   - **En otro entorno con acceso web**, o ampliando la red de este. Para lo segundo, abre el menú del entorno (barra de título de la sesión) → *Edit* → *Network access*, y agrega los dominios que quieras (por ejemplo commons.wikimedia.org, upload.wikimedia.org, archive.org, hathitrust.org, persee.fr, scielo.org.bo, redalyc.org, doaj.org, doi.org). Los pasos están en https://code.claude.com/docs/en/cloud-environments#network-access.
2. **Tus pasteles.** ¿Quieres un canal privado para los escaneos y su proceso? Si entran también los esquemas de encaje, irían rotulados como «esquema hecho con asistencia de IA».
3. **El cruce con *Contenida*.** ¿Se conecta algo de «contenida · la ruina» (Tiwanaku) con el signo escalonado de la Figura 2? Por defecto, no.
4. **La fecha de muerte de Botelho Gosálvez:** 2002, como decía tu borrador, o 2004, como registra el análisis 03.

## 28.3. El prompt revisado

Copia desde la línea siguiente hasta el final del bloque.

````markdown
# Atlas en Are.na para «Cosecha de piedras», un artículo sobre *Altiplano*, de Raúl Botelho Gosálvez

## El proyecto

Estoy terminando un artículo de arquitectura y dibujo sobre la novela *Altiplano* (1945), de Raúl Botelho Gosálvez.

- **Título:** «Cosecha de piedras: el ayllu, el Estado y la mina. Dibujando *Altiplano* de Raúl Botelho Gosálvez».
- **Tesis:** la novela registra, a espaldas de su narrador, la mecánica material del despojo. Marca la posesión con piedras (mojón, pirca, montón), narra su pérdida ante papeles (la aldea, el Estado) y máquinas (la mina), calla el uso aymara de la escritura y recuerda de manera selectiva. La leo con las manos: seis pasteles al óleo funcionan como herramientas de lectura.
- **Secciones y figuras:**
  - §1 Introducción: una cosecha de piedras.
  - §2 Cómo leer: el espacio, las manos y el dibujo (marco teórico y método: manuaje, ensamblaje, collage).
  - §3 La chujlla: una casa a la medida del cuerpo. Figura 1, *Cráneo/nido*; Figura 2, *Signo Escalonado frente al mapa*.
  - §4 Umacachi: la trampa de los papeles (el radio urbano, el tinterillo, el pesebre).
  - §5 El éxodo: los Yungas y la mina. Figura 3, *Umbral de la apacheta*; Figura 4, *El castillete y la caída al plano 450*.
  - §6 La sequía y el linchamiento: el cuerpo en la catástrofe. Figura 5, *Pelvis telúrica / Pachamama sorda*; Figura 6, *El centinela de la resistencia*.
  - §7 El retorno: reparar la casa, elegir la memoria. Figura 7, *La memoria del retorno*.
  - §8 Conclusiones: lo que muestra el dibujo y sus límites. Figura 8, *Tres montones*.
- **Edición que uso:** 7.ª ed., La Paz, Librería Editorial Juventud, 1982. La 1.ª ed. es de Buenos Aires, Ayacucho, 1945. Se cita así: (Botelho Gosálvez, 1982 [1945]: página).
- **Destino:** por decidir. Las candidatas están en `reports/Convocatorias abiertas para el artículo.md`; la primera es *Atenea* (Universidad de Concepción). Extensión actual: unas 10.300 palabras. Citas autor-año con página, «(Apellido, año: página)», con «ibid.» y bibliografía final.
- **Borrador:** `articulo/articulo_cosecha_de_piedras.md`, en el repositorio del proyecto, o el `.docx` adjunto. Los pendientes de verificación están en `analisis/04_verificaciones_y_pendientes.md`.

### Lo que ya tengo (no lo busques de nuevo)

Son las 32 obras citadas:

- **Novela:** Botelho Gosálvez (1982 [1945]).
- **Fuentes andinas:**
  - Bertonio (2011 [1612]), transcripción digital del ILLA-A;
  - Duviols (1979);
  - Dean (2010);
  - Rivera Cusicanqui (2010 [1984]);
  - Barnadas (1978 [1975]), con el prólogo de Choque Canqui;
  - Zavaleta Mercado (1986);
  - Cornejo Polar (2003 [1994]);
  - Spedding (2025) y Rodríguez y Rodríguez (2025), en *Susto al susto*.
- **Arquitectura, dibujo y método:**
  - Frampton (1995);
  - Pallasmaa (2014 [2011]), con Bachelard (1978 [1942]);
  - Bachelard (1983 [1957]);
  - Cárcamo Pino (2019, 2025a, 2025b);
  - Lundberg (2019);
  - Seguí de la Riva (2010);
  - Ingold (2013);
  - Garrington (2013);
  - Vázquez Ramos *et al.* (2023), con Hall (1973 [1966]);
  - Alexander *et al.* (1977);
  - Fuão (2011);
  - Monteys y Fuertes (2001);
  - Martin (2014);
  - Scott (2020 [1998]);
  - Le Guin (2021 [1986]).
- **Cruces con la cultura popular:** The Voidz (2018), *Virtue*; Julian Casablancas+The Voidz (2014), *Tyranny*.

### Lo que todavía no tengo (por prioridad)

1. **Crítica sobre *Altiplano* y su autor.** El artículo se apoya en Cornejo Polar, que trata el indigenismo en general. Busca estudios, reseñas de 1945-1946 y tesis. Pistas sin verificar:
   - un estudio de Josep M. Barnadas sobre *Altiplano* (c. 1977) que figura en catálogos pero no se encontró;
   - un texto de Salazar de la Torre (CIDES) sobre Warisata y la novela;
   - Samuel Arriarán (2021), pp. 29-31.
2. **Las vecinas del concurso de 1940.** Según la nota «Al lector» de la edición de 1982 (p. 4), la novela se escribió para el concurso de la Unión Panamericana y Farrar & Rinehart, que ganó *El mundo es ancho y ajeno*, de Ciro Alegría (1941). El jurado boliviano eligió *Metal del diablo*, de Augusto Céspedes, una novela sobre el estaño. Busca también otras indigenistas andinas (por ejemplo *Raza de bronce*, de Alcides Arguedas, 1919) y las otras novelas de Botelho (*Borrachera verde*, *Coca*).
3. **Warisata.** La nota editorial dice que Jatun-Kolla «es, en realidad, Warisata». Busca la escuela-ayllu (1931), a Avelino Siñani y Elizardo Pérez, y el paso de Botelho por Warisata: estudios y fotos históricas con autor y fecha.
4. **Las cosas que el artículo lee:** mojones y linderos, pircas, montones de piedra despejada, apachetas, chujllas de adobe y paja, castilletes y andariveles de minas de estaño, campamentos mineros, aserraderos y cocales de los Yungas. Busca fotografías, grabados o dibujos con autor, fecha y lugar, y estudios técnicos de arquitectura vernácula del altiplano.
5. **Fuentes coloniales en facsímil.**
   - El *Vocabulario* de Bertonio (1612): el artículo usa la transcripción del ILLA-A, y un facsímil permitiría cotejar.
   - La *Historia del Nuevo Mundo* de Bernabé Cobo, sobre las apachitas (Dean la comenta en pp. 57-58).
   - Duviols (1979) en Persée: la página del artículo, no el PDF.
6. **Datos de catálogo pendientes:**
   - la dirección exacta de Le Guin en es.theanarchistlibrary.org;
   - el editor y la ciudad de Frampton (1995);
   - el año y el ISBN de *Susto al susto*;
   - el editor de Cárcamo Pino (2019): Springer o EGA;
   - las páginas de la 1.ª edición de Cornejo Polar (1994);
   - la página oficial de la letra de «Pyramid of Bones» y de «Father Electricity», para cotejar los dos pasajes que cito. Enlace solamente: no copies letras.
7. **Contexto, con cada fecha verificada:**
   - la Ley de Exvinculación de 1874 y la lucha legal con títulos coloniales;
   - el Congreso Indigenal y el decreto contra el pongueaje de 1945;
   - la minería del estaño en los años cuarenta;
   - el ciclo rebelde de 1947.
8. **Voces aymaras y crítica del indigenismo.**
   - El Taller de Historia Oral Andina (THOA), del que viene el lema de mi epígrafe.
   - Otros textos de Roberto Choque Canqui.
   - Lecturas críticas del indigenismo. Sin hablar por nadie.
9. **Método.**
   - El *capriccio* de Canaletto (dominio público), que Lundberg usa para el ensamblaje.
   - Los dibujos de Gordon Cullen para Lubetkin.
   - Obras de collage que comenta Fuão (Kolář, Max Ernst): enlace al museo, sin subir imágenes con derechos.

## Cómo trabajar

### 0 · Antes de empezar

1. **Confirma la cuenta** con `getCurrentUser`: es joaquin-cuevas, en el plan gratuito.
2. **Lista mis canales** con `getUserContents`. Los once de «contenida» son otro proyecto: no los modifiques, no conectes nada a ellos ni desde ellos y no comentes en ellos. Si ya existe un canal «altiplano», dímelo antes de crear otro.

### 1 · Primero propones, después escribes

No escribas nada en Are.na hasta que yo confirme. Antes:

1. Lee la tesis, las secciones y, si puedes, el borrador.
2. Propón la arquitectura de canales. Parte de esta y ajústala:
   - `altiplano`: la matriz, que conecta todo.
   - `altiplano · la novela y su autor`: ediciones y catálogos (1945, 1967, 1982, 1987), portadas enlazadas, el concurso de 1940, la vida y las otras obras de Botelho, Warisata (§1).
   - `altiplano · piedra`: el ayllu. Mojón, pirca, montón, apacheta, chujlla, signo escalonado (§1, §3, §7; figuras 1-3).
   - `altiplano · papel`: la aldea y el Estado. Títulos, revisitas, Ley de Exvinculación, caciques apoderados, tinterillos, escuelas indigenales (§2, §4).
   - `altiplano · máquina`: los Yungas y la mina. Aserraderos, cocales, estaño, castilletes, campamentos (§5; figuras 3 y 4).
   - `altiplano · cuerpo y memoria`: sequía, rogativas, el susto y su cura, historia oral, el retorno (§6, §7; figuras 5-7).
   - `altiplano · dibujo`: el método. Pastel al óleo y esgrafiado, collage, *capriccio*, notación, dibujo como investigación (§2, §8; figura 8).
   - `altiplano · crítica`: estudios sobre la novela y su autor, crítica del indigenismo, voces aymaras (§1, §8).
   - `altiplano · vecinas`: las novelas del concurso de 1940, otras indigenistas andinas y las otras novelas de Botelho (§1).
   - `altiplano · cruces`: la cultura popular que cruza el artículo, por ahora The Voidz, solo con enlaces oficiales (§2-§4, §7).
3. No propongas un canal de «paisaje». El artículo critica al narrador porque «vuelve paisaje una posesión» (§8). Las imágenes entran por lo que muestran del trabajo y de la posesión, en el canal de su material.
4. Dime, en una tabla, qué irá en cada canal, con qué sección y figura rima, y qué huecos de la lista anterior cubre.
5. Pregúntame si quiero un canal privado para mis pasteles (escaneos y proceso). No lo crees sin mi respuesta.

### 2 · Los canales

- **Todos privados.** *Closed* no es privado: un canal *closed* lo ve cualquiera.
- **Crea primero la matriz** y comprueba con `getChannel` que su visibilidad es `private`. Después sigue con los demás, verificando cada uno.
- **Una descripción por canal**, con su regla. Conecta cada canal a la matriz.
- **En la matriz, dos bloques de texto:**
  - «Cómo se lee este atlas», con los canales, sus reglas y la sección del artículo con que rima cada uno;
  - «Ya citado», con la lista de las 32 obras (autor y año, sin fichas), para no duplicar.
- **Tamaño.** Mi plan es gratuito: en la primera pasada, no más de ocho bloques por canal. Si una creación da un error de límite o de permiso, para y avísame.

### 3 · Dónde buscar

- **Dominio público:** Wikimedia Commons, Internet Archive, HathiTrust, Biblioteca Digital Hispánica, Library of Congress, la John Carter Brown Library (impresos coloniales) y archivos y bibliotecas bolivianos con catálogo en línea (el Archivo y Biblioteca Nacionales de Bolivia, la Biblioteca Virtual de la UMSA).
- **Estudios:** SciELO Bolivia, Redalyc, DOAJ, Persée, repositorios universitarios (UMSA, CIDES), DOI.
- **Are.na:**
  - El buscador (`search`) puede dar `403` en el plan gratuito.
  - No uses `searchAndConnect`: conecta resultados sin revisarlos.
  - Encuentra material de otras personas de dos maneras: siguiendo las conexiones de un bloque hasta los canales donde está (`getBlockConnections` con `EXCLUDE_OWN`), o probando direcciones de canal (por ejemplo `indigenismo`, `andes`, `bolivia`, `latin-american-literature`).
  - Para mirar un canal ajeno o grande, usa `channelDigest`.
- **Verificación de cada dirección.**
  - Puedes buscar en la web, pero si tu entorno no puede abrir una página, no la des por verificada.
  - En cada ficha, anota cómo la verificaste: «abierta», «extracto del buscador» o «el bloque de Are.na trajo título y vista previa».
  - Si no hay forma de verificarla, el bloque va marcado como pendiente.

### 4 · Cómo se crea cada bloque

- **Uno por uno**, con `createBlock`. No uses `batchCreateBlocks`: da `403`. Ve sin ráfagas, muy por debajo de 120 pedidos por minuto.
- **Imágenes de Commons.**
  - Usa `https://commons.wikimedia.org/wiki/Special:FilePath/NOMBRE_DEL_ARCHIVO` como valor.
  - Pon la página del archivo en `original_source_url` (y su título en `original_source_title`), porque ahí están el autor y la licencia.
  - Escribe `alt_text` en cada imagen: qué se ve, en una frase factual.
- **Libros y artículos:** enlace a su página de catálogo o a su DOI, **nunca al PDF**, porque Are.na lo subiría como adjunto. No subas archivos (`presignUpload`).
- **Material de otras personas en Are.na:** se *conecta*, no se copia ni se descarga. No comentes en bloques ajenos.
- **Título:** «§n · Autor · obra · año». Si el bloque sirve a varias secciones, usa la principal.
- **Ficha en la descripción:**
  - quién, qué, cuándo, dónde;
  - licencia: dominio público, licencia libre con enlace a la ficha, o «solo enlace»;
  - por qué está aquí: con qué sección, figura o argumento rima;
  - qué se toma y qué no;
  - cómo se verificó;
  - «Pendiente», si no leíste la fuente entera o no pudiste abrirla.
- **Metadatos (opcional):** en `metadata`, `seccion`, `licencia` y `estado` (verificado o pendiente).

### 5 · Reglas de contenido

- **No inventes.**
  - Si un dato no está verificado, no va, o va marcado como pendiente.
  - Nunca cites de memoria ni copies una cita de otra IA: en este proyecto, otra IA inventó once de trece versos de canciones y corrió páginas de libros.
  - Cada cita, copiada de una fuente abierta y con página.
  - De la novela, usa solo citas que ya están en mi artículo, con su página de la edición de 1982.
- **Derechos.**
  - La novela no es de dominio público: su autor murió en el siglo XXI. Antes de escribir el año de su muerte en una ficha, verifícalo: tengo 2004 en mis notas, y mi borrador decía 2002.
  - No subas su texto ni escaneos: solo citas breves con página.
  - Las portadas, enlazadas a un catálogo. No se suben escaneos.
  - De las canciones, solo enlaces a páginas oficiales. No subas letras.
- **Representación.** *Altiplano* es una novela sobre el mundo aymara escrita desde afuera de él, y mi artículo critica cómo su narrador animaliza, petrifica y sexualiza a los comunarios. Por eso:
  - no uses palabras aymaras o quechuas como adorno ni como título de canal;
  - no juntes fotos de personas indígenas como «tipos» o decoración. Si una foto histórica entra, que diga quién la hizo, cuándo, dónde y, si se sabe, a quién retrata;
  - ninguna imagen de violencia ni de linchamientos: mi serie de pasteles tampoco dibuja el linchamiento;
  - no ilustres a las mujeres que la novela deja sin nombre;
  - busca lecturas críticas del indigenismo y voces aymaras cuando las haya, sin hablar por ellas.
- **Imágenes de IA.** Las figuras del artículo serán los escaneos de mis pasteles. No subas imágenes generadas con IA. Si yo pido un canal de pasteles y entran los esquemas de encaje, van rotulados «esquema hecho con asistencia de IA».
- **El artículo no se toca.** Si algo del atlas debería entrar, propónlo en el registro, con fuente y página. Yo decido.
- **Tono de las fichas:** español, frases simples, factual. Al criticar una obra ajena, describe sin descalificar.

### 6 · Verificar

- **Al terminar cada canal**, revisa su visibilidad (`getChannel`) y el estado de cada bloque. Las respuestas de `getChannelContents` son grandes: pide pocas por página o guárdalas y léelas con un script.
- **Si un bloque quedó en `failed`** porque la página no respondió:
  1. rehazlo como bloque de texto con el enlace adentro, marcado como pendiente;
  2. desconecta el bloque fallido. `deleteConnection` puede devolver un error de formato aunque funcione: confirma con el conteo del canal.
- **No borres canales ni bloques** que no hayas creado en esta tarea.

### 7 · Registro y entrega

- **Escribe el registro.** Si trabajas en el repositorio del artículo, en `analisis/29_atlas_arena.md`; si no, como archivo aparte. Debe tener:
  - la arquitectura;
  - cómo se usó Are.na, y qué herramientas fallaron;
  - una tabla por canal, con los bloques nuevos y lo conectado de otras personas (con su dueño);
  - qué huecos de la lista cubre cada hallazgo;
  - lo que falló, lo que no se encontró y los pendientes;
  - lo que propones que entre al artículo, con fuente y página.
- **Al final, dame:**
  - un resumen corto por canal;
  - las fuentes principales, con enlace;
  - lo que tengo que leer o decidir yo.
````
