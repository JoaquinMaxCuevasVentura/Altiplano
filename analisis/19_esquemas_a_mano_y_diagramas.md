# 19. Tus esquemas a mano y dos diagramas para el artículo

El 30 de septiembre de 2026 enviaste cinco esquemas dibujados a mano y pediste tres cosas:

- analizarlos en detalle;
- ponerlos a trabajar donde de verdad hagan falta en el artículo;
- seguir la misma estrategia que con las ilustraciones: primero una herramienta para dibujar esquemas con trazo de boceto, después el dibujo.

**En corto:**

- **Qué tienen en común las cinco referencias:** son notaciones, no ilustraciones. Tienen líneas finas, rótulos a mano pegados a las cosas, flechas con nombre y un solo acento de color o de material. Las cantidades se hacen con marcas pequeñas repetidas (§19.1).
- **De quién parecen.** Tres (18, 20 y 21) parecen de Jorinde Voigt y otra (17) recuerda a Perry Kulper; la 19 no sé de quién es. Confírmalo antes de citarlas.
- **El criterio.** Un diagrama se gana su lugar cuando muestra un mecanismo que el lector tendría que armar leyendo. Si una frase lo dice más rápido, basta la frase (§19.3).
- **Dos lugares lo piden:**
  - la memoria del retorno (§7): **Figura 7**;
  - el argumento de los tres materiales (conclusiones): **Figura 8**.
- **Ya están en el artículo:**
  - con su mención en el texto, su pie y la declaración de IA al día;
  - la extensión queda en **49.485 caracteres**, dentro del rango;
  - las citas se volvieron a comprobar (§19.6).
- **La herramienta queda en el repositorio** (`esquemas/diagramas/`): rough.js para el trazo y la letra Caveat.
- **Para explorar una versión a mano,** hay prompts de GPT Image 2 como los de los pasteles (§19.8). Si los redibujas tú, cambian el pie y la declaración (§19.9).

## 19.1. Las cinco referencias, de cerca

Los números son los de las imágenes que enviaste. Las leí ampliadas por zonas.

**17. Un dibujo especulativo de arquitectura** (recuerda los de Perry Kulper):

- **Qué hay:**
  - un cuarto en perspectiva, con las líneas de construcción a la vista;
  - en el centro, un embudo doble, como un reloj de arena;
  - una línea que baja desde el embudo como un río o una raíz;
  - un óvalo violeta, como un estanque, con una flecha negra curva que indica giro;
  - bandadas de marcas diminutas que viajan y terminan amontonadas en una loma;
  - signos sueltos: una rueda dentada, un átomo, una doble flecha vertical, una barra en zigzag;
  - abajo, un fragmento de edificio en sección, con losas, pequeñas banderas negras y la rueda dentada junto a los niveles.
- **Qué sirve:**
  - **el montón hecho de marcas:** muchas marcas pequeñas hacen una cantidad; no hace falta escribir «mucho»;
  - **el embudo como operador:** algo entra por arriba y sale transformado;
  - **la sección con niveles, rueda y doble flecha:** se lee como la jaula de una mina.

**18. Una notación vertical con pan de oro** (parece de Jorinde Voigt):

- **Qué hay:**
  - tres estaciones apiladas, cada una con elipses en perspectiva, como órbitas, y un objeto al centro: un fragmento de pan de oro con borde rojo, otro alargado con un punto de plata y un disco de plata;
  - una gran espiral que las une;
  - flechas rectas en todas direcciones, con rótulos en alemán en la punta. Leo *Altes Zentrum*, *Neues Zentrum*, *Inneres Zentrum* y *Äußeres Zentrum*: centro viejo, nuevo, interior y exterior;
  - una leyenda escrita a mano en el margen izquierdo, la firma y la fecha.
- **Qué sirve:**
  - **el mismo aparato aplicado a varias estaciones;**
  - **la leyenda al margen;**
  - **un solo material para lo importante:** el oro no es un color, es una materia. En nuestros diagramas cumple ese papel el siena, el color del óxido de hierro y del adobe (paleta de `17`, §17.3).

**19. Un cuaderno a tinta con TIME y SPACE en las esquinas** (no sé de quién es):

- **Qué hay:**
  - decenas de pictogramas pequeños: soles, estrellas, rejillas, espirales, nubes, una torre de tramado;
  - círculos cortados por una recta con la mitad de abajo rayada;
  - un cerro con flechas que caen sobre su cima;
  - secuencias como «A, B, A, B, A, A, A»;
  - escritura casi ilegible y líneas onduladas que lo conectan todo.
- **Qué sirve:**
  - **el eje nombrado con una palabra en el borde,** sin números. La Figura 7 lo usa: su eje dice «tiempo»;
  - **el círculo cortado y rayado:** es la sección más simple que existe;
  - **las flechas que caen sobre la cima:** una manera de marcar un lugar.

**20. Una notación del horizonte** (parece de Jorinde Voigt):

- **Qué hay:**
  - una línea celeste rotulada *Horizont*, con posiciones marcadas (*Position*) y flechas que terminan en una «x»;
  - una gran banda de acuarela rosa;
  - un haz de líneas paralelas que se doblan, numeradas del (1) al (25), algunas de color, como estratos o curvas de nivel;
  - una elipse roja con flecha y la leyenda *Rotationsrichtung, 1 Umdrehung/Min.*, el sentido de giro, una vuelta por minuto;
  - abajo, la leyenda: *Horizont*, *mögliche Farben des Horizonts* (posibles colores del horizonte), *Position*, *Territorium*…
- **Qué sirve:**
  - **el horizonte como una línea que se dibuja,** con posiciones sobre ella;
  - **las flechas que llevan escrito lo que miden.** En la Figura 7, la mirada es una línea de trazos con su cita encima.

**21. Un inventario de objetos en órbita** (parece de Jorinde Voigt):

- **Qué hay:**
  - formas pequeñas de color: un óvalo naranja, una piedra parda con forma de oreja, un higo violeta, una gota roja, un clavo gris y cinco puntos verdes apilados en columna;
  - cada forma, en el centro de sus propias elipses, con un eje vertical y un rótulo;
  - líneas que las unen y convergen a la derecha;
  - a la izquierda, una gran silueta negra, como un edificio con techo, postes y palos cruzados.
- **Qué sirve:**
  - **el mismo aparato aplicado a cosas distintas** compara sin necesidad de un cuadro. La Figura 8 hace eso con tres estaciones idénticas;
  - **la columna de puntos repetidos a distintas alturas** se lee como niveles.

**Lo que las cinco comparten:**

1. Línea fina de grafito o tinta, sin sombras.
2. Rótulos a mano, pegados a las cosas o escritos a lo largo de las líneas.
3. Flechas con nombre y, a veces, con medida.
4. Un solo acento de color o de material.
5. Cantidades hechas con marcas pequeñas repetidas.
6. Una leyenda al margen, escrita a mano.
7. Líneas de construcción que quedan a la vista.
8. Fragmentos de arquitectura, como secciones y niveles, mezclados con signos.

**Una diferencia importante.** Estos dibujos son abiertos: provocan muchos sentidos y ninguno se impone. Un diagrama de artículo tiene que hacer lo contrario: una figura, una afirmación. De ellos se toma el lenguaje, no la ambigüedad.

## 19.2. La skill y la herramienta

- **La skill:** `artifact-diagramming`. Sus reglas, aplicadas aquí:
  - dibujar el mecanismo, no su nombre;
  - poner nombre a las flechas;
  - rótulos cortos; lo que explica va al pie;
  - una rejilla que ordena;
  - una figura, una afirmación;
  - un solo color para lo que importa.
- **El trazo de boceto:** [rough.js](https://roughjs.com) (licencia MIT) dibuja líneas y figuras que tiemblan como a mano alzada.
- **La letra:** Caveat, una letra manuscrita de Google Fonts (licencia OFL), con todos los signos del castellano.
  - Elegí Caveat frente a Architects Daughter, la otra letra probada al tamaño de impresión, porque se parece más a una mano que escribe y ocupa menos ancho.
  - Va incrustada en cada SVG.
- **El programa:** `esquemas/diagramas/generar_diagramas.js`.
  - Las semillas son fijas: si no cambias nada, el dibujo sale igual cada vez.
  - Los montones se arman con piedras, papeles o fragmentos que no se enciman.
  - `articulo/generar_figuras.py` los pasa a PNG de 2.100 px de ancho (unos 380 ppp a 14 cm), con una paleta de 64 colores: cada uno pesa menos de 160 KB.
- **El acento:** el siena de las figuras 1 a 6 (`#b5542b`), solo en lo que carga la afirmación. En gris sigue leyéndose, por si la revista imprime en blanco y negro.
- **La red.** Todo se bajó de npm y de GitHub. No hizo falta el CDN jsdelivr, que el proxy de este entorno bloquea (403).

## 19.3. Dónde hace falta un diagrama y dónde no

La prueba es la de la skill: ¿el lector tendría que armar el mecanismo leyendo? Si una frase lo dice más rápido, basta la frase.

| Lugar del artículo | Qué tendría que armar el lector | Decisión |
|---|---|---|
| §7, la memoria del retorno | Muralla, foso, atalaya y horizonte; quién vuelve y quién no; la pirca de doble cara con su relleno | **Figura 7** |
| Conclusiones, los tres materiales | La misma operación en el ayllu, la aldea y la mina, repartida en §§1, 3, 4 y 5 | **Figura 8** |
| El Signo Escalonado en cinco lugares | La escalera en el ayllu, la aldea, el cocal, el campamento y el retorno | En reserva: la frase del segundo hallazgo basta y la Figura 2 ya dibuja el Signo |
| Las palabras de piedra de Bertonio | *wanqa*, *chhaxwa*, *saywa*, *achachi*, *apachita*, *jayintilla* | En reserva: es un inventario; si hiciera falta, sirve más un cuadro |
| Zavaleta: archipiélago frente a cercado | Dos maneras de concebir el suelo | En reserva: dos frases lo dicen; entra si un árbitro pide más en §2 |
| Las manos y sus agarres | Arar, firmar, apoyar la huella, quitarse la vida | No: es una lista, no un mecanismo |
| §4, el radio urbano y el embudo | La ordenanza que encierra, el embudo que convierte animales en papel | Ya entra en la Figura 8 |

**La numeración no cambia.** Los diagramas aparecen después de las seis figuras (en §7 y en las conclusiones), así que son la 7 y la 8.

## 19.4. Figura 7. *La memoria del retorno*

**La afirmación.** Desde la atalaya, la mirada pasa por encima de la muralla y del foso y llega al horizonte. La muralla es una pirca de doble cara: las caras son los apellidos que vuelven; el relleno, los sin tierra. En el foso quedan los muertos del hambre.

**Qué dibuja,** de izquierda a derecha, con la página de cada cosa:

- **La atalaya de la esperanza** (p. 157), con los comunarios arriba.
- **La mirada:** «sólo miraban el horizonte» (p. 157), una línea de trazos a la altura de los ojos.
- **La muralla de su visión** (pp. 156-157), dibujada como pirca de doble cara:
  - las caras son los apellidos que vuelven: «los Villca, los Huanca, los Huallpa, los Yupanqui, los Ticona, los Choque, los Chuquihuanca» (p. 156);
  - el relleno, en siena, es la «legión» de los Condori, Mamani y Quispe (p. 22) y los tres vigilantes (p. 75).
- **La mirada que no baja:** «sin atreverse a bajar la cabeza al tremendo hoyo» (p. 157).
- **El foso** «hondo y alquitranado», el intervalo del hambre (p. 157). Adentro, en siena:
  - más de ciento cincuenta muertos, «sin culto y sin recuerdo» (p. 156);
  - Condori, en el cementerio de los mineros (p. 154);
  - Quispe, «en muchos sitios» (p. 69).
- **El horizonte:** la memoria que no recordaba sino «lo pasado antiguo, lo bueno y lo alegre de las cosechas» (p. 156).
- **Un eje de tiempo** abajo: ahora, el hambre, antes del hambre.

**Qué obliga a decidir el diagrama** (el equivalente del plano 3 de las figuras):

- **El orden.** La novela dice «tras la muralla», así que el foso queda más allá del muro, entre los comunarios y el horizonte. Para ver el pasado antiguo, la mirada tiene que saltar el reciente.
- **La distancia es tiempo.** Lo cercano es el hambre; lo lejano, lo de antes. La novela no lo dice con esas palabras. Lo deja ver al poner juntos el foso, el intervalo del hambre y la memoria de lo antiguo.

**Lo que decide el diagrama y no la novela** (lectura del artículo, por eso el pie dice «Diagrama»):

- los muertos en el foso;
- los apellidos en las caras y los sin tierra en el relleno;
- el eje del tiempo.

**Lo que salió del texto** porque ahora lo muestra la figura:

- la frase sobre las tumbas de Condori y de Quispe, que la figura trae con sus páginas;
- «apretadas entre las dos caras».

## 19.5. Figura 8. *Tres montones*

**La afirmación.** El mismo gesto, amontonar, se repite en tres materiales. Cambian lo que entra, lo que sale y para quién. Y en cada lugar alguien queda debajo.

**Tres estaciones con el mismo esquema** (entra → operación → sale; el montón; quién queda debajo):

| | Piedra: el ayllu | Papel: la aldea | Máquina: la mina |
|---|---|---|---|
| Entra | Erial de piedras (p. 9) | Los animales, dentro del radio urbano: ordenanza y firma (p. 96) | «Rieles, maderos, dinamita, hombres» (p. 151) |
| Operación | «Extraen piedras y las amontonan» (p. 9) | El «embudo» (p. 102) | El castillete, el pique y la jaula |
| Sale | «Tierra rescatada», con un «quizá un día» (p. 9) | Los animales, «hasta esfumarse», a las propiedades del Alcalde (p. 102); «mil seiscientos bolivianos en papel» (p. 103), que van al tinterillo (p. 105) | «Miles de cargas de estaño» (p. 142), para la compañía |
| Montón, en siena | «Montaña de piedras» (p. 9), de los comunarios | «Montón de papeles y libracos» (p. 103), del tinterillo | Desmonte, roca sin mineral (p. 140), de la compañía |
| Debajo | Melchora Mamani: «amontonó piedras sobre el cadáver» (p. 35) | Dos guaguas, «bajo el suelo del pesebre» (p. 106) | Juan Condori: «un informe montón de rocas, lodo y maderos astillados» (p. 154) |

**Lo que decide el diagrama:**

- **Los dueños de cada montón** son lectura del artículo: de los comunarios, del tinterillo, de la compañía.
- **La fila de abajo dice «debajo», no «el montón sepulta».** No es el mismo montón:
  - Melchora no está bajo el montón de la cosecha;
  - las guaguas están bajo el suelo del pesebre, no bajo los papeles;
  - Condori queda bajo el derrumbe del 450, no bajo el desmonte.

  Lo que se repite es el lugar donde habitar y enterrar casi no se distinguen (§1).
- **Por qué «debajo» y no «la tumba».** El derrumbe «sepultó a todos ellos» y el lugar quedó cubierto por el «informe montón» (p. 154). Pero tres semanas después la compañía entierra a Condori en el cementerio de los mineros (p. 154). Su tumba es esa; el montón es donde quedó debajo. La palabra «debajo» es exacta en las tres columnas.

**Dónde se menciona:** en las conclusiones, al final del primer hallazgo. Va antes de «¿Qué muestra el dibujo?».

## 19.6. Cómo entraron en el artículo

**Cambios** (marcados en `articulo/articulo_cosecha_de_piedras_cambios.docx` respecto de la versión anterior: 15 cambios):

1. **§7:** «(Figura 7)» después de «recordar es construir, y olvidar también». La figura va al final de ese párrafo.
2. **Conclusiones:** «(Figura 8)» al final del primer hallazgo. La figura va después del párrafo de los hallazgos.
3. **Pies:**
   - «**Figura 7.** *La memoria del retorno*. Diagrama. Fuente: elaboración propia con asistencia de IA.»
   - «**Figura 8.** *Tres montones*. Diagrama. Fuente: elaboración propia con asistencia de IA.»
   - La nota de que los números entre paréntesis son páginas de la novela va dentro de cada figura, porque el texto de la imagen no cuenta en la extensión.
4. **Declaración de IA** (norma 8: el alcance real):
   - las herramientas son ahora «asistentes de IA generativa»;
   - el final dice «y la codificación vectorial de los esquemas de encaje (figuras 1-6) y el diseño y trazado de los diagramas (figuras 7 y 8)». Los diagramas los propuso y trazó la IA; tú decides si entran.
5. **Recortes** para caber:
   - la frase sobre las tumbas de Condori y de Quispe (ahora en la Figura 7);
   - «apretadas entre las dos caras»;
   - «justamente» (§1);
   - «es un conjunto de» por «reúne» (§2, Zavaleta);
   - «de dos metros de alto» y «de las vigas» en el plano (1) de la Figura 1, que repetía el párrafo anterior.

**Comprobaciones:**

- **Extensión:** 49.485 caracteres (antes, 49.472). Quedan 15 de margen.
- **Resúmenes:** 99 y 90 palabras.
- **Citas de la novela:** 147, todas en su página, sin problemas. Hay una menos porque salió la repetición de «en muchos sitios»; la cita sigue en §6.
- **Citas de las demás fuentes:** igual que antes. Solo la de Cornejo Polar queda como coincidencia aproximada, ya conocida.
- **Cadenas de «ibid.»:** todas remiten a la obra correcta, también la que sigue a la Figura 8.
- **El Word:** tiene 24 páginas (antes, 23). Las figuras quedan a 14 cm de ancho y los rótulos, cerca de 7 puntos, legibles en la página impresa.

## 19.7. Cómo cambiarlos

1. **Para cambiar un rótulo o una posición,** edita `esquemas/diagramas/generar_diagramas.js`. Cada figura tiene su función y los rótulos están en castellano, a la vista.
2. **Después, corre en este orden:**
   - `node analisis/esquemas/diagramas/generar_diagramas.js`, que escribe los SVG;
   - `python3 articulo/generar_figuras.py`, que escribe `figura_7.png` y `figura_8.png` (y rehace las demás, que no cambian);
   - `python3 articulo/generar_docx.py`, que rehace el Word.
3. **Si vas a abrir los SVG en Illustrator o Inkscape,** instala antes la letra: `esquemas/diagramas/fuentes/Caveat-Regular-sub.ttf`, o la familia completa de Google Fonts.

## 19.8. La misma estrategia que con los pasteles: explorar con GPT Image 2

Es opcional, y sirve igual que con los pasteles: ver qué propone la IA antes de dibujar tú. Lo que genere no se publica.

**Qué adjuntar:**

- **la figura** (`figura_7.png` o `figura_8.png`) como guía;
- **una o dos de tus referencias** como estilo: la 20 o la 21 para la notación, la 17 para la arquitectura.

**Cuidado con las referencias:**

- son obras de otros artistas: sirven para mirar, no para copiar;
- no nombres a nadie en el prompt; el modelo imitaría a esa persona y no a ti (lo mismo que en `17`, §17.1).

**Bloque de estilo:**

> Dibujo de notación hecho a mano sobre papel de algodón blanco, sin sombras. Línea fina de grafito, algo temblorosa; rótulos pequeños escritos a mano, pegados a las cosas o a lo largo de las líneas; flechas finas con punta abierta. Las cantidades se hacen con marcas pequeñas repetidas, no con números. Un solo acento de color: pigmento siena de óxido de hierro, en lo más importante. Las líneas de construcción quedan a la vista, muy suaves. Usa la imagen adjunta como guía exacta de la composición: conserva la posición de cada elemento y copia sus rótulos palabra por palabra; si no puedes escribirlos bien, deja en su lugar una línea en blanco. Toma de las imágenes de estilo solo la manera de trazar. Nada de aspecto digital ni de infografía.

**Figura 7:**

> Una sección de terreno vista de lado. A la izquierda, una torre de piedras apiladas con siete figuras mínimas arriba, que miran a la derecha. Una línea de trazos sale de sus ojos y cruza todo el dibujo hasta una marca vertical en el borde derecho: el horizonte. En el medio, un muro de doble cara: dos columnas de piedras grandes y, entre ellas, un relleno de piedras menudas en siena. Más allá del muro, un foso hondo cavado en el suelo, rayado en cruz como alquitrán, con rótulos en siena adentro. Desde la línea de la mirada, una línea de puntos baja hacia el foso y se detiene en una barra corta: la mirada no baja. Abajo, un eje de tiempo con tres marcas.

**Figura 8:**

> Tres columnas iguales separadas por líneas de puntos, con un título grande a mano sobre cada una: PIEDRA, PAPEL, MÁQUINA. En cada columna, arriba, lo que entra y lo que sale, unidos por flechas con nombre: en la primera, piedras sueltas y un suelo arado; en la segunda, un círculo trazado con compás con animales dentro, un embudo y billetes que caen; en la tercera, una torre de mina con rueda, un pique y una jaula. En el medio de cada columna, un montón del mismo tamaño y la misma silueta, dibujado en siena con muchas piezas pequeñas: piedras redondeadas en la primera, hojas de papel y libros en la segunda, fragmentos angulosos de roca en la tercera. Abajo, bajo una línea fina, tres rótulos: quién quedó enterrado en cada lugar.

**Qué mirar en lo que salga:**

- ¿El mecanismo se lee antes que los rótulos? Si no, sobran adornos.
- ¿El acento siena cae donde está la afirmación (el relleno y el foso; los tres montones) o se reparte por todo el dibujo?
- ¿La belleza del trazo tapa lo que se dice? Es el mismo riesgo que con los pasteles (`18`, §18.2.4).
- **Los rótulos que invente el modelo no valen:** cada palabra y cada página tienen que venir de las figuras.

## 19.9. Si los redibujas a mano

1. **Materiales:**
   - grafito HB o 2H para la línea;
   - un solo acento siena: pastel, sanguina o tierra de siena;
   - mejor sin pan de oro: embellece, y el artículo desconfía de embellecer (conclusiones, segundo límite).
2. **Medida:** a 14 cm de ancho, las letras necesitan unos 2,5 mm de alto para leerse. Conserva las páginas entre paréntesis.
3. **Pie:** «Diagrama. Fuente: elaboración propia con asistencia de IA» pasa a algo como «Diagrama a mano, grafito y pastel sobre papel, 2026. Fuente: elaboración propia».
4. **Declaración de IA:**
   - si sigues la composición que propuso la IA, sale «y trazado» y queda «el diseño de los diagramas»;
   - si los rediseñas, sale la mención entera de los diagramas.
5. **Extensión:** regenera el Word y comprueba que siga entre 47.500 y 49.500 caracteres.

## 19.10. En reserva

- **El Signo Escalonado en cinco lugares:** cinco escaleras pequeñas iguales, con el último escalón vacío en la del retorno. Entra si un árbitro pide mostrar el segundo hallazgo.
- **Zavaleta:** el archipiélago (puna y valle unidos, dos pisos de una tierra) frente al cercado heredado, con la «muralla que condena el horizonte» (p. 108) cortando la unión. Encajaría en §2 o en §5.
- **Las palabras de piedra de Bertonio:** mejor como cuadro que como diagrama.

## Fuentes consultadas en la web

- Jorinde Voigt, artista de Berlín: notaciones con líneas, diagramas, símbolos y notas a mano sobre el espacio, el tiempo, la rotación o el horizonte, con pan de oro o de cobre, grafito, tinta y pastel: https://en.wikipedia.org/wiki/Jorinde_Voigt · https://www.marcselwynfineart.com/exhibitions/jorinde-voigt · https://www.sicardi.com/artists/jorinde-voigt · https://www.themorgan.org/drawings/item/374658
- Perry Kulper, arquitecto y profesor en la Universidad de Míchigan: dibujos que superponen mapas, símbolos y trazado arquitectónico: https://drawingmatter.org/perry-kulper/ · https://architecturenow.co.nz/articles/idea-building/ · https://www.researchgate.net/publication/347669982_Layering_in_representation_Rethinking_architectural_representation_through_Perry_Kulper's_works
- rough.js: https://roughjs.com (código: https://github.com/rough-stuff/rough, licencia MIT).
- Caveat: https://fonts.google.com/specimen/Caveat (licencia SIL Open Font License).
