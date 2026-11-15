import pathlib,sys
f=pathlib.Path(sys.argv[1]); t=f.read_text(encoding='utf-8')
R=[]
def r(a,b,n=1): R.append((a,b,n))
# --- pasteles hechos
r("y en esos lugares se sitúan los seis pasteles de la serie. De cada uno reproducimos el esquema de encaje, que es el trazado con que se fija la composición (figuras 1-6). Se trata de una investigación en desarrollo.",
  "y en esos lugares se sitúan los seis pasteles de la serie, que reproducimos como figuras 1 a 6.")
r("Los esquemas de encaje que reproducimos ilustran y especifican; descubrir, no descubren nada, aunque obligan a decidir.",
  "Los pasteles que reproducimos están más cerca de la ilustración que del hallazgo, porque no aportan datos nuevos sobre la novela, aunque obligan a decidir lo que el texto deja abierto.")
r("Por eso cada esquema anota, junto al trazo, lo que hace la mano,","Por eso el análisis de cada pastel anota, además de lo que muestra, lo que hizo la mano,")
r("lo que el esquema obliga a decidir","lo que el pastel obliga a decidir")
r("El esquema tiene que decidir desde dónde se mira","El pastel tiene que decidir desde dónde se mira")
r("y el esquema, sin descubrirlo, lo vuelve difícil de ignorar","y el pastel, sin descubrirlo, lo vuelve difícil de ignorar")
r("El esquema sigue al texto y dibuja un umbral sin montón.","El pastel sigue al texto y dibuja un umbral sin montón.")
r("El esquema los traza como mojones,","El pastel los traza como mojones,")
r("Los esquemas obligan a decidir lo que el texto deja abierto","Los pasteles obligan a decidir lo que el texto deja abierto")
r("Esquema de encaje del pastel al óleo. Fuente: elaboración propia con asistencia de IA.","Pastel al óleo sobre papel, [medidas, año]. Fuente: elaboración propia.",6)
r("el diseño y trazado de los esquemas de encaje (figuras 1-6) y de los diagramas (figuras 7 y 8),",
  "el diseño de los esquemas de encaje con que se compusieron los pasteles de las figuras 1 a 6, el trazado de los diagramas (figuras 7 y 8),")
# --- reescrituras de Codex
r("la mecánica material del despojo: cómo se pierde la tierra, con qué objetos y con qué gestos.",
  "la mecánica material del despojo, es decir, los objetos y los gestos con que se pierde la tierra.")
r("Más que una mano enfrentada a un papel, lo que hay son dos manos con dos agarres.",
  "Lo que la novela pone frente a frente son, entonces, dos manos con dos agarres, la que ara y la que firma.")
r("El narrador tampoco le ve cuartos a la casa: «Las chujllas no tienen cuartos ni mucho menos» (ibid.: 30).",
  "Para el narrador, «las chujllas no tienen cuartos ni mucho menos» (Botelho Gosálvez, 1982 [1945]: 30).")
r("Donde el narrador ve una madriguera, cualquiera de ellos vería una casa comprimida.",
  "Leídas con estos autores, las dependencias de los Huanca forman una casa comprimida donde el narrador solo ve una madriguera.")
r("de modo que lo que mueve el despojo tiene más que ver con la casta que con el tamaño.",
  "de modo que, al menos aquí, el despojo tiene más que ver con la casta que con el tamaño.")
r("señala «un Código Penal en infolio y un manual del Procedimiento Civil» y asegura",
  "señala «un Código Penal en infolio y un manual del Procedimiento Civil», un libro de gran formato y otro pequeño, y asegura")
r("(1) *Texto*. En alzado, el orden de las chujllas","(1) *Texto*. En alzado, que es la vista de frente, el orden de las chujllas")
r("Escribir, tejer y arar comparten así el vocabulario de la mano. En los Andes, además, el hilo servía para registrar.",
  "Escribir, tejer y arar comparten así el vocabulario de la mano, y en los Andes el hilo servía además para registrar.")
r("(the boundary marker, the dry wall, the heap)","(the boundary marker, the dry-stone wall, the heap)")
r("La sequía se cuenta con palabras de arquitecto y de dibujante.","La sequía, que en la novela precede al éxodo, se cuenta con palabras de arquitecto y de dibujante.")
r("| Agua, cascotes, montón (144, 154) |","| Agua (145, 152-153), cascotes (144), montón (154) |")
r("cada capa nos hace olvidar la anterior» (Fuão, 2011: 43).","cada capa nos hace olvidar la anterior» (Kolář, cit. en Fuão, 2011: 43).")
r("Del otro lado, las manos del puneño pierden su oficio: «Sabrás arar en la puna, pero aquí esa es otra música» (ibid.: 113).",
  "Del otro lado, las manos del puneño pierden su oficio, y en los Yungas a Paulo le advierten: «Sabrás arar en la puna, pero aquí esa es otra música» (ibid.: 113).")
bad=[(a[:60],t.count(a),n) for a,b,n in R if t.count(a)!=n]
if bad: print('MAL:',bad); sys.exit(1)
for a,b,n in R: t=t.replace(a,b)
f.write_text(t,encoding='utf-8'); print(len(R),'cambios')
