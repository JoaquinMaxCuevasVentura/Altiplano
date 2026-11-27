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

// --- cubierta -------------------------------------------------------------------------------------------------
#page(fill: gris-pagina, footer: none, margin: (top: 18mm, bottom: 18mm, inside: 20mm, outside: 16mm))[
  #text(size: 9pt, weight: "semibold", tracking: 0.08em)[JOAQUIN MAX CUEVAS VENTURA]
  #v(1fr)
  #text(size: 78pt, weight: "black", tracking: -0.035em, style: "italic")[Chhaxwa]
  #v(2mm)
  #text(size: 19pt, weight: "medium", tracking: -0.01em)[Cinco pruebas de construcción \ a partir de _Altiplano_]
  #v(9mm)
  #grid(columns: (1fr, 1fr), column-gutter: 8mm,
    text(size: 8.4pt)[Piedra, tierra y paja del altiplano. Un proyecto de arquitectura a partir de la novela de Raúl Botelho Gosálvez (1945).],
    voz[Noviembre de 2026. Planteado y modelado; ninguna maqueta construida todavía.])
]

// --- entrada gris ---------------------------------------------------------------------------------------------
#page(fill: gris-pagina)[
  #grid(columns: (1fr, 1fr), column-gutter: 7mm,
  [
    #text(weight: "bold")[_Chhaxwa_. Cinco pruebas de construcción a partir de _Altiplano_]

    En el vocabulario aymara que Ludovico Bertonio publicó en 1612, _chhaxwa_ nombra dos piedras. Una es la de los montones que se hacen al limpiar la chacra, las piedras «que amontonan limpiando las chácaras». La otra es la piedra «hincada en la pared para atar en ella los palos del techo» (Bertonio, 2011 [1612]: 330). Este proyecto va de una a otra. Empieza en un terreno que se despiedra y termina bajo el techo de una casa.

    Es una serie de pruebas de construcción con piedra, tierra y paja del altiplano. Cada una parte de un pasaje de la novela _Altiplano_ y de una técnica andina descrita en una fuente, y busca la forma que esa técnica permite. Se quiere explorar técnicas y materiales del altiplano y, con ellos, formas poéticas en arquitectura.

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

// --- las cinco pruebas: índice ----------------------------------------------------------------------------------
#let fila-indice(n, t, pas, tec, esc) = (text(weight: "bold", n), text(weight: "bold", t), pas, tec, esc)
#grid(columns: (8mm, 30mm, 1fr, 46mm, 22mm), column-gutter: 3mm, row-gutter: 3.2mm,
  rotulo[N.º], rotulo[Prueba], rotulo[Pasaje], rotulo[Técnica], rotulo[Escala],
  ..fila-indice("1", "La cosecha", voz[La «cosecha de piedras» (p. 9) y el «informe montón» de la mina (p. 154)], [Despedregar y amontonar], [Natural]),
  ..fila-indice("2", "El relleno", voz[Las pircas «compuestas» al volver (p. 156) y la «piedrecilla menuda» (p. 8)], [La pirca de doble cara], [1:5]),
  ..fila-indice("3", "El dintel", voz[«En el dintel de Jatun-Kolla» se arrodillan (p. 155)], [El arco por aproximación de hiladas], [Natural]),
  ..fila-indice("4", [La _p'ira_], voz[El «techo de paja plomiza» (p. 10) y los techos «desfondados» (p. 79)], [La _p'ira_ y la armadura atada], [Natural]),
  ..fila-indice("5", "El fogón", voz[Las _chujllas_ «rectangulares y chatas» (p. 30) y Paulo en cuclillas junto al fuego (p. 32)], [La casa de Enquelga y el _t'uju_], [1:10]),
)
#v(8mm)
#grid(columns: (1fr, 1fr), column-gutter: 7mm,
  [Las pruebas se encadenan. La piedra menuda que separa la prueba 1 es el relleno de la 2. La _p'ira_ de la 4 cubre los montones de la 1 y la maqueta de la 5. Se propone empezar por la 2, que pone a prueba una frase del artículo, y seguir con la 4 y la 5, que comparten el techo.

  Cada prueba explora también formas. Las cinco referencias que reunió el autor se leen como cinco operaciones (la masa sobre lo liviano, la masa ahuecada, el montón como apoyo, la proporción y las capas, el óculo y el pozo), y de ellas salen tres formas por prueba, quince en total, modeladas como maquetas de estudio.],
  voz[Las páginas de la novela son de su séptima edición (Botelho Gosálvez, 1982 [1945]). Las medidas que vienen de una fuente llevan autor y página; las que salen de una cuenta dicen cómo se hizo; las demás son decisiones del proyecto, que se comprueban o se cambian al construir. Los renders muestran lo que se espera que salga. Cuando exista la maqueta, su foto se pondrá al lado.])

// --- una prueba: dos páginas -------------------------------------------------------------------------------------
#let prueba(n, titulo, texto, pasaje, mide, filas, grande, chicas) = {
  pagebreak(to: "even", weak: true)
  grid(columns: (17mm, 1fr, 1fr), column-gutter: 5mm,
    titulo-vertical(titulo, "Prueba " + n),
    texto,
    [#voz(pasaje)
     #v(4mm)
     #rotulo[Qué se mide]
     #v(1mm)
     #set par(spacing: 0.6em)
     #for m in mide [#grid(columns: (3mm, 1fr), [·], m)]])
  place(bottom + left, dy: 0mm, block(width: 100%, ficha(filas)))
  pagebreak()
  grid(columns: (118mm, 1fr), column-gutter: 7mm,
    render(grande.at(0), grande.at(1), grande.at(2)),
    stack(spacing: 6mm, ..chicas.map(c => render(c.at(0), c.at(1), c.at(2), ancho: 56mm))))
}

#prueba("1", "La cosecha",
  [*Despedregar y amontonar.* El aymara tiene un verbo para la faena, _wanqathapiña_, «amontonar piedras sacándolas» (Bertonio, 2011 [1612]: 77), y un nombre, _chhaxwa_, para las dos piedras del título (ibid.: 330). Las fuentes no dicen cómo se hace un montón en el campo, y la novela tampoco. La prueba mide la faena.

   *La regla.* La obra se levanta solo con la piedra que sale de despedregar el terreno donde se levanta. Su altura no se dibuja antes: la da la cosecha.

   #pasos((
     [Marcar una parcela de 2 × 2 m, en dieciséis cuadros de 50 cm.],
     [Despedregar hasta 20 cm y separar la piedra en grande, mediana y menuda. Pesarla.],
     [Levantar cuatro montones con toda la piedra y nada más. Medir el talud.],
     [Hincar una piedra larga en cada montón, atar dos palos y tender dos fajas de _p'ira_.],
   ))],
  [«A medida que extraen piedras y las amontonan, brotan más y más, como paridas por la tierra» (p. 9). Al final, a Condori lo cubre «un informe montón de rocas, lodo y maderos astillados» (p. 154).],
  ([El peso de cada clase de piedra en cada cuadro.], [El volumen, el talud y la altura de cada montón.], [Las horas y las manos.], [Cuántas parcelas harían falta para que el montón alcance al cerro.]),
  (([prueba], [1]), ([técnica], [despedregar y amontonar]), ([escala], [tamaño natural]), ([parcela], [2 × 2 m, proyecto]), ([fajas], [2,5 × 0,7 m, Šolc (2011 [1975]: 105)]), ([fuentes], [Bertonio (2011 [1612]: 77, 330)])),
  (1, "../renders/render_forma_1B.jpg", [*La montaña de piedras.* Toda la cosecha en un cono de piedra seca de 6 m de diámetro y 4 m de alto, hueco, con una boca baja y un óculo. Maqueta 1:20.]),
  ((2, "../renders/render_forma_1A.jpg", [*Cuatro montones y un techo.* La piedra de una parcela sostiene dos fajas de _p'ira_. 1:10.]),
   (3, "../renders/render_forma_1C.jpg", [*El montón habitado.* Piedra suelta sobre una caja de queñua; se entra en cuclillas. 1:20.]))
)

#prueba("2", "El relleno",
  [*La pirca de doble cara.* Dos caras de piedra grande y un relleno de piedra menuda, para la que Bertonio tenía nombre: «Piedra para entremeter en los edificios y llenar sus huecos. Ch'äta, chillpa, k'ak'i qala» (Bertonio, 2011 [1612]: 246).

   *Lo que pone a prueba.* El artículo dice: «Una pirca de doble cara enseña lo que esa memoria olvida. Las piedras grandes dan la cara, pero adentro van las menudas, y sin ese relleno el muro se cae». La prueba lo comprueba con piedra.

   *La regla.* El relleno ocupa la mitad del corte. Tres variantes a 1:5: con piedra menuda, con tierra apisonada y sin relleno.

   #pasos((
     [Asentar la primera hilada de las dos caras.],
     [Subir las caras y llenar el centro al mismo tiempo.],
     [Cerrar arriba con piedras planas.],
     [Sacar el relleno por una boca al pie, de a poco, hasta que el muro caiga.],
   ))],
  [«Las chujllas fueron reparadas del estrago, las pircas de piedra que separan las parcelas fueron compuestas» (p. 156). En la sequía, «las pircas se derrumbaban igual que murallas milenarias» (p. 72).],
  ([El relleno sacado a la primera grieta y a la caída.], [El desplome de cada cara.], [La forma del derrumbe.], [Si las caras sin relleno se sostienen.]),
  (([prueba], [2]), ([técnica], [pirca de doble cara]), ([escala], [1:5]), ([muro], [2,0 × 1,2 × 0,6 m, proyecto]), ([relleno], [la mitad del corte]), ([fuentes], [Bertonio (2011 [1612]: 246)])),
  (4, "../renders/render_forma_2B.jpg", [*Pilares de mitad y mitad.* Capas alternas de piedra y de tierra apisonada cargan un techo pesado de ichu. Lo que en la pirca se esconde aquí es fachada. 1:20.]),
  ((5, "../renders/render_forma_2A.jpg", [*El tramo de prueba.* Las tres variantes, una junto a otra. 1:5.]),
   (6, "../renders/render_forma_2C.jpg", [*El corral cortado.* Un tercio menos; el corte muestra el relleno. 1:20.]))
)

#prueba("3", "El dintel",
  [*El arco por aproximación de hiladas.* Squier lo vio en los puentes de champa camino a Copacabana: cada capa vuela sobre la de abajo «until the upper ones touch and brace against each other, forming a rude kind of arch» (Squier, 1877: 313). La champa se deja secar unos veinte días (Vitulas-Quille y Reynoso-Machaca, 2025: 9).

   *La regla.* La altura del paso sale de cuánto vuela cada hilada. Con jambas de 60 cm y abertura de 60 cm, si cada hilada vuela 5 cm el paso mide 1,32 m; si vuela 10 cm, 0,96 m; si vuela 15 cm, 0,84 m. El cuerpo dice después si obliga a arrodillarse.

   #pasos((
     [Dos jambas de champa separadas 60 cm.],
     [Cada hilada vuela hacia el centro, con la cola apretada.],
     [Las de arriba se tocan y se apuntalan.],
     [Cargar tierra y piedra encima, y pasar.],
   ))],
  [«En el dintel de Jatun-Kolla se detenían para ponerse de rodillas y besar el suelo que habían abandonado en el terror de la mala época» (p. 155).],
  ([El vuelo máximo de champa, adobe y laja.], [Las hiladas y el alto del paso.], [Quién cruza y cómo: de pie, agachado o de rodillas.]),
  (([prueba], [3]), ([técnica], [hiladas voladas]), ([escala], [tamaño natural]), ([abertura], [60 cm, proyecto]), ([bloque], [40 × 25 × 12 cm, proyecto]), ([fuentes], [Squier (1877: 313)])),
  (7, "../renders/render_forma_3B.jpg", [*La celda volada.* Planta cuadrada de champa, muro inclinado por fuera e hiladas voladas por dentro hasta un óculo, como un putuco. 1:20.]),
  ((8, "../renders/render_forma_3A.jpg", [*El paso.* La abertura de 96 cm que sale de volar 10 cm. 1:10.]),
   (9, "../renders/render_forma_3C.jpg", [*El umbral hundido.* Se entra bajando por una zanja. 1:20.]))
)

#prueba("4", [La _p'ira_],
  [*Un techo que se hace en el suelo.* En Enquelga, el constructor mide con una soga el tamaño del techo, echa encima paja suelta, «cruzada, en varias direcciones», la pisa y la cubre de barro. Los ayudantes pisotean el barro con sus costales, «dejando sobre el barro el dibujo de la estructura de los sacos». Después la cortan en veinte fajas de unos 2,5 × 0,7 m, que se suben a una armadura de pares atados y «se mantienen por su peso propio» (Šolc, 2011 [1975]: 102-107).

   *La regla.* El techo se dibuja primero en el suelo, a tamaño real. Se pisa, queda la huella del tejido, se corta y se sube.

   #pasos((
     [Barrer y marcar con soga una faja de 2,5 × 0,7 m.],
     [Echar la paja cruzada y pisarla.],
     [Extender el barro y pisotearlo con costal, aguayo o el pie.],
     [Cortar la faja y subirla a dos pares de cabrios.],
   ))],
  [«Cada una de las casas [...] tienen en el techo de paja plomiza por el humo que sale de los fogones y por la excesiva sequedad, un crucifijo de palo» (p. 10). Sin gente, los techos quedan «desfondados» (p. 79).],
  ([La paja y el barro por metro cuadrado.], [El peso húmedo y seco.], [La huella de cada tejido, con luz rasante.], [De qué lado queda la huella en el techo.]),
  (([prueba], [4]), ([técnica], [_p'ira_ y armadura atada]), ([escala], [tamaño natural]), ([faja], [2,5 × 0,7 m]), ([techo entero], [unos 7 × 5 m, cálculo]), ([fuentes], [Šolc (2011 [1975]: 102-109)])),
  (10, "../renders/render_forma_4C.jpg", [*El pajar levantado.* Un techo de ichu en capas que sobresalen, sobre doce palos de 1,2 m y un piso excavado: el techo es todo el edificio. 1:20.]),
  ((11, "../renders/render_forma_4A.jpg", [*La faja sobre los pares* y tres muestras de huella. 1:5.]),
   (12, "../renders/render_forma_4B.jpg", [*El techo a medio subir.* Diez fajas arriba y diez en el suelo. 1:20.]))
)

#prueba("5", "El fogón",
  [*La casa de Enquelga y el* _t'uju_. La planta sale de la tabla de Šolc: la mediana de 17 dormitorios de adobe con techo a dos aguas es de 5,75 × 3,30 m (Šolc, 2011 [1975]: 93-94). Muros de 2 m, como en la novela, de 40 cm abajo y 35 arriba, sobre un cimiento de piedra (ibid.: 102). La puerta mira al este (Suárez Jordán, 1990: 130). El _t'uju_ es un «orificio pequeño» al noreste por donde entra el sol y sale el humo (Yampara Blanco, 2019: 13).

   *La regla.* La casa se mide desde el cuerpo en cuclillas. Dos aberturas: entra la luz de la mañana y sale el humo.

   *El sol.* El 21 de junio, en La Paz, el sol pasa por el noreste hacia las 10, a 35° de altura; el 21 de diciembre no pasa nunca. Un agujero de 15 cm en un muro de 40 cm solo deja pasar el sol a menos de unos 20° de su eje. La dirección del _t'uju_ elige la fecha y la hora.],
  [«Las chujllas no tienen cuartos ni mucho menos. Rectangulares y chatas, apenas se alzan dos metros del suelo» (p. 30). «En cuclillas, cerca del fuego, tenía la mirada en la sombra del suelo donde a veces resbalaba la cinta bermeja del resplandor del fogón» (p. 32).],
  ([La mancha de sol en cada fecha y hora.], [Por dónde sale el humo.], [Qué se ve desde las cuclillas, con la cámara a 9 cm del piso.]),
  (([prueba], [5]), ([técnica], [la casa de Enquelga]), ([escala], [1:10]), ([planta], [5,75 × 3,30 m, cálculo]), ([_t'uju_], [15 × 15 cm, proyecto]), ([fuentes], [Šolc; Yampara Blanco; Suárez Jordán])),
  (13, "../renders/render_forma_5C.jpg", [*El cono del fogón.* Un fogón hundido bajo un cono de ichu sobre ocho palos. El _t'uju_ es un tubo de barro apuntado al sol del 21 de junio a las 10; el humo sale por arriba. 1:20.]),
  ((14, "../renders/render_forma_5A.jpg", [*La chujlla de Enquelga.* La maqueta de la prueba. 1:10.]),
   (15, "../renders/render_forma_5B.jpg", [*La casa partida.* Un bloque de tierra ahuecado a la medida de las cuclillas. 1:20.]))
)

// --- la exploración formal ----------------------------------------------------------------------------------------
#pagebreak(to: "even", weak: true)
#grid(columns: (17mm, 1fr, 1fr), column-gutter: 5mm,
  titulo-vertical("Cinco operaciones", "Exploración formal"),
  [Las cinco referencias del autor se leen como operaciones, y cada operación se ata a una técnica o a un dato del altiplano, para que la forma no venga de fuera.

   *La masa sobre lo liviano.* Lo pesado arriba y lo delgado abajo. Las fajas de _p'ira_ «se mantienen por su peso propio» sobre palos atados (Šolc, 2011 [1975]: 107), y Squier vio casas de champa como «tall quadrilateral hay-stacks» (Squier, 1877: 391).

   *La masa ahuecada.* Un volumen macizo al que se le quita un hueco a la medida del cuerpo, como la _amaya uta_, «sepultura como casa sobre la tierra» (Bertonio, 2011 [1612]: 276).

   *El montón como apoyo.* La piedra suelta carga lo que está encima.

   *La proporción y las capas.* Mitad piedra y mitad tierra, o un cuarto y tres cuartos, que en el corte se ven como capas.

   *El óculo y el pozo.* Una abertura arriba y un suelo que baja. El _t'uju_ es «salida del humo como una chimenea» (Yampara Blanco, 2019: 13), y bajar a un pozo obliga a agacharse.],
  voz[Las referencias: dos maquetas de #raw("studio_cifuentes_ethz") (2026), un bloque de tierra con bóveda sobre pilas de piedra seca y una arcada sobre pilares de capas; una pirámide truncada de terciado sobre una plataforma de listones; un cono sobre palos encima de un pozo, y una piedra de granito partida y forrada de madera, que parece ser de Smiljan Radić y Marcela Correa: en _Obra gruesa_ cuentan que cortaron «a mitad el granito de 19 toneladas» para _El Niño Escondido en un Pez_ (Radić, 2017: 230-231). Las imágenes no se reproducen: son obra de terceros.])

// --- el prototipo en el paisaje ---------------------------------------------------------------------------------------
#pagebreak()
#block(width: 100%, {
  image("../renders/render_prototipo_pirca_paisaje.jpg", width: 100%)
  v(1.3mm)
  grid(columns: (6.5mm, 1fr), column-gutter: 1mm, text(weight: "bold", size: 7.6pt, "16"),
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
  voz[Las fórmulas son las de la NOAA y están en #raw("blender/comun.py"). En Blender, el giro del sol del cielo físico coincide con el acimut de esta tabla si el eje y apunta al norte; se comprobó con un render de prueba.])

// --- fuentes y colofón ---------------------------------------------------------------------------------------------------
#pagebreak(to: "even", weak: true)
#grid(columns: (1fr, 1fr), column-gutter: 7mm,
  [#rotulo[Fuentes]
   #v(1mm)
   #set par(spacing: 0.75em)
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

   Los renders los calcula Blender 5.0.1 a partir de geometría, materiales y luz escritos en código (#raw("chhaxwa/blender/")). Son predicciones de cómo quedarían las maquetas y no fotos. Cuando se construyan, sus fotos irán al lado.

   Claude (Anthropic), un asistente de IA generativa, redactó los textos con las indicaciones del autor, cotejó las fuentes, calculó las medidas y la tabla del sol y escribió el código de los modelos y de este documento. Ninguna imagen viene de un generador de imágenes.

   El diseño toma rasgos del de _Obra gruesa_: la grotesca pequeña, los números de página grandes, los títulos verticales, las fichas negras y una segunda voz en gris, que allá es el inglés y aquí es la novela. Compuesto en Typst con la letra Inter.

   #voz[Noviembre de 2026.]])
