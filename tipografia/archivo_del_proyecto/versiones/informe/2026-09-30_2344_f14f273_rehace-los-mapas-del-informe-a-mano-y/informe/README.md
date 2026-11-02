# El informe de decisiones

`contenida_informe_de_decisiones.docx` (y su PDF) reúne las decisiones del proyecto, al modo de las dos tesis de referencia: la obra, el marco, el sistema, la gramática, los estados, el taller, la propuesta de la máquina, la retórica y la poética, lo digital y la ética. Lleva seis mapas esquemáticos que conectan conceptos, teoría, retórica y poética en cada etapa del proyecto.

## Los mapas

| Mapa | Qué conecta | Cómo se dibuja |
|---|---|---|
| 1 · El proyecto entero | Las cinco etapas, de la obra a lo digital, con su concepto, su figura, su verso y sus fuentes | Un eje que baja por las cuatro líneas de la letra (afuera, borde, fondo, desagüe); cada etapa es un objeto en su órbita; la vuelta punteada vuelve a la caja |
| 2 · Teoría y fuentes | Las dos tesis, Posnansky, Agüero, Uribe y Berenguer y la obra: lo que se toma y lo que no | Cada fuente es un objeto en órbita (una vasija rajada, un taburete, una losa con su canal, la ¿ y la ?, una placa en su charco); lo que se toma llega en haces a la o; lo que no, se corta |
| 3 · La obra, decisión por decisión | Las dieciséis decisiones de la obra y su traducción en la letra | La cadena de desplazamientos es un río de aguada que pierde materia (grafito, plata, violeta, lila); de cada eslabón sale una hebra hacia su decisión |
| 4 · Del pie a los 55 signos | Las medidas del pie, la forma de la obra, los parámetros, las partes, los generadores y la caja | El pie a máquina con sus medidas a mano; las cuatro vasijas en órbita, con sus parámetros escritos sobre las órbitas; los signos bajan en bandadas a la caja |
| 5 · La cadena de estados | Pie, calco, placa, cinta, frotado, agua y voz; las frotadas de cada celda | La piscina en perspectiva es la sala; un embudo baja del pie al charco pasando por la placa, que es la matriz |
| 6 · Retórica y poética | El poema, sus trece figuras y lo que cada una hace en la letra | Un cuaderno: el poema entero adentro del agua; alrededor, un dibujo por figura, unido a su verso por una línea |

Toman de sus referencias (notaciones dibujadas a mano, con acuarela, órbitas, ejes y haces; una sala en perspectiva con un embudo y bandadas de signos; un cuaderno de pictogramas) el modo de dibujar, y de *Contenida* el sentido de cada gesto (`mano.py`):

- la línea tiembla apenas, como la mano que calca;
- toda órbita se abre en su punto más bajo, como toda cuenca en su desagüe;
- lo continuo es lo hallado y lo punteado, lo reconstruido o lo que todavía no es;
- cada color es un material: violeta, la tinta del esténcil; lila, el agua; grafito, el frotado; plata, el aluminio; hueso, la cinta; la tinta, lo hallado. El verde es solo luz y no se dibuja;
- a máquina (Courier Prime) va lo que ya estaba escrito: el pie, el poema, los datos. A mano va lo que se hace con eso.

No hay marcos, cajas ni tablas: cada mapa lleva su leyenda a mano y su firma. **La letra de mano es una fuente** (La Belle Aurore, de Kimberly Geswein, SIL OFL; en `../laminas/fuentes/`), no una mano. Los mapas se pueden repasar a mano sobre una impresión: sería la versión que el proyecto pide.

## Rehacerlo

```bash
python3 tipografia/informe/mapas.py     # los seis mapas, en SVG y PNG (necesita Chromium: CHROME)
npm install docx                        # una vez; o NODE_PATH hacia donde esté
pip install fonttools brotli pymupdf
python3 tipografia/informe/armar.py     # el .docx; con LibreOffice (Writer), también el PDF y el índice paginado
```

| Archivo | Qué es |
|---|---|
| `mano.py` | El repertorio de trazos: línea temblada, órbitas abiertas abajo, aguadas (filtros SVG), rayados de grafito, notas sobre las líneas, leyenda y firma |
| `mapas.py` | Dibuja los seis mapas con los datos del proyecto (la caja, las fichas simuladas, los cuerpos de la gramática, el poema) |
| `informe.js` | Arma el .docx con docx (npm): el texto, las tablas, las figuras y los mapas |
| `fuentes_docx.py` | Convierte Newsreader y Courier Prime (SIL OFL) a TTF, una familia por cara, para incrustarlas |
| `armar.py` | Arma el .docx, lo pasa a PDF, busca la página de cada título y vuelve a armarlo con el índice paginado |
| `paginas.json` | Las páginas del índice, de la última vez que se armó con LibreOffice |
| `img/aplicacion.png` | Captura de la aplicación (`../aplicacion/`), para el capítulo 8 |

Hecho con asistencia de IA.
