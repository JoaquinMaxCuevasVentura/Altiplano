# 38. Auditoría del proyecto

14 de noviembre de 2026. El autor pidió revisar todas las decisiones tomadas hasta aquí y mejorar cada archivo final donde hiciera falta. Durante la revisión pidió además mirar los registros de arquitectura que reunió en otra conversación, porque creía que allí había mejores imágenes y datos útiles para el artículo.

Este registro dice qué se revisó, qué se encontró, qué se cambió y qué queda como propuesta. Las interpretaciones, el título, el epígrafe y la tesis no se tocaron.

## 1. Qué se revisó

- El artículo completo, leído de punta a punta, y sus datos parafraseados, contrastados con la edición digital de la novela.
- Los seis documentos de `entregables/`, el `README.md`, `AGENTS.md` y los `LEEME.md` de `entregables/`, `articulo/figuras/` y `taxonomia/`.
- Los dos generadores de Word.
- Las ramas del repositorio.
- La rama `claude/eager-bohr-mx9420`, con los registros de arquitectura: su `LEEME.md`, su catálogo de 95 láminas y su registro.

## 2. El artículo

### Lo que estaba bien

Las 286 citas que había conservan su fuente y su página, y entran tres con las imágenes nuevas. Las cadenas de *ibid.* resuelven a la obra correcta. La bibliografía y las citas se corresponden. Los datos parafraseados que se contrastaron están en su página: las cien hectáreas (p. 9), los más de ciento cincuenta muertos (p. 156), los dos metros de la *chujlla* (p. 30), los siete hombres de la jaula (p. 143), el agua que sube de los tobillos al ombligo (pp. 145 y 153), los cinco gendarmes (p. 101), los techos desfondados (p. 79) y el desmonte (p. 140).

### Lo que se corrigió

| Dónde | Qué decía | Problema | Qué dice ahora |
|---|---|---|---|
| Figura 1, plano (3) | «El narrador, por su parte, la declara cerrada («nadie podía entrar»)» | Por la frase anterior, «la» era la casa. En la novela lo cerrado es el alma: «en su alma, en su secreto, nadie podía entrar» (p. 65). Las conclusiones ya lo decían bien | «declara cerrada el alma de los comunarios, en la que «nadie podía entrar», y a ellos los ve como estatuas» |
| §5, «Se baja en jaula» | «(ibid.: 141-143)» | El *ibid.* venía justo después del pie de la Imagen de la mina, que nombra otra fuente | Referencia completa |
| §8, «manchones» | «(ibid.: 60, 156)» | Lo mismo, después del pie de la Figura 8 | Referencia completa |
| §1, los fragmentos | «(ibid.: 14)» | Seguía a «(Kolář, cit. en Fuão, 2011: 43)», y no quedaba claro a quién remitía | «(Fuão, 2011: 14)» |
| §4, el tinterillo | «(ibid.)» al comienzo de un párrafo | La página no se veía sin volver al párrafo anterior | «(ibid.: 103)» |
| §2, Warisata | «borra la escuela del *ayllu*. Cuando se publicó la novela» | «La novela» dos veces seguidas | «Para cuando se publicó» |
| Abstract | «the indigenista narrator» | Palabra extranjera en un texto en inglés | En cursiva |

### Lo que se revisó y se dejó

- **Los cierres interpretativos** que Codex proponía aplanar. Son del autor (`analisis/37`).
- **Las cursivas.** Van en cursiva ocho voces aymaras, y quedan en redonda los préstamos de uso general (puna, pirca, chácara, yunga, coca). El criterio no coincide del todo con el diccionario académico, que también recoge *apacheta* o *yatiri*, pero es coherente: marca las voces que el artículo estudia como cosas del mundo andino. Si el autor quiere también *pirca* en cursiva, es un cambio corto.
- **Los pasteles como hechos.** Es una decisión del autor del 10 de noviembre. El texto y las figuras no coinciden mientras no lleguen los escaneos, y todos los documentos lo avisan.
- **La Figura 5.** El plano (2) dice «la cadera del ganado vuelta luna menguante», y el plano (1) cita las «nalgas» de la p. 64. La cadera es la lectura del dibujante y está en el plano que le corresponde.

## 3. Las imágenes: lo que aportan los registros de arquitectura

La rama `claude/eager-bohr-mx9420` guarda 95 láminas con dibujos de arquitectura del altiplano, de 1847 a 2025. De ellas, 50 tienen el dominio público comprobado en la ficha de la institución; las demás tienen derechos, licencias con condiciones o derechos por confirmar, y no pueden pasar al artículo (regla 6 de `AGENTS.md`).

El artículo lee la novela desde la arquitectura, pero sus cinco imágenes mostraban un solo edificio, la Puerta del Sol. No había ninguna casa ni ninguna tumba, que son las dos cosas que la tesis junta. Por eso entraron dos láminas, las dos con el dominio público comprobado y con resolución para imprimir.

| Imagen nueva | Lámina de los registros | Dónde entra | Qué se comprobó |
|---|---|---|---|
| **Imagen 1.** *Tumba de un jefe aymara, de la provincia de Carangas (Bolivia)*, de Alcide d'Orbigny (1847: lám. 3 de antigüedades) | N.º 25 | §1, junto a la *amaya uta* de Bertonio, «sepultura como casa sobre la tierra» | El título y el número se leen en la lámina: «Antiquités N.º 3», «Tombeau d'un chef aymara, de la Province de Carangas (Bolivia)», «A. d'Orbigny del.», «E. Lassalle lith.». La ficha de Internet Archive (Smithsonian Libraries, Biodiversity Heritage Library) dice «Not in copyright» |
| **Imagen 3.** *Nuestro dormitorio en Uchusuma*, grabado en Squier (1877: 256) | N.º 5 | §3, después del párrafo sobre el narrador que entra en la *chujlla* como un intruso | Se bajó el texto del libro de Internet Archive y se leyeron las pp. 255-256. El ejemplar del Getty Research Institute está marcado `NOT_IN_COPYRIGHT` |

**Lo que dice Squier** (pp. 255-256), que es lo que cita el artículo:

- las chozas de Uchusuma eran «low stone huts, hardly bigger than the houses the beaver builds, and quite as rude»;
- las habían levantado dos familias indias que pastoreaban llamas y que murieron de viruela unos dos años antes;
- los viajeros durmieron en la que había sido la capilla, de siete pies por cinco, «so low as to prevent a man of ordinary height from standing erect»;
- al fondo había un altar de barro y una cruz de madera contra la pared de piedra tosca.

El artículo traduce la primera frase y parafrasea lo demás. No dice que el dormitorio fuera una vivienda: dice que era la capilla del caserío.

**Por qué estas dos y no otras:**

- La tumba de Carangas tiene muros de piedra y puerta baja, como una casa. Está en el altiplano boliviano, y deja a la vista lo que la sección 1 afirma con Bertonio.
- El interior de Uchusuma es el único interior de una casa corriente en las fuentes libres. Muestra lo mismo que la Figura 1, la pared de piedra y los palos del techo bajo la paja. Además, el viajero compara las chozas con casas de castor, como el narrador ve una madriguera.
- La casa de Inwards hecha con piedras de las ruinas (n.º 2) y la entrada de la iglesia de Tiwanaku de Wiener (n.º 94) también dialogan con el artículo, pero no se sumaron. La primera repetiría un argumento que ya tiene imagen, y la segunda no tiene el dominio público comprobado.
- Las cuatro Puertas del Sol de los registros (d'Orbigny, Angrand, Wiener, Stübel y Uhle) son mejores dibujos que el grabado de Squier, pero el artículo usa el de Squier por lo que cuenta su texto sobre el anciano que labraba una piedra al pie.

**La numeración.** Las imágenes van ahora del 1 al 7, por orden de aparición. Los archivos se renombraron (`articulo/figuras/LEEME.md` tiene la tabla con el nombre anterior de cada uno). La bibliografía suma la entrada de d'Orbigny y pasa a 37 obras.

**Lo que no se pudo hacer.** La otra conversación no se puede leer desde esta: solo se ve lo que dejó en su rama. Los 53 PDF de la carpeta del autor tampoco se localizaron con el conector de Drive.

### Fuentes de los registros que podrían mejorar el artículo

Son propuestas. No se añadió ninguna, porque para citarlas hay que leerlas con su página.

1. **Suárez Jordán (1990),** «Permanencia y cambio: el caso de la vivienda aymara en centros poblados del altiplano boliviano», *Ciudad y Territorio*, 85. Según el catálogo de los registros, su figura 3a es la planta tipo de la casa rural aymara, con tres cuartos sueltos alrededor de un patio. Es lo que el artículo lee en la novela («tres chujllas de adobe y paja brava que rodean al patio»), y hoy lo apoya solo en Alexander y en Monteys y Fuertes, que el propio artículo llama «miradas de fuera».
2. **Yampara Blanco (2019),** «La arquitectura de los pueblos milenarios del altiplano», *Revista Nodo*, 14 (27). Su figura 4 es la planta de una casa de Jalsuri con cada recinto nombrado en aymara (*taru uta*, *wallpa uta*, *pirwa*). Serviría para el primer límite de las conclusiones, que pide «otras fuentes y otros autores» para la manera aymara de entender el espacio.
3. **González Carrasco (2016),** tesis sobre la *uta* aymara en Arica, con las maneras de agrupar sus módulos. Tiene licencia abierta.

Con la carpeta de esos PDF, o su enlace, se pueden leer y proponer las frases con su página.

## 4. Los documentos finales

Varios documentos habían crecido por capas: cada etapa añadía una nota fechada sobre la anterior, y quedaban datos vencidos junto a los vigentes.

| Documento | Qué tenía | Qué se hizo |
|---|---|---|
| `entregables/02_lista_de_envio.md` | Decía «Estado al 2 de noviembre». Su lista de lo hecho mezclaba cotejos viejos y nuevos. Tres filas de «lo que falta» ya estaban resueltas. Dos «mejoras opcionales» (el concurso de 1940 y las fechas del autor) estaban en el artículo desde el 2 de noviembre | Lista de lo hecho rehecha, filas resueltas quitadas, pasos 4 y 6 aclarados, estado al 14 de noviembre |
| `entregables/07_fuentes_para_cotejar.md` | Seguía siendo una lista de pedidos: qué subir, dónde y cómo, con un repositorio privado que no se usó | Rehecho: lo que falta conseguir va arriba, en una tabla; después, dónde se guardan las fuentes y, como referencia, las páginas que cita el artículo de cada obra con lo que se comprobó |
| `entregables/04_fichero_de_pasajes.md` | Cinco párrafos fechados sobre qué estaba comprobado, uno de ellos con la cifra vieja de 157 citas | Dos párrafos: qué está comprobado y qué no |
| `entregables/03`, `05` y `06` | «Versión final, 11 de octubre» en el encabezado, aunque el 03 y el 05 cambiaron después | Fecha de origen y fecha de la última puesta al día |
| `README.md` | 158 líneas con el estado repartido en tres lugares. Decía que el Word de cambios marcaba 914, que *Atenea* pedía 1.800 palabras menos y que los pies de las figuras declaraban la asistencia de IA | Rehecha la primera mitad: estado en una tabla, qué sostiene el artículo, dónde está cada cosa y las ramas relacionadas. El índice de `analisis/` se conserva y suma el 32 y el 38 |
| `AGENTS.md` | Pedía devolver la plantilla después de cada uso del generador. No nombraba la rama de los registros | Al día con los generadores, la rama y el archivo del proyecto |
| `articulo/figuras/LEEME.md` | La serie de cinco imágenes | La serie de siete, con el nombre anterior de cada archivo |

## 5. Los generadores

- **`articulo/generar_docx.py` reescribía la plantilla de estilos en cada uso.** Había que devolverla con `git checkout` cada vez, y `AGENTS.md` lo pedía como un paso más. Ahora arma la plantilla en una carpeta temporal y solo reescribe la guardada con `--plantilla`.
- **Los dos generadores reescribían todos los Word aunque no cambiaran,** porque cada archivo lleva dentro la hora en que se guardó. Después de cada cambio había que comparar a mano cuáles eran distintos de verdad. Ahora comparan el contenido y dejan intacto lo que no cambió. El PDF solo se rehace si cambió el Word del artículo.

## 6. El repositorio

- **`analisis/32_churata.md`** estaba solo en la rama `codex/analisis-churata`. Se trajo como registro, igual que se había hecho con el 34. Ya no falta ningún número del 01 al 38, salvo el 05b, que es una segunda guía.
- **Choque de números.** La rama de los registros tiene su propio `analisis/34_registros_de_arquitectura.md`. Si se une, hay que renumerarlo. `AGENTS.md` lo avisa.
- **La regla de las ramas.** `AGENTS.md` pide a los asistentes trabajar en una rama propia y proponer los cambios con un *pull request*. Las sesiones de Claude han escrito directamente en la rama del artículo, porque así las configura el autor. No se cambió la regla, que sigue valiendo para los demás asistentes, pero conviene que el autor sepa que no se cumple en esas sesiones.
- **El archivo del proyecto.** Las versiones anteriores quedan ordenadas en `archivo_del_proyecto/`.

## 7. Cifras

El artículo tiene 76.939 caracteres con espacios y 13.039 palabras, en 40 páginas, con 37 obras en la bibliografía. Son 241 palabras más que antes de la auditoría, casi todas por las dos imágenes. Para *Atenea* habría que quitar unas 4.500.

## 8. Lo que queda para el autor

1. **Las dos imágenes nuevas.** Si alguna no te convence, sale quitando su frase, su bloque y su pie (`articulo/figuras/LEEME.md` dice cómo). La versión anterior es el commit 7b44456.
2. **Las tres fuentes sobre la casa aymara** del apartado 3. Hace falta la carpeta de los PDF.
3. **Los pasteles.** Mientras no estén, el artículo no se puede enviar.
4. **Lo demás** sigue en `entregables/02_lista_de_envio.md`.
