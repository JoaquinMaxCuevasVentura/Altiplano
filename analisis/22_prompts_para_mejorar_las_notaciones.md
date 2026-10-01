# 22. Prompts para mejorar las notaciones de las Figuras 7 y 8 con GPT Image 2

El 1 de octubre de 2026 pediste prompts para meter las notaciones de las Figuras 7 y 8 en GPT Image 2 y mejorarlas.

**Para qué sirven:** igual que con los pasteles, son para ver qué hace la IA y pensar con eso. No van al artículo. Las figuras finales serán los escaneos de tus propios dibujos.

**En corto:**

- **Qué subir** (§22.1). Preparé las figuras **con sus rótulos** en los tamaños de GPT Image 2:
  - `entrada_fig7_memoria_retorno.png`, de 1536 × 1024;
  - `entrada_fig8_tres_montones.png`, de 1024 × 1536.

  Si subes las figuras del artículo tal cual, el modelo las recorta o las deforma, porque sus proporciones no coinciden.
- **Tres maneras de mejorarlas:**
  - **toda la hoja de una vez** (A), que es lo más libre, aunque el modelo puede torcer las palabras;
  - **todo menos los rótulos** (B), con una máscara que los protege;
  - **zona por zona** (C), con una máscara por zona: muralla, foso, horizonte y atalaya en la 7; montones y castillete en la 8.
- **Un bloque de mejora** que va primero (§22.3): conservar lo que dice la notación y mejorar el papel, la línea, la escritura y la materia.
- **Cuatro variantes para pensar** (§22.6): más materia, más notación, más vacío y «otra mano». Esta última pregunta qué se pierde sin oro ni alquitrán.
- **Correcciones cortas, qué mirar y cuidados** (§§22.7-22.9). Entre los cuidados, la declaración de IA si estas imágenes influyen en tus dibujos.

## 22.1. Qué subir y cómo

**Los archivos** (todos en `esquemas/guias/`):

| | Figura 7 | Figura 8 |
|---|---|---|
| Entrada, con rótulos | `entrada_fig7_memoria_retorno.png` (1536 × 1024) | `entrada_fig8_tres_montones.png` (1024 × 1536) |
| Máscara que protege los rótulos | `mascara_fig7_rotulos.png` | `mascara_fig8_rotulos.png` |
| Máscaras por zona | `mascara_fig7_muralla.png`, `_foso`, `_horizonte`, `_atalaya` | `mascara_fig8_montones.png`, `_castillete` |
| Mapa de zonas | `zonas_fig7.png` | `zonas_fig8.png` |
| Referencias de estilo | Tus imágenes 26 y 23 | Tus imágenes 24 y 25 |

1. **El orden de los adjuntos:** primero la entrada; después, una o dos referencias. Di cuál es cuál: «La primera imagen es la que hay que mejorar; las otras son solo referencias de estilo».
2. **El tamaño de salida:** el mismo de la entrada (1536 × 1024 para la 7; 1024 × 1536 para la 8). **Calidad:** alta.
3. **Las máscaras:**
   - lo transparente se edita y lo opaco se conserva;
   - **cada máscara de zona protege también los rótulos** que caen dentro de ella;
   - hay reportes de que GPT Image 2 a veces edita fuera de la máscara: compara siempre con la entrada.
4. **Dónde usarlas:**
   - **En la API**, la máscara va con la primera imagen.
   - **En ChatGPT** no se sube una máscara. Si tu herramienta deja seleccionar una zona con un pincel, píntala guiándote por el mapa de zonas. Si no, nombra la zona en el prompt («solo la mancha negra del foso») y revisa que no haya tocado lo demás.

## 22.2. Qué se puede mejorar

Las notaciones son dibujo de computadora, y eso se nota en cuatro cosas. Los prompts piden mejorar justo eso, sin tocar lo que dicen:

1. **La línea** es uniforme: no tiene presión ni grano de grafito.
2. **El papel** es un color plano.
3. **La escritura** es una tipografía: todas las letras iguales se ven iguales.
4. **La materia** sale de filtros. La acuarela, el alquitrán y las hojas de metal imitan el material, pero no tienen cuerpo.

**Hay además tres elementos débiles:**
- la atalaya (un eje con cuatro elipses);
- el castillete (una «A» negra);
- los montones, que son pequeños para lo que cargan.

## 22.3. El bloque de mejora (va primero en todos)

> Esta imagen es una notación dibujada en computadora: un diagrama de lectura de una novela. Mejórala como si fuera una obra sobre papel hecha a mano, sin cambiar lo que dice.
>
> **Conserva:** la composición, la posición y el tamaño de cada elemento, las flechas, las órbitas, los ejes y los rótulos. No agregues ni quites elementos. No cambies ninguna palabra ni ningún número.
>
> **Mejora:**
> - **el papel:** algodón blanco y grueso, con el grano visible, fotografiado de frente con luz pareja;
> - **la línea:** grafito duro y tinta de 0,1 a 0,3 mm, con presión que varía y el grano del grafito a la vista; las rectas, con regla; las elipses, a mano alzada, repasadas;
> - **la escritura:** manuscrita de verdad, pequeña e inclinada, a lápiz, con las variaciones de una mano y no una tipografía repetida, en castellano y con tildes;
> - **la materia:** cada mancha de color es un material real con cuerpo (pigmento en polvo frotado, tinta densa, hoja de metal pegada, papel recortado), no un color digital.
>
> Toma de las imágenes de referencia solo la manera de trazar, de escribir y de usar el material, no su contenido, sus formas ni sus palabras. Nada en alemán ni en inglés. Sin firma ni fecha. Sin aspecto de infografía, sin sombras 3D, sin degradados digitales.

## 22.4. Figura 7: *La memoria del retorno*

**A. Toda la hoja** (sin máscara):

> **Figura 7, la memoria del retorno.** Mejora cada elemento así:
> - **La mirada,** que es también el tiempo: la línea de trazos que cruza la hoja, trazada con regla en grafito, con sus tres cruces y su punta de flecha. Donde termina, la tira de oro es una hoja de oro real, pegada, con arrugas finas, brillo irregular y bordes rotos.
> - **La atalaya:** el eje vertical en grafito y las cuatro elipses a mano alzada, repasadas una o dos veces. Arriba, las nueve marcas de tinta, como personas vistas de lejos, sin rostro.
> - **La muralla:**
>   - pigmento de tierra siena real, frotado con el dedo y granuloso, con piedrecilla menuda incrustada;
>   - los siete apellidos de su cara izquierda, escritos a mano, uno por hilada;
>   - la cara derecha, un borde de piedras planas sin nombre, a lápiz.
> - **Las dos líneas de mira** punteadas, del ojo a los bordes del foso, finas.
> - **El foso:**
>   - una mancha de betún o tinta negra densa, con el brillo leve del alquitrán y el borde desgarrado;
>   - adentro, más de ciento cincuenta rayitas raspadas con una punta hasta el blanco del papel, de largos y direcciones distintos;
>   - los cinco grupos de marcas de Quispe, con sus líneas que convergen en la «x»;
>   - la órbita fina a ras del suelo.
> - **La leyenda,** en columna con su corchete, arriba a la izquierda.
>
> No agregues figuras, calaveras, cuerpos ni paisaje.

**B. Todo menos los rótulos** (máscara `mascara_fig7_rotulos.png`):

> Edita solo la zona transparente de la máscara; los rótulos no se tocan. Mejora el papel, la línea y la materia como se describe arriba: la hoja de oro, la tierra siena de la muralla, el alquitrán raspado del foso, el grafito de las elipses, las líneas de mira y la leyenda. Respeta la posición de cada cosa, para que los rótulos sigan junto a lo que nombran.

**C. Zona por zona** (una máscara por vez; en ChatGPT, pinta la zona guiándote por `zonas_fig7.png`):

- **Muralla** (`mascara_fig7_muralla.png`):
  > Repinta solo la zona transparente: la pirca en sección. Que sea tierra siena de verdad: pigmento frotado y granuloso, más oscuro donde se acumula en los bordes, con piedrecilla menuda incrustada (no dibujada con contorno). Su cara derecha es un borde de piedras planas sin nombre, a lápiz. Conserva su forma y su altura: su borde superior tapa la vista del foso.
- **Foso** (`mascara_fig7_foso.png`):
  > Repinta solo la zona transparente: el foso. Que sea betún o tinta negra densa, con el brillo leve del alquitrán y el borde que se acumula y desgarra el papel. Adentro, más de ciento cincuenta rayitas finas raspadas con una punta hasta el blanco del papel, de largos y direcciones distintos, y cinco grupos de marcas de donde salen las líneas que convergen. Nada de figuras, calaveras ni cuerpos.
- **Horizonte** (`mascara_fig7_horizonte.png`):
  > Repinta solo la zona transparente: la tira de oro del horizonte. Que sea una hoja de oro real, delgada, pegada al papel, con arrugas finas, brillo irregular y bordes rotos. La línea de trazos entra en ella.
- **Atalaya** (`mascara_fig7_atalaya.png`):
  > Repinta solo la zona transparente: la atalaya. Un eje vertical de grafito, con cuatro elipses a mano alzada repasadas y, arriba, nueve marcas mínimas de tinta, como personas vistas de lejos. Nada de torre ni de figuras con rostro.

## 22.5. Figura 8: *Tres montones*

**A. Toda la hoja** (sin máscara):

> **Figura 8, tres montones.** Mejora cada elemento así:
> - **El eje vertical de páginas:** una regla de grafito con sus marcas y sus números diminutos, el corte con dos rayitas oblicuas y la punta abajo.
> - **Arriba,** la línea de puntos de la altura del cerro y la flecha de trazos que sube hacia ella.
> - **El montón de piedra:** una loma de pigmento de tierra siena real, frotado, con piedritas dibujadas encima. La bandada de piedritas llega volando desde la izquierda y crece a medida que se acerca.
> - **El montoncito de piedras con su cruz de paja,** a un tercio de altura.
> - **La aldea:**
>   - el círculo de compás, con su centro y su radio;
>   - los cinco animales, como recortes planos de lana parda;
>   - el embudo en perspectiva, a tinta, y los billetes diminutos de papel que caen.
> - **El montón de papeles:** recortes reales de papel marfil y libritos pegados como collage, con sombras mínimas.
> - **El castillete:** una silueta de papel negro recortado y calado, como el «encaje de acero» de la torre con que la novela anuncia la mina (p. 134), con su rueda.
> - **El estaño:** una tira de hoja de plata real, plana y arrugada, con brillo frío.
> - **El desmonte:** fragmentos angulosos de roca gris plomiza, a grafito.
> - **El pique:** la jaula negra y la doble flecha. Lo que baja por él: un riel, un madero, dinamita y dos marcas de hombres.
> - **Al fondo, el informe montón:** rocas a grafito, una mancha de lodo pardo y astillas de madera.
> - **El resto:**
>   - la espiral larga, a grafito, que baja por las tres estaciones;
>   - las órbitas, con sus pequeñas puntas de flecha;
>   - los tres corchetes del margen derecho, con su rótulo de lado;
>   - la leyenda, abajo.
>
> No agregues personas con rostro, paisajes ni maquinaria realista.

**B. Todo menos los rótulos** (máscara `mascara_fig8_rotulos.png`):

> Edita solo la zona transparente de la máscara; los rótulos y los números del eje no se tocan. Mejora el papel, la línea y la materia como se describe arriba: la tierra siena, los recortes de papel, la lana de los animales, el papel negro calado del castillete, la hoja de plata, la roca plomiza, el lodo y la madera, la espiral y las órbitas a grafito. Respeta la posición de cada cosa, para que los rótulos sigan junto a lo que nombran.

**C. Zona por zona** (guíate por `zonas_fig8.png`):

- **Montones** (`mascara_fig8_montones.png`):
  > Repinta solo las zonas transparentes: los cinco montones, cada uno de su materia real:
  > - arriba, una loma de pigmento de tierra siena, frotado, con piedritas;
  > - a un tercio de altura, un montoncito de piedras con una cruz pequeña de paja;
  > - en el medio, recortes de papel marfil y libritos pegados como collage;
  > - junto al castillete, fragmentos angulosos de roca gris plomiza;
  > - al fondo del pique, rocas, una mancha de lodo pardo y astillas de madera.
  >
  > Sombras mínimas de collage, sin volumen 3D.
- **Castillete** (`mascara_fig8_castillete.png`):
  > Repinta solo las zonas transparentes: la torre de la mina, su pique y la tira del estaño. La torre es una silueta de papel negro recortado y calado, con celosía fina y su rueda, como el «encaje de acero» con que la novela anuncia la mina (p. 134). Debajo, el pique con la jaula negra y la doble flecha. La tira del estaño es hoja de plata real, plana y arrugada, con brillo frío.

## 22.6. Variantes para pensar

Agrega una de estas frases al final del prompt A. Cada una cambia una sola cosa, para que veas qué produce:

1. **Más materia:**
   > Que cada materia sea collage real, fotografiado con luz rasante para que se vea el relieve: el pigmento en polvo levanta, el oro brilla, el papel recortado proyecta su sombra.
2. **Más notación:**
   > Agrega, solo con líneas y sin palabras nuevas, el aparato de las notaciones: más órbitas alrededor de cada centro, con sus puntas de giro; rectas finas que salen hacia los márgenes y terminan en una «x»; líneas de construcción tenues.
3. **Más vacío:**
   > Reduce el dibujo a dos tercios y deja que la hoja respire. Quita lo que no haga falta para leer el mecanismo, pero ningún rótulo.
4. **Otra mano:**
   > La misma notación, dibujada solo con grafito y una sola materia, la tierra siena, sin oro, sin negro ni plata.

   Sirve para preguntarte qué se pierde: si la Figura 7 se sigue leyendo sin el alquitrán del foso y el oro del horizonte, o la 8 sin el papel negro del castillete.

## 22.7. Correcciones cortas, para una segunda vuelta

- «Las palabras cambiaron. Vuelve a la imagen anterior y mejora solo con la máscara de rótulos.»
- «Corrige solo este rótulo, letra por letra: "…". No toques nada más.»
- «Quita las letras inventadas y deja en su lugar renglones cortos y vacíos.»
- Las de `20`, §20.9, también sirven: afinar la línea, dar más blanco, borrar firma o fecha y dar cuerpo al material.

## 22.8. Qué mirar en lo que salga

- **¿El mecanismo se sigue leyendo?**
  - En la 7, la muralla tapa el foso y la mirada lo salta hasta el oro.
  - En la 8, los tres montones bajan por el eje de páginas hasta el informe montón.
- **¿Las palabras y los números son los mismos?** Compáralos con la entrada, uno por uno.
- **¿La materia tiene cuerpo, o sigue siendo un color plano?**
- **¿Apareció algo que no va?** Rostros, calaveras, banderas, maquinaria realista, palabras en otro idioma o una firma.
- **¿Qué te dice para tu propio dibujo?** Anótalo: eso es lo que vale de esta exploración.

## 22.9. Cuidados

- **Estas imágenes no se publican.** El artículo llevará los escaneos de tus dibujos.
- **Si influyen en tus dibujos, la declaración de IA tiene que decirlo:**
  - en b), «y la generación de imágenes exploratorias, previas a los dibujos y no reproducidas»;
  - en a), GPT Image 2 (OpenAI) (`17`, §17.7).
- **Cuando tus escaneos reemplacen las Figuras 7 y 8:**
  - el pie pasa a «Diagrama a mano, [técnica], 2026. Fuente: elaboración propia»;
  - la declaración pierde «el trazado de los diagramas», y también «el diseño» si los rediseñas (`19`, §19.9; `21`, §21.9).
- **Tus referencias son obras de otros artistas:** los prompts no nombran a nadie. Sirven para mirar, no para copiar.
- **Lo que escriba el modelo no es fuente:** cada palabra y cada página se comprueban contra la figura.

## 22.10. Cómo regenerar las entradas y las máscaras

Si cambias las notaciones, corre en este orden:

1. `node analisis/esquemas/diagramas/generar_diagramas.js`, que escribe la figura, la guía y la entrada de cada notación;
2. `python3 analisis/esquemas/guias/generar_guias.py`, que las pasa a PNG y rehace las máscaras y los mapas de zonas.

La máscara de rótulos se calcula sola: es la diferencia entre la entrada (con texto) y la guía (sin texto), un poco ensanchada. Las zonas están en `generar_guias.py`, en las coordenadas del dibujo.
