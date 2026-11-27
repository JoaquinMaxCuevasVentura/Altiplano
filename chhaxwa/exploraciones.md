# Las seis exploraciones

27 de noviembre de 2026. De la exploración formal (`exploracion_formal.md`) salieron seis obras que el autor eligió y que juntan las técnicas de las cinco pruebas. Las pruebas miden una técnica cada una. Las exploraciones son lo que se construiría con ellas.

| N.º | Exploración | Viene de | Pasaje de la novela |
|---|---|---|---|
| E1 | La montaña habitada | Las formas 1B y 1C | La «montaña de piedras» (p. 9) |
| E2 | El corral techado | Las formas 2C y 5C | Las pircas «compuestas» (p. 156) |
| E3 | La casa redonda | Una imagen del autor, corregida | El «dintel de Jatun-Kolla» (p. 155) |
| E4 | La chullpa | La pieza 3h, con la nota del autor | La «tumba agreste y anónima» (p. 154) |
| E5 | La casa de la bóveda | La referencia R16 | Las *chujllas* «rectangulares y chatas» (p. 30) |
| E6 | La *pirwa* | La referencia R8 y la pieza 3h | Los «trojes altos» (p. 157) |

Las páginas son de la novela (Botelho Gosálvez, 1982 [1945]). Los pasajes de E3 a E6 los propuso Claude y los decide el autor.

## Cómo se cruzan con las pruebas

| | 1. La cosecha | 2. El relleno | 3. El dintel | 4. La *p'ira* | 5. El fogón |
|---|---|---|---|---|---|
| E1 | ● toda la piedra | | ● la cámara volada | | ○ se entra en cuclillas |
| E2 | ○ la piedra de la pirca | ● la pirca de doble cara | | ○ el techo de ichu | |
| E3 | ○ la piedra de la pirca | ● la pirca de doble cara | ● el paso y la cúpula volados | ● las fajas y la *chhaxwa* | ● el fogón, el óculo y el *t'uju* |
| E4 | ● las pilas de piedra | | ● las pilas y la cámara voladas | ○ la cornisa de ichu | |
| E5 | | ● los muros de doble cara | ● la bóveda volada | | ● el fogón, el humo y el *t'uju* |
| E6 | ○ un apoyo es un montón | ○ el otro es una pirca | ● la V volada | ● las fajas y la *chhaxwa* | |

● es la técnica principal de la obra; ○, una que también usa.

Tres cosas atan las seis obras.

- **Una sola cosecha.** Todas usan la misma piedra, la angulosa que sale de despedregar el campo, y no traen otra. La tierra es la del lugar, y la paja es el ichu de la puna. La madera se reduce a palos cortos de queñua, porque en el altiplano no hay árboles: Squier lo dice al hablar de los puentes de champa, «The absence of wood and timber has led the people of the Sierra to adopt a great many novel and striking devices» (Squier, 1877: 313).
- **Lo que cierra arriba se vuela.** Donde no hay vigas, lo que cubre un espacio se hace volando hiladas, que es la técnica de la prueba 3. Así se cierran la cámara de E1, el paso y la cúpula de E3, las pilas y la cámara de E4, la bóveda de E5 y la V de E6. Las chullpas se cubrían igual. Sobre la de Palca, Squier escribe que «A rude arch of converging and overlapping stones, filled in or cemented together with clay, was raised over this cist» (ibid.: 243), y en la cámara de la de Acora, «the stones begin to overlap, forming a kind of pointed arch» (ibid.: 353).
- **El cuerpo como medida.** Se entra en cuclillas a E1, de rodillas a E3, agachado bajo E4 y de lado por la ranura de E5, y bajo la V de E6 se pasa de pie, justo. La boca de la chullpa mide lo que medía la de Palca, «about eighteen inches wide and high» (ibid.: 244).

El orden va de una cosecha a otra. Empieza en el montón que deja la cosecha de piedras (E1) y en la pirca que la ordena (E2). Siguen la casa redonda, a la que se entra de rodillas como al *ayllu* (E3), la tumba (E4) y la casa rectangular (E5), y termina en el troje donde se guarda la cosecha de granos (E6), que es como termina la novela. E3 y E5 son la pareja de casas que describe Yampara Blanco, la redonda y la cuadrada, y E6 es una de las *pirwas* que las acompañan (2019: 9 y 14). E1, E2 y E3 son redondas, y cada una cubre el círculo con un material de la cosecha: piedra, paja y tierra.

El título se cumple en tres de ellas. E1 es la *chhaxwa* de los montones de la chacra, y en E3 y en E6 los palos se atan a piedras hincadas, que es la otra *chhaxwa* de Bertonio (2011 [1612]: 330).

Las seis son maquetas de estudio a 1:20, modeladas en Blender (`blender/formas.py`), con un corte de cada una y la serie a la misma escala (`blender/diagramas.py`). En las tablas, «proyecto» marca una decisión que se comprueba o se cambia al construir, y «cálculo», una cifra que sale de una cuenta.

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

## E3. La casa redonda

La casa redonda aymara sobre una base de pirca. Yampara Blanco describe el *muruqu uta*, la «casa de base de forma circular usada cotidianamente», que se usa sobre todo en las épocas de heladas y de lluvia. Su puerta mira al este, tiene un fogón de arcilla al centro y un *t'uju* al noreste, «por donde penetran los rayos solares» y por donde sale el humo (2019: 13). El putuco de champa, en cambio, suele ser de planta cuadrada (Vitulas-Quille y Reynoso-Machaca, 2025: 5).

Sale de una imagen que mandó el autor: una base de piedra, una cúpula de tierra en anillos escalonados, ichu arriba y una puerta angosta. La imagen no está en el repositorio, porque no se sabe de dónde viene; si es de un generador de imágenes, sirve solo como boceto (regla 5). Se corrigió en dos tandas. Primero, cuatro problemas de la imagen:

1. **La piedra es la de la cosecha.** La base es una pirca redonda de doble cara, de piedra angulosa y no de río, con relleno de piedra menuda (prueba 2).
2. **El óculo queda abierto.** El ichu se vuelve un sombrero levantado 30 cm sobre tres palos de queñua. El humo sale por los costados y la lluvia no cae de lleno sobre el fogón.
3. **La cúpula volada es un cono por dentro.** Cada hilada solo puede volar una parte de su largo, así que una cúpula por aproximación de hiladas se cierra en punta, como la cámara de E1. La forma baja y redonda de la imagen es un relleno de tierra sobre la cámara volada, que además carga las colas de las hiladas, que es lo que las sostiene.
4. **El *t'uju*** atraviesa la pirca del noreste, apuntado al sol del 21 de junio a las 10, como en E5.

Después, cuando el autor decidió que reemplazara a la torre de champa, tomó lo que la torre traía al proyecto:

- **El umbral.** Se entra por un paso de piedra de 1,2 m de largo, con jambas de 60 cm y tres hiladas que vuelan 10 cm hasta cerrarse a 96 cm, que es la regla de la prueba 3. Hay que entrar de rodillas, como los comunarios que vuelven y se arrodillan «en el dintel de Jatun-Kolla» (p. 155).
- **La *p'ira*.** La tierra se cubre con fajas de *p'ira* de 0,7 m de ancho, como las de Enquelga (Šolc, 2011 [1975]: 105), puestas en seis cursos alrededor de la cúpula. Cada curso se traslapa 15 cm sobre el de abajo, como tejuelas, y así escurre el agua. La prueba 4 suma una pregunta: si una faja fresca se puede doblar a la curva de una cúpula.
- **La *chhaxwa*.** Los palos del sombrero se atan a tres piedras hincadas en el collar del óculo. Unas lajas hincadas en el relleno, del lado sureste, sirven de escalones para subir a poner y quitar el sombrero; son una decisión del proyecto, sin fuente.

| Medida | Valor | Origen |
|---|---|---|
| Cuarto | 4,0 m de diámetro | Proyecto |
| Pirca | 0,6 m de espesor y 1,2 m de alto, con un talud de 5° | Proyecto |
| Paso de entrada | 0,6 m de ancho y 0,96 m de alto, 1,2 m de largo, al este | La regla de la prueba 3; la puerta al este, Yampara Blanco (2019: 13) |
| Cúpula | Dieciséis hiladas de champa de 12 cm, que vuelan de 10 a 13 cm | Proyecto; el bloque, el de la prueba 3 |
| Cubierta | Seis cursos de fajas de *p'ira* de 0,7 m, traslapados 15 cm | Šolc (2011 [1975]: 105), el ancho; lo demás, proyecto |
| Óculo | 60 cm, con un sombrero de ichu de 1,2 m de diámetro | Proyecto |
| Alto | 3,2 m hasta el óculo | Cálculo |
| *T'uju* | 15 cm, al noreste | Yampara Blanco (2019: 13); tabla del sol de la prueba 5 |

Es la única de las seis que usa las cinco pruebas. Con E5 forma la pareja de la casa redonda y la cuadrada, que juntas, dice Yampara Blanco, «representan simbólica y culturalmente la feminidad y la masculinidad» (2019: 9).

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

## E6. La *pirwa*

Un troje alto: un depósito de champa levantado sobre dos apoyos de piedra. Yampara Blanco describe las *pirwas* de la vivienda aymara como «silos aéreos de granos, quinua y papas deshidratadas», con «dos aperturas laterales libres»: una arriba, de unos 30 × 35 cm, por donde se metían los alimentos, y otra abajo, por donde se sacaban (2019: 14). Las que describe son chicas, de un metro por 60 cm. Esta es un troje grande, como los «graneros colectivos» que se llenan con el trabajo de la comunidad (p. 16) y los que anuncia el final de la novela, cuando todo es «pronóstico de abundancia, de trojes altos y almiares llenos» (p. 157).

Era la torre de champa, una interpretación de la referencia R8, una torre de tablas apiladas sobre dos apoyos. Cuando la casa redonda tomó su lugar como E3, el autor pidió mejorarla para que ocupara otro y entrara como sexta. Como depósito, cada parte tiene un uso:

- **Los dos apoyos** son las dos maneras de poner la piedra de la cosecha, una pirca y un montón, y levantan lo guardado del suelo húmedo.
- **La V** entre los apoyos se hace volando las hiladas de champa, como en los puentes de champa que Squier vio camino a Copacabana, donde cada capa vuela sobre la de abajo «until the upper ones touch and brace against each other, forming a rude kind of arch» (Squier, 1877: 313). En su clave está la boca de abajo, con una trampa de queñua, por donde se saca lo guardado. En las *pirwas* de Yampara Blanco las dos bocas están a un costado; ponerla en la clave, por debajo, es una decisión del proyecto.
- **La escalera.** Unas lajas hincadas en la cara sur suben en diagonal desde la pirca hasta la boca de carga, de unos 30 × 35 cm. Otras lajas atraviesan el muro, traban las hiladas y asoman, como las tablas sueltas de la referencia, y algunos huecos entre los bloques dejan pasar el aire.
- **El techo** es de un agua, con fajas de *p'ira* (Šolc, 2011 [1975]: 105) sobre seis palos de queñua. Cada palo se ata a una piedra hincada en el muro debajo de su extremo, la *chhaxwa* «hincada en la pared para atar en ella los palos del techo» (Bertonio, 2011 [1612]: 330).

La champa sirve para esto. En el Ramis, Squier vio que con ella se hacían «their dwellings and the corrals», y que esas casas parecían «tall quadrilateral hay-stacks» (Squier, 1877: 391).

| Medida | Valor | Origen |
|---|---|---|
| Planta | 3,0 × 1,6 m | Proyecto |
| Alto | 3,6 m del lado bajo y 4,6 m del alto | Proyecto (antes, 4,2 y 5,4 m) |
| Apoyos | 0,9 m de alto; una pirca y un montón | Proyecto |
| Bloque de champa | 40 × 25 × 12 cm | Proyecto (el de la prueba 3) |
| La V | Siete hiladas que vuelan 6 cm cada una; la clave queda a 1,8 m del suelo | Cálculo |
| Bocas | Arriba, de unos 30 × 35 cm, para cargar; abajo, en la clave de la V, para sacar | Yampara Blanco (2019: 14) |
| Fajas de *p'ira* | 2,5 × 0,7 m, en dos hileras traslapadas | Šolc (2011 [1975]: 105) |

La champa se deja secar unos veinte días antes de usarla (Vitulas-Quille y Reynoso-Machaca, 2025: 9). Se bajó un metro para que sea menos arriesgada, pero si un depósito de champa de más de cuatro metros se sostiene lleno es lo primero que hay que probar.

## Lo que se descartó y lo que cambió

- ***La A de piedra y tierra***, modelada a partir de la referencia R6: dos muros de piedra amontonada que se tocaban arriba, con tierra apisonada entre los dos, sobre una base de pirca atravesada por un paso volado. El autor la descartó. Solo hubo renders rápidos.
- ***La torre de champa*** fue E3 hasta que el autor la reemplazó por la casa redonda. Mejorada como depósito, volvió como E6.
- **La casa redonda** entró primero como candidata (E6), con un análisis de a cuál de las cinco podía reemplazar; se proponía E2. El autor eligió reemplazar la torre, y se le pasó lo que la torre traía: el umbral, la *p'ira* y la *chhaxwa* (`analisis/43`, §13 y §14).

## Lo que decide el autor

- Los pasajes de E3 a E6, y la lectura de la chullpa como tumba.
- Si el techo de E2 lleva *p'ira* bajo el ichu.
- Si la casa de E5 se baja hasta los dos metros de la novela.
- Si las seis van en un mismo sitio. Por ahora se muestran juntas solo a la misma escala.
- El autor de R8 y de R16, antes de mostrarlas junto a estas maquetas.
