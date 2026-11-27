# Las cinco exploraciones

27 de noviembre de 2026. De la exploración formal (`exploracion_formal.md`) salieron cinco obras que el autor eligió y que juntan las técnicas de las cinco pruebas. Las pruebas miden una técnica cada una. Las exploraciones son lo que se construiría con ellas.

| N.º | Exploración | Viene de | Pasaje de la novela |
|---|---|---|---|
| E1 | La montaña habitada | Las formas 1B y 1C | La «montaña de piedras» (p. 9) |
| E2 | El corral techado | Las formas 2C y 5C | Las pircas «compuestas» (p. 156) |
| E3 | La torre de champa | La referencia R8 y la pieza 3h | El «dintel de Jatun-Kolla» (p. 155) |
| E4 | La chullpa | La pieza 3h, con la nota del autor | La «tumba agreste y anónima» (p. 154) |
| E5 | La casa de la bóveda | La referencia R16 | Las *chujllas* «rectangulares y chatas» (p. 30) |

Las páginas son de la novela (Botelho Gosálvez, 1982 [1945]). Los pasajes de E3, E4 y E5 los propuso Claude y los decide el autor.

## Cómo se cruzan con las pruebas

| | 1. La cosecha | 2. El relleno | 3. El dintel | 4. La *p'ira* | 5. El fogón |
|---|---|---|---|---|---|
| E1 | ● toda la piedra | | ● la cámara volada | | ○ se entra en cuclillas |
| E2 | ○ la piedra de la pirca | ● la pirca de doble cara | | ○ el techo de ichu | |
| E3 | ○ un apoyo es un montón | ○ el otro es una pirca | ● la V volada | ● las fajas y la *chhaxwa* | |
| E4 | ● las pilas de piedra | | ● las pilas y la cámara voladas | ○ la cornisa de ichu | |
| E5 | | ● los muros de doble cara | ● la bóveda volada | | ● el fogón, el humo y el *t'uju* |

● es la técnica principal de la obra; ○, una que también usa.

Tres cosas atan las cinco obras.

- **Una sola cosecha.** Todas usan la misma piedra, la angulosa que sale de despedregar el campo, y no traen otra. La tierra es la del lugar, y la paja es el ichu de la puna. La madera se reduce a palos cortos de queñua, porque en el altiplano no hay árboles: Squier lo dice al hablar de los puentes de champa, «The absence of wood and timber has led the people of the Sierra to adopt a great many novel and striking devices» (Squier, 1877: 313).
- **Lo que cierra arriba se vuela.** Donde no hay vigas, lo que cubre un espacio se hace volando hiladas, que es la técnica de la prueba 3. Así se cierran la cámara de E1, la V de E3, las pilas y la cámara de E4 y la bóveda de E5. Las chullpas se cubrían igual. Sobre la de Palca, Squier escribe que «A rude arch of converging and overlapping stones, filled in or cemented together with clay, was raised over this cist» (ibid.: 243), y en la cámara de la de Acora, «the stones begin to overlap, forming a kind of pointed arch» (ibid.: 353).
- **El cuerpo como medida.** Se entra en cuclillas a E1, de pie y por un paso estrecho bajo E3, agachado bajo E4 y de lado por la ranura de E5. La boca de la chullpa mide lo que medía la de Palca, «about eighteen inches wide and high» (ibid.: 244).

El orden va del campo a la casa: el montón que deja la cosecha, la pirca que la ordena, el umbral del *ayllu*, la tumba y el fuego. El título se cumple en dos de ellas. E1 es la *chhaxwa* de los montones de la chacra, y en E3 los palos del techo se atan a piedras hincadas en el muro, que es la otra *chhaxwa* de Bertonio (2011 [1612]: 330).

Las cinco son maquetas de estudio a 1:20, modeladas en Blender (`blender/formas.py`), con un corte de cada una y la serie a la misma escala (`blender/diagramas.py`). En las tablas, «proyecto» marca una decisión que se comprueba o se cambia al construir, y «cálculo», una cifra que sale de una cuenta.

## E1. La montaña habitada

Toda la piedra de la cosecha en un cono bajo y hueco. Por dentro, una cámara redonda de muros verticales que, desde un metro de alto, vuelan hilada sobre hilada hasta dejar un óculo arriba. Se entra en cuclillas por una caja de queñua que atraviesa el muro por el sur.

| Medida | Valor | Origen |
|---|---|---|
| Diámetro al pie y alto | 7,2 m y 2,6 m | Proyecto (la elección del autor: el cono de 1B, más chato) |
| Cámara | 2,8 m de diámetro; vertical hasta 1 m, después vuela 13,5 cm por hilada de 20 cm | Proyecto |
| Óculo | 64 cm | Proyecto |
| Boca | 0,9 × 1,0 m, forrada de queñua | Proyecto (la entrada de 1C) |
| Piedra | Unos 28 m³ | Cálculo: el cono menos la cámara, sin contar los huecos |

La prueba 1 dice cuánta piedra da una parcela de 2 × 2 m, y con eso se sabrá cuántas parcelas hay que despedregar para levantar la montaña.

## E2. El corral techado

Un corral redondo de pirca de doble cara, con relleno de piedra menuda, abierto al sur. Encima, sin tocarlo, un cono de ichu sobre ocho palos de queñua. Entre la piedra y la paja queda una franja de cielo de 90 cm.

| Medida | Valor | Origen |
|---|---|---|
| Corral | 6 m de diámetro; pirca de 0,7 m de espesor y 1,4 m de alto | Proyecto |
| Relleno | La mitad del corte | La regla de la prueba 2 |
| Entrada | Un cuarto de la vuelta, al sur | Proyecto |
| Palos | Ocho, de 2,3 m | Proyecto |
| Techo | Cono de ichu de 6,8 m de diámetro y 3,4 m de alto | Proyecto (el techo de 5C) |

El autor eligió el cono. La versión con techo de pirámide (`renders/render_forma_E2P.jpg`) queda como registro. Falta decidir si bajo el ichu va una capa de *p'ira*, como en Enquelga (Šolc, 2011 [1975]: 105-109), lo que pondría la prueba 4 en esta obra.

## E3. La torre de champa

Es una interpretación de la referencia R8, una torre de tablas apiladas sobre dos apoyos de piedra, con los materiales del proyecto. Las tablas se vuelven hiladas delgadas de champa, el bloque de tierra con raíces que se corta del suelo. En la desembocadura del Ramis, Squier vio que con ella se hacían «their dwellings and the corrals», y que esas casas parecían «tall quadrilateral hay-stacks» (Squier, 1877: 391).

- **Los dos apoyos** son las dos maneras de poner la piedra de la cosecha. Uno es una pirca, la piedra ordenada de E2, y el otro un montón, la piedra suelta de E1. Arriba de cada uno, una cama de lajas.
- **La V** entre los dos apoyos se hace volando las hiladas de champa, como en los puentes de champa que Squier vio camino a Copacabana, donde cada capa vuela sobre la de abajo «until the upper ones touch and brace against each other, forming a rude kind of arch» (ibid.: 313). Por ahí se pasa por debajo de la torre, y ese paso es el umbral.
- **Las lajas pasantes** atraviesan el muro, traban las hiladas y asoman por fuera, como las tablas sueltas de la referencia.
- **El techo** es de un agua, con fajas de *p'ira* (Šolc, 2011 [1975]: 105) sobre seis palos de queñua de lado a lado. Cada palo se ata a una piedra hincada en el muro debajo de su extremo, la *chhaxwa* «hincada en la pared para atar en ella los palos del techo» (Bertonio, 2011 [1612]: 330).

| Medida | Valor | Origen |
|---|---|---|
| Planta de la torre | 3,0 × 1,6 m | Proyecto |
| Alto | 4,2 m del lado bajo y 5,4 m del alto | Proyecto |
| Apoyos | 0,9 m de alto; una pirca y un montón | Proyecto |
| Bloque de champa | 40 × 25 × 12 cm | Proyecto (el de la prueba 3) |
| La V | Siete hiladas que vuelan 6 cm cada una; la clave queda a 1,8 m del suelo | Cálculo |
| Paso entre los apoyos | 1 m arriba y medio metro al pie, donde se abre el montón | Proyecto |
| Fajas de *p'ira* | 2,5 × 0,7 m, en dos hileras traslapadas | Šolc (2011 [1975]: 105) |
| Pendiente del techo | Unos 22° | Cálculo |

La champa se deja secar unos veinte días antes de usarla (Vitulas-Quille y Reynoso-Machaca, 2025: 9). Si una torre de champa de más de cinco metros se sostiene es lo primero que hay que probar, y la prueba 3 empieza por ahí.

## E4. La chullpa

Una chullpa levantada del suelo. Cuatro pilas de pirca cuyas dos últimas hiladas vuelan hacia los pasos, una cama de lajas que los cruza, una hilada de piedra que separa el adobe del suelo y, encima, una pirámide escalonada de adobitos puestos de pie. Cerca de la cima, una cornisa de ichu prensado. La boca es baja y mira al este. Por dentro, una cámara de adobe volada. Por debajo se pasa agachado, entre las cuatro pilas.

El autor pidió que la base fuera de piedra, y no de madera, y que la pirámide fuera de adobe con aparejo vertical. Casi todo lo demás sale de la chullpa que Squier describió cerca de Palca, junto a un camino «from the coast to the interior» (Squier, 1877: 244):

- tenía 16 pies de alto, unos 4,9 m, la altura de esta;
- tenía «a cornice or projection of four inches, and of about six inches in vertical thickness, formed by a layer of compacted ichu, or coarse mountain grass, placed horizontally, and cut off evenly as by a shears»;
- estaba asentada en una plataforma «of roughly hewn stones» (ibid.: 243);
- su boca miraba al este, al nivel de la plataforma (ibid.: 244).

Squier también vio que las casas de champa del Ramis tenían «a kind of cornice at the point where the roof begins to converge from the vertical walls», y pensó que venía de las chullpas (ibid.: 392). La cornisa de ichu une la tumba con la casa.

**El aparejo de librero.** Los adobitos van de pie, como libros en un estante. Agüero Benites y otros citan a la arqueóloga Isabel Flores, para quien la técnica de la Huaca Pucllana «consiste en colocar los adobitos en posición vertical, con la argamasa sólo en la parte superior e inferior, sin ponerla entre los adobes» (Flores, cit. en Agüero Benites et al., 2015: 3). En su muro de ensayo dejaron «un espacio libre de 1,5 cm aproximadamente entre cada uno de los bloques» (ibid.: 6). Es una técnica de la costa, de la cultura Lima. El mismo texto recuerda que los antiguos peruanos «construían con adobe en la costa y casi exclusivamente con piedra en la sierra» (Gallegos, cit. en ibid.: 3). En esta chullpa, el adobe de la costa va encima de la piedra del altiplano. Es una decisión del autor, y el texto lo dice.

| Medida | Valor | Origen |
|---|---|---|
| Base | 3,3 × 3,3 m; cuatro pilas de 1,2 × 1,2 × 1,2 m | Proyecto |
| Pasos entre pilas | 0,9 m al pie y 0,5 m arriba, donde vuelan dos hiladas de 10 cm | Proyecto |
| Alto total | 4,9 m | Squier (1877: 243): 16 pies |
| Pirámide | De 3,0 a 1,1 m de lado, en quince hiladas | Proyecto |
| Adobito | 19 × 14 × 6 cm, de pie | Proyecto |
| Separación entre adobitos | 1,5 cm | Agüero Benites et al. (2015: 6) |
| Cornisa de ichu | 15 cm de alto; vuela 10 cm | Squier (1877: 243): seis y cuatro pulgadas |
| Boca | 48 × 42 cm, al este, con una laja de dintel | Squier (1877: 244): dieciocho pulgadas |
| Cámara | 1,0 × 1,0 m; vertical tres hiladas y volada cuatro | Proyecto |

**Una tumba.** «Chulpa is the Aymara word for tomb», escribe Squier (1877: 354). La novela no nombra las chullpas, pero tiene dos muertes sin sepultura del *ayllu*. Condori queda bajo «la tumba agreste y anónima» de la mina (Botelho Gosálvez, 1982 [1945]: 154), y los que murieron en el éxodo, «abandonados en el cobijo de las tumbas de otras tierras, se pudrieron sin culto y sin recuerdo» (ibid.: 156). La chullpa sería la tumba que les faltó. Es una lectura que decide el autor.

## E5. La casa de la bóveda

La casa de Enquelga dentro de un bloque de pirca en talud. El cuarto tiene la planta de la mediana de Šolc, 5,75 × 3,30 m (2011 [1975]: 93-94). Los muros son de pirca de doble cara, como en la prueba 2, y hasta 80 cm de alto son verticales por dentro. Desde ahí arranca una bóveda de adobe por aproximación de hiladas, que vuela poco al principio y más cerca de la clave, hasta que las dos mitades quedan a 30 cm y se cierran con lajas. Falta una laja sobre el fogón, y por ahí sale el humo. Los riñones de la bóveda se rellenan con tierra hasta 2,1 m, para cargar las colas de las hiladas. La pirca sigue hasta 2,6 m como un parapeto, y la bóveda queda adentro, como en la referencia R16.

Se entra por una ranura de 50 cm en el muro del este, el ancho de un cuerpo. La puerta mide 1,30 m de alto, y sobre ella la ranura se cierra con un tímpano de adobe. La puerta al este sigue a la casa grande que describe Suárez Jordán (1990: 130). El *t'uju*, un tubo de 15 cm, atraviesa la esquina noreste apuntado al sol del 21 de junio a las 10, cuando está a 35° de altura y 44° de acimut (prueba 5).

| Medida | Valor | Origen |
|---|---|---|
| Cuarto | 5,75 × 3,30 m | Cálculo: mediana de 17 dormitorios de Šolc (2011 [1975]: 93-94) |
| Bloque | 7,55 × 5,10 m al pie y 2,6 m de alto | Proyecto |
| Muros | 0,9 m al pie, en talud de 10° por fuera | Proyecto |
| Bóveda | Arranca a 0,8 m; cada hilada de 11 cm vuela de 7 a 13 cm; la clave queda a unos 2,6 m | Proyecto y cálculo |
| Adobe | 40 × 20 × 10 cm, a tizón | Proyecto |
| Ranura y puerta | 50 cm de ancho; la puerta, 1,30 m de alto | Proyecto |
| *T'uju* | 15 cm, al noreste | Yampara Blanco (2019: 13); tabla del sol de la prueba 5 |

La novela dice que las *chujllas* «apenas se alzan dos metros del suelo» (p. 30). Esta casa los pasa, porque una bóveda volada sobre 3,30 m de luz necesita casi dos metros de alto, y el bloque llega a 2,6 m. Si se quiere la casa chata, hay que bajar el arranque o angostar el cuarto, y eso lo decide el autor.

## Una candidata: la casa redonda

El autor mandó una imagen de una casa redonda: una base de piedra, una cúpula de tierra en anillos escalonados, ichu arriba y una puerta angosta. Preguntó qué opinaba. Se le respondió que la técnica tiene fuentes, pero que tenía cuatro problemas: la piedra era de río, la puerta no tenía dintel, el ichu tapaba la salida del humo y las gradas de tierra juntaban el agua de la lluvia. Pidió corregirla y analizar a cuál de las cinco podría reemplazar. La imagen no está en el repositorio, porque no se sabe de dónde viene. Si es de un generador de imágenes, sirve solo como boceto (regla 5).

**Es la casa redonda aymara.** Yampara Blanco describe el *muruqu uta*, la «casa de base de forma circular usada cotidianamente», que se usa sobre todo en las épocas de heladas y de lluvia. Su puerta mira al este, tiene un fogón de arcilla al centro y un *t'uju* al noreste, «por donde penetran los rayos solares» y por donde sale el humo (2019: 13). Forma pareja con el *taru uta*, la casa de base cuadrada o rectangular: juntas, «representan simbólica y culturalmente la feminidad y la masculinidad» (ibid.: 9). El putuco de champa, en cambio, suele ser de planta cuadrada (Vitulas-Quille y Reynoso-Machaca, 2025: 5), así que esta casa es redonda como el *muruqu uta*, no como el putuco.

**Las correcciones.** Se modeló en Blender (`blender/formas.py`, forma E6) con estos cambios:

1. **La piedra es la de la cosecha.** La base es una pirca redonda de doble cara, de piedra angulosa, con relleno de piedra menuda (prueba 2).
2. **La puerta lleva dintel.** Mide 60 cm × 1 m, mira al este y la cubre una laja que atraviesa el muro (prueba 3).
3. **El óculo queda abierto.** El ichu se vuelve un sombrero levantado 30 cm sobre tres palos de queñua. El humo sale por los costados y la lluvia no cae de lleno sobre el fogón.
4. **El agua escurre.** La tierra se revoca con barro, y el borde de cada anillo sube hacia adentro para que el agua corra hacia afuera.
5. **La cúpula volada es un cono por dentro.** Esto apareció al modelar. Cada hilada solo puede volar una parte de su largo, así que una cúpula por aproximación de hiladas se cierra en punta, como la cámara de E1. La forma baja y redonda de la imagen es, entonces, un relleno de tierra sobre la cámara volada. Además carga las colas de las hiladas, que es lo que las sostiene.
6. **Se suma el *t'uju*** al noreste, apuntado al sol del 21 de junio a las 10, como en E5.

| Medida | Valor | Origen |
|---|---|---|
| Cuarto | 4,0 m de diámetro | Proyecto |
| Pirca | 0,6 m de espesor y 1,2 m de alto, con un talud de 5° | Proyecto |
| Puerta | 0,6 × 1,0 m, al este, con dintel de laja | Proyecto; la puerta al este, Yampara Blanco (2019: 13) |
| Cúpula | Dieciséis hiladas de champa de 12 cm, que vuelan de 10 a 13 cm | Proyecto; el bloque, el de la prueba 3 |
| Óculo | 60 cm, con un sombrero de ichu de 1,2 m de diámetro | Proyecto |
| Relleno | Cinco anillos de tierra revocada; cada uno entra 16 cm | Proyecto |
| Alto | 3,2 m hasta el óculo | Cálculo |
| *T'uju* | 15 cm, al noreste | Yampara Blanco (2019: 13); tabla del sol de la prueba 5 |

Es la única de las seis que usa las cinco pruebas: la piedra de la cosecha y la pirca de doble cara en la base, la cúpula y el dintel volados, el ichu del sombrero y el fogón con el *t'uju*.

### A cuál podría reemplazar

| | En qué se parece | Qué se pierde si sale | Juicio |
|---|---|---|---|
| E1. La montaña habitada | En la forma: redonda, baja, volada por dentro, con óculo y entrada baja. Es la más parecida | La única obra hecha solo con la piedra de la cosecha, la «montaña de piedras» de la p. 9, que es también el título del artículo, y la primera *chhaxwa* del título. La serie pierde su comienzo | Posible, pero cuesta mucho |
| E2. El corral techado | En la base: la misma pirca redonda de doble cara, de unos 5 a 6 m; y el ichu arriba | El único techo liviano, la franja de cielo entre la piedra y la paja y la serie del tiempo, que está hecha sobre E2. La pirca de doble cara sigue en la base de la candidata y en E5 | La mejor opción |
| E3. La torre de champa | Solo en la champa | La V volada del umbral, el techo de *p'ira* y la *chhaxwa* atada | No |
| E4. La chullpa | En la cámara volada y la piedra de la base | La tumba, la cornisa de ichu y los adobitos | No |
| E5. La casa de la bóveda | En el uso: las dos son casas con fogón, *t'uju* y puerta al este | La casa rectangular de la novela («rectangulares y chatas», p. 30), la planta medida de Šolc y la referencia R16 | Posible, pero rompe la pareja |

**La propuesta es que reemplace a E2.** La candidata junta lo que E2 y E1 tienen de redondo, la pirca de E2 y la cámara volada de E1. Si entra en lugar de E2, la serie queda así:

- empieza con la cosecha (E1), sigue con el umbral (E3) y la tumba (E4);
- termina con la casa doble que describe Yampara Blanco, la redonda para todos los días y la rectangular (E5).

Al pasar de E2 a la casa redonda, el pasaje de la p. 156 sigue sirviendo, y mejor, porque nombra las dos cosas: «Las chujllas fueron reparadas del estrago, las pircas de piedra que separan las parcelas fueron compuestas».

Reemplazar E5 daría una casa más estable, porque en una cúpula volada cada hilada es un anillo cerrado, mientras que en una bóveda volada cada hilada depende solo del peso que carga su cola. Pero la serie se quedaría sin la casa rectangular de la novela y sin la pareja de las dos casas. Reemplazar E1 conserva la pareja, pero quita la obra que lleva el título.

Lo decide el autor. Si elige, se rehace la serie a la misma escala, la tabla de las pruebas y el documento.

## Lo que se descartó

El autor descartó una tercera exploración que se modeló el mismo día, *La A de piedra y tierra*. Eran dos muros de piedra amontonada que se tocaban arriba, con tierra apisonada entre los dos, sobre una base de pirca atravesada por un paso volado, a partir de la referencia R6. La reemplaza la torre de champa. No se renderizó a resolución completa ni entra al documento.

## Lo que decide el autor

- Los pasajes de E3, E4 y E5, y la lectura de la chullpa como tumba.
- Si el techo de E2 lleva *p'ira* bajo el ichu.
- Si la casa de E5 se baja hasta los dos metros de la novela.
- Si las cinco van en un mismo sitio. Por ahora se muestran juntas solo a la misma escala.
- El autor de R8 y de R16, antes de mostrarlas junto a estas maquetas.
- Si la casa redonda reemplaza a E2, a E1 o a E5, o si queda fuera.
