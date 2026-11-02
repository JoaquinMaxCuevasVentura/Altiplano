# Archivo del proyecto *Contenida*

Este archivo ordena lo que se produjo al desarrollar *Contenida*, la tipografía en homenaje a *Contener una ruina: acciones para desenterrar una voz*, de Rebeca Paz Prada. Reúne lo que quedó registrado en la rama del proyecto, en esta conversación y en los artefactos publicados en claude.ai. Sirve para ver qué se hizo, cómo cambió y recuperar cualquier versión anterior sin confundirla con la vigente.

No es una versión nueva del proyecto ni una selección: guarda también las pruebas, los borradores y lo descartado. Los originales siguen en su lugar, sin cambios.

## Qué abarca

- **Solo *Contenida*.** Es la carpeta `tipografia/` y sus 41 commits en la rama `claude/fervent-lovelace-exgqzl`, del 29.09 al 30.10.2026 (de `0cabb65` a `02dcb14`). El repositorio guarda también el artículo *Altiplano* (la raíz, `articulo/` y `analisis/`, con su propia rama): es otro proyecto y queda fuera. Por eso este archivo está dentro de `tipografia/` y no en la raíz.
- **De git:** 562 versiones anteriores de archivos, copiadas tal cual, y los 617 archivos vigentes, registrados en su lugar.
- **De la conversación:** 138 piezas que no entraron en git como estaban: borradores, una propuesta descartada, pruebas y las imágenes de prueba que se vieron.
- **En línea:** 5 registros de los artefactos del proyecto en claude.ai, con sus copias.
- **Copias funcionales:** 273 dependencias copiadas al lado de las páginas y los SVG que las piden, para que abran.
- **Lo que falta:** 34 registros de lo que no se archiva o no está, con el motivo. Están en [pendientes.md](pendientes.md).
- **Peso de lo copiado:** 422 MB. Lo que viene de git no agranda el repositorio: git guarda una sola vez cada contenido.

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
│           └── …           los archivos, con su ruta original desde tipografia/
├── recursos_compartidos/   lo que usan varias versiones (sigue en su lugar)
└── herramientas/           el guion que armó el archivo y el que lo verifica
```

- [inventario.csv](inventario.csv) · [linea_de_tiempo.md](linea_de_tiempo.md) · [pendientes.md](pendientes.md) · [verificacion.md](verificacion.md) · [versiones/](versiones/README.md) · [recursos_compartidos/](recursos_compartidos/README.md) · [herramientas/](herramientas/)

## Las líneas de trabajo

| Línea | Versiones | Lo vigente, en su lugar |
|---|---|---|
| [Los documentos](versiones/documentos/README.md) | 37 de git | [`tipografia/`](../) |
| [Los textos de partida](versiones/textos/README.md) | 1 de git | [`tipografia/textos/`](../textos/) |
| [Los esquemas](versiones/esquemas/README.md) | 5 de git | [`tipografia/esquemas/`](../esquemas/) |
| [La simulación del taller](versiones/simulacion/README.md) | 11 de git | [`tipografia/simulacion/`](../simulacion/) |
| [Las láminas de exposición](versiones/laminas/README.md) | 7 de git | [`tipografia/laminas/`](../laminas/) |
| [La aplicación de las decisiones de la letra](versiones/aplicacion/README.md) | 5 de git, 3 de la conversación, 2 en línea | [`tipografia/aplicacion/`](../aplicacion/) |
| [El informe de decisiones](versiones/informe/README.md) | 12 de git, 1 de la conversación | [`tipografia/informe/`](../informe/) |
| [La póliza en OpenType](versiones/digital/README.md) | 2 de git | [`tipografia/digital/`](../digital/) |
| [Los planos de la anatomía base](versiones/planos/README.md) | 3 de git | [`tipografia/planos/`](../planos/) |
| [La taxonomía de las referencias](versiones/taxonomia/README.md) | 3 de git | [`tipografia/taxonomia/`](../taxonomia/) |
| [El ensayo del repujado](versiones/repujado/README.md) | 3 de git, 1 en línea | [`tipografia/repujado/`](../repujado/) |
| [El libro de Contenida](versiones/editorial/README.md) | 2 de git, 3 de la conversación, 1 en línea | [`tipografia/editorial/`](../editorial/) |

## Cómo se lee

### Las carpetas de versión

Se llaman `AAAA-MM-DD_HHMM_<origen>_<nombre>`: la fecha y la hora (UTC), el origen (el commit, `conversacion` o `en-linea`) y unas palabras del commit o de lo que es. No hay números de versión: el proyecto no los usó y el archivo no los inventa.

Cada carpeta guarda **lo que en esa versión era distinto de lo vigente**: lo que cambió en ese commit y ya no está así. Lo que no cambió está en una carpeta anterior o sigue vigente en su lugar. La ficha dice cuántos archivos tenía la versión completa, y el inventario dice cuáles (columna `en_versiones`). Debajo de cada carpeta, los archivos conservan su ruta desde `tipografia/` para que sus enlaces funcionen. Por eso las páginas HTML y los SVG llevan al lado copias de lo que piden: imágenes, estilos, letras y guiones.

### Los estados

Cada material lleva uno, y solo cuando hay un registro que lo sostenga:

- **Versión vigente:** el estado actual de la rama, o la última versión publicada en línea. Es lo más reciente, no lo aprobado.
- **Versión anterior:** la reemplazó un commit posterior, o es un estado intermedio que dejó la conversación antes del commit.
- **Alternativa:** otro camino para lo mismo. Es el caso del encargo editorial para otra IA.
- **Prueba o experimento:** lo que sirvió para comprobar: guiones de prueba, capturas, vistas de páginas.
- **Material descartado:** lo que un commit o un mensaje sacó del proyecto. Su ficha o su fila citan el registro.
- **Estado sin confirmar:** lo que salió sin que el registro diga por qué, o lo que no se sabe si es del proyecto.
- **Entregable aprobado:** ninguno, porque en los registros no consta una aprobación.

Las referencias de terceros, como los videos y las imágenes de otros libros, no llevan estado: no son material del proyecto.

### Las fechas

Cada fecha dice qué representa, en la columna `que_representa_la_fecha`:

- **La de un commit** es cuándo entró ese contenido en git. No es la fecha en que se creó la obra, ni necesariamente la del archivo.
- **La de la conversación** es cuándo se escribió o se vio algo.
- **La de un artefacto** es cuándo se publicó esa versión, deducida de su identificador.

La obra de Rebeca Paz Prada es del 22 de agosto de 2026: ningún archivo del proyecto tiene esa fecha.

### Los números del inventario

| Prefijo | Qué es |
|---|---|
| `V-` | Vigente, en su lugar: no se copia |
| `H-` | Versión anterior recuperada de git: copia exacta |
| `D-` | Copia funcional de una dependencia: el original tiene su propio número |
| `C-` | De la conversación |
| `L-` | De un artefacto en línea |
| `N-` | Lo que no se archiva o no está |

### Las copias y los duplicados

Todo se comparó por contenido, con SHA-256 y con el hash de git. Un contenido que ya está archivado o vigente no se copia otra vez: se anota como «duplicado exacto», con el número del original. Las copias funcionales son la única repetición, y se hacen para que una versión abra. No cuentan como duplicado otra exportación, otro formato o una copia reducida: un .docx y su PDF, una lámina en HTML y en PNG, una captura y la copia reducida que guardó la conversación.

### Lo documentado y lo deducido

Las fichas separan lo que respalda cada versión (el mensaje del commit, un mensaje del pedido, el README de esa versión) de lo que deduce el archivo, como el estado. Ninguna decisión se atribuye al autor sin un registro, y lo que es deducción se dice.

## La versión vigente

Está en su lugar, en [`tipografia/`](../), y no se copia. El inventario la registra con su número `V-`, su hash y el commit en que entró cada archivo. En línea, lo vigente son los artefactos «Gramática de Contenida» (versión 5) y «El repujado de Contenida», copiados en sus líneas.

## Cómo recuperar una versión

- **Un archivo:** copia el de su carpeta de versión. Es idéntico al de git: tiene el mismo hash.
- **Desde git, sin pasar por el archivo:** `git show <commit>:<ruta>`. Por ejemplo, `git show e8962b4:tipografia/aplicacion/app.js` da la aplicación de septiembre.
- **El repositorio entero como estaba:** `git worktree add ../contenida_<commit> <commit>`. Sirve para rehacer los resultados con sus generadores, que leen de varias carpetas a la vez.

## Verificación

[verificacion.md](verificacion.md) dice qué se comprobó y con qué resultado. Para repetirlo, desde la raíz del repositorio:

```bash
python3 tipografia/archivo_del_proyecto/herramientas/verificar_archivo.py
```

El armado se puede leer en `herramientas/armar_archivo.py`. Su parte de git se puede rehacer en cualquier copia del repositorio; la de la conversación necesita su registro, que no está en el repositorio.

## Asistencia de IA

Este archivo lo armó Claude a pedido de quien lleva el proyecto. Ordena y registra; no decide. Lo que deduce, lo dice.
