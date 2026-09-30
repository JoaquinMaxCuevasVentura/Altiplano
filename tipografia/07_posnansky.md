# 07. Lo que se rescata del libro de Posnansky

**El libro:** Arthur Posnansky, *Tihuanacu, la cuna del hombre americano / Tihuanacu, the Cradle of American Man*, tomo I. Nueva York: J. J. Augustin, 1945. Traducción inglesa de James F. Shearer. Edición bilingüe: inglés a la izquierda, castellano a la derecha. En la tapa del ejemplar escaneado se lee «Obra custodiada por el Archivo y Biblioteca Nacionales de Bolivia».

**Lo que se leyó:** un PDF de 72 páginas escaneadas. Trae las portadillas, el índice completo del tomo I y las páginas 1 a 62: prólogos y capítulos I a V. El texto se leyó con reconocimiento óptico de caracteres y se cotejó a la vista en los pasajes citados. **El PDF no se sube al repositorio**, ni nada de él.

## 1. Lo que no se toma

Posnansky es la voz del archivo. El pie de la lámina lo cita en tercera persona: «EL IDOLO KOCHAMAMA, según Posnansky». No es una autoridad para el proyecto, y hay tres cosas que no entran:

- **Su cronología.** Da a Tiwanaku una antigüedad de miles de años más de la que acepta la arqueología de hoy.
- **Su tesis del título.** Tiwanaku como «cuna del hombre americano».
- **Su lectura racial de la historia.** Los «inteligentes Khollas» que someten a las «hordas Aruwakes» (p. 51), las razas y los cráneos (cap. IV).

Tampoco se usan sus lecturas de los signos como significados (cap. IX a XI). Lo que se dijo en `06` sigue valiendo: el proyecto no interpreta la iconografía.

## 2. Lo que se toma

| Lo que dice | Dónde | Qué rima con la obra y con *Contenida* |
|---|---|---|
| «Durante siglos enteros estos monumentos fueron objeto de saqueo para aprovechar sus materiales en la construcción de casas, templos […], puentes, etc., lo mismo en La Paz que en otros lugares.» Con piedra de Tiwanaku, Alonso de Mendoza edificó «la primera parte de la nueva ciudad de La Paz» | p. 59 | **La Paz contiene la ruina.** La obra ocurrió en La Paz: *Contener una ruina* es también un hecho de la ciudad, que tiene la ruina en sus muros |
| «Las hermosas losas de la cloaca máxima sirven hoy de pavimento en la plaza del pueblo» | p. 60 | **El desagüe hecho piso.** Las losas del desagüe de Tiwanaku terminaron como piso de una plaza, y los azulejos de la piscina, como piso de una obra. El desagüe de *Contenida* tiene un antecedente monumental: el índice anuncia «La cloaca máxima, un “overflow”», en Akapana (cap. VI, pp. 74-76) |
| El lago «se extendió hasta los mismos alrededores de la metrópoli»; los muelles de sus puertos «son visibles actualmente» | p. 25 y pp. 33-34 | **El agua que se fue.** Es una hipótesis de Posnansky, discutida. Pero es la imagen de la obra: un lugar hecho para el agua, del que el agua se retiró. La piscina vacía, a escala de un lago |
| Piedras hundidas en el lago que, «cuando el lago se retiró aparecieron, lavando entonces la lluvia el lodo que cubría su superficie»; otras siguen «cubiertas por las verduzcas olas del lago» | p. 35 | **La lluvia y el verde.** La lluvia que lava la piedra, como la intemperie de la gramática. Las olas verdosas, como la luz verde de la proyección |
| El río Desaguadero, que desagua el Titicaca, «en la actualidad no tiene agua», por la bajante del lago | p. 40 | **El desagüe tiene nombre de río.** El lago de la «madre del agua» se vacía por un desaguadero |
| Los primeros constructores eligieron «el material más blando y el que menor resistencia ofreciera a sus primitivos utensilios de piedra y hueso»: el asperón colorado de la serranía de Quimzachata | p. 51 | **La forma la decide el material.** Es la regla 3 de `03`, dicha por el propio archivo: el asperón elegido por blando, como el aluminio de cocina que cede al punzón |
| «Chuki-pajcha», en aymara, «chorrera de oro», el nombre de unas ruinas vecinas | p. 62, n. 59 | **La chorrera.** El líquido que chorrea de la boca (D16) y la gota de la gramática. Se registra como rima; no se usa como nombre (`03`, §3.1) |
| Cieza de León vio en 1540 murallas «hoy ya desaparecidas», que el arqueólogo solo puede reconstruir «mediante el levantamiento de planos topográficos» | p. 59 | **Lo que no está se reconstruye.** Es la condición del pie de la lámina, y la del punteado |
| El índice del tomo I: «El signo escalonado» (pp. 102-110), «El signo “Pez”» (pp. 119-121), «El signo “Boca”» (pp. 124-125), «Dos ídolos del I período» (pp. 76-79) | pp. vi-vii | **Dónde buscar.** Para verificar el signo «pez» del cuerpo de la Kochamama hay que leer las pp. 119-121, que no están en el PDF |
| Edición bilingüe, en dos columnas enfrentadas | todo el libro | **Un doble opuesto con variaciones.** Las dos columnas dicen lo mismo, pero nunca igual |

**Lo que falta del libro.** La lámina de la Kochamama está en el tomo II: Posnansky 1945, vol. 2, figs. 100, 101a, 101b y 102a, según Agüero, Uribe y Berenguer (2003). Tampoco se tiene todavía el libro de donde salió la lámina de Rebeca, el que la cita «según Posnansky».

## 3. El testigo: lo que se probó y lo que quedó

**Se probó la letra del libro.** El libro está compuesto en una letra de imprenta de 1945 y en el escaneo su altura de x mide unos 22 px. Alcanzaba para medir. Pero no es la letra del pie de la lámina, y se descartó: el testigo tiene que salir del pie mismo, no de otro libro del mismo archivo.

**Se probó la foto del pie.** Con una foto cercana de la lámina (el pie en cuatro líneas, con el papel doblado: la tercera línea sube sobre el pliegue), `simulacion/extraer_testigos.py` endereza cada línea, reparte la tinta entre líneas donde se tocan, deshace en parte el desenfoque y corta cada palabra en sus letras. Las 336 letras quedan en `simulacion/testigos/`, sin la foto.

- **Lo que la foto da:** medidas. La altura de x mide 11,7 px; las ascendentes, 1,71 veces la altura de x; las descendentes, 0,43. El trazo mide al menos 0,19 de la altura de x. El desenfoque de la foto es de σ = 1,66 px, medido en 57 trazos aislados. El trazo se mide por la tinta que junta, no por su borde: el desenfoque corre la tinta, pero no cambia cuánta hay.
- **Lo que no da:** formas. A esa escala la tinta corrida cierra los ojos de la a y de la e, y los testigos que salen son manchas. Una gramática armada con ellos tiene letras más pesadas y torpes.

**La decisión.** Las formas del testigo siguen saliendo de la letra sustituta (Liberation Serif, impresa con tipos de plomo simulados). De la foto se toma una sola cosa: **la altura de x, más baja**. La zona de x de cada testigo se achata hasta que las ascendentes miden 1,71 veces la altura de x, como en el pie real. La base, la línea de afuera y la de desagüe no se mueven. En la placa, la altura de x pasa de 62 a 55 mm.

Lo demás que la foto mide (descendentes más cortas, trazo más grueso) queda escrito en `simulacion/informe.md`, en *Lo que dice la foto*, para confrontarlo con la mano.

**Qué se guarda en el repositorio:** letras sueltas, no la foto.
