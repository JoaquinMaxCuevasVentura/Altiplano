// Chhaxwa. Cinco pruebas de construcción a partir de Altiplano
// El documento del proyecto, con un diseño que toma rasgos de Obra gruesa, de Smiljan Radić (2017):
// grotesca pequeña, números de página muy grandes, títulos verticales, fichas negras con texto blanco,
// una segunda voz en gris (allá, el inglés; aquí, la novela) y una página gris de entrada.
// Se compila con chhaxwa/documento/compilar.py (Typst 0.15).

#let negro = rgb("#151413")
#let gris = rgb("#8d8a85")
#let gris-pagina = rgb("#b7b5b0")
#let grotesca = ("Inter", "Liberation Sans", "Arial")

#set document(title: "Chhaxwa. Cinco pruebas de construcción a partir de Altiplano",
  author: "Joaquin Max Cuevas Ventura", date: none)
#set text(font: grotesca, size: 8.4pt, fill: negro, lang: "es", hyphenate: true)
#set par(leading: 0.5em, spacing: 0.95em, justify: false)
#set page(width: 230mm, height: 240mm, binding: left,
  margin: (top: 15mm, bottom: 36mm, inside: 20mm, outside: 15mm),
  footer-descent: 5mm,
  footer: context {
    let n = counter(page).get().first()
    align(if calc.even(n) { left } else { right },
      text(weight: "black", size: 46pt, tracking: -0.03em, str(n)))
  })

// --- piezas ------------------------------------------------------------------------------------------------
#let voz(cuerpo) = text(fill: gris)[#cuerpo]
#let rotulo(t) = text(size: 6.6pt, weight: "semibold", tracking: 0.08em, upper(t))
#let ficha(filas) = block(fill: negro, inset: (x: 3.2mm, y: 3mm), width: 100%, {
  set text(fill: white, size: 6.8pt)
  set par(spacing: 0.55em)
  for (k, v) in filas {
    grid(columns: (auto, 1fr, auto), column-gutter: 1.6mm, k, box(width: 1fr, repeat[#h(0.9mm)·]), v)
  }
})
#let titulo-vertical(t, sub) = rotate(-90deg, reflow: true)[
  #text(size: 25pt, weight: "bold", tracking: -0.01em, t) #h(3mm) #text(size: 11pt, fill: gris, sub)]
#let render(n, ruta, pie, ancho: 100%) = block(width: ancho, breakable: false, {
  image(ruta, width: 100%)
  v(1.3mm)
  grid(columns: (6.5mm, 1fr), column-gutter: 1mm,
    text(weight: "bold", size: 7.6pt, str(n)),
    [#text(size: 6.9pt)[#pie] \ #text(size: 6.9pt, fill: gris)[Render de Blender. No es una foto.]])
})
#let pasos(lista) = {
  set par(spacing: 0.7em)
  for (i, p) in lista.enumerate() [
    #grid(columns: (4mm, 1fr), text(weight: "bold", str(i + 1)), p)
  ]
}

#let diagrama(n, ruta, pie, ancho: 100%) = block(width: ancho, breakable: false, {
  image(ruta, width: 100%)
  v(1mm)
  grid(columns: (6.5mm, 1fr), column-gutter: 1mm,
    text(weight: "bold", size: 7.6pt, str(n)),
    [#text(size: 6.9pt)[#pie] \ #text(size: 6.9pt, fill: gris)[Diagrama en masas, cortado por la mitad, con una figura de 1,65 m.]])
})
#let lista-pruebas(lista) = {
  set par(spacing: 0.6em)
  for (marca, p, que) in lista [#grid(columns: (3.5mm, 1fr), text(weight: "bold", marca), [#text(weight: "bold")[#p.] #que])]
}

// --- cubierta -------------------------------------------------------------------------------------------------
#page(fill: gris-pagina, footer: none, margin: (top: 18mm, bottom: 18mm, inside: 20mm, outside: 16mm))[
  #text(size: 9pt, weight: "semibold", tracking: 0.08em)[JOAQUIN MAX CUEVAS VENTURA]
  #v(1fr)
  #text(size: 78pt, weight: "black", tracking: -0.035em, style: "italic")[Chhaxwa]
  #v(2mm)
  #text(size: 19pt, weight: "medium", tracking: -0.01em)[Cinco pruebas de construcción \ a partir de _Altiplano_]
  #v(9mm)
  #grid(columns: (1fr, 1fr), column-gutter: 8mm,
    text(size: 8.4pt)[Piedra, tierra y paja del altiplano. Cinco pruebas de técnica y seis exploraciones de forma, a partir de la novela de Raúl Botelho Gosálvez (1945).],
    voz[Noviembre de 2026. Planteado y modelado; ninguna maqueta construida todavía.])
]

// --- entrada gris ---------------------------------------------------------------------------------------------
#page(fill: gris-pagina)[
  #grid(columns: (1fr, 1fr), column-gutter: 7mm,
  [
    #text(weight: "bold")[_Chhaxwa_. Cinco pruebas de construcción a partir de _Altiplano_]

    En el vocabulario aymara que Ludovico Bertonio publicó en 1612, _chhaxwa_ nombra dos piedras. Una es la de los montones que se hacen al limpiar la chacra, las piedras «que amontonan limpiando las chácaras». La otra es la piedra «hincada en la pared para atar en ella los palos del techo» (Bertonio, 2011 [1612]: 330). Este proyecto va de una a otra. Empieza en un terreno que se despiedra y termina bajo el techo de una casa.

    Tiene dos partes. Cinco pruebas de construcción con piedra, tierra y paja del altiplano miden cada una una técnica andina descrita en una fuente, a partir de un pasaje de la novela _Altiplano_. Seis exploraciones juntan esas técnicas en obras: una montaña de piedra habitada, un corral techado, una casa redonda, una chullpa, una casa con bóveda y un troje alto.

    Va aparte del artículo «Cosecha de piedras», que lee la misma novela desde el dibujo. Es especulativo, porque Jatun-Kolla, el _ayllu_ de la novela, no existe; las técnicas y los materiales son reales.

    #v(3mm)
    #rotulo[Las reglas]
    #v(1mm)
    #pasos((
      [Una técnica documentada por prueba, con su fuente y su página.],
      [Un pasaje de la novela que la pida, con su página.],
      [Trabajo de riesgo: maquetas de material real, a tamaño natural, a 1:5 o a 1:10.],
      [La forma sale de la técnica. El arco se hace volando hiladas y el techo es de paja y barro.],
      [Nada de imágenes hechas con IA. Fotos de las maquetas sin retoques; los renders, rotulados como renders.],
      [Lo ritual se documenta y no se escenifica.],
      [Las manos se registran: cuántas personas, cuánto tiempo, quién hizo qué.],
    ))
  ],
  [
    #voz[«No más de cien hectáreas de tierra de labrantío, el resto es erial de piedras e inútil para la agricultura [...]. A medida que extraen piedras y las amontonan, brotan más y más, como paridas por la tierra. ¡Piedras! El trabajo más duro, más reñido y tenaz en Jatun-Kolla, rinde cosecha de piedras. Pero no importa: quizá un día la montaña de piedras sobrepase la altura del cerro; entonces será buena la tierra rescatada».]

    #voz[Raúl Botelho Gosálvez, _Altiplano_ (1982 [1945]: 9).]

    #v(8mm)
    #voz[Las referencias del método son dos. Las maquetas de material real de #raw("studio_cifuentes_ethz"), «HS26 – Atlas Works – 50% Stone and 50% Earth» (2026), con su proporción de materiales como regla y sus dibujos de proceso. Y _Obra gruesa_, de Smiljan Radić (2017), donde la hornilla del carbonero, cubierta «con barro y paja, apisonándolos con un palo corto, hasta formar una cúpula», se vuelve una esfera de barro que «no sirve para nada» (Radić, 2017: 24).]
  ])
]

// --- las seis exploraciones y las cinco pruebas -------------------------------------------------------------------
#let c(m, t) = [#text(weight: "bold", m) #t]
#rotulo[Seis exploraciones, cinco pruebas]
#v(2mm)
#{
  set text(size: 7.4pt)
  table(columns: (7mm, 31mm, 1fr, 1fr, 1fr, 1fr, 1fr), inset: (x: 1.2mm, y: 1.7mm),
    stroke: (x, y) => if y == 0 { (bottom: 0.6pt) } else { (bottom: 0.3pt + gris) },
    [], [*Exploración*], [*1. La cosecha*], [*2. El relleno*], [*3. El dintel*], [*4. La _p'ira_*], [*5. El fogón*],
    [*E1*], [La montaña habitada], c("●", [toda la piedra]), [], c("●", [la cámara volada]), [], c("○", [se entra en cuclillas]),
    [*E2*], [El corral techado], c("○", [la piedra de la pirca]), c("●", [la pirca de doble cara]), [], c("○", [el techo de ichu]), [],
    [*E3*], [La casa redonda], c("○", [la piedra de la pirca]), c("●", [la pirca de doble cara]), c("●", [el paso y la cúpula volados]), c("●", [las fajas y la _chhaxwa_]), c("●", [el fogón, el óculo y el _t'uju_]),
    [*E4*], [La chullpa], c("●", [las pilas de piedra]), [], c("●", [las pilas y la cámara]), c("○", [la cornisa de ichu]), [],
    [*E5*], [La casa de la bóveda], [], c("●", [los muros de doble cara]), c("●", [la bóveda volada]), [], c("●", [el fogón, el humo y el _t'uju_]),
    [*E6*], [La _pirwa_], c("○", [un apoyo es un montón]), c("○", [el otro, una pirca]), c("●", [la V volada]), c("●", [las fajas y la _chhaxwa_]), [],
  )
}
#v(1mm)
#text(size: 6.9pt, fill: gris)[● la técnica principal de la obra; ○ una que también usa.]
#v(5mm)
#grid(columns: (1fr, 1fr, 1fr), column-gutter: 6mm,
  [*Una sola cosecha.* Las seis usan la misma piedra, la angulosa que sale de despedregar el campo; la tierra del lugar y el ichu de la puna. La madera se reduce a palos cortos de queñua: «The absence of wood and timber has led the people of the Sierra to adopt a great many novel and striking devices» (Squier, 1877: 313).],
  [*Lo que cierra arriba se vuela.* Sin vigas, lo que cubre un espacio se hace volando hiladas: la cámara de E1, el paso y la cúpula de E3, las pilas y la cámara de E4, la bóveda de E5 y la V de E6. En la chullpa de Acora, «the stones begin to overlap, forming a kind of pointed arch» (ibid.: 353).],
  [*Del campo al troje.* Se entra en cuclillas a E1, de rodillas a E3 y de lado a E5. El orden va de una cosecha a otra: el montón, la pirca, la casa redonda, la tumba, la casa rectangular y el troje. E3 y E5 son la pareja de casas que describe Yampara Blanco, y E6, una de sus _pirwas_ (2019: 9 y 14).])
#v(1fr)
#block(width: 100%, breakable: false, {
  image("../renders/diagramas/diagrama_serie.png", width: 100%)
  v(0.5mm)
  box(width: 100%, height: 3.5mm, for (t, f) in (("E1", 9.8%), ("E2", 29.7%), ("E3", 45.4%), ("E4", 60.5%), ("E5", 77.4%), ("E6", 94.5%)) {
    place(left + top, dx: f - 2mm, text(weight: "bold", size: 7.6pt, t))
  })
  v(1mm)
  grid(columns: (6.5mm, 1fr), column-gutter: 1mm, text(weight: "bold", size: 7.6pt, "1"),
    [#text(size: 6.9pt)[*Las seis a la misma escala*, de frente, con una figura de 1,65 m junto a cada una. No es un plano de conjunto: si van en un mismo sitio lo decide el autor.] \ #text(size: 6.9pt, fill: gris)[Diagrama en masas.]])
})

// --- una exploración: dos páginas ------------------------------------------------------------------------------------
#let exploracion(n, titulo, texto, pasaje, pruebas, filas, nd, diag, pie-diag, nr, rend, pie-rend) = {
  pagebreak(to: "even", weak: true)
  grid(columns: (17mm, 1fr, 1fr), column-gutter: 5mm,
    titulo-vertical(titulo, "Exploración " + n),
    texto,
    [#voz(pasaje)
     #v(3mm)
     #rotulo[Las pruebas que junta]
     #v(1mm)
     #lista-pruebas(pruebas)
     #v(3mm)
     #diagrama(nd, diag, pie-diag)])
  place(bottom + left, block(width: 100%, ficha(filas)))
  pagebreak()
  grid(columns: (150mm, 1fr), column-gutter: 5mm,
    image(rend, width: 100%),
    align(bottom, grid(columns: (6.5mm, 1fr), column-gutter: 1mm, text(weight: "bold", size: 7.6pt, str(nr)),
      [#text(size: 6.9pt)[#pie-rend] \ #text(size: 6.9pt, fill: gris)[Render de Blender. No es una foto.]])))
}

#exploracion("E1", "La montaña habitada",
  [*Toda la cosecha en un cono.* La piedra que sale de despedregar no se lleva a otra parte. Se amontona en un cono bajo y hueco, de 7,2 m de diámetro y 2,6 m de alto. Por dentro hay una cámara redonda de muros verticales que, desde un metro de alto, vuelan hilada sobre hilada hasta dejar un óculo. Se entra en cuclillas por una caja de queñua que atraviesa el muro por el sur.

   Es la forma que eligió el autor recomponiendo dos de la exploración formal: el cono de piedra de 1B, más chato, con la entrada de 1C.

   #pasos((
     [Despedregar y separar la piedra en grande, mediana y menuda.],
     [Levantar la cámara con la piedra grande, hasta un metro.],
     [Volar las hiladas hacia el centro y cargar sus colas con la mediana y la menuda.],
     [Dejar el óculo arriba y forrar la boca con queñua.],
   ))

   La prueba 1 dirá cuánta piedra da una parcela de 2 × 2 m, y con eso cuántas parcelas hay que despedregar para levantar la montaña.],
  [«Pero no importa: quizá un día la montaña de piedras sobrepase la altura del cerro; entonces será buena la tierra rescatada» (p. 9).],
  (("●", "1. La cosecha", [toda la piedra, y nada más]), ("●", "3. El dintel", [la cámara volada]), ("○", "5. El fogón", [se entra en cuclillas])),
  (([exploración], [E1]), ([escala], [1:20]), ([diámetro y alto], [7,2 × 2,6 m, proyecto]), ([cámara], [2,8 m, volada desde 1 m, proyecto]), ([boca], [0,9 × 1,0 m, al sur, proyecto]), ([piedra], [unos 28 m³, cálculo])),
  2, "../renders/diagramas/diagrama_x1.png", [*Corte por la boca.* La cámara vuela 13,5 cm por cada hilada de 20 cm.],
  3, "../renders/render_forma_E1.jpg", [*La montaña habitada.* Maqueta 1:20.]
)

#exploracion("E2", "El corral techado",
  [*La pirca y el techo, separados.* Un corral redondo de pirca de doble cara, de 6 m, abierto al sur, con la mitad del corte llena de piedra menuda. Encima, sin tocarlo, un cono de ichu sobre ocho palos de queñua y un anillo atado. Entre la piedra y la paja queda una franja de cielo de 90 cm.

   El cerramiento es la pirca de la prueba 2 y el techo es el de la forma 5C. El autor eligió el cono; la versión con techo de pirámide queda como registro.

   #pasos((
     [Asentar las dos caras de la pirca y llenar el centro al mismo tiempo.],
     [Hincar ocho palos y atar el anillo.],
     [Atar los pares al anillo y techar con ichu en capas.],
     [Dejar arriba la salida del humo.],
   ))

   Falta decidir si bajo el ichu va una capa de _p'ira_, como en Enquelga (Šolc, 2011 [1975]: 105-109).],
  [«Las chujllas fueron reparadas del estrago, las pircas de piedra que separan las parcelas fueron compuestas» (p. 156).],
  (("●", "2. El relleno", [la pirca de doble cara]), ("○", "1. La cosecha", [la piedra de la pirca]), ("○", [4\. La _p'ira_], [el techo de ichu])),
  (([exploración], [E2]), ([escala], [1:20]), ([corral], [6 m, 1,4 m de alto, proyecto]), ([pirca], [0,7 m; relleno: la mitad, prueba 2]), ([palos], [ocho, de 2,3 m, proyecto]), ([techo], [cono de 6,8 × 3,4 m, proyecto])),
  4, "../renders/diagramas/diagrama_x2.png", [*Corte por la entrada.* Las dos caras de la pirca y el relleno de piedra menuda; los palos, el anillo y los pares.],
  5, "../renders/render_forma_E2C.jpg", [*El corral techado.* Maqueta 1:20.]
)

#exploracion("E3", "La casa redonda",
  [*La casa de todos los días.* Yampara Blanco describe el _muruqu uta_, la «casa de base de forma circular usada cotidianamente», con la puerta al este, un fogón al centro y un _t'uju_ al noreste, «por donde penetran los rayos solares» (2019: 13). Esta es una pirca redonda de doble cara y, encima, una cámara de champa volada hilada sobre hilada. Como una cúpula volada se cierra en cono, la forma baja de afuera es tierra que carga las colas de las hiladas.

   Se entra de rodillas por un paso de piedra de 1,2 m, con jambas de 60 cm y tres hiladas que vuelan 10 cm hasta cerrarse a 96 cm. La tierra se cubre con fajas de _p'ira_ de 0,7 m traslapadas como tejuelas, que escurren el agua. El óculo queda abierto bajo un sombrero de ichu, cuyos palos se atan a tres piedras hincadas, la _chhaxwa_. Unas lajas hincadas sirven de escalones para subir a quitarlo.

   Sale de una imagen del autor, corregida: la piedra de río pasó a ser la de la cosecha, y el ichu que tapaba el humo, un sombrero. Con E5 forma la pareja de la casa redonda y la cuadrada, que juntas «representan simbólica y culturalmente la feminidad y la masculinidad» (ibid.: 9).],
  [«En el dintel de Jatun-Kolla se detenían para ponerse de rodillas y besar el suelo que habían abandonado en el terror de la mala época» (p. 155).],
  (("●", "2, 3, 4 y 5", [la pirca, el paso y la cúpula volados, las fajas y la _chhaxwa_, el fogón y el _t'uju_]), ("○", "1. La cosecha", [la piedra de la pirca])),
  (([exploración], [E3]), ([escala], [1:20]), ([cuarto], [4,0 m; pirca de 0,6 × 1,2 m, proyecto]), ([paso], [0,6 × 0,96 m, la regla de la prueba 3]), ([cubierta], [fajas de 0,7 m, Šolc (2011 [1975]: 105)]), ([alto], [3,2 m hasta el óculo, cálculo])),
  6, "../renders/diagramas/diagrama_x3.png", [*Corte por el paso de entrada.* Las hiladas voladas del paso y de la cámara, la tierra que las carga y las fajas de _p'ira_.],
  7, "../renders/render_forma_E3.jpg", [*La casa redonda.* Maqueta 1:20.]
)

#exploracion("E4", "La chullpa",
  [*Una tumba levantada del suelo.* Cuatro pilas de pirca cuyas dos últimas hiladas vuelan hacia los pasos, una cama de lajas, una hilada de piedra y una pirámide escalonada de adobitos de pie, con una cámara volada adentro. El autor pidió la base de piedra y el adobe en aparejo vertical.

   Lo demás sale de la chullpa que Squier vio cerca de Palca: tenía 16 pies de alto, una plataforma «of roughly hewn stones» y una cornisa «formed by a layer of compacted ichu [...] placed horizontally, and cut off evenly as by a shears» (Squier, 1877: 243). Su boca miraba al este y medía «about eighteen inches wide and high» (ibid.: 244).

   Los adobitos van como libros en un estante, «en posición vertical, con la argamasa sólo en la parte superior e inferior» (Flores, cit. en Agüero Benites et al., 2015: 3), con 1,5 cm entre uno y otro (ibid.: 6). Es una técnica de la costa, de la Huaca Pucllana: aquí el adobe de la costa va sobre la piedra del altiplano, por decisión del autor.

   «Chulpa is the Aymara word for tomb» (Squier, 1877: 354). Sería la tumba que les faltó a los muertos de la novela.],
  [Condori queda bajo «la tumba agreste y anónima» de la mina (p. 154). Los que murieron en el éxodo, «abandonados en el cobijo de las tumbas de otras tierras, se pudrieron sin culto y sin recuerdo» (p. 156).],
  (("●", "1. La cosecha", [las pilas de piedra]), ("●", "3. El dintel", [las pilas y la cámara voladas]), ("○", [4\. La _p'ira_], [la cornisa de ichu])),
  (([exploración], [E4]), ([escala], [1:20]), ([base], [3,3 m; cuatro pilas, proyecto]), ([alto], [4,9 m, Squier (1877: 243)]), ([adobito], [19 × 14 × 6 cm, proyecto; 1,5 cm entre uno y otro]), ([boca y cornisa], [48 × 42 cm al este; 15 cm, Squier])),
  8, "../renders/diagramas/diagrama_x4.png", [*Corte por la boca.* La cámara vuela cuatro hiladas; abajo, el paso entre las pilas.],
  9, "../renders/render_forma_E4.jpg", [*La chullpa.* Maqueta 1:20.]
)

#exploracion("E5", "La casa de la bóveda",
  [*La casa de Enquelga bajo una bóveda volada.* El cuarto tiene la planta de la mediana de Šolc, 5,75 × 3,30 m (2011 [1975]: 93-94), dentro de un bloque de pirca de doble cara en talud. Hasta 80 cm los muros son verticales por dentro; de ahí arranca una bóveda de adobe por aproximación de hiladas, que vuela poco al principio y más cerca de la clave, hasta que las dos mitades quedan a 30 cm y se cierran con lajas. Falta una laja sobre el fogón, y por ahí sale el humo. Los riñones se rellenan con tierra para cargar las colas de las hiladas, y la pirca sigue arriba como un parapeto, con la bóveda adentro, como en la referencia R16.

   Se entra por una ranura de 50 cm en el muro del este, el ancho de un cuerpo, hacia donde mira la puerta de la casa grande (Suárez Jordán, 1990: 130). El _t'uju_ atraviesa la esquina noreste, apuntado al sol del 21 de junio a las 10 (prueba 5).

   La novela dice que las _chujllas_ «apenas se alzan dos metros del suelo». Una bóveda volada de 3,30 m de luz necesita casi dos metros de alto, y el bloque llega a 2,6 m. Si se quiere la casa chata, hay que bajar el arranque o angostar el cuarto.],
  [«Las chujllas no tienen cuartos ni mucho menos. Rectangulares y chatas, apenas se alzan dos metros del suelo» (p. 30). «En cuclillas, cerca del fuego, tenía la mirada en la sombra del suelo» (p. 32).],
  (("●", "5. El fogón", [el fogón, el humo y el _t'uju_]), ("●", "3. El dintel", [la bóveda volada]), ("●", "2. El relleno", [los muros de doble cara])),
  (([exploración], [E5]), ([escala], [1:20]), ([cuarto], [5,75 × 3,30 m, Šolc (2011 [1975]: 93-94)]), ([bloque], [7,55 × 5,10 × 2,6 m, proyecto]), ([bóveda], [arranque a 0,8 m; vuelos de 7 a 13 cm]), ([ranura y _t'uju_], [50 cm al este; 15 cm al noreste])),
  10, "../renders/diagramas/diagrama_x5.png", [*Corte por el fogón.* La bóveda volada, el relleno de los riñones, el humo y el sol que entra por el _t'uju_.],
  11, "../renders/render_forma_E5.jpg", [*La casa de la bóveda.* Maqueta 1:20.]
)

#exploracion("E6", [La _pirwa_],
  [*Un troje alto.* Yampara Blanco describe las _pirwas_ como «silos aéreos de granos, quinua y papas deshidratadas», con una boca arriba para cargar y otra abajo para sacar (2019: 14). Esta es un troje grande de champa en hiladas delgadas, levantado sobre dos apoyos que son las dos maneras de poner la piedra: una pirca y un montón.

   Entre los apoyos, la V se hace volando las hiladas de champa, como en los puentes que Squier vio, donde cada capa vuela «until the upper ones touch and brace against each other» (1877: 313). En su clave está la trampa por donde se saca lo guardado. Unas lajas hincadas en la cara sur suben hasta la boca de carga, y otras traban las hiladas y asoman.

   El techo es de un agua, de fajas de _p'ira_ sobre seis palos de queñua. Cada palo se ata a una piedra hincada bajo su extremo, la _chhaxwa_ «hincada en la pared para atar en ella los palos del techo» (Bertonio, 2011 [1612]: 330).

   Era la torre de champa, que fue E3. Se bajó un metro; aun así, lo primero que hay que probar es si se sostiene llena.],
  [«Todo era pronóstico de abundancia, de trojes altos y almiares llenos» (p. 157).],
  (("●", "3. El dintel", [la V volada]), ("●", [4\. La _p'ira_], [las fajas y la _chhaxwa_]), ("○", "1 y 2", [un apoyo es un montón y el otro una pirca])),
  (([exploración], [E6]), ([escala], [1:20]), ([planta], [3,0 × 1,6 m; de 3,6 a 4,6 m, proyecto]), ([champa], [40 × 25 × 12 cm, proyecto]), ([bocas], [unos 30 × 35 cm, Yampara Blanco (2019: 14)]), ([fajas], [2,5 × 0,7 m, Šolc (2011 [1975]: 105)])),
  12, "../renders/diagramas/diagrama_x6.png", [*Corte a lo largo.* La V volada con la trampa en su clave, lo guardado y el techo sobre palos atados a las piedras hincadas.],
  13, "../renders/render_forma_E6.jpg", [*La _pirwa_.* Maqueta 1:20.]
)

// --- las cinco pruebas: una página cada una ----------------------------------------------------------------------
#let prueba(n, titulo, texto, pasaje, mide, filas, formas) = {
  pagebreak()
  grid(columns: (17mm, 1fr, 1fr), column-gutter: 5mm,
    titulo-vertical(titulo, "Prueba " + n),
    texto,
    [#voz(pasaje)
     #v(3mm)
     #rotulo[Qué se mide]
     #v(1mm)
     #set par(spacing: 0.6em)
     #for m in mide [#grid(columns: (3mm, 1fr), [·], m)]
     #v(3mm)
     #ficha(filas)])
  v(1fr)
  rotulo[Formas exploradas]
  v(1.5mm)
  grid(columns: (1fr, 1fr, 1fr), column-gutter: 5mm, ..formas.map(f => render(f.at(0), f.at(1), f.at(2))))
}

#prueba("1", "La cosecha",
  [*Despedregar y amontonar.* El aymara tiene un verbo para la faena, _wanqathapiña_, «amontonar piedras sacándolas» (Bertonio, 2011 [1612]: 77), y un nombre, _chhaxwa_, para las dos piedras del título (ibid.: 330). Las fuentes no dicen cómo se hace un montón en el campo, y la novela tampoco. La prueba mide la faena.

   *La regla.* La obra se levanta solo con la piedra que sale de despedregar el terreno donde se levanta.

   #pasos((
     [Marcar una parcela de 2 × 2 m, en dieciséis cuadros de 50 cm.],
     [Despedregar hasta 20 cm y separar la piedra en grande, mediana y menuda. Pesarla.],
     [Levantar cuatro montones con toda la piedra. Medir el talud.],
     [Hincar una piedra larga en cada montón, atar dos palos y tender dos fajas de _p'ira_.],
   ))],
  [«A medida que extraen piedras y las amontonan, brotan más y más, como paridas por la tierra» (p. 9).],
  ([El peso de cada clase de piedra en cada cuadro.], [El volumen, el talud y la altura de cada montón.], [Las horas y las manos.]),
  (([prueba], [1]), ([escala], [tamaño natural]), ([parcela], [2 × 2 m, proyecto]), ([fuentes], [Bertonio (2011 [1612]: 77, 330)])),
  ((14, "../renders/render_forma_1B.jpg", [*La montaña de piedras.* 1:20.]),
   (15, "../renders/render_forma_1A.jpg", [*Cuatro montones y un techo.* 1:10.]),
   (16, "../renders/render_forma_1C.jpg", [*El montón habitado.* 1:20.]))
)

#prueba("2", "El relleno",
  [*La pirca de doble cara.* Dos caras de piedra grande y un relleno de piedra menuda, para la que Bertonio tenía nombre: «Piedra para entremeter en los edificios y llenar sus huecos. Ch'äta, chillpa, k'ak'i qala» (Bertonio, 2011 [1612]: 246).

   *Lo que pone a prueba.* El artículo dice que en una pirca de doble cara «las piedras grandes dan la cara, pero adentro van las menudas, y sin ese relleno el muro se cae».

   *La regla.* El relleno ocupa la mitad del corte. Tres variantes a 1:5: con piedra menuda, con tierra apisonada y sin relleno. Se saca el relleno por una boca al pie, de a poco, hasta que el muro caiga.],
  [En la sequía, «las pircas se derrumbaban igual que murallas milenarias» (p. 72).],
  ([El relleno sacado a la primera grieta y a la caída.], [El desplome de cada cara.], [La forma del derrumbe.]),
  (([prueba], [2]), ([escala], [1:5]), ([muro], [2,0 × 1,2 × 0,6 m, proyecto]), ([fuentes], [Bertonio (2011 [1612]: 246)])),
  ((17, "../renders/render_forma_2C.jpg", [*El corral cortado.* 1:20.]),
   (18, "../renders/render_forma_2A.jpg", [*El tramo de prueba.* 1:5.]),
   (19, "../renders/render_forma_2B.jpg", [*Pilares de mitad y mitad.* 1:20.]))
)

#prueba("3", "El dintel",
  [*El arco por aproximación de hiladas.* Squier lo vio en los puentes de champa camino a Copacabana: cada capa vuela sobre la de abajo «until the upper ones touch and brace against each other, forming a rude kind of arch» (Squier, 1877: 313). La champa se deja secar unos veinte días (Vitulas-Quille y Reynoso-Machaca, 2025: 9).

   *La regla.* La altura del paso sale de cuánto vuela cada hilada. Con jambas de 60 cm y abertura de 60 cm, si cada hilada vuela 5 cm el paso mide 1,32 m; si vuela 10 cm, 0,96 m; si vuela 15 cm, 0,84 m.

   Es la técnica que más se repite en las exploraciones: la cámara de E1, el paso y la cúpula de E3, las pilas y la cámara de E4, la bóveda de E5 y la V de E6.],
  [«En el dintel de Jatun-Kolla se detenían para ponerse de rodillas y besar el suelo» (p. 155).],
  ([El vuelo máximo de champa, adobe y laja.], [Las hiladas y el alto del paso.], [Quién cruza y cómo.]),
  (([prueba], [3]), ([escala], [tamaño natural]), ([bloque], [40 × 25 × 12 cm, proyecto]), ([fuentes], [Squier (1877: 313)])),
  ((20, "../renders/render_forma_3B.jpg", [*La celda volada.* 1:20.]),
   (21, "../renders/render_forma_3A.jpg", [*El paso.* 1:10.]),
   (22, "../renders/render_forma_3C.jpg", [*El umbral hundido.* 1:20.]))
)

#prueba("4", [La _p'ira_],
  [*Un techo que se hace en el suelo.* En Enquelga, el constructor echa paja «cruzada, en varias direcciones», la pisa y la cubre de barro, que los ayudantes pisotean con sus costales, «dejando sobre el barro el dibujo de la estructura de los sacos». Después la cortan en fajas de unos 2,5 × 0,7 m que se suben a una armadura de pares atados y «se mantienen por su peso propio» (Šolc, 2011 [1975]: 102-107).

   *La regla.* El techo se dibuja primero en el suelo, a tamaño real. Se pisa, queda la huella del tejido, se corta y se sube.

   En las exploraciones, las fajas cubren la casa redonda (E3), traslapadas como tejuelas, y el techo de la _pirwa_ (E6).],
  [Sin gente, los techos quedan «desfondados» (p. 79).],
  ([La paja y el barro por metro cuadrado.], [El peso húmedo y seco.], [La huella de cada tejido, con luz rasante.]),
  (([prueba], [4]), ([escala], [tamaño natural]), ([faja], [2,5 × 0,7 m]), ([fuentes], [Šolc (2011 [1975]: 102-109)])),
  ((23, "../renders/render_forma_4C.jpg", [*El pajar levantado.* 1:20.]),
   (24, "../renders/render_forma_4A.jpg", [*La faja sobre los pares.* 1:5.]),
   (25, "../renders/render_forma_4B.jpg", [*El techo a medio subir.* 1:20.]))
)

#prueba("5", "El fogón",
  [*La casa de Enquelga y el* _t'uju_. La planta sale de la tabla de Šolc: la mediana de 17 dormitorios de adobe es de 5,75 × 3,30 m (Šolc, 2011 [1975]: 93-94). La puerta mira al este (Suárez Jordán, 1990: 130). El _t'uju_ es un «orificio pequeño» al noreste por donde entra el sol y sale el humo (Yampara Blanco, 2019: 13).

   *La regla.* La casa se mide desde el cuerpo en cuclillas.

   *El sol.* El 21 de junio el sol pasa por el noreste hacia las 10, a 35° de altura; el 21 de diciembre no pasa nunca. Un agujero de 15 cm en un muro de 40 cm solo deja pasar el sol a menos de unos 20° de su eje, así que la dirección del _t'uju_ elige la fecha y la hora.],
  [«En cuclillas, cerca del fuego, tenía la mirada en la sombra del suelo donde a veces resbalaba la cinta bermeja del resplandor del fogón» (p. 32).],
  ([La mancha de sol en cada fecha y hora.], [Por dónde sale el humo.], [Qué se ve desde las cuclillas.]),
  (([prueba], [5]), ([escala], [1:10]), ([planta], [5,75 × 3,30 m, cálculo]), ([fuentes], [Šolc; Yampara Blanco; Suárez Jordán])),
  ((26, "../renders/render_forma_5C.jpg", [*El cono del fogón.* 1:20.]),
   (27, "../renders/render_forma_5A.jpg", [*La chujlla de Enquelga.* 1:10.]),
   (28, "../renders/render_forma_5B.jpg", [*La casa partida.* 1:20.]))
)

// --- el proceso: las piezas para recomponer y la serie del tiempo ---------------------------------------------------
#pagebreak()
#let pieza(codigo, ruta) = block(width: 100%, breakable: false, {
  image(ruta, width: 100%)
  v(0.3mm)
  text(weight: "bold", size: 6.8pt, codigo)
})
#grid(columns: (17mm, 1fr), column-gutter: 5mm,
  titulo-vertical("El proceso", "Piezas para recomponer"),
  [#grid(columns: (1fr,) * 8, column-gutter: 2.5mm, row-gutter: 2mm,
     ..("3a", "3b", "3c", "3d", "3e", "3f", "3g", "3h", "4a", "4b", "4c", "4d", "4e", "4f", "4g", "4h", "4i", "4j",
        "5a", "5b", "5c", "5d", "5e", "5f", "5g", "5h", "5i", "t1", "t2", "t3", "t4").map(p =>
        pieza(p, "../renders/piezas/pieza_" + p + ".png")))
   #v(3mm)
   #grid(columns: (1fr, 1fr), column-gutter: 7mm,
     [Para recomponer las pruebas 3, 4 y 5, el autor pidió piezas en diagrama: 3a a 3h para el dintel, 4a a 4j para la _p'ira_ y 5a a 5i para el fogón. De la torre de hiladas voladas sobre dos pircas (3h) salieron la chullpa (E4), con una nota del autor, y la _pirwa_ (E6). Los adobitos de pie de 5i pasaron a la chullpa.

      La serie t1 a t4 muestra E2 en el tiempo: recién hecho, con el techo «desfondado» (p. 79), con solo los palos y con la pirca a medio caer. Un techo de paja dura de diez a doce años (Šolc, 2011 [1975]: 109).],
     voz[Diagramas en masas, con una figura de 1,65 m. Las medidas son del proyecto y se ajustaron al recomponer.])])

// --- la exploración formal ----------------------------------------------------------------------------------------
#pagebreak()
#grid(columns: (17mm, 1fr, 1fr), column-gutter: 5mm,
  titulo-vertical("Cinco operaciones", "Exploración formal"),
  [Las referencias del autor se leen como operaciones, y cada operación se ata a una técnica o a un dato del altiplano, para que la forma no venga de fuera.

   *La masa sobre lo liviano.* Lo pesado arriba y lo delgado abajo. Las fajas de _p'ira_ «se mantienen por su peso propio» sobre palos atados (Šolc, 2011 [1975]: 107).

   *La masa ahuecada.* Un volumen macizo al que se le quita un hueco a la medida del cuerpo, como la _amaya uta_, «sepultura como casa sobre la tierra» (Bertonio, 2011 [1612]: 276).

   *El montón como apoyo.* La piedra suelta carga lo que está encima.

   *La proporción y las capas.* Mitad piedra y mitad tierra, o un cuarto y tres cuartos, que en el corte se ven como capas.

   *El óculo y el pozo.* Una abertura arriba y un suelo que baja. El _t'uju_ es «salida del humo como una chimenea» (Yampara Blanco, 2019: 13).

   De estas operaciones salieron quince formas, tres por prueba, y de ellas, de las piezas y de las referencias, las seis exploraciones.],
  voz[Las referencias: dos maquetas de #raw("studio_cifuentes_ethz") (2026); una pirámide truncada de terciado sobre una plataforma de listones; un cono sobre palos encima de un pozo, y una piedra de granito partida y forrada de madera, que parece ser de Smiljan Radić y Marcela Correa: en _Obra gruesa_ cuentan que cortaron «a mitad el granito de 19 toneladas» para _El Niño Escondido en un Pez_ (Radić, 2017: 230-231). Después llegaron once más: dos planos inclinados con paja (R6), una masa de paja sobre zancos con una caja (R7), una torre de maderos sobre dos pircas (R8, de la que sale E6), un anillo de tierra con rendijas, una torre en ruina con corona de tablas, un tronco de cono de tablillas, una torre de lamas, una torre de celosía sobre una base escalonada, una pirámide sobre patas en V y un bloque de muros en talud con una ranura y una bóveda adentro (R16, de la que sale E5), las fotos del autor de los adobitos de la Huaca Pucllana y una imagen suya de una casa redonda, de la que sale E3. Las imágenes no se reproducen: son obra de terceros o fotos del autor que no se publican sin su permiso.])

// --- el prototipo en el paisaje ---------------------------------------------------------------------------------------
#pagebreak()
#block(width: 100%, {
  image("../renders/render_prototipo_pirca_paisaje.jpg", width: 100%)
  v(1.3mm)
  grid(columns: (6.5mm, 1fr), column-gutter: 1mm, text(weight: "bold", size: 7.6pt, "29"),
    [#text(size: 6.9pt)[*Una pirca en el altiplano.* La primera prueba del flujo de trabajo: 460 piedras procedurales, 2.260 matas de ichu y el cielo físico de Blender a 3.850 m, con el sol del 21 de junio a las 10 (altura 35,1°, acimut 44,3°).] \ #text(size: 6.9pt, fill: gris)[Render de Blender. No es una foto.]])
})
#v(8mm)
#grid(columns: (1fr, 1fr), column-gutter: 7mm,
  [*El sol en La Paz.* 16,5° S y 68,15° O, hora de Bolivia, sin contar los cerros. Altura y acimut del sol, en grados; el acimut, desde el norte.

   #set text(size: 7.4pt)
   #table(columns: 5, stroke: (x, y) => if y == 0 { (bottom: 0.6pt) } else { (bottom: 0.3pt + gris) }, inset: (x: 0pt, y: 1.6mm),
     column-gutter: 2.5mm,
     [*Fecha*], [*Salida*], [*9:00*], [*10:00*], [*Mediodía*],
     [21 de junio], [7:04, 65,5°], [24,2° · 53,9°], [35,1° · 44,3°], [12:34, 50,0° N],
     [20 de marzo], [6:40, 90,6°], [33,3° · 79,4°], [47,3° · 72,1°], [12:41, 73,9° N],
     [21 de diciembre], [6:01, 114,5°], [40,3° · 107,0°], [54,1° · 107,3°], [12:30, 83,1° S])],
  voz[Las fórmulas son las de la NOAA y están en #raw("blender/comun.py"). En Blender, el giro del sol del cielo físico coincide con el acimut de esta tabla si el eje y apunta al norte; se comprobó con un render de prueba. El _t'uju_ de E5 apunta a la columna de las 10 del 21 de junio.])

// --- fuentes y colofón ---------------------------------------------------------------------------------------------------
#pagebreak()
#grid(columns: (1fr, 1fr), column-gutter: 7mm,
  [#rotulo[Fuentes]
   #v(1mm)
   #set par(spacing: 0.75em)
   #set text(size: 7.8pt)
   Agüero Benites, Johnny; Cerón Uribe, Javier; Gonzáles Lévano, Juan Carlos y Méndez Landa, María Teresa (2015). «Análisis estructural de dos muros de adobe con diferente sistema de aparejo». Ponencia en el 15.º Seminario Iberoamericano de Arquitectura y Construcción con Tierra (SIACOT). En Dialnet.

   Bertonio, Ludovico (2011 [1612]). _Transcripción del vocabulario de la lengua aymara_. La Paz: Radio San Gabriel (1993) e ILLA-A (ed. digital).

   Botelho Gosálvez, Raúl (1982 [1945]). _Altiplano_. 7.ª ed. La Paz: Juventud.

   Chandler, Alan (2017). «Smiljan Radić: Traducir el diseño a la materialidad–el “trabajo de riesgo”». En Radić (2017): 213 y ss.

   Radić, Smiljan (2017). _Obra gruesa. Arquitectura ilustrada por Smiljan Radić_. Ed. de Smiljan Radić y Gonzalo Puga. Santiago de Chile: Ediciones Puro Chile y Fundación Antenna.

   Šolc, Václav (2011 [1975]). «Casa aymara en Enquelga». _Chungara_, 43(1): 89-111.

   Squier, Ephraim George (1877). _Peru: Incidents of Travel and Exploration in the Land of the Incas_. Nueva York: Harper & Brothers.

   #raw("studio_cifuentes_ethz") (2026). «HS26 – Atlas Works – 50% Stone and 50% Earth». Instagram.

   Suárez Jordán, Marina (1990). «Permanencia y cambio: el caso de la vivienda aymara en centros poblados del altiplano boliviano». _Ciudad y Territorio_, 85: 127-135.

   Vitulas-Quille, Yasmani y Reynoso-Machaca, Karina (2025). «Putuco as a Pre-Hispanic Construction Technology and Ch'ampa as Traditional Masonry Blocks». IntechOpen. doi: 10.5772/intechopen.1009877.

   Yampara Blanco, Pacha Yapucha (2019). «La arquitectura de los pueblos milenarios del altiplano». _Revista Nodo_, 14(27): 8-23.],
  [#rotulo[Colofón]
   #v(1mm)
   _Chhaxwa_ es un proyecto de Joaquin Max Cuevas Ventura. Las traducciones de Squier y de Vitulas-Quille y Reynoso-Machaca son nuestras.

   Los renders los calcula Blender 5.0.1 a partir de geometría, materiales y luz escritos en código (#raw("chhaxwa/blender/")). Son predicciones de cómo quedarían las maquetas y no fotos. Cuando se construyan, sus fotos irán al lado. Los diagramas son modelos de masas del mismo código.

   Claude (Anthropic), un asistente de IA generativa, redactó los textos con las indicaciones del autor, cotejó las fuentes, calculó las medidas y la tabla del sol y escribió el código de los modelos y de este documento. Ninguna imagen viene de un generador de imágenes.

   El diseño toma rasgos del de _Obra gruesa_: la grotesca pequeña, los números de página grandes, los títulos verticales, las fichas negras y una segunda voz en gris, que allá es el inglés y aquí es la novela. Compuesto en Typst con la letra Inter.

   #voz[Noviembre de 2026.]])
