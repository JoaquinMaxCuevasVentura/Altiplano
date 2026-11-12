# El espécimen

Un espécimen muestra una letra. *Contenida* todavía no existe: la hacen las manos, placa por placa, desde el pie de la lámina (`../04_taller_analogico.md`, acciones 3 y 4). Por eso este espécimen **no compone texto con ella**. Muestra lo que ya hay:

- la caja y sus 56 celdas;
- las letras halladas en el pie;
- la celda y sus líneas;
- los estados en lugar de los pesos;
- la regla de componer con placas;
- y, rotulado, lo que propuso la máquina.

Donde irá la letra dice «por hacer: la mano». Cuando las placas existan, se rehace con ellas.

**Descarga:** [`contenida_especimen.pdf`](contenida_especimen.pdf), dieciséis páginas de 180 × 200 mm. Las vistas de cada página están en [`paginas/`](paginas/).

## Lo que se toma de los especímenes de referencia

Se toma la manera de presentar una familia, no sus páginas ni su letra:

- de *Monument Grotesk* (Dinamo Typefaces), la cabeza a máquina con la sección y el folio, y el cuadro de signos por categoría;
- de *Monopol* (Nguyen Gobber), la familia en filas con su rótulo, la ficha técnica en una tabla con filetes y el cuadro de signos con su rótulo al costado.

Los dos se citan, no se suben.

Lo propio sale del proyecto:

- **La página tiene la proporción de la celda:** 180 × 200 mm, 0,90. La retícula es la caja: 8 columnas por 7 filas de celdas de 18 × 20 mm, con juntas de 3 mm.
- **Estados, no pesos.** Donde un espécimen pone Light, Regular y Bold, este pone calco, placa, cinta, frotado, agua y voz. El peso se mide en frotadas.
- **Rasgos: decisiones.** Donde un espécimen muestra rasgos opcionales (alternativas, cifras), este muestra las 24 decisiones de anatomía de los planos.
- **El texto de muestra es el pie.** La lámina dice una sola cosa, su pie: va a máquina, con la primera aparición de cada signo hallado. Componer, aquí, es ordenar placas: cada verso es una fila de celdas con el número de su placa (la póliza).
- **Cada imagen dice qué es.** Como en el libro, la etiqueta dice si es una letra hallada en la lámina, una propuesta de la máquina (punteada) o algo por hacer por la mano. Todo marco se abre abajo, en su desagüe.

## Las páginas

| Pág. | Sección | Qué muestra |
|---|---|---|
| 1 | Portada | La caja de 8 × 7, vacía: la letra no está, está su caja. En la celda 1, la coma de «KOCHAMAMA,» |
| 2 | Qué es | La letra en cuatro párrafos, lo que hay y lo que no; abajo, el pie a máquina con lo hallado |
| 3 | Ficha técnica | Familia, estados, signos, caja, celda, líneas, trazo, placas, proporciones, formatos, uso, diseño |
| 4 | La celda · 1:1 | La placa de 150 mm a tamaño real, con la celda (0,90) y sus cuatro líneas: aquí va la placa de la mano |
| 5 | Estados, no pesos | La «a» en cada estado: la de la máquina, ya hecha; la de la mano, por hacer. Con el nombre propuesto de cada estilo |
| 6 | El peso: frotadas | La «a» frotada una y otra vez; cuántas frotadas resisten las halladas y las reconstruidas |
| 7 | La caja: lo hallado | Las 30 letras halladas en su celda, recortadas de la foto; a puntos, las 25 que faltan; el ¶ |
| 8 | La propuesta de la máquina | Los 55 cuerpos base de la gramática, rotulados: no es la letra |
| 9 | Anatomía | Los cuatro generadores y las 24 decisiones |
| 10 | De punta a punta | La «a» y la «z» por todos sus estados |
| 11 | Componer con placas | Tres versos del poema, celda por celda, con la placa que le toca a cada signo |
| 12 | La póliza | Las 119 placas: cuántas tiene cada signo |
| 13 | Las proporciones | La celda (0,90) y la altura de x (1,71): la foto de cámara y la lámina enderezada (plano P-11) |
| 14 | Las reglas | Lo que la letra no hace |
| 15 | Lo que falta | De la Acción 0 a rehacer este espécimen con las placas |
| 16 | Colofón | Cómo se hizo |

## Cómo se arma

Con [Typst](https://typst.app), que controla la página al milímetro y lee los datos del proyecto (la caja, la gramática, la póliza) tal como están:

```bash
pip install typst fonttools brotli pillow numpy pymupdf
python3 tipografia/especimen/armar.py
```

`armar.py` prepara en `.cache/`, que no entra en el repositorio:

- las fuentes en TTF, porque Typst no lee WOFF2;
- las letras halladas, recortadas de los testigos;
- los estados de la «a» y de la «z», recortados de sus cadenas;
- los datos.

Después compila `especimen.typ` con la raíz en `tipografia/` y deja el PDF y las vistas. La fecha del PDF es fija: rehacerlo con los mismos datos da el mismo archivo.

Con el programa `typst` en vez del paquete de Python, después de correr `armar.py` una vez:

```bash
typst compile --root tipografia --font-path tipografia/especimen/.cache/fuentes \
  tipografia/especimen/especimen.typ tipografia/especimen/contenida_especimen.pdf
```

Si cambian la caja, la gramática o la simulación, se vuelve a correr `armar.py`.

## Archivos

| Archivo | Qué es |
|---|---|
| `especimen.typ` | El espécimen: la retícula, las piezas (la cabeza, el marco con desagüe, las etiquetas) y las dieciséis páginas |
| `armar.py` | Prepara la caché y compila |
| `contenida_especimen.pdf` | El espécimen |
| `paginas/` | Una vista de cada página, a 72 ppp |

Hecho con asistencia de IA.
