# 30. Taxonomía visual con imágenes de dominio público

18 de octubre de 2026. Registro de la etapa. Lo vigente está en `taxonomia/LEEME.md`.

## El pedido

El autor propuso buscar material en el Public Domain Image Archive (PDIA) y en otras fuentes para armar una taxonomía visual. Dio cuatro ejemplos:

- el «Tree Diagram» de Kengo Kuma, con materiales arriba, métodos abajo y obras unidas por líneas;
- un mapa de las vanguardias con fechas y palabras clave;
- una tira de fases («Phase 01 form finding … Phase 07 refinement») con imágenes sobre una línea de horizonte;
- un tablero narrativo, «Doing a Duchamp», con líneas rojas para el desarrollo y azules para las conclusiones.

## Qué se hizo

1. **El PDIA.**
   - El sitio sirve sus galerías en JSON. Se bajaron los metadatos de unas 70 etiquetas (piedras, minas, geología, textiles, escritura, huesos, máquinas, mapas y otras): 2.322 imágenes.
   - Se revisaron por obra y se eligieron 15.
   - De cada una se leyó su ficha: fuente, derechos de la obra y derechos digitales.
2. **Guaman Poma (Det Kgl. Bibliotek).**
   - Se bajaron 17 dibujos de la *Nueva corónica y buen gobierno*: el calendario agrícola, los khipus, los puentes y caminos, el escribano, la petición, las minas y los entierros.
   - Títulos, rótulos y paginación vienen de la transcripción de la propia biblioteca, página por página. Un primer borrador con títulos escritos de memoria se descartó.
   - La página del proyecto declara la marca de dominio público 1.0.
3. **Squier (1877).**
   - Se usó el escaneo del Getty Research Institute en Internet Archive, que sus metadatos marcan `NOT_IN_COPYRIGHT`.
   - La lista de ilustraciones del OCR dio las páginas, y el mapa de páginas del ejemplar dio la hoja escaneada.
   - Los grabados se recortaron de la página de forma automática: la mancha más grande de tinta sin líneas blancas. Luego se revisaron a ojo. La planta y el corte de la chullpa se recortaron a mano.
   - Se tomaron 15 grabados: Tiwanaku, Sillustani, Hatuncolla, Santiago de Machaca, el Desaguadero, el Titicaca, Cuzco y Yucay.
4. **Library of Congress.**
   - Cuatro fotos: dos de la mina Siglo XX (1940), el cerro de Potosí y el lavado de cobre en Corocoro (1908). Sus enlaces salieron de una búsqueda hecha antes, el mismo día.
   - Luego el sitio pidió una verificación de navegador (error 403). Las fotos se bajaron del servidor de imágenes, pero sus derechos quedan por confirmar.
5. **La taxonomía y los tableros.** Seis materiales, siete gestos y nueve fases, que son los capítulos de la novela con sus páginas de inicio según el índice de la 7.ª edición. Tres tableros hechos con `taxonomia/generar_tableros.py` (SVG y Chromium):
   - el árbol;
   - las fases;
   - el mapa de fechas.
6. **Las citas.**
   - Las del tablero de fases y las de las fichas son las del artículo, tomadas del fichero de pasajes.
   - Se comprobaron otra vez contra la transcripción paginada: 21 de 21.
   - Tres pasan solo con las correcciones de la sección 2 del fichero o por un salto de página:
     - p. 20, «empotró»;
     - p. 87, «para»;
     - p. 36, cita que sigue en la 37.

## Lo que falló o se descartó

- **Wikimedia Commons.** Respondió con el error 429, «demasiadas solicitudes», tanto en la API como en las miniaturas. No se pudo bajar nada. Se buscó en su lugar con Openverse, que indexa Commons, pero rinde poco para grabados antiguos. Solo encontró un dibujo de apacheta con licencia CC0, que quedó pendiente.
- **La lámina de Zubler (1607).** Venía del PDIA con derechos digitales CC BY-SA y se descartó para no atar los tableros a esa licencia.
- **Las fotos de mineros bolivianos de 1986-1994** de la Library of Congress. Son recientes y tendrían derechos de autor.
- **La nota del tablero 1.** Decía al principio que todas las imágenes llevaban una referencia explícita. No era cierto: solo 15 de 51 la tienen. Se corrigió antes de publicarlo.

## Datos que conviene saber

- **Las fechas de la novela.**
  - La nota «Al lector» (p. 4) dice que la novela se escribió «entre junio y agosto de 1940» para el concurso.
  - El tablero 3 marca 1940 y 1945, el año de la primera edición en Buenos Aires.
- **El impreso de Posada** dice «Número 1»; el PDIA lo titula «Number 2».
- **La foto del cerro de Potosí** está fechada en 1880 en su ficha, pero la firma la agencia Ewing Galloway. La fecha conviene confirmarla.
- **El artículo no cita ningún pasaje de *La Abundancia* (pp. 39-55).**

## Estado

Los tableros, el catálogo y las 51 imágenes están en `taxonomia/`. No se cambió el artículo.
