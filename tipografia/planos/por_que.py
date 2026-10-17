"""El porqué de cada lámina: las decisiones de anatomía tipográfica y sus razones.

Cada lámina numera sus decisiones formales (contraste, ojo, apertura, terminales,
remates, hombro, sobrepaso…). El mismo número, en un rombo, marca en el dibujo
el lugar de la letra donde la decisión ocurre. En la columna, cada decisión dice
qué se decidió, con su medida, y por qué: el concepto (las decisiones de la obra,
D1 … D16, de 01_la_obra_decision_por_decision.md), la figura retórica que la
sostiene y, cuando rima, el verso del poema (textos/poema.txt, sin tocar).

Bloques de la columna:
  ("titulo", texto) · ("p", texto) · ("verso", texto) · ("espacio", mm)
  ("decision", (n, término, texto, verso o None))
Los textos admiten **negrita** y _cursiva_; los números entran con {clave}.
"""

TEXTOS = {}

TEXTOS["P-00"] = [
    ("titulo", "Qué son estas láminas"),
    ("p", "**Los planos de la forma de _Contenida_**, dibujados con la precisión de un plano de arquitectura: la "
          "celda y sus líneas, el trazo, los cuatro generadores (o, l, n, a), las partes que salen de ellos y la "
          "caja. Cada medida sale de simulacion/gramatica.py y se acota en milímetros de la placa y en unidades "
          "de la fuente."),
    ("p", "**Son la concepción formal, no la letra.** La mano calca el esqueleto del pie aplicando estas reglas "
          "(Acción 3), repuja (Acción 4) y sigue con los estados. Lo que la placa contradiga se anota (05, §5.6); "
          "no se corrige la placa para que se parezca al plano. Es la propuesta de la máquina: no entra en la caja "
          "ni en la fuente. Mientras no llegue el libro, el testigo del pie es un sustituto: pueden cambiar las "
          "medidas, no las reglas."),
    ("titulo", "Cómo se lee el porqué"),
    ("p", "Cada lámina numera sus **decisiones de anatomía tipográfica**. El número, en un rombo, está en el dibujo, "
          "en el lugar de la letra donde ocurre, y en esta columna con su razón: el concepto (las decisiones de la "
          "obra, D1 … D16), la figura retórica y el verso con que rima."),
    ("titulo", "Lo que vale para todas"),
    ("decision", (1, "Hallado y reconstruido", "**La decisión.** Lo hallado en el pie se dibuja con línea continua; "
                  "lo reconstruido por analogía, a puntos y en violeta, en todos los estados. **Por qué.** Es la "
                  "convención del dibujo arqueológico, y la que la lámina no cumple: su pie confiesa que el dibujo es "
                  "reconstructivo, pero el dibujo no dice qué parte lo es. La letra cumple esa confesión.",
                  "No se salvó la piedra,\nsolo la opinión sobre ella.")),
    ("decision", (2, "La gravedad: tres reglas", "**La decisión.** El agua se va por abajo (el desagüe), la "
                  "intemperie gasta desde arriba (los remates) y lo que se derrama cae (las gotas). **Por qué.** "
                  "Todo en la obra es un continente y ninguno retiene lo que le ponen adentro (01, §1.3). En lugar "
                  "del norte, cada lámina lleva la gravedad.", None)),
    ("titulo", "Unidades"),
    ("p", "1 mm de la placa son 4 px del lienzo de la gramática. La celda mide {celda_alto} mm de alto, que son "
          "1000 UPM: 1 UPM = {upm_mm} mm. Las cotas dan milímetros y, entre paréntesis, UPM. Los niveles se miden "
          "desde el fondo (±0), como el piso terminado de un plano."),
]

TEXTOS["P-01"] = [
    ("titulo", "Qué se dibuja"),
    ("p", "La celda de la cabeza de la ídolo dentro de la placa de 150 mm, con las cuatro líneas que da el pie. "
          "Abajo, a 1:3, tres signos en su celda y la celda vacía."),
    ("titulo", "Decisiones"),
    ("decision", (1, "El cuerpo: la celda de la cabeza", "**La decisión.** El cuerpo del tipo es una celda de 0,84 de "
                  "ancho por alto: {celda_ancho} × {celda_alto} mm, 840 × 1000 UPM. **Por qué.** Es la proporción "
                  "de las celdas de la cabeza en la lámina: se parte del registro y no de la piedra (D1). Es el único "
                  "préstamo directo del monolito, y entra vacío: también es el .notdef, lo que la fuente muestra "
                  "cuando no tiene la letra. _Retórica:_ metonimia; la celda de la cabeza está por la ídolo entera.",
                  "Quedó el contenedor\nde lo que ya no está.")),
    ("decision", (2, "El ancho: monoespaciada", "**La decisión.** Todas las letras miden una celda y nada se estira "
                  "para llenar. Entre palabras queda una celda vacía. **Por qué.** Las celdas de la cabeza y la "
                  "máquina de escribir del poema son retículas de celdas iguales. La letra se adapta a su "
                  "contenedor, y no al revés: la m llena su celda y la i queda rodeada de piel, la que se ve entre "
                  "placa y placa sobre el cuerpo (D3).", None)),
    ("decision", (3, "Las líneas: nombres de vasija", "**La decisión.** La base se llama fondo (±0); la altura de x, "
                  "borde (+{borde_upm}); las ascendentes llegan afuera (+{afuera_upm}); las descendentes caen al "
                  "desagüe ({desague_upm}). **Por qué.** En la obra todo es un continente, y la letra también se "
                  "mide como un vaso. Son además las partes de la piscina, con el público adentro y afuera (D6, "
                  "D9). _Retórica:_ metáfora; la letra es un vaso.", None)),
    ("decision", (4, "La altura de x: {razon}", "**La decisión.** Las ascendentes miden {razon} veces la altura de x: "
                  "una x baja, con ascendentes largas y descendentes cortas. Ninguna altura se redondea a una "
                  "retícula. **Por qué.** Es la única proporción que se toma de la foto del pie real (07, §3); el "
                  "testigo sustituto daba 1,52. Las alturas las da el registro, no una norma.", None)),
    ("titulo", "Para la mano"),
    ("p", "La pauta a 1:1 está en esquemas/pauta_azulejo.svg. Se calca con el fondo de la pauta sobre la base del "
          "pie ampliado (Acción 3). Si algo se sale de la celda, se deja salir y se anota."),
]

TEXTOS["P-02"] = [
    ("titulo", "Qué se dibuja"),
    ("p", "El trazo como un canal: su ancho, su curva mínima, lo que pasa si se dobla más, cómo queda en la placa "
          "y cómo lo gasta la intemperie."),
    ("titulo", "Decisiones"),
    ("decision", (1, "Contraste: ninguno", "**La decisión.** Un solo grosor, {canal_mm} mm ({canal_upm} UPM), en todo "
                  "el recorrido y en todas las letras: no hay finos y gruesos ni eje de modulación. **Por qué.** El "
                  "contraste de una romana es la huella de una pluma que cambia de ancho con la dirección. El "
                  "punzón y la cinta no modulan (D2, D12). Del pie se toma la medida, no el contraste: el canal es "
                  "la media entre el grueso y el fino de su o. _Retórica:_ silepsis; _canal_ es a la vez el trazo, el "
                  "surco del punzón y el cauce del agua.",
                  "Desenterrar una voz\nes desenterrar la mano del que la escribió.")),
    ("decision", (2, "La curva mínima: {radio_mm} mm", "**La decisión.** Ninguna curva del eje tiene un radio menor "
                  "que 0,6 canal: no hay vértices agudos. **Por qué.** Con un radio menor que medio canal, el "
                  "contorno interior se cruza consigo mismo; en la hoja, ahí el punzón la rasga (D2). Es una "
                  "condición geométrica y una material a la vez.", None)),
    ("decision", (3, "Remates: ninguno", "**La decisión.** Los trazos terminan en un corte recto; todas las esquinas "
                  "se gastan con un radio de {intemperie_mm} mm. **Por qué.** El pie lo dice de la piedra: «hoy está "
                  "muy erosionado y casi no se ven esos detalles». La letra no reconstruye lo que la intemperie se "
                  "llevó. _Retórica:_ elipsis; lo que falta también dice.", None)),
    ("decision", (4, "El desagüe: 3 mm", "**La decisión.** Ningún contorno cierra: se abre 3 mm. **Por qué.** Es el "
                  "surco del punzón con sus lomas, el hueco más chico que queda abierto. El punzón se detiene 3 mm "
                  "antes de cerrar (Acción 4).", None)),
    ("decision", (5, "El relieve: 2,5D", "**La decisión.** El canal se hunde por el reverso y sale en relieve por el "
                  "anverso; su profundidad no se fija. **Por qué.** Se repuja por el reverso y en espejo, como el "
                  "primer libro en relieve para ciegos (Haüy, 1786). La profundidad la decide la mano y se mide en "
                  "las placas.", None)),
    ("titulo", "Para la mano"),
    ("p", "En el calco se dibuja el contorno, no el eje. Los radios no se miden: si la mano dobla más que la "
          "chapa, la chapa avisa. Una placa rota no se corrige: va a su ficha y a la caja (Acción 4, paso 7)."),
]

TEXTOS["P-03"] = [
    ("titulo", "Qué se dibuja"),
    ("p", "El primer generador, a 1:1: un solo trazo abierto. Abajo, cómo se construye en cuatro pasos."),
    ("titulo", "Decisiones"),
    ("decision", (1, "El ojo, arriba: el del pie", "**La decisión.** La mitad alta del ojo es la elipse del ojo de la "
                  "o del pie, con su ancho ({o_ancho} mm entre ejes) y su alto. **Por qué.** Del pie se toman las "
                  "medidas (D1): arriba, el registro queda intacto. _Retórica:_ cita; media letra es una cita "
                  "literal del archivo.", None)),
    ("decision", (2, "La panza, abajo: una vasija", "**La decisión.** La pared baja vertical, se abomba (0,55: entre "
                  "la pared recta, 0, y el cuenco, 1) y llega de plano a un fondo que mide 0,70 del ancho mayor "
                  "({o_fondo} mm). **Por qué.** La mitad baja la dicta la obra: el trapecio con que la proyección "
                  "llega a la pared (D8) y el fondo de la piscina vacía (D6). _Retórica:_ metáfora; la o es una "
                  "vasija.", "Una piscina vacía,\ndonde una vez aprendí a flotar,\nahora aprendo a mirar.")),
    ("decision", (3, "Sobrepaso: arriba sí, abajo no", "**La decisión.** Arriba, la curva pasa el borde {o_sobre} mm, "
                  "como en el pie. Abajo no pasa el fondo: se apoya en él. **Por qué.** Lo redondo tiene que pasarse "
                  "de la línea para parecer tan alto como lo plano; un fondo plano no lo necesita. La o se asienta "
                  "en la línea como un vaso en una mesa.", None)),
    ("decision", (4, "Apertura: el desagüe", "**La decisión.** El ojo no cierra: el trazo se corta 3 mm en el centro "
                  "del fondo. **Por qué.** Todo lo cerrado es una cuenca, y toda cuenca se abre abajo (D16). La e, la "
                  "a, la g y el 8 heredan de aquí su desagüe. _Retórica:_ oxímoron; un contenedor que no contiene.",
                  "y ningún contenedor aguanta lo que contiene.")),
    ("decision", (5, "El eje: vertical", "**La decisión.** La o es simétrica respecto de un eje vertical. **Por qué.** "
                  "El eje inclinado de las romanas es el de la pluma en la mano; aquí manda la gravedad, que es "
                  "vertical.", None)),
    ("titulo", "Para la mano"),
    ("p", "La mitad alta se calca del pie tal cual. La baja se rehace: desde el punto más ancho del ojo, la pared "
          "baja y cierra hasta dejar el fondo en siete décimas de ese ancho, con las esquinas redondeadas. El "
          "punzón se detiene 3 mm antes de cerrar el fondo."),
]

TEXTOS["P-04"] = [
    ("titulo", "Qué se dibuja"),
    ("p", "El segundo generador, a 1:1: un asta que baja en tres planos, cortada arriba y asentada abajo."),
    ("titulo", "Decisiones"),
    ("decision", (1, "El asta: un fuste en tres planos", "**La decisión.** El asta no es una recta: son tres planos de "
                  "{l_plano} mm que se apartan 1,6° del eje; el eje se corre {l_desvio} mm y vuelve. **Por qué.** La placa "
                  "cambia de plano al apoyarse en el cuerpo (D3) y la figura se mueve como la piedra, apenas (D11). "
                  "Es pariente de la éntasis de las columnas: se siente más de lo que se ve. _Retórica:_ anáfora y "
                  "litote; tres veces «es decir», y un «apenas» que se mide en grados.",
                  "Moverse como se mueve la piedra,\nes decir, apenas, es decir, temblor,\nes decir, un presente "
                  "continuo.")),
    ("decision", (2, "Arriba: un corte", "**La decisión.** Arriba no hay serifa ni gota: un corte recto, gastado. "
                  "**Por qué.** La intemperie gasta desde arriba (el pie: «muy erosionado»), y lo que mira arriba no "
                  "gotea: la gravedad no se da vuelta.", None)),
    ("decision", (3, "Abajo: el asiento", "**La decisión.** El asta se ensancha de un canal a dos ({asiento_ancho_mm} "
                  "mm) en una curva cóncava de {asiento_alto_mm} mm, sin serifa. **Por qué.** El peso se asienta en "
                  "la tierra: la piedra en pie. En arquitectura, la curva que une el fuste con la basa es la apófige; "
                  "la tipografía usa el mismo nombre para la que une el asta con su remate. Aquí hay apófige y no "
                  "hay remate. _Retórica:_ antítesis; arriba se pierde, abajo pesa.", None)),
    ("titulo", "Para la mano"),
    ("p", "Los planos no se miden con transportador: aparecen solos en la placa, donde la chapa se apoya. Arriba "
          "no se calca el remate del pie; abajo, el asiento se dibuja a mano alzada, de un canal a dos. El "
          "laboratorio de discrepancias mide después cómo cambian los planos con el cansancio de la mano (05, "
          "§5.6)."),
]

TEXTOS["P-05"] = [
    ("titulo", "Qué se dibuja"),
    ("p", "El tercer generador, a 1:1: un fuste que sale del borde y un arco que se tensa arriba y baja como otro "
          "fuste. En línea de comparación, la elipse que no se eligió."),
    ("titulo", "Decisiones"),
    ("decision", (1, "El hombro: una superelipse", "**La decisión.** El arco no es una elipse (exponente 2): es una "
                  "superelipse de exponente 3, más tensa y achatada arriba. **Por qué.** Es la chapa de aluminio "
                  "doblada a la fuerza sobre un hombro o una clavícula (D3): el metal no se curva como el giro de una "
                  "pluma. _Retórica:_ metáfora literalizada; _hombro_ es una palabra de la tipografía que aquí "
                  "recupera su cuerpo.", "Es lo más parecido a estar viva\nque puede hacer una imagen.")),
    ("decision", (2, "El arranque: tangente", "**La decisión.** El arco sale del fuste en su misma dirección, sin "
                  "muesca ni adelgazamiento en la unión. **Por qué.** Sin contraste no hay nada que adelgazar, y un "
                  "encuentro tangente no tiene rincón: el aluminio no se rasga y no hace falta alivio (D2).", None)),
    ("decision", (3, "La altura del arranque: 0,40", "**La decisión.** El arco se vuelve vertical al 0,40 de la "
                  "distancia del borde al fondo ({n_caida} mm bajo el tope del arco). **Por qué.** Se tomó a ojo del "
                  "testigo de la n. Es la medida más débil de estos planos, y se dice: falta medirla en el libro "
                  "(03c, §7).", None)),
    ("decision", (4, "La bajada: otro fuste", "**La decisión.** Después del arco, el trazo baja como un fuste: tres "
                  "planos y asiento. **Por qué.** Las partes se reúsan y no se inventan en cada letra: la n son dos "
                  "fustes y una chapa.", None)),
    ("titulo", "Para la mano"),
    ("p", "En el calco, el arco se tensa: arriba se aplana más de lo que dice el pie. Si la mano no lo encuentra, "
          "tiene razón la mano, y se anota."),
]

TEXTOS["P-06"] = [
    ("titulo", "Qué se dibuja"),
    ("p", "El cuarto generador, a 1:1: la a de dos pisos, que es la suma de las otras tres partes."),
    ("titulo", "Decisiones"),
    ("decision", (1, "El gancho: termina a 105°", "**La decisión.** El gancho es un hombro que no baja: termina a los "
                  "105°, mirando abajo. **Por qué.** Solo gotea lo que mira abajo, y a 105° la gota cuelga libre, "
                  "sin tocar la cuenca.", None)),
    ("decision", (2, "El terminal: una gota", "**La decisión.** Del gancho cuelga una gota: un cuello de "
                  "{gota_cuello_mm} mm y una masa de {gota_masa_mm} mm que cae {gota_caida_mm} mm a plomada. "
                  "**Por qué.** En las romanas, la gota remata el giro del trazo; aquí cae por su peso, a plomada, "
                  "sin seguir la dirección del gancho. Es el líquido que se vierte en la boca y chorrea (D16). _Retórica:_ sinécdoque; una gota por todo el "
                  "líquido vertido.", "La tierra se dio de beber a sí misma")),
    ("decision", (3, "El ojo: una cuenca que se abre", "**La decisión.** El ojo de la a es una cuenca: arriba, el del "
                  "pie; abajo, pared y fondo que siguen hasta el fuste. Se abre en su punto más bajo y se corre hacia "
                  "abajo para que la gota caiga libre. **Por qué.** Todo lo cerrado se abre abajo, y la gota no toca "
                  "nada: cuelga sobre su propia cuenca, y la letra se da de beber a sí misma. **Una discrepancia.** La "
                  "regla pide 0,4 canal ({a_libre_regla} mm), pero mide desde la gota sin estirar: en el cuerpo "
                  "quedan {a_libre} mm. Se anota; la placa dirá si alcanza.", None)),
    ("decision", (4, "La suma: dos pisos", "**La decisión.** La a es de dos pisos, como la del pie: gancho (n), fuste "
                  "(l) y cuenca (o). **Por qué.** Prueba que las partes se combinan. Es el método con que Agüero, "
                  "Uribe y Berenguer (2003) leen la litoescultura de Tiwanaku: elementos que se combinan en motivos, "
                  "y motivos en figuras.", None)),
    ("titulo", "Para la mano"),
    ("p", "La gota se calca a plomada: vertical, aunque el gancho venga inclinado. Si la gota toca la cuenca, se "
          "corre la cuenca, no la gota."),
]

TEXTOS["P-07"] = [
    ("titulo", "Qué se dibuja"),
    ("p", "El cuadro de las partes, como el cuadro de aberturas de un plano: cada parte, marcada en un signo; de "
          "dónde viene, en qué signos está y qué la mide."),
    ("titulo", "Las reglas de la derivación"),
    ("decision", (1, "Todo lo cerrado se abre abajo", "Las contraformas de b, d, p, q, a, e, g, 0, 6, 8 y 9 son "
                  "cuencas con desagüe. El ojo de la e se abre en su barra; el del 8, en el ojo de abajo (D16).", None)),
    ("decision", (2, "Solo gotea lo que mira abajo", "Los terminales que miran abajo llevan gota: a, c, f, r, s, y, 2, "
                  "3, 6, ? y la coma. Los que miran arriba terminan en un corte: e, j, la s abajo, 3, 5, 9 y ¿. La "
                  "gravedad no se da vuelta.", None)),
    ("decision", (3, "La coma: un punto que gotea", "Un punto de cinta del que cae una gota: la puntuación también "
                  "obedece a la gravedad.", None)),
    ("decision", (4, "Las cifras: elzevirianas, en su celda", "El pie no trae ninguna cifra: las diez se "
                  "reconstruyen. Lo que mide el tiempo es, en el archivo, lo que no se sabe leer (el calendario "
                  "«todavía no bien interpretado»).", None)),
    ("decision", (5, "Lo reconstruido: las mismas partes", "Solo cambia la ejecución: se calca en punteado y se "
                  "repuja a puntos.", None)),
    ("p", "**Por qué.** Agüero, Uribe y Berenguer (2003) leen la litoescultura de Tiwanaku como elementos que se "
          "combinan en motivos, y motivos en figuras. Aquí, partes en signos y signos en textos. Se toma el método, "
          "no los motivos: ningún signo tiwanacota entra en la letra (D5). _Retórica:_ derivación; palabras de una "
          "misma raíz (enterrar, desenterrar), signos de cuatro raíces."),
    ("verso", "A la ídolo la desenterraron,\nle pusieron nombre,\notra manera de enterrar."),
]

TEXTOS["P-08"] = [
    ("titulo", "Qué se dibuja"),
    ("p", "Seis detalles: las partes que no son trazo corrido y los encuentros que el aluminio no perdona."),
    ("titulo", "Decisiones"),
    ("decision", (1, "El punto: un cuadrado de cinta", "**La decisión.** Un cuadrado de {punto_mm} mm, el ancho de la "
                  "cinta. **Por qué.** El punto de una romana es una gota de tinta; este es un parche: la cinta que "
                  "tapó ojos y boca (D12) y el punto de luz que no se mueve en los videos (01, §1.4).",
                  "A la boca la taparon, a las manos no,")),
    ("decision", (2, "La tilde: una gota", "**La decisión.** La punta arriba y el peso abajo. **Por qué.** La tilde "
                  "marca dónde carga la voz; la voz de la obra no se entiende (D14) y el líquido cae de la boca "
                  "(D16).", None)),
    ("decision", (3, "La virgulilla: una onda", "**La decisión.** Un período de onda, de 0,7 canal de alto. **Por "
                  "qué.** Es el agua tocada (D15).", "Tocas el agua y la diosa se deforma.")),
    ("decision", (4, "El enlace de la g: un sifón", "**La decisión.** Las dos cuencas de la g y del 8 se comunican "
                  "por un cuello de 0,6 canal ({sifon_mm} mm), el único trazo más fino. **Por qué.** Vasos "
                  "comunicantes. Se queda la física; la lectura ritual no entra (01, §1.6).", None)),
    ("decision", (5, "El alivio: una trampa al revés", "**La decisión.** En cada rincón agudo, un rebaje de "
                  "{alivio_mm} mm sobre la bisectriz. **Por qué.** Las trampas de tinta de la Bell Centennial "
                  "(Matthew Carter, 1978) dejaban lugar a la tinta que sobraba; este alivio deja lugar al metal, "
                  "para que no se desgarre bajo el punzón (D2).", None)),
    ("decision", (6, "La cifra: dentro de su celda", "**La decisión.** Un rectángulo dentro de otro, con desagüe; "
                  "las cifras son elzevirianas. **Por qué.** Es la celda de la cabeza: el único lugar del juego donde "
                  "se ve la retícula del calendario.", None)),
]

TEXTOS["P-09"] = [
    ("titulo", "Qué se dibuja"),
    ("p", "Tres pares que en una tipografía común serían uno el reflejo del otro. A la derecha, el segundo con el "
          "primero dado vuelta encima, en línea de comparación: lo que no coincide es la variación."),
    ("titulo", "Decisiones"),
    ("decision", (1, "¿ no es ? dada vuelta", "El punto queda arriba y el gancho abajo, y el gancho no gotea, porque "
                  "mira arriba.", None)),
    ("decision", (2, "9 no es 6 dado vuelta", "El 6 sube y gotea; el 9 baja del fondo y termina en un corte.", None)),
    ("decision", (3, "» no es « en espejo", "Las dos se arman con su propio azar: cada ángulo es otro.", None)),
    ("p", "**Por qué.** En la litoescultura de Tiwanaku, las figuras enfrentadas casi nunca son idénticas (Agüero, "
          "Uribe y Berenguer 2003). Aquí la asimetría la decide la gravedad: un signo dado vuelta no puede gotear "
          "hacia arriba. _Retórica:_ quiasmo imperfecto; A B, B A′: el cruce nunca cierra."),
    ("verso", "la misma diosa dos veces\ny ninguna igual."),
    ("titulo", "Para la mano"),
    ("p", "Los seis son reconstruidos: se calcan en punteado y se repujan a puntos (Acciones 3 y 4)."),
]

TEXTOS["P-10"] = [
    ("titulo", "Qué se dibuja"),
    ("p", "El plan general de la caja, a 1:5: 8 × 7 compartimentos de una placa, con juntas de 3 mm. En cada uno, "
          "su signo, el número de su celda y el generador del que deriva."),
    ("titulo", "Decisiones"),
    ("decision", (1, "Solo caja baja", "**La decisión.** No hay mayúsculas: una mayúscula tecleada se escribe en caja "
                  "baja. **Por qué.** Las mayúsculas latinas son letras de monumento (Brookes), y el pie escribe en "
                  "mayúsculas justamente el nombre impuesto. La obra cambia el material del monumento por uno "
                  "doméstico; la letra cambia la del monumento por la de la mano.",
                  "le pusieron nombre,\notra manera de enterrar.")),
    ("decision", (2, "Cincuenta y seis celdas", "**La decisión.** 30 signos hallados, 25 reconstruidos y uno hecho. Lo "
                  "que no cabe se ve como celda vacía. **Por qué.** La caja mide lo que un paño de la pared de la "
                  "piscina ({caja_m}; D6). Ningún contenedor aguanta lo que contiene.", None)),
    ("decision", (3, "El orden", "**La decisión.** Primero lo hallado, por orden de aparición en el pie; después lo "
                  "reconstruido, en el orden en que lo pide el poema.", None)),
    ("decision", (4, "El ¶: con los dedos", "**La decisión.** La celda 56 no se dibuja: se hace sin punzón, con los "
                  "dedos, y se le propone a Rebeca (Acción 7). **Por qué.** De la boca sale un signo (D13). El "
                  "calderón marcaba dónde empezaba un párrafo; aquí va al final. _Retórica:_ paradoja.",
                  "Termina y empieza,\ntermina y empieza.")),
    ("decision", (5, "La puerta", "**La decisión.** La tapa tiene una sola puerta, calada sobre la celda 1. **Por "
                  "qué.** Como las puertas dibujadas en el pecho y en la espalda (D4).", None)),
    ("titulo", "Para la mano"),
    ("p", "La caja física es una bandeja de 8 × 7 compartimentos: cada uno guarda las placas de su signo y sus "
          "fichas. Las placas rotas van en su compartimento, junto a la que se hizo después."),
]


def bloques(codigo, M):
    out = []
    for tipo, cont in TEXTOS[codigo]:
        if tipo in ("p", "titulo"):
            cont = cont.format(**M)
        elif tipo == "decision":
            n, termino, texto, verso = cont
            cont = (n, termino.format(**M), texto.format(**M), verso)
        out.append((tipo, cont))
    return out
