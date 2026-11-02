# 34. Auditoría de la versión final de «Cosecha de piedras»

2 de noviembre de 2026. Auditoría de Codex. Base: `3eb412cfdfe8a344d64cc82e2c24274c61efb6dd`, rama `claude/altiplano-botelho-article-jm2nlr`. Las líneas citadas corresponden al Markdown de ese commit, no a páginas del Word.

**Lectura y límites, antes del dictamen.** Se leyeron completos `AGENTS.md`, el artículo (358 líneas), `analisis/33_version_final_sin_patrones_de_ia.md`, `entregables/04_fichero_de_pasajes.md` y `entregables/02_lista_de_envio.md`. Los demás registros se buscaron completos por texto y se leyeron sus pasajes pertinentes, no todos de principio a fin. Los libros PDF de Churata adjuntos en esta conversación no se leyeron enteros para esta auditoría: se cotejaron visualmente las cinco hojas que contienen los pasajes utilizados. No están disponibles las fuentes primarias de las demás obras ni la transcripción de la novela. La concordancia con un registro no es una nueva verificación contra el libro. Las dos citas en bloque están abreviadas en el fichero y no permiten el cotejo íntegro letra por letra. No se declara cerrado lo que dependa de esas fuentes ausentes.

## Resumen y diez prioridades

La tesis se mantiene de la introducción a las conclusiones. El resumen y el abstract dicen sustancialmente lo mismo; el problema más claro entre ambos y el cuerpo es el estado de realización de los pasteles. Las 157 citas de la novela entre comillas tienen coincidencia literal exacta en el fichero, incluidos acentos, mayúsculas y puntuación interior; hay una discrepancia local de página y otra remisión adicional sin respaldo literal. No apareció ningún *ibid.* dirigido a otra obra: se resolvieron los 108, contando el de «cit. en ibid.».

Los recuentos siguientes cuentan **filas de hallazgo**, no cada palabra o cada repetición de un problema sistemático. «Error» es una discordancia comprobable en estos documentos; «dudoso» exige fuente, precisión o decisión del autor; «estilo» es una propuesta opcional. No son una puntuación de autoría de IA. Una fila puede afectar a varias líneas; no vuelve a contarse en los anexos de evidencia.

| Frente | Error | Dudoso | Estilo | Total |
|---|---|---|---|---|
| Escritura | 1 | 1 | 20 | 22 |
| Estructura | 0 | 4 | 5 | 9 |
| Citas | 1 | 11 | 2 | 14 |
| Referencias | 1 | 14 | 4 | 19 |
| Total | 3 | 30 | 31 | 64 |

1. **C01:** dar a «erial de piedras» su referencia propia a p. 9; la p. 6 solo respalda la primera cita del párrafo.
2. **C02:** comprobar Fuão p. 29 antes de conservar como literal «un segundo recorte desfigura…».
3. **C03-C04:** comprobar la formulación literal de la definición de *manuaje* y del papel sujeto con dos yemas; el registro confirma temas y páginas, no esas secuencias exactas.
4. **C05-C06:** localizar el ejemplo de Canaletto y las palabras sobre la carne atribuidas a Martin; evitar una cita compuesta de memoria o una mediación omitida.
5. **C08:** comprobar «Fauces del abismo» del Cuadro 1: el fichero solo trae «fauce».
6. **C09:** comprobar el segundo localizador, p. 156, de «manchones» en las conclusiones.
7. **E16:** aligerar el engarce de relativos «la forman… y que…» en el párrafo de Konkachi.
8. **S01:** aclarar si se estudian pasteles realizados o esquemas para obras pendientes, y hacerlo igual en los dos resúmenes.
9. **R01/E18:** aplicar las comillas y cursivas pedidas sin modernizar las citas de las fuentes.
10. **C10/R03-R09:** recuperar las fuentes necesarias para la condición completa de Fuão y los pendientes bibliográficos y de paginación. No marcar como cotejado con originales lo que solo concuerda con el registro.

No se propone un recorte por extensión. Tampoco se cambia el título, el epígrafe ni una interpretación. Durante la auditoría, el autor indicó conservar el femenino solo dentro de citas y usar **«el collage»** en la prosa propia. Esa preferencia se registra abajo; el artículo permanece intacto en este PR de auditoría. Todas las redacciones siguientes son propuestas para aprobar por separado. No se ha editado el artículo, regenerado sus Word ni modificado el fichero.

## 1. Escritura y redacción

### 1.1. Recuento de patrones

Se contó la prosa propia española de las secciones 1-8, incluidos los análisis de figuras. Se excluyeron las citas textuales, los pies, el cuadro, las referencias, los rótulos y los títulos. Los dos resúmenes se contrastaron aparte. Las categorías son indicios editoriales, no pruebas de uso de IA. Los casos interpretativos llevan su lista de localizaciones para que el autor pueda aceptar o discutir el cómputo.

| Patrón | Número | Criterio y localizaciones |
|---|---:|---|
| Dos puntos que anuncian una explicación o lectura como revelación | 5 | L39,79,100,114,168. No se cuentan los que solo introducen una cita, una lista de método o un rótulo. El caso de L100 es fronterizo: también introduce una cita. Hay uno adicional en el abstract L17, fuera de este cómputo español. |
| «No… sino» literal | 1 | L246. Otros dos paralelismos equivalentes, pero no literales, están en L57 («Más que…») y L208 («…y no como…»). No se cuentan los de Vázquez Ramos o Ingold que están dentro de citas. |
| Cierres sentenciosos o muy simétricos | 23 | L33,37,45,53,57,73,114,116,120,132,144,156,162,168,192,206,246,248,250,260,274,276,278. Es un juicio de lectura; algunos, especialmente el cierre final, pueden conservarse con toda intención. |
| Series de tres | 18 | Inventario manual a continuación. No se cuentan los tres planos obligatorios de las figuras, las tres limitaciones de método ni listas dentro de citas. No toda serie es prescindible. |
| Vocabulario inflado de la familia solicitada | 0 | «crucial», «clave», «fundamental» y «subrayar», en prosa propia con función enfática. «Una pieza clave» es cita de Rivera. «Importante» en L37 no se clasifica por sí solo como inflación. |
| Gerundios que comentan la importancia | 0 | Los hallados expresan operación, modo o proceso: siguiendo, sumando, quitando, labrando, consumiendo, midiendo, etc. No se penalizan por su terminación. |
| Frases cortas encadenadas | 1 cadena de 2 | L146: dos oraciones propias consecutivas de hasta doce palabras. Se excluyen los cortes producidos por citas, abreviaturas, pies y etiquetas. |
| Párrafos consecutivos que empiezan igual | 0 | Igualdad de las dos primeras palabras significativas entre párrafos consecutivos de prosa. Las coincidencias aisladas de «El» o «La» no bastan. Los arranques repetidos «El narrador» existen, pero no son consecutivos. |

Las 18 series registradas: L39 (cómo/objetos/gestos); L41 (tres materiales) y L41 (títulos/expedientes/ordenanzas); L45 (animales/cuerpos/piedras); L47 (punto de vista/escala/límite); L57 (piensan/expresan/comunican); L104 (muros/fuego/herramientas), L104 (bóveda/puerta/fuego) y L104 (hollín/camastros/herramientas); L144 (tambo/iglesia-fuerte/instituciones republicanas, agrupación de tres etapas); L146 (escribir/tejer/arar); L170 (cuerpo/familia/fauce); L246 (muralla/foso/atalaya); L248 (Condori/Mamani/Quispe); L260 (jornal/revólver/boquete); L274 (desde dónde/escala/dentro-fuera), L274 (chujlla/tribuna/cumbres), y L264 (mojones/pircas/linderos, seguida de un cuarto término, apellido: caso fronterizo). Con criterio estricto de listas de exactamente tres sin agrupación histórica ni prolongación, resultan **16**; se conservan los dos casos fronterizos para no esconder decisiones de cómputo.

### 1.2. Hallazgos y quince reescrituras más visibles

E01-E15 son los quince casos seleccionados. Su numeración no obliga a corregirlos todos.

| N.º | Sección, primeras palabras y línea | Tipo | Qué dice el texto | Problema | Propuesta exacta | Respaldo |
|---|---|---|---|---|---|---|
| E01 | 1. Introducción: una cosecha de piedras; «Este artículo se pregunta, primero, qué sabe…»; L39 | estilo | la mecánica material del despojo: cómo se pierde la tierra, con qué objetos y con qué gestos | Dos puntos explicativos más una serie de tres que vuelve a anunciar la tesis. | Creemos que la novela registra, sin que su narrador lo advierta, las operaciones concretas del despojo. | 33, diagnóstico; comparación con L11 y L41. |
| E02 | 2. Cómo leer: el espacio, las manos y el dibujo; «El ensamblaje tiene además una teoría propia,…»; L79 | estilo | Fuão pone una condición que adoptamos: se pueden juntar figuras e ideas lejanas | El anuncio hace de la condición una revelación y repite «condición» al introducir la cita. | Con Fuão, adoptamos la condición de que las analogías entre figuras e ideas lejanas tengan una referencia explícita (Fuão, 2011: 53). | 26, L324. Revisar primero el calificativo «relativizada»; C10. |
| E03 | 3. La chujlla: una casa a la medida del cuerpo; «El narrador presenta el ayllu desde lo…»; L100 | estilo | como en un plano de situación: «las chujllas…» | Los dos puntos adelantan una interpretación que podría apoyarse en la cita sin anunciarla. | La descripción inicial del ayllu se parece a un plano de situación cuando el narrador escribe que «las chujllas de las familias más antiguas han trepado en los riscos del cerro y desde allí parecen ocupar un sitio de preeminencia sobre el resto de chozas» (Botelho Gosálvez, 1982 [1945]: 6). | 04_fichero, fila p. 6; sin nuevo cotejo de la novela. |
| E04 | 3. La chujlla: una casa a la medida del cuerpo; «El narrador tampoco le ve cuartos a…»; L114 | estilo | El narrador tampoco le ve cuartos a la casa: «Las chujllas no tienen cuartos ni mucho menos» | Anuncio seguido de cita que revela la misma afirmación. | El narrador afirma que «Las chujllas no tienen cuartos ni mucho menos» (ibid.: 30). | 04_fichero, p. 30; mantener el antecedente Botelho si se mueve el párrafo. |
| E05 | 5. El éxodo: los Yungas y la mina; «Del otro lado, las manos del puneño…»; L168 | estilo | Del otro lado, las manos del puneño pierden su oficio: | Otro diagnóstico presentado como descubrimiento tras dos puntos. | En los Yungas le dicen a Paulo: «Sabrás arar en la puna, pero aquí esa es otra música» (ibid.: 113). Su experiencia de labranza no le asegura trabajo allí. | 04_fichero, p. 113; la segunda frase conserva la interpretación, no añade dato. |
| E06 | 2. Cómo leer: el espacio, las manos y el dibujo; «La lectura que proponemos se hace con…»; L57 | estilo | Más que una mano enfrentada a un papel, lo que hay son dos manos con dos agarres. | Antítesis de efecto semejante a «no X, sino Y»; remate demasiado simétrico. | Ambos actos emplean las manos, aunque el arado y la firma cumplen funciones distintas en el despojo. | 27, §27.6: los agarres no equivalen por sí solos a clases sociales. |
| E07 | 2. Cómo leer: el espacio, las manos y el dibujo; «La palabra *manuaje* tiene antecedentes, que Cárcamo…»; L73 | estilo | Lo que distingue unas palabras de otras es quién consigue que las suyas valgan como ley. | Cierre sentencioso que generaliza desde varios usos distintos de la palabra. | En estos conflictos, la autoridad decide cuáles de esos escritos reconoce como títulos válidos. | 08, pp. 99 y 101 de Rivera; limitar la frase al conflicto estudiado. |
| E08 | 3. La chujlla: una casa a la medida del cuerpo; «El narrador tampoco le ve cuartos a…»; L114 | estilo | Donde el narrador ve una madriguera, cualquiera de ellos vería una casa comprimida. | Remate redondo y atribución hipotética de una lectura a varios autores. | Estas comparaciones permiten leer las dependencias de los Huanca como partes de una casa, aunque cada autor estudie un contexto diferente. | 25 y 26; propuesta interpretativa para el autor. |
| E09 | 3. La chujlla: una casa a la medida del cuerpo; «Esa mirada tiene un antecedente en el…»; L120 | estilo | El viajero convierte en piedra al que trabaja la piedra, como hará después el narrador con los comunarios. | Juego especular muy visible; la petrificación es una interpretación, no una frase de Squier. | Al describir al anciano como parte de los monumentos, Squier lo asimila a las ruinas; proponemos comparar ese gesto con la mirada del narrador de Altiplano. | 31, L254-262. Poner *Altiplano* en cursiva en la versión aprobada. |
| E10 | 3. La chujlla: una casa a la medida del cuerpo; «**Figura 2. *Signo Escalonado frente al mapa*.**…»; L132 | estilo | en eso el mito y el mapa coinciden, porque los dos escalonan | Remate que repite la metáfora del título y no precisa qué se compara. | El esquema permite comparar la jerarquía familiar con la distribución de las viviendas. | Figura 2; no se propone cambiar la interpretación sin aprobación. |
| E11 | 4. Umacachi: la trampa de los papeles; «El despojo, por otro lado, no tiene…»; L156 | estilo | lo que mueve el despojo tiene más que ver con la casta que con el tamaño | Antítesis y cierre generalizador; un caso no refuta toda la explicación de Alexander. | La relación personal con el tinterillo no protege a Vicente; en este caso, la proximidad convive con la desigualdad de casta. | 25, p. 405; 04_fichero, pp. 103-105. |
| E12 | 4. Umacachi: la trampa de los papeles; «Dos niños mueren de hambre y los…»; L162 | estilo | la aldea los alojó como se aloja a los animales de casa | Remate etimológico que vuelve a formular la domesticación ya citada. | El término «domesticados» prolonga la comparación entre el alojamiento de los Villca y el de los animales (ibid.: 107). | 04_fichero, p. 107; etimología independiente pendiente si se mantiene. |
| E13 | 7. El retorno: reparar la casa, elegir la memoria; «Con una muralla, un foso y una…»; L246 | estilo | Los comunarios de la novela no caminan mirando al pasado, sino que lo esconden en un foso. | Único «no… sino» literal en la prosa española propia. Reitera el contraste con el epígrafe. | Frente al lema del epígrafe, la memoria del retorno aparta el hambre y conserva las cosechas. | 04_fichero, pp. 156-157; no cambiar el epígrafe. |
| E14 | 7. El retorno: reparar la casa, elegir la memoria; «Una pirca de doble cara enseña lo…»; L250 | estilo | Los comunarios besan el suelo, pero no vuelven a la memoria, y la paz se paga con ese olvido. | Cierre aforístico que repite el diagnóstico de L246. | El retorno repara las casas, pero deja fuera del recuerdo común el hambre y a parte de quienes la padecieron. | 04_fichero, pp. 155-159; decisión interpretativa del autor. |
| E15 | 7. El retorno: reparar la casa, elegir la memoria; «Ursula K. Le Guin opuso dos formas…»; L260 | estilo | La novela, que guarda lo que el ayllu prefiere no mirar, resulta ser el recipiente más grande. | La escala del recipiente remata la analogía en lugar de precisar su alcance. | La novela conserva también los padecimientos que el relato del retorno deja fuera. | 07, límites de Le Guin; 04_fichero, pp. 156-157. |
| E16 | 3. La chujlla: una casa a la medida del cuerpo; «El narrador tampoco le ve cuartos a…»; L114 | estilo | la forman «dos habitaciones que hacen ángulo» y que, junto con una pirca, cierran el patio | Los relativos «que hacen» y «que cierran» pueden coordinarse gramaticalmente. Al quedar el primero dentro de una cita y el segundo fuera, el engarce resulta difícil de seguir; no se clasifica como falta de concordancia. | La forman «dos habitaciones que hacen ángulo»; estas y una pirca cierran el patio. [Conservar la referencia Churata, 2017: 123 al final del pasaje.] | Churata, 2017: 123, PDF hoja 121; sintaxis del propio artículo. |
| E17 | 3. La chujlla: una casa a la medida del cuerpo; «El narrador tampoco le ve cuartos a…»; L114 | dudoso | La mayor «no tiene dos metros» | El antecedente es «una casa» y no se dice qué magnitud se mide. La copia de Churata tampoco explicita «de alto»: no completarlo de memoria. | Churata escribe que la mayor «no tiene dos metros» (Churata, 2017: 123), sin precisar aquí la magnitud. | PDF de Textos esenciales, p. 123; no resolver una posible errata de la fuente. |
| E18 | 1. Introducción: una cosecha de piedras; «El aymara colonial tenía palabras para todo…»; L37 | error | chujlla; ayllu; yatiri; achachis; pututus; Jilakata; huaca; apacheta, en redonda fuera de citas | Incumple la cursiva solicitada para voces aymaras y quechuas. Algunas son préstamos castellanizados, pero aquí rige la instrucción expresa del autor. | Aplicar cursiva solo a las voces comunes fuera de citas: *chujlla*, *chujllas*, *ayllu*, *yatiri*, *achachis*, *pututus*, *Jilakata*, *huaca* y *apacheta*. No poner en cursiva el apellido Huanca ni cambiar grafías dentro de citas. | Instrucción de esta auditoría; localizaciones en §1.3 del informe. |
| E19 | 3. La chujlla: una casa a la medida del cuerpo; «**Figura 1. *Cráneo/nido*.** (1) *Texto*. Muros de…»; L104 | estilo | calota; infolio; alzado | La calota no se explica; «infolio» aparece en cita y se reutiliza en las conclusiones, y «alzado» es técnico. | Tras calota: «la parte superior del cráneo»; tras infolio, fuera de la cita: «un libro de gran formato»; al primer alzado: «una vista vertical». | AGENTS.md: explicar términos técnicos; definiciones de trabajo, no citas nuevas. |
| E20 | 4. Umacachi: la trampa de los papeles; «Allí manda el Alcalde vitalicio, el doctor…»; L146 | estilo | Escribir, tejer y arar comparten así el vocabulario de la mano. En los Andes, además, el hilo servía para registrar. | Única cadena detectada de dos oraciones propias consecutivas de hasta doce palabras, excluidos pies, rótulos y citas. | La novela comparte ese vocabulario entre escritura, tejido y labranza; el registro mediante hilos tiene, además, un antecedente en los dibujos de Guaman Poma. | 31, Imagen 3; propuesta conserva la relación sin llamar escritura al khipu. |
| E21 | 1. Introducción: una cosecha de piedras; «El narrador, por otra parte, dista de…»; L45 | estilo | por otra parte… por otra parte | La locución aparece dos veces en el mismo párrafo. | Conservar «El narrador, por otra parte…» y sustituir «En ella se asegura, por otra parte» por «La nota editorial asegura también». | Lectura del párrafo; no altera citas. |
| E22 | Preliminares; «This article reads *Altiplano* (1945), by Raúl…»; L17 | estilo | the dry wall | La expresión puede sugerir construcción en seco genérica y no la pirca de piedras del resumen. | Sustituir «the dry wall» por «the dry-stone wall». | Resumen L11 y abstract L17; propuesta de precisión terminológica, no fuente nueva. |

### 1.3. Coherencia y normas revisadas

**Decisión recibida del autor:** proponer «el collage» fuera de citas. Casos: L39 «el collage»; nota L43 «en el collage»; L79 «la del collage»; L132 «hace collage» no cambia, pues no tiene artículo; L190 «distinta del collage»; L206 «otro collage»; L276 «el collage». Conservar sin cambio la cita de L132 «no escribe, inscribe», *casa collage* y los títulos de obras, así como cualquier femenino que aparezca dentro de una cita. Es la decisión editorial recibida para la prosa del artículo; no se presenta como una corrección de las fuentes.

- **Chujlla/chuklla:** solo hay una *chuklla* y está dentro de la cita de Churata de L102. No debe corregirse. Fuera de ella se usa chujlla de manera consistente.
- **Wanqa, wank'a y huanca:** el texto distingue *wanqa* en la transcripción de Bertonio, *huanca* como grafía colonial y *wank'a* en Dean. No se normalizan entre sí. Huanca como apellido se conserva en redonda. La relación interpretativa con el apellido sigue siendo decisión del autor.
- **Nombres:** se mantienen Paulo Huanca, Juan Condori, Vicente Villca, Basilio Quispe y Margarito Mendoza; no se confunde alcalde con tinterillo ni a las dos hijas mayores. Choquehuanca en el nombre de Braulio y Chuquihuanca en la lista citada no se igualan sin ver la novela. Tiwanaco está dentro de una cita del glosario; no se cambia por Tiwanaku.
- **Manuaje y Signo Escalonado:** la definición del primero está explicada; el segundo conserva mayúsculas cuando designa el término. «Signo», abreviado en L218, es recuperable pero menos preciso. No confundir *manuage*, la forma citada de McLeod, con una errata española.
- **Cursivas fuera de citas:** chujlla/chujllas en L37,57,94,98,102,111,114,116,190,232,274; yatiri L206,250; achachis L218; pututus L130; Jilakata L94; huaca L89; apacheta L91,166,170,177. Ayllu aparece además en títulos, palabras clave y numerosos párrafos: la corrección de E18 es sistemática, no una sustitución ciega dentro de citas o nombres propios. Los títulos de libros ya llevan cursiva. Los de canciones llevan comillas.
- **Números:** no hay un decimal que exija coma en la prosa; las fechas, páginas, DOI e identificadores no son millares ordinarios. No convertir 1412, 1612, GKS 2232 ni páginas 1153 en «1.412», «1.612», etc. No se halló un caso confirmado de separador decimal incorrecto.
- **Ortografía y tiempos:** no se identificó una falta ortográfica general comprobable fuera de citas; la acumulación de relativos de E16 es una propuesta de claridad, no una discordancia demostrada. El paso entre presente de lectura y pasado histórico es generalmente coherente. «aun hoy» y grafías como «obscuras» pertenecen a citas: no se corrigen por gusto.

## 2. Estructura

| N.º | Sección, primeras palabras y línea | Tipo | Qué dice el texto | Problema | Propuesta exacta | Respaldo |
|---|---|---|---|---|---|---|
| S01 | Preliminares; «Este artículo lee *Altiplano* (1945), de Raúl…»; L11 | dudoso | seis pasteles al óleo usados como instrumento de lectura | Resumen y abstract se corresponden, pero parecen afirmar que existen los pasteles terminados; el cuerpo y la lista de envío dicen que se reproducen esquemas y que los pasteles faltan. | Si aún faltan las obras: «seis esquemas de encaje para pasteles al óleo como instrumento de lectura»; en inglés: «six compositional sketches for oil pastels used as tools for reading». Si el autor sí trabajó con pasteles no publicados, aclararlo en el método. | L47, L75, L83; lista de envío, paso 4. Decisión del autor. |
| S02 | 2. Cómo leer: el espacio, las manos y el dibujo; «La oposición entre la mano que ara…»; L59 | estilo | La oposición entre la mano que ara… | Un solo párrafo junta Umacachi, la historia de Warisata, Rivera y dos columnas de Churata. Se pierde el paso entre silencio narrativo y comparación histórica. | Abrir párrafo antes de «Gamaliel Churata, escritor puneño…» y antes de «Cuando se publicó, por otra parte…». | L59; continuidad de las referencias revisada; no mover citas entre obras. |
| S03 | 3. La chujlla: una casa a la medida del cuerpo; «La chujlla de los Huanca tiene dos…»; L102 | estilo | La chujlla de los Huanca tiene… | La descripción, la teoría de la casa, el narrador y el abecedario mural ocupan el mismo párrafo. | Abrir párrafo en «El narrador entra en ella…» y en «Gamaliel Churata, en cambio…». Explicitar Botelho en la primera cita del párrafo nuevo si se mueve texto. | L102; PDF de Churata p. 20; 10 y 26. |
| S04 | 6. La sequía y el linchamiento: el cuerpo en la catástrofe; «## 6. La sequía y el linchamiento:…»; L202 | estilo | 6. La sequía y el linchamiento… | Tras el éxodo se vuelve a causas anteriores sin aviso cronológico. El orden por escalas es legítimo; falta hacer visible el regreso. | Añadir al comienzo de L204: «Volvamos a la sequía que precede al éxodo para examinar cómo se representa el cuerpo en la catástrofe». | Índice y orden de capítulos del fichero, §1; no cambia la estructura elegida. |
| S05 | 5. El éxodo: los Yungas y la mina; «**Figura 3. *Umbral de la apacheta*.** (1)…»; L170 | dudoso | Figura 3… (3) Contraste… | Los seis análisis conservan Texto → Operación → Contraste, pero el alcance no es parejo: la Figura 3 añade léxico, traducción y dos teorías; la 4 se limita a una comparación interna. No es necesario igualar su largo. | Conservar los tres planos; sacar del plano (3) de la Figura 3, si el autor lo aprueba, la frase general sobre la cola y situarla junto a la explicación del ensamblaje. No añadir una fuente a la Figura 4 solo para equilibrar. | L104,132,170,192,208,218; 08, circularidad del dibujo. |
| S06 | 2. Cómo leer: el espacio, las manos y el dibujo; «No todo dibujo descubre algo. Javier Seguí…»; L75 | dudoso | descubrir, no descubren nada, aunque obligan a decidir | El texto niega descubrimientos de los esquemas y después titula cuatro hallazgos de la lectura. No es contradicción necesaria, pero podría parecerlo. | Los esquemas no aportan nuevos datos de la novela; permiten comparar sus descripciones y hacer explícitas nuestras decisiones de lectura. | 08, objeción 3; L264. El autor decide si mantiene la negación enfática. |
| S07 | 4. Umacachi: la trampa de los papeles; «Los Villca llegan a la aldea con…»; L158 | estilo | Los Villca llegan a la aldea… | La ordenanza, Fuão, Scott, The Voidz, Zavaleta y la tasación compiten dentro del mismo párrafo. La canción llega sin identificar qué añade a Scott. | Abrir párrafo antes de «James C. Scott observa…». Ante la canción, si se conserva: «La desigualdad de aplicación tiene un eco en estos versos de The Voidz». | 27, límites del cruce con cultura popular; no se propone quitarla por extensión. |
| S08 | 1. Introducción: una cosecha de piedras; «Conviene decir desde el principio algunos supuestos…»; L47 | dudoso | Se trata de una investigación en desarrollo. | Se presenta como versión final, pero permanece una fórmula procedente de otra convocatoria; además los esquemas y los pasteles tienen estados diferentes. | Conservar si el autor quiere declarar ese estado; alternativa: «Los esquemas reproducidos fijan las composiciones de una serie de pasteles todavía por realizar». | Lista de envío, pasos 4 y 10; propuesta condicionada al estado real. |
| S09 | 2. Cómo leer: el espacio, las manos y el dibujo; «\| 4. Castillete \| Callapos; viga que…»; L92 | estilo | Agua, cascotes, montón (144,154) | La celda Masa agrupa datos distintos y no da los localizadores145/152-153 que el cuerpo asigna al agua. | Agua (145,152-153), cascotes (144), montón (154). Mantener pendiente cotejo con la novela. | L190 y §2.3; coincidencia documental, fuente primaria pendiente. |

### 2.1. Tesis, distribución y traducción del resumen

| Sección | Función respecto del resumen y los hallazgos de §8 | Evaluación |
|---|---|---|
| 1 | Montón como arquitectura mínima; piedra/papel/máquina; diferencia entre narrador y registro material | Sostiene los hallazgos 1 y4; presenta las preguntas sin alterar la tesis. |
| 2 | Espacio histórico, manos y escritura indígena; método y Cuadro 1 | Sostiene 3 y4. Es densa por la acumulación de teorías y por Warisata. |
| 3 | Casa, jerarquía y Kero-Pata; Squier y Churata | Sostiene 1-4. Los párrafos L102 y114 superponen varios contrastes; sus atribuciones hipotéticas merecen la cautela de E08. |
| 4 | Cadena de agentes y soportes del despojo | Es el desarrollo más directo del hallazgo 3. La abundancia de analogías dentro de L158 no equivale a falta de argumento. |
| 5 | Trabajo desplazado, cuerpo, mina y máquina | Sostiene 1,2,3 y4. La hija sin nombre prepara la crítica de género; el salto hacia la sequía requiere S04. |
| 6 | Violencia, metáfora maternal y vigías | Sostiene 2 y4 y el límite ético del dibujo; no es una digresión por ser menos jurídica. |
| 7 | Reparación, memoria y ausentes | Sostiene 1 y2 y explicita la selección de memoria anunciada en el resumen. Dean/Fuão, la canción, Spedding y Le Guin tienden a reexplicar el mismo cierre; E13-E15 ofrecen alternativas locales. |
| 8 | Cuatro hallazgos, posiciones del dibujo y tres límites | Recapitula lo desarrollado. Churata vuelve con un fragmento nuevo, pero del mismo pasaje de Konkachi ya presentado; no introduce un corpus distinto. |

Recuento por espacios del Markdown de cada sección, incluidos pies, cuadro y marcas: §1 **1.345**, §2 **2.109**, §3 **2.256**, §4 **1.056**, §5 **1.554**, §6 **984**, §7 **1.370**, §8 **712**. No equivale al cómputo del generador. El peso de §3 se debe en parte a dos figuras y a una imagen; la menor extensión de §6 no demuestra debilidad. No se recomienda igualarlas mecánicamente.

Resumen: **122 palabras**; abstract: **118**, por separación por espacios, coincidentes con 33. Ambos anuncian posesión en piedra, pérdida ante papeles y máquinas, silencio sobre escritura aymara y memoria selectiva. «That possession» explicita bien el sujeto de «se pierde». «Tools for reading» es admisible; *dry wall* puede sugerir tabique seco en inglés y, si se busca precisión para *pirca*, conviene **dry-stone wall**. «Indian history» sigue «historia india», pero su adecuación editorial puede decidirse con la revista; no se impone una reinterpretación. Los dos resúmenes comparten el problema de S01. El segundo hallazgo sobre el Signo Escalonado es desarrollo del cuerpo, no una tesis diferente omitida fraudulentamente en el resumen.

### 2.2. Figuras e imágenes

Se verificaron existencia y apertura de los trece archivos. La posición siguiente es la del Markdown, no una garantía de proximidad en cada página del Word/PDF. El PDF existente tiene 38 páginas; no se lo regeneró ni se inspeccionó visualmente página por página. Se vieron además los archivos de las imágenes2 y4: el primero permite identificar al trabajador y los viajeros; el segundo muestra casas mayores abajo e hileras menores en la ladera. La inspección de esas copias no verifica sus fechas, títulos de catálogo ni la identidad de sus ocupantes.

| Elemento | Llamada / archivo / pie | Pasaje que lo pide | Resultado |
|---|---|---|---|
| Imagen 1 | L61 /66 /70 | Escribano andino y testamento | Autor, obra, año, doble paginación, dibujo307, institución, signatura y dominio público presentes. |
| Figura 1 | L104 /107 /111 | Chujlla de los Huanca | Título, esquema, técnica proyectada y elaboración con IA presentes. |
| Imagen 2 | L120 /123 /127 | Grabado de Squier y trabajador | Página288, procedencia y derechos presentes. El hombre del grabado no se identifica como el anciano del relato: conservar esa cautela. |
| Figura 2 | L132 /135 /139 | Signo y mapa | Completo para un esquema. |
| Imagen 3 | L146 /149 /153 | Tejedora y contador | Díptico con páginas215/360, numeración digital, dibujos80/143, autor y fuente. |
| Figura 3 | L170 /173 /177 | Paso de la apacheta | Completo para un esquema. |
| Imagen 4 | L180 /183 /187 | Campamento minero | Rango de fechas, archivo, colección, código y derechos. Falta página porque es fotografía; R12 distingue ficha y observación. |
| Figura 4 | L192 /195 /199 | Mina y descenso | Completo para un esquema. |
| Figura 5 | L208 /211 /215 | Sequía y cuerpo | Completo para un esquema. |
| Figura 6 | L218 /221 /225 | Vigías del ayllu | Completo para un esquema. |
| Imagen 5 | L232 /235 /239 | Arado de pie y trabajo corporal | Autor, obra, año, doble paginación y dibujo393 presentes. |
| Figura 7 | L246 /253 /257 | Arquitectura de la memoria | La pirca de L250 queda entre llamada y archivo; pertenece al mismo argumento. No hay un salto a otra sección. |
| Figura 8 | L264 /267 /271 | Tres montones y captura minera | Diagrama situado junto al primer hallazgo. Pie completo para el estado actual. |

En figuras1-6, Texto → Operación → Contraste conserva el orden en los seis casos. Sus análisis tienen respectivamente **372,268,370,158,238,295 palabras** por espacios de la línea completa. La operación sigue siendo una prescripción de cómo trabajar el pastel, no un informe de resultados observados. No deben inventarse medidas, soporte físico o año de obras todavía pendientes para completar los pies. Las imágenes1,3 y5 conservan la limitación de resolución ya advertida en la lista de envío.

### 2.3. Cuadro 1

| Fila | Comparación con cuerpo y fichero | Pendiente |
|---|---|---|
| 1 | Muros8, vigas31, portal34, hollín30-31 y huaca10 concuerdan con la distribución textual. | Cotejo primario de los datos, no solo de las citas. |
| 2 | Villca20, peones21, ausencia de historia22 y títulos36-37 son compatibles con el cuerpo. | El orden es una disección del autor; no atribuir el catastro dibujado a un plano que exista en la novela. |
| 3 | Muralla108 y escena109 corresponden a L166-170. | «Fauces del abismo» no está reproducido en el fichero; C08. Niebla no está transcrita allí como dato: pendiente p.109. |
| 4 | Callapos145, viga154, nichos141, jaula143 y boquete144 concuerdan. | «Agua, cascotes, montón (144,154)» deja fuera de la celda las páginas145,152-153 que el cuerpo da para el agua. Propuesta: «Agua (145,152-153), cascotes (144), montón (154)». Es precisión de localizadores, no una nueva cita literal. |
| 5 | Ganado64, vertientes58, grietas56 y cielo57 coinciden con L204-208. | La pelvis es decisión del dibujante, no anatomía descrita en la novela. |
| 6 | Cayado75, puertas79, casa79 y vigías80 concuerdan con L218. | Vara del Jilakata73 está respaldada por su identificación en el fichero, pero no por una transcripción de la vara; «Mirada sobre la inmensidad (80)» tampoco se transcribe. Pendiente ver pp.73/80. |

## 3. Citas

| N.º | Sección, primeras palabras y línea | Tipo | Qué dice el texto | Problema | Propuesta exacta | Respaldo |
|---|---|---|---|---|---|---|
| C01 | 1. Introducción: una cosecha de piedras; «En Jatun-Kolla, el ayllu aymara que Raúl…»; L29 | error | «erial de piedras» tras la referencia a p. 6 | El fichero asigna el fragmento a p. 9. La referencia a p. 6 sirve a la primera cita del párrafo, pero no a esta. | Añadir inmediatamente después de «erial de piedras»: «(ibid.: 9)». No cambiar palabras; cotejar la página con el impreso antes del envío. | 04_fichero, fila p. 9. Error de concordancia documental; fuente primaria pendiente. |
| C02 | 1. Introducción: una cosecha de piedras; «[^pastel]: El pastel al óleo es pigmento…»; L43 | dudoso | «un segundo recorte desfigura la imagen rectangular inicial, dándole un nuevo significado» (ibid.: 29) | Sin respaldo literal en el registro: 27 documenta «A segunda incisão» y otra frase, no este pasaje completo. | Mantener en suspenso la cita hasta ver Fuão p. 29. Si no se consigue la fuente, retirar solo las comillas de esta frase y presentarla como paráfrasis atribuida, tras aprobación; no reconstruir el original. | 26 y 27, búsqueda completa de la secuencia; fuente pendiente. |
| C03 | 2. Cómo leer: el espacio, las manos y el dibujo; «La lectura que proponemos se hace con…»; L57 | dudoso | «neologismo homólogo al lenguaje, pero con las manos» | El registro 02 trae «un homólogo al lenguaje, pero con las manos» para 2025a p. 12 n. 1; 04 registra la remisión 2019→2025b, pero no transcribe literalmente esta definición. | Cotejar 2025b p. 244 y su cita de 2019 p. 1412. No sustituir la cita por la variante de otro artículo. | 02 L17; 04, tabla de fuentes n.º 3. Sin respaldo literal de esta formulación; pendiente. |
| C04 | 2. Cómo leer: el espacio, las manos y el dibujo; «La lectura que proponemos se hace con…»; L57 | dudoso | «sujetar un papel con dos yemas dactilares» (2025a: 10) | El registro respalda los agarres y la página, pero no se localizó esta secuencia literal en ningún registro. | Cotejar el PDF de Cárcamo Pino p. 10; mantener pendiente el fragmento. | 27 §27.6 y 04, tabla n.º 2; sin respaldo literal en el registro. |
| C05 | 2. Cómo leer: el espacio, las manos y el dibujo; «El método sigue los cuatro pasos que…»; L77 | dudoso | ciudad «completamente imaginaria» (ibid.: 3) | El registro 03 respalda el método de Lundberg, pero no se localizó este fragmento literal ni la página del ejemplo de Canaletto. | Cotejar Lundberg p. 3. Si no se confirma, dejar la comparación como propuesta del autor sin cita textual ni atribución del ejemplo a Lundberg. | 03 §3.1 y 04, tabla n.º 6; sin respaldo literal en el registro; pendiente. |
| C06 | 6. La sequía y el linchamiento: el cuerpo en la catástrofe; «El yatiri Basilio Quispe, que vendía «piedra…»; L206 | dudoso | «las manipulaciones de la carne» (Martin, 2014: 85) | Sin respaldo literal en el registro. La tabla de 04 menciona Bacon en una lectura de Deleuze; no permite saber quién enuncia esas palabras ni reconstruir su original inglés. | Consultar p. 85 de Martin y su nota antes de decidir si corresponde «cit. en». No atribuir palabras a Deleuze sin verlas. | 04, tabla n.º 7; 03 y 08. Fuente, voz y página pendientes. |
| C07 | 6. La sequía y el linchamiento: el cuerpo en la catástrofe; «**Figura 6. *El centinela de la resistencia*.**…»; L218 | dudoso | «en quien hallan todo amparo» (ibid.: 447) | Se documentan saywa y «Amparo, defensor, refugio, padre», pero no se halló esta secuencia literal en los registros. | Cotejar la entrada de Bertonio p. 447 y conservar la cita pendiente; no fabricarla con las palabras de la definición resumida. | 08 L341, 09 L34 y 23 L175. Sin respaldo literal en el registro. |
| C08 | 2. Cómo leer: el espacio, las manos y el dibujo; «\| 3. Apacheta \| Paulo, «gallardete clavado»…»; L91 | dudoso | «Fauces del abismo» (109) | El fichero solo reproduce «fauce», en singular; la secuencia plural completa no figura allí ni en 06. No se puede asumir que sean equivalentes en una cita literal. | Opción que sí respalda el fichero: «“fauce” del yunga (109)» en la celda Vano, con comillas latinas en el manuscrito. Aprobar tras consultar la p. 109 de la novela. | 04_fichero y 06, p. 109; literal completo pendiente. |
| C09 | 8. Conclusiones: lo que muestra el dibujo y sus límites; «El dibujo muestra, ante todo, posiciones. Los…»; L274 | dudoso | «manchones» (ibid.: 60, 156) | El fichero contiene «manchones» para p. 60; no transcribe ese término de p. 156. No es un ibid. dirigido a otra obra. | Cotejar p. 156. Si no se confirma allí: «se dejan “manchones” (ibid.: 60)» con comillas latinas. | 04_fichero, fila p. 60; la segunda localización queda pendiente. |
| C10 | 2. Cómo leer: el espacio, las manos y el dibujo; «El ensamblaje tiene además una teoría propia,…»; L79 | dudoso | «con la condición de que haya una referencia explícita» | El registro da «com a condição de que haja uma referência explícita relativizada». La cita corta termina antes de un calificativo que podría limitar la condición. | Cotejar el contexto de Fuão p. 53; propuesta de traducción completa: «con la condición de que haya una referencia explícita relativizada». No decidir el sentido de «relativizada» sin el párrafo original. | 26 L324. Diferencia registrada; original completo pendiente. |
| C11 | 3. La chujlla: una casa a la medida del cuerpo; «El narrador tampoco le ve cuartos a…»; L114 | estilo | (ibid.), sin página explícita | Hay siete ibid. sin localizador escrito; se pueden resolver, pero la forma pedida es «(ibid.: página)». | L114→30; L160→103; L168→132; L218 primer ibid.→75 y segundo→80; L230 primer ibid.→155 y segundo→156. Escribir esas páginas, conservando las fuentes resueltas en el anexo B. | Anexo B: lista exhaustiva de las remisiones; no cambiar fuentes. |
| C12 | Preliminares; ««Mirando al pasado para caminar por el…»; L22 | estilo | Epígrafe y comillas del Cuadro 1 | El epígrafe lleva la referencia en otro bloque, y las cinco citas del cuadro usan solo páginas con la fuente bajo la tabla. Son excepciones de formato, no citas sin autor recuperable. | Para cumplir literalmente «mismo párrafo», unir el epígrafe y su atribución en el mismo bloque. Mantener la fuente del cuadro en L96 y aclarar en su título «según Botelho Gosálvez, 1982 [1945]». | L22-24 y L90-96; no añadir fuentes inventadas. |
| C13 | 4. Umacachi: la trampa de los papeles; «Los Villca llegan a la aldea con…»; L158 | dudoso | Versos de Pyramid of Bones y Father Electricity sin página ni localización interna | Las canciones no se paginan. El año está, pero falta un localizador utilizable; Father Electricity sigue sin fuente oficial disponible. | En Pyramid: añadir «s. p., pista 3» al citar el librillo identificado; en Father: «s. p., pista 6», y mantener el cotejo oficial pendiente. Añadir minuto solo después de escucharlo y medirlo. | 27 §27.12; lista de envío paso 8. No se han recibido las fotos del librillo en esta tarea. |
| C14 | 2. Cómo leer: el espacio, las manos y el dibujo; «\| 6. Centinela \| Cayado; vara de…»; L94 | dudoso | niebla (109); vara de Jilakata (73); mirada sobre la inmensidad (80) | El fichero no transcribe esos datos completos. Su ausencia no demuestra falsedad, pero impide validarlos solo con sus citas. | Cotejar pp.73,80 y109 antes de dar por revisado todo el Cuadro 1; no añadir comillas a estas paráfrasis. | 04_fichero y06; pendiente novela. |

### 3.1. Novela: comparación exhaustiva con el fichero

Se extrajeron **157 ocurrencias entre comillas** atribuidas a Botelho en la prosa y análisis de figuras, sin contar las cinco del cuadro, y se compararon con las filas del fichero. La comparación de cada cadena se hizo literalmente, sin quitar acentos, cambiar mayúsculas, modernizar palabras ni alterar puntuación interior. Resultado: **157 coincidencias; cero diferencias de texto**. La diferencia de página comprobable entre documentos es C01. C09 señala un localizador adicional sin su fragmento en el fichero.

Las referencias amplias contienen las páginas puntuales del fichero: L102 usa30-31 para fragmentos de30 y31; L118 usa22-23 para tres citas registradas en22; L130 usa36-37 para fragmentos de ambas; L180 usa134-135 para el andarivel134 y «Pensylvania»135; L190 usa141-143 para nichos141 y cuerpos143. No se clasifican como páginas equivocadas. Si se desea precisión, se puede citar cada fragmento con su página puntual. No se decide por el registro cuál es la página real del impreso.

Las dos citas en bloque, L31 y244, tienen localizadores9 y156-157, pero el fichero omite tramos con puntos suspensivos. Los segmentos transcritos coinciden; **la parte omitida no se puede cotejar letra por letra con ese documento**. Mantener pendiente el texto completo. Las correcciones de OCR declaradas en §2 del fichero tampoco equivalen a verificación del impreso.

Las cinco citas del cuadro se tratan aparte: «no tienen historia» coincide; «gallardete clavado» y «góticas» son subcadenas de las citas de p.109; «Muralla que condena el horizonte» cambia a mayúscula la inicial de «muralla» para abrir la celda, sin otra diferencia de esas palabras; «Fauces del abismo» carece de concordancia literal documentada. La mayúscula inicial no se debe presentar como corrupción del contenido de la novela.

### 3.2. Todas las citas sin fuente/página dentro del mismo párrafo

1. L7, «San Pablo»: nombre propio de la universidad, no una cita de fuente.
2. L22, el epígrafe: su atribución y página están en L24, dentro del bloque de epígrafe, pero fuera de la misma línea/párrafo de Markdown. Excepción formal recuperable; C12.
3. L90, «no tienen historia»: página22 en la celda y autor/año en L96.
4. L91, «gallardete clavado», «Fauces del abismo», «góticas», «Muralla que condena el horizonte»: páginas109/108 en la celda y autor/año en L96; no hay anonimato de obra, sí la cautela literal de C08.
5. L187, «Catavi»: se identifica como lectura de una tira de negativo y se da su código de archivo. No existe página que añadir. La fuente se localiza por código.
6. L29, «erial de piedras»: fuente y una página sí están en el párrafo, pero esa página no corresponde según el fichero; C01.
7. L158 y246, versos de canciones: autor/año presentes; falta un localizador no paginado; C13. Los títulos de canciones entre comillas de L73,118,158 y246 no son por sí solos extractos que exijan página.

Las restantes citas entre comillas de la prosa tienen una referencia bibliográfica y localizador recuperables en el mismo párrafo, incluso cuando la referencia sigue a varios fragmentos o precede a una cita tardía del párrafo (p.ej. «vieja historia» en L168). Esto no significa que cada literal esté respaldado por un original visible.

### 3.3. Omisiones y mediaciones

La ordenanza de L158 emplea **[...]**, como el fichero. No se encontró una omisión interior marcada como «…» que deba corregirse en el artículo. Los puntos suspensivos de las abreviaciones del fichero son parte de ese documento auxiliar, no del manuscrito. Los recortes al comienzo o al final de un fragmento no exigen insertar automáticamente [...]; sí exigen no suprimir un calificativo que cambie el alcance, como en C10.

Las citas secundarias identificadas: Hall vía Vázquez Ramos (L51), Bachelard vía Pallasmaa (L57), Cárcamo2019 vía2025b (L57), Bachelard vía Monteys/Fuertes (L232), y Kolář vía Fuão (L39, mediación explícita en prosa). Martin/Deleuze queda pendiente de la fuente; no se infiere su voz de un nombre mencionado en un registro. El *ibid.* dentro de la cita de Hall remite a Vázquez Ramos p.3, no al libro de Hall p.133. Las siete remisiones sin página escrita se detallan en C11 y anexo B.

### 3.4. Traducciones y originales disponibles en los registros

No se han recibido los originales de estas obras. «Disponible» aquí significa transcrito en un registro. No se corrigen traducciones de memoria ni se presentan como forzadas las metáforas que son del autor original.

| Localización | Traducción del artículo | Original registrado, junto a ella | Evaluación / propuesta |
|---|---|---|---|
| L55, Duviols8 | el doble mineral del cadáver sagrado | «le double minéral du cadavre sacré (mallqui)» —08 L99 | Traducción defendible; no falta el paréntesis si se cita solo el fragmento anterior. |
| L55, Duviols13 | al Huari que primero amojonó… | «Les pierres rurales commémorent le Huari qui le premier a borné tel champ, celui qui l’a clôturé, celui qui l’a défriché» —08 | El fragmento conserva las operaciones; no proponer cambiarlo sin el contexto. |
| L33, Ingold78 | no se construye: crece | «the mound is not built but grows» —08 L216 | Concordancia conceptual. Los dos puntos son decisión de traducción y no se cuentan como patrón de prosa propia. |
| L170, Ingold86 | es interrumpir de golpe la correspondencia | «is to bring the correspondence abruptly to a halt» —08 L219 | «Interrumpir bruscamente la correspondencia» sería más directo; la actual no tergiversa el fragmento. |
| L79, Fuão53 | referencia explícita | «uma referência explícita relativizada» —26 L324 | Falta el calificativo final; C10. |
| Nota L43, Fuão43 | reduplican su significado | «reduplicam seu significado» —26 L320 | Literal pero poco llano; R17. |
| L170, Fuão80 | separados por las gargantas de los abismos geográficos | «separadas pelas gargantas dos abismos geográficos» —26 L326 | Metáfora del original. No es evidencia de inflación introducida por el artículo. |
| L230, Alexander xiii | reparar el mundo a su alrededor, y dentro de él | «must also repair the world around it, and within it» —25 L336 | Referente del pronombre por revisar; R16. |
| L114, Alexander611 | sabe exactamente hasta dónde puede penetrar en la casa | «knows exactly how far into the house he may penetrate» —25 L356 | «Hasta dónde puede entrar» es más llano; no hay error semántico demostrado. La página puntual del registro es611. |
| L55, Dean5 | la petrificación señalaba la suspensión, pero no el fin, de la vida | «Petrifaction signaled the suspension of, but not an end to, life» —27 L236 | Conserva el sentido. |
| L246, Dean39 | recordar una versión del pasado exige olvidar o reprimir otra versión de ese mismo pasado | «Remembering one version of the past requires the forgetting or repressing of another version of that same past» —27 L237 | Conserva el sentido. |
| L77, Lundberg21 | con el realismo visual | «immersion is not to be confused with visual realism» —03 L41 | El complemento se integra sin alterar el sentido. |
| L158, The Voidz | juegan con otras reglas e insisten en que todo es igual | «they play the game by different rules, insisting / it's all equal» —27 L384-385 | Traducción razonable y corte de verso coincidente con el registro del librillo; no se ha visto el librillo aquí. |
| L246, Father Electricity | no quiero ver todo el desastre, ojalá pudiera vivir mirando atrás | «I do not want to see the whole mess / I wish I could live in retrospect» —27 L309 | «Mirando atrás» explicita la lectura de memoria; «en retrospectiva» sería más literal, pero tampoco resuelve por sí sola el sentido de vivir retrospectivamente. Fuente oficial pendiente. |

Frampton5, Scott3, Vázquez Ramos4 y Hall3/133 tienen traducciones o descripciones en los registros, pero allí no se reproduce junto a cada fragmento el original completo que permitiría una nueva comparación bilingüe. Lo mismo ocurre con la cita de Martin85. No se inventa ese original en esta tabla. La nota de traducciones es la segunda nota por orden de aparición, aunque su identificador Markdown sea `[^trad]`.

## 4. Referencias y afirmaciones de hecho

| N.º | Sección, primeras palabras y línea | Tipo | Qué dice el texto | Problema | Propuesta exacta | Respaldo |
|---|---|---|---|---|---|---|
| R01 | Bibliografía; «Cárcamo Pino, Mauricio Arnoldo (2019). "Thinking and…»; L300 | error | Títulos de artículos y capítulos entre comillas rectas | Nueve entradas incumplen las comillas latinas solicitadas. Las comillas de atributos Markdown no son parte de este problema. | Cambiar solo las delimitadoras de los títulos a «…» en L300,302,304,306,316,332,344,350 y356; conservar las comillas internas de Duviols en segundo nivel “huanca”. | AGENTS.md, regla de comillas. Libros y revistas ya llevan cursiva. |
| R02 | Bibliografía; «Cárcamo Pino, Mauricio Arnoldo (2019). "Thinking and…»; L300 | dudoso | Cham: Springer: 1411-1423 | La lista de envío registra la discrepancia con «Alicante: EGA, 2019». No elegir una ficha por preferencia ni mezclar sede de congreso y editorial de actas. | Mantener pendiente hasta comprobar la portada y la ficha del capítulo; separar editorial y páginas con puntuación uniforme una vez comprobadas. | Paso 7, Cárcamo Pino 2019; 04 tabla n.º 4. |
| R03 | Bibliografía; «Frampton, Kenneth (1995). *Studies in Tectonic Culture:…»; L318 | dudoso | Ed. John Cava. Cambridge, MA y Londres: MIT Press. | Ciudad y editor siguen pendientes de portada; el escaneo descrito en 07 solo contenía la introducción. | Cotejar portada y créditos; conservar la ficha provisional sin presentar los datos como verificados. | 07 §7.5 y paso 7, Frampton. |
| R04 | Bibliografía; «Le Guin, Ursula K. (2021 [1986]). "La…»; L332 | dudoso | https://es.theanarchistlibrary.org | Es la portada del sitio y no identifica la traducción citada. No se ha verificado un enlace exacto. | Sustituir la URL general por la URL específica del texto de Nedev y Pérez de Lama solo cuando se compruebe; mientras, marcar «URL exacta pendiente». | Paso 7, Le Guin; no se inventa un slug. |
| R05 | Bibliografía; «Alexander, Christopher; Ishikawa, Sara y Silverstein, Murray…»; L288 | dudoso | Páginas de Alexander, Scott y Martin | Que concuerden con un registro no confirma paginaciones reconstruidas o deducidas de índices. | Priorizar cotejo de Alexander xiii, xliii,395,405,610-611,621,1166; Scott 3; Martin 85. No trasladar páginas a una traducción castellana distinta. | 25 §25.7; 07 §7.1; 03 §3.2; paso 7. |
| R06 | Bibliografía; «Spedding, Alison (2025). "Piedras en el camino".…»; L350 | dudoso | Spedding XIII-XXIII; Rodríguez y Rodríguez 43-61; 2025 | El registro 16 precisa año y dirección editorial; no permite dar por cerrado el ISBN ni el final p. 61. No todos estos pendientes son errores de la ficha. | Mantener 2025 con respaldo de 16 y cotejar portadilla/colofón y fin del capítulo para XIII-XXIII y61. No añadir un ISBN incompleto. Respetar «alfonso borragán» en minúscula. | 15 y16, colofón; paso 7. |
| R07 | Bibliografía; «Cornejo Polar, Antonio (2003 [1994]). *Escribir en…»; L312 | dudoso | Cornejo Polar, 2003 [1994]:41,68,180,181 | Las páginas se vinculan a la segunda edición. El año original entre corchetes no autoriza a usar páginas de 1994. | Conservar la segunda edición de 2003 en todas las remisiones; si el autor elige 1994, recotejar todas las páginas citadas. | 08 §8.3; paso 7. |
| R08 | Bibliografía; «Bertonio, Ludovico (2011 [1612]). *Transcripción del vocabulario…»; L296 | dudoso | Bertonio, transcripción de 2011; jayintilla (p. 361) | No se ha visto el facsímil; además 16 transcribe Jayntilla, frente a jayintilla del artículo. Puede ser normalización, pero no está explicada. | Identificar la grafía adoptada y cotejar la transcripción digital p. 361 antes de cambiarla. Mantener 2011 [1612] y distinguir esa transcripción del impreso. | 16 §16.2; 08 ficha de Bertonio; paso 7. |
| R09 | Bibliografía; «Churata, Gamaliel (2007 [1957]). *El pez de…»; L308 | dudoso | Churata (2007 [1957]), p. 20 | La entrada describe correctamente una versión digital, no la edición de 1957. El archivo recibido da 2007 en portada y 2006 al cierre; falta una ubicación estable. | Añadir, si se aprueba, una nota: «La paginación corresponde a la versión digital de Rolando Diez de Medina, cuya portada fecha 2007; no a la edición de 1957». La URL queda pendiente hasta identificarla. | PDF recibido, hojas 1,20,364; 33 y paso 6. Cita p. 20 comprobada en imagen. |
| R10 | Bibliografía; «Churata, Gamaliel (2017). *Textos esenciales*. Recopilación y…»; L310 | estilo | Churata (2017), sin fechas originales de las piezas | La antología se identifica bien; las fechas 1936,1939 y1943 del cuerpo salen de los pies editoriales del PDF, no de periódicos originales consultados. | Añadir a una nota: «Las piezas de 1936, 1939 y 1943 se citan por la recopilación de 2017; sus fechas se toman de las notas editoriales de esa recopilación». No hace falta inventar tres entradas independientes. | PDF, pp. 109-110,123,129; cotejadas en esta auditoría. |
| R11 | 1. Introducción: una cosecha de piedras; «En Jatun-Kolla, el ayllu aymara que Raúl…»; L29 | dudoso | Raúl Botelho Gosálvez (1917-2004) | No lleva cita local, pero sí existe respaldo en el registro: 29 enlaza la autoridad BnF. No se volvió a abrir esa ficha en esta auditoría. | Añadir una nota de procedencia: «Las fechas de Botelho Gosálvez siguen la ficha de autoridad de la Bibliothèque nationale de France, ark:/12148/cb12175725j». Cotejo del catálogo pendiente. | 29 L88,224,228; 33 y lista de envío, mejoras opcionales. |
| R12 | 5. El éxodo: los Yungas y la mina; «La mina «Pensylvania», de la compañía yanqui…»; L180 | estilo | Foto de Siglo XX, Patiño, 1940-1946; Catavi | La ficha y la inscripción están registradas en 31 y30. La comparación de tamaños de casas es lectura visual; no prueba quién vivía en cada vivienda de la foto. | Cerrar la frase de la foto con «(Imagen 4; ficha LC-USE6-D-000117)». Mantener la descripción como observación; no identificar residentes. Para «Catavi», se cita la tira del negativo, no una página. | 31 L251,254-270; 30, tabla de derechos. Archivo original y ficha web no recotejados aquí. |
| R13 | 7. El retorno: reparar la casa, elegir la memoria; «Con las heladas vuelven los sobrevivientes, que…»; L230 | dudoso | la palabra compuestas, que los tratados de arquitectura reservaban al arquitecto | Afirmación histórica general sin tratado ni página identificados; no basta que sea una analogía sugerente. | La palabra «compuestas» permite leer la reparación de las pircas como una faena de recomposición comunal. | Sin respaldo localizado en el registro para la reserva exclusiva a arquitectos; fuente pendiente. |
| R14 | 1. Introducción: una cosecha de piedras; «[^pastel]: El pastel al óleo es pigmento…»; L43 | dudoso | el pastel… nunca termina de secar | Generalización técnica sin fuente identificada; las operaciones previstas no prueban esa propiedad de todos los productos. | El pastel al óleo permite volver a trabajar las capas de materia. Si se mantiene la afirmación sobre secado, aportar la ficha del material utilizado. | Fuente técnica pendiente; no se propone cambiar de técnica ni de material. |
| R15 | 1. Introducción: una cosecha de piedras; «Este artículo se pregunta, primero, qué sabe…»; L39 | estilo | Kolář citado por Fuão | La mediación se explica en prosa, pero no usa «cit. en», a diferencia de otras citas indirectas. | Después de la cita: «(Kolář, cit. en Fuão, 2011: 43)». No añadir año ni página de un original de Kolář no consultado. | 26 L319; fuente primaria de Kolář pendiente. |
| R16 | 7. El retorno: reparar la casa, elegir la memoria; «Con las heladas vuelven los sobrevivientes, que…»; L230 | dudoso | reparar el mundo a su alrededor, y dentro de él | El «it» del original registrado no tiene referente visible en el fragmento aislado; el español puede sugerir que se repara dentro del mundo. | Releer el párrafo de Alexander antes de fijar el referente. Si «it» es la construcción: «reparar el mundo que la rodea y el que queda en su interior». Propuesta condicionada, no corrección ya demostrada. | 25 L336: «must also repair the world around it, and within it»; contexto primario pendiente. |
| R17 | 1. Introducción: una cosecha de piedras; «[^pastel]: El pastel al óleo es pigmento…»; L43 | estilo | reduplican su significado | La traducción conserva el original registrado, pero el verbo resulta poco llano. | Alternativa a valorar: «duplican su significado»; mantener «reduplican» si el contexto distingue duplicación y refuerzo. | 26 L320: «reduplicam seu significado»; contexto completo pendiente. |
| R18 | 7. El retorno: reparar la casa, elegir la memoria; «Una pirca de doble cara enseña lo…»; L250 | dudoso | sin ese relleno el muro se cae | La definición de piedras de relleno de Bertonio no demuestra una regla constructiva absoluta para toda pirca. | Para la pirca de doble cara que usamos como analogía, el relleno ayuda a trabar los dos paramentos. Confirmar esta explicación con una fuente técnica del tipo de muro representado antes de incorporarla. | Bertonio246 y26 respaldan la analogía; comprobación técnica pendiente. |
| R19 | 2. Cómo leer: el espacio, las manos y el dibujo; «La oposición entre la mano que ara…»; L59 | dudoso | Churata vivía entonces en La Paz; Konkachi cerca de Chucuito, frente al Titikaka | Los pies de los textos dan lugar de publicación, no por sí solos residencia; p.123 menciona Chucuito, pero no fija una distancia ni todas las relaciones geográficas del artículo. | Para L59, «Churata defendió a Warisata en la prensa paceña»; para L114, «en el ayllu de Konkachi, en la región de Chucuito». Conservar las formulaciones más precisas solo con respaldo biográfico y geográfico. | PDF pp.109,123,129 y33; datos específicos pendientes. |

### 4.1. Correspondencia entre citas y bibliografía

Se revisaron las **36 entradas**. Todas tienen uso en el cuerpo o en una nota; no se encontró una obra citada por autor/año que falte en bibliografía, ni una entrada sin uso. Esa correspondencia no demuestra que todos los datos de las fichas sean correctos. Hay cuatro entradas de originales que solo se citan indirectamente: Cárcamo2019, Hall y las dos de Bachelard tienen mediadores explícitos, y no deben hacerse pasar por lecturas directas. Los autores nombrados como antecedentes o temas (Shakespeare, McLeod, Canaletto, Cullen, Lubetkin, Bacon, Ragone, Peirce) no se presentan como fuentes directamente consultadas: su ausencia como entradas independientes no es un desajuste automático.

| Entrada | Uso localizable en el artículo |
|---|---|
| Alexander1977 | L102,114,116,156,230 |
| Bachelard1978 [1942] | L57, vía Pallasmaa |
| Bachelard1983 [1957] | L232, vía Monteys y Fuertes |
| Barnadas1978 [1975] | L61,160 |
| Bertonio2011 [1612] | L37,55,170,208,218,230,250 |
| Botelho1982 [1945] | Desde L29; corpus principal |
| Cárcamo2019 | L57, vía2025b |
| Cárcamo2025a | L57,102 |
| Cárcamo2025b | L47,57,61,73,132 |
| Choque Canqui1978 [1974] | L276 |
| Churata2007 [1957] | L102 |
| Churata2017 | L59,114,276 |
| Cornejo Polar2003 [1994] | L45,160,180,260 |
| Dean2010 | L55,246 |
| Duviols1979 | L55 |
| Frampton1995 | L37,102 |
| Fuão2011 | Desde L39 y nota L43 |
| Garrington2013 | L83 |
| Guaman Poma1615 | L61,146,232 y pies |
| Hall1973 [1966] | L51, vía Vázquez Ramos |
| Ingold2013 | L33,75,170 |
| Julian Casablancas+The Voidz2014 | L246 |
| Le Guin2021 [1986] | L260 |
| Lundberg2019 | L77 |
| Martin2014 | L206 |
| Monteys y Fuertes2001 | Desde L61 |
| Pallasmaa2014 [2011] | L37,57,102 |
| Rivera Cusicanqui2010 [1984] | Epígrafe y L59,73,130,160 |
| Rodríguez y Rodríguez2025 | L250 |
| Scott2020 [1998] | L158 |
| Seguí2010 | L75,104 |
| Spedding2025 | L250 |
| Squier1877 | L120 y pie L127 |
| The Voidz2018 | L73,118,158 |
| Vázquez Ramos2023 | L51 |
| Zavaleta1986 | L53,158 |

La ficha BnF y la ficha de la Library of Congress son otras dos fuentes documentales de datos; no tienen entradas bibliográficas propias. Se localizan en R11-R12 y pueden incorporarse como notas de procedencia o recursos de archivo identificados. Los pies ya identifican la fotografía por archivo y código, de modo que no es una fuente anónima.

Formato: los años con corchetes se emplean de manera coherente para obra original/edición utilizada. No se exigen corchetes a toda antología de piezas anteriores si la ficha identifica la edición efectivamente consultada. Las páginas de capítulo figuran en Cárcamo2019, Choque, Duviols, Rodríguez/Rodríguez y Spedding; Choque tiene «s. p.» declarado. Los DOI visibles corresponden a Cárcamo2025a y Vázquez Ramos; la ausencia de DOI en otra entrada no demuestra por sí sola que haya que inventarlo. No se han consultado catálogos externos para completar editoriales, DOI o ciudades. Los rangos de páginas y el año entre corchetes no son millares que deban llevar punto.

### 4.2. Otros datos afirmados sin cita inmediata

| Dato y línea | Respaldo localizado | Estado y acción concreta |
|---|---|---|
| Nacimiento/muerte1917-2004, L29 | 29: ficha BnF con enlace; 33 y lista de envío | R11: añadir procedencia; catálogo primario pendiente. |
| Publicación de la novela en Buenos Aires1945 y concurso1940, L45 | 06, nota editorial; 29 §29.7; 33 | Respaldado por el registro de la edición; no verificadas la convocatoria original ni las otras novelas. Atribuirlo a la nota editorial, como ya se hace. |
| Churata puneño, residencia paceña, 1936/1939/1943, L59/114/276 | Portadilla y notas editoriales de Textos esenciales; 33 | Las fechas y lugares de las piezas están en los PDF cotejados. La biografía completa y «vivía entonces» no se reconstruyen únicamente de un lugar de publicación; mantener pendiente una referencia biográfica específica si se exige prueba de residencia. |
| Konkachi cerca de Chucuito/frente al Titikaka, L114 | PDF p.123 menciona Chucuito y describe la región; 33 | Relación regional plausible; distancia exacta y orientación no comprobadas. Propuesta prudente: «en el ayllu de Konkachi, en la región de Chucuito». |
| Treinta y cuatro ovejas y cincuenta bolivianos, L158 | Cautela de 04_fichero §1 y06; p.92 citada en el mismo párrafo | Cotejar pp.91-92 por duplicación de la transcripción. No declarar los datos verificados de nuevo. |
| Fotografía, empresa, fecha y ubicación de casas, L180/187 | 31 y30; ficha LC-USE6-D-000117 | R12. No inferir que las casas mayores de la foto son las de los ingenieros por analogía con la ficción. |
| Más de ciento cincuenta muertos, L230 | El artículo remite expresamente a p.156; registro de la trama | Fuente primaria pendiente; la cifra no carece de cita. |
| Explicación de domesticar/domus e hystéra, L162/208 | Se trata de análisis etimológicos reiterados en09 y16 | No se aportó diccionario etimológico primario; atribuir la función interpretativa al artículo y cotejar si se mantienen como hechos lingüísticos. |
| Compuestas en los tratados, L230 | No se localizó tratado ni página | R13. No dar por demostrado un uso reservado. |
| Pirca de doble cara y estabilidad por relleno, L250 | Registro de la analogía en26; Bertonio246 nombra piedras de relleno | La definición léxica sí tiene referencia; la afirmación constructiva «sin ese relleno el muro se cae» no está demostrada por esa definición. Si se mantiene literalmente, precisar el tipo de muro y aportar respaldo técnico; no universalizar. |
| Pastel que nunca seca, nota L43 | Operaciones descritas en los registros, sin ficha del material | R14: pendiente. |

## Anexo A. Cotejo de cada fragmento de las otras fuentes

Una fila por cada ocurrencia entre comillas no incluida en las 157 de la novela. Se conserva un comienzo breve para localizarla; no es una nueva transcripción de la fuente. **R** = coincide con un pasaje del registro en texto/página o con una traducción cuyo original está allí; **F** = cotejado en la imagen del PDF recibido; **P** = pendiente o sin respaldo literal. R no equivale a fuente primaria vista en esta auditoría. Los títulos, nombres propios y excepciones del cuadro no se fingen citas bibliográficas nuevas.

| N.º | Fragmento y línea | Referencia del artículo | Estado | Respaldo / límite |
|---|---|---|---|---|
| A001 | L7: «San Pablo» | Ver excepción | — | Nombre propio; no cita bibliográfica |
| A002 | L22: «Mirando al pasado para caminar por el presente y…» | Ver excepción | R | Atribución L24; 04 tabla de fuentes n.º15; p.17 pendiente original |
| A003 | L33: «no se construye: crece» | Ingold, 2013: 78 | R | 08 L216: original inglés, p.78; 09 L47: traducción |
| A004 | L37: «amontonar piedras sacándolas» | Bertonio, 2011 [1612]: 77 | R | 08 L29; comprobar localizador con la ficha de esa obra |
| A005 | L37: «que amontonan limpiando las chácaras» | ibid.: 330 | R | 08 L26; comprobar localizador con la ficha de esa obra |
| A006 | L37: «hincada en la pared para atar en ella los…» | ibid.: 330 | R | 08 L26; comprobar localizador con la ficha de esa obra |
| A007 | L37: «sepultura como casa sobre la tierra» | ibid.: 276 | R | 08 L74; comprobar localizador con la ficha de esa obra |
| A008 | L37: «las experiencias arquitectónicas básicas tienen carácter de verbos más…» | Pallasmaa, 2014 [2011]: 158 | R | 10 L28; comprobar localizador con la ficha de esa obra |
| A009 | L37: «apilamiento repetitivo de elementos pesados» | Frampton, 1995: 5 | R | 34 L329; comprobar localizador con la ficha de esa obra |
| A010 | L37: «ya sea piedra o adobe» | Frampton, 1995: 5 | R | 34 L330; comprobar localizador con la ficha de esa obra |
| A011 | L37: «componentes ligeros y lineales» | Frampton, 1995: 5 | R | 34 L331; comprobar localizador con la ficha de esa obra |
| A012 | L39: «En la vida nos cubrimos con una acumulación de…» | Fuão, 2011: 43 | R | 26 L319; comprobar localizador con la ficha de esa obra |
| A013 | L41: «estaban hechos básicamente de piedra» | ibid.: 14 | R | 26 L110; comprobar localizador con la ficha de esa obra |
| A014 | L41: «engranajes» | ibid.: 14 | R | 26 L110; comprobar localizador con la ficha de esa obra |
| A015 | L41: «reproducciones mecánicas» | ibid.: 14 | R | 26 L110; comprobar localizador con la ficha de esa obra |
| A016 | L41: «papeles» | ibid.: 14 | R | 26 L16; comprobar localizador con la ficha de esa obra |
| A017 | L43: «Si la cola añade, la *décollage* suprime» | Fuão, 2011: 43 | R | 26 L119; comprobar localizador con la ficha de esa obra |
| A018 | L43: «reduplican su significado» | Fuão, 2011: 43 | R | 26 L119; comprobar localizador con la ficha de esa obra |
| A019 | L43: «la segunda incisión» | ibid.: 29 | R | 27 L32; comprobar localizador con la ficha de esa obra |
| A020 | L43: «un segundo recorte desfigura la imagen rectangular inicial, dándole…» | ibid.: 29 | P | Sin respaldo literal en el registro; ver tabla C |
| A021 | L45: «ajeno al mundo indio aunque se solidarice con él» | Cornejo Polar, 2003 [1994]: 180 | R | 08 L16; comprobar localizador con la ficha de esa obra |
| A022 | L45: «más en términos de naturaleza que de historia» | Cornejo Polar, 2003 [1994]: 180 | R | 08 L16; comprobar localizador con la ficha de esa obra |
| A023 | L51: «no habla sobre la arquitectura, sino sobre nosotros» | Vázquez Ramos et al., 2023: 4 | R | 03 L111, p.4; original portugués no transcrito aquí |
| A024 | L51: «proyectan sobre el mundo visual del pasado las estructuras…» | Hall, 1973 [1966]: 133, cit. en ibid.: 3 | R | 03 L110, p.3, en infinitivo «proyectar»; localizador Hall133 no recotejado |
| A025 | L53: «dos concepciones que son ambas espacialistas» | Zavaleta Mercado, 1986: 29-30 | R | 08 L166; comprobar localizador con la ficha de esa obra |
| A026 | L53: «archipiélago» | Zavaleta Mercado, 1986: 29-30 | R | 08 L19; comprobar localizador con la ficha de esa obra |
| A027 | L53: «este espacio no puede concebirse sin otro espacio» | Zavaleta Mercado, 1986: 29-30 | R | 08 L165; comprobar localizador con la ficha de esa obra |
| A028 | L53: «el dominio final del suelo como atribución ligada a…» | Zavaleta Mercado, 1986: 29-30 | R | 08 L166; comprobar localizador con la ficha de esa obra |
| A029 | L55: «piedra muy grande» | Bertonio, 2011 [1612]: 506 | R | 08 L33; comprobar localizador con la ficha de esa obra |
| A030 | L55: «contenido religioso» | Duviols, 1979: 8 | R | 08 L33; comprobar localizador con la ficha de esa obra |
| A031 | L55: «el doble mineral del cadáver sagrado» | Duviols, 1979: 8 | R | 08 L99: original francés, p.8 |
| A032 | L55: «al Huari que primero amojonó tal campo, al que…» | ibid.: 13 | R | 08 L32; comprobar localizador con la ficha de esa obra |
| A033 | L55: «la petrificación señalaba la suspensión, pero no el fin,…» | Dean, 2010: 5 | R | 27 L236; comprobar localizador con la ficha de esa obra |
| A034 | L57: «La vista las nombra, pero la mano las conoce» | Bachelard, 1978 [1942]: 7-8, cit. en Pallasmaa, 2014 [2011]: 53 | R | 10 L27; comprobar localizador con la ficha de esa obra |
| A035 | L57: «neologismo homólogo al lenguaje, pero con las manos» | Cárcamo Pino, 2019: 1412, cit. en Cárcamo Pino, 2025b: 244 | P | Sin respaldo literal en el registro; ver tabla C |
| A036 | L57: «sujetar un papel con dos yemas dactilares» | Cárcamo Pino, 2025a: 10 | P | Sin respaldo literal en el registro; ver tabla C |
| A037 | L59: «La única comunidad libre que subsistía en la región» | ibid.: 150 | R | 08 L127; comprobar localizador con la ficha de esa obra |
| A038 | L59: «era una antigua pelea de linderos» | ibid.: 150 | R | 08 L127; comprobar localizador con la ficha de esa obra |
| A039 | L59: «mientras Caquiaviri se enquista en la aldea, Warisata lo…» | Churata, 2017: 109-110 | F | Textos esenciales, p.109 y110, hojas107-108; coincidencia de palabras en imagen; fechas por nota editorial |
| A040 | L59: «debe asentarse en el ayllu, que es de donde…» | Churata, 2017: 109-110 | F | Textos esenciales, p.109 y110, hojas107-108; coincidencia de palabras en imagen; fechas por nota editorial |
| A041 | L59: «crimen cometido con la escuela de Warisata» | ibid.: 129 | F | Textos esenciales, p.129, hoja127; coincidencia de palabras en imagen; fechas por nota editorial |
| A042 | L59: «Posteriormente destruirían también a Warisata» | Rivera Cusicanqui, 2010 [1984]: 105 | R | 08 L123; comprobar localizador con la ficha de esa obra |
| A043 | L61: «minusvaloradas, invisibilizadas» | Cárcamo Pino, 2025b: 259 | R | 02 L25, 2025b p.259 |
| A044 | L61: «monopolio de la escritura y el lenguaje» | Cárcamo Pino, 2025b: 259 | R | 27 L166; comprobar localizador con la ficha de esa obra |
| A045 | L61: «lenta y sistemática» | Monteys y Fuertes, 2001: 26 | R | 26 L130; comprobar localizador con la ficha de esa obra |
| A046 | L61: «una opinión no escrita pero de innegable valor» | Monteys y Fuertes, 2001: 26 | R | 26 L130; comprobar localizador con la ficha de esa obra |
| A047 | L73: «inventado in situ por los personajes» | Cárcamo Pino, 2025b: 241-242 | R | 27 L170; comprobar localizador con la ficha de esa obra |
| A048 | L73: «con la mano de Shakespeare, no con la boca» | Cárcamo Pino, 2025b: 241-242 | R | 27 L172; comprobar localizador con la ficha de esa obra |
| A049 | L73: «All Wordz Are Made Up» | The Voidz, 2018 | R | 27 L8; comprobar localizador con la ficha de esa obra |
| A050 | L75: «servir como ilustración de un texto narrativo previo» | Seguí de la Riva, 2010: 93 | R | 08 L18; comprobar localizador con la ficha de esa obra |
| A051 | L75: «especifican» | Ingold, 2013: 125 | R | 34 L371; comprobar localizador con la ficha de esa obra |
| A052 | L75: «mostraban cómo construir, montar o incluso reparar» | Monteys y Fuertes, 2001: 128, 132 | R | 26 L134; comprobar localizador con la ficha de esa obra |
| A053 | L75: «personas haciendo cosas» | Monteys y Fuertes, 2001: 128, 132 | R | 26 L135; comprobar localizador con la ficha de esa obra |
| A054 | L75: «Dibujar es dejar huellas estables en un soporte a…» | Seguí de la Riva, 2010: 13 | R | 08 L233; comprobar localizador con la ficha de esa obra |
| A055 | L77: «completamente imaginaria» | ibid.: 3 | P | Sin respaldo literal en el registro; ver tabla C |
| A056 | L77: «con el realismo visual» | ibid.: 21 | R | 03 L41: original inglés, p.21 |
| A057 | L79: «intervalo» | Fuão, 2011: 8, 52 | R | 26 L86; comprobar localizador con la ficha de esa obra |
| A058 | L79: «antes de que la cola las fije» | Fuão, 2011: 8, 52 | R | 26 L126; comprobar localizador con la ficha de esa obra |
| A059 | L79: «con la condición de que haya una referencia explícita» | ibid.: 53 | R | 26 L127; comprobar localizador con la ficha de esa obra |
| A060 | L79: «no cabe en una sola casa» | Monteys y Fuertes, 2001: 12 | R | 26 L89; comprobar localizador con la ficha de esa obra |
| A061 | L81: «la mejor evidencia del recorte» | Fuão, 2011: 39 | R | 26 L278; comprobar localizador con la ficha de esa obra |
| A062 | L81: «una sutura de cuatro puntos» | Fuão, 2011: 39 | R | 26 L278; comprobar localizador con la ficha de esa obra |
| A063 | L90: «no tienen historia» | Ver excepción | R | Cuadro 1; fuente general L96; ver §2.3 yC08 |
| A064 | L91: «gallardete clavado» | Ver excepción | R | Cuadro 1; fuente general L96; ver §2.3 yC08 |
| A065 | L91: «Fauces del abismo» | Ver excepción | P | Cuadro 1; fuente general L96; ver §2.3 yC08 |
| A066 | L91: «góticas» | Ver excepción | R | Cuadro 1; fuente general L96; ver §2.3 yC08 |
| A067 | L91: «Muralla que condena el horizonte» | Ver excepción | R | Cuadro 1; fuente general L96; ver §2.3 yC08 |
| A068 | L102: «ella misma deviene utensilio» | Monteys y Fuertes, 2001: 112 | R | 26 L143; comprobar localizador con la ficha de esa obra |
| A069 | L102: «una casa es una vivienda más la gente que…» | ibid.: 14 | R | 26 L89; comprobar localizador con la ficha de esa obra |
| A070 | L102: «las cosas que cuentan tu historia» | Alexander et al., 1977: 1166 | R | 25 L121; comprobar localizador con la ficha de esa obra |
| A071 | L102: «la casa es una metáfora del cuerpo y el…» | Pallasmaa, 2014 [2011]: 159 | R | 10 L31; comprobar localizador con la ficha de esa obra |
| A072 | L102: «una de las paredes de su chuklla en abecedario…» | Churata, 2007 [1957]: 20 | F | El pez de oro, versión digital, hoja/p.20; coincidencia literal en imagen |
| A073 | L104: «empieza siendo un corte, sajadura de cualquier cosa, rotura,…» | Seguí de la Riva, 2010: 97 | R | 08 L241; comprobar localizador con la ficha de esa obra |
| A074 | L104: «Desde dentro es el único posicionamiento para la acción.…» | ibid.: 23 | R | 08 L234; comprobar localizador con la ficha de esa obra |
| A075 | L104: «eliminan una pared» | Monteys y Fuertes, 2001: 30 | R | 26 L156; comprobar localizador con la ficha de esa obra |
| A076 | L104: «en reposo» | Monteys y Fuertes, 2001: 58 | R | 26 L158; comprobar localizador con la ficha de esa obra |
| A077 | L104: «desde el punto de vista de quien va a…» | Monteys y Fuertes, 2001: 58 | R | 26 L158; comprobar localizador con la ficha de esa obra |
| A078 | L114: «sabe exactamente hasta dónde puede penetrar en la casa» | Alexander et al., 1977: 610-611 | R | 25 L65; comprobar localizador con la ficha de esa obra |
| A079 | L114: «el resultado de una operación de agregación, más que…» | Monteys y Fuertes, 2001: 56 | R | 26 L342; comprobar localizador con la ficha de esa obra |
| A080 | L114: «no tiene dos metros» | Churata, 2017: 123 | F | Textos esenciales, p.123, hoja121; coincidencia de palabras en imagen; fechas por nota editorial |
| A081 | L114: «dos habitaciones que hacen ángulo» | Churata, 2017: 123 | F | Textos esenciales, p.123, hoja121; coincidencia de palabras en imagen; fechas por nota editorial |
| A082 | L114: «esa habitación principal de la vivienda indígena» | Churata, 2017: 123 | F | Textos esenciales, p.123, hoja121; coincidencia de palabras en imagen; fechas por nota editorial |
| A083 | L114: «charlar con los amigos» | Churata, 2017: 123 | F | Textos esenciales, p.123, hoja121; coincidencia de palabras en imagen; fechas por nota editorial |
| A084 | L114: «en una simple cabaña de una sola habitación» | Alexander et al., 1977: xliii | R | 25 L53; comprobar localizador con la ficha de esa obra |
| A085 | L116: «la comida y el fuego» | Alexander et al., 1977: 621 | R | 25 L75; comprobar localizador con la ficha de esa obra |
| A086 | L116: «un modo de domesticar el fuego» | Monteys y Fuertes, 2001: 104 | R | 26 L151; comprobar localizador con la ficha de esa obra |
| A087 | L116: «que pervive aun hoy en la tradición rural» | Monteys y Fuertes, 2001: 104 | R | 26 L25; comprobar localizador con la ficha de esa obra |
| A088 | L116: «se cocina, se trabaja, se recibe o se duerme,…» | Monteys y Fuertes, 2001: 104 | R | 26 L344; comprobar localizador con la ficha de esa obra |
| A089 | L116: «casi arquetípico» | Alexander et al., 1977: 611 | R | 25 L131; comprobar localizador con la ficha de esa obra |
| A090 | L118: «Pyramid of Bones» | The Voidz, 2018 | R | 27 L18; comprobar localizador con la ficha de esa obra |
| A091 | L120: «tallando una cruz» | ibid.: 302-303 | R | 31 L257: «cutting out a cross», pp.302-303 |
| A092 | L120: «como parte integrante de los monumentos» | ibid.: 302-303 | R | 31 L258: original inglés, p.303 |
| A093 | L130: «a desenterrar antiguos títulos de propiedad» | Rivera Cusicanqui, 2010 [1984]: 99 | R | 08 L47; comprobar localizador con la ficha de esa obra |
| A094 | L130: «una pieza clave en la lucha legal» | Rivera Cusicanqui, 2010 [1984]: 99 | R | 08 L47; comprobar localizador con la ficha de esa obra |
| A095 | L130: «destrucción simbólica de mojones o linderos» | ibid.: 125 | R | 08 L126; comprobar localizador con la ficha de esa obra |
| A096 | L132: «en sentido fuerte» | Cárcamo Pino, 2025b: 259 | R | 27 L165; comprobar localizador con la ficha de esa obra |
| A097 | L132: «no escribe, inscribe» | Fuão, 2011: 36 | R | 26 L162; comprobar localizador con la ficha de esa obra |
| A098 | L132: «en profundidad» | Fuão, 2011: 36 | R | 26 L162; comprobar localizador con la ficha de esa obra |
| A099 | L156: «a ciegas» | Alexander et al., 1977: 405 | R | 25 L143; comprobar localizador con la ficha de esa obra |
| A100 | L158: «un instrumento al servicio de la razón» | Fuão, 2011: 33-35 | R | 26 L168; comprobar localizador con la ficha de esa obra |
| A101 | L158: «entre lo incluido y lo excluido, el dentro y…» | Fuão, 2011: 33-35 | R | 26 L168; comprobar localizador con la ficha de esa obra |
| A102 | L158: «no se limita a describir un sistema de tenencia…» | Scott, 2020 [1998]: 3 | R | 07 L62; comprobar localizador con la ficha de esa obra |
| A103 | L158: «la fuerza de la ley» | Scott, 2020 [1998]: 3 | R | 34 L423; comprobar localizador con la ficha de esa obra |
| A104 | L158: «Pyramid of Bones» | The Voidz, 2018 | R | 27 L18; comprobar localizador con la ficha de esa obra |
| A105 | L158: «they play the game by different rules, insisting /…» | The Voidz, 2018 | R | 27 L302; comprobar localizador con la ficha de esa obra |
| A106 | L158: «de dudosa cuantificación como Bolivia» | Zavaleta Mercado, 1986: 21, n. 1 | R | 08 L164; comprobar localizador con la ficha de esa obra |
| A107 | L160: «mucho más fetiche que texto y mucho más gesto…» | Cornejo Polar, 2003 [1994]: 41 | R | 08 L51; comprobar localizador con la ficha de esa obra |
| A108 | L160: «abogados de pueblo (peyorativamente designados como “tinterillos”)» | Rivera Cusicanqui, 2010 [1984]: 101 | R | 08 L50; comprobar localizador con la ficha de esa obra |
| A109 | L160: «la manifestación embrionaria del indigenismo criollo» | Rivera Cusicanqui, 2010 [1984]: 101 | R | 08 L50; comprobar localizador con la ficha de esa obra |
| A110 | L160: «doctrinas» | Barnadas, 1978 [1975]: 46-47 | R | 34 L430; comprobar localizador con la ficha de esa obra |
| A111 | L160: «los encargados de consignar por escrito sus reclamaciones» | Barnadas, 1978 [1975]: 46-47 | R | 33 L74; comprobar localizador con la ficha de esa obra |
| A112 | L166: «una casa compuesta de piezas dispersas en el territorio» | Monteys y Fuertes, 2001: 146 | R | 26 L176; comprobar localizador con la ficha de esa obra |
| A113 | L170: «montón de piedras, que por superstición van haciendo los…» | Bertonio, 2011 [1612]: 317 | R | 08 L76; comprobar localizador con la ficha de esa obra |
| A114 | L170: «coca mascada con las manos» | ibid.: 349 | R | 08 L40; comprobar localizador con la ficha de esa obra |
| A115 | L170: «el cimiento» | ibid.: 486 | R | 08 L81; comprobar localizador con la ficha de esa obra |
| A116 | L170: «el horizonte o término de la tierra» | ibid.: 486 | R | 08 L81; comprobar localizador con la ficha de esa obra |
| A117 | L170: «es interrumpir de golpe la correspondencia» | Ingold, 2013: 86 | R | 08 L219: original inglés, p.86 |
| A118 | L170: «el abismo del recorte» | Fuão, 2011: 80 | R | 26 L180; comprobar localizador con la ficha de esa obra |
| A119 | L170: «separados por las gargantas de los abismos geográficos» | Fuão, 2011: 80 | R | 26 L180; comprobar localizador con la ficha de esa obra |
| A120 | L180: «como puros soportes físicos» | Cornejo Polar, 2003 [1994]: 68 | R | 08 L182; comprobar localizador con la ficha de esa obra |
| A121 | L180: «conexión física entre representante y representado» | Fuão, 2011: 28 | R | 26 L184; comprobar localizador con la ficha de esa obra |
| A122 | L180: «el control sobre los cuerpos» | ibid.: 48 | R | 26 L322; comprobar localizador con la ficha de esa obra |
| A123 | L180: «registro institucional» | ibid.: 48 | R | 26 L185; comprobar localizador con la ficha de esa obra |
| A124 | L187: «Catavi» | Ver excepción | R | 31 L270, inscripción del negativo; sin página |
| A125 | L190: «más técnica, más mecánica, un juntar y pegar» | Fuão, 2011: 102 | R | 26 L189; comprobar localizador con la ficha de esa obra |
| A126 | L190: «de la cultura industrial, del montaje de turbinas, de…» | ibid.: 97 | R | 26 L189; comprobar localizador con la ficha de esa obra |
| A127 | L206: «separados del cuerpo original» | Fuão, 2011: 16 | R | 26 L196; comprobar localizador con la ficha de esa obra |
| A128 | L206: «distanciados unos de otros» | Fuão, 2011: 16 | R | 26 L196; comprobar localizador con la ficha de esa obra |
| A129 | L206: «las manipulaciones de la carne» | Martin, 2014: 85 | P | Sin respaldo literal en el registro; ver tabla C |
| A130 | L206: «mediante un distanciamiento de la mirada y el ocultamiento…» | Fuão, 2011: 24 | R | 26 L297; comprobar localizador con la ficha de esa obra |
| A131 | L208: «nombre de reverencia» | Bertonio, 2011 [1612]: 420 | R | 08 L79; comprobar localizador con la ficha de esa obra |
| A132 | L208: «yo seré tu hijo» | Bertonio, 2011 [1612]: 420 | R | 08 L79; comprobar localizador con la ficha de esa obra |
| A133 | L218: «la cepa de una casa o familia» | Bertonio, 2011 [1612]: 307 | R | 08 L36; comprobar localizador con la ficha de esa obra |
| A134 | L218: «término o mojón de las tierras» | Bertonio, 2011 [1612]: 307 | R | 08 L36; comprobar localizador con la ficha de esa obra |
| A135 | L218: «el montón de piedras puesto por mojón» | ibid.: 447 | R | 08 L341; comprobar localizador con la ficha de esa obra |
| A136 | L218: «en quien hallan todo amparo» | ibid.: 447 | P | Sin respaldo literal en el registro; ver tabla C |
| A137 | L218: «Amparo, defensor, refugio, padre» | ibid.: 447 | R | 09 L34, p.447 |
| A138 | L218: «aguarda y guarda» | Fuão, 2011: 65 | R | 26 L201; comprobar localizador con la ficha de esa obra |
| A139 | L230: «aglutina, reúne, lo que fue disperso» | Fuão, 2011: 81 | R | 26 L208; comprobar localizador con la ficha de esa obra |
| A140 | L230: «cubierta, techo de la casa» | Bertonio, 2011 [1612]: 132 | R | 13 L77; comprobar localizador con la ficha de esa obra |
| A141 | L230: «mojonar las chácaras con montones de piedra» | ibid.: 466 | R | 08 L80; comprobar localizador con la ficha de esa obra |
| A142 | L230: «el poder legal y la oportunidad física de modificar…» | Alexander et al., 1977: 395 | R | 25 L93; comprobar localizador con la ficha de esa obra |
| A143 | L230: «reparar el mundo a su alrededor, y dentro de…» | ibid.: xiii | R | 25 L94; comprobar localizador con la ficha de esa obra |
| A144 | L232: «los gestos más finos, los gestos primeros, son súbitamente…» | Bachelard, 1983 [1957]: 45, cit. en Monteys y Fuertes, 2001: 42 | R | 26 L341; comprobar localizador con la ficha de esa obra |
| A145 | L232: «la casa natal ha inscrito en nosotros la jerarquía…» | Bachelard, 1983 [1957]: 45, cit. en Monteys y Fuertes, 2001: 42 | R | 26 L341; comprobar localizador con la ficha de esa obra |
| A146 | L232: «ayau haylli yau» | Guaman Poma de Ayala, 1615: 1153 [1163]; Imagen 5 | R | 34 L466; comprobar localizador con la ficha de esa obra |
| A147 | L246: «memorias materializadas» | Dean, 2010: 39 | R | 27 L237; comprobar localizador con la ficha de esa obra |
| A148 | L246: «recordar una versión del pasado exige olvidar o reprimir…» | Dean, 2010: 39 | R | 27 L237; comprobar localizador con la ficha de esa obra |
| A149 | L246: «la ilusión de integridad» | Fuão, 2011: 88 | R | 26 L212; comprobar localizador con la ficha de esa obra |
| A150 | L246: «no cura ni salva, solo cierra la boca de…» | Fuão, 2011: 88 | R | 26 L212; comprobar localizador con la ficha de esa obra |
| A151 | L246: «cierra cicatrices» | ibid.: 91 | R | 26 L212; comprobar localizador con la ficha de esa obra |
| A152 | L246: «Father Electricity» | Julian Casablancas+The Voidz, 2014 | R | 27 L81; comprobar localizador con la ficha de esa obra |
| A153 | L246: «I do not want to see the whole mess…» | Julian Casablancas+The Voidz, 2014 | R | 27 L309; comprobar localizador con la ficha de esa obra |
| A154 | L248: «son la casa» | Monteys y Fuertes, 2001: 148 | R | 26 L219; comprobar localizador con la ficha de esa obra |
| A155 | L250: «Piedra para entremeter en los edificios y llenar sus…» | Bertonio, 2011 [1612]: 246 | R | 08 L73; comprobar localizador con la ficha de esa obra |
| A156 | L250: «corazón de piedra» | Spedding, 2025: XV | R | 15 L1; comprobar localizador con la ficha de esa obra |
| A157 | L250: «hay que lamer el batán de moler» | Spedding, 2025: XV | R | 15 L18; comprobar localizador con la ficha de esa obra |
| A158 | L250: «volverse piedra o endurecerse» | Bertonio, 2011 [1612]: 444 | R | 16 L146; comprobar localizador con la ficha de esa obra |
| A159 | L250: «retornar al territorio y a la memoria» | Rodríguez y Rodríguez, 2025: 55 | R | 34 L479; comprobar localizador con la ficha de esa obra |
| A160 | L260: «Una novela es un botiquín» | Le Guin, 2021 [1986]: 10 | R | 07 L146; comprobar localizador con la ficha de esa obra |
| A161 | L260: «que contiene cosas en una relación particular, poderosa, entre…» | Le Guin, 2021 [1986]: 10 | R | 09 L46, traducción p.10 |
| A162 | L260: «un recipiente para personas» | ibid.: 8 | R | 07 L18; comprobar localizador con la ficha de esa obra |
| A163 | L260: «estado sólido, siempre repetido» | Cornejo Polar, 2003 [1994]: 181 | R | 08 L185; comprobar localizador con la ficha de esa obra |
| A164 | L260: «Necesita un escenario, o un pedestal, o una cima» | Le Guin, 2021 [1986]: 11 | R | 07 L152; comprobar localizador con la ficha de esa obra |
| A165 | L274: «no son neutros» | Fuão, 2011: 8 | R | 26 L88; comprobar localizador con la ficha de esa obra |
| A166 | L276: «hace tiempo, hemos añorado por escribir» | Choque Canqui, 1978 [1974]: s. p. | R | 34 L486; comprobar localizador con la ficha de esa obra |
| A167 | L276: «juguetes cubistas» | Churata, 2017: 123 | F | Textos esenciales, p.123, hoja121; coincidencia de palabras en imagen; fechas por nota editorial |

El anexo A incluye también coincidencias de traducción reconocidas por su original, no solo búsquedas de la misma cadena española. En Fuão y Monteys/Fuertes se contrastaron las páginas de las tablas de26 §26.7; en Alexander, la tabla de25 §25.7. Los rangos conjuntos (p.ej.128,132 o33-35) engloban las páginas puntuales del registro; no se declararon diferencias por el solo hecho de ser rangos. C10 yR16-R17 especifican los puntos de traducción que requieren volver al contexto.

## Anexo B. Resolución de todas las remisiones ibid.

Se mantiene el orden de aparición. Las notas se leyeron también como unidades independientes: sus referencias a Fuão no alteran el resultado porque nombran la misma obra que estaba activa en la prosa correspondiente. Los pies de imágenes identifican recursos visuales y no sustituyen sin aviso el antecedente de las citas literarias. Ninguna remisión termina en una obra equivocada en esta versión. Las páginas resueltas no quedan por ello verificadas contra un original.

| N.º | Línea | Remisión | Obra y página resueltas |
|---|---|---|---|
| 1 | L31 | ibid.: 9 | Botelho Gosálvez, 1982 [1945]: 9 |
| 2 | L33 | ibid.: 8 | Botelho Gosálvez, 1982 [1945]: 8 |
| 3 | L33 | ibid.: 35 | Botelho Gosálvez, 1982 [1945]: 35 |
| 4 | L33 | ibid.: 154 | Botelho Gosálvez, 1982 [1945]: 154 |
| 5 | L37 | ibid.: 330 | Bertonio, 2011 [1612]: 330 |
| 6 | L37 | ibid.: 276 | Bertonio, 2011 [1612]: 276 |
| 7 | L41 | ibid.: 14 | Fuão, 2011: 14 |
| 8 | L43 | ibid.: 29 | Fuão, 2011: 29 |
| 9 | L45 | ibid.: 5 | Botelho Gosálvez, 1982 [1945]: 5 |
| 10 | L45 | ibid.: 145 | Botelho Gosálvez, 1982 [1945]: 145 |
| 11 | L51 | Hall, 1973 [1966]: 133, cit. en ibid.: 3 | Vázquez Ramos et al., 2023: 3 |
| 12 | L55 | ibid.: 13 | Duviols, 1979: 13 |
| 13 | L55 | ibid.: 30 | Botelho Gosálvez, 1982 [1945]: 30 |
| 14 | L55 | ibid.: 133 | Botelho Gosálvez, 1982 [1945]: 133 |
| 15 | L57 | ibid.: 96 | Botelho Gosálvez, 1982 [1945]: 96 |
| 16 | L59 | ibid.: 5 | Botelho Gosálvez, 1982 [1945]: 5 |
| 17 | L59 | ibid.: 150 | Rivera Cusicanqui, 2010 [1984]: 150 |
| 18 | L59 | ibid.: 129 | Churata, 2017: 129 |
| 19 | L77 | ibid.: 3 | Lundberg, 2019: 3 |
| 20 | L77 | ibid.: 21 | Lundberg, 2019: 21 |
| 21 | L79 | ibid.: 53 | Fuão, 2011: 53 |
| 22 | L102 | ibid.: 30-31 | Botelho Gosálvez, 1982 [1945]: 30-31 |
| 23 | L102 | ibid.: 14 | Monteys y Fuertes, 2001: 14 |
| 24 | L102 | ibid.: 34 | Botelho Gosálvez, 1982 [1945]: 34 |
| 25 | L102 | ibid.: 31 | Botelho Gosálvez, 1982 [1945]: 31 |
| 26 | L104 | ibid.: 10 | Botelho Gosálvez, 1982 [1945]: 10 |
| 27 | L104 | ibid.: 23 | Seguí de la Riva, 2010: 23 |
| 28 | L114 | ibid.: 30 | Botelho Gosálvez, 1982 [1945]: 30 |
| 29 | L114 | ibid. | Botelho Gosálvez, 1982 [1945]: 30 |
| 30 | L114 | ibid.: 31 | Botelho Gosálvez, 1982 [1945]: 31 |
| 31 | L116 | ibid.: 32 | Botelho Gosálvez, 1982 [1945]: 32 |
| 32 | L118 | ibid.: 28 | Botelho Gosálvez, 1982 [1945]: 28 |
| 33 | L118 | ibid.: 22-23 | Botelho Gosálvez, 1982 [1945]: 22-23 |
| 34 | L118 | ibid.: 163 | Botelho Gosálvez, 1982 [1945]: 163 |
| 35 | L120 | ibid.: 302-303 | Squier, 1877: 302-303 |
| 36 | L130 | ibid.: 36-37 | Botelho Gosálvez, 1982 [1945]: 36-37 |
| 37 | L130 | ibid.: 125 | Rivera Cusicanqui, 2010 [1984]: 125 |
| 38 | L132 | ibid.: 35 | Botelho Gosálvez, 1982 [1945]: 35 |
| 39 | L132 | ibid.: 9 | Botelho Gosálvez, 1982 [1945]: 9 |
| 40 | L146 | ibid.: 86 | Botelho Gosálvez, 1982 [1945]: 86 |
| 41 | L146 | ibid.: 29 | Botelho Gosálvez, 1982 [1945]: 29 |
| 42 | L156 | ibid.: 101 | Botelho Gosálvez, 1982 [1945]: 101 |
| 43 | L158 | ibid.: 96 | Botelho Gosálvez, 1982 [1945]: 96 |
| 44 | L158 | ibid.: 103 | Botelho Gosálvez, 1982 [1945]: 103 |
| 45 | L160 | ibid. | Botelho Gosálvez, 1982 [1945]: 103 |
| 46 | L160 | ibid.: 104 | Botelho Gosálvez, 1982 [1945]: 104 |
| 47 | L160 | ibid.: 105 | Botelho Gosálvez, 1982 [1945]: 105 |
| 48 | L162 | ibid.: 105 | Botelho Gosálvez, 1982 [1945]: 105 |
| 49 | L162 | ibid.: 107 | Botelho Gosálvez, 1982 [1945]: 107 |
| 50 | L166 | ibid.: 7 | Botelho Gosálvez, 1982 [1945]: 7 |
| 51 | L168 | ibid.: 113 | Botelho Gosálvez, 1982 [1945]: 113 |
| 52 | L168 | ibid.: 123 | Botelho Gosálvez, 1982 [1945]: 123 |
| 53 | L168 | ibid.: 129 | Botelho Gosálvez, 1982 [1945]: 129 |
| 54 | L168 | ibid.: 125 | Botelho Gosálvez, 1982 [1945]: 125 |
| 55 | L168 | ibid.: 132 | Botelho Gosálvez, 1982 [1945]: 132 |
| 56 | L168 | ibid. | Botelho Gosálvez, 1982 [1945]: 132 |
| 57 | L168 | ibid.: 154 | Botelho Gosálvez, 1982 [1945]: 154 |
| 58 | L168 | ibid.: 121 | Botelho Gosálvez, 1982 [1945]: 121 |
| 59 | L170 | ibid.: 33 | Botelho Gosálvez, 1982 [1945]: 33 |
| 60 | L170 | ibid.: 109 | Botelho Gosálvez, 1982 [1945]: 109 |
| 61 | L170 | ibid.: 121 | Botelho Gosálvez, 1982 [1945]: 121 |
| 62 | L170 | ibid.: 349 | Bertonio, 2011 [1612]: 349 |
| 63 | L170 | ibid.: 486 | Bertonio, 2011 [1612]: 486 |
| 64 | L180 | ibid.: 135 | Botelho Gosálvez, 1982 [1945]: 135 |
| 65 | L180 | ibid.: 140 | Botelho Gosálvez, 1982 [1945]: 140 |
| 66 | L180 | ibid.: 48 | Fuão, 2011: 48 |
| 67 | L180 | ibid.: 142 | Botelho Gosálvez, 1982 [1945]: 142 |
| 68 | L190 | ibid.: 141-143 | Botelho Gosálvez, 1982 [1945]: 141-143 |
| 69 | L190 | ibid.: 144 | Botelho Gosálvez, 1982 [1945]: 144 |
| 70 | L190 | ibid.: 145 | Botelho Gosálvez, 1982 [1945]: 145 |
| 71 | L190 | ibid.: 151 | Botelho Gosálvez, 1982 [1945]: 151 |
| 72 | L190 | ibid.: 97 | Fuão, 2011: 97 |
| 73 | L190 | ibid.: 153 | Botelho Gosálvez, 1982 [1945]: 153 |
| 74 | L190 | ibid.: 154 | Botelho Gosálvez, 1982 [1945]: 154 |
| 75 | L192 | ibid.: 140 | Botelho Gosálvez, 1982 [1945]: 140 |
| 76 | L204 | ibid.: 57 | Botelho Gosálvez, 1982 [1945]: 57 |
| 77 | L204 | ibid.: 60 | Botelho Gosálvez, 1982 [1945]: 60 |
| 78 | L204 | ibid.: 80 | Botelho Gosálvez, 1982 [1945]: 80 |
| 79 | L206 | ibid.: 67 | Botelho Gosálvez, 1982 [1945]: 67 |
| 80 | L206 | ibid.: 68 | Botelho Gosálvez, 1982 [1945]: 68 |
| 81 | L206 | ibid.: 69 | Botelho Gosálvez, 1982 [1945]: 69 |
| 82 | L208 | ibid.: 64 | Botelho Gosálvez, 1982 [1945]: 64 |
| 83 | L208 | ibid.: 58 | Botelho Gosálvez, 1982 [1945]: 58 |
| 84 | L208 | ibid.: 159 | Botelho Gosálvez, 1982 [1945]: 159 |
| 85 | L208 | ibid.: 79 | Botelho Gosálvez, 1982 [1945]: 79 |
| 86 | L208 | ibid.: 35 | Botelho Gosálvez, 1982 [1945]: 35 |
| 87 | L218 | ibid. | Botelho Gosálvez, 1982 [1945]: 75 |
| 88 | L218 | ibid.: 79 | Botelho Gosálvez, 1982 [1945]: 79 |
| 89 | L218 | ibid.: 80 | Botelho Gosálvez, 1982 [1945]: 80 |
| 90 | L218 | ibid. | Botelho Gosálvez, 1982 [1945]: 80 |
| 91 | L218 | ibid.: 79 | Botelho Gosálvez, 1982 [1945]: 79 |
| 92 | L218 | ibid.: 160 | Botelho Gosálvez, 1982 [1945]: 160 |
| 93 | L218 | ibid.: 447 | Bertonio, 2011 [1612]: 447 |
| 94 | L230 | ibid. | Botelho Gosálvez, 1982 [1945]: 155 |
| 95 | L230 | ibid. | Botelho Gosálvez, 1982 [1945]: 156 |
| 96 | L230 | ibid.: 79 | Botelho Gosálvez, 1982 [1945]: 79 |
| 97 | L230 | ibid.: 466 | Bertonio, 2011 [1612]: 466 |
| 98 | L230 | ibid.: xiii | Alexander et al., 1977: xiii |
| 99 | L232 | ibid.: 156 | Botelho Gosálvez, 1982 [1945]: 156 |
| 100 | L232 | ibid.: 31 | Botelho Gosálvez, 1982 [1945]: 31 |
| 101 | L244 | ibid.: 156-157 | Botelho Gosálvez, 1982 [1945]: 156-157 |
| 102 | L246 | ibid.: 91 | Fuão, 2011: 91 |
| 103 | L248 | ibid.: 22 | Botelho Gosálvez, 1982 [1945]: 22 |
| 104 | L250 | ibid.: 159 | Botelho Gosálvez, 1982 [1945]: 159 |
| 105 | L250 | ibid.: 361 | Bertonio, 2011 [1612]: 361 |
| 106 | L260 | ibid.: 8 | Le Guin, 2021 [1986]: 8 |
| 107 | L274 | ibid.: 60, 156 | Botelho Gosálvez, 1982 [1945]: 60, 156 |
| 108 | L278 | ibid.: 154 | Botelho Gosálvez, 1982 [1945]: 154 |

## Comprobaciones de esta entrega

- Rama nueva desde la base indicada; solo se prepara `analisis/34_auditoria_de_la_version_final.md`.
- Artículo, fichero, lista de envío, Word, PDF e imágenes permanecen sin cambios.
- No se incorporan PDF, OCR, fotos, capturas de cotejo ni transcripciones extensas de fuentes a Git. Los auxiliares de búsqueda y verificación quedan fuera del checkout.
- Las redacciones propuestas se aplicarán únicamente si el autor aprueba correcciones concretas. Entonces corresponderá regenerar Word y entregables, actualizar cifras, ajustar el fichero si cambia una cita de la novela y revisar con el autor la declaración de IA. Esta auditoría no adelanta esa aprobación.
