// El espécimen de Contenida. Se compila con armar.py (que prepara .cache/) y la raíz en tipografia/.
//
// Un espécimen muestra una letra. Esta todavía no existe: la hacen las manos, placa por placa, desde el pie
// de la lámina (04, acciones 3 y 4). Por eso este espécimen no compone texto con ella. Muestra lo que hay:
// la caja y sus 56 celdas, las letras halladas en el pie, la celda y sus líneas, los estados en lugar de los
// pesos, la regla de componer con placas y, rotulado, lo que propuso la máquina.
//
// La página tiene la proporción de la celda: 180 × 200 mm (0,90). La retícula es la caja: 8 columnas × 7 filas
// de celdas de 18 × 20 mm, con juntas de 3 mm. Todo marco se abre abajo, en su desagüe.

#let D = json("/especimen/.cache/datos.json")
#let R = json("/esquemas/celda_medida.json")
#let P = json("/esquemas/razon_medida.json")
#let M = D.medidas

#let papel = rgb("#f6f4ee")
#let tinta = rgb("#1d1c1a")
#let violeta = rgb("#4a2470")
#let lila = rgb("#b9a6d6")
#let grafito = rgb("#55534e")
#let gris = rgb("#6d6a63")
#let gris2 = rgb("#9a968d")
#let filete = rgb("#cfcac0")
#let serif = "Newsreader 16pt 16pt"
#let mono = "Courier Prime"

// ---------------------------------------------------------------- la retícula
#let COL = 18mm
#let FIL = 20mm
#let J = 3mm
#let x(c) = (c - 1) * (COL + J)
#let y(f) = (f - 1) * (FIL + J)
#let an(k) = k * (COL + J) - J
#let al(k) = k * (FIL + J) - J
#let total = 16

#let coma(v, d: 1) = {
  let s = str(calc.round(v, digits: d))
  if not s.contains(".") and d > 0 { s = s + "." + "0" * d }
  let partes = s.split(".")
  if partes.len() == 2 and partes.at(1).len() < d { s = s + "0" * (d - partes.at(1).len()) }
  s.replace(".", ",")
}

// ---------------------------------------------------------------- trazos
#let fino(c: tinta, w: 0.4pt) = (paint: c, thickness: w)
#let punteado(c: violeta, w: 0.7pt) = (paint: c, thickness: w, dash: (array: (0pt, 1.6pt), phase: 0pt), cap: "round")
#let rayado(c: gris2, w: 0.4pt) = (paint: c, thickness: w, dash: (array: (1.6pt, 1.2pt), phase: 0pt))

// un marco que se abre abajo, en su punto más bajo: el desagüe
#let marco(px, py, w, h, s, hueco: 2mm) = place(top + left, curve(
  stroke: s,
  curve.move((px + w / 2 - hueco / 2, py + h)),
  curve.line((px, py + h)),
  curve.line((px, py)),
  curve.line((px + w, py)),
  curve.line((px + w, py + h)),
  curve.line((px + w / 2 + hueco / 2, py + h)),
))

#let en(c, f, cuerpo, k: 1, dx: 0mm, dy: 0mm) = place(top + left, dx: x(c) + dx, dy: y(f) + dy, block(width: an(k), cuerpo))
#let linea(a, b, s) = place(top + left, line(start: a, end: b, stroke: s))

// ---------------------------------------------------------------- la letra de la página
#set text(font: serif, size: 8.6pt, lang: "es", fill: tinta, weight: 400, hyphenate: true)
#set par(leading: 0.62em, justify: false, spacing: 0.95em)
#show raw: set text(font: "Courier Prime", size: 1.04em)

#let m(cuerpo, t: 6.2pt, c: tinta, peso: 400) = text(font: mono, size: t, fill: c, weight: peso, tracking: 0.02em, cuerpo)
#let rotulo(cuerpo, c: gris) = m(upper(cuerpo), t: 5.8pt, c: c)
#let titulo(cuerpo) = text(font: serif, size: 22pt, weight: 300, cuerpo)
#let bajada(cuerpo) = text(font: serif, size: 11pt, weight: 300, style: "italic", fill: grafito, cuerpo)

// la etiqueta del estado de cada imagen, como en el libro: lo de la máquina, punteado
#let etiqueta(e) = {
  let (txt, s, c) = if e == "maquina" { ("propuesta de la máquina", punteado(w: 0.5pt), violeta) }
    else if e == "hallada" { ("hallada en la lámina", fino(w: 0.4pt), tinta) }
    else if e == "mano" { ("por hacer: la mano", punteado(c: gris, w: 0.5pt), gris) }
    else { ("propia", none, gris) }
  box(stroke: s, inset: (x: 1.2mm, y: 0.6mm), m(txt, t: 5.4pt, c: c))
}

// ---------------------------------------------------------------- la hoja: cabeza, folio y retícula
#let cabeza(seccion) = {
  place(top + left, dx: 7.5mm, dy: 7.6mm, rotulo("Contenida · espécimen", c: tinta))
  place(top + left, dx: 7.5mm + x(4), dy: 7.6mm, rotulo(seccion, c: tinta))
  place(top + right, dx: -7.5mm, dy: 7.6mm, context {
    let n = counter(page).get().first()
    rotulo([#(if n < 10 { "0" } else { "" })#n / #total], c: tinta)
  })
  place(top + left, dx: 7.5mm, dy: 10.6mm, line(length: 165mm, stroke: fino(w: 0.5pt)))
  // abajo, la celda de la página: se abre en su desagüe
  place(bottom + left, dx: 7.5mm, dy: -11mm, rotulo("una letra que se hace a mano · noviembre de 2026"))
}
#let reticula() = for c in range(1, 9) { for f in range(1, 8) {
  place(top + left, dx: x(c), dy: y(f), rect(width: COL, height: FIL, stroke: (paint: filete, thickness: 0.2pt)))
} }

#let hoja(seccion, cuerpo, ver_reticula: false) = page(
  width: 180mm, height: 200mm, fill: papel,
  margin: (left: 7.5mm, right: 7.5mm, top: 16mm, bottom: 26mm),
  background: cabeza(seccion),
  { if ver_reticula { reticula() }; cuerpo },
)

#set document(title: "Contenida: espécimen", author: "Joaquin Max Cuevas Ventura",
  keywords: ("Contenida", "tipografía", "espécimen", "repujado", "Contener una ruina"))

// ================================================================= 1 · portada
#hoja("portada", {
  en(1, 1, k: 6, [
    #text(font: serif, size: 52pt, weight: 300, tracking: -0.01em)[contenida]
    #v(-3mm)
    #bajada[espécimen de una letra que todavía no existe]
  ])
  // la caja de 8 × 7, vacía: la letra no está; está su caja
  let h = 13.6mm
  let w = h * 0.9
  let j = 1.7mm
  let ox = 0mm
  let oy = y(3) - 6mm
  for c in D.caja {
    let px = ox + (c.columna - 1) * (w + j)
    let py = oy + (c.fila - 1) * (h + j)
    let s = if c.estado == "hallada" { fino(w: 0.45pt) } else if c.estado == "reconstruida" { punteado(w: 0.6pt) } else { punteado(c: gris, w: 0.6pt) }
    marco(px, py, w, h, s, hueco: 1.6mm)
    place(top + left, dx: px + 0.8mm, dy: py + 0.7mm, m(str(c.celda), t: 4.6pt, c: if c.estado == "hallada" { gris } else { violeta }))
    if c.celda == 1 {
      place(top + left, dx: px + w / 2 - h * c.ancho / 2 * 0.9, dy: py + h * 0.05, image(c.testigo, height: h * 0.9))
    }
  }
  let cx = ox + 8 * (w + j) + 4mm
  place(top + left, dx: cx, dy: oy, block(width: 165mm - cx, [
    #set par(leading: 0.55em)
    #text(size: 9.5pt)[*56 celdas.* 30 signos hallados en el pie de la lámina, 25 reconstruidos y uno que se hace con los dedos.]

    #text(size: 9.5pt)[*Ninguna letra.* Las letras de la caja las hacen las manos, placa por placa, desde el pie. Este espécimen muestra lo que ya hay: la caja, las letras halladas, la celda y sus líneas, los estados y la regla de componer.]

    #v(2mm)
    #grid(columns: (8mm, 1fr), row-gutter: 2.2mm, column-gutter: 2mm,
      box(width: 7mm, height: 0pt, line(length: 7mm, stroke: fino(w: 0.45pt))), m[hallado],
      box(width: 7mm, height: 0pt, line(length: 7mm, stroke: punteado(w: 0.6pt))), m(c: violeta)[reconstruido],
      box(width: 7mm, height: 0pt, line(length: 7mm, stroke: punteado(c: gris, w: 0.6pt))), m(c: gris)[con los dedos],
    )
    #v(2mm)
    #m(c: gris)[en la celda 1, la coma de «KOCHAMAMA,»: el primer signo hallado]
  ]))
})

// ================================================================= 2 · qué es
#hoja("qué es", {
  en(1, 1, k: 5, [
    #titulo[una letra que contiene]
    #v(3mm)
    *Contenida* es la tipografía de _Contener una ruina: acciones para desenterrar una voz_, de Rebeca Paz Prada con CreaciónxAcuerpamiento (La Paz, 22 de agosto de 2026). En la obra, la cinta tapó los ojos y la boca de una ídolo dibujada según Posnansky, en el fondo de una piscina vacía. La letra sale de lo único que la lámina dice: su pie.

    *Del pie, las medidas; de la obra, la forma.* Las letras se calcan del pie, se repujan en papel de aluminio de cocina y siguen por los estados de la obra: la cinta, el frotado, el agua, la voz. Ninguna placa es igual a otra: dentro de un verso, ninguna se repite.

    *No hay Regular.* No es una familia de pesos ni una fuente variable: cada estilo es un estado de la letra en la cadena de la obra, y el peso se mide en frotadas.

    *Una letra, una celda.* La de la cabeza de la ídolo: 8 columnas por 7 filas de celdas de 0,90 de ancho por alto, la caja. Monoespaciada y solo caja baja: la letra de la mano, no la del monumento.
  ])
  en(6, 1, k: 3, [
    #rotulo("lo que hay", c: tinta)
    #line(length: 100%, stroke: fino(w: 0.5pt))
    #set text(size: 7.6pt)
    #set par(leading: 0.5em)
    #grid(columns: (1fr), row-gutter: 2.4mm,
      [*El pie de la lámina:* 336 letras recortadas de una foto, sin la foto.],
      [*La caja:* 56 celdas, en el orden en que los signos aparecen en el pie.],
      [*La gramática:* la anatomía base, en vectores. Es la propuesta de la máquina.],
      [*Los planos:* doce láminas A3 con el porqué de cada decisión.],
      [*La simulación:* los seis estados, hechos por código para confrontarlos con la mano.],
    )
    #v(5mm)
    #rotulo("lo que no hay", c: violeta)
    #line(length: 100%, stroke: punteado(w: 0.6pt))
    #grid(columns: (1fr), row-gutter: 2.4mm,
      [*La letra.* Las 119 placas de la mano, por hacer.],
      [*La fuente digital.* Si cierra, se escanea de las placas (05).],
      [*El nombre acordado.* _Contenida_ es el de trabajo: los nombres se acuerdan con Rebeca (Acción 0).],
    )
  ])
  // lo único que la lámina dice: su pie, a máquina, con la primera aparición de cada signo hallado
  place(top + left, dx: 0mm, dy: y(5) + 2mm, block(width: 165mm, [
    #rotulo("lo que la lámina dice: su pie", c: tinta)
    #line(length: 100%, stroke: fino(w: 0.5pt))
    #v(1mm)
    #set par(leading: 0.95em, justify: true)
    #for s in D.pie {
      if "celda" in s {
        box(baseline: 0pt, inset: (x: 0.3mm), outset: (y: 0.9mm), stroke: punteado(w: 0.5pt),
          text(font: mono, size: 8pt, fill: violeta, s.t))
        h(0.05mm)
        box(text(font: mono, size: 4.4pt, fill: violeta, baseline: -2.4pt, str(s.celda)))
      } else {
        text(font: mono, size: 8pt, fill: grafito, s.t)
      }
    }
    #v(1.5mm)
    #m([en violeta, la primera aparición de cada signo hallado y el número de su celda: así se llenó la caja], t: 5.8pt, c: gris)
  ]))
})

// ================================================================= 3 · ficha técnica
#hoja("ficha técnica", {
  en(1, 1, k: 8, titulo[ficha técnica])
  let filas = (
    ("Familia", [Contenida (nombre de trabajo; se acuerda con Rebeca: `08_nombres.md`)]),
    ("Estados", [calco · placa · cinta · frotado 01…n · agua quieta y tocada · voz. Son estados, no pesos: no hay Regular]),
    ("Signos", [55 y un gesto: 30 hallados en el pie, 25 reconstruidos por analogía y el ¶, que se hace con los dedos]),
    ("Caja", [8 × 7 celdas, la retícula de la cabeza de la ídolo. Solo caja baja: una mayúscula tecleada se escribe en caja baja]),
    ("Celda", [#coma(M.celda_razon, d: 2) de ancho por alto: #coma(M.celda.ancho) × #coma(M.celda.alto) mm en la placa, #M.celda.avance × 1000 UPM. Monoespaciada]),
    ("Líneas", [afuera +#M.lineas.afuera.upm · borde +#M.lineas.borde.upm · fondo ±0 · desagüe #str(M.lineas.desague.upm).replace("-", "−") (UPM). Las ascendentes miden #coma(P.razon, d: 2) veces la altura de x, como en el pie]),
    ("Trazo", [un canal de #coma(M.canal.mm) mm (#M.canal.upm UPM), sin contraste; todo contorno se abre abajo, en su desagüe]),
    ("Placas", [#D.poliza.total: las que pide el verso que más usa cada signo (la póliza). Papel de aluminio de cocina, repujado por el reverso]),
    ("Proporciones", [la celda y la altura de x, medidas en la lámina enderezada (plano P-11)]),
    ("Formatos", [placas de 150 mm; la fuente digital, si cierra, con una variante escaneada por placa]),
    ("Uso", [ningún uso comercial sin acuerdo con Rebeca. Los motivos de Tiwanaku son referencia, nunca letra]),
    ("Diseño", [las manos, desde el pie de la lámina «según Posnansky». Proyecto: Joaquin Max Cuevas Ventura]),
    ("Asistencia", [hecho con asistencia de IA: la gramática, la simulación y este espécimen son código]),
  )
  place(top + left, dx: 0mm, dy: y(2) - 4mm, block(width: 165mm, {
    set text(size: 7.8pt)
    set par(leading: 0.48em)
    grid(columns: (an(2) + J, 1fr), row-gutter: 0mm,
      ..filas.map(((k, v)) => (
        block(width: 100%, inset: (y: 1.6mm), stroke: (top: fino(w: 0.4pt)), m(k, t: 6.4pt)),
        block(width: 100%, inset: (y: 1.6mm), stroke: (top: fino(w: 0.4pt)), v),
      )).flatten(),
      block(width: 100%, stroke: (top: fino(w: 0.4pt))), block(width: 100%, stroke: (top: fino(w: 0.4pt))),
    )
  }))
})

// ================================================================= 4 · la celda, a tamaño real
#hoja("la celda · 1:1", {
  // la placa de 150 mm, a 1:1, con la celda y sus cuatro líneas: vacía, porque la placa la hace la mano
  let ox = 7.5mm
  let oy = 4mm
  place(top + left, dx: ox, dy: oy, rect(width: 150mm, height: 150mm, stroke: fino(c: gris, w: 0.5pt)))
  let c = M.celda
  marco(ox + c.x0 * 1mm, oy + c.y0 * 1mm, c.ancho * 1mm, c.alto * 1mm, fino(w: 0.6pt), hueco: 3mm)
  for (nombre, k) in (("afuera", "afuera"), ("borde", "borde"), ("fondo", "fondo"), ("desagüe", "desague")) {
    let yy = oy + M.lineas.at(k).mm * 1mm
    linea((ox, yy), (ox + 150mm, yy), rayado(c: gris))
    place(top + left, dx: ox + 1.2mm, dy: yy - 3mm, m(nombre, t: 6pt, c: gris))
    let u = M.lineas.at(k).upm
    place(top + left, dx: ox + 151.5mm, dy: yy - 1.6mm, m(if u == 0 { "±0" } else if u > 0 { "+" + str(u) } else { "−" + str(-u) }, t: 6.2pt))
  }
  place(top + left, dx: ox + c.x0 * 1mm + 1.2mm, dy: oy + c.y0 * 1mm + 1.2mm,
    m([celda #coma(M.celda_razon, d: 2) : 1 · #coma(c.ancho) × #coma(c.alto) mm · #c.avance × 1000 UPM], t: 6pt))
  place(top + left, dx: ox + 30mm, dy: oy + 76mm, block(width: 90mm, align(center, [
    #text(size: 11pt, style: "italic", fill: grafito)[aquí va la placa de la mano]
    #v(1mm)
    #etiqueta("mano")
  ])))
  place(top + left, dx: ox, dy: oy + 152.5mm, m([1:1 · impreso al 100 %, la placa mide 150 mm: es la pauta de calco (`esquemas/pauta_azulejo.svg`)], t: 6pt, c: gris))
}, ver_reticula: false)

// ================================================================= 5 · la familia: estados
#hoja("la familia: estados, no pesos", {
  en(1, 1, k: 8, [
    #titulo[estados, no pesos]
    #v(1mm)
    #text(size: 8.4pt)[Cada estilo es un estado de la letra en la cadena de la obra. Ninguno es la versión normal de los demás. Aquí, la «a» de la celda 8, hallada en «erosionado», en cada estado: la de la máquina, ya hecha; la de la mano, por hacer. En cursiva, el nombre que se propone para cada estilo (08).]
  ])
  let filas = (
    ("calco", "acción 3", (2,), "Calcada"),
    ("placa", "acción 4", (3, 4), "Repujada"),
    ("cinta", "acción 6", (5,), "Tapada"),
    ("frotado", "acción 8", (6,), "Frotada 01 … n"),
    ("agua", "acción 9", (7, 8), "Mojada · Tocada"),
    ("voz", "acción 10", (9,), "Dicha"),
  )
  let oy = y(2) + 10mm
  let alto = 17.6mm
  for (i, (estado, accion, paneles, nombre)) in filas.enumerate() {
    let py = oy + i * (alto + 3mm)
    linea((0mm, py - 1.6mm), (165mm, py - 1.6mm), fino(w: 0.4pt))
    place(top + left, dx: 0mm, dy: py, block(width: an(2), [
      #rotulo(estado, c: tinta) \
      #m(accion, t: 5.6pt, c: gris) \
      #v(0.5mm)
      #text(size: 7.4pt, style: "italic", fill: grafito)[#nombre]
    ]))
    for (k, p) in paneles.enumerate() {
      let px = x(3) + k * (alto + 2mm)
      place(top + left, dx: px, dy: py, box(width: alto, height: alto, clip: true, image(D.estados.a.at(p), width: alto, height: alto, fit: "cover")))
      place(top + left, dx: px - 0.6mm, dy: py - 0.6mm, rect(width: alto + 1.2mm, height: alto + 1.2mm, stroke: punteado(w: 0.45pt)))
    }
    // la de la mano: una celda vacía
    marco(x(7), py, alto * 0.9, alto, punteado(c: gris, w: 0.55pt), hueco: 1.6mm)
    place(top + left, dx: x(7) + alto * 0.9 + 2mm, dy: py + alto / 2 - 2mm, m("la mano", t: 5.6pt, c: gris))
  }
  place(top + left, dx: x(3), dy: oy + 6 * (alto + 3mm) - 0.4mm, etiqueta("maquina"))
  place(top + left, dx: x(7), dy: oy + 6 * (alto + 3mm) - 0.4mm, etiqueta("mano"))
})

// ================================================================= 6 · el peso se mide en frotadas
#hoja("el peso: frotadas", {
  en(1, 1, k: 8, [
    #titulo[el peso se mide en frotadas]
    #v(1mm)
    #text(size: 8.4pt)[No hay Light ni Bold. Un papel sobre la placa, frotado con grafito hasta que la letra no se lee: cada frotada se lleva un poco del relieve. La serie va del _Frotado 01_, el más cargado, al último que se lee. Es la cadena de la obra hecha escala tipográfica.]
  ])
  place(top + left, dx: 0mm, dy: y(3) - 4mm, block(width: 165mm, [
    #image("/simulacion/salida/08b_frotadas_de_la_a.jpg", width: 165mm)
    #v(-1mm)
    #etiqueta("maquina") #h(2mm) #m([las frotadas de la «a», de la primera a la última que se lee], t: 6pt, c: gris)
  ]))
  place(top + left, dx: 0mm, dy: y(6) - 2mm, block(width: 165mm, {
    set text(size: 8pt)
    grid(columns: (an(4), an(4)), column-gutter: J,
      [#text(size: 30pt, weight: 300)[#D.frotadas.halladas] \ #m([frotadas, en promedio, hasta que no se lee una hallada], t: 6pt, c: gris)],
      [#text(size: 30pt, weight: 300, fill: violeta)[#D.frotadas.reconstruidas] \ #m([las reconstruidas: hechas a puntos, tienen menos relieve y se borran antes], t: 6pt, c: violeta)],
    )
  }))
})

// ================================================================= 7 · la caja: lo hallado
#hoja("la caja: lo hallado", {
  // cada celda de la página es una celda de la letra: la caja entera, con las letras que el pie ya tiene
  for c in D.caja {
    let px = x(c.columna)
    let py = y(c.fila)
    if c.estado == "hallada" {
      marco(px, py, COL, FIL, fino(w: 0.45pt))
      let h = FIL * 0.62                      // el recorte va de 2,1 x arriba a 0,9 x abajo: la base, al 70 %
      place(top + left, dx: px + COL / 2 - h * c.ancho / 2, dy: py + FIL * 0.733 - h * 0.7, image(c.testigo, height: h))
      place(top + left, dx: px + 0.7mm, dy: py + 0.6mm, m(str(c.celda), t: 4.6pt, c: gris))
    } else if c.estado == "reconstruida" {
      marco(px, py, COL, FIL, punteado(w: 0.6pt))
      place(top + left, dx: px + 0.7mm, dy: py + 0.6mm, m(str(c.celda), t: 4.6pt, c: violeta))
      place(top + left, dx: px, dy: py + FIL / 2 - 2.6mm, block(width: COL, align(center, text(font: mono, size: 11pt, fill: lila, c.signo))))
    } else {
      marco(px, py, COL, FIL, punteado(c: gris, w: 0.6pt))
      place(top + left, dx: px + 0.7mm, dy: py + 0.6mm, m(str(c.celda), t: 4.6pt, c: gris))
      place(top + left, dx: px, dy: py + FIL / 2 - 3mm, block(width: COL, align(center, text(font: serif, size: 13pt, fill: gris2, "¶"))))
    }
  }
  place(top + left, dx: 0mm, dy: y(7) + FIL + 3.2mm, block(width: 165mm, [
    #etiqueta("hallada") #h(1.5mm) #m([las 30 halladas: la primera aparición de cada signo en el pie, recortada de la foto. En violeta, a puntos, las 25 que faltan; en gris, el ¶, que se hace con los dedos.], t: 5.8pt, c: gris)
  ]))
}, ver_reticula: false)

// ================================================================= 8 · la caja: la propuesta de la máquina
#hoja("la caja: la propuesta de la máquina", {
  en(1, 1, k: 8, [
    #titulo[la propuesta de la máquina]
    #v(1mm)
    #text(size: 8.4pt)[La gramática arma los 55 cuerpos base desde cuatro generadores (o, l, n, a): del pie, las medidas; de la obra, la forma. *No es la letra:* no entra en la caja ni en la fuente, y no se usa para componer. Es una hipótesis, para confrontarla con la mano.]
  ])
  // la caja de la máquina: los 55 cuerpos en vectores, cada uno en su celda
  let cw = 14mm
  let ch = cw / 0.9
  let cj = 2.4mm
  for c in D.caja {
    let px = (c.columna - 1) * (cw + cj)
    let py = y(2) + 3mm + (c.fila - 1) * (ch + cj)
    let hallada = c.estado == "hallada"
    marco(px, py, cw, ch, if hallada { fino(c: filete, w: 0.4pt) } else { punteado(c: lila, w: 0.5pt) }, hueco: 1.4mm)
    place(top + left, dx: px + 0.6mm, dy: py + 0.4mm, m(str(c.celda), t: 3.6pt, c: gris2))
    if "cuerpo" in c {
      place(top + left, dx: px, dy: py, image(c.cuerpo, width: cw, height: ch))
    } else {
      place(top + left, dx: px, dy: py + ch * 0.4, block(width: cw, align(center, m([los dedos], t: 4pt, c: gris2))))
    }
  }
  place(top + left, dx: 8 * (cw + cj) + 1mm, dy: y(2) + 3mm, block(width: 165mm - 8 * (cw + cj) - 1mm, [
    #set text(hyphenate: false)
    #set par(justify: false)
    #etiqueta("maquina")
    #v(1.5mm)
    #m([en tinta, lo hallado; en violeta y a puntos, lo reconstruido], t: 5.8pt, c: gris)
    #v(2mm)
    #m([la celda 56 no es de la máquina: el signo final se hace con los dedos], t: 5.8pt, c: gris)
    #v(2mm)
    #m([el terminal en gota: el trazo engorda hacia su final y hacia abajo, como chorrea el líquido en la obra], t: 5.8pt, c: gris)
  ]))
})

// ================================================================= 9 · anatomía
#hoja("anatomía", {
  en(1, 1, k: 8, [
    #titulo[anatomía: veinticuatro decisiones]
    #v(1mm)
    #text(size: 8.4pt)[En lugar de rasgos opcionales, la letra tiene decisiones. Cada una está dibujada en los planos (`planos/`), con su porqué al lado.]
  ])
  let gens = (("o", "la cuenca"), ("l", "el fuste"), ("n", "el hombro"), ("a", "el gancho y la gota"))
  for (i, (g, nombre)) in gens.enumerate() {
    let px = x(1 + 2 * i)
    marco(px, y(2) + 2mm, an(2), an(2) / 0.9, fino(c: filete, w: 0.4pt), hueco: 2.4mm)
    place(top + left, dx: px, dy: y(2) + 2mm, block(width: an(2), [
      #box(width: an(2), height: an(2) / 0.9, image(D.caja.find(c => c.signo == g).cuerpo, width: an(2), height: an(2) / 0.9))
      #v(-0.6mm)
      #m([#g · #nombre], t: 6pt)
    ]))
  }
  place(top + left, dx: 0mm, dy: y(2) + 2mm + an(2) / 0.9 + 6mm, etiqueta("maquina"))
  let cuadro = (
    ("cuerpo", [la celda de la cabeza, #coma(M.celda_razon, d: 2) : 1]), ("ancho", [monoespaciada: una letra, una celda]),
    ("líneas", [fondo, borde, afuera, desagüe]), ("altura de x", [#coma(P.razon, d: 2) de las ascendentes]),
    ("contraste", [ninguno: un canal de #coma(M.canal.mm) mm]), ("curvas", [radio mínimo de 0,6 canal]),
    ("remates", [ninguno: un corte, gastado]), ("contornos", [abiertos: un desagüe de 3 mm]),
    ("ojo", [arriba, el del pie; abajo, una vasija]), ("sobrepaso", [arriba sí; abajo no]),
    ("eje", [vertical: sin pluma]), ("asta", [un fuste en tres planos]),
    ("pie del asta", [un asiento cóncavo, sin serifa]), ("hombro", [superelipse n = 3, arranque tangente]),
    ("terminales", [en gota si mira abajo; corte si mira arriba]), ("a", [de dos pisos: la suma de las partes]),
    ("punto", [un cuadrado de cinta]), ("tilde", [una gota]),
    ("virgulilla", [una onda]), ("enlace de la g", [un sifón]),
    ("rincones agudos", [un alivio]), ("cifras", [elzevirianas, cada una en su celda]),
    ("dobles opuestos", [varían: ? ¿ · 6 9 · « »]), ("mayúsculas", [ninguna: solo caja baja]),
  )
  place(top + left, dx: 0mm, dy: y(5) + 4mm, block(width: 165mm, {
    set text(size: 7.2pt)
    grid(columns: (an(4), an(4)), column-gutter: J,
      ..range(2).map(col => grid(columns: (an(1) + 6mm, 1fr), row-gutter: 0mm,
        ..cuadro.slice(col * 12, col * 12 + 12).map(((k, v)) => (
          block(width: 100%, inset: (y: 1.05mm), stroke: (bottom: fino(c: filete, w: 0.4pt)), m(k, t: 6pt)),
          block(width: 100%, inset: (y: 1.05mm), stroke: (bottom: fino(c: filete, w: 0.4pt)), v),
        )).flatten())))
  }))
})

// ================================================================= 10 · de punta a punta
#hoja("de punta a punta", {
  en(1, 1, k: 8, [
    #titulo[una letra de punta a punta]
    #v(1mm)
    #text(size: 8.4pt)[Del pie a la voz, una letra por todos sus estados. Una hallada y una reconstruida: en el frotado y en el agua, la reconstruida se ve menos.]
  ])
  let lado = 15.6mm
  for (fila, (clave, titulo_, estado)) in (("a", "la «a», celda 8, hallada en «erosionado»", "hallada"), ("z", "la «z», celda 32, que no está en el pie", "reconstruida")).enumerate() {
    let py = y(2) + 6mm + fila * 58mm
    place(top + left, dx: 0mm, dy: py - 5.4mm, m(titulo_, t: 6.4pt, c: if estado == "hallada" { tinta } else { violeta }))
    for (k, ruta) in D.estados.at(clave).enumerate() {
      let px = calc.rem(k, 5) * (lado * 2 + 1.5mm)
      let fy = py + calc.floor(k / 5) * (lado + 9mm)
      place(top + left, dx: px, dy: fy, box(width: lado * 2, height: lado, clip: true, image(ruta, width: lado * 2, height: lado, fit: "contain")))
      place(top + left, dx: px, dy: fy + lado + 0.8mm, m(D.estados.nombres.at(k), t: 5.4pt, c: gris))
    }
  }
  place(top + left, dx: 0mm, dy: y(7) + 6mm, etiqueta("maquina"))
})

// ================================================================= 11 · componer
#hoja("componer: el poema en la caja", {
  en(1, 1, k: 8, [
    #titulo[componer con placas]
    #v(1mm)
    #text(size: 8.4pt)[No se compone con una fuente: se compone con placas. Cada signo es una placa; entre palabras, una celda vacía. *Dentro de un verso, ninguna placa se repite:* a cada signo le toca la primera placa que no esté ya en el verso. La caja tiene #D.poliza.total placas: las que pide el verso que más usa cada signo.]
  ])
  let estados = (:)
  for c in D.caja { estados.insert(c.signo, c.estado) }
  for (i, v) in D.compuestos.enumerate() {
    let n = v.celdas.len()
    let w = calc.min(165mm / n, 9.2mm)
    let h = w / 0.9
    let py = y(2) + 10mm + i * (h + 16mm)
    place(top + left, dx: 0mm, dy: py - 5mm, text(size: 8.4pt, style: "italic", fill: grafito, v.verso))
    for (k, c) in v.celdas.enumerate() {
      let px = k * w
      if c.s == " " { continue }
      let e = estados.at(c.s, default: "reconstruida")
      let s = if e == "hallada" { fino(w: 0.4pt) } else { punteado(w: 0.55pt) }
      marco(px + 0.4mm, py, w - 0.8mm, h, s, hueco: 1mm)
      place(top + left, dx: px, dy: py + h * 0.22, block(width: w, align(center, text(font: mono, size: 9pt, fill: if e == "hallada" { tinta } else { violeta }, c.s))))
      if e != "hallada" { place(top + left, dx: px + w / 2 - 0.3mm, dy: py + h * 0.22 + 4.3mm, circle(radius: 0.3mm, fill: violeta)) }
      place(top + left, dx: px, dy: py + h + 0.8mm, block(width: w, align(center, m([#c.placa/#c.de], t: 4.6pt, c: gris))))
    }
  }
  place(top + left, dx: 0mm, dy: y(7) + 2mm, block(width: 165mm, [
    #m([cada celda: el signo y su placa (la que le toca / las que tiene). En tinta, hallado; en violeta y con un punto debajo, reconstruido: es la marca de la letra dudosa en epigrafía, y se lee también sin color. No es la letra: es el orden de las placas], t: 5.8pt, c: gris)
  ]))
})

// ================================================================= 12 · la póliza
#hoja("la póliza", {
  en(1, 1, k: 8, [
    #titulo[ciento diecinueve placas]
    #v(1mm)
    #text(size: 8.4pt)[Cuántas placas tiene cada signo: las que pide el verso que más lo usa, y al menos una por celda. Si un texto pide más, las que sobran toman la última: la caja se acabó.]
  ])
  let ox = 0mm
  let oy = y(2) + 4mm
  let w = an(1)
  let h = 15.4mm
  for c in D.caja {
    let px = ox + (c.columna - 1) * (w + J)
    let py = oy + (c.fila - 1) * (h + 2.4mm)
    let n = D.poliza.placas.at(c.signo, default: 0)
    let col = if c.estado == "hallada" { tinta } else if c.estado == "reconstruida" { violeta } else { gris }
    let s = if c.estado == "hallada" { fino(w: 0.4pt) } else if c.estado == "reconstruida" { punteado(w: 0.55pt) } else { punteado(c: gris, w: 0.55pt) }
    marco(px, py, w, h, s, hueco: 1.4mm)
    place(top + left, dx: px + 1mm, dy: py + 1mm, text(font: mono, size: 9pt, fill: col, c.signo))
    place(top + left, dx: px, dy: py + h - 6.4mm, block(width: w - 1.2mm, align(right, text(font: serif, size: 15pt, weight: 300, fill: col, str(n)))))
  }
  place(top + left, dx: 0mm, dy: oy + 7 * (h + 2.4mm) + 1mm, m([en la celda, el signo y sus placas · #D.poliza.versos versos; el más largo, #D.poliza.maximo signos con los espacios], t: 5.8pt, c: gris))
})

// ================================================================= 13 · las proporciones
#hoja("las proporciones", {
  en(1, 1, k: 8, [
    #titulo[de dónde salen las proporciones]
    #v(1mm)
    #text(size: 8.4pt)[La letra toma del registro dos proporciones: la celda, de la retícula de la cabeza, y la altura de x, del pie. Se midieron en una foto de cámara y, el 8 de noviembre, en la lámina enderezada (plano P-11).]
  ])
  // el ancho por alto de cada columna: la foto de cámara y la lámina enderezada
  let gx = 8mm
  let gy = y(2) + 11mm
  let gw = 74mm
  let gh = 52mm
  let v0 = 0.78
  let v1 = 1.0
  let Q(i, v) = (gx + 4mm + i * (gw - 8mm) / 6, gy + gh - (v - v0) / (v1 - v0) * gh)
  for v in (0.80, 0.85, 0.90, 0.95, 1.00) {
    let (a, b) = (Q(-0.3, v), Q(6.3, v))
    linea(a, b, fino(c: filete, w: 0.4pt))
    place(top + left, dx: gx - 7mm, dy: a.at(1) - 1.5mm, m(coma(v, d: 2), t: 5.4pt, c: gris))
  }
  let viejo = R.antes.ancho_por_alto
  let nuevo = R.paso_x.map(p => p / R.paso_y_mediana)
  place(top + left, curve(stroke: rayado(c: gris, w: 0.6pt), curve.move(Q(0, viejo.at(0))), ..range(1, 7).map(i => curve.line(Q(i, viejo.at(i))))))
  place(top + left, curve(stroke: fino(w: 0.9pt), curve.move(Q(0, nuevo.at(0))), ..range(1, 7).map(i => curve.line(Q(i, nuevo.at(i))))))
  for i in range(7) {
    let (px, py) = Q(i, nuevo.at(i))
    place(top + left, dx: px - 0.8mm, dy: py - 0.8mm, circle(radius: 0.8mm, fill: papel, stroke: fino(w: 0.5pt)))
    let (qx, qy) = Q(i, viejo.at(i))
    place(top + left, dx: qx - 0.6mm, dy: qy - 0.6mm, circle(radius: 0.6mm, fill: papel, stroke: fino(c: gris, w: 0.4pt)))
    place(top + left, dx: px - 3mm, dy: gy + gh + 1.6mm, block(width: 6mm, align(center, m([#(i + 1)–#(i + 2)], t: 5pt, c: gris))))
  }
  for (v, s, t, c) in ((R.antes.celda, rayado(c: gris2, w: 0.5pt), "antes 0,84", gris), (R.celda, fino(c: violeta, w: 0.8pt), "celda " + coma(R.celda, d: 2), violeta)) {
    let (a, b) = (Q(-0.3, v), Q(6.3, v))
    linea(a, b, s)
    place(top + left, dx: b.at(0) + 1.5mm, dy: b.at(1) - 1.6mm, m(t, t: 5.8pt, c: c))
  }
  place(top + left, dx: gx, dy: gy - 6mm, m([ancho por alto, entre las columnas · — lámina enderezada · - - foto de cámara], t: 5.6pt, c: gris))
  // los números
  place(top + left, dx: x(6) + 2mm, dy: gy - 2mm, block(width: an(3) - 2mm, [
    #rotulo("la celda", c: tinta)
    #line(length: 100%, stroke: fino(w: 0.5pt))
    #text(size: 34pt, weight: 300)[#coma(R.celda, d: 2)]
    #v(-2mm)
    #text(size: 7.4pt)[la retícula entera, ocho columnas sobre siete filas. En la foto de cámara medía #coma(R.antes.global, d: 2) y la celda usaba 0,84: la cámara angostaba la cabeza.]
    #v(3mm)
    #rotulo("la altura de x", c: tinta)
    #line(length: 100%, stroke: fino(w: 0.5pt))
    #text(size: 34pt, weight: 300)[#coma(P.razon, d: 2)]
    #v(-2mm)
    #text(size: 7.4pt)[las ascendentes, sobre la x. La lámina enderezada da #coma(P.lamina_enderezada.razon, d: 2): menos que el paso de la medida. En la placa, #coma(P.en_la_placa.diferencia_mm) mm.]
  ]))
  place(top + left, dx: 0mm, dy: y(6) + 4mm, block(width: an(5), [
    #text(size: 7.6pt)[Las columnas se angostan hacia los bordes (#coma(calc.min(..R.ancho_por_alto), d: 2)) y se ensanchan al centro (#coma(calc.max(..R.ancho_por_alto), d: 2)): el dibujo curva la cabeza como un cilindro. La letra toma el dibujo, no la piedra. A confirmar con regla en el impreso.]
  ]))
})

// ================================================================= 14 · las reglas
#hoja("las reglas", {
  en(1, 1, k: 8, titulo[lo que la letra no hace])
  let reglas = (
    ([*No se compone con la máquina.*], [Lo que hizo la máquina se rotula siempre como propuesta de la máquina. Ninguna de esas formas es la letra ni se usa para componer texto.]),
    ([*No hay Regular.*], [No es una fuente variable y no se interpolan pesos: los estilos son estados.]),
    ([*No hay mayúsculas.*], [Las mayúsculas son letras de monumento, y el pie escribe en mayúsculas justamente el nombre impuesto.]),
    ([*No lleva motivos.*], [Los motivos de Tiwanaku son referencia visual, nunca parte de una letra.]),
    ([*No se nombra con la ídolo.*], [La fuente no se llama Kochamama ni toma palabras aymaras o quechuas como marca.]),
    ([*No se vende sin acuerdo.*], [Ningún uso comercial sin acuerdo con Rebeca.]),
    ([*No muestra la obra sin permiso.*], [Ni fotos ni videos de la obra o del cuerpo de Rebeca sin su permiso escrito.]),
    ([*El verde es luz.*], [Aparece solo como luz, en el agua y en la voz; nunca como tinta.]),
  )
  place(top + left, dx: 0mm, dy: y(2) - 2mm, block(width: 165mm, {
    set text(size: 8.2pt)
    set par(leading: 0.5em)
    grid(columns: (an(3), 1fr), column-gutter: J, row-gutter: 0mm,
      ..reglas.map(((k, v)) => (
        block(width: 100%, inset: (y: 2.2mm), stroke: (top: fino(w: 0.4pt)), k),
        block(width: 100%, inset: (y: 2.2mm), stroke: (top: fino(w: 0.4pt)), v),
      )).flatten())
  }))
})

// ================================================================= 15 · lo que falta
#hoja("lo que falta", {
  en(1, 1, k: 8, titulo[lo que falta])
  let falta = (
    ([Acción 0], [Acordar con Rebeca el nombre de la familia y de sus estados.]),
    ([Acciones 3 y 4], [Calcar el pie y repujar las 119 placas: la letra.]),
    ([La celda], [Medir con regla la retícula de la cabeza en el impreso: si no mide 0,90, se rehacen la gramática, los planos y el libro.]),
    ([El libro], [Encontrar el libro del que sale la lámina «según Posnansky».]),
    ([La fuente digital], [Si cierra: una variante escaneada por placa, y la póliza en OpenType (`digital/poliza.py`).]),
    ([Este espécimen], [Rehacerlo con las placas de la mano: donde hoy dice «por hacer», la letra.]),
  )
  place(top + left, dx: 0mm, dy: y(2) - 2mm, block(width: 165mm, {
    set text(size: 8.4pt)
    grid(columns: (an(3), 1fr), column-gutter: J, row-gutter: 0mm,
      ..falta.map(((k, v)) => (
        block(width: 100%, inset: (y: 2.4mm), stroke: (top: punteado(c: gris, w: 0.6pt)), m(k, t: 6.6pt)),
        block(width: 100%, inset: (y: 2.4mm), stroke: (top: punteado(c: gris, w: 0.6pt)), v),
      )).flatten())
  }))
})

// ================================================================= 16 · colofón
#hoja("colofón", {
  en(1, 1, k: 8, titulo[colofón])
  place(top + left, dx: x(4), dy: y(2) - 2mm, block(width: an(5), [
    #set text(size: 8.2pt)
    #set par(leading: 0.55em, spacing: 1.1em)
    *Contenida: espécimen.* Compuesto el #D.fecha en Typst, desde `tipografia/especimen/` en el repositorio del proyecto, con los datos de la caja, de la gramática y de la simulación. Proyecto: Joaquin Max Cuevas Ventura. Homenaje a _Contener una ruina: acciones para desenterrar una voz_, de Rebeca Paz Prada con CreaciónxAcuerpamiento.

    *Las letras de este espécimen* no son Contenida, que todavía no existe: son Newsreader (Production Type), para leer, y Courier Prime (Alan Dague-Greene), a máquina. Las dos con licencia SIL Open Font License, incrustadas.

    *Las imágenes* dicen qué son: hallada en la lámina (las letras del pie, recortadas de una foto que no se publica) o propuesta de la máquina (la gramática y la simulación). Lo de la máquina va punteado, y todo marco se abre abajo, en su desagüe.

    *Hecho con asistencia de IA.* La gramática, la simulación, los planos y este espécimen son código; las decisiones se discutieron con el autor del proyecto.

    #v(4mm)
    #m([página de 180 × 200 mm: 0,90, la proporción de la celda · retícula: la caja de 8 × 7], t: 6pt, c: gris)
  ]))
})
