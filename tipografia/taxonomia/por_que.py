"""El porqué de cada lámina de la taxonomía: la columna de la derecha.

Cada lámina numera sus decisiones de dibujo en rombos, como los planos. La
decisión dice cómo se dibuja; el porqué la ata a una regla del proyecto, no
al estilo del reel.
"""

TEXTOS = {
    "R-00": [
        ("titulo", "Qué son estas láminas"),
        ("p", "**Las referencias de 10, conectadas por lo que hacen.** Veinticinco obras de dominio público, "
              "ordenadas por el mecanismo que activan y no por su estilo, con un método prestado: «A Taxonomy of "
              "Visuals», de Jason Murray (Modern Art Direction)."),
        ("p", "**Del método se toma la manera de ordenar, no la de mostrar.** Las láminas siguen las reglas de "
              "los planos y de la letra: la hoja, el cajetín, las líneas, la celda y la gravedad."),
        ("p", "**No son la letra.** Ninguna forma pasa a la caja ni a la fuente (06, §6.4). Cada referencia dice "
              "dónde cae: en qué acción, en qué plano, en qué regla."),
        ("titulo", "Lo que vale para todas"),
        ("decision", (1, "Visto y no visto",
                      "**La decisión.** Lo que la máquina no vio va a puntos y en violeta; lo que miraste, en "
                      "línea continua. **Por qué.** Es la regla de lo hallado y lo reconstruido (03, §3.2, "
                      "regla 2). La máquina buscó las imágenes y no pudo abrirlas: cada ficha está reconstruida "
                      "desde lo que dice su archivo.",
                      "No se salvó la piedra,\nsolo la opinión sobre ella.")),
        ("decision", (2, "El mecanismo, no la imagen",
                      "**La decisión.** Cada técnica se dibuja como un detalle de plano: en corte, en planta o "
                      "en serie. Las imágenes van solo en el atlas (R-09): de dominio público, en tinta y con su "
                      "archivo. **Por qué.** Se toma el procedimiento, no las formas (04; 06, §6.4). Lo ajeno se "
                      "cita: queda el enlace.", None)),
        ("decision", (3, "Ninguna caja cierra",
                      "**La decisión.** Las cajas de la taxonomía y las fichas se abren abajo, y lo que no cabe "
                      "tiene su celda vacía. **Por qué.** Todo contorno cerrado tiene desagüe (03b, regla 2). "
                      "Una clasificación cerrada vuelve a enterrar lo que nombra.",
                      "le pusieron nombre,\notra manera de enterrar.")),
        ("decision", (4, "Se toma, no se toma",
                      "**La decisión.** Una línea que termina en punto se toma; una que termina en corte, no. "
                      "**Por qué.** Es la convención del mapa 2 del informe, el de la teoría y las fuentes.",
                      None)),
        ("decision", (5, "La ficha dice de dónde viene",
                      "**La decisión.** Cada ficha lleva quién, cuándo, con qué medio, en qué archivo y con qué "
                      "licencia; lo que se toma y lo que no. **Por qué.** Es la regla de las referencias visuales "
                      "(06, §6.4). La impresión natural lo enseña: Auer acusó a Bradbury de plagio.", None)),
    ],
    "R-01": [
        ("titulo", "Qué se dibuja"),
        ("p", "El método del reel como un edificio que se reforma: lo que se conserva, lo que cambia, lo que se "
              "demuele y lo que se construye. Arriba, sus niveles en corte. Abajo, sus 41 técnicas por dominio y "
              "las 7 que se suman."),
        ("titulo", "De dónde sale"),
        ("p", "Un reel de Instagram de Jason Murray (Modern Art Direction, 2026; 1 min 42 s). No se encontró "
              "una página del método. Murray tiene un podcast, _Modern Art Direction_, y un directorio de "
              "herramientas, _Art Director Toolbox_: ahí se puede seguir buscando (los enlaces, abajo a la "
              "izquierda)."),
        ("titulo", "Decisiones"),
        ("decision", (1, "Se toma: el mecanismo",
                      "**La decisión.** Se conservan la idea del reel, sus cuatro operaciones, el camino del "
                      "encargo a la referencia y el cuadro de muchos a muchos. **Por qué.** Clasificar por el "
                      "procedimiento ya era una regla (04; 06, §6.4): el reel le da un orden.", None)),
        ("decision", (2, "Cambian: los dominios",
                      "**La decisión.** El rasgo pasa a materia y tacto; lo social, a la mano; lo cultural, a "
                      "procedencia. **Por qué.** Aquí la vista pasa por el tacto, del cuerpo queda la mano, y "
                      "una cultura no se cita: se dice de dónde viene cada cosa.", None)),
        ("decision", (3, "Se suma: la huella",
                      "**La decisión.** Un dominio nuevo, la huella, y un nivel más abajo de todo: dónde cae "
                      "cada referencia. **Por qué.** La letra se hace apretando, frotando y mojando. Y una "
                      "referencia que no cae en una acción es gusto: la crítica del propio reel.", None)),
        ("decision", (4, "Lo que se deja, cae",
                      "**La decisión.** Cada dominio es una caja abierta abajo. Lo que se deja cae por el "
                      "desagüe, bajo el fondo: a trazos lo que no sirve; con trazo y punto lo que no se hace. "
                      "**Por qué.** Dejar también es una decisión, y se dibuja. El color es material (03, §3.9), "
                      "la obra tapa ojos y boca (D12) y el cuerpo de Rebeca no se usa (06, §6.1).",
                      "La tierra se dio de beber a sí misma\ny ningún contenedor aguanta lo que contiene.")),
    ],
    "R-02": [
        ("titulo", "Qué se dibuja"),
        ("p", "Las veinticinco referencias contra las acciones del taller (04): en qué acción, en qué plano o en "
              "qué regla cae cada una. Es el cuarto nivel del método cruzado con el quinto."),
        ("titulo", "Decisiones"),
        ("decision", (1, "Un cuadro, no una nube",
                      "**La decisión.** Las conexiones van en filas y columnas, como el cuadro de acabados de un "
                      "plano. **Por qué.** En un cuadro cada cruce tiene su lugar y lo que falta se ve. En una "
                      "nube de nodos, lo vacío no se nota.", None)),
        ("decision", (2, "Las columnas son las acciones",
                      "**La decisión.** Las columnas siguen el taller, de la Acción 0 a la 12, en sus tres "
                      "cuadernos; antes, los planos; después, la cadena, el reparto y lo que no se hace. "
                      "**Por qué.** Es el quinto nivel: una referencia que no cae en ninguna parte no se toma.",
                      None)),
        ("decision", (3, "Lo vacío, en celda vacía",
                      "**La decisión.** Una acción sin referencias lleva la celda vacía y dice qué falta. "
                      "**Por qué.** Lo que no cabe se ve (03, §3.2, regla 7). La Acción 6 no tiene ninguna: la "
                      "oclusión se toma del reel, es la cinta de D12, pero ningún archivo trajo una.", None)),
        ("decision", (4, "La casilla de visto",
                      "**La decisión.** Cada fila tiene una casilla a puntos, para la mano. **Por qué.** La "
                      "máquina buscó y no vio. Lo visto se marca a mano, con fecha, y la fila pasa a línea "
                      "continua.",
                      "Tocas el agua y la diosa se deforma.\nTodos los archivos funcionan así.")),
    ],
    "R-03": [
        ("titulo", "Qué se dibuja"),
        ("p", "**Diferenciar:** separar algo de su fondo. En el reel, _Differentiate_. **Retórica:** antítesis: "
              "continuo y punteado, relieve y hundido. Aquí, el relieve del plano, lo hallado de lo "
              "reconstruido, la letra de la piel y Contenida de sus vecinas."),
        ("titulo", "Decisiones"),
        ("decision", (1, "El relieve, en corte",
                      "**La decisión.** La técnica 1 se dibuja en corte, con el recorrido del dedo. **Por qué.** "
                      "Lo que se lee con los dedos no se ve de frente: se ve en corte, como la placa de P-02 · 3. "
                      "Es el libro de Haüy (1786): por el reverso y en espejo.", None)),
        ("decision", (2, "Tres huellas, un corte",
                      "**La decisión.** La mano, la voz y un helecho hunden el mismo corte; solo cambia quién "
                      "aprieta. **Por qué.** El mecanismo es uno: un metal blando que guarda la forma. En "
                      "Contenida, el papel de aluminio de cocina.", None)),
        ("decision", (3, "La vecina, en dos hilos",
                      "**La decisión.** Cada vecina se une a Contenida por dos hilos: el que termina en punto "
                      "dice en qué se parece; el que termina en corte, en qué se separa. **Por qué.** Una obra "
                      "se define por lo que la vecina hace distinto (10, §10.7).", None)),
        ("decision", (4, "Quién lo hizo, en cajetín",
                      "**La decisión.** La técnica 4 se dibuja como un cajetín, con un renglón vacío para la "
                      "mano. **Por qué.** El cajetín ya dice quién dibujó y quién calca. La procedencia hace "
                      "la pregunta de Tshuma: «Who wrote it?».",
                      "Desenterrar una voz\nes desenterrar la mano del que la escribió.")),
        ("titulo", "Para la mano"),
        ("p", "Mira el libro de Haüy en la Wellcome Collection y anota cómo se fundían y se apretaban las "
              "letras: puede ajustar la Acción 4 (10, §10.11)."),
    ],
    "R-04": [
        ("titulo", "Qué se dibuja"),
        ("p", "**Agrupar:** hacer de muchos uno. En el reel, _Group_. **Retórica:** sinécdoque: una celda por "
              "toda la cabeza; una mano por todo el calendario. Aquí, la celda, la caja y las partes que "
              "comparten los signos."),
        ("titulo", "Decisiones"),
        ("decision", (1, "La mano, sin la mano",
                      "**La decisión.** La mano de Beda se dibuja como sus casillas, sin su contorno: cinco "
                      "columnas de celdas, catorce articulaciones y cinco uñas. **Por qué.** Se toma la "
                      "retícula, no la figura. Y la retícula ya era la caja (Cooperrider, 2022).", None)),
        ("decision", (2, "Los estados, uno sobre otro",
                      "**La decisión.** La técnica 6 se dibuja en axonometría: placa, cinta y frotado apilados, "
                      "como los bloques de un tipo cromático. **Por qué.** La misma letra, varias manos "
                      "(10, §10.6). En el espécimen se pueden superponer.", None)),
        ("decision", (3, "Lo que no se hace, no se dibuja",
                      "**La decisión.** La técnica 7 queda en una celda vacía, con trazo y punto. **Por qué.** "
                      "La obra ya pone el cuerpo, y el de Rebeca no se usa (06, §6.1). _The Human Alphabet_ es "
                      "la vecina opuesta: se cita para no repetirla.",
                      "Quedó el contenedor\nde lo que ya no está.")),
        ("titulo", "Para la mano"),
        ("p", "Decide si el _Bourbonnoise Alphabet_ entra como contraste (10, §10.11)."),
    ],
    "R-05": [
        ("titulo", "Qué se dibuja"),
        ("p", "**Secuenciar:** ordenar en el tiempo o en un recorrido. En el reel, _Sequence_. **Retórica:** "
              "gradación y ciclo: frotado 01 … n; «termina y empieza». Aquí, la cadena de estados, la serie de "
              "frotados, el bucle y el poema verso a verso."),
        ("titulo", "Decisiones"),
        ("decision", (1, "En serie, no en una foto",
                      "**La decisión.** La técnica 8 se dibuja en cuadros numerados, como los frotados. "
                      "**Por qué.** Worthington fotografió cada gota en secuencia, y la Acción 9 pide por eso "
                      "fotos seguidas.",
                      "la misma diosa dos veces\ny ninguna igual.")),
        ("decision", (2, "Componer es recorrer",
                      "**La decisión.** La técnica 9 se dibuja en planta, sobre los azulejos: una placa por "
                      "azulejo y un azulejo vacío entre palabras. **Por qué.** Feuillet escribió el recorrido de "
                      "un cuerpo (1701); componer también es trazar un recorrido (Acción 11).", None)),
        ("decision", (3, "La huella cambia de signo",
                      "**La decisión.** La cadena se dibuja con el relieve de cada paso: hundido, en relieve, "
                      "plano. **Por qué.** En la impresión natural la huella pasa del plomo al cobre y del "
                      "cobre al papel. En Contenida, cada paso pierde materia y gana luz.", None)),
        ("decision", (4, "El tiempo, en una cota",
                      "**La decisión.** La voz se dibuja como trazo, y lo que tardó en oírse, como una cota: "
                      "148 años. **Por qué.** Lo que vuelve, vuelve escrito: Scott escribió la voz en 1860, y se "
                      "oyó en 2008.",
                      "Y es que lo que vuelve, vuelve escrito;\npocas veces vuelve hablado.")),
        ("titulo", "Para la mano"),
        ("p", "Escucha el fonautograma de 1860 en First Sounds y decide si se cita en el espécimen "
              "(10, §10.11)."),
    ],
    "R-06": [
        ("titulo", "Qué se dibuja"),
        ("p", "**Inferir:** que quien mira complete lo que no está. En el reel, _Infer_. **Retórica:** elipsis "
              "y metáfora: lo que falta también dice; la letra es un vaso. Aquí, el desagüe, la vasija, lo "
              "reconstruido por analogía y la voz que no se entiende."),
        ("titulo", "Decisiones"),
        ("decision", (1, "La arena, donde no vibra",
                      "**La decisión.** La técnica 12 se dibuja en planta: las líneas donde la placa no vibra y "
                      "los dedos que la sujetan. **Por qué.** La figura depende de dónde apoyan los dedos: las "
                      "manos deciden lo que se ve (Chladni, 1787).", None)),
        ("decision", (2, "La aguja, a puntos",
                      "**La decisión.** En la técnica 13, la aguja que lee el surco va a puntos y en violeta. "
                      "**Por qué.** No existe: se calculó desde la luz (Bell, 1885; leído en 2013). Es una "
                      "reconstrucción, y se dibuja como tal.", None)),
        ("decision", (3, "El ¶, sin dibujo",
                      "**La decisión.** El ¶ no se dibuja: queda en su celda, la 56, con su nota. **Por qué.** "
                      "Se hace con los dedos, sin punzón (Acción 7). Es el único signo que no se halla ni se "
                      "reconstruye.",
                      "No tiene lengua pero igual dice.")),
        ("decision", (4, "Dada vuelta",
                      "**La decisión.** La técnica 15 compara dos filas: una cosa distinta por letra, a trazos; "
                      "la misma vasija para todas, en línea continua. **Por qué.** Es la metáfora de Contenida "
                      "dada vuelta (Publicius, 1482).", None)),
    ],
    "R-07": [
        ("titulo", "Qué se dibuja"),
        ("p", "El camino al revés: del encargo a la referencia, y no de la imagen al encargo. Cada columna baja "
              "de un verso o de una decisión de la obra, pasa por la operación, el dominio y la técnica, y llega "
              "a las referencias y a lo que cae en Contenida."),
        ("titulo", "Decisiones"),
        ("decision", (1, "El encargo es la obra",
                      "**La decisión.** El encargo no viene de un cliente: lo dan las decisiones de la obra "
                      "(D1 … D16) y los versos del poema. **Por qué.** Contenida traduce una obra; lo que la "
                      "obra pide es lo que se busca.", None)),
        ("decision", (2, "Todo cae",
                      "**La decisión.** Las columnas bajan, con la gravedad, hasta el ±0: lo que cae en "
                      "Contenida. **Por qué.** En lugar del norte, la gravedad (P-00). Lo que no llega al fondo "
                      "no se toma.", None)),
        ("decision", (3, "Por el reverso",
                      "**La decisión.** Se busca desde el verso hacia la imagen. **Por qué.** El repujado se "
                      "trabaja por el reverso y se lee por el frente. Juntar imágenes por gusto y buscarles un "
                      "uso después es lo que el reel critica.", None)),
        ("decision", (4, "Una columna vacía",
                      "**La decisión.** La última columna está vacía, con sus niveles a puntos. **Por qué.** La "
                      "máquina propone; la mano completa. El próximo encargo lo escribes tú, y la referencia "
                      "aparece cuando aparece.",
                      "Vuelve sin que la llames.")),
        ("titulo", "Para la mano"),
        ("p", "Escribe tu encargo en la columna vacía: un verso o una decisión de la obra. Pregunta qué operación "
              "pide, en qué dominio y con qué técnica; recién entonces, busca la referencia. Abajo hay cuatro "
              "encargos que ya esperan."),
    ],
    "R-08": [
        ("titulo", "Qué se dibuja"),
        ("p", "Lo que quedó afuera de la taxonomía: lo que se dejó a propósito, lo que se buscó y no se "
              "encontró, dónde seguir buscando y lo que queda pendiente."),
        ("titulo", "Decisiones"),
        ("decision", (1, "Lo que se deja, se dice",
                      "**La decisión.** Cada cosa dejada afuera va con su corte y su razón. **Por qué.** Dejar "
                      "también es una decisión (06, §6.4): una máscara de Paracas no es de Tiwanaku, y las «razas "
                      "monstruosas» y el orientalismo no se citan como referencia.", None)),
        ("decision", (2, "Lo no encontrado, en su celda",
                      "**La decisión.** Lo que se buscó y no apareció ocupa una celda vacía, con la acción en la "
                      "que caería, a puntos. **Por qué.** Es el .notdef de la caja: la celda vacía de la lámina, "
                      "calcada a mano (Acción 5). Lo que falta también se ve.", None)),
        ("decision", (3, "Nada se baja",
                      "**La decisión.** De los archivos queda el enlace: nada se descarga ni se sube. "
                      "**Por qué.** Lo ajeno se cita (06, §6.4). Como en la piscina, no se saca nada (03, §3.2, "
                      "regla 9).",
                      "Nos fuimos con las manos secas,\nque es como se sale de todas las ruinas.")),
    ],
}
