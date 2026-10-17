# El informe de decisiones

`contenida_informe_de_decisiones.docx` (y su PDF) reúne las decisiones del proyecto, al modo de las dos tesis de referencia: la obra, el marco, el sistema, la gramática, los estados, el taller, la propuesta de la máquina, la retórica y la poética, lo digital, lo que está alrededor y la ética. Lleva seis mapas esquemáticos que conectan conceptos, teoría, retórica y poética en cada etapa del proyecto.

## Los mapas

| Mapa | Qué conecta | Cómo se dibuja |
|---|---|---|
| 1 · El proyecto entero | Las cinco etapas, de la obra a lo digital, con su concepto, su verso y sus fuentes | De arriba abajo, unidas por un hilo de tinta: la piscina, el pie y su calco, las vasijas con la placa y la caja, el frotado y el agua, y lo digital punteado, que vuelve a la caja |
| 2 · Teoría y fuentes | Las dos tesis, Posnansky, Agüero, Uribe y Berenguer, la obra, Cárcamo y Johnson: lo que se toma y lo que no | Cada fuente es un objeto (una vasija rajada, un taburete, una losa con su desagüe, la ¿ y la ?, una placa sobre el agua, un lápiz, los anillos de un tronco); lo que se toma llega en hebras a la o; lo que no, se corta con un tope |
| 3 · La obra, decisión por decisión | Las dieciséis decisiones de la obra y su traducción en la letra | La cadena de desplazamientos es un río hecho de sus materiales (piedra, foto, dibujo, escaneo, aluminio, cuerpo, video, charco, azulejo); de cada tramo sale una línea hacia su decisión, que lleva su dibujo |
| 4 · Del pie a los 55 signos | Las medidas del pie, la forma de la obra, los parámetros, los generadores, sus familias y la caja | El pie a máquina; las cuatro vasijas en aguada con sus cotas, medidas sobre los cuerpos de la gramática; debajo de cada una, su familia; abajo, la caja |
| 5 · La cadena de estados | Pie, calco, placa, cinta, frotado, agua y voz | Cada estado con su material, unidos por un hilo de tinta que baja hasta la piscina; la vuelta punteada devuelve el esténcil a la placa |
| 6 · Retórica y poética | El poema, sus trece figuras y lo que cada una hace en la letra | El poema entero en una columna de agua que gotea; a cada lado, la figura junto a su verso, con su dibujo |

Se rehicieron el 17.10.2026 tomando como modelo las versiones mejoradas que trajo Joaquin. De ellas se toma el modo de dibujar; de *Contenida*, el sentido de cada gesto (`mano.py`, `materia.py`):

- cada material se dibuja como material: el aluminio se arruga y la letra sube en relieve de contorno, como la deja el punzón; el grafito raya; la cinta se corta en tiras; el calco se transparenta; el agua ondula. No son fotos: son filtros de SVG (ruido, luz rasante, desplazamiento) y trazos calculados;
- un hilo de tinta violeta une las etapas y gotea donde la obra gotea;
- la línea tiembla apenas, como la mano que calca;
- lo continuo es lo hallado y lo punteado, lo reconstruido o lo que todavía no es;
- cada color es un material: violeta, la tinta del esténcil; lila, el agua; grafito, el frotado; plata, el aluminio; hueso, la cinta; la tinta, lo hallado. El verde es solo luz y no se dibuja;
- a máquina (Courier Prime) va lo que ya estaba escrito y lo que hay que saber: el pie, el poema, los datos, las notas. A mano van los títulos.

**La letra de mano es una fuente** (La Belle Aurore, de Kimberly Geswein, SIL OFL; en `../laminas/fuentes/`), no una mano. Los mapas se pueden repasar a mano sobre una impresión: sería la versión que el proyecto pide.

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
| `materia.py` | Los materiales: aluminio con luz rasante y la letra en relieve, frotado de grafito, cinta, calco, papel rasgado, agua con ondas y reflejo, el hilo de tinta y los rótulos |
| `mapas.py` | Dibuja los seis mapas con los datos del proyecto (la caja, las fichas simuladas, los cuerpos de la gramática, el poema) |
| `informe.js` | Arma el .docx con docx (npm): el texto, las tablas, las figuras y los mapas |
| `fuentes_docx.py` | Convierte Newsreader y Courier Prime (SIL OFL) a TTF, una familia por cara, para incrustarlas |
| `armar.py` | Arma el .docx, lo pasa a PDF, busca la página de cada título y vuelve a armarlo con el índice paginado |
| `paginas.json` | Las páginas del índice, de la última vez que se armó con LibreOffice |
| `img/aplicacion.png` | Captura de la aplicación (`../aplicacion/`), para el capítulo 8 |

Hecho con asistencia de IA.
