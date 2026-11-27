# Archivo del proyecto «Cosecha de piedras»

Este archivo ordena lo que se produjo al desarrollar el artículo «Cosecha de piedras: el *ayllu*, el Estado y la mina. Dibujando *Altiplano* de Raúl Botelho Gosálvez». Reúne lo que quedó registrado en la rama del artículo, en las ramas relacionadas y en la conversación donde se hizo. Sirve para ver qué se hizo, cómo cambió y recuperar cualquier versión anterior sin confundirla con la vigente.

No es una versión nueva del proyecto ni una selección: guarda también los borradores, las pruebas y lo descartado. Los originales siguen en su lugar, sin cambios.

## Qué abarca

- **La rama del artículo,** `claude/altiplano-botelho-article-jm2nlr`: 59 commits, del 25.09.2026 al 27.11.2026 (de `903f43e` a `c5a0489`).
- **De git:** 468 versiones anteriores de archivos (453 copiadas tal cual y 15 que repiten un contenido ya guardado) y los 291 archivos vigentes, registrados en su lugar.
- **De la conversación:** 123 piezas de la carpeta de trabajo (111 copiadas): borradores, dos Word de cambios que se enviaron al autor, guiones de comprobación y vistas de página.
- **Copias funcionales:** 319 imágenes copiadas junto a las páginas que las piden, para que se vean como entonces.
- **Otras ramas:** 211 registros. Las dos ramas de Codex entregaron su archivo a la rama del artículo. La de los registros de arquitectura (`claude/eager-bohr-mx9420`) y la de *La tierra que queda* (`proyecto/la-tierra-que-queda`), que hizo GPT, son otros trabajos que salen de esta rama; se registran y no se copian.
- **En línea:** 11 canales del atlas de Are.na, descritos y no copiados.
- **Lo que falta:** 22 registros de lo que no se archiva o no está, con el motivo. Están en [pendientes.md](pendientes.md).
- **Peso de lo copiado:** 202 MB de git, 82 MB de copias funcionales y 32 MB de la conversación. Lo que viene de git no agranda el repositorio, porque git guarda una sola vez cada contenido.
- **Fuera del archivo:** las ramas `claude/fervent-lovelace-exgqzl` y `claude/zen-cannon-kqblsc` son de otro proyecto (la tipografía *Contenida*) y no se tocan.

## Cómo está ordenado

```
archivo_del_proyecto/
├── README.md               esta guía
├── inventario.csv          un registro por material, con su procedencia
├── linea_de_tiempo.md      todo lo que tiene fecha, en orden
├── pendientes.md           lo que falta, lo que no se copia y las dudas
├── verificacion.md         lo que se comprobó y cómo
├── versiones/              las versiones, por línea de trabajo
│   └── <línea>/
│       ├── README.md       sus versiones, en orden
│       └── AAAA-MM-DD_HHMM_<origen>_<nombre>/
│           ├── ficha.md    qué es, qué cambió y qué lo respalda
│           └── …           los archivos, con su ruta original desde la raíz
├── recursos_compartidos/   lo que usan varias versiones (sigue en su lugar)
└── herramientas/           el guion que armó el archivo y el que lo verifica
```

- [inventario.csv](inventario.csv) · [linea_de_tiempo.md](linea_de_tiempo.md) · [pendientes.md](pendientes.md) · [verificacion.md](verificacion.md) · [versiones/](versiones/README.md) · [recursos_compartidos/](recursos_compartidos/README.md) · [herramientas/](herramientas/)

## Las líneas de trabajo

| Línea | Versiones | Lo vigente, en su lugar |
|---|---|---|
| [El artículo](versiones/articulo/README.md) | 35 de git, 5 de la conversación | [`articulo/`](../articulo/) |
| [Las figuras y las imágenes del artículo](versiones/figuras/README.md) | 26 de git, 1 de la conversación | [`articulo/figuras/`](../articulo/figuras/) |
| [Los esquemas, las notaciones y las guías](versiones/esquemas/README.md) | 10 de git | [`analisis/esquemas/`](../analisis/esquemas/) |
| [El registro de análisis](versiones/analisis/README.md) | 55 de git | [`analisis/`](../analisis/) |
| [Los entregables](versiones/entregables/README.md) | 9 de git | [`entregables/`](../entregables/) |
| [La taxonomía visual](versiones/taxonomia/README.md) | 5 de git | [`taxonomia/`](../taxonomia/) |
| [El informe de convocatorias](versiones/convocatorias/README.md) | 6 de git | [`reports/`](../reports/) |
| [Chhaxwa. Cinco pruebas de construcción](versiones/chhaxwa/README.md) | 4 de git | [`chhaxwa/`](../chhaxwa/) |
| [El índice y las reglas del repositorio](versiones/repositorio/README.md) | 52 de git | [`README.md y AGENTS.md`](../) |
| [Las comprobaciones de la conversación](versiones/comprobaciones/README.md) | 8 de la conversación | no entraron en git |
| [La tierra que queda (rama de GPT, sin unir)](versiones/tierra/README.md) | 1 de la rama relacionada | no está en esta rama |
| [Los registros de arquitectura (rama relacionada, sin unir)](versiones/registros/README.md) | 3 de la rama relacionada | no está en esta rama |

## Cómo se lee

### Las carpetas de versión

Se llaman `AAAA-MM-DD_HHMM_<origen>_<nombre>`: la fecha y la hora (UTC), el origen (el commit o `conversacion`) y unas palabras del commit o de lo que es. No hay números de versión, porque el proyecto no los usó de forma continua y el archivo no los inventa. Los documentos hablan de una «versión 3» y de una «versión final»; cuando lo hacen, la ficha cita el documento.

Cada carpeta guarda **lo que en esa versión era distinto de lo vigente**: lo que cambió en ese commit y ya no está así. Lo que no cambió está en una carpeta anterior o sigue vigente en su lugar. La ficha dice cuántos archivos tenía la línea completa, y el inventario dice cuáles (columna `en_versiones`). Debajo de cada carpeta, los archivos conservan su ruta desde la raíz del repositorio, para que sus enlaces funcionen. Por eso el artículo en `.md` lleva al lado sus figuras tal como eran en ese commit.

### Los estados

Cada material lleva uno, y solo cuando hay un registro que lo sostenga:

- **Versión vigente:** el estado actual de la rama. Es lo más reciente, no lo aprobado.
- **Versión anterior:** la reemplazó un commit posterior, o es un estado intermedio que dejó la conversación antes del commit.
- **Alternativa:** otro camino para lo mismo. Son `articulo/articulo_altiplano` (la «versión 3», que el README conserva como alternativa) y los dos Word de cambios que parten de otra versión.
- **Prueba o experimento:** lo que sirvió para comprobar: guiones, listas de citas y vistas de página.
- **Material descartado:** lo que un commit sacó del proyecto y su mensaje lo dice. Son la cita de Potteiger y Purinton, revertida a pedido del autor, y los recursos del primer generador de diagramas.
- **Estado sin confirmar:** lo que el registro no permite clasificar, como la rama sin unir y los canales en línea que no se volvieron a abrir.
- **Entregable aprobado:** ninguno. En los registros no consta que el autor haya dado por definitivo un archivo ([pendientes.md](pendientes.md)).

Las fuentes de terceros que no se archivan no llevan estado, porque no son material del proyecto.

### Las fechas

Cada fecha dice qué representa, en la columna `que_representa_la_fecha`:

- **La de un commit** es cuándo entró ese contenido en git. No es la fecha en que se creó la obra, ni necesariamente la del archivo.
- **La de la conversación** es la última modificación del archivo en la carpeta de trabajo de la sesión.
- **La del registro** es la que da un documento del proyecto, como las del atlas de Are.na.

Los pies de las figuras 1 a 6 dicen «[medidas, año]»: los pasteles todavía no tienen fecha en el proyecto, y el archivo no les pone una.

### Los números del inventario

| Prefijo | Qué es |
|---|---|
| `V-` | Archivo vigente, registrado en su lugar. No se copia |
| `H-` | Versión anterior sacada de git. Copia exacta, o referencia a otra copia si el contenido se repite |
| `D-` | Copia funcional: una imagen que pide una página archivada |
| `C-` | Pieza de la conversación que no entró en git como estaba |
| `R-` | Archivo de otra rama. No se copia: se dice cómo recuperarlo |
| `L-` | Material en línea. No se copia |
| `N-` | Lo que no se archiva o no está |

### Copias y duplicados

Los duplicados se detectan por contenido: el SHA-256 y el identificador de git de cada archivo están en el inventario. Si un contenido ya está guardado, no se copia otra vez: su fila dice de cuál es duplicado y dónde está. Pasa con el Word de `entregables/01`, que es copia del de `articulo/`, y con los archivos que solo cambiaron de nombre. Un duplicado no es lo mismo que otra exportación: dos Word generados del mismo texto en fechas distintas pueden diferir, y entonces se guardan los dos.

### Lo documentado y lo deducido

Las fichas citan el mensaje del commit y el documento de `analisis/` que respalda cada versión. Eso es lo documentado. La línea de trabajo de cada archivo, el estado «versión anterior» de lo reemplazado y la relación entre un borrador de la conversación y su commit son deducciones del orden y de las fechas, y las fichas lo dicen. Las decisiones del autor que constan están en `analisis/`; el archivo no le atribuye otras.

## La versión vigente

Es el estado de la rama en el commit `c5a0489` (27.11.2026): el artículo en [`articulo/articulo_cosecha_de_piedras.md`](../articulo/articulo_cosecha_de_piedras.md), sus Word y los archivos de [`entregables/`](../entregables/). Qué es cada cosa: el [`README.md`](../README.md) de la raíz. Lo que falta para enviar el artículo: [`entregables/02_lista_de_envio.md`](../entregables/02_lista_de_envio.md).

## Cómo recuperar una versión

- **Un archivo:** ábrelo en su carpeta de `versiones/`, o búscalo en `inventario.csv` por su ruta original.
- **Un archivo, desde git:** `git show <commit>:<ruta>`, con el commit y la ruta del inventario.
- **El proyecto entero como estaba:** `git worktree add ../altiplano_<commit> <commit>`. Cuando termines, `git worktree remove ../altiplano_<commit>`.
- **Volver a una versión:** copia el archivo a su lugar en una rama nueva y propón el cambio. No lo hagas sobre la rama del artículo sin que el autor lo pida.

## Verificación

[verificacion.md](verificacion.md) dice qué se comprobó: que cada copia coincide con su origen en git, que el inventario ubica todo lo recuperado, que los enlaces funcionan y que los originales no cambiaron. Se rehace con `python3 archivo_del_proyecto/herramientas/verificar_archivo.py`.

El archivo se arma con `python3 archivo_del_proyecto/herramientas/armar_archivo.py`. No se edita a mano: si el proyecto cambia, se corre otra vez.
