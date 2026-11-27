# 41. Auditoría de «La tierra que queda», el proyecto paralelo de GPT

27 de noviembre de 2026. El autor pidió auditar un proyecto que GPT hizo en paralelo a partir del artículo y que, a su juicio, es deficiente pero tiene mucho potencial. GPT lo subió a la rama `proyecto/la-tierra-que-queda` (commit d2591eb, firmado por Codex) y abrió el *pull request* en borrador n.º 1 hacia la rama del artículo. La auditoría no cambia esa rama ni el *pull request*.

## 1. Qué se revisó y cómo

- **Todo lo que hay en la rama:** el `README.md`, las cuatro imágenes, los 22 archivos de `guiones_recuperados/` (21 guiones y una nota) y las dos comprobaciones (`traza.json` y `mediciones_de_cumbrera.txt`).
- **Los datos internos de las imágenes:** tamaño, formato, metadatos y huella de cada una.
- **Los guiones que se pueden ejecutar:** se corrieron en un espacio de trabajo aparte, con las rutas cambiadas.
- **El modelo frente a la novela:** se cotejó con la edición digital de la UMSA y con las fuentes de la sección 3 del artículo (Suárez Jordán, 1990; Yampara Blanco, 2019).
- **Las reglas del proyecto:** se contrastó con las de `AGENTS.md`.
- **Las referencias externas:** se buscaron las dos obras de Smiljan Radić que cita el proyecto.

## 2. Qué es

Es una serie de tres estudios de arquitectura que GPT llamó *La tierra que queda. Del lindero al fogón*. Cada uno toma un pasaje de la novela y propone una construcción en Jatun-Kolla:

| Estudio | Pasaje | Qué propone |
|---|---|---|
| 01. Lindero: *El recinto que queda abierto* | El retorno y las pircas recompuestas (p. 156) | Un recinto de pirca con una entrada entre dos remates y una cubierta plegada de acero patinado sobre tres apoyos. Precedente: *Corral*, de Radić |
| 02. Umbral: *El claro de la piedra* | Los comunarios se arrodillan «en el dintel de Jatun-Kolla» (p. 155) | Un paso entre dos pircas, cubierto por una membrana sobre costillas, que se abre al final. En la última revisión deja a la vista el relleno de piedra menuda de la pirca |
| 03. Interior: *La mirada en cuclillas* | La *chujlla* de los Huanca (pp. 8 y 30-31) y la Figura 1 | Una *chujlla* cortada, sin muro sur, con una ranura de vidrio en la cubierta, un conducto de extracción y una figura en cuclillas junto al fogón. Precedente: la *Casa para el Poema del Ángulo Recto*, de Radić |

En la conversación con GPT el proyecto llegó a tener un archivo de Blender con seis escenas, siete renders, dos comparaciones, un dossier de cinco páginas compuesto en Typst, una lámina A3 y un ZIP. **Nada de eso se conserva.** La rama guarda lo que GPT pudo recuperar después.

## 3. Lo que vale

1. **Pasa de la lectura al proyecto.** El artículo lee la novela con el dibujo y termina en sus límites. Este trabajo pregunta qué construiría un arquitecto a partir de esa lectura. Para un autor que es arquitecto, es una continuación natural y un producto distinto del artículo.
2. **Las páginas de la novela están bien.** Las cinco que cita (8, 30-31, 155, 156 y 156-157) dicen lo que el proyecto les atribuye.
3. **La mejor idea es la del estudio 02 en su última revisión.** El paso deja a la vista la piedra menuda que rellena la pirca de doble cara, y el guion lo justifica con el artículo (§7, la «legión» de piedrecilla menuda, p. 8) y con la analogía de `analisis/11` (§11.5 B). Convierte en construcción el argumento del artículo, según el cual el retorno se olvida del relleno, que son los sin tierra. Vale para ella la misma cautela que anota ese registro: la novela no dice cómo están hechas las pircas de Jatun-Kolla.
4. **La pirca está bien modelada.** Se arma con doce formas de piedra repetidas por instancias en Blender, con dos caras y un corazón de relleno, y cada parte se puede editar.
5. **Los guiones dejan constancia de cada decisión.** Las escenas guardan su fuente, su decisión y su hipótesis material, y casi todos los guiones terminan comprobando la geometría con aserciones.
6. **Los tres dibujos de detalle constructivo** (`anteproyecto/nudos.py`) son claros y se pueden rehacer: el encuentro de la pirca con la cubierta, el apoyo de la membrana y la ranura de la cubierta.
7. **GPT siguió la regla de ramas de `AGENTS.md`:** trabajó en una rama propia y propuso los cambios con un *pull request* en borrador.

## 4. Lo que falla

| N.º | Problema | Gravedad |
|---|---|---|
| F1 | **El proyecto no se puede reabrir.** Se perdieron el `.blend`, los renders, el dossier y el ZIP. De los 21 guiones, 11 necesitan escenas de ese `.blend`, y otros 8 editan, componen o empaquetan archivos que se perdieron o que también dependen de él. Solo dos corren con lo que hay en la rama: la lámina A3 y los dibujos de detalle | Alta |
| F2 | **La ruta que GPT le dio al autor no le servía.** `/workspace/La_tierra_que_queda/...` está en el espacio de trabajo de la conversación de GPT. El autor no tiene acceso a esa carpeta, y ese espacio se borra cuando la sesión termina | Alta |
| F3 | **Todo indica que dos de las tres imágenes de la serie están tratadas con GPT Image.** La nota del propio proyecto dice que las versiones de presentación se hicieron así: «img2img contiene las versiones de presentación, tratadas con GPT Image» (`anteproyecto/LEEME_fuentes.txt`). *El recinto* y *La mirada* no conservan ningún metadato de Blender, mientras que *El claro*, que es un render directo, guarda el archivo, la escena, la cámara y el tiempo de render. GPT o el autor pueden confirmarlo. La regla 6 de `AGENTS.md` dice que las imágenes hechas con generadores de IA son solo exploración y no se publican | Alta |
| F4 | **Las imágenes parecen fotos de maquetas.** Muestran una base de contrachapado, figuras de papel y un fondo de estudio, sin serlo. Ni el `README.md` ni la lámina dicen que son modelos digitales retocados con IA, y la lámina tampoco trae declaración de uso de IA (regla 7) | Alta |
| F5 | **La *chujlla* del estudio 03 contradice la novela, aunque la lámina dice que «retoma» su lectura.** La novela dice que las *chujllas* son «rectangulares y chatas, apenas se alzan dos metros del suelo» (p. 30). En el modelo, los aleros están a 3,09 y 4,09 m y la cumbrera a 4,21 m (`traza.json` y `mediciones_de_cumbrera.txt`), más del doble. La novela les pone techo de paja (pp. 10, 41, 57 y 72); el modelo, una «costra de tierra». La novela pone los braseros «en el centro del cuarto» (p. 30); la imagen pone las piedras del fogón contra el muro del fondo | Alta |
| F6 | **El modelo se ajustó a una imagen y no al texto.** `traza.json` guarda cinco puntos de una imagen de referencia, en píxeles, y los vértices del testero coinciden con ellos a menos de una milésima de píxel. La «fidelidad» que buscó GPT fue fidelidad a esa imagen. De ahí sale la altura | Media |
| F7 | **El estudio 03 mejora la *chujlla* desde fuera.** El vidrio laminado y el conducto de extracción resuelven la luz y el humo con recursos ajenos, cuando la fuente que el artículo ya cita describe la solución aymara: el *t'uju*, un «orificio pequeño» al noreste por donde entra el sol y que sirve de ventilación y de «salida del humo como una chimenea» (Yampara Blanco, 2019: 13). Es la «mirada de fuera» que el artículo critica en su sección 3 y el riesgo de «embellecer la miseria» que nombra en sus conclusiones | Media |
| F8 | **Las tres partes no responden al mismo argumento.** El estudio 01 dice partir de «las ausencias en la lista del retorno», pero la cubierta de acero no se relaciona con esas ausencias. El 02, en su última revisión, sí lo hace | Media |
| F9 | **La serie mezcla versiones.** La imagen de *El claro de la piedra* es del 18 de noviembre y muestra la piedra suelta. La revisión posterior (`dintel-claro/revisar.py`) quita esa piedra, cambia el nombre a *El claro de la pirca* y deja el relleno a la vista, pero esa versión no está en la serie. El texto de la lámina describe la anterior | Media |
| F10 | **El detalle de la cubierta no es un render nuevo.** Es un recorte de unos 470 × 280 píxeles de *El recinto*, ampliado unas 2,6 veces (correlación de 0,88 con la imagen grande). No agrega información y tiene menos definición | Baja |
| F11 | **Los precedentes son todos de Radić**, un arquitecto chileno de autor. Faltan los andinos que el autor ya reunió: Suárez Jordán, Yampara Blanco, Šolc (la construcción de una casa en Enquelga, paso a paso) y los estudios sobre el putuco | Baja |
| F12 | **La documentación es mínima.** El `README.md` no dice cuál es la premisa (un proyecto especulativo sobre un lugar de ficción), en qué estado está, qué hizo la IA ni cómo se reproduce. Las mediciones de la cumbrera no explican qué se midió. Los guiones usan rutas absolutas de la sesión. La carpeta `proyectos/` no figura en el `README.md` ni en `AGENTS.md` del repositorio | Baja |

**Sin problemas en:**

- **Datos personales:** no hay correos ni enlaces privados.
- **Derechos:** ningún PDF ajeno entró en el repositorio; el de *Obra gruesa* quedó en la conversación.
- **Formato:** no hay espacios sobrantes.
- **Commits:** el mensaje está en español y dice qué cambia.

## 5. Comprobaciones

| Qué | Resultado |
|---|---|
| Las páginas de la novela que cita el proyecto (8, 30-31, 155, 156, 156-157) | Correctas, en la edición digital de la UMSA |
| *Corral*, de Smiljan Radić, en *Obra gruesa*, p. 204 | El índice del libro la pone en la p. 204. El libro existe en edición chilena y en edición bilingüe de Hatje Cantz (2020) |
| *Casa para el Poema del Ángulo Recto*, de Radić | Existe: Vilches, Chile, 2010-2012 |
| Alan Chandler, «Trabajo de riesgo», pp. 214-217 | Chandler figura entre los autores de *Obra gruesa*. El título y las páginas del texto no se pudieron comprobar |
| Metadatos de las imágenes | Solo *El claro* trae los de Blender (render Cycles de 49,8 s, 45 muestras) |
| `altiplano-serie-selection/lamina.py` | Corre con las imágenes de la rama. Se rehízo la lámina A3 con otra tipografía, porque la original no está instalada |
| `anteproyecto/nudos.py` | Corre. Se rehicieron los tres dibujos de detalle en SVG |
| Los otros 19 guiones | No corren: dependen del `.blend` o de archivos que se perdieron |

La lámina y los dibujos rehechos quedaron fuera del repositorio. Se le entregaron al autor.

## 6. Cómo llevarlo adelante

En orden:

1. **Rescatar el ZIP ahora.** El enlace «Descargar el proyecto completo para Windows» de la conversación con GPT puede seguir funcionando mientras la sesión no se cierre. Si baja, el ZIP va a la carpeta privada de Drive: el `.blend` puede pesar más de los 100 MB que admite GitHub por archivo.
2. **Darle al proyecto un lugar propio.** No conviene meterlo en el artículo: el artículo ya está cerrado, y para *Atenea* habría que quitarle unas 5.000 palabras. Puede ser una pieza aparte, como una exposición junto a los pasteles, una entrega de proyecto o un segundo texto sobre proyectar desde una novela. El `README.md` tiene que decir que es un proyecto especulativo sobre un lugar de ficción.
3. **Separar los renders de las imágenes de IA.** Para mostrar el proyecto sirven los renders directos de Blender y, mejor todavía, fotos de las cinco maquetas del autor que los guiones nombran como base («Ensayo basado en las cinco maquetas de Joaquin Cuevas»). Las versiones de GPT Image quedan como exploración y, si se muestran, van rotuladas.
4. **Volver a la novela en el estudio 03.** Una *chujlla* de unos dos metros, techada con paja brava, con los braseros en el centro y la puerta al este. Hay dos fuentes andinas, ya cotejadas, para resolverlo:
   - Yampara Blanco cuenta que se traía «paja brava para el techado» (2019: 16) y describe el *t'uju* (ibid.: 13);
   - Suárez Jordán anota que la puerta de la casa grande está «siempre orientada hacia el Este» (1990: 130).

   Si el proyecto quiere intervenir la casa, el *t'uju* es un punto de partida más coherente con el artículo que la ranura de vidrio.
5. **Poner en el centro la idea del relleno.** El estudio 02 en su última revisión (el relleno a la vista) es el que mejor conversa con el artículo. El 01 necesita una razón para la cubierta de acero o se puede dejar de lado.
6. **Sumar precedentes andinos.** A Radić se le pueden sumar Šolc, Suárez Jordán y Yampara Blanco, que están en la carpeta de los registros de arquitectura.
7. **Usar el modelo 3D como ayuda para los pasteles.** Puede dar las perspectivas y los cortes de las figuras 1, 2 y 4 como hicieron los esquemas de encaje, sin ser la imagen que se publica.
8. **Dejar el *pull request* en borrador** hasta resolver los puntos 1, 3 y 4, y completar el `README.md` (premisa, estado, uso de IA, derechos y cómo reproducirlo).

## 7. Lo que decide el autor

- Si el proyecto sigue y en qué forma.
- Si las cuatro imágenes quedan en la rama, que es pública, rotuladas como exploración, o salen de ella.
- Qué hacer con el *pull request*.

Nada de esto toca el artículo, que sigue como quedó el 15 de noviembre (`analisis/40`).
