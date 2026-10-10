# 25. *A Pattern Language* frente al artículo

El 10 de octubre de 2026 pediste analizar *A Pattern Language* (Alexander, Ishikawa y Silverstein, 1977), ver en qué puede fortalecer, discutir o llevar más allá los argumentos del artículo, e iterar el artículo con ello. Aquí está el análisis, lo que ya cambié en el artículo y lo que queda propuesto.

**En corto:**

- **El libro sirve, sobre todo, en la sección 3 (la chujlla) y en la 7 (el retorno).** Le da al artículo una mirada de arquitecto para contestar al narrador. Donde él ve una madriguera, Alexander ve una casa comprimida. Y la posesión que la novela marca con piedras, Alexander la llama *control*.
- **Leyéndolo apareció un dato de la novela que el artículo no usaba.** Los Huanca no viven en una chujlla, sino en «tres chujllas de adobe y paja brava que rodean al patio» (p. 30). Cuando el narrador dice que «Las chujllas no tienen cuartos ni mucho menos», mide con la casa de ciudad: los cuartos son las chujllas.
- **También hay que discutirlo.** Alexander habla de patrones «arquetípicos» que valdrían para todas las culturas. Es otra manera de sacar a la chujlla de la historia, la que critica Cornejo Polar. Y su explicación del papeleo (las oficinas grandes) no explica Umacachi, que es una aldea.
- **El artículo cambió poco y queda en 49.969 caracteres.** Entraron dos ideas de Alexander, con su página, y una entrada de bibliografía. Para no pasar de 50.000 recorté dos frases y varios incisos que repetían o sobraban (§25.5).
- **Hay siete textos más listos para usar** si una revista da más espacio (§25.6). Hay también una propuesta de fondo: escribir los «patrones» del ayllu con el formato de Alexander, a partir de Bertonio y la novela (§25.4).

## 25.1. El libro y cómo se cita

**Qué es.** Un libro de 1977 con 253 «patrones», ordenados de la región a los detalles de construcción. Cada patrón describe «un problema que ocurre una y otra vez en nuestro entorno» y «el núcleo de la solución» (p. x). Todos tienen el mismo formato (pp. x-xi):

- una fotografía con un ejemplo «arquetípico»;
- un párrafo que lo une a los patrones mayores;
- el problema, en negrita;
- la evidencia;
- la solución, que empieza con «Therefore:» («Por lo tanto»);
- un diagrama;
- los patrones menores que lo completan.

Los autores marcan cada patrón con dos asteriscos, uno o ninguno, según cuánto confían en él (p. xiv). Dicen que cada patrón es «una hipótesis como las de la ciencia» (p. xv).

**Qué trae el archivo.** El OCR que enviaste (unos 5.000 párrafos) tiene la introducción completa (pp. ix-xliv), el índice de los 253 patrones y 59 patrones, no todos completos:

- 18-20, 26, 30, 31, 36, 40, 43, 45, 58, 63, 68, 69;
- 75, 76, 78, 79, 81, 82, 88, 92, 93, 100;
- 120-127, 129-136, 142, 150, 155, 157-159;
- 171-176, 185-187, 203, 204, 221 y 253.

Faltan algunos que interesarían mucho (§25.7).

**Cómo se fijó cada página.**

- El número de página va al pie y muchos faltan en el OCR.
- Las páginas impares llevan como cabeza el nombre del patrón y las pares, TOWNS o BUILDINGS. La primera página de cada patrón no lleva cabeza.
- Con esas tres pistas se reconstruyó la página de cada cita. Cuando la reconstrucción no es segura, se cita el número del patrón y no la página.
- El script `alexander_scripts/verificar.py` del scratchpad comprueba que cada frase citada está en el OCR y junto a qué marca de página cae. La tabla de §25.8 trae el original inglés de cada cita.

**Traducción.** No hay traducción castellana a mano. La de Gustavo Gili existe, pero no la tenemos. Las traducciones son nuestras, como dice la nota del artículo sobre las citas en inglés. Si consigues la edición castellana, conviene citarla.

**En el artículo** el libro se cita como Alexander et al. (1977), y en la bibliografía con sus tres autores principales.

## 25.2. Dónde fortalece el artículo

### 1. La chujlla de una sola habitación es una casa comprimida, no una madriguera (sección 3)

- **Qué dice la novela.** El narrador se queja: «Las chujllas no tienen cuartos ni mucho menos» (p. 30). Describe hollín, cuyes y camastros «morada de piojos y pulgas» (p. 31), y el artículo concluye que hace de la chujlla una madriguera.
- **Qué dice Alexander.**
  - Todos los patrones de una casa pueden estar, «de alguna forma», presentes y superpuestos «en una simple cabaña de una sola habitación» (p. xliii).
  - A esa superposición la llama *compresión*. Es «la economía de espacio más corriente» y la única manera de hacer edificios «que sean poemas» (pp. xliii-xliv).
  - En la casa pequeña, el truco es «comprimir los patrones» y «hacer que cada pulgada cuente doble». Bien hecha, una olla de sopa llena la casa, y eso «no puede ocurrir si el lugar está dividido en cuartos» (p. 391).
- **Lo que gana el artículo.** Un arquitecto del siglo XX defiende la habitación única por las mismas razones por las que el narrador la desprecia. La crítica al narrador deja de ser solo ética: también es técnica.
- **Cuidado.** El patrón 78, el de la casa pequeña, es para una persona sola. Por eso el artículo cita la frase general de p. xliii y no la de p. 391.
- **Estado:** integrado en la sección 3.

### 2. La casa de los Huanca es un conjunto alrededor de un patio (sección 3 y Figura 1)

- **Qué dice la novela, y el artículo no usaba.** Los Huanca viven «en tres chujllas de adobe y paja brava que rodean al patio que tiene mohines floridos con la presencia de varias kantutas», junto al corral y la parva (p. 30). De noche, Paulo está en su chujlla con su mujer y los hijos menores. Llama a gritos a los mayores, que estaban «en las chozas próximas», y ellos entran «en la cabaña» (p. 31).
- **Qué dice Alexander.**
  - Llama *gradiente de intimidad* a la secuencia que va de lo público a lo íntimo. Sin ella, las visitas «siempre serán un poco incómodas» (p. 610).
  - Lo estudió en casas populares peruanas, «un caso que hemos estudiado en detalle» (p. 610). En una fiesta, algunos «ni siquiera pasan del umbral de la puerta» y cada persona «sabe exactamente hasta dónde puede penetrar en la casa» (p. 611).
  - Compara ese orden con el de un *compound* africano (p. 611).
- **Lo que gana el artículo.**
  - El gradiente existe, pero no está dentro de una chujlla: está entre chujllas, a través del patio.
  - El narrador busca cuartos dentro de un edificio y no ve que los cuartos son edificios.
  - El narrador, que entra hasta los camastros, se salta el gradiente que los propios hijos respetan.
- **Estado:**
  - Entró el dato de las tres chujllas y la frase «los cuartos son las chujllas».
  - El gradiente quedó fuera por extensión; el texto está listo en §25.6, texto 1.

### 3. La comida y el fuego al centro (sección 3 y Figura 1)

- **Qué dice la novela.** Los braseros arden «en el centro del cuarto» (p. 30). La familia se reúne alrededor del fuego, con Paulo «en cuclillas, cerca del fuego» y los hijos «frente a sus padres», para decidir que los mayores se vayan (p. 32).
- **Qué dice Alexander.**
  - Para el lugar común de un grupo, lo más básico es «la comida y el fuego» (p. 621).
  - Ese lugar común es «quizá el patrón más básico que hay para formar la cohesión de un grupo» (p. 620).
  - Para que la gente se siente en círculo, «el fuego, sobre todo, ayuda a anclar» ese círculo (p. 859).
- **Lo que gana el artículo.**
  - Respalda la decisión de la Figura 1: el corte va a la altura de quien está en cuclillas junto al brasero, que es la postura de Paulo (p. 32).
  - La notación ya lo anota (documento 23).
  - Muestra además que el fuego no es solo calor ni hollín: es el lugar donde la familia decide el éxodo.
- **Estado:** no entró en el texto, por extensión (§25.6, texto 3). La Figura 1 ya lo dibuja.

### 4. Poseer es controlar y reparar (secciones 1, 3 y 7)

- **Qué dice Alexander.**
  - Los procesos que fomentan la especulación con la tierra «invitan a tratar las casas como mercancías» (p. 394).
  - Pide poner el acento de la propiedad «en el control, no en la propiedad financiera» (p. 395).
  - Pide dar a la gente «el poder legal y la oportunidad física de modificar y reparar sus propios lugares» (p. 395).
  - Y en general, quien construye algo tiene que «reparar el mundo a su alrededor, y dentro de él» (p. xiii).
- **Qué dice la novela.**
  - Juan Condori recibe una chujlla abandonada y la hace suya con las manos: «repuso la techumbre de paja, limpió los abrojos, rehizo los valladares de piedra que cercaban el corral» (p. 35).
  - En el retorno, «Las chujllas fueron reparadas del estrago, las pircas de piedra que separan las parcelas fueron compuestas» (p. 156): la casa y el lindero a la vez, como pide Alexander en p. xiii.
  - Y en Kero-Pata, «así lo declaraban los papeles del Gobierno» (pp. 36-37).
- **Lo que gana el artículo.**
  - La tesis «ante la ley, un mojón no vale lo que un título» (sección 1) recibe un nombre.
  - Alexander une dos cosas que la novela separa: el poder legal, que está en los papeles, y la oportunidad física, que está en las manos.
  - La piedra, el papel y la máquina se vuelven tres maneras de poseer: control, título y mercancía.
- **Estado:** integrado en la sección 7, en dos frases.

### 5. El umbral se hincha al llegar y al partir (secciones 3 y 7)

- **Qué dice Alexander (patrón 130, pp. 622-623).** Al llegar o al partir, el tiempo «parece hincharse» respecto de los minutos de antes y de después, y el espacio de la entrada debe hincharse con él. La página exacta es dudosa: hay que confirmarla en el impreso.
- **Qué dice la novela.**
  - Paulo despide a sus hijos «desde el portal de su chujlla», rodeado de su familia (p. 34).
  - Los que vuelven se arrodillan «en el dintel de Jatun-Kolla» para besar el suelo (p. 155).
- **Lo que gana el artículo.**
  - La frase de la sección 7, «El ayllu tiene dintel: es una casa», se apoya en un patrón de arquitecto.
  - El dintel une el portal de la despedida, que ya está en el Cuadro 1, con el retorno.
- **Estado:** propuesto (§25.6, texto 4), con la página por confirmar.

### 6. Las cosas de la vida colgadas de las vigas (sección 3)

- **Qué dice la novela.** De las vigas cuelgan «las hoces, el arado, el yugo de madera, los ponchos y rebozos para los días de fiesta»; los pinquillos y charangos dormitan «en espera de la mano que les acaricie» (p. 31).
- **Qué dice Alexander.**
  - Un cuarto vale cuando es «la expresión viva de una persona, o de un grupo de personas», donde se ven «sus vidas, sus historias» (p. 1165).
  - La decoración es más bella cuando sale de la propia vida: «las cosas que te importan, las cosas que cuentan tu historia» (p. 1166).
- **Lo que gana el artículo.** El inventario del narrador es, sin que él lo sepa, el retrato de una familia: trabajo, fiesta y música. Refuerza la frase del artículo sobre la caja de herramientas (Cárcamo Pino, 2025a: 12).
- **Estado:** propuesto (§25.6, texto 5).

## 25.3. Dónde hay que discutirlo

### 1. El arquetipo también saca a la chujlla de la historia

- **El problema.**
  - Alexander cree que muchos de sus patrones son «arquetípicos», tan arraigados «en la naturaleza de las cosas» que valdrán dentro de quinientos años (p. xvii).
  - Del gradiente de intimidad dice que es «un principio de orden casi arquetípico para todos los edificios del hombre» (p. 611).
  - Habla de culturas «tradicionales y primitivas» (p. 861).
- **Por qué importa.** Es lo que Cornejo Polar critica en el narrador indigenista: imaginar la vida india «más en términos de naturaleza que de historia» (2003 [1994]: 180). El narrador convierte a los comunarios en piedra; Alexander convertiría la chujlla en arquetipo. Uno desprecia y el otro admira, pero los dos miran desde fuera.
- **El mismo hecho, dos valores.** El narrador ve en los camastros compartidos «morada de piojos y pulgas» y «revolcones amorosos» (p. 31). Alexander, que no conoce la chujlla, celebra el sueño compartido de las aldeas indias, donde los hombres sacan las camas al patio al anochecer (p. 861), y propone dormir todos juntos «cerca del fuego» (p. 863).
- **Cómo lo resuelve el artículo.**
  - Usa a Alexander solo para contestar al narrador.
  - En la sección 8 lo pone en la lista de las «maneras de ver ajenas al mundo narrado», junto al corte, el *capriccio*, Bacon, la tectónica y la pelvis. Es la advertencia de Hall.
  - El texto completo de la crítica quedó listo en §25.6, texto 2.

### 2. El papeleo no se explica por el tamaño

- **Qué dice Alexander (patrón 81).**
  - Las oficinas no funcionan si son grandes. Cuando la gente ya no puede tratarse cara a cara, necesita reglamentos, que en los escalones bajos se cumplen «a ciegas y al pie de la letra» (p. 405).
  - Propone oficinas de doce personas como máximo.
- **Por qué Umacachi lo desmiente.**
  - Es una aldea: un alcalde, una subprefectura, unos tinterillos.
  - Vicente trata en persona con el tinterillo (pp. 104-105), y el papel despoja igual.
  - Lo que decide no es el tamaño, sino la casta: a los mestizos «no les alcanzaba la Ordenanza» (p. 102).
- **Lo que sí se cumple.** Su segundo remedio: cuando el cliente tiene una relación activa con la institución, esta «pierde su poder de intimidarlo» (p. 405). Es lo que hicieron las comunidades que desenterraron sus títulos coloniales y se aliaron con tinterillos (Rivera Cusicanqui, 2010 [1984]: 99, 101). La novela lo calla, como dice el artículo.
- **Estado:** propuesto (§25.6, texto 6).

### 3. La estaca y el papel no valen lo mismo

- **Qué dice Alexander.**
  - Al terminar el diseño, uno tiene un esquema de espacios «marcado en el suelo, con estacas, o en un papel» (p. xxxi). Para él son dos soportes equivalentes del mismo plano.
  - Después pide «poner estacas en el suelo para marcar las columnas» (p. xxxii).
  - Para las puertas y ventanas va más lejos: solo se fijan en obra, a ojo, con cuerdas; «es imposible hacerlo en el papel» (p. 1047).
- **Qué dice la novela.** La estaca y el papel no valen lo mismo:
  - Pedro Villca «empotró en el suelo del ayllu las estacas de propiedad» (p. 20);
  - en Kero-Pata, el doctor gana por «una gran cuestión de títulos, papel sellado y pago de impuestos» (pp. 36-37).
- **Lo que gana el artículo.** Alexander, como arquitecto, prefiere la obra al papel, igual que el ayllu. Pero su libro ignora la otra cara: ante la ley, el papel le gana a la estaca. Es la regla del juego de piedra, papel o tijera de la sección 1.
- **Estado:** solo en este documento.

### 4. Alexander teme a su propio libro

- **Qué dice Alexander.**
  - Se pregunta si no hay el peligro de que la gente confíe en «este único lenguaje impreso» en vez de desarrollar los suyos (p. xvi).
  - Dice que los lenguajes que la gente tiene hoy son «tan brutales y tan fragmentados» que casi nadie tiene ya un lenguaje (p. xvi).
- **Con qué se cruza.**
  - Con el «libro fetiche» de Cornejo Polar (2003 [1994]: 41), que el artículo ya cita para el infolio del tinterillo.
  - Con el «monopolio de la escritura» de Cárcamo Pino (2025b: 259).
  - Y con la novela: en los Yungas, al puneño le dicen «Sabrás arar en la puna, pero aquí esa es otra música» (p. 113). Sus manos tienen un lenguaje que allí no sirve.
- **Lo que gana el artículo.** Un argumento para el *manuaje*: el lenguaje de patrones de Alexander es un lenguaje para construir con las manos. El ayllu tenía uno, que Bertonio dejó escrito a medias.
- **Estado:** solo en este documento; base para la propuesta de §25.4.

### 5. La casa propia frente a la tierra del ayllu

El patrón 79 piensa en el hogar de una familia y en su parcela: cada casa debe ser «de alguna manera» de quienes viven en ella (p. 394). El ayllu es otra cosa: tierra de la comunidad, con parcelas separadas por pircas. Por eso el artículo usa de Alexander solo la idea de control y reparación, no su modelo de propiedad. El patrón de la tierra común, COMMON LAND (67), no está en el OCR.

## 25.4. Cómo llevarlo más allá

### 1. Escribir los patrones del ayllu con el formato de Alexander

Es la propuesta de fondo, para una revisión mayor, una figura o un segundo artículo. Alexander invita a hacerlo: pide añadir patrones propios y cambiarles el nombre para hacer el lenguaje «propio» (pp. xxxix-xl). La idea es invertir la dirección: no aplicar patrones universales al ayllu, sino escribir con el formato de Alexander los patrones que la novela y Bertonio registran.

Cada patrón llevaría:

- el problema, tomado de la novela;
- la solución, tomada de Bertonio;
- lo que hace el narrador con él;
- un grado de apoyo, como los asteriscos de Alexander:
  - ** si está en la novela y en Bertonio;
  - * si está en una de las dos;
  - sin asterisco si es una decisión del dibujo.

| Patrón | Problema (novela) | Solución (Bertonio u otra fuente) | El narrador | Apoyo |
|---|---|---|---|---|
| CHHAXWA, la piedra que se saca y la piedra que ata | La tierra «pare» piedras (p. 9) | La misma palabra para las piedras del despedre y para la que ata el techo (p. 330) | «erial de piedras» (p. 9) | ** |
| SAYWA, el mojón que cuida | Mojones «desde tiempos antiguos» (p. 9); tres vigías en el ayllu vacío (pp. 75, 79) | *saywa*: montón por mojón y «amparo, defensor» (p. 447); *saywaña*: amojonar (p. 466) | «cancerberos», «muertos en vida» (p. 80) | ** |
| TRES CHUJLLAS ALREDEDOR DEL PATIO | Una familia de doce (p. 30) | Tres chujllas, patio, corral y parva (p. 30); gradiente de Alexander (pp. 610-611) | «no tienen cuartos ni mucho menos» (p. 30) | * |
| EL FUEGO AL CENTRO | Decidir quién se va (pp. 31-32) | Brasero «en el centro del cuarto» (p. 30); «la comida y el fuego» (Alexander: 621) | hollín, «aire pesado» (p. 32) | * |
| APACHITA, el montón que crece con cada viajero | Cruzar la cordillera (p. 109) | Montón «que van haciendo los caminantes» (p. 317) y coca pegada (p. 349) | Muralla y cuerpo clavado (pp. 108-109) | * |
| PIRCA DE DOBLE CARA | Rehacer los linderos (p. 156) | Piedrecilla «legión» que baja a las pircas (p. 8) | «voluntad de siglos de piedra» (p. 156) | sin asterisco: la doble cara es analogía del dibujo |
| DINTEL DEL AYLLU | Partir y volver (pp. 34, 155) | Portal de la chujlla, dintel del ayllu; patrón 130 de Alexander | Escena de arrepentimiento (p. 155) | * |

- **Lo que se gana.** El artículo dejaría de oponer solo la mano al papel. Mostraría que el ayllu tenía un lenguaje de patrones, que la novela registra a pedazos y que el vocabulario de 1612 deja nombrado.
- **El límite.** Bertonio es un jesuita y el formato es de Alexander. Sería una herramienta de lectura, no la teoría aymara del espacio que la sección 8 dice que el artículo no puede dar.

### 2. Un grado de apoyo para cada figura

El formato de Alexander se parece mucho a los tres planos de cada figura del artículo:

- la fotografía es el pastel;
- el problema es el *Texto*;
- la solución es la *Operación*;
- los patrones menores son las otras figuras.

Lo que el artículo no tiene son los asteriscos. Se podría añadir a cada *Contraste* un grado, o una columna al Cuadro 1:

| Figura | Decisión principal | Apoyo |
|---|---|---|
| 1 | Corte en cuclillas junto al brasero | En la novela (p. 32) |
| 1 | Perfil de cráneo | Decisión del dibujo |
| 2 | El signo no encaja en la pendiente | En la novela (pp. 6, 35) |
| 3 | La apacheta como umbral sin montón | Contraste con Bertonio (pp. 317, 349) |
| 4 | La mina como doble invertido del ayllu | Lectura sobre datos de la novela (pp. 134-154) |
| 5 | La tierra como pelvis | Decisión del dibujo; la tierra madre, en Bertonio (p. 420) |
| 6 | Los vigías como mojones | Decisión respaldada por Bertonio (pp. 307, 447) |

En las notaciones, el asterisco ya marca la «decisión del dibujo» (documento 23). Si se adopta la escala de Alexander, hay que cambiar ese signo: en Alexander, más asteriscos quieren decir más confianza.

### 3. El retorno como reparación del lugar

Si hay espacio, la sección 7 o la Figura 7 pueden leer el retorno como reparación del lugar, con dos ideas:

- quien construye repara el mundo alrededor y dentro de lo construido (p. xiii);
- la propiedad se define por el control y la reparación (p. 395).

La novela da las dos escenas: Condori arreglando la chujlla abandonada (p. 35) y el ayllu arreglando chujllas y pircas (p. 156). La Figura 6 ya habla del cuidado de los vigías como «trabajo de mantenimiento»: el hilo existe.

### 4. Construir sobre la roca para dejar la tierra buena (por verificar)

Las chujllas de las familias antiguas «han trepado en los riscos del cerro» (p. 6), y el ayllu está «en la planta de una alta y rojiza peñería» (p. 6). El artículo dice que la jerarquía que ve el narrador es una lectura de la pendiente.

Hay otra lectura posible: construir en la peor tierra para dejar la mejor a la siembra. Es lo que propone el patrón SITE REPAIR (104), que no está en el OCR. El índice del libro lo presenta como el momento de fijar los edificios «según la naturaleza del sitio» (p. xxvi), y el patrón 171 lo recuerda como el que deja intactos los árboles (p. 799).

No lo uses hasta leer el patrón completo en el impreso.

## 25.5. Qué cambió en el artículo

| Lugar | Cambio | Caracteres |
|---|---|---|
| Sección 3, tras la Figura 1 | Párrafo nuevo: «El narrador tampoco le ve cuartos [...]. Pero los Huanca viven en “tres chujllas de adobe y paja brava que rodean al patio” (ibid.): los cuartos son las chujllas. Para Christopher Alexander, todos los patrones de una casa caben, superpuestos, “en una simple cabaña de una sola habitación” (Alexander et al., 1977: xliii). Donde el narrador ve una madriguera, él vería una casa comprimida.» | +443 |
| Sección 7, tras *saywaña* | «Alexander define la propiedad por el control, no por el dinero, y pide “el poder legal y la oportunidad física de modificar y reparar sus propios lugares” (Alexander et al., 1977: 395). La novela las separa: el poder, en los papeles; la oportunidad, en las manos.» | +263 |
| Sección 8, primer límite | Alexander entra en la lista de las maneras de ver ajenas al mundo narrado | +11 |
| Bibliografía | Alexander, Ishikawa y Silverstein (1977), Oxford University Press | +159 |
| Sección 1, último párrafo | «La lectura se hace desde la arquitectura y el dibujo, con las herramientas de ese oficio [...]. Primero [...]. Segundo [...]. Tercero» pasa a «La lectura parte de tres premisas [...]. Y si dibujar es» | recorte |
| Sección 1, nota del pastel | Sale el inciso «A diferencia de la tinta, que fija la línea al secar» | recorte |
| Sección 3 | Salen «en la falda del cerro» (repetía «los riscos del cerro») y «Hasta los edificios son cómplices.» (lo dice ya la cita de la iglesia y la hacienda) | recorte |
| Sección 3, Figura 1 | La cita de p. 65 pasa a «ibid.», porque el párrafo ya citaba la novela; en el plano (3), «el texto ofrece dos lugares» pasa a «el texto ofrece dos» | recorte |
| Sección 2 | «recuerda además que» pasa a «recuerda que» | recorte |
| Sección 4 | «en la historia real» pasa a «en la historia» | recorte |
| Sección 5 | El aserradero conserva la mano cercenada y pierde el inciso «y solo lo anota en la planilla cuando Paulo se ofrece como “peón, siquiera”» | recorte |
| Sección 6 | Sale «Pronto, “cielo y tierra eran para ellos como una tremenda cárcel” (ibid.: 72).» | recorte |

- **Extensión:** de 49.549 a 49.969 caracteres con espacios. Sigue bajo los 50.000 de *Estudios Bolivianos*, con poco margen: cualquier añadido pide un recorte igual.
- **Lo que no se tocó:** la frase «Se trata de una investigación en desarrollo» se queda, porque las normas de *Estudios Bolivianos* piden decirlo al inicio (documento 01).
- **Palabras:** unas 8.370, incluidos títulos, resúmenes, pies y bibliografía. *Atenea*, primera del informe de convocatorias, pide hasta 8.500 con resumen y bibliografía; su versión se ajustará al enviarla.
- **Comprobaciones:**
  - las 147 citas de la novela están en su página, sin problemas;
  - las de Bertonio y las demás fuentes también, salvo la línea de Cornejo Polar de siempre, que el cotejo marca como aproximada;
  - los «ibid.» nuevos apuntan a la novela;
  - las dos citas de Alexander están en el OCR en las páginas indicadas (§25.8).
- **Word con cambios marcados.** `articulo/articulo_cosecha_de_piedras_cambios.docx` compara ahora con la versión anterior a Alexander, para que veas solo estos cambios.

## 25.6. Textos listos para usar si hay más espacio

Las cifras son el aumento aproximado de extensión. Las citas están verificadas como en §25.8.

1. **El gradiente (sección 3, tras «los cuartos son las chujllas»), +250:**
   > De noche, los hijos mayores están en las chozas próximas y entran en la del padre cuando él los llama (ibid.: 31). Alexander, que estudió casas populares peruanas, llama a ese orden *gradiente de intimidad*: cada persona «sabe exactamente hasta dónde puede penetrar en la casa» (Alexander et al., 1977: 611).
2. **La crítica del arquetipo (sección 3, al final del párrafo nuevo), +190:**
   > Pero también él mira de fuera: llama a su gradiente un principio «casi arquetípico» (Alexander et al., 1977: 611), y el arquetipo, como la naturaleza que critica Cornejo Polar, saca a la chujlla de la historia.
3. **El fuego al centro (Figura 1, plano 2 o 3), +200:**
   > El corte va a la altura de Paulo Huanca, «en cuclillas, cerca del fuego», cuando reúne a sus hijos para decidir quién se va (Botelho Gosálvez, 1982 [1945]: 32). Para Alexander, lo más básico de un lugar común es «la comida y el fuego» (Alexander et al., 1977: 621).
4. **El umbral (sección 7, tras «El ayllu tiene dintel: es una casa»), +260. Antes, confirmar la página en el impreso:**
   > Para Alexander, al llegar o al partir el tiempo «parece hincharse», y la entrada debe hincharse con él (Alexander et al., 1977: 622-623). La novela lo cumple en las dos puntas: Paulo despide a sus hijos desde el portal de su chujlla (Botelho Gosálvez, 1982 [1945]: 34).
5. **Las cosas de la vida (sección 3, tras la caja de herramientas), +220:**
   > Para Alexander, un cuarto vale cuando deja ver «las cosas que cuentan tu historia» (Alexander et al., 1977: 1166). De las vigas cuelgan, además, «los ponchos y rebozos para los días de fiesta», y los charangos esperan «la mano que les acaricie» (Botelho Gosálvez, 1982 [1945]: 31).
6. **El papeleo (sección 4, al final del párrafo de la «bestia opresora»), +310:**
   > Alexander explica el papeleo por el tamaño: cuando la gente ya no puede tratarse cara a cara, los reglamentos se cumplen «a ciegas» (Alexander et al., 1977: 405). Umacachi lo desmiente: es una aldea, Vicente trata en persona con el tinterillo y el papel despoja igual. No lo mueve el tamaño, sino la casta.
7. **La reparación (sección 7, tras la frase de Alexander), +170:**
   > Es lo que Alexander pide a todo el que construye: «reparar el mundo a su alrededor, y dentro de él» (Alexander et al., 1977: xiii).

**Cómo hacer sitio:**

- Para *Literatura y Lingüística* o *Estudios Filológicos* (9.000 palabras) y *Kipus* (9.500), caben casi todos sin cortar.
- Para *Estudios Bolivianos* (50.000 caracteres) no cabe ninguno sin recortar en otra parte.
- Mi orden de prioridad es 1, 2 y 3.

## 25.7. Qué hay que verificar en el impreso

Estos patrones no están en el OCR y podrían servir. Antes de citarlos hay que leerlos en el libro:

| Patrón | Por qué interesa |
|---|---|
| SACRED SITES (24) | Los lugares sagrados como política de la comunidad: la huaca del techo (p. 10), la *wank'a* |
| ACCESS TO WATER (25) | La sequía y las vertientes secas (pp. 57-58) |
| HOUSE CLUSTER (37) | Las chujllas agrupadas por familias |
| HOLY GROUND (66) | El sacrificio de la llama en los campos colectivos (p. 157) |
| COMMON LAND (67) | La tierra del ayllu frente a la casa propia del patrón 79 |
| GRAVE SITES (70) | Las tumbas de piedras (p. 35), el pesebre (p. 106), los pedazos de Basilio (p. 69). En el índice, las tumbas van en la tierra común junto a las casas (p. xxiii) |
| ANIMALS (74) | El corral, el pesebre, las ovejas |
| SITE REPAIR (104) | Construir en los riscos para dejar la tierra buena (§25.4, punto 4) |
| CONNECTION TO THE EARTH (168) | La chujlla de muros de piedra «del cerro» (p. 8) |
| ALCOVES (179) y BED ALCOVE (188) | Los camastros contra la pared (pp. 30-31) |
| THE FIRE (181) | El brasero al centro (p. 30) |
| PAVING WITH CRACKS BETWEEN THE STONES (247) | La «piedrecilla menuda» y el suelo pedregoso |

Hay tres más que sí están en el OCR y quedaron como notas:

- **SECRET PLACE (204).** Un lugar escondido en la casa «donde se guarden los archivos de la casa». Podría leerse junto a los títulos coloniales que las comunidades desenterraron (Rivera Cusicanqui, 2010 [1984]: 99). La página del patrón no se pudo fijar.
- **MARRIAGE BED (187).** Ulises prueba quién es con la cama que él mismo construyó sobre un olivo vivo, que nadie puede mover. Es una imagen del lugar con dueño, como la *wank'a*. Es solo una analogía, y la página no se pudo fijar.
- **LIFE CYCLE (26).** Cada comunidad debe tener los lugares que marcan el paso de una edad a otra (p. 145). En Umacachi, el cura y el municipio cobran el entierro, y los Villca entierran a sus hijos bajo el pesebre (p. 106).

## 25.8. Citas verificadas

Original inglés según el OCR, con las erratas del OCR corregidas («intimídate» → «intimidate»). La traducción es nuestra. La línea es la de `apl.txt` en el scratchpad.

| Página | Original | Traducción | Línea |
|---|---|---|---|
| x | «unless they are made by all the people in society, and unless these people share a common pattern language» | «a menos que los haga toda la gente de la sociedad, y a menos que esa gente comparta un lenguaje de patrones común» | 130 |
| x | «Each pattern describes a problem which occurs over and over again in our environment, and then describes the core of the solution» | «Cada patrón describe un problema que ocurre una y otra vez en nuestro entorno, y luego describe el núcleo de la solución» | 132 |
| xiii | «must also repair the world around it, and within it» | «reparar el mundo a su alrededor, y dentro de él» | 164 |
| xv | «each pattern may be looked upon as a hypothesis like one of the hypotheses of science» | «cada patrón puede verse como una hipótesis como las de la ciencia» | 185 |
| xvi | «a danger that people might come to rely on this one printed language» | «el peligro de que la gente confíe en este único lenguaje impreso» | 193 |
| xvi | «so brutal, and so fragmented» | «tan brutales y tan fragmentados» | 194 |
| xvii | «Many of the patterns here are archetypal—so deep, so deeply rooted in the nature of things» | «Muchos de estos patrones son arquetípicos: tan hondos, tan arraigados en la naturaleza de las cosas» | 201 |
| xxxi | «either marked on the ground, with stakes, or on a piece of paper» | «marcado en el suelo, con estacas, o en un papel» | 605 |
| xxxii | «put stakes in the ground to mark the columns on the site» | «poner estacas en el suelo para marcar las columnas» | 628 |
| xliii | «all the patterns for a house might, in some form be present, and overlapping, in a simple one-room cabin» | «todos los patrones de una casa pueden estar, de alguna forma, presentes y superpuestos en una simple cabaña de una sola habitación» | 799 |
| xliv | «the only way of using a pattern language to make buildings which are poems» | «la única manera de usar un lenguaje de patrones para hacer edificios que sean poemas» | 806 |
| 145 | «the full slate of settings which best mark the ritual crossing of life from one stage to the next» | «todos los lugares que mejor marcan el paso ritual de una etapa de la vida a la siguiente» | 1241 |
| 390 | «it need only be one room» | «basta con que sea una habitación» | 2434 |
| 391 | «to compress the patterns [...]; to make every inch count double» | «comprimir los patrones [...]; hacer que cada pulgada cuente doble» | 2441 |
| 391 | «This cannot happen if the place is divided into rooms» | «Esto no puede ocurrir si el lugar está dividido en cuartos» | 2441 |
| 394 | «invite people to treat houses as commodities» | «invitan a tratar las casas como mercancías» | 2487 |
| 395 | «Keep the emphasis in the definition of ownership on control, not on financial ownership» | «Pongan el acento de la propiedad en el control, no en la propiedad financiera» | 2500 |
| 395 | «give people the legal power, and the physical opportunity to modify and repair their own places» | «el poder legal y la oportunidad física de modificar y reparar sus propios lugares» | 2500 |
| 405 | «these formal regulations are followed blindly and narrowly» | «esos reglamentos se cumplen a ciegas y al pie de la letra» | 2552 |
| 405 | «the institution loses its power to intimidate them» | «la institución pierde su poder de intimidarlos» | 2553 |
| 610 | «an example from Peru—a case which we have studied in detail» | «un ejemplo del Perú, un caso que hemos estudiado en detalle» | 3238 |
| 611 | «some do not even get beyond the threshold of the front door» | «algunos ni siquiera pasan del umbral de la puerta» | 3243 |
| 611 | «knows exactly how far into the house he may penetrate» | «sabe exactamente hasta dónde puede penetrar en la casa» | 3243 |
| 611 | «It is almost an archetypal ordering principle for all man's buildings» | «Es un principio de orden casi arquetípico para todos los edificios del hombre» | 3246 |
| 620 | «It is perhaps the most basic pattern there is in forming group cohesion» | «Es quizá el patrón más básico que hay para formar la cohesión de un grupo» | 3342 |
| 621 | «Most basic of all to common areas are food and fire» | «Lo más básico de los lugares comunes es la comida y el fuego» | 3372 |
| 622-623 | «the time of arriving, or leaving, seems to swell» | «el momento de llegar, o de partir, parece hincharse» | 3389 |
| 859 | «The fire especially helps to anchor a sitting circle» | «El fuego, sobre todo, ayuda a anclar un círculo de asientos» | 4686 |
| 861 | «in Indian villages during the dry season the men pull their beds into the compound at sundown» | «en las aldeas de la India, en la estación seca, los hombres sacan las camas al patio al anochecer» | 4720 |
| 863 | «in the common area near the fireplace» | «en el lugar común cerca del fuego» | 4742 |
| 1047 | «It is impossible to do it on paper» | «Es imposible hacerlo en el papel» | 4916 |
| 1165 | «the living expression of a person, or a group of people, so that you can see their lives, their histories» | «la expresión viva de una persona, o de un grupo de personas, donde se ven sus vidas, sus historias» | 5010 |
| 1166 | «the things you care for, the things that tell your story» | «las cosas que te importan, las cosas que cuentan tu historia» | 5024 |

**Las páginas menos seguras:**

- **pp. 610-611.** La marca de p. 610 falta. La frase del Perú va antes de la cabeza de p. 611.
- **p. 621.** Se deduce de la cabeza «129 COMMON AREAS AT THE HEART» y de la marca 624.
- **pp. 622-623.** El patrón 130 ocupa esas dos páginas y no se sabe en cuál cae la frase.
- **p. 391.** Se deduce de la cabeza «78 HOUSE FOR ONE PERSON» tras la marca 390.
- **pp. 394-395.** Se deducen de las cabezas TOWNS y «79 YOUR OWN HOME» tras la marca 390.

Las dos páginas que usa el artículo, xliii y 395, están entre marcas o cabezas claras.
