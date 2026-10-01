# 20. Prompts para llevar los diagramas al estilo de tus referencias

> **Actualización (1 de octubre de 2026).** Las Figuras 7 y 8 se rehicieron como notaciones (`21_diagramas_como_notaciones.md`), y las guías se regeneraron desde ellas: la de la Figura 8 ahora es vertical (1024 × 1536). Siguen valiendo el bloque de estilo (§20.6), los materiales (§20.3), las correcciones (§20.9), qué mirar (§20.10) y los cuidados (§20.11). Para la composición, usa los prompts de `21`, §21.8, en lugar de los de §§20.7-20.8, que describen la versión anterior.

El 30 de septiembre de 2026 pediste prompts para que, a partir de los diagramas, GPT Image 2 llegue de verdad al estilo de tus cinco imágenes de referencia (17 a 21). Reemplazan los de `19`, §19.8.

**En corto:**

- **Por qué los primeros prompts no bastaban** (§20.1):
  - la guía era la figura del artículo, y el modelo copiaría su trazo grueso y su letra;
  - el estilo de tus referencias no es solo una línea: también es aire, un aparato de órbitas y ejes, una leyenda al margen y materiales reales.
- **Dos guías nuevas, sin texto** (§20.4), en `esquemas/guias/`:
  - tienen línea fina y los materiales marcados;
  - se generan con el mismo programa que las figuras, así que coinciden con ellas.
- **Un bloque de estilo** que nombra, rasgo por rasgo, el lenguaje de tus referencias (§§20.2 y 20.6).
- **Dos prompts por figura** (§§20.7 y 20.8):
  - **A**, fiel a la guía;
  - **B**, una notación abierta, más cerca de las referencias.
- **Los materiales, por lo que son** (§20.3), como pediste para los pasteles: tierra siena, alquitrán, pan de oro, papel, grafito, hoja de plata.
- **Correcciones cortas** para una segunda vuelta (§20.9) y **qué mirar** en el resultado (§20.10).
- **Sigue siendo exploración.** No se publica, y en los prompts no se nombra a ningún artista (§20.11).

## 20.1. Por qué los prompts de §19.8 no bastaban

1. **La guía empujaba en contra.** La figura del artículo tiene trazo de marcador tembloroso, letra Caveat grande y rótulos por todas partes. GPT Image 2 toma mucho de la imagen que recibe, y eso es lo contrario de tus referencias, que tienen línea finísima, letra diminuta y aire.
2. **El estilo de tus referencias es una manera de componer:**
   - el dibujo ocupa poco más de la mitad de la hoja;
   - los objetos flotan, cada uno con sus órbitas y su eje;
   - las flechas llevan el rótulo en la punta;
   - una leyenda en columna ocupa un margen.

   Si solo se cambia la línea, sale una infografía prolija, no una notación.
3. **La materia es parte del estilo:** el pan de oro y la hoja de plata de 18, la acuarela que se acumula en los bordes de 20, las formas planas de color y la silueta negra de 21. El bloque anterior pedía «un solo acento de color», y eso deja fuera lo que hace que esas hojas se vean como obra y no como esquema.

## 20.2. El lenguaje de tus referencias, rasgo por rasgo

| Rasgo | Dónde se ve | Cómo pedirlo |
|---|---|---|
| Aire | 18, 20 y 21 | «El dibujo ocupa poco más de la mitad de la hoja; el resto es blanco, con márgenes amplios» |
| Línea | Todas | «Finísima y segura: grafito duro gris claro y tinta negra de 0,1 a 0,3 mm; nada de trazo grueso ni tembloroso» |
| Rectas con regla, curvas a mano | 18, 20 y 21 | «Las rectas largas, con regla; las elipses, a mano alzada, fluidas, a veces abiertas o repasadas» |
| Órbitas y ejes | 18 y 21 | «Alrededor de cada objeto, dos o tres elipses finas en perspectiva, atravesadas por un eje vertical con una punta de flecha arriba» |
| Flecha con rótulo en la punta | 18 y 20 | «Flechas rectas largas que terminan en una punta mínima o en una "x", con el rótulo escrito en la punta» |
| Escritura | 18, 20 y 21 | «Letra diminuta (2 a 3 mm), cursiva e inclinada, a lápiz, escrita a lo largo de las líneas, a veces girada; algunas palabras subrayadas» |
| Leyenda al margen | 18, 20 y 21 | «En un margen, una leyenda en columna, escrita a mano, con un corchete» |
| Haz de líneas que se doblan | 20 | «Un haz de líneas finas paralelas que se doblan juntas, como estratos» |
| Cantidad hecha de marcas | 17 | «Lo que es mucho se dibuja con muchas marcas diminutas repetidas que siguen trayectorias y se amontonan» |
| Materia | 18, 20 y 21 | «Pan de oro u hoja de plata, planos, recortados y pegados, con arrugas finas; pigmento en polvo; tinta densa; recortes de papel» |
| Silueta negra | 21 | «Una silueta negra plana y pesada, el contrapeso de la hoja» |
| Signos negros de arquitectura | 17 | «Una rueda dentada, una doble flecha negra, losas en sección con líneas dobles finas» |
| Líneas de construcción | 17 | «Quedan a la vista, muy tenues, proyecciones verticales, un arco de compás, una línea de fuga» |
| Palabra-eje en el borde | 19 | «En el extremo del eje, una sola palabra en mayúsculas finas» |
| Obra fotografiada | Todas | «Una obra sobre papel fotografiada de frente, con luz pareja y el grano del papel apenas visible» |

## 20.3. Los materiales, por lo que son

El criterio es el de `17`, §17.3: el material se elige por lo que es y hace, no por lo que un color «significa».

| Elemento | Material | Qué hace | Figura |
|---|---|---|---|
| Relleno de la muralla, la «piedrecilla menuda» (p. 8) | Tierra siena en polvo | Óxido de hierro, mate y granuloso: la misma tierra del adobe | 7 |
| Foso «hondo y alquitranado» (p. 157) | Tinta negra densa con brillo de betún | El alquitrán absorbe la luz y apenas brilla. El raspado lo abre hasta el papel: más de ciento cincuenta marcas claras | 7 |
| Horizonte, «lo pasado antiguo» (p. 156) | Una tira delgada de pan de oro | Es un metal batido hasta volverse piel: refleja la luz y no deja ver adentro. Es la superficie que mira la memoria (lectura propia; §20.11) | 7 |
| «Montaña de piedras» (p. 9) | Tierra siena | La misma del relleno | 8 |
| «Montón de papeles y libracos» (p. 103) | Recortes de papel marfil | El papel es papel | 8 |
| Desmonte, roca sin mineral (p. 140) | Grafito gris plomizo | Carbono mineral, mate. En la novela el camino del desmonte es «tierra plomiza» (p. 140) | 8 |
| Estaño (p. 142) | Hoja de plata o de aluminio | El estaño es un metal blanco plateado: lo único que brilla sale de la mina, hacia la compañía | 8 |
| Castillete (pp. 134-135) | Tinta negra plana o papel negro recortado | La torre de acero; la masa más pesada de la hoja, como la silueta negra de 21 | 8 |
| Animales del radio urbano (p. 102) | Recortes planos de lana parda | La lana sin teñir de la paleta de `17` | 8 |

## 20.4. Las guías

| Guía | Qué tiene |
|---|---|
| `esquemas/guias/guia_fig7_memoria_retorno.png` (1536 × 1024) | La sección de la Figura 7 con línea fina. Lleva tierra siena en el relleno, un foso negro con 150 marcas raspadas y una tira de oro en el horizonte. El suelo es un haz de líneas que se dobla en el foso |
| `esquemas/guias/guia_fig8_tres_montones.png` (1536 × 1024) | Las tres estaciones de la Figura 8. Cada montón tiene su material, sus órbitas y su eje, y una línea larga los une. El castillete es una silueta negra con doble flecha; el estaño, una tira de plata; los animales, siluetas pardas; el embudo, una boca elíptica |

- **Sin texto,** para que el modelo no copie letras. Las flechas que quedan sin rótulo marcan dónde va cada palabra, y el prompt lo dice.
- **Con aire alrededor:** el dibujo ocupa cerca del 80 % del ancho, con márgenes para la leyenda.
- **Para regenerarlas:** `node analisis/esquemas/diagramas/generar_diagramas.js` y después `python3 analisis/esquemas/guias/generar_guias.py`. Las figuras del artículo no cambian: salen idénticas byte por byte.

## 20.5. Cómo usarlas con GPT Image 2

1. **Qué adjuntar, en este orden** (tres o cuatro imágenes; más, diluyen el estilo):

   | | Figura 7 | Figura 8 |
   |---|---|---|
   | 1.ª: la guía | `guia_fig7_memoria_retorno.png` | `guia_fig8_tres_montones.png` |
   | 2.ª: estilo | Tu referencia 20 (el horizonte) | Tu referencia 21 (el inventario en órbita) |
   | 3.ª: estilo | Tu referencia 17 (la arquitectura y las bandadas) | Tu referencia 18 (las estaciones y el pan de oro) |
   | 4.ª: opcional | Tu referencia 19 (la palabra-eje) | Tu referencia 17 (el embudo, la rueda, las marcas) |

2. **Qué escribir:** el bloque de estilo (§20.6) y, debajo, el prompt de la figura (§20.7 o §20.8).
3. **Tamaño:** 1536 × 1024, apaisado. **Calidad:** alta.
4. **El texto.** GPT Image 2 escribe bien, pero la letra diminuta y cursiva en castellano se le puede torcer. Los rótulos van cortos y literales. Si salen mal:
   - corrígelos uno por uno con una segunda vuelta (§20.9);
   - o pide la versión sin texto y escríbelos tú.
5. **El orden de las pruebas:**
   - primero la variante A, para ver el estilo sobre la composición conocida;
   - después la B, para ver cuánto cambia la composición cuando el estilo manda.

   Cambia una sola cosa por vez.

## 20.6. El bloque de estilo (va primero en los dos)

> **Estilo.** Una obra sobre papel fotografiada de frente, con luz pareja: papel de algodón blanco, grueso, con su grano apenas visible. Es una notación, no una ilustración: un diagrama de pensamiento dibujado a mano, con precisión y calma. El dibujo ocupa poco más de la mitad de la hoja; el resto es aire, con márgenes amplios.
>
> **Línea.** Finísima y segura: grafito duro gris claro y tinta negra de 0,1 a 0,3 mm. Las rectas largas se trazan con regla y terminan en una punta de flecha mínima o en una pequeña «x». Las curvas y las elipses se hacen a mano alzada, fluidas, a veces abiertas o repasadas dos veces. Nada de trazo grueso, tembloroso o de marcador.
>
> **Órbitas y ejes.** Alrededor de los objetos principales, dos o tres elipses finas en perspectiva, como órbitas, atravesadas por un eje vertical delgado con una punta de flecha arriba.
>
> **Escritura.** Letra manuscrita diminuta, de 2 a 3 mm, cursiva e inclinada, a lápiz, escrita a lo largo de las líneas o en la punta de las flechas, a veces girada para seguir la línea. Algunas palabras subrayadas. En un margen, una leyenda en columna escrita a mano, con un corchete. Toda la escritura va en castellano, con tildes. Copia literalmente los rótulos que se indican y no agregues otros.
>
> **Cantidad.** Lo que es mucho se dibuja con muchas marcas diminutas repetidas (puntos, piedritas, rayitas) que siguen trayectorias y se amontonan; nunca con números.
>
> **Materia.** Pocos acentos, y cada uno de un material real con cuerpo: pigmento de tierra siena, mate y granuloso; pan de oro u hoja de plata, planos, recortados y pegados, con arrugas finas y bordes irregulares; tinta negra densa; recortes de papel. Todo lo demás es gris de grafito sobre blanco.
>
> **Construcción.** Quedan a la vista, muy tenues, algunas líneas de construcción: proyecciones verticales, un arco de compás, una línea de fuga.
>
> **Imágenes adjuntas.** La primera es la guía: respeta la posición, el tamaño y el material de cada elemento, pero no su aspecto digital. Las demás son referencias de estilo: toma de ellas solo la manera de dibujar, de escribir y de usar el material, no su contenido, sus formas ni sus palabras.
>
> **Prohibido:** firma, fecha, nombres de artistas, cualquier palabra en alemán o en inglés. Tampoco: aspecto de infografía, de ilustración vectorial, de pizarra o de *sketchnote*; sombras, volumen 3D o degradados digitales; papel envejecido o manchado; figuras humanas con rostro; llenar la hoja.

## 20.7. Figura 7: *La memoria del retorno*

**Variante A: fiel a la guía**

> **Figura 7: la memoria del retorno, en sección.** Una sección de terreno vista de lado, en la hoja apaisada, con los elementos donde están en la guía.
>
> - **A la izquierda, la atalaya:** una torre estrecha de piedras apiladas, dibujada con línea fina, como un fragmento de arquitectura en sección. Arriba, siete marcas mínimas en fila, las personas que miran a la derecha.
> - **La mirada:** desde ellas sale una línea de trazos, recta y hecha con regla, que cruza la hoja a la altura de los ojos. En el borde derecho termina en una tira delgada de pan de oro, plana y con arrugas finas: el horizonte.
> - **En el medio, la muralla:** una pirca de doble cara en sección, dos columnas de piedras grandes con línea fina. Entre las dos caras va el relleno: una bandada apretada de piedritas diminutas de tierra siena, mate, como polvo de adobe. Una flecha fina en siena entra en el relleno desde arriba a la derecha.
> - **Más allá de la muralla, el foso:** una zanja honda cortada en el suelo, llena de tinta negra densa con un brillo leve de alquitrán. Dentro del negro, más de ciento cincuenta marcas diminutas raspadas hasta el papel, claras, como un esgrafiado. Son marcas, no figuras.
> - **La mirada que no baja:** sobre el foso, desde la línea de la mirada baja una línea de puntos que se detiene en una barra corta, lejos del foso.
> - **El suelo:** un haz de tres o cuatro líneas finas paralelas que siguen el terreno y se doblan juntas hacia abajo en el foso, como estratos.
> - **Abajo, un eje:** una recta larga con tres marcas y una punta de flecha a la derecha; en su extremo, en mayúsculas finas: TIEMPO. Dos proyecciones verticales tenues bajan al eje desde la atalaya y desde el foso.
>
> **Rótulos** (copia exactamente estas palabras):
> - junto a la atalaya: «atalaya de la esperanza (157)»;
> - a lo largo de la línea de la mirada: «sólo miraban el horizonte (157)»;
> - sobre la tira de oro: «horizonte» y, debajo, «lo pasado antiguo (156)»;
> - a lo largo del borde de la muralla: «muralla de su visión (156-157)»;
> - en el extremo de la flecha siena: «relleno: la legión sin tierra»;
> - en el extremo libre de la flecha que sube desde abajo a la izquierda hasta la base de la muralla: «caras: los que vuelven (156)»;
> - junto a la línea de puntos: «sin atreverse a bajar la cabeza (157)»;
> - encima del foso: «foso hondo y alquitranado (157)»;
> - bajo las marcas del eje, de izquierda a derecha: «ahora», «el hambre», «antes».
>
> **Leyenda,** en columna, en el margen inferior izquierdo:
> - «( ) páginas de la novela»
> - «caras: Villca, Huanca, Huallpa, Yupanqui, Ticona, Choque, Chuquihuanca (156)»
> - «relleno: Condori, Mamani, Quispe (22); tres vigilantes (75)»
> - «foso: más de ciento cincuenta muertos (156)»

**Variante B: notación abierta**

> **Figura 7, como notación abierta.** La misma sección, más pequeña y con más aire: ocupa la franja central de la hoja y deja arriba y abajo grandes márgenes vacíos. Todo flota sobre el blanco; del suelo solo queda el haz de líneas finas que se dobla en el foso.
>
> - **La línea de la mirada es el eje de la hoja:** una recta de trazos que va de borde a borde, como un horizonte dibujado. Tiene tres posiciones marcadas con pequeñas cruces: la atalaya, el foso y la tira de pan de oro.
> - **El resto, como en la guía:**
>   - la atalaya, pequeña y en sección;
>   - la muralla de doble cara con su relleno de tierra siena;
>   - el foso negro con sus marcas raspadas;
>   - la línea de puntos que no baja.
> - **Las flechas finas llevan el rótulo en la punta.** Los rótulos se escriben a lo largo de las líneas, girados si hace falta.
> - **Abajo, el eje del tiempo,** muy tenue, con la palabra TIEMPO en su extremo.
>
> **Rótulos:** «atalaya de la esperanza (157)», «sólo miraban el horizonte (157)», «horizonte», «lo pasado antiguo (156)», «muralla de su visión (156-157)», «relleno», «foso hondo y alquitranado (157)», «sin atreverse a bajar la cabeza (157)», «ahora», «el hambre», «antes».
>
> **Leyenda,** en columna, con un corchete, en el margen izquierdo: la misma de la variante A.

## 20.8. Figura 8: *Tres montones*

**Variante A: fiel a la guía**

> **Figura 8: tres montones.** Tres estaciones iguales, en fila sobre una misma línea de suelo, con los elementos donde están en la guía.
>
> - **Todas tienen el mismo aparato:**
>   - en el centro, un montón bajo y ancho hecho de muchas piezas diminutas;
>   - alrededor, dos órbitas elípticas finas en perspectiva;
>   - un eje vertical delgado que lo atraviesa, con una punta de flecha arriba.
> - **Cada montón es de un material:**
>   - a la izquierda, piedritas de tierra siena, mate y granulosa;
>   - en el medio, recortes diminutos de papel marfil, algunos con una línea, como hojas y libros;
>   - a la derecha, fragmentos angulosos de roca gris plomiza, a grafito.
> - **Una línea larga y fina,** como una espiral estirada, pasa por la cima de los tres montones y los une.
> - **Arriba de cada montón, lo que lo produce:**
>   - **Izquierda:**
>     - piedras sueltas sobre un trazo de suelo;
>     - una flecha curva que las lleva al montón;
>     - a la derecha, un suelo arado, hacia el que sube desde el montón una flecha de trazos.
>   - **Medio:**
>     - un círculo trazado con compás, con su centro y su radio, que encierra cinco animales pequeños de lana parda, planos como recortes;
>     - una flecha los lleva a un embudo en perspectiva;
>     - del embudo sale una flecha recta a la derecha y caen tres billetes diminutos de papel marfil hacia el montón.
>   - **Derecha:**
>     - el castillete de la mina: una silueta negra, plana y pesada, con su rueda arriba;
>     - debajo, un pique estrecho con una jaula negra y una doble flecha negra vertical;
>     - una flecha curva entra al pique desde la izquierda;
>     - de la rueda sale hacia la derecha una tira de hoja de plata, plana y brillante: el estaño.
> - **Debajo del suelo,** bajo cada montón, una línea corta.
>
> **Rótulos** (copia exactamente estas palabras):
> - en lo alto de cada eje, de izquierda a derecha: «PIEDRA · ayllu», «PAPEL · aldea», «MÁQUINA · mina»;
> - bajo cada montón: «montaña de piedras (9)», «montón de papeles y libracos (103)», «desmonte (140)»;
> - **izquierda:** sobre las piedras sueltas, «erial de piedras (9)»; en la flecha curva, «extraen y amontonan (9)»; en la flecha de trazos, «quizá un día (9)»;
> - **medio:** junto al círculo, «radio urbano (96)»; sobre el embudo, «embudo (102)»; en la punta de la flecha recta, «hasta esfumarse (102)»; junto a los billetes, «bolivianos en papel (103)»;
> - **derecha:** en la flecha que entra al pique, «rieles, maderos, dinamita, hombres (151)»; en la punta de la tira de plata, «miles de cargas de estaño (142)»;
> - sobre la línea larga que une los montones: «el mismo gesto»;
> - bajo las líneas cortas: «debajo: Melchora Mamani (35)», «debajo: dos guaguas (106)», «debajo: Juan Condori (154)».
>
> **Leyenda,** en el margen inferior derecho: «( ) páginas de la novela».

**Variante B: inventario en órbita**

> **Figura 8, como inventario en órbita.** Las tres estaciones flotan en el blanco, a alturas un poco distintas, como objetos de un inventario. Cada montón es un objeto pequeño en el centro de sus propias órbitas, con su eje. La hoja respira: grandes márgenes y casi nada de suelo, solo un trazo corto bajo cada montón.
>
> - **Los materiales de los montones** son los de la variante A: tierra siena, papel marfil y roca plomiza a grafito.
> - **El castillete negro es la masa más pesada de la hoja,** con su tira de hoja de plata hacia la derecha.
> - **Arriba de cada estación,** en pequeño, lo mismo que en la variante A:
>   - las piedras sueltas;
>   - el círculo con los animales y el embudo;
>   - el pique con la jaula.
> - **Las flechas:** de cada estación salen flechas rectas muy finas hacia los márgenes, con el rótulo en la punta.
> - **Una espiral larga y abierta** pasa por los tres montones.
>
> **Rótulos:** «PIEDRA · ayllu», «PAPEL · aldea», «MÁQUINA · mina», «montaña de piedras (9)», «montón de papeles y libracos (103)», «desmonte (140)», «embudo (102)», «miles de cargas de estaño (142)», «el mismo gesto».
>
> **Leyenda,** en columna, con un corchete, en el margen inferior izquierdo:
> - «( ) páginas de la novela»
> - «debajo: Melchora Mamani (35); dos guaguas (106); Juan Condori (154)»

## 20.9. Una segunda vuelta: correcciones cortas

Úsalas sobre la imagen generada, de a una:

1. «Afina toda la línea a la mitad de su grosor: que parezca grafito duro y tinta de 0,1 mm. No cambies nada más.»
2. «Deja más blanco: reduce el dibujo a dos tercios y céntralo. No agregues nada en el espacio que queda libre.»
3. «Borra toda palabra en alemán o en inglés, y cualquier firma o fecha.»
4. «Corrige solo este rótulo, letra por letra: «…». No toques nada más.»
5. «Quita todo el texto. Deja en su lugar líneas cortas y finas, como renglones vacíos.»
6. «Da cuerpo al material: que el pan de oro (o la hoja de plata) tenga arrugas finas y bordes recortados, y que la tierra siena se vea granulosa, como pigmento en polvo.»
7. «Quita todo lo que no esté en la guía, salvo las órbitas, los ejes, la leyenda y las líneas de construcción.»
8. «Sin oro: el horizonte es una línea de grafito como las demás.» (Para comparar; véase §20.11.)

## 20.10. Qué mirar en lo que salga

**Contra tus referencias:**

- ¿Tiene el aire de 18, 20 y 21? ¿El dibujo ocupa poco más de la mitad de la hoja?
- ¿La línea es tan fina y segura como en ellas, o sigue siendo de marcador?
- ¿La letra es diminuta, cursiva y sigue las líneas? ¿Hay una leyenda al margen?
- ¿El material se ve material (el oro con arruga, la tierra con grano, la tinta con brillo) o es un color plano?

**Contra el artículo:**

- ¿Se sigue leyendo el mecanismo?
  - En la 7, la mirada salta el foso.
  - En la 8, el mismo montón aparece en tres materiales.
- ¿El acento cae solo donde está la afirmación: el relleno, el foso y el horizonte en la 7, los tres montones en la 8?
- ¿Apareció algo que la novela no pone: figuras con rostro, cadáveres, banderas, palabras inventadas? Descarta esa imagen o corrígela.
- ¿Quedó algo en alemán o en inglés, una firma o una fecha? Bórralo (§20.9, corrección 3).

## 20.11. Cuidados

- **Tus referencias son obras de otros artistas.** Sirven para mirar, no para copiar. Los prompts no nombran a nadie: el modelo imitaría a esa persona y no a ti (`17`, §17.1). Lo que publiques tiene que ser tu mano (`19`, §19.9).
- **Lo que escriba el modelo no es fuente.** Cada palabra y cada página vienen de las figuras del artículo, y cada una se comprueba.
- **El oro del horizonte es la mirada de la memoria, no la del dibujo.** La memoria dora el pasado antiguo y no mira el foso; por eso el oro va solo ahí.
  - Aun así, es la parte más bella de la hoja, y la belleza puede tapar lo que se dice (`18`, §18.2.4).
  - Prueba también sin oro (§20.9, corrección 8) y compara.
- **Si estas imágenes influyen en tu versión a mano,** la declaración de IA tiene que decirlo (`19`, §19.9; `17`, §17.7).
