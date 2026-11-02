# 06. Ética, fuentes y pendientes

## 6.1. Consentimiento y créditos

*Contenida* es un homenaje, pero se hace con la obra de otra persona. Las dos tesis insisten en esto:

- Mahendran, en la ética del que viene de afuera;
- Tshuma, en que la autoría y la economía del trabajo creativo también se descolonizan.

**Reglas:**

- **Rebeca primero.** Nada se hace antes de la Acción 0. Si ella no está de acuerdo, el proyecto se detiene o cambia.
- **Créditos.**
  - Rebeca Paz Prada y CreaciónxAcuerpamiento van en el colofón, en la forma que ellas elijan.
  - Artefacto Tatuajes, como sede.
  - Cada mano de la cadena, con su nombre o con «sin nombre registrado».
- **El cuerpo.** Acuerdo escrito de quien vista las placas. El cuerpo de Rebeca no se usa salvo que ella lo proponga.
- **La piscina.** Permiso escrito del estudio y del edificio. No se saca ni se deja nada.
- **El dinero.** Nada se vende sin acuerdo. Si alguna vez hay ingresos, el reparto se acuerda antes (`05`, §5.6).

## 6.2. Lo que no está en el repositorio

- **Las fotos de la obra y los dos videos.** Son imágenes de Rebeca y de su cuerpo, y la foto de la lámina parece venir de su propio registro. Por eso no se suben. Lo que el proyecto usa de ellas está descrito en `01`, con los segundos de cada observación.
- **Tu lámina con el poema.** El poema está transcrito en `textos/poema.txt`; el dibujo no se sube.

Si Rebeca lo autoriza, se puede agregar una carpeta `referencias/`.

## 6.3. Asistencia de inteligencia artificial

Los textos de esta carpeta, el recuento de `inventario.py`, los esquemas de `esquemas/`, el código de `simulacion/` y las láminas de `laminas/` se hicieron con asistencia de inteligencia artificial. Es la misma práctica de declaración del artículo de este repositorio.

**Las formas de letra que genera `simulacion/` son la propuesta de la máquina.** Están hechas para confrontarlas con las de la mano y no entran en la caja ni en la fuente. Salen de un testigo sustituto, Liberation Serif (licencia SIL OFL), porque el pie del libro no se puede calcar desde la foto. Los esquemas son planos (caja, pauta, ficha, cadena, montajes), y las letras de la caja quedan para la mano. Si el proyecto se muestra o se publica, esto va en el colofón.

## 6.4. Qué está verificado y qué no

| Afirmación | Estado | Cómo verificar |
|---|---|---|
| El texto del pie | Transcrito desde una foto de baja resolución | Transcribirlo desde el libro y volver a correr `inventario.py` |
| 8 × 7 = 56 celdas en la cabeza | Contado en la foto | Recontar en el impreso |
| El libro de la lámina | Sin identificar. Pistas: es un desplegable, el pie habla de Posnansky en tercera persona y la página de enfrente cita a Ponce Sanginés | Autor, título, año, página |
| El dibujo de Posnansky | Agüero, Uribe y Berenguer (2003, fig. 12) lo citan: Posnansky 1945, vol. 2, figs. 100, 101a, 101b y 102a | Cotejar esas figuras con la lámina de Rebeca |
| Registro de Posnansky: hallado al sur del Akapana, asperón colorado, excavado en 1903, cuerpo cubierto por el signo «pez» | Según tu texto. Agüero, Uribe y Berenguer (2003) registran cabezas de pez de perfil en los personajes de la Kochamama, y un Personaje Frontal en el pecho y otro en la espalda | Buscar la lámina o la figura en *Tihuanacu, la cuna del hombre americano* (Posnansky, 1945-1957) |
| Quién excavó en 1903 | Sin dato | En 1903 trabajó en Tiwanaku una misión francesa (Créqui-Montfort); hay que confirmar si esta pieza fue suya |
| El nombre «Kochamama» y su sentido (madre del agua) | Según tu texto | Quién la nombró y cuándo. *Qucha* es quechua y *quta*, aymara: revisar Bertonio (ya citado en el artículo) y un diccionario quechua |
| El monolito se llama «vaso» en su ficha | Según tu texto | ¿Qué ficha? ¿De qué museo o catálogo? |
| Dónde está hoy el monolito | Sin dato | — |
| El boceto «Monolita / Rebe», con puertas en el pecho y la espalda | Según tu texto; no lo vi | Pedírselo a Rebeca, o su permiso para citarlo |
| La duración del bucle | Sin dato | Preguntarle a Rebeca (Acción 0) |
| La tilde en «És lo más parecido» | Se ve en la imagen del poema | Decidir si es errata |
| Quién hizo el dibujo de tu lámina con el poema | Sin confirmar | Confirmarlo si se reproduce |
| La receta del hectógrafo y la compatibilidad del esténcil térmico con la gelatina | Receta de partida | Probarlas antes de la tirada (Acción 8) |
| Citas de las dos tesis | Cotejadas con el texto de los `.docx` | Agregar páginas desde los PDF originales si se citan en público |
| La frase de otro asistente sobre «nuestro envase convulso: el cuerpo» | Citada en tu texto | No se usa. Si se usa, pedir permiso y nombrar a su autor |

**Fuente publicada:** Agüero Piwonka, Carolina; Mauricio Uribe Rodríguez y José Berenguer Rodríguez (2003). «La iconografía Tiwanaku: el caso de la escultura lítica». *Textos Antropológicos* 14 (2): 47-82. El PDF no se sube al repositorio: se cita.

## 6.5. Lo que el proyecto no afirma

- **No interpreta la iconografía de Tiwanaku** ni el «calendario» de la Kochamama.
- **Los números del sistema son convenios, no lecturas.** Las 56 celdas, las 7 filas y los 30 hallazgos cuentan contenedores y letras. Ninguno se presenta como clave de nada.
- **No es una tipografía «andina».** Es una tipografía latina de caja baja, hecha con las operaciones de una obra que ocurrió en La Paz.

## 6.6. Pendientes, en orden

- [ ] Acción 0: hablar con Rebeca y con CreaciónxAcuerpamiento; pedir los permisos del estudio y del edificio.
- [ ] Identificar el libro de la lámina y fotografiar el pie con luz rasante.
- [ ] Corregir `textos/pie_de_lamina.txt` y volver a correr `inventario.py` y `generar_esquemas.py`.
- [ ] Medir la piscina (azulejo, tesela, junta, paredes) y regenerar la pauta.
- [ ] Hacer los frotados (paño de pared de 8 × 7 y paño de piso).
- [ ] Probar el repujado en hoja simple y doble; decidir.
- [ ] Probar la receta del hectógrafo y los dos tipos de matriz.
- [ ] Verificar los datos de Posnansky, el nombre y la ficha del «vaso».
- [ ] Confrontar la propuesta de la mano con la de la máquina (`simulacion/informe.md`, «Cómo confrontar»).
