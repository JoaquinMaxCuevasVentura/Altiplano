# 33. La versión final: lo recuperado, Churata y una redacción sin patrones de IA

2 de noviembre de 2026. Registro de la etapa. El texto vigente está en `articulo/articulo_cosecha_de_piedras.md`.

## El pedido

El autor pidió una versión final con tres condiciones:

- **Sin límite de extensión.** El artículo ya no responde a ninguna convocatoria, y la cantidad de palabras no importa por ahora.
- **Recuperar lo importante.** Hay que revisar la conversación, los documentos y las versiones anteriores. Para llegar a los límites de palabras se quitaron cosas que importaban.
- **Que se lea como escrito por una persona.** Antes de redactar, hay que estudiar los patrones de escritura de la IA para no cometerlos. El autor va a reescribir esta primera versión final.

## Los patrones de la IA: qué dicen las fuentes

- **La guía de Wikipedia** («Signs of AI writing», del proyecto WikiProject AI Cleanup) reúne lo que sus editores han visto en miles de artículos. Para un artículo académico en español importan estos patrones:
  - el énfasis inflado en la importancia de algo;
  - los análisis superficiales que cuelgan de un gerundio;
  - un vocabulario repetido (*crucial*, *clave*, *subrayar*, *tapiz*);
  - evitar el verbo *ser* con perífrasis como «se erige como» o «funciona como»;
  - los paralelismos negativos, del tipo «no es X, sino Y»;
  - la regla de tres;
  - las conclusiones de esquema y las listas con encabezados en negrita.

  La guía advierte que un solo rasgo no prueba nada, que los detectores fallan y que la gramática perfecta no es un indicio.
- **Alonso Simón, Fernández-Pampillón Cesteros, Fernández Trinidad y Márquez Cruz (2025)**, «¿Tienen GPT-3.5 y GPT-4 un estilo de escritura diferente del estilo humano? Un estudio exploratorio para el español», *Revista Electrónica de Lingüística Aplicada*, 23(1), https://doi.org/10.58859/rael.v23i1.666. Compararon 41 rasgos, y 17 separan a los modelos de los humanos (sección 7):
  - los modelos usan más adjetivos, y menos adverbios y pronombres;
  - los humanos usan más puntuación de casi todo tipo: comas, paréntesis, dos puntos, comillas, guiones y punto y coma;
  - los modelos usan más puntos, porque escriben más oraciones por texto;
  - los textos humanos tienen más riqueza léxica.
- **Laines y Nazar (2024)**, en la *Revista de Lingüística Teórica y Aplicada* (Concepción), compararon tesis humanas y sintéticas. Según su resumen, los textos humanos muestran más riqueza léxica y más variedad de recursos discursivos. El texto completo no se pudo abrir desde el entorno de trabajo.

## El diagnóstico

Un guion (`patrones`, fuera del repositorio) midió la prosa propia del artículo, sin citas ni referencias, antes y después:

| Rasgo | Antes (commit 6f9bed8) | Ahora |
|---|---|---|
| Dos puntos por cada mil palabras | 37,5 | 16,7 |
| «No… sino» y semejantes | 11 | 1 |
| Largo medio de la oración | 17,3 palabras | 19,4 palabras |
| Oraciones de 35 palabras o más | 7 % | 11 % |
| «También» | 15 | 12 |

Lo que más delataba al texto anterior era el remate:

- el uso de dos puntos para revelar algo («El ayllu tiene dintel: es una casa»);
- las antítesis («No es una mano frente a un papel, sino dos manos con dos agarres»);
- la frase corta y redonda al final de cada párrafo («El mito y el mapa no se oponen: los dos escalonan»).

En la versión nueva:

- las oraciones tienen largos distintos y más subordinadas;
- hay menos dos puntos y menos antítesis;
- el plural de autor aparece donde un ensayista lo usaría («nos interesa», «creemos»);
- los remates se funden con la frase anterior o desaparecen.

**No cambian:** el título, el epígrafe, la tesis, los cuatro hallazgos, los tres planos de cada figura, las figuras, las imágenes y las citas.

## Lo que vuelve

Todo esto se había quitado por extensión, o se había dejado «en reserva» por falta de espacio. Cada cita se comprobó en su fuente en la etapa que se indica. Las fuentes ya no estaban en el entorno el 2 de noviembre, así que no se volvieron a comprobar ese día.

| Qué | Dónde va | Fuente | Registro |
|---|---|---|---|
| *Amaya uta*, «sepultura como casa sobre la tierra» | §1 | Bertonio, p. 276 | `08` |
| La novela se escribió «entre junio y agosto de 1940» para un concurso; ganó Ciro Alegría, «cuyo argumento tiene un sorprendente parecido al de “Altiplano”» | §1 | Botelho Gosálvez, p. 4 | `02` (mejoras opcionales), `06`, `30` |
| Las fechas del autor, 1917-2004 | §1 | Ficha de autoridad de la Biblioteca Nacional de Francia | `entregables/02`, mejoras opcionales |
| «Dibujar es dejar huellas estables en un soporte a partir de movimientos corporales» | §2 | Seguí, p. 13 | `08` |
| Warisata, «La única comunidad libre que subsistía en la región», y su «antigua pelea de linderos» | §2 | Rivera Cusicanqui, p. 150 | `08` |
| «Posteriormente destruirían también a Warisata» | §2 | Rivera Cusicanqui, p. 105 | `08` |
| Paulo despide a sus hijos «desde el portal de su chujlla» | §3 | Botelho Gosálvez, p. 34 | `16` (recorte 9), `06` |
| El título como «mojón que cabe en un bolsillo» | §3, Kero-Pata | Analogía propia | `11`, en reserva |
| La sección como «búsqueda de un interior»; «Desde dentro» y «Desde fuera» | Figura 1 | Seguí, pp. 97 y 23 | `08` |
| La circular de 1886 contra «los encargados de consignar por escrito sus reclamaciones» | §4 | Barnadas, pp. 46-47 | `08`. El OCR estaba dañado: hay que cotejarla |
| El narrador mira la cordillera con la arquitectura de Europa | §5 | Frase propia, sin comillas | `16` (recorte 6) |
| La escritura sitúa a quienes no la dominan «como puros soportes físicos» | §5, la huella | Cornejo Polar, p. 68 | `08` |
| La bendición: «que en las apachetas no les detenga el Supaya» | Figura 3 | Botelho Gosálvez, p. 33 | `13` |
| *Thaxsi*, «el cimiento» y «el horizonte o término de la tierra» | Figura 3 | Bertonio, p. 486 | `08` |
| Volver monumento la apacheta interrumpe la «correspondencia» | Figura 3 | Ingold, p. 86 (traducción propia) | `08`. Estaba en la Figura 3 hasta la versión llana |
| La cita completa de la p. 155, «en el terror de la mala época» | §7 | Botelho Gosálvez, p. 155 | `16` (recorte 7) |
| *Uta*, «cubierta, techo de la casa»; los techos desfondados | §7 | Bertonio, p. 132; Botelho Gosálvez, p. 79 | `13`, `07` |
| «Piedra para entremeter en los edificios y llenar sus huecos» | §7, la pirca | Bertonio, p. 246 | `08` |
| *Qalaptaña*, «volverse piedra o endurecerse» | §7 | Bertonio, p. 444 | `16` |
| El mundo indio como «estado sólido, siempre repetido» | §7, el final | Cornejo Polar, p. 181 | `08` |

### Lo que no vuelve, y por qué

- **Vidler, Deleuze, Foucault, Colomina, Schmarsow y otros.** No salieron por extensión, sino porque el arbitraje simulado los objetó y el argumento no los necesita (`08`, §8.6).
- **Lo que no tiene una cita o una página fijadas.** No vuelve:
  - Barnadas y Coy (p. 11), reconstruido de un OCR en tablas;
  - Zavaleta (pp. 32, 146 y 186), que solo está en OCR;
  - el umbral de Alexander (pp. 622 o 623);
  - la *saywa* y la *apachita* de Cobo en Dean;
  - Frampton (pp. 7-8);
  - la escena de Churata de las chukllas incendiadas, que no tiene página.
- **Lo que recargaría un pasaje que ya tiene apoyo.** Tampoco vuelve:
  - Garrington (p. 2), en la huella;
  - Duviols (p. 21), en la Figura 5;
  - Venturi, Sedlmayr y la perspectiva de Fuão;
  - Ingold (pp. 76 y 80);
  - las piedras *awicha* de Spedding.
- **Lo que pide una entrada nueva sin datos completos:**
  - las *illas* y el *qulla q'ipi* de Sixto Icuña;
  - el refrán de Hans van den Berg.

## Churata

El 2 de noviembre, el autor envió dos libros que Codex había revisado antes (su informe está en la rama `codex/analisis-churata`, `analisis/32_churata.md`, todavía sin unir):

- *Textos esenciales* (Tacna, Perro Calato, 2017);
- *El pez de oro*, en la versión digital de Rolando Diez de Medina.

Se leyeron las piezas sobre Warisata, la vivienda y la escritura. Las páginas de *Textos esenciales* coinciden con el índice del libro y con la estructura de páginas del Word. Las de *El pez de oro* son las del PDF que usó Codex: el Word no conserva la paginación.

| Qué | Dónde va | Fuente |
|---|---|---|
| La escuela en el ayllu y no en la aldea: «mientras Caquiaviri se enquista en la aldea, Warisata lo ha hecho en el ayllu» | §2 | *La Calle*, 27 de octubre de 1936; *Textos esenciales*, pp. 109-110 |
| El «crimen cometido con la escuela de Warisata» | §2 | *La Calle*, 18 de febrero de 1943; *Textos esenciales*, p. 129 |
| Un indio convierte «una de las paredes de su chuklla en abecedario mural» y lo llevan preso | §3 | *El pez de oro*, p. 20 de la versión digital |
| La casa de Konkachi (1939): «dos habitaciones que hacen ángulo», una pirca y la cocina fuera | §3 | *Kollasuyu*, agosto de 1939; *Textos esenciales*, p. 123 |
| Los «juguetes cubistas»: Churata también exotiza | §8, primer límite | *Textos esenciales*, p. 123 |

De las cinco propuestas de Codex no entra ninguna:

- La 1 (la piedra «buena siempre») es buena, pero el párrafo de Dean ya hace ese trabajo.
- La 2 (el bilingüismo, 1958) es posterior a la novela, y la columna de 1936 dice más.
- Las 3, 4 y 5 no aportan lo suficiente.

## Verificación

- **Cada cita con su fuente y su página.** Un guion asignó cada cita a la referencia que la sigue, resolviendo los *ibid.*, en la versión anterior (296 citas) y en la nueva (326):
  - ninguna cita cambió de fuente ni de página;
  - la de la p. 155 volvió a su forma completa;
  - entraron 31, todas en las tablas de arriba.
- **Las cadenas de *ibid.*** Todas remiten a la obra correcta.
- **Citas de la novela:** 157 entre comillas y 2 en bloque (antes, 153 y 2). `entregables/04_fichero_de_pasajes.md` tiene las cuatro filas nuevas.
- **Bibliografía:** 36 entradas, con las dos obras de Churata. No hay citas sin entrada.
- **Extensión:** 74.594 caracteres y 12.609 palabras con notas y bibliografía. El PDF tiene 38 páginas, y el resumen pasa a 122 palabras y el *abstract* a 118.
- **El Word con cambios marcados** compara con el commit 6f9bed8, el anterior a esta versión. Marca 914 cambios, porque la redacción es nueva de punta a punta.
- **La declaración de IA** nombra ahora también a Codex (OpenAI), que hizo el primer análisis de Churata.

## Lo que decide el autor

1. **Reescribir el texto con su voz.** Esta versión sirve de base. Cuando la reescriba, debe ajustar la declaración de IA a lo que haya quedado.
2. **Las interpretaciones nuevas.** Conviene mirar sobre todo estas:
   - «La novela pone la negativa en la aldea y borra la escuela del ayllu» (§2);
   - el abecedario de la chuklla frente a las paredes sin letras de los Huanca (§3);
   - el título como mojón de bolsillo (§3);
   - el horizonte como cimiento (*thaxsi*, Figura 3);
   - el final que «restaura el ciclo» (§7);
   - Churata en el primer límite (§8).
3. **Los cotejos pendientes:**
   - *El pez de oro*, p. 20, y una edición de referencia;
   - las páginas de *Textos esenciales* en el PDF;
   - Barnadas, pp. 46-47;
   - las citas recuperadas, contra sus fuentes, cuando estén a mano.
4. **El resumen.** Creció a 122 palabras. Algunas revistas piden 150 como máximo.
