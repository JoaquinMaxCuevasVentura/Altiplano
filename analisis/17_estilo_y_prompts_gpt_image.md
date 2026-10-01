# 17. Tu estilo y seis prompts para explorar los pasteles con GPT Image 2

El 30 de septiembre de 2026 pediste tres cosas:

- analizar el estilo de tus pasteles al óleo;
- rescatar de ahí los prompts de las seis obras del artículo, para generarlas con GPT Image 2 acompañadas de los esquemas, como en un *inpainting*;
- elegir el color por sus propiedades físicas, no por la psicología del color.

**Para qué sirven estas imágenes.** Para explorar, no para publicar. El artículo llevará los escaneos de tus pasteles. Lo planteas desde la tesis de Dishita Turakhia, que definía la creatividad como la suma de diversidad cognitiva e interacción social: lo que genere la IA es otro interlocutor, «carne para pensar», y la obra es tuya.

**En corto:**

- **Tu estilo, en una frase:** una sola forma monumental, casi abstracta, entre piedra, hueso y carne, quieta en un espacio de ensueño, definida por la luz y no por la línea. El detalle está en §17.1.
- **Los esquemas:**
  - corregí la Figura 2 del artículo, que dibujaba la pirámide simétrica que tu propia guía pedía evitar;
  - hice seis guías de composición sin texto, en los tamaños de GPT Image 2;
  - agregué una máscara opcional para la Figura 5 (§17.2).
- **La paleta matérica:** cada color se nombra por el material de la novela del que sale y por lo que hace físicamente (§17.3). Ningún color «significa» algo.
- **Los seis prompts** están listos para copiar: un bloque de estilo común, un prompt por obra, una variante, qué evitar y qué mirar en el resultado (§§17.5-17.6).
- **Ajustados el mismo día** tras la evaluación de `18_estilo_y_articulo_evaluacion.md`:
  - el bloque de estilo pide dos capas, la serena y el raspado que la abre;
  - el ensueño queda solo en las Figuras 5 y 6;
  - la medida del cuerpo entra en las Figuras 1 y 4;
  - el agua queda solo donde la novela la pone.
- **Si esas imágenes influyen en los pasteles, la declaración de IA tiene que decirlo.** Cuando entren los escaneos hay que cambiar los pies, dos frases del texto y esa declaración (§17.7).

## 17.1. Tu estilo, leído en nueve pasteles

Las referencias son las cinco que enviaste hoy (arco sobre el agua, portada en la niebla, monolito nocturno y dos losas perforadas) y las cuatro de la primera ronda (`referencias_visuales/`). Dos de estas repiten obras de hoy: la portada y la losa de cielo tormentoso.

1. **Una sola forma, frontal y central.** Un arco, una portada, un monolito, una losa perforada. Ocupa el tercio central y no hace nada: está.
   - A veces una segunda forma diminuta da la escala: el monolito lejano que se ve por el agujero de las losas, o la figura mínima al pie de la roca en el formato alto de la primera ronda.
2. **Entre piedra, hueso y carne.** Es tu «materia cárnica».
   - Las aristas son blandas; los volúmenes se hinchan como músculo o se pulen como hueso.
   - El arco se apoya como una pierna.
   - La losa del cielo tormentoso tiene la base de una articulación, casi un sacro.
   - Los cantos brillan con el blanco cálido del hueso o de la piel.
3. **Definición mínima.** Pocos signos bastan para saber qué es: un vano oscuro, un nicho, un relieve apenas insinuado. En el monolito nocturno, algo que parece unas manos y una faja. Todo lo demás es masa.
4. **Sin contorno.** El borde aparece donde la luz choca con la sombra y se pierde en la bruma. No hay línea: hay valor.
5. **Espacio de ensueño:**
   - horizonte bajo;
   - suelo llano o agua somera que refleja;
   - nubes o niebla que disuelven los bordes;
   - escala incierta: puede ser un monumento o un objeto de mesa;
   - a menudo, un marco dentro del marco: el agujero de la losa que deja ver otra piedra lejos.

   Es tu «artefacto de ensoñación»: una cosa sacada de su lugar y puesta en un paisaje que no se mueve.
6. **Luz difusa y lateral.** La forma está más iluminada que su entorno.
   - La cavidad es lo más oscuro (el arco, la portada).
   - O es una ventana a algo más claro (las losas).
   - En el monolito nocturno, la piedra clara se recorta contra un fondo casi negro.
7. **El trazo** (lo que muestran los detalles ampliados):
   - grandes zonas fundidas con el dedo;
   - trazos cortos que siguen la forma, curvos en el intradós del arco y verticales en la losa;
   - rayado horizontal en el agua;
   - el grano del papel a la vista;
   - empaste en los brillos;
   - zonas casi esfumadas, como la base del monolito.
8. **El color:**
   - tierras (ocre, siena, sombra), blancos cálidos de hueso y crema, grises azulados y violáceos, azul pizarra en cielos y aguas;
   - la saturación es baja y el contraste fuerte es de valor, no de color.

**Parentescos.** Recuerdan la luz de la pintura romántica de paisaje y la soledad de la pintura metafísica, donde una forma aislada ocupa un paisaje vacío. Conviene **no nombrar pintores en los prompts**: el modelo imitaría a esos pintores y no a ti.

**Lo que piden las seis obras y tus pasteles no tenían:**

- **cortes y plantas** (Figuras 1, 2 y 4);
- **escenas nocturnas** (1, 4 y 6);
- **figuras humanas** (3, 4 y 6).

Los prompts las traducen a tu idioma:

- el corte se trata como una reliquia en pie;
- la planta, como una losa rayada;
- las personas, como masas sin rostro, postes o mojones.

Así se respetan también los límites del artículo: no entrar en el alma de los comunarios, no dibujar el linchamiento, no sexualizar.

**Qué de tu estilo suma al artículo y qué resta** está en `18_estilo_y_articulo_evaluacion.md`. Suman la materia, las operaciones, la piedra con cuerpo y el vano. Restan el ensueño sin tiempo, la escala incierta y el agua donde la novela no la pone.

## 17.2. Los esquemas

**Corregí la Figura 2** (`esquemas/fig2_signo_mapa.svg` y `articulo/figuras/figura_2.png`).

- **El problema.** La sección era una pirámide escalonada y simétrica. Es justo lo que tu guía pedía evitar (`05b`, Figura 2: «Una pirámide limpia y simétrica que confirme el diagrama de clases del narrador»).
- **Cómo queda:**
  - el cerro es asimétrico, con terrazas irregulares;
  - la chujlla abandonada del peón queda casi en la cumbre, más arriba que los Villca;
  - el Signo Escalonado se traza encima, simétrico, como una línea incisa que no coincide con la pendiente: flota de un lado y se hunde en la roca del otro.
- **El texto del artículo no cambia.** Ya decía «el signo no encaja en la pendiente, porque el peón vive en un escalón alto». Ahora el esquema lo muestra.
- **La extensión sigue en 49.472 caracteres**: las figuras no cuentan.
- Los otros cinco esquemas anotados siguen de acuerdo con el texto actual.

**Seis guías de composición sin texto** (`esquemas/guias/`, con la numeración del artículo):

| Figura | Guía | Tamaño |
|---|---|---|
| 1. Cráneo/nido | `guia_fig1_craneo_nido.png` | 1536 × 1024 |
| 2. Signo frente al mapa | `guia_fig2_signo_mapa.png` | 1024 × 1536 |
| 3. Apacheta | `guia_fig3_apacheta.png` | 1536 × 1024 |
| 4. Castillete | `guia_fig4_castillete.png` | 1024 × 1536 |
| 5. Pelvis | `guia_fig5_pelvis.png` (y `guia_fig5_pelvis_mascara.png`) | 1536 × 1024 |
| 6. Centinela | `guia_fig6_centinela.png` | 1024 × 1536 |

- **Por qué sin rótulos:** el modelo copia las letras que ve.
- **Cómo están hechas:** son manchas de valor con los bordes gastados y el grano del papel, como un encaje previo al pastel, con los colores de la paleta matérica.
- **Los tamaños** son los que admite GPT Image 2 (apaisado 1536 × 1024, vertical 1024 × 1536).
- **Qué cambia respecto de los esquemas anotados:**
  - la chujlla de la Figura 1 toma el perfil de un cráneo (frente a la izquierda, occipucio a la derecha, la puerta en arco como órbita);
  - las cumbres de la Figura 3 son agujas quebradas;
  - el cielo de la Figura 3 cambia de estado cerca de la cresta, sin costura recta.
- **Para cambiarlas:** abre los SVG en tu editor vectorial, o edita `generar_guias.py` y vuelve a correrlo.

**La máscara de la Figura 5 es opcional.**

- Si la herramienta acepta máscara, deja el cielo intacto y solo repinta la tierra, la pelvis y el cerro del humo.
- Es la operación que el artículo describe para esa figura: el cielo se deja en papel desnudo, sin tocar (reserva).
- En GPT Image 2 la zona transparente de la máscara se edita y la opaca se conserva. Hay reportes de que la máscara no siempre se respeta, así que tómala como un ensayo.

## 17.3. La paleta matérica

**El criterio es el que usas en diseño.** El color se elige por lo que el material es y hace:

- cuánto cubre;
- cómo toma la luz;
- de qué está hecho;
- qué le pasa con el calor, el agua o el tiempo.

La asociación poética queda liviana y sale del propio material, nunca de una tabla de significados («rojo = peligro»).

| Color | Material en la novela | Qué es y qué hace | En el pastel | Figuras |
|---|---|---|---|---|
| Negro de humo | Paredes «renegridas por el hollín» (p. 30) | Carbono puro: absorbe casi toda la luz y mancha lo que toca. El pigmento se hace del mismo hollín | Capa oscura que se raspa para sacar la luz | 1, 4, 6 |
| Siena, ocre y sombra | Adobe; la «rojiza peñería» (p. 6); la llanura «amarillosa, parda» (p. 6) | Óxidos de hierro, y de manganeso en la sombra: opacos y granulosos. El ocre calentado se vuelve siena, como el barro cocido | Masas que cubren y admiten esgrafiado | 1, 2, 5, 6 |
| Paja plomiza | Techo de paja «plomiza por el humo» (p. 10) | Fibra de ichu con hollín pegado: gris cálido | Trazo lineal, fibroso | 1, 6 |
| Blanco hueso | La pelvis; los postes-mojón | Fosfato de calcio: mate, calcáreo, se blanquea al sol | Empaste final; brillo sin reflejo | 5, 6 y los cantos de todas |
| Plomizo mineral | «El color plomizo y mineral del altiplano» (p. 66) | Polvo de roca gris, sin brillo | Fondo de la sequía | 5 |
| Pizarra | La planta del catastro | La piedra que se raja en láminas y en la que se escribía. Es piedra y es escritura | Capa gris sobre una clara; la incisión la descubre | 2 |
| Brasa de boñiga | El aire «oloroso a boñiga quemada» y la «cinta bermeja» del fogón (p. 32) | Combustión lenta y fría: rojo anaranjado, casi sin llama, mucho humo | Un solo foco bajo; el resto de la luz sale por raspado | 1 |
| Lana sin teñir o carmín de cochinilla | El poncho de Paulo (p. 109) | La lana de llama tiene sus propios pardos y negros. El carmín es tinte de insecto, del tejido andino | Si hay acento, que sea tinte y no bandera | 3 |
| Polvo de la puna | La puna seca | Limo fino y seco, mate: no refleja | Pastel seco con presión; el grano asoma como piedra | 3, 6 |
| Verde húmedo | El yunga; los «kollis verdinegros» (p. 6) | La hoja mojada refleja el cielo; la humedad baja el contraste | Veladura con solvente que chorrea | 3 |
| Blanco de niebla | La «muselina de vapor» (p. 109) | Gotas de agua que dispersan toda la luz por igual: por eso es blanca | Fundido con el dedo; borra los bordes | 3, 6 |
| Nieve | Las cumbres | Cristales de hielo: en la sombra devuelven azul | Blanco con sombra azul fría | 3 |
| Casiterita | La roca de la mina; la piel «ennegrecida por el polvillo que despide el estaño» (p. 138) | Mena de estaño: pardo negruzco con destellos. Su polvo apaga la carne | Fondo de la mina; los cuerpos, en carne apagada | 4 |
| Amarillo de copajira | El agua «sulfurosa y amarillenta» (p. 136) | Agua ácida con sulfatos de hierro: tiñe la roca de ocre amarillo | Banda disuelta que sube | 4 |
| Óxido de los rieles | «Rieles, maderos, dinamita, hombres» (p. 151) | Óxido de hierro hidratado | Acentos pequeños | 4 |
| Calamina | Los «cuchitriles de calamina» (p. 135) | Chapa de hierro cubierta de zinc: gris claro que blanquea al oxidarse | Techos del campamento | 4 |
| Llama de carburo | La «lamparilla de carburo» (p. 138); las luces como «prendedor de topacios» (p. 134) | Acetileno: llama blanca amarillenta, muy puntual | Puntos duros de empaste | 4 |
| Marte | «Sirio y Marte» (p. 72) | Hematita en su superficie: el mismo óxido del adobe. Es tierra en el cielo | Un punto de siena | 6 |
| Sirio | La misma página | Es una estrella blanco azulada. El narrador la llama «coágulo», pero no es roja | Un punto blanco frío | 6 |
| Cielo de altura | «El papel celeste y deslumbrador del cielo» (p. 57) | Con poco aire, el azul es más oscuro y limpio | Papel celeste sin tocar | 5 |
| Luna con polvo | La luna que «tenía sangre» (p. 72) | El polvo seco en el aire enrojece la luz que lo atraviesa | Un borde siena, no rojo sangre | 5 |

**Lo que cambia respecto de la guía `05b`.** Las paletas de las fichas nombraban colores de pintor: «rojo bermellón», «un solo acento rojo… ("tenía sangre")», «dos estrellas rojas». Aquí se dice de qué material sale cada color. El rojo de la luna es polvo, el de Marte es óxido, y Sirio vuelve a su color.

## 17.4. Cómo usar las guías con GPT Image 2

1. **Dónde.** En ChatGPT, con la opción de imagen, o en la API, con la edición de imágenes. Las dos admiten imágenes de referencia.
2. **Qué adjuntar,** en este orden:
   - **la guía** de la figura;
   - **dos de tus pasteles** como referencia de estilo, porque el modelo aprende más de tus imágenes que de las palabras. Sugiero:
     - el arco sobre el agua y la losa del cielo tormentoso, para las escenas de día (Figuras 2, 3 y 5), porque tienen el trazo y la materia cárnica;
     - el monolito nocturno y el arco oscuro de la primera ronda, para las de noche (1, 4 y 6).
3. **Qué escribir:** el bloque de estilo (§17.5) y, debajo, el prompt de la figura (§17.6).
4. **El tamaño:** el de la guía.
5. **Si copia el aspecto plano de la guía,** agrega: «No conserves los colores planos ni los bordes de la guía; solo la posición y el valor de las masas».
6. **Si copia el agua o la bruma de tus pasteles** donde la novela no las pone, agrega: «Sin agua ni niebla: el suelo es seco».
7. **Cambia una sola cosa por vez:** la luz, la distancia o un material. Así puedes ver qué produce cada decisión.
8. **Anota lo que aparece.**
   - Esas notas no son hallazgos del artículo: un hallazgo sale del pastel (`05b`, §5.5).
   - Pero sirven para decidir la composición antes de tomar el pastel.

## 17.5. El bloque de estilo (va primero en los seis)

Ya no pide ensueño ni escala incierta (`18`, §18.6). Pide las dos capas de §18.5: la serena, que es la mirada del narrador, y el raspado que la abre.

> Pastel al óleo sobre papel de grano medio, trabajado a mano en dos capas. Primero, una capa serena: masas gruesas fundidas con el dedo, trazos cortos que siguen la forma, grano del papel visible, luz difusa y lateral que hace brillar los cantos como hueso. Después, raspados finos hechos con una punta abren esa capa y dejan ver la de abajo: por ahí aparecen los detalles que importan. Una sola forma principal, casi abstracta, frontal y quieta, que parece a la vez piedra, hueso y carne; sus bordes aparecen y se pierden con la luz, sin línea de contorno. Pocos detalles, solo los necesarios para saber qué es. Colores de materiales reales: tierras de óxido de hierro (ocre, siena, sombra), negro de humo, blanco hueso mate, grises azulados; saturación baja; el contraste es de valor, no de color. Sin idealizar: nada de postal ni de paisaje sublime. Usa la imagen de composición adjunta solo como guía: respeta la posición, la proporción y el claro-oscuro de las masas, pero no copies sus bordes ni sus colores planos. Toma la textura, la luz y la manera de las imágenes de estilo adjuntas. Sin texto, sin letras ni números, sin aspecto digital ni fotográfico.

## 17.6. Las seis obras

### Figura 1. *Cráneo/nido*

**Guía:** `guia_fig1_craneo_nido.png` · 1536 × 1024 · estilo: pasteles nocturnos.

> Corte transversal de una chujlla aymara del altiplano, una choza de piedra y adobe con techo de paja, vista de noche a la altura de una persona sentada junto al fuego. El contorno del corte tiene, sin exagerar, el perfil de un cráneo: la bóveda de paja como calota, la única puerta, en arco, como órbita, el fuego en el centro, donde estaría el pensamiento. Adentro todo es hollín: negro de humo espeso sobre siena, pegado a las paredes. La luz no se pinta, se saca raspando esa capa oscura: así aparecen, en líneas claras, las vigas atadas con paja, las hoces, el yugo y el arado colgados. La chujlla se alza apenas dos metros del suelo y los camastros, la altura de un adobe: la escala es la de un cuerpo, no la de un monumento. Un brasero de boñiga: brasa roja anaranjada, sin llama alta, con humo. Sobre el techo, una cruz de palo con una figurita de barro cocido. A un lado, la ladera del cerro de arenisca rojiza de donde salieron las piedras de los muros. La chujlla parece a la vez casa, cabeza y nido, apoyada en la llanura oscura. Nadie adentro: el cuerpo que la habita se adivina por las herramientas y el fuego.

- **Variante (reliquia):** La chujlla-cráneo sola sobre la llanura seca, como una reliquia en pie, pero de dos metros de alto, a la medida de un cuerpo; el resplandor del brasero sale por la puerta en arco, y la cruz con la figurita de barro es un pequeño brillo en la cima.
- **Evita:** personas, rostros, escenas de costumbres, postal folclórica, llamaradas, ventanas, niebla, texto.
- **Qué mirar:**
  - ¿La chujlla se lee como la «madriguera» del narrador o como caja de herramientas y nido?
  - ¿El perfil de cráneo se impone o sale forzado?

### Figura 2. *Signo Escalonado frente al mapa*

**Guía:** `guia_fig2_signo_mapa.png` · 1024 × 1536 · estilo: pasteles de día.

> Dos vistas del mismo cerro en una sola hoja vertical, como un dibujo de arquitecto. Arriba, el cerro cortado en sección: una masa de arenisca rojiza, pesada y carnosa, de pendiente irregular, más empinada a la izquierda, con terrazas hechas de capas gruesas de pastel, como piedras apiladas. En las terrazas, chozas pequeñas y oscuras; la más alta de todas, casi en la cumbre, está vacía, abandonada, apenas un contorno. Sobre esa masa, trazado con una punta, un signo escalonado perfecto y simétrico que no coincide con la pendiente: queda en el aire en un lado y se hunde en la roca en el otro. Abajo, la planta del mismo terreno: un tablero de parcelas un poco desigual, un poco contrahecho, sobre una capa gris de pizarra, rayado con punzón hasta que asoma la capa clara de abajo; pequeños mojones de piedra en los cruces y, en un borde, dos bloques oscuros enfrentados, la hacienda y la iglesia. Entre las dos vistas, líneas de proyección finas, rayadas. Luz de día, cenital, casi sin sombra. La sección parece un cuerpo; la planta, una piel escrita.

- **Variante (más materia):** Las mismas dos vistas, con más materia: la sección en empaste grueso, piedra sobre piedra, y el signo inciso encima sin calzarle; la planta, una losa de pizarra rayada con punzón, con el grano a la vista. Sigue siendo un dibujo de análisis, sin horizonte ni cielo.
- **Evita:** una pirámide limpia, perspectiva aérea, paisaje, personas, letras, números, mapas modernos.
- **Qué mirar:**
  - ¿La escalera social cabe en la pendiente o se rompe?
  - ¿Qué pasa cuando el mito (la sección) y el mapa (la planta) se hacen con la misma materia?

### Figura 3. *Umbral de la apacheta*

**Guía:** `guia_fig3_apacheta.png` · 1536 × 1024 · estilo: pasteles de día.

> Paisaje apaisado partido en dos por la cresta de una cordillera, a las cinco de la tarde. A la izquierda, la puna: llanura seca de polvo gris y ocre pálido bajo un cielo violeta, horizonte recto; pastel seco apretado sobre papel de grano grueso, de modo que el blanco del grano asome como piedra. A la derecha, el yunga: dos paredes de verde húmedo que bajan y se cierran como una garganta, tragándose una bruma blanca que sube; ahí el pastel está disuelto, en capas transparentes que chorrean como cera derretida. En la cresta, donde una técnica se vuelve la otra, un hombre de pie, pequeño y sin rostro, como un poste clavado, con el poncho de lana sacudido por el viento como un gallardete; a su lado, una familia arrodillada, tres masas oscuras. Al fondo, cumbres nevadas afiladas como construcciones góticas, con sombras azules. Abajo, en el fondo del yunga, sobre el río, una cadena diminuta de monos cogidos de las manos. La luz rasante viene del lado de la puna.

- **Variante (umbral):** El hombre de la cresta como un poste de piedra y lana, con el poncho sacudido por el viento; a su lado, la garganta del yunga abierta como un vano orgánico que deja ver, muy lejos, la bruma que sube.
- **Evita:** la postal de los Yungas, la selva exuberante, montones de piedras en la cresta (la novela no los pone), rostros, texto.
- **Qué mirar:**
  - ¿El paso de lo seco a lo húmedo se lee como otro paisaje o como un cambio de estado de la materia?
  - ¿El puente de monos pesa o queda como anécdota?

### Figura 4. *El castillete y la caída al plano 450*

**Guía:** `guia_fig4_castillete.png` · 1024 × 1536 · estilo: pasteles nocturnos.

> Corte vertical de una mina de estaño, de noche, en tres partes. Arriba, contra la noche, la torre de acero del pique como un encaje de líneas claras rayadas en la cera; a su lado, un montón grande y pálido de roca estéril: una montaña de piedras hecha con un cerro deshecho; a la izquierda, el campamento en escalera, de casas grandes a cuchitriles de calamina gris; pocas luces pequeñas y duras de carburo. Debajo, la roca: pardo negruzco de casiterita, con destellos. En el centro, el pique, un vacío vertical que baja como un edificio al revés, con galerías a tres alturas, cada una del alto de un hombre; en la entrada, dos nichos en arco. En el pique, la jaula: siete cuerpos apretados, hechos solo con el dedo, masas de carne apagada por el polvo de estaño, sin rasgos, y encima una rejilla de líneas claras raspadas. Al fondo, la galería más baja, inundada: agua ácida de un amarillo ocre que sube por el cuerpo, de los tobillos a las rodillas y al ombligo; un montón informe de roca, barro y maderos astillados, y una viga quebrada.

- **Variante (medida del cuerpo):** Solo la galería más baja, de cerca y a la altura de una persona: el agua amarilla deja en la pared las marcas de lo que sube, de los tobillos a la cintura y al ombligo, como una regla; arriba, por el pique, la luz lejana del carburo.
- **Evita:** sangre, disparos, cadáveres, rostros, cascos modernos, charcos que reflejan, números, texto.
- **Qué mirar:**
  - ¿La mina se lee como lo contrario del ayllu o como su doble invertido?
  - ¿El montón de arriba se reconoce como la montaña de piedras que soñaban los comunarios?

### Figura 5. *Pelvis telúrica / Pachamama sorda*

**Guía:** `guia_fig5_pelvis.png` · 1536 × 1024 · estilo: pasteles de día · máscara opcional: `guia_fig5_pelvis_mascara.png`.

> Paisaje de sequía visto desde lo alto. El cielo es papel celeste desnudo, sin una sola pincelada; en él, una luna menguante delgada, con un borde apenas siena, del polvo seco del aire. Abajo, tierra agrietada de color tierra de sombra y gris plomizo mineral, con grietas raspadas hasta el papel. En el centro, la cuenca de las vertientes secas tiene la forma de una pelvis de vaca vista en escorzo: dos alas y una abertura central, en blanco hueso mate y calcáreo, como una losa de hueso que carga peso. Dentro de la abertura, el cauce seco, arenoso y blanquecino, con piedritas. Al fondo, a la izquierda, un cerro pequeño con un hilo de humo de ofrendas. Luz blanca de mediodía, dura, sin sombra que proteja. Quietud de ensueño: nada se mueve. La pelvis es estructura, hueso que sostiene, no recipiente.

- **Variante (ensueño):** La pelvis de hueso en pie, como una losa perforada sobre la tierra agrietada; por su abertura se ve, muy lejos, el cerro con el hilo de humo. Es tu motivo de la losa con el agujero, puesto al servicio de la figura.
- **Evita:** cuerpos humanos (sobre todo femeninos), erotismo, vasijas, calaveras, sangre, texto.
- **Qué mirar:** ¿la pelvis se lee como estructura que carga o vuelve a leerse como sexo, el tropo del narrador? Si pasa lo segundo, anótalo.

### Figura 6. *El centinela de la resistencia*

**Guía:** `guia_fig6_centinela.png` · 1024 × 1536 · estilo: pasteles nocturnos.

> Nocturno vertical, con el horizonte bajo y un cielo enorme, azul casi negro, sin luna. En la llanura de polvo ocre, la casa más grande de un ayllu vacío, de adobe y paja. En el vano oscuro de su puerta, tres figuras de pie tratadas como postes o mojones: tres piedras claras y verticales, sin rostro ni gesto, pálidas como hueso. Un cayado de palo apoyado junto a ellas, como un cuarto apoyo. Una puerta suelta, entreabierta, golpeada por el viento. A lo lejos, a un lado, un campanario oscuro con dos buitres. Del suelo suben formas pálidas y transparentes, veladas con el dedo: los muertos que salen de la tierra a mirar el cielo. En el cielo, estrellas pequeñas; Marte, un punto de óxido rojizo; Sirio, un punto blanco azulado. Atmósfera de ensueño, quieta y silenciosa: es la noche en que los muertos salen a mirar. Las figuras se leen por su silueta.

- **Variante (ensueño):** Los tres vigías como tres mojones pequeños, piedras con cuerpo, en el vano de una puerta enorme; la casa y la llanura se funden en la noche, y el campanario, al fondo, es otra piedra que vigila.
- **Evita:** héroes, puños alzados, poses épicas, rostros, fantasmas de película, texto.
- **Qué mirar:**
  - ¿Los vigías se leen como cuidado y permanencia o como ruina, los «cancerberos» del narrador?
  - ¿Hacia dónde miran?

## 17.7. Qué cambia en el artículo cuando entren los escaneos

Hoy el artículo presenta los esquemas de encaje como Figuras 1 a 6. Las Figuras 7 y 8 son diagramas, no pasteles, y se quedan (`19_esquemas_a_mano_y_diagramas.md`). Cuando reemplaces los esquemas por los escaneos de tus pasteles (`articulo/figuras/LEEME.md`):

1. **Pies de figura.** «Esquema de encaje del pastel al óleo. Fuente: elaboración propia con asistencia de IA» pasa a «Pastel al óleo sobre papel, [medidas], 2026. Fuente: elaboración propia».
2. **Dos frases del texto:**
   - §1: «de los que se reproduce el esquema de encaje, el trazado que fija la composición (figuras 1-6)».
   - §2: «Los esquemas de encaje que aquí se reproducen […] no descubren nada, pero obligan a decidir».
   - Con los pasteles, los planos (3) se reescriben con lo que mostró cada pieza (`05b`, §5.5).
3. **La declaración de IA** (norma 8: declarar el alcance real):
   - Sale «de los esquemas de encaje (figuras 1-6) y»; queda «y el diseño y trazado de los diagramas (figuras 7 y 8)». (Desde el 1 de octubre los esquemas también son notaciones diseñadas con IA: `23_esquemas_de_encaje_como_notaciones.md`.)
   - Si las imágenes de GPT Image 2 influyeron en los pasteles, entra algo como: «y la generación de imágenes exploratorias, previas a los pasteles y no reproducidas». Entre las herramientas se agrega GPT Image 2 (OpenAI).
   - Las dos cosas miden casi lo mismo, así que la extensión no se mueve.
   - «El autor es autor exclusivo de los pasteles al óleo» sigue siendo cierto.

## Fuentes consultadas en la web

- Guía de GPT Image 2: tamaños, referencias y edición: https://masonry.so/blog/gpt-image-2-guide
- Edición con máscara en GPT Image 2 (alfa 0 se edita, alfa 255 se conserva): https://www.adpicto.com/en/blog/gpt-image-2-image-editing-workflow
- API de edición de GPT Image 2 (hasta 16 imágenes, tamaños admitidos): https://fal.ai/models/openai/gpt-image-2/edit/api
- Reporte sobre fallas de la máscara: https://community.openai.com/t/gpt-image-2-masking-issue/1379510
