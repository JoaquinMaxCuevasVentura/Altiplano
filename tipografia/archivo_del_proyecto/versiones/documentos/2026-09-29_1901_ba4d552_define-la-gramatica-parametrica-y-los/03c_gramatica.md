# 03c. La gramática: la anatomía base, antes de los estados

`03b` escribió las reglas del cuerpo de la letra, pero la máquina las aplicaba al final, sobre la silueta del testigo: primero calcaba una romana y después la gastaba, la abría y la hacía gotear. Este documento invierte el orden:

> **anatomía base → estados**

Primero se define, en vectores, cómo se comporta la forma. Recién después esa forma pasa por *Placa*, *Piel*, *Copia*, *Agua* y *Azulejo*.

## 1. Qué se toma del pie, y qué no

El pie da **medidas**. No da formas.

- las cuatro líneas: afuera, borde, fondo y desagüe;
- dónde van las astas;
- cuánto miden el ojo de la o y el de la a;
- a qué altura empieza el gancho de la a;
- el grueso y el fino del trazo.

Todo lo demás lo deciden los parámetros de la §2, que salen de la obra.

**El testigo sigue siendo el sustituto** (Liberation Serif) hasta que llegue el libro. El código mide el testigo, así que cambiarlo cambia las medidas, no las reglas.

## 2. Los parámetros

Cada parámetro tiene un valor, controla una sola cosa y viene de una decisión de la obra. Están en `simulacion/salida/gramatica/gramatica.json`. Las medidas van en píxeles del lienzo de la placa: 4 px son 1 mm.

| Parámetro | Valor | Qué controla | De dónde sale |
|---|---|---|---|
| `canal` | 31,8 px (8 mm) | El grosor único del trazo: la media entre el grueso y el fino de la o del pie. **Sin contraste** | El punzón y la cinta no modulan: no hay pluma (D2, D12) |
| `radio_chapa` | 0,6 canal | El radio mínimo de toda curva. Al ser mayor que medio canal, el contorno interior nunca se cruza | El aluminio se rasga en un ángulo agudo (D2) |
| `trapecio` | 0,70 | El ancho del fondo plano de cada cuenca, sobre su ancho mayor | La proyección llega en trapecio; la bandeja (D8) |
| `pared` | 0,55 | Cuánto se abomba la pared de la cuenca al bajar: 0 es recta, 1 es una vasija redonda | El vaso |
| `desague` | 3 mm | La abertura en el fondo de cada cuenca: el surco del punzón con sus lomas | «Ningún contenedor aguanta lo que contiene» (D16) |
| `hombro` | 3 | El exponente de la superelipse de los arcos altos (2 sería una elipse): el arco se tensa | La chapa curvada sobre un hombro o una clavícula (D3) |
| `hombro_caida` | 0,40 | Dónde el arco se vuelve vertical, del borde al fondo | El testigo de la n, a ojo. Falta medirlo en el libro |
| `facetas`, `quiebre` | 3 planos, 1,6° | Cada fuste tiene tres planos, con un quiebre apenas visible | La placa cambia de plano al apoyarse en el cuerpo (D3). «Apenas» (D11) |
| `asiento_ancho`, `asiento_alto` | 2 y 0,9 canales | El pie de cada fuste se ensancha hacia el fondo en una curva cóncava | El peso se asienta en la tierra |
| `intemperie` | 0,12 canal | El radio con que se gastan todas las esquinas. Arriba no hay remates: el fuste termina en un corte | «Hoy está muy erosionado y casi no se ven esos detalles» (el pie) |
| `alivio` | 0,28 canal | El rebaje en cada encuentro interior en ángulo | Para que el aluminio no se desgarre (D2) |
| `gancho_fin` | 125° | Dónde termina el gancho alto antes de soltar la gota | Que la gota cuelgue libre |
| `gota_masa`, `gota_caida`, `gota_cuello` | 1,25, 0,5 y 0,55 canales | La gota: un cuello y una masa que cae vertical, por su peso | El líquido que chorrea de la boca (D16) |
| `cinta` | 1 canal | El ancho de la cinta, a la escala en que iguala al canal | La cinta que tapó ojos y boca (D12) |

**Una condición geométrica que es también una condición material:** si una curva tiene un radio menor que medio canal, el contorno interior se cruza consigo mismo. Es la misma curva en la que el aluminio se rasga. `radio_chapa` cumple las dos.

## 3. Las siete partes de tu propuesta

| Parte | Cómo entra | Qué se ajustó |
|---|---|---|
| 1. **La cuenca** (o, d, p, b, e) | Arriba, el ojo del pie. Abajo, la pared baja abombada (`pared`) hasta un fondo plano (`trapecio`), y el fondo se abre (`desague`) | Nada |
| 2. **La banda facetada** (l, i, t, h) | Fustes en tres planos, con quiebres de 1,6° | La cinta no entra aquí: tiene su propio estado (§5). Si el fuste fuera cinta, las curvas también serían facetas, y eso contradice al punzón |
| 3. **El desborde gravitacional** (a, c, f, r) | Una gota con cuello, que cae vertical y no sigue la dirección del trazo | Nada |
| 4. **El pliegue dermometálico** (n, m, h) | El arco es una superelipse de exponente 3: tenso, achatado | Nada |
| 5. **La asimetría de la intemperie** | Arriba, corte sin remate. Abajo, asiento | Sin «siglos de viento en Akapana»: no sabemos dónde estuvo el ídolo (el pie supone Pumapuncu). La fuente es el pie: «muy erosionado» |
| 6. **El sifón** (g) | Se define al derivar la g: dos cuencas unidas por un canal estrangulado, como vasos comunicantes | Sin la *challa* invertida. Las lecturas rituales no se vuelven operaciones del proyecto (`01`, §1.6). Queda la física del sifón |
| 7. **El alivio de rasgado** (v, w, k, x) | Parámetro `alivio`, para los encuentros en ángulo | En los cuatro generadores no aparece: todo encuentro es tangente (el arco sale del fuste en su misma dirección), y un encuentro tangente no tiene rincón que rasgar |

## 4. Las curvas maestras de los cuatro generadores

Cada generador es una lista de **trazos**: ejes (poligonales densas) que se engrosan con el ancho del canal. A eso se suman **formas** (asientos y gotas) y se restan **alivios**. Después, todo se gasta con el radio de `intemperie`. El código está en `simulacion/gramatica.py`.

**o: la cuenca.** Es un solo trazo abierto.
1. Del pie: el ancho y la altura del ojo.
2. La mitad de arriba es una elipse con esas medidas: es la del pie.
3. En cada lado, desde el punto más ancho, la pared baja en una curva (una Bézier cúbica). Sale vertical y llega horizontal al fondo, sobre la línea de fondo. El fondo plano mide `trapecio` del ancho mayor.
4. En el centro del fondo, el trazo se corta: el desagüe.

**l: el fuste.**
1. Del pie: la posición del asta y su altura.
2. El eje baja en tres planos, con quiebres de `quiebre`.
3. Arriba termina en un corte plano.
4. Abajo se ensancha en el asiento: dos curvas cóncavas que van de un canal a dos.

**n: el hombro.**
1. Del pie: las dos astas y la altura del arco.
2. Fuste izquierdo, desde el borde.
3. El arco es media superelipse de exponente `hombro`. Sale del fuste izquierdo en su misma dirección, se tensa arriba y baja como fuste derecho.
4. Los dos fustes terminan en asiento.

**a: todo junto.** Es la suma de los otros tres.
1. Del pie: el asta, el ojo y el extremo del gancho.
2. **El gancho** es un hombro que baja por el fuste hasta el asiento. Del otro lado termina a los 125° y suelta la gota.
3. **La cuenca** tiene arriba el ojo del pie. Abajo, pared abombada y fondo plano. Se abre en el punto más bajo del ojo, y el fondo sigue hasta el fuste.

Así la o, la l y la n dan las piezas de las demás letras: la cuenca, el fuste y el hombro. La a prueba que se pueden combinar.

**La lámina:** `simulacion/salida/20_gramatica.png`. Cada generador se ve en seis columnas:
1. el testigo con sus medidas;
2. las curvas maestras, con sus nodos;
3. el cuerpo en vectores (también en `gramatica/<letra>.svg`);
4. el calco que haría la mano;
5. la cinta puesta;
6. la cinta arrancada.

## 5. Un estado nuevo: *Cinta*

La cinta que tapó ojos y boca (D12) tiene sus propias leyes. La simulación las aplica sobre las curvas maestras:

| Ley | Cómo se simula |
|---|---|
| **Ancho constante** | Cada tramo es una banda del ancho de `cinta` |
| **No curva en su plano** | La curva maestra se vuelve tramos rectos: se simplifica con una tolerancia de 0,3 del ancho. Para girar, la cinta se pliega (el pliegue sigue la bisectriz del giro) o se superpone otro tramo. Donde hay dos capas, la luz pasa por dos capas |
| **Memoria de adhesión** | Arrugas cortas junto a cada pliegue |
| **Se corta con la mano** | Los extremos quedan dentados |
| **Se arranca** | Deja el rastro del adhesivo, más oscuro donde hubo dos capas |

**La cinta no hace gotas ni asientos.** Solo sigue los trazos. En la cinta, la letra pierde lo que la gravedad le había dado.

**Dónde va en la cadena.** Al lado de *Piel*: en la obra, la cinta y las placas estuvieron sobre el cuerpo al mismo tiempo. La cadena quedaría así:

> calco → placa → piel | cinta → copia → agua → voz → azulejo

**Qué falta saber:**
- **El tipo de cinta:** ¿masking o cinta color piel de farmacia? Cambia el color, el ancho (la de farmacia suele medir 12,5 mm) y cómo se rasga. La simulación usa, por ahora, el color piel.
- **Qué se usa de la obra:** el material, no el rostro de Rebeca. La cinta se pone sobre papel o sobre la placa, nunca sobre una cara.

## 6. Qué cambia respecto de `03b`

| En `03b` | En la gramática |
|---|---|
| El trazo del testigo, con su contraste | El canal: **un solo grosor**, sin contraste |
| La bandeja con paredes rectas | La pared abombada, controlada por `pared` (con 0 vuelven a ser rectas) |
| La lluvia gasta, más arriba que abajo | La intemperie: corte arriba y asiento abajo, con un radio de desgaste |
| El asta cae en una línea de media tesela | Sale: la tesela ya no es unidad de medida |
| La media caña de la piscina en la panza | El radio de la chapa: la curva mínima la pone el aluminio, no el zócalo |
| El marco de la letra: el azulejo | **La celda de la cabeza del ídolo**, 0,84 de ancho por alto, como el `.notdef` (a confirmar) |
| Las juntas de la pared | Solo en el estado *Azulejo*, cuando la letra llega a la pared |

**Se quedan:**
- el desagüe;
- las gotas;
- los puntos, las tildes y la virgulilla de `03b`, hasta que se deriven los signos que los llevan;
- las cifras en celdas;
- los nombres de las líneas: fondo, borde y desagüe son palabras de cualquier vasija.

## 7. Lo que falta

1. **Derivar de los cuatro generadores los otros 51 signos:** 26 hallados y 25 reconstruidos. Ahí entran el alivio (v, w, k, x, y) y el sifón (g).
2. **Conectar la gramática a `simular.py`** en lugar de `anatomia.py`, para que todos los estados partan del cuerpo base.
3. **Rehacer las láminas de exposición** que dependen de la anatomía anterior.
4. **Medir en el libro** lo que hoy es a ojo: `hombro_caida`, y el grueso y el fino.
