# Taxonomía visual de «Cosecha de piedras»

51 imágenes de dominio público, ordenadas por lo que muestran (un material) y por lo que se hace con ese material (un gesto), y montadas en cuatro tableros. 18 de octubre de 2026.

## Qué hay

| Archivo | Qué es |
|---|---|
| `tablero_1_arbol.jpg` y `.pdf` | **El árbol.** 42 imágenes. Seis materiales arriba y siete gestos abajo; cada imagen está en la columna de su gesto, y una línea del color de su material la ata a él. Sigue el «Tree Diagram» de Kengo Kuma |
| `tablero_2_fases.jpg` y `.pdf` | **Las fases.** Los nueve capítulos de la novela como fases, sobre una línea de horizonte: arriba, lo que se levanta y queda a la vista; abajo, lo que va a la tierra. 24 imágenes. Sigue la tira «Phase 01 … Phase 07» |
| `tablero_3_fechas.jpg` y `.pdf` | **El mapa de fechas.** Las 51 imágenes por año, en una franja por gesto; una línea une las imágenes de una misma obra. Sigue el mapa de las vanguardias |
| `tablero_4_relato.jpg` y `.pdf` | **El relato.** El argumento del artículo como un collage. Un hilo rojo recorre nueve pasos en el orden de la novela, del «erial de piedras» (p. 9) a la pirca compuesta (p. 156). Un hilo azul ata cada uno de los cuatro hallazgos de las conclusiones a los pasos que lo sostienen. Aparte, en un recuadro, va lo que la novela calla: la escritura andina. 16 imágenes. Sigue «The Narrative – Doing a Duchamp» |
| `catalogo.json` | La fuente de datos: la ficha de cada imagen, los materiales, los gestos, las fases y el relato. Se edita a mano |
| `catalogo.md` | La misma ficha en una tabla legible. La escribe el generador: no se edita |
| `imagenes/` | Las 51 imágenes, reducidas a 900 px de lado como máximo |
| `generar_tableros.py` | Rehace los tableros y `catalogo.md` |

## Cómo se clasifica

- **El material** es la materia que la imagen muestra trabajada:
  - piedra;
  - tierra;
  - fibra;
  - papel;
  - metal (el mineral, la mina y la máquina);
  - cuerpo.
- **El gesto** es lo que se hace con esa materia:
  - **amontonar:** despedrar y apilar;
  - **cercar:** amojonar, levantar pircas y muros;
  - **cosechar:** abrir la tierra, sembrar, recoger;
  - **tejer:** atar, trenzar, tender puentes;
  - **escribir:** anudar cuentas, labrar signos, firmar;
  - **medir:** trazar, levantar planos, clasificar;
  - **excavar:** minar y enterrar.
- **De dónde salen.** Las categorías nacen del artículo: la piedra, el papel y la máquina, el cuerpo de las secciones 6 y 7, y los gestos de la mano.
- **Una casilla por imagen.** Muchas imágenes caben en dos, pero elegir obliga a decir qué se ve primero. Si una clasificación no te convence, cámbiala en `catalogo.json` y regenera.
- **La regla de la analogía.** Las imágenes no ilustran la novela: son analogías. El artículo adopta una condición de Fuão para juntar figuras lejanas: «con la condición de que haya una referencia explícita» (Fuão, 2011: 53).
  - **Con referencia (15).** Llevan una cita de la novela o un vínculo con el artículo. Las citas son las del artículo, ya comprobadas, con su página en la 7.ª edición (`entregables/04_fichero_de_pasajes.md`).
  - **Sin referencia (36).** Todavía no la tienen: son candidatas.

## Lo que muestran los tableros

Son observaciones sobre esta selección, no sobre la historia de la imagen.

1. **Las dos fuentes andinas cubren casi todos los gestos.**
   - Guaman Poma (1615) aparece en seis gestos; Squier (1877), en los siete.
   - Las demás fuentes se quedan en uno o dos.
   - Para un tablero sobre el altiplano, el centro está en esas dos fuentes, no en los grabados europeos.
2. **La escritura andina.**
   - Guaman Poma dibuja un escribano andino del cabildo que redacta un testamento (n.º 27), una mujer que presenta su petición (n.º 28) y un contador con su khipu (n.º 25).
   - Son imágenes de lo que, según las conclusiones del artículo, la novela calla: lo que los aymaras hicieron con la escritura.
3. **La cosecha aparece dos veces en la novela.**
   - Está al principio, en el ayllu: el trabajo más duro de Jatun-Kolla «rinde cosecha de piedras» (p. 9).
   - Y en la mina: «Aquí cosecharás miles de cargas de estaño» (p. 142).
   - El tablero 1 pone el lavado de mineral de Corocoro (n.º 18) en la columna «Cosechar». Así se ve el paso que el artículo describe en sus conclusiones: la máquina captura el gesto de la cosecha.
4. **El capítulo que el artículo no cita.**
   - *La Abundancia* (pp. 39-55) es el único capítulo sin ninguna cita en el artículo.
   - En el tablero 2 solo lo llenan las cosechas de Guaman Poma.
   - El título del artículo habla de cosecha: conviene releer ese capítulo.
5. **El mapa de fechas tiene un hueco entre 1680 y 1800.** Es un efecto de la selección, no un dato.
6. **El montón cambia de materia.**
   - El tablero 4 sigue la palabra a lo largo de la novela: primero es de piedras («erial de piedras», p. 9), luego de papeles («un desordenado montón de papeles y libracos», p. 103) y al final un derrumbe en la mina («un informe montón de rocas, lodo y maderos astillados», p. 154).
   - El hilo rojo discontinuo une el primero con el último, como hace el artículo al cerrar: la profecía de la montaña de piedras se cumple al revés.

## Fuentes y derechos

| Fuente | Imágenes | Derechos |
|---|---|---|
| Det Kgl. Bibliotek (Copenhague): Guaman Poma, *Nueva corónica y buen gobierno*, 1615 (GKS 2232 4º) | 17 | Marca de dominio público 1.0, según la página del proyecto. Títulos y páginas tomados de la transcripción de la propia biblioteca |
| Internet Archive, escaneo del Getty Research Institute: E. G. Squier, *Peru: Incidents of Travel and Exploration in the Land of the Incas*, 1877 | 15 | `NOT_IN_COPYRIGHT` en los metadatos del ejemplar. Grabados recortados de la página; el catálogo da la página impresa |
| Public Domain Image Archive (PDIA) | 15 | «Public Domain Worldwide» y «No Additional Rights» en la ficha de cada imagen, que también da la institución de origen |
| Library of Congress | 4 | Confirmados el 18 de octubre en la ficha de cada foto. Las dos de la mina Siglo XX (n.os 39 y 51) son de la colección FSA/OWI, de dominio público. Las de Potosí (n.º 40) y Corocoro (n.º 18) no tienen «restricciones conocidas para publicar». Las fichas dan rangos de fechas: 1940-1946, 1880-1923 y 1908-1919 |

- **Lo que se descartó.** Una lámina de Zubler (1607) del PDIA tiene derechos digitales CC BY-SA. Habría obligado a compartir los tableros con esa licencia, así que se dejó fuera.
- **Wikimedia Commons** no respondió desde el entorno de trabajo: dio el error 429, «demasiadas solicitudes». Por eso faltan las apachetas, Cieza de León y d'Orbigny (véase abajo).

## Lo que falta o decides tú

1. **Las fechas de las fotos de la Library of Congress** son rangos. El mapa de fechas las pone en el primer año del rango.
2. **El impreso de Posada** (n.º 5). El PDIA lo titula «Number 2», pero en la hoja se lee «Número 1».
3. **Las categorías** son una propuesta. Puedes añadir un material, como madera o agua; mover una imagen de casilla o quitarla.
4. **Las 36 imágenes sin referencia.** Cada una necesita su cita de la novela o salir del tablero.
5. **Fuentes que faltan,** cuando Wikimedia Commons responda:
   - la apacheta (hay un dibujo con licencia CC0, «Apacheta, monticule votif»);
   - el Potosí de Cieza de León;
   - las láminas de d'Orbigny y de Wiener.
6. **Las imágenes que pasaron al artículo.** El 18 de octubre entraron seis, como imágenes 1-5 en serie aparte (`analisis/31_proyecto_de_imagenes_de_dominio_publico.md`):
   - el escribano (n.º 27);
   - la Puerta del Sol (n.º 29);
   - la tejedora y el contador, en un díptico (n.os 20 y 25);
   - la mina Siglo XX (n.º 39);
   - agosto (n.º 13).

   La numeración de las figuras no cambió. La declaración de uso de IA nombra ya la búsqueda y la preparación de las imágenes, que son históricas y no se hicieron con IA. Los tableros no entran al artículo.

## Cómo regenerar

```bash
python3 taxonomia/generar_tableros.py      # los cuatro tableros y catalogo.md
python3 taxonomia/generar_tableros.py 2    # solo el tablero 2
```

Necesita Pillow y Chromium (variable `CHROME`).

Para añadir una imagen:

1. Ponla en `imagenes/`, a 900 px de lado como máximo.
2. Añade su ficha a `catalogo.json`. La ficha lleva fuente, página, derechos, material, gesto y, si la tiene, la fase y la referencia.
3. En el tablero 1 entran las fichas con número hasta el 42; las demás solo salen en los tableros 2 y 3.
