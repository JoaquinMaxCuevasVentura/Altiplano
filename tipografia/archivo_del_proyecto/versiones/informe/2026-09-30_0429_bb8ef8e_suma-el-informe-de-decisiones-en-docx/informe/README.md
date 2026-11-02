# El informe de decisiones

`contenida_informe_de_decisiones.docx` (y su PDF) reúne las decisiones del proyecto, al modo de las dos tesis de referencia: la obra, el marco, el sistema, la gramática, los estados, el taller, la propuesta de la máquina, la retórica y la poética, lo digital y la ética. Lleva seis mapas esquemáticos que conectan conceptos, teoría, retórica y poética en cada etapa del proyecto.

## Los mapas

| Mapa | Qué conecta |
|---|---|
| 1 · El proyecto entero | Las cinco etapas (la obra, desenterrar, contener, devolver, lo digital), en ciclo, con su concepto, su teoría, su figura y su verso |
| 2 · Teoría y fuentes | Las dos tesis, Posnansky, Agüero, Uribe y Berenguer y la obra: lo que se toma y lo que no, sobre la caja de 8 × 7 |
| 3 · La obra, decisión por decisión | Las dieciséis decisiones de la obra sobre la cadena de desplazamientos, con su traducción en la letra |
| 4 · Del pie a los 55 signos | Las medidas del pie y la forma de la obra; los parámetros, las partes, los cuatro generadores y la caja |
| 5 · La cadena de estados | Calco, placa, cinta, frotado, agua y voz: la materia que se pierde y la luz que se gana; las frotadas de cada celda |
| 6 · Retórica y poética | Los versos del poema, sus figuras y lo que cada figura hace en la letra |

Toman de las referencias el modo de dibujar: haces de líneas finas, rayado vertical, vasijas acotadas, redes sobre un plano y una ficha en la esquina. De *Contenida* toman todo lo demás. La tinta es el violeta del esténcil y el gris del grafito; los nodos son celdas de la cabeza del ídolo, abiertas en su desagüe; las vasijas son los generadores o, l, n y a; los rótulos van en Courier Prime y los versos en Newsreader cursiva.

## Rehacerlo

```bash
python3 tipografia/informe/mapas.py     # los seis mapas, en SVG y PNG (necesita Chromium: CHROME)
npm install docx                        # una vez; o NODE_PATH hacia donde esté
pip install fonttools brotli pymupdf
python3 tipografia/informe/armar.py     # el .docx; con LibreOffice (Writer), también el PDF y el índice paginado
```

| Archivo | Qué es |
|---|---|
| `mapas.py` | Dibuja los mapas con los datos del proyecto (la caja, las fichas simuladas, los cuerpos de los generadores, el poema) |
| `informe.js` | Arma el .docx con docx (npm): el texto, las tablas, las figuras y los mapas |
| `fuentes_docx.py` | Convierte Newsreader y Courier Prime (SIL OFL) a TTF, una familia por cara, para incrustarlas |
| `armar.py` | Arma el .docx, lo pasa a PDF, busca la página de cada título y vuelve a armarlo con el índice paginado |
| `paginas.json` | Las páginas del índice, de la última vez que se armó con LibreOffice |
| `img/aplicacion.png` | Captura de la aplicación (`../aplicacion/`), para el capítulo 8 |

Hecho con asistencia de IA.
