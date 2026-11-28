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
    [#text(size: 6.9pt)[#pie] \ #text(size: 6.9pt, fill: gris)[Diagrama en masas, cortado por la mitad.]])
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
    [*E2*], [El corral techado], c("○", [la piedra de la pirca]), c("●", [la pirca de doble cara]), [], c("●", [la _p'ira_ bajo el ichu]), [],
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
  [*Del campo al troje.* Los pasajes salen del artículo «Cosecha de piedras» y se leen de a pares: el montón en que se habita y el que entierra (E1 y E4), las dos casas (E3 y E5), el lindero y el troje (E2 y E6). El orden va de una cosecha a otra: el montón, la pirca, la casa redonda, la tumba, la casa rectangular y el troje. E3 y E5 son la pareja de casas que describe Yampara Blanco, y E6, una de sus _pirwas_ (2019: 9 y 14).])
#v(1fr)
#block(width: 100%, breakable: false, {
  image("../renders/diagramas/diagrama_serie.png", width: 100%)
  v(0.5mm)
  box(width: 100%, height: 3.5mm, for (t, f) in (("E1", 9.8%), ("E2", 29.7%), ("E3", 45.4%), ("E4", 60.5%), ("E5", 77.4%), ("E6", 94.5%)) {
    place(left + top, dx: f - 2mm, text(weight: "bold", size: 7.6pt, t))
  })
  v(1mm)
  grid(columns: (6.5mm, 1fr), column-gutter: 1mm, text(weight: "bold", size: 7.6pt, "1"),
    [#text(size: 6.9pt)[*Las seis a la misma escala*, de frente. No es un plano de conjunto: si van en un mismo sitio lo decide el autor.] \ #text(size: 6.9pt, fill: gris)[Diagrama en masas.]])
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
  [*La pirca y el techo, rehechos.* Un corral redondo de pirca de doble cara, de 6 m, abierto al sur, con la mitad del corte llena de piedra menuda. Encima, un cono de ichu con _p'ira_ debajo, como en Enquelga (Šolc, 2011 [1975]: 105-107). Entre la piedra y la paja queda una franja de cielo de 90 cm.

   El techo se apoya en palos de queñua de 1,4 m parados sobre la pirca y en dos más largos que flanquean la entrada. Sobre ellos va un anillo atado, del anillo a la punta suben dieciséis pares, y sobre los pares van las fajas de _p'ira_ y el ichu en capas.

   #pasos((
     [Asentar las dos caras de la pirca y llenar el centro al mismo tiempo.],
     [Parar los palos sobre la pirca y atar el anillo.],
     [Atar los pares, subir las fajas de _p'ira_ y techar con ichu en capas.],
     [Dejar arriba la salida del humo.],
   ))

   El autor eligió el cono y pidió la _p'ira_; la versión con techo de pirámide queda como registro.],
  [«Las pircas derruidas; desfondados los techos de las casas» (p. 79). Al volver, «las chujllas fueron reparadas del estrago, las pircas de piedra que separan las parcelas fueron compuestas» (p. 156).],
  (("●", "2. El relleno", [la pirca de doble cara]), ("●", [4\. La _p'ira_], [las fajas bajo el ichu]), ("○", "1. La cosecha", [la piedra de la pirca])),
  (([exploración], [E2]), ([escala], [1:20]), ([corral], [6 m, 1,4 m de alto, proyecto]), ([pirca], [0,7 m; relleno: la mitad, prueba 2]), ([palos], [1,4 m, sobre la pirca, proyecto]), ([techo], [6,8 × 3,4 m; fajas de 0,7 m, Šolc (2011 [1975]: 105)])),
  4, "../renders/diagramas/diagrama_x2.png", [*Corte por la entrada.* La pirca y su relleno; los palos sobre la pirca, el anillo, los pares, la _p'ira_ y el ichu.],
  5, "../renders/render_forma_E2C.jpg", [*El corral techado.* Maqueta 1:20.]
)

#exploracion("E3", "La casa redonda",
  [*La casa de todos los días.* Yampara Blanco describe el _muruqu uta_, la «casa de base de forma circular usada cotidianamente», con la puerta al este, un fogón al centro y un _t'uju_ al noreste, «por donde penetran los rayos solares» (2019: 13). Esta es una pirca redonda de doble cara y, encima, una cámara de champa volada hilada sobre hilada. Como una cúpula volada se cierra en cono, la forma baja de afuera es tierra que carga las colas de las hiladas.

   Se entra de rodillas por un paso de piedra de 1,2 m, con jambas de 60 cm y tres hiladas que vuelan 10 cm hasta cerrarse a 96 cm. La tierra se cubre con fajas de _p'ira_ de 0,7 m traslapadas como tejuelas, que escurren el agua. El óculo queda abierto bajo un sombrero de ichu, cuyos palos se atan a tres piedras hincadas, la _chhaxwa_. Unas lajas hincadas sirven de escalones para subir a quitarlo.

   Sale de una imagen del autor, corregida: la piedra de río pasó a ser la de la cosecha, y el ichu que tapaba el humo, un sombrero. Con E5 forma la pareja de la casa redonda y la cuadrada, que juntas «representan simbólica y culturalmente la feminidad y la masculinidad» (ibid.: 9).],
  [«Desde el portal de su chujlla el Paulo Huanca, rodeado de su mujer e hijos, miró irse a los desterrados» (p. 34). Al volver, «en el dintel de Jatun-Kolla se detenían para ponerse de rodillas y besar el suelo que habían abandonado en el terror de la mala época» (p. 155).],
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
  [Juan Condori, a su compañera muerta, «amontonó piedras sobre el cadáver» (p. 35). A él, en la mina, lo cubre «un informe montón de rocas, lodo y maderos astillados» (p. 154).],
  (("●", "1. La cosecha", [las pilas de piedra]), ("●", "3. El dintel", [las pilas y la cámara voladas]), ("○", [4\. La _p'ira_], [la cornisa de ichu])),
  (([exploración], [E4]), ([escala], [1:20]), ([base], [3,3 m; cuatro pilas, proyecto]), ([alto], [4,9 m, Squier (1877: 243)]), ([adobito], [19 × 14 × 6 cm, proyecto; 1,5 cm entre uno y otro]), ([boca y cornisa], [48 × 42 cm al este; 15 cm, Squier])),
  8, "../renders/diagramas/diagrama_x4.png", [*Corte por la boca.* La cámara vuela cuatro hiladas; abajo, el paso entre las pilas.],
  9, "../renders/render_forma_E4.jpg", [*La chullpa.* Maqueta 1:20.]
)

#exploracion("E5", "La casa de la bóveda",
  [*La casa de Enquelga bajo una bóveda volada, en dos metros.* El cuarto tiene la planta de la mediana de Šolc, 5,75 × 3,30 m (2011 [1975]: 93-94), dentro de un bloque de pirca de doble cara en talud que no pasa de los dos metros de la novela. Los muros son verticales por dentro solo hasta 35 cm, la altura de los camastros; de ahí arranca una bóveda de adobe por aproximación de hiladas, empinada como el arco apuntado de la chullpa de Acora (Squier, 1877: 353), hasta que las dos mitades quedan a 43 cm y se cierran con lajas, a 1,86 m. Falta una laja sobre el fogón, y por ahí sale el humo. Los riñones se rellenan con tierra para cargar las colas de las hiladas, y la pirca sigue arriba como un parapeto, con la bóveda adentro, como en la referencia R16.

   Se entra por una ranura de 50 cm en el muro del este, el ancho de un cuerpo, hacia donde mira la puerta de la casa grande (Suárez Jordán, 1990: 130). El _t'uju_ atraviesa la esquina noreste, apuntado al sol del 21 de junio a las 10 (prueba 5).

   Adentro se está de pie solo al centro, y junto a los muros, en cuclillas o acostado. Para que quepa en dos metros, cada hilada vuela de 11 a 13 cm, un tercio de su largo: es lo primero que hay que probar.],
  [«Rectangulares y chatas, apenas se alzan dos metros del suelo» (p. 30). «De las vigas toscas y mal unidas con lazos de paja trenzada, cuelgan las hoces, el arado, el yugo de madera» (p. 31).],
  (("●", "5. El fogón", [el fogón, el humo y el _t'uju_]), ("●", "3. El dintel", [la bóveda volada]), ("●", "2. El relleno", [los muros de doble cara])),
  (([exploración], [E5]), ([escala], [1:20]), ([cuarto], [5,75 × 3,30 m, Šolc (2011 [1975]: 93-94)]), ([bloque], [7,55 × 5,10 × 2 m, la novela (p. 30)]), ([bóveda], [arranque a 0,35 m; clave a 1,9 m]), ([ranura y _t'uju_], [50 cm al este; 15 cm al noreste])),
  10, "../renders/diagramas/diagrama_x5.png", [*Corte por el fogón.* La bóveda volada, el relleno de los riñones, el humo y el sol que entra por el _t'uju_.],
  11, "../renders/render_forma_E5.jpg", [*La casa de la bóveda.* Maqueta 1:20.]
)

#exploracion("E6", [La _pirwa_],
  [*Un troje alto.* Yampara Blanco describe las _pirwas_ como «silos aéreos de granos, quinua y papas deshidratadas», con una boca arriba para cargar y otra abajo para sacar (2019: 14). Esta es un troje grande de champa en hiladas delgadas, levantado sobre dos apoyos que son las dos maneras de poner la piedra: una pirca y un montón.

   Entre los apoyos, la V se hace volando las hiladas de champa, como en los puentes que Squier vio, donde cada capa vuela «until the upper ones touch and brace against each other» (1877: 313). En su clave está la trampa por donde se saca lo guardado. Unas lajas hincadas en la cara sur suben hasta la boca de carga, y otras traban las hiladas y asoman.

   El techo es de un agua, de fajas de _p'ira_ sobre seis palos de queñua. Cada palo se ata a una piedra hincada bajo su extremo, la _chhaxwa_ «hincada en la pared para atar en ella los palos del techo» (Bertonio, 2011 [1612]: 330).

   Era la torre de champa, que fue E3. Se bajó un metro; aun así, lo primero que hay que probar es si se sostiene llena.],
  [«Todo era pronóstico de abundancia, de trojes altos y almiares llenos». Del hambre no se hablaba: «los comunarios, desde la atalaya de la esperanza, sólo miraban el horizonte» (p. 157).],
  (("●", "3. El dintel", [la V volada]), ("●", [4\. La _p'ira_], [las fajas y la _chhaxwa_]), ("○", "1 y 2", [un apoyo es un montón y el otro una pirca])),
  (([exploración], [E6]), ([escala], [1:20]), ([planta], [3,0 × 1,6 m; de 3,6 a 4,6 m, proyecto]), ([champa], [40 × 25 × 12 cm, proyecto]), ([bocas], [unos 30 × 35 cm, Yampara Blanco (2019: 14)]), ([fajas], [2,5 × 0,7 m, Šolc (2011 [1975]: 105)])),
  12, "../renders/diagramas/diagrama_x6.png", [*Corte a lo largo.* La V volada con la trampa en su clave, lo guardado y el techo sobre palos atados a las piedras hincadas.],
  13, "../renders/render_forma_E6.jpg", [*La _pirwa_.* Maqueta 1:20.]
)

// --- las láminas de detalle: una por página, en serie aparte (L1-L6) ------------------------------------------------
#let lamina(n, ruta, pie, texto) = {
  pagebreak()
  block(width: 100%, breakable: false, {
    image(ruta, width: 100%)
    v(1.3mm)
    grid(columns: (6.5mm, 1fr), column-gutter: 1mm,
      text(weight: "bold", size: 7.6pt, "L" + str(n)),
      [#text(size: 6.9pt)[#pie] \ #text(size: 6.9pt, fill: gris)[Lámina A3 en DXF, editable en QCAD (#raw("detalles/detalle_E" + str(n) + ".dxf")). Dibujo hecho con código.]])
  })
  v(4mm)
  texto
}

#lamina(1, "../detalles/detalle_E1.png", [*E1. La montaña habitada.* Corte por la boca, 1:25.],
  grid(columns: (1fr, 1fr), column-gutter: 7mm,
    [*Los detalles.* Cada exploración tiene una lámina de detalle, un A3 a una sola escala, dibujado en metros reales en DXF, que se abre y se edita en QCAD o en cualquier programa de CAD. Las seis están en `detalles/`, con un PDF para imprimirlas. Los grosores son los del dibujo de arquitectura: lo que el plano corta lleva un contorno grueso y sus juntas finas, lo que se ve más allá va en gris y los sombreados, uno por material, van en un gris muy fino. Las láminas resuelven cosas que los modelos dejaban abiertas, y las marcan como decisiones del proyecto.],
    [La cámara es vertical hasta un metro y después vuela 13,5 cm por cada hilada de 20 cm, hasta el óculo de 64 cm. El paso de la boca atraviesa el cono bajo un dintel de lajas y sigue por la caja de queñua, que sale 55 cm más allá del pie del cono. Toda la piedra es la de la cosecha.]))

#lamina(2, "../detalles/detalle_E2.png", [*E2. El corral techado.* La pirca y el alero, 1:20.],
  columns(2, gutter: 7mm)[La pirca tiene dos caras de 20 cm y, entre ellas, el relleno de piedra menuda que ocupa la mitad del corte. Un palo de queñua de 1,4 m, parado en el eje de la pirca, carga el anillo atado, y el anillo recibe los pares. Sobre los pares van las fajas de _p'ira_ y encima el ichu, con una pendiente de 48°. Entre la piedra y la paja queda una franja de cielo de 90 cm.])

#lamina(3, "../detalles/detalle_E3.png", [*E3. La casa redonda.* Corte por el paso de entrada, de oeste a este, 1:20.],
  columns(2, gutter: 7mm)[Al oeste se ve la pirca de doble cara, con su talud de 5°, y al este el paso, cortado por su eje. El paso mide 96 cm hasta lo alto de la hilada que lo cierra, como pide la regla de la prueba 3, pero las dos mitades de esa hilada se tocan por abajo y al centro quedan 84 cm libres, de modo que se entra de rodillas. La cúpula de champa vuela dieciséis hiladas hasta el óculo, a 3,20 m. El relleno de tierra carga las colas, y las fajas de _p'ira_ se traslapan 15 cm, como tejuelas.])

#lamina(4, "../detalles/detalle_E4.png", [*E4. La chullpa.* La base, la cámara y la boca, 1:20; el aparejo y la cornisa.],
  columns(2, gutter: 7mm)[El corte va de este a oeste por la boca. Abajo, al fondo, están las pilas, cuyas dos últimas hiladas vuelan hacia el paso; encima, la cama de lajas y la hilada de piedra. La cámara de adobitos tiene tres hiladas verticales y cuatro voladas, y la boca de 48 × 42 cm la atraviesa bajo una laja. Aparte van el aparejo de librero en alzado, con 1,5 cm entre adobitos (Agüero Benites et al., 2015: 6), y la cornisa de ichu prensado que describe Squier (1877: 243).])

#lamina(5, "../detalles/detalle_E5.png", [*E5. La casa de la bóveda.* Corte de través por el fogón, 1:20.],
  columns(2, gutter: 7mm)[El bloque no pasa de dos metros. La bóveda de adobe arranca a 35 cm, a la altura del camastro, y cada hilada de 11 cm vuela de 11 a 13 cm hasta dejar una rendija de 43 cm. Las lajas la cierran a 1,86 m, salvo la que falta sobre el fogón, por donde sale el humo. El relleno de tierra llega a 1,70 m, y la pirca sigue hasta los dos metros como un parapeto.])

#lamina(6, "../detalles/detalle_E6.png", [*E6. La _pirwa_.* La V volada con la trampa y, aparte, la _chhaxwa_, 1:20.],
  columns(2, gutter: 7mm)[El corte va a lo largo. Los dos apoyos son una pirca y un montón, y sobre ellos la V de champa vuela 6 cm por hilada hasta cerrarse a 1,79 m. Encima va un piso de palos de queñua de muro a muro, con la trampa bajo un hueco. Aparte, un corte de través por un palo del techo muestra la _chhaxwa_: la piedra hincada bajo el extremo del palo, la soga que los ata y las fajas de _p'ira_ encima.])

// --- la exploración paramétrica: el piloto en E5 (serie P) --------------------------------------------------------
#let figura-p(n, ruta, pie, nota) = block(width: 100%, breakable: false, {
  image(ruta, width: 100%)
  v(1.3mm)
  grid(columns: (6.5mm, 1fr), column-gutter: 1mm,
    text(weight: "bold", size: 7.6pt, "P" + str(n)),
    [#text(size: 6.9pt)[#pie] \ #text(size: 6.9pt, fill: gris)[#nota]])
})

#let lamina-p(n, ruta, pie, dxf, texto) = {
  pagebreak()
  figura-p(n, ruta, pie, [Lámina A3 en DXF, editable en QCAD (#raw("parametrico/" + dxf)). Dibujo hecho con código.])
  v(4mm)
  texto
}

#pagebreak()
#grid(columns: (17mm, 1fr), column-gutter: 5mm,
  titulo-vertical("Exploración paramétrica", "Piloto en E5"),
  [#grid(columns: (1fr, 1fr), column-gutter: 7mm,
     [*Un piloto en E5.* El autor pidió explorar las seis obras de forma paramétrica mientras se dibujan los detalles, y empezar por E5. La bóveda se volvió una función de sus reglas de construcción. Cambian el arranque, el vuelo de la primera hilada y el de la última, y lo demás queda como está. Un guion barre 825 variantes y revisa en cada una si cabe en la casa de la novela: la clave bajo los dos metros, el relleno cargando las colas y una rendija que una laja pueda cerrar.

      *Lo que decide la prueba 3.* Todavía no se sabe cuánto vuela un adobe con la cola cargada, y eso lo mide la prueba 3, así que se probaron tres escenarios. Si vuela 12 cm, cumplen 18 variantes; si vuela un tercio de su largo, 42, y si vuela 15 cm, 120. Por debajo de unos 11 cm ninguna cabe en dos metros. Con un tercio, la mejor es la E5 que ya estaba dibujada, en el borde de la regla de las colas. Con 15 cm, la bóveda puede arrancar a 60 cm, gasta 112 adobes y unos 2 m³ de relleno menos y deja más ancho para sentarse junto a los muros.],
     [#figura-p(5, "../parametrico/e5_nodos.jpg", [*Cuatro bóvedas, un solo grupo de nodos.* Las dos primeras son de hiladas voladas (la E5 actual y la mejor si el adobe vuela 15 cm); las otras dos, de medio punto y rebajada, de dovelas de adobe trabadas. En Blender se mueven los controles del grupo y la bóveda cambia.], [Render de Blender. No es una foto. #raw("parametrico/e5_parametrica.blend").])

      #v(3mm)
      #voz[El guion es #raw("parametrico/boveda_e5.py"), en Python; los nodos los arma #raw("boveda_e5_nodos.py"), y se comprobó que dan las mismas hiladas y la misma clave que el cálculo.]])
   #v(5mm)
   #figura-p(1, "../parametrico/e5_campo.png", [*El campo de las 825 variantes.* Cada celda es una variante: el arranque contra el vuelo de la primera hilada, en cinco paneles según cuánto más vuela la última. El gris dice cuánto tiene que volar el adobe para que la variante se sostenga. En blanco van las que no caben en la casa.], [Los marcos señalan las tres elegidas. Datos en #raw("parametrico/e5_variantes.csv").])])

#lamina-p(2, "../parametrico/e5_matriz.png", [*Veinticuatro variantes, a 1:100.* Cuatro arranques por seis maneras de volar. La línea de trazos marca los dos metros de la novela, y la línea corta, el ancho donde se está de pie.], "e5_matriz.dxf",
  columns(2, gutter: 7mm)[Cuanto menos vuela cada hilada, más hiladas hacen falta y más alta queda la clave. Con 8 o 10 cm la bóveda no cabe en dos metros con ningún arranque. Con 14 a 16 cm cabe incluso arrancando alto, pero pide un vuelo que el adobe quizá no aguante. Entre las dos, la franja que cumple es angosta, y ahí está E5.])

#lamina-p(3, "../parametrico/e5_elegidas.png", [*Las elegidas, según vuele el adobe, a 1:50.* En cada escenario, la que cumple con más ancho para estar sentado.], "e5_elegidas.dxf",
  columns(2, gutter: 7mm)[Si el adobe vuela 12 cm, la mejor vuela 12 cm en todas las hiladas y es casi igual a E5. Si vuela un tercio, la mejor es E5. Si vuela 15 cm, cambia la casa: la bóveda arranca a 60 cm, los muros quedan verticales hasta la altura de un banco y el ancho para sentarse pasa de 2,16 a 2,45 m. En ninguna se está de pie en más de 43 cm: con hiladas voladas y dos metros, se está de pie solo al centro.])

#lamina-p(4, "../parametrico/e5_verdaderas.png", [*Hiladas voladas o bóveda verdadera, a 1:50.* La E5 actual y la mejor bóveda verdadera de cada tipo, de dovelas de canto, con su línea de presiones.], "e5_verdaderas.dxf",
  grid(columns: (1fr, 1fr), column-gutter: 7mm,
    [*La bóveda verdadera.* El autor preguntó si E5 podía tener una bóveda convencional y mandó la foto de un arco de adobe de dovelas, cada adobe con su junta hacia el centro. Una bóveda así empuja hacia los lados, y se sostiene si su línea de presiones, el camino de los empujes, cabe dentro del anillo. El guion probó 258 bóvedas de medio punto, catenarias y rebajadas, con anillos de 10, 20 o 40 cm, y cumplen 145. Con dovelas de canto, de 20 cm, como las de la foto, las elegidas dejan de 0,93 a 1,20 m de ancho de pie, contra 0,43 en E5, y gastan entre 558 y 718 adobes, contra 728.],
    [*Lo que cambia.* E5 dejaría de cerrarse volando hiladas, que es la técnica de la prueba 3 y lo que la ata a la chullpa de Acora. La de medio punto y la rebajada piden cimbra mientras se levantan, y en el altiplano falta la madera. La catenaria podría levantarse sin cimbra, a la manera de las bóvedas nubias, una técnica que todavía no está cotejada en las fuentes del proyecto. La cuenta es plana, con pesos supuestos, y no mide la resistencia del adobe. Una bóveda verdadera pediría su propia prueba, la del arco. Por eso el autor eligió seguir volando hiladas, como en las otras obras.]))

// --- el piloto en las otras cinco: un par de páginas cada una (P6-P15) ------------------------------------------
#let piloto(titulo, texto, nc, campo, pie-campo, nota-campo, nl, lamina, pie-lamina, dxf, texto-lamina) = {
  pagebreak(to: "even", weak: true)
  grid(columns: (17mm, 1fr), column-gutter: 5mm,
    titulo-vertical("Exploración paramétrica", titulo),
    [#columns(2, gutter: 7mm, texto)
     #v(4mm)
     #block(width: 88%, figura-p(nc, campo, pie-campo, nota-campo))])
  lamina-p(nl, lamina, pie-lamina, dxf, columns(2, gutter: 7mm, texto-lamina))
}

#piloto("E1. La montaña",
  [*Las reglas.* Cambian el radio al pie del cono, el radio de la cámara y lo que vuela cada hilada de la cámara, y salen 324 variantes. El talud no puede pasar de 40°, el que supone la prueba 1 para la piedra suelta, y detrás de cada piedra que vuela tienen que quedar sus 40 cm de cola, para que algo la cargue.

   *Lo que encontró.* La montaña dibujada termina en punta justo en el borde del óculo, y sus últimas hiladas no tienen piedra detrás. Con un collar de 40 cm alrededor del óculo, el talud sube a 42°. Además, la cámara vuela 13,5 cm por hilada, un poco más que un tercio del largo de la piedra, así que solo se sostendría si la prueba 3 muestra que la piedra vuela 0,375 de su largo. Si vuela un tercio, la variante que da más piso por metro cúbico de piedra guarda la cámara de 2,8 m, vuela 12 cm y se abre al pie hasta 8,4 m. Pide 51,8 m³ de piedra, unas 118 parcelas despedregadas en lugar de 66.

   *Lo que decide el autor.* Si la montaña crece o la cámara se achica. Con una cámara de 2 m de diámetro que vuele 12 cm, el cono cumple con la piedra de ahora, 28,9 m³, y un pie de 6,8 m.],
  6, "../parametrico/e1_campo.png", [*El campo de E1.* El radio al pie contra el radio de la cámara, con dos maneras de volar. El gris dice cuánta piedra lleva el cono. En blanco quedan las que pasan de 40° (T) o dejan colas sin cargar (C); con V, las que piden que la piedra vuele más de un tercio.], [Datos en #raw("parametrico/e1_variantes.csv"); el guion es #raw("parametrico/montana_e1.py").],
  7, "../parametrico/e1_matriz.png", [*Dieciséis variantes de la montaña, a 1:100.* Todas con el collar y la cámara volando 13,5 cm, como la actual. La línea corta marca el ancho donde se está de pie.], "e1_matriz.dxf",
  [Con el pie de 3,2 m ninguna variante cumple el talud, y con el de 4,4 m cumplen todas. Al crecer la cámara crece también la montaña, porque hacen falta más hiladas para llegar al óculo, y el talud se empina. Una cámara de 3,2 m pide un pie de 4,4 m de radio.

   Las parcelas se cuentan con los 0,44 m³ de piedra que supone el dibujo de la prueba 1. Cuando la prueba diga cuánta piedra da de verdad una parcela, la cuenta cambia en la misma proporción.])

#piloto("E2. El corral",
  [*Las reglas.* Cambian el diámetro del corral, el alto del cono y cuántos pares lo arman, y salen 189 variantes. El techo tiene que tener 45° de pendiente o más, como el de la prueba 4. En el alero, los pares no pueden quedar a más de 70 cm, el ancho de una faja de _p'ira_, porque cada faja se apoya de un par al otro. En el techo que vio Šolc los pares quedan a unos 70 cm, según la cuenta de la prueba 4.

   *Lo que encontró.* Con los dieciséis pares de ahora, el alero de 6,8 m de diámetro los deja a 1,34 m, casi el doble del ancho de una faja, y ninguna variante con dieciséis pares cumple. El corral de 6 m necesita 32. La que gasta menos queñua tiene un cono de 3,1 m, con 45° justos, y lleva 138 m de palos entre pares, postes y anillo, contra 88 ahora. Pide 64 fajas, algo más de tres techos de Enquelga, que llevan 20 cada uno. Con 32 pares, un corral de más de 6 m vuelve a dejar los pares demasiado separados.

   *Lo que decide el autor.* Si duplica los pares o pone correas, palos atados en anillo sobre los pares para que las fajas se apoyen en ellos. Las correas no están en el piloto. Las fuentes del proyecto tampoco dicen si la queñua da pares de 3,3 m.],
  8, "../parametrico/e2_campo.png", [*El campo de E2.* El diámetro del corral contra el alto del cono, con los dieciséis pares de ahora y con 32. El gris dice cuánta queñua llevan los pares, los postes y el anillo. En blanco quedan las que no llegan a 45° (P) o separan los pares más de 70 cm (S).], [Datos en #raw("parametrico/e2_variantes.csv"); el guion es #raw("parametrico/corral_e2.py").],
  9, "../parametrico/e2_matriz.png", [*Dieciséis variantes del corral, a 1:200.* Todas con 32 pares. El techo arranca 90 cm sobre la pirca, como en la lámina 2.], "e2_matriz.dxf",
  [El alto del cono decide la pendiente, y el diámetro del corral decide cuánto se separan los pares. Con el corral de 6 m, el cono tiene que medir al menos 3,1 m para llegar a 45°. En los corrales de 7 y 8 m, aunque sean 32, los pares quedan a 77 y 86 cm.

   La piedra de la pirca no cambia con el techo: son 12,2 m³, unas 28 parcelas de la prueba 1.])

#piloto("E3. La casa redonda",
  [*Las reglas.* Cambian el radio del cuarto, el alto de la pirca y cómo vuela la cúpula, y salen 360 variantes. La pirca tiene que ser al menos tan alta como el paso de 96 cm y la laja que lo cubre. El relleno de tierra tiene que cubrir la cola de cada hilada, y la hilada que más vuela no puede pasar de lo que aguante la champa.

   *Lo que encontró.* El relleno cubre las colas en todas las variantes. La E3 actual vuela hasta 12,7 cm, un poco más que los 12 cm del escenario más prudente, y cumple si la champa vuela un tercio de su largo. Si la prueba 3 muestra que vuela solo 12 cm, alcanza con que las hiladas vuelen de 8 a 12 cm. La cúpula pasa de 16 a 18 hiladas, sube de 3,20 a 3,44 m y gasta unos 80 bloques más. Como se cierra más despacio, el área donde se está de pie crece de 7,9 a 8,7 m². Para que la cúpula baje, volando de 12 a 15 cm, la champa tendría que volar 0,375 de su largo.

   *Lo que decide el autor.* Cuál de las tres maneras de volar, cuando la prueba 3 dé su resultado. Con la pirca de 1,2 m, las tres caben.],
  10, "../parametrico/e3_campo.png", [*El campo de E3.* El radio del cuarto contra el alto de la pirca, con la manera de volar actual y la más prudente. El gris dice cuánta área queda de pie. En blanco, las pircas más bajas que el paso y su laja (K).], [Datos en #raw("parametrico/e3_variantes.csv"); el guion es #raw("parametrico/cupula_e3.py"), y la cúpula sale de la misma cuenta que la lámina 3.],
  11, "../parametrico/e3_matriz.png", [*Doce variantes de la casa redonda, a 1:100.* Cuatro cuartos por tres maneras de volar, con la pirca de 1,2 m. La línea corta marca el ancho donde se está de pie.], "e3_matriz.dxf",
  [Cuanto menos vuela cada hilada, más hiladas hacen falta y más alta queda la cúpula, pero más espacio queda para estar de pie. El relleno crece con el cuarto: el de 5,6 m de diámetro lleva 29 m³ de tierra, más del doble que el de 4 m.

   Los bloques se cuentan de 40 × 25 × 12 cm, puestos a tizón, con el largo hacia adentro, y sin descontar el paso ni el _t'uju_.])

#piloto("E4. La chullpa",
  [*Las reglas.* Cambian lo que vuela cada hilada de la cámara, lo que se retira cada hilada de la pirámide y la pieza que forra la cámara, y salen 140 variantes. La pieza vuela lo que aguante con la cola cargada, y su cola tiene que caber en el relleno. Sobre la laja que cierra la cámara tiene que quedar una hilada. Ningún adobito de la cara puede apoyarse en menos de la mitad de su fondo, así que cada hilada se retira 7 cm como mucho, una decisión del proyecto.

   *Lo que encontró.* La cámara dibujada vuela 10 cm por hilada con adobitos de 14 cm de fondo, con casi tres cuartos de cada pieza en el aire. No se sostiene en ningún escenario, porque un adobito así vuela de 4,2 a 5,25 cm. Para cumplir, la cámara tiene que volar 4 cm por hilada. Entonces necesita nueve hiladas voladas en lugar de cuatro, sube de 1,47 a 2,52 m y queda alta y angosta, con 1,39 m³. Si el forro se hace con adobes de 40 cm, los de E5, la cámara de ahora cumple en los tres escenarios. El retiro de 6,2 cm cumple.

   *Lo que decide el autor.* Si la cámara se forra de adobes grandes o se vuelve alta y angosta. Una tercera salida, cerrarla con lajas largas, no está en el piloto.],
  12, "../parametrico/e4_campo.png", [*El campo de E4.* El vuelo de la cámara contra el retiro de la pirámide, con el forro de adobitos de pie y con adobes de 40 cm. El gris dice el volumen de la cámara. En blanco quedan las que no cierran a tiempo (T), dejan la cola fuera del relleno (C) o se retiran más de 7 cm (R); con V, las que piden que la pieza vuele más de un tercio.], [Datos en #raw("parametrico/e4_variantes.csv"); el guion es #raw("parametrico/chullpa_e4.py").],
  13, "../parametrico/e4_matriz.png", [*Quince variantes de la chullpa, a 1:100.* Todas con el forro de adobitos de pie, sin la cornisa ni la boca.], "e4_matriz.dxf",
  [Solo la fila de arriba, que vuela 4 cm, cumple, salvo donde la pirámide se retira 8 cm. Las cámaras que vuelan 7 y 10 cm se ven más holgadas, pero sus adobitos vuelan la mitad de su fondo o más.

   El retiro no cambia la cámara, pero sí la cima: con 4,4 cm de retiro queda de 1,77 m de lado, y con 8 cm, de 0,76 m.])

#piloto("E6. La pirwa",
  [*Las reglas.* Cambian lo que vuela cada hilada de la V y el alto del depósito, y salen 100 variantes. Bajo la trampa hay que estar de pie, así que la clave queda a 1,70 m o más, el alto que se usa en E5. El lado alto no pasa de 4,6 m, el que el autor aceptó al bajar la _pirwa_ un metro, hasta que se pruebe uno mayor.

   *Lo que encontró.* Cumplen 18. Si la V vuela 7 cm o más, se cierra antes y la clave baja de 1,70 m. Si vuela menos, la clave sube y le quita alto a lo guardado. La E6 actual, que vuela 6 cm, es la que más guarda: 5,75 m³ sobre el piso, con 535 bloques de champa. Su vuelo es el 15 % del largo del bloque, muy por debajo del tercio, así que la V no depende de la prueba 3.

   *Lo que decide el autor.* Nada por ahora: la E6 actual queda como está. Falta probar si un depósito de champa de más de 4,6 m aguanta lleno, y esa prueba todavía no está en el proyecto.],
  14, "../parametrico/e6_campo.png", [*El campo de E6.* El vuelo de la V contra el alto del lado alto. El gris dice cuánto se guarda. En blanco quedan las que bajan la clave de 1,70 m (P) o pasan de 4,6 m (E).], [Datos en #raw("parametrico/e6_variantes.csv"); el guion es #raw("parametrico/pirwa_e6.py").],
  15, "../parametrico/e6_matriz.png", [*Doce variantes de la _pirwa_, a 1:100.* Cortadas por el eje largo, donde el muro mide el promedio de sus dos lados. La V se ve en el muro largo, al fondo.], "e6_matriz.dxf",
  [Las columnas de 8 y 10 cm cierran la V más rápido y guardan más, pero dejan la clave a 1,55 y 1,43 m. La de 4 cm la sube a 2,27 m y guarda 1,3 m³ menos. La fila de abajo pasa del alto que aceptó el autor.

   Lo guardado se mide sobre el piso de palos, hasta 10 cm bajo el techo, en la planta interior de 2,5 × 1,1 m.])

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

   En las exploraciones, las fajas van bajo el ichu del corral (E2), cubren la casa redonda (E3), traslapadas como tejuelas, y el techo de la _pirwa_ (E6).],
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
     voz[Diagramas en masas. Las medidas son del proyecto y se ajustaron al recomponer.])])

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
