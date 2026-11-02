# 04. El taller analógico: acciones

La obra de Rebeca se subtitula *acciones para desenterrar una voz*. *Contenida* se hace también con acciones. Cada acción lleva:

- el verso de tu poema que le corresponde;
- la decisión de la obra con la que rima (numerada como en `01`);
- los materiales, los pasos y lo que queda registrado.

Las acciones se documentan en tres cuadernos, como Tshuma documentó Isiko en tres libros. Sus nombres son verbos de la obra:

| Cuaderno | Acciones | Qué pasa |
|---|---|---|
| **1 · Desenterrar** | 0 a 3 | Pedir, medir, hallar las letras y calcarlas |
| **2 · Contener** | 4 a 7 | Repujar, llenar la caja, vestir y hacer el signo final |
| **3 · Devolver** | 8 a 12 | Copiar, mojar, dar voz, llevar a la pared, componer y cerrar |

Plantillas para imprimir al 100 %: `esquemas/plantillas_imprimibles.pdf` (pauta de calco, fichas y mapa de la caja).

---

## Cuaderno 1 · Desenterrar

### Acción 0 · Pedir

> «Vuelve sin que la llames.»

**Rima con:** la obra se hizo junto a otros (CreaciónxAcuerpamiento) y en un lugar prestado.

Antes de repujar la primera letra:

1. **Rebeca.** Mostrarle el proyecto; el resumen de `README.md` alcanza. Preguntarle:
   - si está de acuerdo;
   - si quiere participar, y cómo (por ejemplo, haciendo el signo final);
   - cómo quiere que se la nombre;
   - cuánto dura el bucle del video.
2. **CreaciónxAcuerpamiento.** Lo mismo: acuerdo y forma de crédito.
3. **Artefacto Tatuajes y la administración del edificio.** Permiso para medir, frotar y fotografiar la piscina y, más adelante, para componer y proyectar en ella.
4. **El estudio.** Preguntar si puede hacer los esténciles hectográficos (Acción 8) y en qué condiciones.

**Registro:** las respuestas, con fecha, al principio del cuaderno 1. Si Rebeca no está de acuerdo, el proyecto se detiene o cambia; no sigue igual.

### Acción 1 · Medir y frotar

> «Quedó el contenedor / de lo que ya no está.»

**Rima con:** D6 y D9 (la piscina como caja, pantalla y tema). Regla 9: de la piscina no se saca nada.

**Materiales:**

- cinta métrica y regla metálica;
- papel de seda o papel manteca en pliegos;
- grafito en barra o crayón de cera negro;
- cinta de pintor, que se pega al esmalte del azulejo y nunca a la junta;
- el celular.

**Pasos:**

1. **Medir** con la cinta métrica, en milímetros:
   - el lado de diez azulejos de pared distintos (anota cada uno y el promedio);
   - el ancho de la junta;
   - el lado de diez teselas del piso;
   - el largo y el alto de cada pared, contados en azulejos.
2. **Frotar** un paño de **8 × 7 azulejos** de la pared: papel encima, sujeto con cinta al esmalte, y el grafito pasado de plano, en una sola dirección. Salen las juntas, las grietas y los bordes gastados. Es la pauta definitiva.
3. **Frotar** también un paño del piso: es la pauta del cuerpo tesela.
4. **Fotografiar** los paños frotados antes de levantar el papel, con la regla metálica en cuadro.
5. **Regenerar** la pauta con las medidas reales:

   ```bash
   python3 tipografia/esquemas/generar_esquemas.py --azulejo 152 --teselas 6 --junta 3
   ```

   (Las cifras son un ejemplo: pon las que midas.)

**Registro:** las medidas, los frotados numerados y las fotos. No se despega, raspa ni limpia nada.

### Acción 2 · Desenterrar el pie

> «A la ídolo la desenterraron, / le pusieron nombre, / otra manera de enterrar.»

**Rima con:** D1 (partir del registro) y *Nedmural* (letras extraídas de una inscripción).

**Materiales:**

- el libro de la lámina;
- una lámpara de mesa;
- el celular sobre un soporte fijo;
- una regla pequeña;
- acceso a una fotocopiadora.

**Pasos:**

1. **Identificar el libro:** autor, título, año y página. Van al colofón.
2. **Fotografiar el pie con luz rasante.** La lámpara casi a ras del papel (10 a 15 grados), de un solo lado. La regla va en cuadro. Con esa luz se ve la huella del tipo en el papel, como se leen las inscripciones gastadas.
3. **Transcribir el pie letra por letra**, tildes incluidas, y corregir `textos/pie_de_lamina.txt`.
4. **Recontar:** `python3 tipografia/inventario.py`. Si cambian los números, cambian la caja y los esquemas: vuelve a correr también `generar_esquemas.py`.
5. **Ampliar.** Imprimir la foto y ampliarla en fotocopiadora, en generaciones sucesivas, hasta que la letra más alta y la más baja del pie quepan en el azulejo con media tesela de aire (`03`, §3.6). Con azulejos de 15 cm, la altura de x queda en unos 6 cm.
   - Corregir las líneas de la pauta con lo que resulte y regenerarla.
   - Numerar cada generación.
   - Cada una pierde detalle: es el «según viejas fotografías» del pie, repetido a propósito.
6. **Elegir un testigo por signo.** Donde hay varios (la «e» aparece 41 veces), elegir el mejor conservado y anotar la palabra y la línea. Donde hay uno solo («j», «k», «q», los paréntesis), ese es.

**Registro:** fotos, generaciones numeradas y, en cada ficha, la sección *Pie*.

### Acción 3 · Calcar y reconstruir

> «No se salvó la piedra, / solo la opinión sobre ella.»

**Rima con:** el dibujo reconstructivo de Posnansky, hecho desde fotos viejas.

**Materiales:**

- la pauta impresa o el frotado;
- papel de calco;
- lápiz HB y 2B;
- las ampliaciones.

**Pasos:**

1. **Poner el calco** sobre la ampliación, con la línea de base de la pauta sobre la del pie.
2. **Calcar el contorno, no el relleno**, como la lámina, que es un dibujo de línea.
   - Donde la tinta del pie se corrió, hay que decidir dónde está el borde. Esa decisión es la «opinión»: anótala si fue difícil.
3. **Lo hallado va en línea continua. Lo reconstruido, en punteado**, armado por analogía (lista en `03`, §3.4).
   - En la ficha se anota de qué letras sale cada parte.
4. **Si algo se sale del azulejo**, se deja salir y se anota (`03`, §3.6).
5. **Escanear** los 56 calcos (primer estilo: *Calco*).

**Registro:** en la ficha, *Calco* y, si corresponde, *Reconstrucción*.

---

## Cuaderno 2 · Contener

### Acción 4 · Repujar

> «de la boca sale un signo / hecho con las manos»

**Rima con:** D2 (asperón → aluminio) y D3 (placas sueltas).

**Materiales:**

- papel de aluminio de cocina, el mismo material de Rebeca, en hoja simple; si se rompe demasiado, doble;
- punzón de bola, o un bolígrafo sin tinta, o un palito de brocheta con la punta redondeada;
- base blanda: fieltro, goma eva, una pila de periódico o una alfombrilla de ratón;
- cinta de papel.

**Pasos:**

1. **Cortar la placa** del tamaño de un azulejo, con las esquinas redondeadas como la placa de la foto.
2. **Poner el calco en espejo.** Darlo vuelta, porque el repujado se trabaja por el reverso, y pegarlo con cinta sobre el reverso de la placa, que va apoyada en la base blanda.
3. **Repasar el contorno con el punzón.**
   - Lo hallado, con un trazo continuo.
   - Lo reconstruido, a puntos: el punteado queda en relieve para siempre.
4. **Retirar el calco y dar vuelta la placa.** Por el frente, la letra está al derecho y en relieve.
5. **Rellenar solo si hace falta.** Si una letra pide más cuerpo, se sube desde el reverso con el lado redondo del punzón, y se anota.
6. **El orden de trabajo:**
   - primero una placa por celda: 56;
   - después, el resto de la póliza hasta 119, en sesiones distintas, para que cada «a» sea de otro momento.
7. **Si se rompe:** la placa no se tira. Va a la ficha («roturas») y a la caja, junto a la que se hizo después.

**Tiempo:** es el grueso del trabajo. A 15-20 minutos por placa, 119 placas son entre 30 y 40 horas.

**Registro:** en la ficha, *Placa*. Cada placa se fotografía con luz rasante desde un lado fijo (la misma lámpara, a la misma altura y el mismo ángulo): segundo estilo, *Placa*.

### Acción 5 · Llenar la caja

> «ningún contenedor aguanta lo que contiene»

**Rima con:** D5 (la retícula de la cabeza) y D4 (las puertas).

**Materiales:**

- cartón gris grueso o terciado fino;
- cola;
- cúter;
- la lámina de la caja (`esquemas/caja_8x7.svg`).

**Pasos:**

1. **Armar una bandeja de 8 × 7 compartimentos** de un azulejo de lado, con paredes bajas.
2. **Cada placa va a su celda**, con su ficha, según el orden de `textos/inventario.md`.
3. **La tapa** lleva una sola puerta calada del tamaño de una celda, sobre la celda 1: con la caja cerrada se ve solo la coma.
4. **Fuera de la caja**, pegado en la tapa por dentro, el `.notdef`: la celda de la lámina calcada a mano.

### Acción 6 · Vestir

> «Moverse como se mueve la piedra, / es decir, apenas, es decir, temblor, / es decir, un presente continuo.»

**Rima con:** D3 (placas sobre el cuerpo) y D11 (moverse como la piedra).

**Materiales:**

- esparadrapo de papel (del que no irrita);
- ropa lisa o piel, según quien vista;
- la lámpara de la Acción 4.

**Pasos:**

1. **Elegir qué se viste.** A 15 cm por letra, un cuerpo lleva una palabra o un verso corto: «voz», «ninguna igual».
   - Para que el estilo *Piel* tenga todas sus letras, las 56 placas de la primera tanda se visten, en varias sesiones.
   - Las demás placas de la póliza se visten si se puede: son variantes.
2. **Quién viste** lo decide la persona, que da su acuerdo por escrito en el cuaderno. Puede ser quien hace el proyecto. Nunca el cuerpo de Rebeca, salvo que ella lo proponga.
3. **Fijar las placas** con esparadrapo, dejando piel o tela a la vista entre ellas.
   - Ninguna placa va sobre la cara, la boca o la nariz: la obra tapó ojos y boca, y el proyecto no repite ese gesto.
   - Cuidado con los bordes del aluminio, que cortan.
4. **Moverse apenas** durante lo que dura un bucle del video: el dato se le pide a Rebeca en la Acción 0. Si no se consigue, un tiempo elegido y anotado.
5. **Retirar las placas y aplanarlas solo con la palma.** No se plancha ni se prensa: los pliegues son el registro.
6. **Fotografiar** cada placa con la misma luz rasante de la Acción 4: tercer estilo, *Piel*.

**Registro:** en la ficha, *Piel*: quién, cuánto tiempo, dónde.

### Acción 7 · El signo final

> «Al final del ciclo, / de la boca sale un signo / hecho con las manos, / ninguna palabra, / acciones del cuerpo.»

**Rima con:** D13 (la placa que sale de la boca).

1. **Se le propone a Rebeca** que haga el signo final: una placa trabajada solo con los dedos, sin punzón. La forma la decide quien la hace.
2. **Si ella no quiere**, lo hace quien compone, y así se anota.
3. **Va a la celda 56.** Es el único signo de la caja que no se halló ni se reconstruyó.

---

## Cuaderno 3 · Devolver

### Acción 8 · Hectografiar

> «La tierra se dio de beber a sí misma / y ningún contenedor aguanta lo que contiene.»

**Rima con:**

- la bandeja baja de la proyección (D8);
- el líquido que la boca no retiene (D16);
- el estudio de tatuajes (D6): el esténcil de tatuaje es hectográfico;
- «cada paso pierde materia y gana luz».

**El hectógrafo.** Es un duplicador de gelatina: una bandeja baja de gelatina con glicerina. La matriz, escrita con tinta de anilina, se apoya boca abajo y la gelatina absorbe la tinta. Después, cada hoja que se apoya se lleva un poco: salen decenas de copias, cada una más clara que la anterior. La tinta que queda se hunde en la gelatina, que a los uno o dos días está limpia otra vez. Se bebe la matriz y vuelve a empezar.

**Materiales:**

- una asadera o bandeja metálica baja, de unos 25 × 35 cm;
- gelatina sin sabor y glicerina líquida (de farmacia);
- guantes;
- papel bond;
- una matriz, de una de estas dos formas:
  - **a) En el estudio:** una impresión en alto contraste de las fotos de las 56 placas en su estado *Piel*, dispuestas como la caja en cuerpo tesela (cabe en una A4), pasada por la máquina de esténcil térmico.
  - **b) A mano:** la misma disposición calcada con lápiz tinta (lápiz copiativo) o lápiz hectográfico. No se moja con la lengua, como se hacía antes: la anilina es tóxica. Se moja con un pincel húmedo.

**Receta de partida** (hay que probarla y anotar los cambios):

1. Hidratar 2 sobres de gelatina sin sabor (unos 15 g) en media taza de agua fría.
2. Disolver a fuego bajo, sin hervir, con una taza de glicerina.
3. Verter en la bandeja hasta 1,5-2 cm de alto, reventar las burbujas y dejar cuajar 24 horas.

**Pasos:**

1. **Transferir la matriz.** Humedecer apenas la gelatina con una esponja, apoyar la matriz boca abajo 1-2 minutos y retirarla.
2. **Sacar copias.** Apoyar una hoja, pasar la mano sin presionar de más y levantarla: copia 1. Seguir hasta que la caja no se lea más.
3. **Numerar** cada copia a lápiz, en el reverso.
4. **Dejar que la bandeja beba.** Sin lavarla, en uno o dos días la tinta se hunde y la gelatina queda lista.

Si el esténcil térmico no transfiere bien a la gelatina, probar la matriz a mano: los dos caminos se prueban antes de la tirada.

**Registro:** las copias numeradas son el estilo *Copia 01 … Copia n*. En cada ficha va el número de la última copia en que ese signo todavía se lee: algunos se borran antes que otros.

**Seguridad:** guantes, ventilación, y la bandeja y los utensilios no vuelven a la cocina.

### Acción 9 · Pasar por el agua

> «Tocas el agua y la diosa se deforma. / Todos los archivos funcionan así.»

**Rima con:** D8 (la proyección a través de la bandeja) y D15 (tocar el agua).

**Materiales** (esquema A en `esquemas/montajes_con_agua.svg`):

- una bandeja un poco más grande que una placa;
- agua;
- una lámpara LED a pilas o una linterna, con celofán verde delante: el verde es luz, no tinta;
- dos o tres azulejos sueltos parecidos a los de la piscina, o el frotado de la pared pegado en un cartón;
- el celular.

**Pasos:**

1. **Preparar el reflejo.** En un cuarto oscuro, poner la placa en el fondo de la bandeja con un dedo de agua (1,5 cm). Pasan por el agua las 56 placas de la primera tanda, una por vez; las demás, si se puede.
2. **Iluminar.** La lámpara, a unos 30 grados, apunta a la placa. El reflejo sube hacia los azulejos y la letra llega temblando y al revés.
   - Puede llegar legible o como pura luz: las dos cosas se registran.
3. **Fotografiar con el agua quieta**: *Agua quieta*.
4. **Tocar el agua con un dedo, en una esquina**, y hacer varias fotos seguidas. Ninguna sale igual: *Agua tocada*.

**Registro:** en la ficha, *Agua*, con el número de foto.

**Seguridad:** nada con enchufe junto al agua.

### Acción 10 · Dar voz

> «Y es que lo que vuelve, vuelve escrito; / pocas veces vuelve hablado.»

**Rima con:** D14 (el canto que se oye y no se entiende) y la tipografía sonora de Mahendran.

**Materiales** (esquema B):

- el montaje de la Acción 9;
- un parlante pequeño a pilas dentro de una bolsa plástica;
- tu voz leyendo el poema, grabada por ti.

**Pasos:**

1. **Poner la bandeja sobre el parlante**, con el volumen bajo.
2. **Reproducir tu lectura.** El agua vibra y la letra reflejada se deshace en ondas.
3. **Fotografiar** y anotar qué verso sonaba en cada foto: *Voz*.

**La grabación no se publica ni entra en el espécimen.** Solo queda lo que la voz le hizo al agua: «no tiene lengua pero igual dice».

### Acción 11 · Llegar a la pared y componer

> «Cada vuelta pasa por el agua / y el agua no repite, / la misma diosa dos veces / y ninguna igual.»

**Rima con:** D9 (la piscina es escenario, pantalla y tema), D7 (placas en el fondo) y D10 (el bucle).

En la piscina, con permiso:

1. ***Azulejo*.** Al atardecer, montar la Acción 9 frente a la pared de la piscina. La letra cae sobre los azulejos verdaderos, en trapecio y cortada por las juntas.
   - Fotografiarla.
   - Después, calcar sobre el frotado lo que quedó: dónde la cortan las juntas y cuánto se abre el trapecio. Es el último estilo, *Azulejo*.
2. **Componer.** Un verso por vez:
   - en el fondo, con las placas apoyadas sin nada que las pegue;
   - o en la pared, con cinta de pintor sobre el esmalte, nunca sobre la junta.

   Una placa por azulejo, un azulejo vacío entre palabras. Si la pared no alcanza (el verso más largo ocupa 44 azulejos, contando los espacios), el verso dobla la esquina.
3. **Fotografiar** el verso compuesto.
4. **Distribuir.** Devolver cada placa a su celda: en la imprenta, *distribuir* es devolver los tipos a la caja.
5. **Siguiente verso.** Componer, registrar y distribuir: «termina y empieza».
6. **Al irse**, no queda nada pegado ni nada se llevó.

### Acción 12 · Cerrar la caja

> «Nos fuimos con las manos secas, / que es como se sale de todas las ruinas.»

1. Completar las 119 fichas.
2. Escribir el colofón de manos (`03`, §3.11) con los nombres que se hayan confirmado.
3. Fotografiar la caja abierta y cerrada.
4. Revisar la lista de `05`, §5.1, y decidir si el proyecto migra a lo digital o termina aquí.

---

## Materiales, todo junto

| Material | Para qué | Dónde |
|---|---|---|
| Papel de aluminio de cocina (unos 3 m²) | Placas | Mercado o supermercado |
| Punzón de bola o bolígrafo sin tinta | Repujado | Librería o bazar |
| Fieltro o goma eva | Base del repujado | Librería |
| Papel de calco, papel de seda o manteca, bond | Calcos, frotados y copias | Librería |
| Grafito en barra o crayón de cera | Frotados | Librería de arte |
| Cinta de pintor y esparadrapo de papel | Fijar sin dejar marca | Ferretería y farmacia |
| Cartón gris o terciado, cola y cúter | La caja | Librería o barraca |
| Gelatina sin sabor y glicerina | Hectógrafo | Supermercado y farmacia |
| Lápiz tinta, lápiz hectográfico o esténcil térmico | Matriz | Librería antigua o el estudio |
| Guantes | Tinta de anilina | Farmacia |
| Bandejas bajas (dos) | Hectógrafo y agua | Bazar |
| Lámpara LED a pilas y celofán verde | Luz rasante y reflejo | Ferretería y librería |
| Parlante a pilas y bolsa plástica | Voz | — |
| Cinta métrica y regla metálica | Medir | Ferretería |

## Seguridad, todo junto

- **Electricidad:** nada con enchufe sobre el agua ni al lado de la bandeja.
- **Anilinas** (lápiz tinta, tinta hectográfica): guantes y ventilación. No se lleva nada a la boca. Los utensilios no vuelven a la cocina.
- **Aluminio:** los bordes cortan. Redondear las esquinas y cuidar la piel al vestir.
- **Cuerpo:** acuerdo escrito de quien viste. Nada sobre la cara, la boca ni la nariz.
- **Piscina:** permiso escrito. No se despega, raspa, pinta ni pega nada fuera del esmalte, y no queda nada al irse.
