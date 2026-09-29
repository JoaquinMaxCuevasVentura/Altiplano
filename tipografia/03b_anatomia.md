# 03b. La anatomía de *Contenida*

> **Actualización:** `03c_gramatica.md` lleva estas reglas a una gramática paramétrica en vectores, aplicada **antes** de los estados. Lo que cambia está en su §6.

`03` decidió de dónde salen las letras (el pie), dónde viven (la caja), sobre qué se dibujan (la piscina) y por qué estados pasan. Faltaba el cuerpo de cada letra: sus astas, sus ojos, sus remates, sus puntos. Este documento lo resuelve.

## El principio: del pie, el esqueleto; de la obra, el cuerpo

- **Del pie se toma el esqueleto:** dónde va cada trazo, cuánto mide, qué proporción guarda con los demás. Es lo que el archivo dice, y no se cambia.
- **La anatomía la dicta la obra.** Cada parte de la letra responde a una decisión de *Contener una ruina*.

Es lo que hizo Rebeca con la lámina: no copió los relieves, los llevó a otro material y a otro cuerpo.

**Tres reglas obedecen a la gravedad.** El agua se va por abajo (el desagüe), la lluvia gasta desde arriba (los remates) y lo que se derrama cae (las gotas). La piscina vacía es eso: un lugar donde el agua ya se fue por abajo.

**Una observación, no una regla.** En el agua la imagen llega al revés: las gotas suben y el desagüe queda arriba (`simulacion/salida/09_agua_quieta.jpg`).

## Las reglas

| Nº | Parte | Regla | De dónde viene |
|---|---|---|---|
| 1 | **El trazo** | Es un **canal**: se dibuja su contorno, dos paredes y un fondo vacío. La letra es hueca | Contener. La piscina sin agua. El repujado, que levanta el contorno |
| 2 | **Todo contorno cerrado** | Tiene **desagüe**: se abre en su punto más bajo, con una abertura del ancho de una junta (3 mm). Vale para la letra, para sus ojos y para la celda vacía del `.notdef` | «Ningún contenedor aguanta lo que contiene» (D16). La piscina vacía |
| 3 | **El ojo** (contraforma cerrada) | Su mitad de arriba es la del pie. Su mitad de abajo es la **bandeja**: paredes rectas que se cierran hacia abajo en la proporción del trapecio de la proyección (0,70) y fondo plano con media caña | La bandeja con un dedo de agua (D8). El trapecio (`01`, §1.4) |
| 4 | **La panza**, por fuera | Se **asienta plana**, como el fondo de la piscina, con las esquinas redondeadas de la media caña. La letra queda como un vaso: arco arriba, fondo abajo | La piscina (D6). La ficha del monolito que lo llama vaso (a verificar) |
| 5 | **Los remates** | Los **gasta la lluvia**, que corre de arriba hacia abajo: se redondea todo, los remates altos casi desaparecen y los del pie quedan como muñones | La piedra erosionada: «casi no se ven esos detalles» (el pie) |
| 6 | **Los terminales** | Donde un trazo termina en el aire mirando hacia abajo, cuelga una **gota** que cae (la a, la c, la f, la s) | El líquido que se vierte en la boca y chorrea (D16) |
| 7 | **Los puntos** (de la i, la j, la ü, el punto, los dos puntos, el punto y coma, los puntos suspensivos, el de ¿?) | Son **cuadrados de media tesela** (12,5 mm), planos | La cinta color piel que tapó ojos y boca (D12). La tesela del piso. El punto de luz que no se mueve en los videos |
| 8 | **Las tildes** | Son **gotas**: la punta arriba y el peso abajo | La tilde marca dónde carga la voz. La voz de la obra no se entiende (D14) y el líquido cae de la boca (D16) |
| 9 | **La virgulilla de la ñ** | Es una **onda**: la del agua tocada | Tocar el agua (D15) |
| 10 | **El asta** | La letra se corre hasta que su asta principal cae en una **línea de media tesela**. Las letras sin asta quedan centradas | Contenida: la letra se acomoda a su contenedor. *The Great Stone* (`02`) |
| 11 | **Las líneas** | Base y altura de x caen en líneas de media tesela, y se llaman como la piscina: **desagüe** (descendentes), **fondo** (base), **borde** (altura de x), **afuera** (ascendentes) | La piscina como pauta (D6, D9). El público, dentro y fuera de la piscina |
| 12 | **Las cifras** | Cada una vive en una **celda**: un rectángulo dentro de otro, la celda de la cabeza del ídolo. Es el único lugar del juego donde se ve la retícula del calendario | El calendario que nadie ha leído. Todas las cifras son reconstruidas (`03`, §3.4) |

Siguen valiendo las reglas de `03`:

- lo hallado, continuo, y lo reconstruido, punteado;
- solo caja baja;
- monoespaciada;
- sin Regular;
- el signo final, hecho con los dedos.

**El temblor no es una regla de anatomía.** Lo pone la mano: «moverse como se mueve la piedra, es decir, apenas».

## Cómo lo hace la mano

Se aplica en el calco (Acción 3), en este orden, sobre la ampliación del pie:

1. **Calcar el esqueleto:** el contorno de la letra hallada, con la base y el borde de la pauta.
2. **Gastar los remates.** Los de arriba no se calcan; los de abajo, a la mitad y redondeados. Las esquinas, redondeadas.
3. **Rehacer la mitad baja de cada ojo** como bandeja. Poner la regla desde el punto más ancho del ojo, cerrar hacia abajo hasta dejar el fondo en siete décimas de ese ancho y redondear las esquinas. Por fuera, asentar plana la panza.
4. **Colgar las gotas** de los terminales que miran hacia abajo: una línea corta y una gota del grueso del trazo.
5. **Cambiar puntos y tildes.** Los puntos, por cuadrados de 12,5 mm; las tildes, por gotas.
6. **Correr la letra** hasta que su asta caiga en una línea de media tesela de la pauta.
7. **Enmarcar las cifras.** Dibujar la celda alrededor de cada una.
8. **Abrir el desagüe.** En el punto más bajo de cada contorno, borrar 3 mm de línea.

En el repujado (Acción 4), el punzón se detiene 3 mm antes de cerrar cada contorno.

## Lo que la anatomía no hace

- **No agrega motivos tiwanacotas.** Del monolito sigue entrando solo la celda.
- **No se inventa en cada letra.** Cada regla vale para todo el juego, y las reconstruidas la heredan de las partes de donde salen. La é y la ó llevan la gota de la á; la ü, los cuadrados de la i; el 0, el 6, el 8 y el 9, la bandeja de la o.
- **No borra el pie.** La mitad de arriba de cada ojo, las proporciones y la posición de cada trazo son las del archivo.

## La simulación

La máquina aplica estas reglas en `simulacion/anatomia.py`. El resultado está en `simulacion/informe.md` («La anatomía»), con dos láminas:

- `03c_anatomia.png`: seis letras con sus partes nombradas;
- `03d_antes_y_despues.png`: lo que dio el pie, la anatomía y el calco.

**Al ajustar la retícula,** la base pasó de 1,71 a 1,5 teselas y la altura de x, de 2,48 a 2,5. La pauta provisional de `03`, §3.6, ya proponía esas medidas.
