"""La taxonomía de las referencias de Contenida: los datos de las láminas R.

El método viene de un reel de Jason Murray (Modern Art Direction), «A Taxonomy of
Visuals»: clasificar las imágenes por el mecanismo que activan, no por su estilo,
en cuatro niveles (operación, dominio, técnica, ejecución). Aquí se toma con
cuidado: se conserva lo que sirve, se deja lo que no y se suma lo que le falta
para este proyecto (la huella, la procedencia, lo que no se toma, lo visto y lo
no visto, y un quinto nivel: dónde cae en Contenida).

Las referencias son las de 10_imagenes_de_dominio_publico.md. Ninguna la vio la
máquina: cuando mires una en su archivo, cambia su `mirada` a True y rehace las
láminas. Su marca pasa de puntos a línea continua, como lo hallado.
"""

# ---------------------------------------------------------------- la fuente del método

FUENTE = dict(
    autor="Jason Murray",
    obra="«A Taxonomy of Visuals»",
    medio="un reel de Instagram de Modern Art Direction, 2026 (1 min 42 s)",
    nota="No se encontró una página del método: se trabaja con el reel y con la descripción que trajiste.",
)

ENLACES_FUENTE = [
    ("el podcast Modern Art Direction", "https://podcastrepublic.net/podcast/1788684591"),
    ("Art Director Toolbox", "https://toolbox.super.site/articles"),
]

# ---------------------------------------------------------------- el método, nivel por nivel
# estado: toma, cambia, deja, no (lo que el proyecto no hace) o suma (lo que el reel no trae)

METODO = [
    ("toma", "clasificar por el mecanismo, no por el estilo"),
    ("toma", "del encargo a la referencia"),
    ("toma", "un cuadro de muchos a muchos"),
    ("toma", "juntar por gusto no es un método"),
    ("cambia", "Linneo, como imagen: solo procedimientos"),
    ("deja", "destacar, llamar la atención"),
    ("deja", "un grafo en Obsidian o en Notion"),
]

NIVELES = [
    dict(n="01", nombre="Operación", murray="Operation", reel="Differentiate · Group · Sequence · Infer",
         ideas=[("toma", "las cuatro operaciones"), ("suma", "una figura retórica para cada una")]),
    dict(n="02", nombre="Dominio", murray="Domain",
         reel="Feature · Grouping · Space · Social · Semantic · Cultural",
         ideas=[("cambia", "seis, siete: cuatro cambian de nombre"), ("suma", "la huella")]),
    dict(n="03", nombre="Técnica", murray="Technique", reel="41 técnicas",
         ideas=[("toma", "15 se toman"), ("cambia", "6 cambian"), ("deja", "13 se dejan"),
                ("no", "7 no se hacen"), ("suma", "7 se suman")]),
    dict(n="04", nombre="Referencia", murray="Execution", reel="campañas: Loewe, Jacquemus, Absolut, WWF, Esquire",
         ideas=[("cambia", "obras de dominio público"), ("suma", "su procedencia"), ("suma", "lo que no se toma"),
                ("suma", "visto y no visto")]),
    dict(n="05", nombre="En Contenida", murray="—", reel="no está",
         ideas=[("suma", "dónde cae: la acción, el plano o la regla")]),
]

# ---------------------------------------------------------------- lo que muestra el reel

OPERACIONES_MURRAY = [("Differentiate", "Diferenciar"), ("Group", "Agrupar"), ("Sequence", "Secuenciar"),
                      ("Infer", "Inferir")]

# los seis dominios del reel y en qué se convierten aquí: (inglés, español, estado, dominio de Contenida)
DOMINIOS_MURRAY = [
    ("Feature", "Rasgo", "cambia", "materia"),
    ("Grouping", "Agrupación", "toma", "estructura"),
    ("Space", "Espacio", "cambia", "tiempo"),
    ("Social", "Social", "cambia", "mano"),
    ("Semantic", "Semántico", "toma", "sentido"),
    ("Cultural", "Cultural", "cambia", "procedencia"),
]

# las técnicas que se leen en el reel, por dominio: (español, inglés, estado, dónde ya trabaja en Contenida o por qué no)
# estado: toma, cambia (se toma cambiada), deja (no sirve aquí) o no (el proyecto no lo hace)
TECNICAS_MURRAY = {
    "Rasgo": [
        ("Textura contra plano", "texture against flat", "toma", "el relieve de la placa (P-02 · 5)"),
        ("Claroscuro", "chiaroscuro", "cambia", "la luz rasante: para leer el relieve (Acciones 2 y 4)"),
        ("Aislamiento en el vacío", "isolation in void", "cambia", "la coma sola en la puerta de la tapa (Acción 5)"),
        ("Pares complementarios", "complementary pairing", "deja", "el color es material (03, §3.9)"),
        ("Pop-out", "pop-out", "deja", "llamar la atención"),
        ("Luz de contorno", "rim light", "deja", "llamar la atención"),
        ("Bloques de saturación", "saturation blocking", "deja", "el color es material (03, §3.9)"),
        ("Silueta", "silhouette", "deja", "se calca el contorno, no el relleno (Acción 3)"),
        ("Contraste simultáneo", "simultaneous contrast", "deja", "el color es material (03, §3.9)"),
        ("Disparidad de escala", "scale disparity", "deja", "una letra, una celda"),
        ("Foco selectivo", "selective focus", "deja", "un recurso de cámara"),
        ("Bloques de color", "color blocking", "deja", "el color es material (03, §3.9)"),
        ("Frío y cálido", "warm and cool split", "no", "el verde es solo luz, nunca tinta"),
    ],
    "Agrupación": [
        ("Región común", "common region", "toma", "la celda y la caja (P-01, P-10)"),
        ("Buena continuación", "good continuation", "toma", "el arranque tangente (P-05 · 2)"),
        ("Figura y fondo", "figure-ground reversal", "toma", "anverso y reverso (P-02 · 5)"),
        ("Proximidad", "proximity clustering", "toma", "un azulejo vacío entre palabras (Acción 11)"),
        ("Cierre", "closure", "toma", "el ojo cierra el desagüe (P-07 · 1)"),
        ("Simetría", "symmetry", "cambia", "el eje de la o; los dobles varían (P-09)"),
        ("Ruptura de patrón", "pattern break", "cambia", "ninguna placa se repite (03, §3.8)"),
    ],
    "Espacio": [
        ("Al centro", "center placement", "toma", "cada signo, en el eje de su celda (P-01)"),
        ("Marco dentro del marco", "frame within a frame", "toma", "la cifra en su celda (P-08 · 6)"),
        ("Oclusión", "occlusion", "toma", "la cinta que tapa ojos y boca (D12; Acción 6)"),
        ("Recorrido de lectura", "reading path", "toma", "componer (Acción 11)"),
        ("Síntesis temporal", "temporal synthesis", "toma", "la serie de frotados (Acción 8)"),
        ("Perspectiva forzada", "forced perspective", "cambia", "el trapecio de la proyección (01, §1.4)"),
        ("Jerarquía de tamaño", "size hierarchy", "deja", "una letra, una celda"),
        ("Recorte en el borde", "crop at the edge", "deja", "lo que se sale, se deja salir (Acción 3)"),
        ("Líneas guía", "leading lines", "deja", "dirigir la mirada"),
    ],
    "Social": [
        ("Esquema de rostro", "face schema", "no", "la obra tapa ojos y boca (D12)"),
        ("Mirada", "gaze cue", "no", "no hay rostro (03, §3.2, regla 6)"),
        ("Vector del cuerpo", "body vector", "no", "el cuerpo de Rebeca no se usa"),
        ("Antropomorfismo", "anthropomorphism", "no", "los signos no se personifican"),
    ],
    "Semántico": [
        ("Contraste semántico", "semantic contrast", "toma", "las vecinas (10, §10.7)"),
        ("Composición semántica", "semantic compounding", "toma", "la a es la suma de dos pisos (P-06 · 4)"),
        ("Metáfora contextual", "contextual metaphor", "toma", "las líneas tienen nombres de vasija (P-01 · 3)"),
        ("Sustitución de forma", "form substitution", "cambia", "dada vuelta: todas, la misma vasija"),
        ("Exageración caricaturesca", "caricatural exaggeration", "deja", "aquí, la litote: «apenas»"),
    ],
    "Cultural": [
        ("Factura visible", "visible facture", "toma", "el punteado, el temblor, la placa rota"),
        ("Cita visual", "visual quotation", "no", "se cita el procedimiento, no la imagen"),
        ("Cita de género", "genre quotation", "no", "ningún estilo ni motivo se copia"),
    ],
}

# lo que se suma, por dominio de llegada: (nombre, el número de la técnica en Contenida)
SUMADAS = {
    "Social": [("El gesto como signo", 14)],
    "Cultural": [("Quién lo hizo", 4)],
    "Huella": [("Huella en metal blando", 2), ("Cadena de soportes", 10), ("La voz como línea", 11),
               ("Hacer visible lo que suena", 12), ("Leer sin tocar", 13)],
}

# ---------------------------------------------------------------- la taxonomía de Contenida

OPERACIONES = {
    "diferenciar": dict(i=1, nombre="Diferenciar", murray="Differentiate", que="Separar algo de su fondo.",
                        aqui="El relieve del plano, lo hallado de lo reconstruido, la letra de la piel, "
                             "Contenida de sus vecinas.",
                        figura="Antítesis", figura_que="continuo y punteado; relieve y hundido"),
    "agrupar": dict(i=2, nombre="Agrupar", murray="Group", que="Hacer de muchos uno.",
                    aqui="La celda, la caja y las partes que comparten los signos.",
                    figura="Sinécdoque", figura_que="una celda por toda la cabeza; una mano por todo el calendario"),
    "secuenciar": dict(i=3, nombre="Secuenciar", murray="Sequence", que="Ordenar en el tiempo o en un recorrido.",
                       aqui="La cadena de estados, la serie de frotados, el bucle, el poema verso a verso.",
                       figura="Gradación y ciclo", figura_que="frotado 01 … n; «termina y empieza»"),
    "inferir": dict(i=4, nombre="Inferir", murray="Infer", que="Que quien mira complete lo que no está.",
                    aqui="El desagüe, la vasija, lo reconstruido por analogía, la voz que no se entiende.",
                    figura="Elipsis y metáfora", figura_que="lo que falta también dice; la letra es un vaso"),
}

DOMINIOS = {
    "materia": dict(nombre="Materia y tacto", murray="Feature", estado="cambia"),
    "huella": dict(nombre="Huella", murray="—", estado="suma"),
    "estructura": dict(nombre="Estructura", murray="Grouping", estado="toma"),
    "tiempo": dict(nombre="Espacio y tiempo", murray="Space", estado="cambia"),
    "mano": dict(nombre="La mano", murray="Social", estado="cambia"),
    "sentido": dict(nombre="Sentido", murray="Semantic", estado="toma"),
    "procedencia": dict(nombre="Procedencia", murray="Cultural", estado="cambia"),
}

# n: el número de la técnica (su celda); estado: toma, cambia, suma o no (la vecina opuesta)
# vista: cómo se dibuja su mecanismo (corte, planta, serie, comparación, cajetín…), nunca la imagen
TECNICAS = [
    dict(n=1, op="diferenciar", dom="materia", nombre="Textura contra plano", murray="texture against flat",
         estado="toma", vista="corte", que="Una forma sube del plano y se lee con los dedos.",
         aqui="La placa: por el reverso un canal; por el frente, la letra en relieve."),
    dict(n=2, op="diferenciar", dom="huella", nombre="Huella en metal blando", murray="—",
         estado="suma", vista="corte", que="Algo aprieta un metal blando y la forma queda hundida.",
         aqui="El papel de aluminio de cocina: lo hunde la mano."),
    dict(n=3, op="diferenciar", dom="sentido", nombre="Contraste semántico", murray="semantic contrast",
         estado="toma", vista="comparación", que="Una obra se define por lo que la vecina hace distinto.",
         aqui="Las vecinas de 10, §10.7: en qué se parecen y en qué se separan."),
    dict(n=4, op="diferenciar", dom="procedencia", nombre="Quién lo hizo", murray="—",
         estado="suma", vista="cajetín", que="Lo que distingue una huella es la mano que la hizo, y se dice.",
         aqui="El colofón de manos y las fichas."),
    dict(n=5, op="agrupar", dom="estructura", nombre="Región común", murray="common region",
         estado="toma", vista="planta", que="Lo que cae dentro de un mismo borde se lee como uno.",
         aqui="La celda de la cabeza; la caja de 8 × 7; las cifras en su celda."),
    dict(n=6, op="agrupar", dom="estructura", nombre="Composición por partes", murray="semantic compounding",
         estado="cambia", vista="axonometría", que="La letra se arma con partes, construcciones o capas.",
         aqui="La gramática: cuatro generadores y sus partes; los estados, uno sobre otro."),
    dict(n=7, op="agrupar", dom="mano", nombre="Cuerpos que forman letra", murray="body vector",
         estado="no", vista="no se dibuja", que="Personas dispuestas en forma de letra.",
         aqui="No se hace: la obra ya pone el cuerpo, y el de Rebeca no se usa."),
    dict(n=8, op="secuenciar", dom="tiempo", nombre="Síntesis temporal", murray="temporal synthesis",
         estado="toma", vista="serie", que="Una serie de instantes muestra lo que el ojo no ve de una vez.",
         aqui="La serie de frotados; el agua tocada, foto tras foto."),
    dict(n=9, op="secuenciar", dom="tiempo", nombre="Recorrido de lectura", murray="reading path",
         estado="toma", vista="planta", que="El movimiento de un cuerpo se vuelve trazo en la página.",
         aqui="Componer como partitura de un recorrido (Acción 11)."),
    dict(n=10, op="secuenciar", dom="huella", nombre="Cadena de soportes", murray="—",
         estado="suma", vista="cadena", que="La forma pasa de un soporte a otro y cambia en cada paso.",
         aqui="La cadena de estados: calco, placa, cinta, frotado, agua, voz."),
    dict(n=11, op="secuenciar", dom="huella", nombre="La voz como línea", murray="—",
         estado="suma", vista="alzado", que="La voz deja un trazo que avanza con el tiempo.",
         aqui="Acción 10: «lo que vuelve, vuelve escrito»."),
    dict(n=12, op="inferir", dom="huella", nombre="Hacer visible lo que suena", murray="—",
         estado="suma", vista="planta", que="La arena o la tinta dibujan la figura de un sonido.",
         aqui="El agua tocada y la voz sobre el agua (Acciones 9 y 10)."),
    dict(n=13, op="inferir", dom="huella", nombre="Leer sin tocar", murray="—",
         estado="suma", vista="corte", que="Una máquina lee una huella con luz, sin tocarla.",
         aqui="El reparto: la máquina lee y mide; la mano hace."),
    dict(n=14, op="inferir", dom="mano", nombre="El gesto como signo", murray="—",
         estado="suma", vista="celda", que="La mano dice sin la boca.",
         aqui="El ¶, hecho con los dedos; las dos manos del repujado."),
    dict(n=15, op="inferir", dom="sentido", nombre="Sustitución de forma", murray="form substitution",
         estado="cambia", vista="comparación", que="Una letra se recuerda por una cosa con su forma.",
         aqui="Dada vuelta: todas las letras son la misma vasija."),
    dict(n=16, op="inferir", dom="sentido", nombre="Metáfora material", murray="contextual metaphor",
         estado="cambia", vista="alzado", que="La letra parece de otra materia: cartílago, líquido.",
         aqui="Lo blando sale del aluminio y del agua: la cuenca, el sifón, la gota."),
    dict(n=17, op="inferir", dom="sentido", nombre="Prosopopeya", murray="anthropomorphism",
         estado="no", vista="no se dibuja", que="Los signos o las máquinas hablan como personas.",
         aqui="No se hace: los signos no se personifican; la máquina no habla."),
]
TECNICA = {t["n"]: t for t in TECNICAS}

# ---------------------------------------------------------------- dónde cae en Contenida (el quinto nivel)
# (nombre, dónde está, columna del cuadro)

DESTINOS = {
    "placa": ("La placa en relieve", "P-02 · 5", "P"),
    "gramatica": ("Las partes de la gramática", "03c · P-07", "P"),
    "vaso": ("La letra es un vaso", "P-01 · 3", "P"),
    "gota": ("La gota", "P-06 · 2", "P"),
    "a2": ("Desenterrar el pie", "Acción 2", "A2"),
    "a4": ("Repujar", "Acción 4", "A4"),
    "caja": ("La celda y la caja", "Acción 5 · P-10", "A5"),
    "a7": ("El signo final: el ¶", "Acción 7", "A7"),
    "a8": ("Frotar", "Acción 8", "A8"),
    "a9": ("Pasar por el agua", "Acción 9", "A9"),
    "a10": ("Dar voz", "Acción 10", "A10"),
    "a11": ("Componer", "Acción 11", "A11"),
    "colofon": ("El colofón de manos", "03, §3.11 · Acción 12", "A12"),
    "cadena": ("La cadena de estados", "03, §3.7", "cadena"),
    "reparto": ("La máquina lee; la mano hace", "06, §6.3", "06"),
    "no": ("Lo que no se hace", "06, §6.4", "no"),
}

# las columnas del cuadro: los planos, las trece acciones del taller (04) y tres más
COLUMNAS = [
    ("P", "los planos", None),
    ("A0", "pedir", 1), ("A1", "medir y frotar", 1), ("A2", "desenterrar", 1), ("A3", "calcar", 1),
    ("A4", "repujar", 2), ("A5", "llenar la caja", 2), ("A6", "encintar", 2), ("A7", "el signo final", 2),
    ("A8", "frotar", 3), ("A9", "el agua", 3), ("A10", "dar voz", 3), ("A11", "componer", 3), ("A12", "cerrar", 3),
    ("cadena", "la cadena", None), ("06", "el reparto", None), ("no", "no se hace", None),
]
CUADERNOS = {1: "desenterrar", 2: "contener", 3: "devolver"}

# ---------------------------------------------------------------- las referencias (10_imagenes_de_dominio_publico.md)
# tec: la técnica principal primero; mirada: si ya la miraste en su archivo
# medio y licencia: «cada referencia dice de dónde viene» (06, §6.4)

PDIA = "Public Domain Image Archive"
PDR = "The Public Domain Review"

REFERENCIAS = {
    "hauy": dict(
        corto="Haüy, 1786", autor="Valentin Haüy", obra="Essai sur l'éducation des aveugles", anio="1786",
        medio="libro impreso en relieve", licencia="dominio público",
        tec=[1, 4], destinos=["a4", "placa", "colofon"], mirada=False,
        archivo=("Wellcome Collection", "https://wellcomecollection.org/works/fwj4w4rp"),
        otros=[("Project Gutenberg", "https://gutenberg.org/ebooks/26609"),
               ("Perkins", "https://www.perkins.org/first-embossed-book-for-the-blind/"),
               ("APH Museum", "https://aphmuseum.org/record/essai-sur-leducation-des-aveugles-embossed-roman-letters/")],
        toma="Trabajar por el reverso, en espejo, y leer con los dedos lo que sale por el frente.",
        no_toma="Sus letras; el braille, que llegó después.",
        rima="Lo imprimieron sus alumnos ciegos, con el impresor Clousier."),
    "moon": dict(
        corto="Moon, 1845", autor="William Moon", obra="el tipo Moon", anio="1845",
        medio="letras en relieve para leer con los dedos", licencia="se cita la ficha",
        tec=[1, 3], destinos=["placa"], mirada=False,
        archivo=("ficha", "https://en.wikipedia.org/wiki/Moon_type"), otros=[],
        toma="Letras latinas simplificadas, en relieve, para leer con los dedos.",
        no_toma="Que cada letra se lea siempre igual: aquí cada placa es distinta.",
        rima="Moon perdió la vista de adulto."),
    "fonografo": dict(
        corto="Balcomb, 1878", autor="J. T. Balcomb", obra="Edison Phonograph with a Carbon Microphone",
        anio="1878", medio="grabado coloreado", licencia="dominio público (fuente: Wellcome Library)",
        tec=[2, 11], destinos=["a4", "a10"], mirada=False,
        archivo=(PDIA, "https://pdimagearchive.org/images/b8be5944-796f-44dc-80bf-163a58743449/"),
        otros=[("«Inventing the Recording»", "https://publicdomainreview.org/essay/inventing-the-recording/")],
        toma="La voz también repuja: mueve una membrana y una aguja que hunde una hoja de estaño.",
        no_toma="La máquina y la grabación: en la Acción 10 no se publica.",
        rima="Allá la hunde la voz; aquí, la mano."),
    "impresion": dict(
        corto="Auer y Bradbury, 1852-1855", autor="Alois Auer y Andreas Worring; Henry Bradbury",
        obra="la impresión natural", anio="1852-1855",
        medio="láminas impresas desde una huella en plomo", licencia="falta el archivo de la imagen",
        tec=[10, 2, 4], destinos=["a4", "cadena", "colofon"], mirada=False,
        archivo=("ficha", "https://en.wikipedia.org/wiki/The_Ferns_of_Great_Britain_and_Ireland"), otros=[],
        toma="Un helecho hundido en plomo blando; la huella pasa al cobre y del cobre al papel.",
        no_toma="Las plantas y el ornamento.",
        rima="Auer acusó a Bradbury de plagio: por eso se dice de dónde sale cada cosa."),
    "scott": dict(
        corto="Scott, 1857-1860", autor="Édouard-Léon Scott de Martinville", obra="los fonautogramas",
        anio="1857-1860", medio="trazos de la voz sobre papel ahumado",
        licencia="se citan los escaneos de First Sounds",
        tec=[11], destinos=["a10"], mirada=False,
        archivo=("First Sounds", "https://www.firstsounds.org/sounds/earlier-playback.php"),
        otros=[("Library of Congress",
                "https://blogs.loc.gov/now-see-hear/2021/08/from-the-recording-registry-phonautograms-c-1853-61/")],
        toma="La voz que queda escrita y no se oye: 148 años fue solo trazo.",
        no_toma="La máquina.",
        rima="«Au clair de la lune», 1860: al doble de velocidad pareció una niña."),
    "bell": dict(
        corto="Bell, 1885", autor="Alexander Graham Bell", obra="«hear my voice», disco de cera del Volta Laboratory",
        anio="1885", medio="disco de cera, leído con luz en 2013", licencia="se cita el Smithsonian",
        tec=[13], destinos=["reparto"], mirada=False,
        archivo=("Smithsonian", "https://insider.si.edu/2013/04/hear-my-voice-smithsonian-identifies-130-year-old-"
                                "recording-as-alexander-graham-bells-voice/"),
        otros=[],
        toma="Leer una huella sin tocarla: se escaneó el surco y se calculó la aguja.",
        no_toma="Que la máquina haga la huella: aquí solo la lee.",
        rima=""),
    "watts": dict(
        corto="Watts Hughes, 1891", autor="Margaret Watts Hughes", obra="las figuras de voz del eidófono",
        anio="1891", medio="figuras de voz sobre vidrio", licencia="ensayo de hoy: se cita, no se copia",
        tec=[12], destinos=["a10", "a8"], mirada=False,
        archivo=("«Picturing a Voice»",
                 "https://publicdomainreview.org/essay/picturing-a-voice-margaret-watts-hughes-and-the-eidophone/"),
        otros=[],
        toma="Una impresión hecha con la voz: la mano pasa la membrana; la figura la pone el canto.",
        no_toma="Las figuras como forma de letra.",
        rima="Rima con los frotados: una impresión por contacto."),
    "chladni": dict(
        corto="Chladni, 1787", autor="Ernst Chladni", obra="Entdeckungen über die Theorie des Klanges",
        anio="1787", medio="lámina de libro", licencia="dominio público",
        tec=[12], destinos=["a9", "a10", "a7"], mirada=False,
        archivo=(PDIA, "https://pdimagearchive.org/images/d3a940a7-aac0-49e7-9af4-23b2356be7b5/"), otros=[],
        toma="La arena dibuja lo que suena; la figura depende de dónde apoyan los dedos.",
        no_toma="Las figuras como forma de letra.", rima=""),
    "kempelen": dict(
        corto="Kempelen, 1791", autor="Wolfgang von Kempelen", obra="la máquina que habla", anio="1791",
        medio="una máquina, contada en un ensayo de hoy", licencia="ensayo de hoy: se cita",
        tec=[17, 14], destinos=["no", "a7"], mirada=False,
        archivo=("«Early Androids and Artificial Speech»",
                 "https://publicdomainreview.org/essay/early-androids-and-artificial-speech"),
        otros=[],
        toma="La boca hecha por las manos, pieza por pieza: glotis de marfil, garganta de cuero.",
        no_toma="Que la máquina hable: aquí la máquina no habla.",
        rima="«A la boca la taparon.»"),
    "moreda": dict(
        corto="Moreda, 2021", autor="Eva Moreda Rodríguez", obra="«Inventing the Recording», ensayo y libro",
        anio="2021", medio="ensayo; libro de Oxford University Press", licencia="texto de hoy: se cita, no se copia",
        tec=[4], destinos=["a10", "colofon"], mirada=False,
        archivo=(PDR, "https://publicdomainreview.org/essay/inventing-the-recording/"), otros=[],
        toma="Las primeras grabaciones en castellano las hicieron unos cuarenta gabinetes pequeños.",
        no_toma="La industria: en el proyecto, tu voz la grabas tú.",
        rima=""),
    "bulwer": dict(
        corto="Bulwer, 1644", autor="John Bulwer", obra="Chirologia, or the Naturall Language of the Hand",
        anio="1644", medio="láminas de libro", licencia="dominio público",
        tec=[14], destinos=["a4", "a7"], mirada=False,
        archivo=(PDIA, "https://pdimagearchive.org/images/4ad90c06-f3dc-40f0-bd62-a8953db26439/"),
        otros=[("lámina 2", "https://pdimagearchive.org/images/30081167-67cc-47a3-b9a4-2d97fa779c37/")],
        toma="El gesto es un signo: un libro entero sobre lo que dicen las manos sin la boca.",
        no_toma="Las formas de las manos como forma de letra.",
        rima="«No tiene lengua pero igual dice.»"),
    "bonet": dict(
        corto="Bonet, 1620", autor="Juan Pablo Bonet",
        obra="Reduction de las letras, y arte para enseñar a ablar los mudos", anio="1620",
        medio="libro", licencia="marca de dominio público",
        tec=[14], destinos=["a7", "no"], mirada=False,
        archivo=("Wellcome Collection", "https://wellcomecollection.org/works/sx9e24hu"),
        otros=[("The Paris Review",
                "https://www.theparisreview.org/blog/2017/08/16/teaching-speak-juan-pablo-bonet-history-oralism/")],
        toma="Un alfabeto hecho con una mano, en castellano.",
        no_toma="Su método: era oralista, y describe a las personas sordas con desprecio.", rima=""),
    "anianus": dict(
        corto="Anianus, 1492", autor="Anianus", obra="«Manual Mnemonic», en Compotus cum commento", anio="1492",
        medio="grabado en un libro", licencia="dominio público",
        tec=[5], destinos=["caja"], mirada=False,
        archivo=(PDIA, "https://pdimagearchive.org/images/137949be-a852-417d-b318-c94e0117ab40/"), otros=[],
        toma="La mano como retícula: cada articulación, una casilla del calendario.",
        no_toma="Ninguna lectura del calendario de la Kochamama.", rima=""),
    "mano1466": dict(
        corto="Mano de 1466", autor="Anónimo alemán", obra="La mano como espejo de la salvación", anio="1466",
        medio="grabado en madera", licencia="dominio público",
        tec=[5], destinos=["caja", "a4"], mirada=False,
        archivo=(PDIA, "https://pdimagearchive.org/images/2502c9fe-691e-47ec-8cd9-38b6e1c35e76/"), otros=[],
        toma="La mano como superficie que contiene escritura, dividida en celdas.",
        no_toma="Su contenido religioso y sus textos.", rima=""),
    "cooperrider": dict(
        corto="Cooperrider, 2022", autor="Kensy Cooperrider",
        obra="«Handy Mnemonics: The Five-Fingered Memory Machine»", anio="2022",
        medio="ensayo", licencia="texto de hoy: se cita",
        tec=[5], destinos=["caja"], mirada=False,
        archivo=(PDR, "https://publicdomainreview.org/essay/handy-mnemonics"), otros=[],
        toma="Beda contaba en la mano catorce articulaciones y cinco uñas: diecinueve casillas.",
        no_toma="Los usos religiosos de la mano.", rima="La mano ya era una caja de celdas."),
    "worthington": dict(
        corto="Worthington, 1895", autor="A. M. Worthington, con fotografías de R. S. Cole",
        obra="The Splash of a Drop", anio="1895", medio="fotografías instantáneas, en un libro",
        licencia="dominio público",
        tec=[8], destinos=["gota", "a9", "a8"], mirada=False,
        archivo=(PDR, "https://publicdomainreview.org/collection/the-splash-of-a-drop-1895/"),
        otros=[("secuencia 1", "https://pdimagearchive.org/images/fe3fc9b0-6acd-486b-a72a-4aeef1441c04/"),
               ("secuencia 2", "https://pdimagearchive.org/images/06940cce-b7fa-462b-addb-75de4747f7f6/")],
        toma="La serie de instantes: cada gota deja otra figura.",
        no_toma="Las salpicaduras como forma: se toma la serie.",
        rima="«La misma diosa dos veces / y ninguna igual.»"),
    "feuillet": dict(
        corto="Feuillet, 1701", autor="Raoul-Auger Feuillet", obra="Choregraphie", anio="1701",
        medio="lámina de libro: una notación de la danza", licencia="dominio público",
        tec=[9], destinos=["a11"], mirada=False,
        archivo=(PDIA, "https://pdimagearchive.org/images/d4b9020a-cb94-444f-a612-7bd487eac204/"), otros=[],
        toma="Escribir el recorrido de un cuerpo: componer como partitura.",
        no_toma="Sus signos como letras.", rima="El cuerpo de la obra se mueve «apenas» (D11)."),
    "page": dict(
        corto="Page, 1874", autor="Wm. H. Page & Co.", obra="Specimens of Chromatic Wood Type, Borders, Etc.",
        anio="1874", medio="espécimen de tipos de madera", licencia="dominio público",
        tec=[6], destinos=["caja", "cadena"], mirada=False,
        archivo=(PDIA, "https://pdimagearchive.org/images/62ae7660-5aed-41cc-a421-11d9ead9553a/"), otros=[],
        toma="Una letra hecha de capas que se imprimen una sobre otra.",
        no_toma="Sus formas decorativas.", rima="El tipo de madera es el pariente grande de la placa."),
    "hoefnagel": dict(
        corto="Hoefnagel, hacia 1595", autor="Joris Hoefnagel, en el libro de Georg Bocskay",
        obra="guía para construir las letras", anio="hacia 1595",
        medio="lámina de un libro de modelos de caligrafía", licencia="dominio público, según el archivo",
        tec=[6, 3], destinos=["gramatica"], mirada=False,
        archivo=(PDR, "https://publicdomainreview.org/product/guide-for-constructing-the-letters-k-and-l/"),
        otros=[("Getty Museum", "https://www.getty.edu/art/collection/object/105TPX")],      # Ms. 20, fol. 144v
        toma="Cada letra dibujada con su construcción geométrica, como en los planos.",
        no_toma="Los motivos que rodean cada letra.", rima=""),
    "publicius": dict(
        corto="Publicius, 1482", autor="Jacobus Publicius", obra="«Mnemonic Alphabet», en Ars Memorativa",
        anio="1482", medio="grabado en un libro", licencia="dominio público",
        tec=[15, 3], destinos=["vaso"], mirada=False,
        archivo=(PDIA, "https://pdimagearchive.org/images/8f60966e-039b-4395-ba0f-2e66398fbbf5/"),
        otros=[("colección", "https://publicdomainreview.org/collection/mnemonic-alphabet-of-jacobus-publicius-1482/")],
        toma="Cada letra se recuerda por una cosa con su forma: la A, una escalera de tijera; la C, una herradura.",
        no_toma="Un objeto distinto para cada letra.",
        rima="La metáfora de Contenida, dada vuelta."),
    "organica": dict(
        corto="Bierpfaff y Falck, hacia 1650", autor="Jan Christian Bierpfaff y Jeremias Falck",
        obra="Libellus Novus Elementorum Latinorum", anio="hacia 1650", medio="grabados",
        licencia="CC0 (Rijksmuseum)",
        tec=[16, 3], destinos=["gota", "gramatica"], mirada=False,
        archivo=(PDR, "https://publicdomainreview.org/collection/an-alphabet-of-organic-type-ca-1650/"),
        otros=[("Rijksmuseum", "https://www.rijksmuseum.nl/")],
        toma="Letras blandas, como de cartílago o de líquido: la cuenca, el sifón, la gota.",
        no_toma="El ornamento de orfebre: aquí lo blando sale del material y del agua.", rima=""),
    "silvestre": dict(
        corto="Silvestre, 1843", autor="Joseph-Balthazar Silvestre", obra="Alphabet-album", anio="1843",
        medio="sesenta hojas de alfabetos copiados", licencia="dominio público",
        tec=[3], destinos=["a2", "no"], mirada=False,
        archivo=(PDIA, "https://pdimagearchive.org/images/4113be3d-a919-4880-acef-723a9f424979/"), otros=[],
        toma="Sacar letras de manuscritos, hoja por hoja, como Contenida las saca del pie.",
        no_toma="El ornamento: es un catálogo de lo que no se hace.", rima=""),
    "fry": dict(
        corto="Fry, 1799", autor="Edmund Fry", obra="Pantographia", anio="1799",
        medio="espécimen de 405 alfabetos", licencia="dominio público, según el archivo",
        tec=[3], destinos=["caja"], mirada=False,
        archivo=(PDR, "https://publicdomainreview.org/collection/pantographia"), otros=[],
        toma="Cada letra cortada a mano, en punzones de acero: unos dieciséis años de trabajo.",
        no_toma="Juntarlos todos: Contenida hace uno solo, con las letras de un pie.", rima=""),
    "puntuacion": dict(
        corto="Punctuation Personified, 1824", autor="John Harris, editor", obra="Punctuation Personified",
        anio="1824", medio="libro ilustrado", licencia="dominio público, según el archivo",
        tec=[17, 3], destinos=["no", "caja"], mirada=False,
        archivo=(PDR, "https://publicdomainreview.org/collection/punctuation-personified"), otros=[],
        toma="Cada signo con su regla; la caja también empieza en la coma y termina en el ¶.",
        no_toma="Personificarlos: los signos se tratan con el mismo cuidado que las letras.", rima=""),
    "humano": dict(
        corto="The Human Alphabet, 1534-1789", autor="Peter Flötner y otros",
        obra="«The Human Alphabet»: Flötner, 1534; The Comical Hotch Potch, 1782; Bourbonnoise Alphabet, 1789",
        anio="1534-1789", medio="alfabetos hechos con cuerpos, en grabados", licencia="dominio público, según el archivo",
        tec=[7, 3], destinos=["no"], mirada=False,
        archivo=(PDR, "https://publicdomainreview.org/collection/the-human-alphabet"), otros=[],
        toma="Nada: es la vecina opuesta.",
        no_toma="Hacer letras con cuerpos: la obra ya pone el cuerpo, y el de Rebeca no se usa.", rima=""),
}

# ---------------------------------------------------------------- las imágenes del atlas (R-09)
# De qué página se baja la imagen de cada referencia, y con qué licencia. Solo las de dominio público:
# las fotos de hoy (el Smithsonian, Perkins, el museo de la APH, The Paris Review) quedan como enlace,
# y Haüy y Bonet se toman de la Wellcome Collection. Se bajan con descargar_imagenes.py a imagenes/,
# que no entra en el repositorio (06, §6.4). De Wikimedia se baja la miniatura de 960 px, por
# thumb.wikimedia.org: upload.wikimedia.org contestó 429 (demasiados pedidos).
DP_PDIA = "dominio público, según el Public Domain Image Archive"
DP_PDR = "dominio público, según The Public Domain Review"

IMAGENES = {
    "hauy": dict(pagina="https://wellcomecollection.org/works/fwj4w4rp", pagina_libro=14,
                 licencia="marca de dominio público, Wellcome Collection"),       # el capítulo I, con sus letras
    "moon": dict(pagina="https://commons.wikimedia.org/wiki/File:Moon-type-chart.jpg",
                 imagen="https://thumb.wikimedia.org/wikipedia/commons/thumb/b/b3/Moon-type-chart.jpg/"
                        "960px-Moon-type-chart.jpg",
                 licencia="dominio público, según Wikimedia Commons (Moon, Light for the Blind, 1877)"),
    "fonografo": dict(pagina="https://pdimagearchive.org/images/b8be5944-796f-44dc-80bf-163a58743449/",
                      licencia=DP_PDIA),
    "impresion": dict(pagina="https://commons.wikimedia.org/wiki/File:Polypodium_vulgare_Moore1.png",
                      imagen="https://thumb.wikimedia.org/wikipedia/commons/thumb/e/eb/Polypodium_vulgare_Moore1.png/"
                             "960px-Polypodium_vulgare_Moore1.png",
                      licencia="dominio público, según Wikimedia Commons (Moore y Bradbury, 1857)"),
    "scott": dict(pagina="https://commons.wikimedia.org/wiki/File:Phonautogram_-_Scott_1859.jpg",
                  imagen="https://upload.wikimedia.org/wikipedia/commons/e/e5/Phonautogram_-_Scott_1859.jpg",
                  girar=90,         # la tira es vertical: girada, la voz avanza de izquierda a derecha
                  licencia="dominio público en EE. UU., según Wikimedia Commons (patente de Scott, 1859, en el INPI); "
                           "revisar: el escaneo es de First Sounds, que publica sus facsímiles con CC BY-ND"),
    "bell": dict(pagina="https://insider.si.edu/2013/04/hear-my-voice-smithsonian-identifies-130-year-old-"
                        "recording-as-alexander-graham-bells-voice/",
                 licencia="foto del Smithsonian de 2013: no es de dominio público", descarga=False),
    "watts": dict(pagina="https://publicdomainreview.org/essay/picturing-a-voice-margaret-watts-hughes-and-the-"
                         "eidophone/", licencia=DP_PDR),
    "chladni": dict(pagina="https://pdimagearchive.org/images/d3a940a7-aac0-49e7-9af4-23b2356be7b5/",
                    licencia=DP_PDIA),
    "kempelen": dict(pagina="https://publicdomainreview.org/essay/early-androids-and-artificial-speech",
                     licencia=DP_PDR),
    "moreda": dict(pagina="https://publicdomainreview.org/essay/inventing-the-recording/", licencia=DP_PDR),
    "bulwer": dict(pagina="https://pdimagearchive.org/images/4ad90c06-f3dc-40f0-bd62-a8953db26439/",
                   licencia=DP_PDIA),
    "bonet": dict(pagina="https://wellcomecollection.org/works/sx9e24hu", pagina_libro=162,
                  licencia="marca de dominio público, Wellcome Collection"),      # el «Abecedario demostrativo»
    "anianus": dict(pagina="https://pdimagearchive.org/images/137949be-a852-417d-b318-c94e0117ab40/",
                    licencia=DP_PDIA),
    "mano1466": dict(pagina="https://pdimagearchive.org/images/2502c9fe-691e-47ec-8cd9-38b6e1c35e76/",
                     licencia=DP_PDIA),
    "cooperrider": dict(pagina="https://publicdomainreview.org/essay/handy-mnemonics", licencia=DP_PDR),
    "worthington": dict(pagina="https://pdimagearchive.org/images/fe3fc9b0-6acd-486b-a72a-4aeef1441c04/",
                        licencia=DP_PDIA),
    "feuillet": dict(pagina="https://pdimagearchive.org/images/d4b9020a-cb94-444f-a612-7bd487eac204/",
                     licencia=DP_PDIA),
    "page": dict(pagina="https://pdimagearchive.org/images/62ae7660-5aed-41cc-a421-11d9ead9553a/",
                 licencia=DP_PDIA),
    "hoefnagel": dict(pagina="https://www.getty.edu/art/collection/object/105TPX",      # Ms. 20, fol. 144v
                      imagen="https://media.getty.edu/iiif/image/e2497fe5-d2be-402c-826b-ffe768822c51/full/"
                             "!1600,1600/0/default.jpg",
                      licencia="dominio público, según el Getty Museum (Open Content)"),
    "publicius": dict(pagina="https://pdimagearchive.org/images/8f60966e-039b-4395-ba0f-2e66398fbbf5/",
                      licencia=DP_PDIA),
    "organica": dict(pagina="https://publicdomainreview.org/collection/an-alphabet-of-organic-type-ca-1650/",
                     licencia="CC0, Rijksmuseum"),
    "silvestre": dict(pagina="https://pdimagearchive.org/images/4113be3d-a919-4880-acef-723a9f424979/",
                      licencia=DP_PDIA),
    "fry": dict(pagina="https://publicdomainreview.org/collection/pantographia", licencia=DP_PDR),
    "puntuacion": dict(pagina="https://publicdomainreview.org/collection/punctuation-personified", licencia=DP_PDR),
    "humano": dict(pagina="https://publicdomainreview.org/collection/the-human-alphabet", licencia=DP_PDR),
}

# lo que se usaría de cada archivo y no se baja: son fotos de hoy
SOLO_ENLACE = [
    ("Smithsonian", "la foto del disco de Bell (2013)"),
    ("Perkins y el museo de la APH", "las fotos del libro de Haüy: se baja el de la Wellcome Collection"),
    ("The Paris Review", "la imagen de Bonet: se baja la de la Wellcome Collection"),
]

# el orden de las referencias: por técnica principal
ORDEN = sorted(REFERENCIAS, key=lambda k: (REFERENCIAS[k]["tec"][0], REFERENCIAS[k]["anio"], k))


def de_la_operacion(op):
    """Las referencias cuya técnica principal es de esta operación, en orden."""
    return [k for k in ORDEN if TECNICA[REFERENCIAS[k]["tec"][0]]["op"] == op]


def columnas_de(ref):
    """Las columnas del cuadro en las que cae una referencia."""
    return {DESTINOS[d][2] for d in REFERENCIAS[ref]["destinos"]}


# las vecinas de 10, §10.7, en dos hilos: en qué se parece cada una y en qué se separa
VECINAS = [
    ("moon", "Moon, 1845", "letras en relieve, para los dedos", "cada letra, siempre igual"),
    ("silvestre", "Silvestre, 1843", "letras sacadas de un documento", "copia el ornamento"),
    ("fry", "Fry, 1799", "cada letra, cortada a mano", "405 alfabetos; aquí, uno"),
    ("hoefnagel", "Hoefnagel, h. 1595", "la letra con su construcción", "la rodea de motivos"),
    ("publicius", "Publicius, 1482", "la letra es una cosa", "una cosa distinta por letra"),
    ("organica", "Bierpfaff y Falck", "letras blandas", "lo blando es ornamento"),
    ("puntuacion", "Punctuation Personified", "cada signo con su regla", "los signos son personas"),
    ("humano", "The Human Alphabet", "la letra sale de un cuerpo", "la hace con cuerpos"),
]

# ---------------------------------------------------------------- del encargo a la referencia

# el encargo no es un cliente: es la obra (D1 … D16) y el poema
ENCARGOS = [
    dict(encargo="La letra se lee con los dedos.", de="D2 y la Acción 4",
         op="diferenciar", dom="materia", tec=1, refs=["hauy", "moon"],
         cae="la placa en relieve (P-02 · 5); Acción 4, paso 3"),
    dict(encargo="la misma diosa dos veces\ny ninguna igual.", de="el poema y D15",
         op="secuenciar", dom="tiempo", tec=8, refs=["worthington"],
         cae="el agua tocada, foto tras foto (Acción 9); la serie de frotados (Acción 8)"),
    dict(encargo="Y es que lo que vuelve,\nvuelve escrito;\npocas veces vuelve\nhablado.", de="el poema y D14",
         op="secuenciar", dom="huella", tec=11, refs=["scott", "fonografo"],
         cae="Acción 10; si el fonautograma va en el espécimen (10, §10.11)"),
    dict(encargo="de la boca sale un signo\nhecho con las manos,", de="el poema y D13",
         op="inferir", dom="mano", tec=14, refs=["bulwer", "bonet"], cae="el ¶, con los dedos (Acción 7)"),
    dict(encargo="Quedó el contenedor\nde lo que ya no está.", de="el poema y D6, la piscina vacía",
         op="agrupar", dom="estructura", tec=5, refs=["anianus", "mano1466", "cooperrider"],
         cae="la celda y la caja de 8 × 7 (Acción 5; P-01, P-10)"),
    dict(encargo="Desenterrar una voz\nes desenterrar la mano\ndel que la escribió.", de="el poema y 06",
         op="diferenciar", dom="procedencia", tec=4, refs=["hauy", "moreda", "impresion"],
         cae="el colofón de manos (03, §3.11; Acción 12)"),
]

# encargos que la obra hace y que ninguna referencia contesta todavía: para la mano
ENCARGOS_ABIERTOS = [
    dict(encargo="D12 · la cinta tapa los ojos y la boca", op="inferir", tecnica="oclusión, del reel",
         cae="Acción 6 · encintar"),
    dict(encargo="D10 · el video es un bucle", op="secuenciar", tecnica="síntesis temporal: el ciclo",
         cae="Acción 11 · distribuir y volver a empezar"),
    dict(encargo="D11 · «Moverse como se mueve la piedra, / es decir, apenas»", op="secuenciar",
         tecnica="síntesis temporal: dos cuadros casi iguales", cae="Acción 9 · el agua quieta y la tocada"),
    dict(encargo="D3 · placas sueltas, con piel entre una y otra", op="agrupar",
         tecnica="región común: lo que separa", cae="P-01 · 2; Acción 11"),
]

# cómo entra una referencia nueva: los pasos del reel, hechos a la medida del proyecto
PASOS = [
    "Mírala en su archivo, no en una copia.",
    "Di qué mecanismo activa: la operación, el dominio y la técnica. Si no hay técnica, se suma una celda.",
    "Escribe qué se toma y qué no.",
    "Di dónde cae: la acción, el plano o la regla. Si no cae en ninguna parte, no entra.",
    "Di de dónde viene: quién, cuándo, con qué medio y con qué licencia.",
    "Marca su casilla, cambia su mirada a True y rehace las láminas.",
]

# ---------------------------------------------------------------- lo que queda afuera (10, §10.8 a §10.11)

AFUERA = [
    ("Una máscara de Paracas", "es andina, pero no de Tiwanaku: mezclarla confunde la referencia"),
    ("Los blemios de una crónica de prodigios, 1557", "la imaginería de las «razas monstruosas»"),
    ("La «muchacha turca» de Desprez", "una figura orientalista de vestuario"),
    ("Dos fotos de Tiahuanaco, en la Library of Congress", "sin fecha segura ni derechos confirmados"),
]

# lo que no se encontró, y dónde caería si aparece: (qué, columna, técnica)
NO_ENCONTRADO = [
    ("Visible Speech, de Melville Bell", "A10", 11),
    ("la imprenta de la Encyclopédie", "A5", 5),
    ("los frotados de latón", "A1", 1),
    ("el armonógrafo", "A10", 12),
    ("el fonodeik de Dayton Miller", "A10", 12),
    ("las sombras chinescas de Bursill", "A7", 14),
    ("la retícula del Romain du roi", "A3", 5),
    ("Geoffroy Tory", "A3", 6),
    ("Joseph Moxon", "A3", 6),
]

PENDIENTES = [
    "Mirar cada imagen y cada libro en su archivo, y corregir lo que no coincida con su ficha. En el fonógrafo, "
    "anotar si se ve la hoja de estaño.",
    "Leer en el libro de Haüy cómo se fundían y se apretaban las letras: puede ajustar la Acción 4.",
    "Escuchar el fonautograma de 1860 en First Sounds y decidir si se cita en el espécimen.",
    "Decidir si el Bourbonnoise Alphabet entra como contraste.",
    "Recorrer los archivos con tus ojos, empezando por la vista infinita del Public Domain Image Archive.",
    "Buscar una referencia para la cinta (Acción 6): la oclusión se toma del reel, pero ningún archivo trajo una.",
]

ARCHIVOS = [
    (PDR, "colecciones y ensayos; etiquetas alphabet, hand gestures, cymatics, recording",
     "https://publicdomainreview.org/"),
    (PDIA, "imágenes sueltas, con su libro y su año", "https://pdimagearchive.org/infinite-view/"),
    ("Wellcome Collection", "libros enteros de dominio público: Bonet, Haüy", "https://wellcomecollection.org/"),
    ("First Sounds y Library of Congress", "los fonautogramas: la voz escrita antes de oírse",
     "https://www.firstsounds.org/"),
    ("Smithsonian", "las grabaciones del Volta Laboratory, leídas con luz", "https://insider.si.edu/"),
    ("Perkins y APH Museum", "libros en relieve de 1786 a 1924", "https://aphmuseum.org/"),
    ("Rijksmuseum", "grabados con licencia CC0", "https://www.rijksmuseum.nl/"),
    ("Project Gutenberg", "textos de libros antiguos, como el de Haüy", "https://gutenberg.org/"),
]


def contar():
    """Los totales que citan las láminas y los documentos."""
    murray = [t for ts in TECNICAS_MURRAY.values() for t in ts]
    estados = {e: sum(1 for t in murray if t[2] == e) for e in ("toma", "cambia", "deja", "no")}
    return dict(murray=len(murray), sumadas=sum(len(v) for v in SUMADAS.values()), **estados,
                tecnicas=len(TECNICAS), referencias=len(REFERENCIAS),
                vistas=sum(1 for r in REFERENCIAS.values() if r["mirada"]))


if __name__ == "__main__":
    print(contar())
    for op in OPERACIONES:
        print(op, de_la_operacion(op))
