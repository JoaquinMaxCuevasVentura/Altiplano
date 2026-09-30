# 05. La migración digital: si cierra

## 5.1. ¿Es coherente migrar?

**La obra ya migra, y no termina en lo digital.** Su orden es repujado (analógico) → video (digital) → agua (luz) → pared (azulejo). El video es un estado intermedio: se proyecta a través del agua y vuelve a ser materia sobre una pared.

**Por eso la migración de *Contenida* es coherente solo si repite ese lugar.** Lo digital tiene que ser un estado más de la cadena, no el final limpio. Tiene que volver a pasar por el agua y volver a ser placa.

**Lista para decidir** (Acción 12). Si algún punto falla, no se migra: la caja ya es la tipografía completa.

1. **La caja está completa:** 56 celdas, 119 placas, 119 fichas.
2. **Rebeca está de acuerdo** con la versión digital y con su licencia.
3. **La procedencia viaja con la fuente:** las fichas y el colofón van dentro del archivo y a su lado (§5.3).
4. **Lo reconstruido sigue punteado** en todos los estilos digitales.
5. **No hay un estilo limpio ni un Regular:** cada estilo digital sale de un registro físico.
6. **La salida vuelve a lo analógico:** se proyecta a través del agua y se imprime como esténcil para placas nuevas (§5.5).

## 5.2. Qué se digitaliza y cómo

**Herramientas libres.** FontForge, fontTools y potrace son gratuitas, como pide Tshuma para el acceso y Mahendran para las tecnologías abiertas.

| Estilo | Registro de origen | Captura |
|---|---|---|
| Calco | Los 56 calcos | Escáner, 600 ppp, en grises |
| Placa y Cinta | Las placas, por las dos caras, y la cinta sobre el plástico | Foto con la luz rasante fija de las Acciones 4 y 6, con regla en cuadro. Probar también el escáner plano, que ilumina desde un solo lado |
| Frotado 01 … *n* | Los frotados numerados | Escáner, 600 ppp. Cada frotado es de una placa: se escanea en orden, del primero al último que se lee |
| Agua, Voz | Las fotos de las Acciones 9 y 10 | Sin corregir la perspectiva: el trapecio se queda |

**Vectorización.**

- Umbral a blanco y negro, y después potrace, con parámetros que conserven las irregularidades (por ejemplo, `--turdsize 2 --alphamax 1.0`).
- Los parámetros de cada estilo se anotan en un archivo junto a la fuente.
- A mano solo se corrigen errores técnicos, como contornos abiertos o cruzados. Ni un nodo por estética.

## 5.3. La fuente

| Parámetro | Valor | Por qué |
|---|---|---|
| Unidades por eme | 200 por tesela: 1200 si el azulejo mide 6 teselas | El eme es el azulejo; la unidad, la tesela |
| Avance | Azulejo + junta, en la proporción medida (1224 con azulejo de 150 mm y junta de 3 mm) | Monoespaciada: la junta es el espacio entre letras |
| Alto de línea | Igual al avance | Las filas de azulejos se apilan con su junta |
| Métricas verticales | Las de la pauta corregida (`03`, §3.6) | Las decide el pie, no una norma |
| Glifos | Los 56 de la caja, más `.notdef` | El juego cabe en la retícula |
| Mapa de caracteres | Las mayúsculas se escriben con los glifos de caja baja. «¡ !», el guion, las comillas inglesas y el apóstrofo quedan sin glifo | Lo que no cabe se ve como celda vacía |
| `.notdef` | La celda de la lámina, calcada a mano y escaneada | El único préstamo directo del monolito es un marco vacío |
| `¶` | El signo final de la celda 56 | Se escribe con la tecla o el atajo del calderón |
| Variantes | Cada placa de la póliza que pasó por ese estado es una variante: `a.01` … `a.09`, `e.01` … `e.08` | Cada «a» es una placa distinta |
| Alternancia | `calt`: la variante cambia según el signo anterior, con la técnica habitual de las letras de apariencia manual. En el componedor web (§5.4) el ciclo es exacto por letra, como en la caja | En el archivo de fuente, la alternancia es aproximada, y se dice. El antecedente es *Beowolf* (LettError, 1990), que cambiaba sus contornos en cada impresión |
| Estilos | Un archivo por estado: Calco, Placa, Cinta, Frotado 01 … *n*, Agua, Voz | No hay pesos interpolados: si falta el frotado 17, no hay estilo 17 |
| Nombres | Familia tipográfica *Contenida* y subfamilia con el nombre del estado (campos 16 y 17 de la tabla `name`). El campo 2 dice *Regular* porque los sistemas lo exigen | Es el único lugar donde aparece esa palabra: un campo técnico que nadie lee |
| Descripción | El colofón de manos completo (campo 10) | La procedencia viaja dentro del archivo |
| Diseño | Todas las manos de la cadena (campo 9) | — |
| Fichas | `contenida_fichas.json`, junto a la fuente, y una nota de procedencia en cada glifo | — |
| Licencia | A acordar con Rebeca (§5.6) | — |

## 5.4. El espécimen digital

Una página web: la versión digital de la bandeja, no un catálogo.

- **Oscura.** El texto es luz verde, que en este proyecto solo existe como luz. Debajo, apenas visible, está el frotado de la pared: la retícula real, con sus grietas.
- **El texto es el poema en bucle**, línea por línea, en filas de azulejo. Se usa el ciclo exacto de la póliza: dentro de un verso ninguna letra se repite igual.
- **El bloque de texto llega en trapecio**, más ancho arriba, como la proyección.
- **Tocar deforma.** Al tocar o pasar el puntero, entran ondas concéntricas desde ese punto (un filtro de desplazamiento) y se apagan en unos segundos.
  - Cuando el texto se recompone, el ciclo de variantes avanzó: vuelve, pero no igual.
  - Opcional: los puntos (el de la i, el punto final) no se deforman, como el punto de luz fijo de los videos (`01`, §1.4).
- **Sin sonido.**
- **Sin estado por defecto fijo.** La página abre en el estado siguiente al de la última visita, guardado solo en el navegador de quien mira.

Es la misma página que se proyecta en la presentación a través de la bandeja (§5.5).

## 5.5. Cómo cierra: termina y empieza

**La presentación.** Si el edificio lo permite, en la misma piscina:

- el espécimen digital, proyectado a través de una bandeja con un dedo de agua sobre la misma pared donde se proyectó el video de Rebeca;
- el pliego de agua (esquema C), colgado sobre otra bandeja;
- los frotados, repartidos al público en orden de llegada. Quien llega primero recibe el *Frotado 01*; quien llega último, casi nada. El peso de cada frotado depende de cuándo llegó quien lo recibe.

**La vuelta.** La fuente se imprime en la máquina de esténcil térmico del estudio y el esténcil sirve de calco para repujar placas nuevas. Esas placas llenan una segunda caja, cuyas fichas dicen «generación 2».

Lo digital no termina la cadena: le da la vuelta, como la mesa serif de Tshuma, que va del objeto al signo y del signo al objeto. «Termina y empieza, / termina y empieza.»

## 5.6. Lo que no se hace

- **No se publica un máster limpio:** ninguna versión redibujada «bien» de las letras.
- **No se interpolan pesos.** Los frotados intermedios no se inventan.
- **No se generan letras** con inteligencia artificial ni por procedimiento. Las variantes son placas.
- **No se agregan** mayúsculas, exclamaciones ni signos fuera de la caja.
- **No se usa** el nombre del ídolo ni signos tiwanacotas.
- **No se vende sin acuerdo.** Hay dos caminos, a decidir con Rebeca:
  - **Licencia libre (SIL Open Font License):** permite usar, modificar y redistribuir, incluso en trabajos comerciales, pero no vender la fuente sola. Es coherente con el acceso que piden las dos tesis.
  - **Licencia de uso no comercial,** redactada entre ustedes. Protege más la obra y circula menos.
