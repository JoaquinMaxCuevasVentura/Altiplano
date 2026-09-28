# 3. Replanteo: de la fuente a las vasijas

El 28 de septiembre de 2026 dijiste que la primera versión era una aproximación muy convencional para un proyecto de este tipo. Mandaste como referencia *EthnoGraphemes: Scripts as Vessels for Culture*, la tesis de MFA en Diseño Gráfico de Vaishnavi Mahendran (Rhode Island School of Design, 2020).

**Resultado.**

- Tres piezas nuevas en `vasijas/`: **Tocas el agua**, **La voz sobre la placa** y **La cadena**.
- **Placa**, una escritura que se canta y no se lee.
- Un mapa de otras vasijas posibles.
- Contenedor, la fuente de la primera versión, sigue en el repositorio, pero ahora es una pieza más y no el proyecto entero.

Después mandaste fotos y videos de la obra. Con ellos las piezas se ajustaron a lo que pasó de verdad y se sumó una cuarta, **Espalda** (§ 3.9). El marco de cuatro ejes que enviaste más tarde tiene su propio documento: `04_ruina.md`.

Las páginas de la tesis que se citan son las de su índice.

## 3.1. Qué tenía de convencional la primera versión

- **Era un producto cerrado.** Una fuente con su muestrario, lista para aplicar. La tesis cita a Genese Sodikoff contra la preservación que archiva una cultura «en una botella» y produce «arcas congeladas» («Notes», p. 20). Una fuente cerrada es esa botella.
- **Tradujo la obra en parámetros de forma.** Ejes, módulos, alternativas. La obra quedaba como proveedora de formas, y lo que la obra hace (pasar por el agua, cantar, desgastarse) quedaba afuera.
- **Tenía una sola modalidad.** Ver, y un solo uso: componer texto.
- **No le devolvía nada a nadie.** Ni a la obra ni a quienes la hicieron.

Se conserva lo que sí funcionaba: la verificación de las fuentes, la decisión de no imitar la iconografía de Tiwanaku y el cálculo de lo que cada letra contiene.

## 3.2. Qué propone *EthnoGraphemes*

| Idea | Dónde está en la tesis | Qué se toma aquí |
|---|---|---|
| La escritura como vasija que lleva una cultura, no como sistema que se aplica | Resumen y «Confluence» (p. 14) | La pregunta de partida |
| Preservación activa frente a las «arcas congeladas» | «Notes: Active Preservation» (p. 20), a partir de Sodikoff | Ninguna pieza es un producto terminado |
| Transmodalidad: el lenguaje visto, sentido y vivido; lo espacial, el color, el sonido y el tacto, y el cruce entre lo sensible y lo temporal | «Notes: Transmodality»; proyectos *Chromascript* y *Sonic typeface* (p. 42 en adelante) | Una pieza para la luz, una para la voz y una para el tiempo |
| La metalurgia del lenguaje: la letra como mineral que se funde en aleaciones y vuelve a su materia | «Notes: Metallurgy of Language?» | La placa de aluminio como soporte de la voz |
| Objetos especulativos: Dunne y Raby; Morehshin Allahyari, que reconstruyó en impresión 3D piezas destruidas en Mosul; Jane Bennett, para quien las piedras y los fósiles no son materia muerta | «Notes: Speculative Objects» y «Speculative objects» en *Ellipsis* (p. 154) | La cadena, que reconstruye y vuelve a perder |
| Inmersión y diálogo: el viaje a la aldea sora, las listas de palabras con los mayores, las grabaciones y los escaneos 3D | «My journey» (p. 120) | Lo que falta hacer, ahora con la gente de la obra (§ 3.6) |
| Un método en cuatro momentos: inmersión; juego, experimentación e investigación; producción. En el medio, el diálogo y las herramientas compartidas | Esquema de *Ellipsis* (p. 154), a partir del taller Oax-i-fornia | § 3.6 |
| *Ellipsis*: «no son proyectos, sino espacios abiertos», que quedan siempre sin terminar | *Ellipsis* (p. 154) | El estado de las tres piezas |

### Tres entrevistas que importan aquí

- **Tim Brookes** (p. 30) dice que las mayúsculas latinas vienen de los monumentos y encarnan valores de permanencia y estabilidad. La obra hace lo contrario: cambia el asperón del monumento por aluminio de cocina. La traducción tipográfica tiene que abandonar también esos valores y preferir el temblor, el ciclo y el agua. Brookes cuenta además que las mujeres amazigh mantuvieron vivo el tifinagh en joyas y tatuajes. Eso importa en un estudio de tatuajes (§ 3.5).
- **Wael Morcos** (p. 102) advierte contra dos maneras de diseñar con la escritura de otros. Una corta y gira letras latinas para que parezcan de otra escritura: la tipografía «Frankenstein», en palabras de Nadine Chahine. La otra, que él llama «Aladino», le agrega al latín pinceladas y adornos que fetichizan lo que uno cree que es la otra cultura.
- **Agyei Archer** (p. 252) recomienda mostrar el trabajo como propuesta y no como solución, y trabajar por pasos para que la gente pueda opinar.

## 3.3. El cruce con la obra

*Contener una ruina* ya trata de una vasija que no retiene: la piscina vacía, el vaso del monolito, el recipiente que chorrea sobre la boca. La tesis advierte contra la botella que guarda una cultura quieta. Las dos cosas empujan en la misma dirección: aquí la letra no puede quedar guardada. Solo existe de paso: por el agua, por la voz, por el desgaste. Cada pieza es una de esas travesías.

## 3.4. Las piezas

Están en `vasijas/` y se abren en cualquier navegador, sin servidor. Eran tres; con la foto de espalda se sumó una cuarta.

### Tocas el agua (luz y agua) · `vasijas/agua.html`

- **De la obra:** el proyector que apuntaba a una bandeja con un dedo de agua. La imagen rebotaba temblando hasta la pared de azulejo, teñida de verde. Cuando Rebeca tocó el agua, su imagen se deformó con ecos.
- **Qué hace:** el poema nunca se muestra directo. Llega como luz refractada por una superficie de agua simulada y cae sobre una pared de azulejos. Tocar la imagen perturba el agua y la letra se deforma con estela. Cada estrofa entra atravesando el agua; el ciclo sigue solo, con gotas que caen solas.
- **Cómo está hecha:** una simulación de onda de 240 × 150 celdas y un sombreador WebGL que desplaza la imagen del texto según la pendiente del agua. Las cáusticas salen de la curvatura. El eco es una imagen que se realimenta.
- **Qué se puede hacer con ella:** en pantalla completa se puede proyectar en la piscina.
- **Con los videos:** la luz no atraviesa el agua, rebota en ella. La imagen llega a la pared en trapecio, con el reflejo de la lámpara encima, y la bandeja muestra abajo la misma imagen, más débil. La pieza ahora reproduce esa geometría, y el botón «Proyectar un video tuyo» pasa cualquier video por el agua sin que el archivo salga de la computadora.

### La voz sobre la placa (voz y metal) · `vasijas/placa.html` y `vasijas/placa/`

- **De la obra:** el canto de timbre sepulcral que se oye pero no se entiende, y las placas de aluminio del traje. «De la boca sale un signo / hecho con las manos, / ninguna palabra».
- **Qué hace:** en 1787 Ernst Chladni esparció arena sobre una placa de metal y la hizo sonar con un arco; la arena se juntó en las líneas donde la placa no vibra. Aquí cada letra es un modo de vibración de una placa cuadrada de aluminio. Escribes una palabra o eliges una estrofa. La placa la canta con una voz grave y la arena dibuja cada signo.
- **Cómo está hecha:**
  - Las letras más frecuentes del castellano tienen los modos más simples y más graves. Un texto corriente es un canto bajo.
  - Las vocales suenan con los formantes de su vocal; las consonantes llevan aliento.
  - Cada letra muestra una palabra del poema que empieza con ella. La g, la j, la k, la ñ, la w, la x y la z no tienen ninguna: el poema nunca empieza una palabra con ellas.
- **Placa:** la escritura de esas figuras, como fuente (`placa/Placa.ttf` y `.woff2`, 47 glifos).
  - Cada glifo es la franja donde la placa casi no se mueve. Por eso la línea engorda donde vibra poco y adelgaza donde vibra mucho, como la arena real.
  - La voz no tiene caja: mayúsculas y minúsculas comparten figura.
  - Una vocal con tilde suena más fuerte y lleva doble borde. El espacio es una placa vacía: un silencio.
  - Filas y columnas quedan a la misma distancia, de modo que un texto en Placa es una pared de azulejos, o un cuerpo cubierto de relieves (`placa/lamina.png`).
- **Por qué importa:** frente al calendario que nadie supo traducir, Placa es una partitura: leerla es cantarla.
- **El canto real:** en los videos, el canto es un zumbido de unos 225 Hz (un la grave) con su octava encima, que oscila unos pocos hercios, y debajo un golpe doble cada dos segundos y medio. `placa/canto.json` guarda solo ese contorno (altura, intensidad y golpes cada 50 ms), no el audio. «Escuchar el canto sobre la placa» lo vuelve a cantar y lo transcribe en la Lámina II: casi todo cae en la figura de la q, la de «quedó». No es que el canto diga q: es que esta escritura lo oye así. También se puede cargar el video o el audio de la obra y la placa lo escucha mientras suena; el análisis se hace en la página.

### La cadena (tiempo y materia) · `vasijas/cadena.html`

- **De la obra:** el texto que escribiste sobre ella. «Una piedra borrada, una fotografía vieja, un dibujo reconstructivo, un escaneo, un repujado en aluminio, un cuerpo, un video, un charco, una pared de azulejo. Cada paso pierde materia y gana luz».
- **Qué hace:** la palabra que escribas recorre nueve pasos.
  1. **Piedra:** se talla en asperón colorado.
  2. **Erosión:** una simulación de gotas de lluvia; el control va de 0 a 123 años, desde 1903.
  3. **Fotografía:** placa de vidrio con luz rasante.
  4. **Lámina:** el dibujante completa lo que la foto no muestra.
  5. **Escaneo.**
  6. **Repujado:** en aluminio.
  7. **Cuerpo:** parches con piel entre uno y otro.
  8. **Agua.**
  9. **Pared:** de azulejo.

  **Otra vuelta** parte de la pared y no de la piedra, así que ninguna vuelta repite a la anterior.
- **Qué se puede hacer con ella:** series para risografía, o una secuencia de proyección.
- **Con una foto:** «O una foto» convierte una imagen propia en la piedra de la primera vuelta.

### Espalda (cuerpo y página) · `vasijas/espalda.html`

- **De la obra:** la foto de espalda. Las placas de aluminio no cubren el cuerpo: lo marcan en ocho lugares, con piel entre una y otra.
- **Qué hace:** las ocho placas son marcos de texto enlazados. El poema entra por la placa grande del centro y sigue por los hombros, los brazos y la cintura, en el orden en que se lee un cuerpo. Lo que no cabe se derrama por debajo. Cada placa se repuja con su parte del texto, y «Revés» la muestra como la ve la mano que la trabaja.
- **Cómo está hecha:** el contorno de cada placa se tomó de la foto, en sus coordenadas. De la foto se usó solo la disposición; la imagen no está en la página. Contenedor corta por palabras; Placa, en cualquier signo, y tiene su propio tamaño para que el poema recorra las ocho placas.

## 3.5. Otras vasijas posibles (no hechas)

| Vasija | Propuesta | Necesita |
|---|---|---|
| Cuerpo | Repujar de verdad las placas que Espalda compone y ponerlas sobre un cuerpo que se mueve. El repujado se trabaja por el revés, así que la letra se dibuja invertida, como en un tipo de imprenta | A Rebeca y a CreaciónxAcuerpamiento |
| Sitio | Azulejos de cerámica con signos de Placa, sueltos en el fondo de la piscina como las baldosas oscuras que se leían como peces | Un taller de cerámica y permiso del edificio |
| Piel | Una hoja de tatuajes con signos de Placa para Artefacto Tatuajes, el lugar donde los signos se inciden en la piel | El estudio |
| Archivo | Contenedor (§ 1 y § 2) queda como la letra del archivo: la matriz de las máquinas que registran | Nada; ya está |

## 3.6. Cómo seguir

Es el esquema de la tesis aplicado a este caso.

1. **Inmersión.** Ya tienes la tarde en el patio, el poema, el dibujo, las fotos y los videos. Falta el escaneo de la lámina.
2. **Diálogo.** Con Rebeca Paz y CreaciónxAcuerpamiento; con quienes estuvieron esa tarde (uno escribió que la pieza lo devolvió a «nuestro envase convulso: el cuerpo»); y con hablantes de aimara, para todo lo que toque la lengua.
3. **Experimentación.** Las cuatro piezas, y las que salgan de probarlas con esa gente.
4. **Producción.** Proyección en la piscina, risografía, placas repujadas, azulejos. La tesis pregunta si el modelo puede seguir funcionando sin el diseñador; aquí cada pieza debería poder quedarse con quien la use.

## 3.7. Cuidados

- **No imitar la iconografía de Tiwanaku.** Se traducen procesos, no motivos. Ninguna pieza nueva copia el signo «pez» ni el escalonado. Queda uno de la primera versión: el calderón (¶) de Contenedor es el signo escalonado (§ 2). Ruina lo cambia por un calderón de imprenta dibujado en la retícula.
- **Las fotos, los videos y el audio son de la obra.** No se incrustan en las páginas ni se suben al repositorio. Se usan datos derivados (el contorno del canto, la disposición de las placas) y cargadores locales: quien tenga los archivos puede abrirlos en las piezas, y no salen de su computadora.
- **La obra es de Rebeca Paz.** Antes de mostrar esto afuera, conviene enseñárselo, preguntarle y acreditarla. Archer lo dice así: mostrarlo como propuesta y por pasos.
- **Nombrar es otra manera de enterrar.** Lo dice el poema, y por eso ninguna pieza se llama Kochamama.
- **Tu lugar es el de espectador.** Como la autora de la tesis frente a la escritura sora, estás afuera de la obra que traduces. Conviene decirlo en cualquier texto público.

## 3.8. Qué haría falta de ti

- El escaneo de la lámina de Posnansky, para el pie textual (§ 1).
- Hablar con Rebeca, y mostrarle las piezas antes de publicarlas.
- Los otros cinco libros técnicos, que siguen sin llegar. Si son los seis cuadernos de *A Typographic Quest*, de Carl Dair, sirven también para cotejar las páginas que cita el marco (§ 4).

## 3.9. Lo que trajeron las fotos y los videos

| Material | Qué mostró | Dónde entró |
|---|---|---|
| Videos de la proyección | La luz rebota en la bandeja, no la atraviesa. La imagen llega en trapecio, con el reflejo de la lámpara, y la bandeja repite la imagen más débil | Tocas el agua |
| Audio de los videos | Un zumbido de unos 225 Hz con su octava, que oscila unos pocos hercios, y un golpe doble cada dos segundos y medio | La voz sobre la placa (`placa/canto.json`, Lámina II) |
| Foto de espalda | Ocho placas separadas por piel, no un traje entero | Espalda |
| Las otras dos fotos | Una placa repujada sola, sobre negro, y otra apoyada contra la pared de azulejos, sobre las baldosas chicas del piso. El relieve del aluminio tiene los bordes blandos, con brillo de un lado y sombra del otro | Ruina: el eje de repujado y la retícula (§ 4) |

Nada de ese material está en el repositorio ni en las páginas publicadas (§ 3.7).
