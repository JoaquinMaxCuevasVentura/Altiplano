# 39. El archivo del proyecto

15 de noviembre de 2026. El autor pidió ordenar todo lo que se produjo al desarrollar el artículo, con sus versiones e iteraciones, en una carpeta que permita ver qué se hizo, cómo cambió y recuperar una versión anterior sin confundirla con la vigente. No quería una versión nueva ni una selección de lo mejor. El resultado está en `archivo_del_proyecto/`, y su guía es `archivo_del_proyecto/README.md`.

Este documento registra de dónde salió cada cosa y las decisiones de organización. Todas se pueden deshacer: el archivo lo arma un guion, y los originales no se tocaron.

## 1. De dónde se reconstruyó

| Fuente | Qué dio |
|---|---|
| La rama del artículo, commit por commit | Cada contenido que tuvo cada archivo, con la fecha en que entró en git y el mensaje que lo explica |
| Las ramas de Codex (`codex/analisis-churata` y `codex/auditoria-version-final`) | Dónde aparecieron por primera vez `analisis/32` y `analisis/34` |
| La rama `claude/eager-bohr-mx9420` | Los registros de arquitectura, de donde salieron dos imágenes del artículo |
| `analisis/`, `README.md`, `AGENTS.md` y los `LEEME.md` | El porqué de los cambios y las decisiones del autor que constan |
| El registro de la conversación, desde el 18 de octubre | Qué se le envió al autor y cuándo |
| La carpeta de trabajo de la sesión | Borradores, guiones de comprobación y vistas de página que nunca entraron en git |

La conversación anterior al 18 de octubre solo quedó resumida, y sus archivos de trabajo se perdieron. Lo que produjo sí está en git.

## 2. Decisiones de organización

- **Por líneas de trabajo.** El artículo, las figuras, los esquemas, el registro de análisis, los entregables, la taxonomía, las convocatorias y el índice del repositorio cambian a ritmos distintos. Ordenarlos juntos por fecha habría mezclado cuarenta versiones del artículo con las de los tableros.
- **Sin números de versión nuevos.** El proyecto habla de una «versión 3» y de una «versión final», pero no numeró las demás. Las carpetas llevan la fecha, el commit y unas palabras de su mensaje.
- **Lo vigente no se copia.** Sigue en su lugar y el inventario lo registra allí. Cada carpeta de versión guarda solo lo que entonces era distinto.
- **Las rutas se conservan.** Dentro de cada carpeta, los archivos mantienen su ruta desde la raíz. El artículo en `.md` de cada versión lleva al lado sus figuras de entonces, para que se vea como era.
- **Los duplicados se detectan por contenido.** Un contenido ya guardado no se copia otra vez: su registro dice de cuál es duplicado. Pasa con el Word de `entregables/01`, que es copia del de `articulo/`.
- **Los estados, solo con registro.** «Material descartado» se usa donde un mensaje de commit lo dice, como la cita de Potteiger y Purinton, que se revirtió a pedido del autor. Lo que solo fue reemplazado es «versión anterior».
- **Ningún entregable figura como aprobado.** El autor aprobó correcciones y tomó decisiones, pero no consta que haya dado por definitivo un archivo, y piensa reescribir el artículo con su voz. Lo más reciente figura como «versión vigente».
- **Las fechas dicen qué son.** La de un commit es cuándo entró ese contenido en git, no cuándo se creó la obra. Los pasteles no tienen fecha en el proyecto y el archivo no les pone una.

## 3. Lo que quedó fuera, y por qué

- **Las fuentes** (los 25 archivos del cotejo, los dos libros de Churata y sus textos extraídos) tienen derechos de autor y el repositorio es público. El inventario dice dónde están.
- **El registro de la conversación** contiene datos privados del autor y el enlace de su carpeta.
- **Los registros de arquitectura** siguen en su rama. El inventario los lista uno por uno y dice cómo recuperarlos, pero no los copia: es otro trabajo, tiene imágenes con derechos y no consta la decisión de unirlo.
- **Las ramas `claude/fervent-lovelace-exgqzl` y `claude/zen-cannon-kqblsc`** son de la tipografía *Contenida*, que tiene su propio archivo.
- **El atlas de Are.na** está en línea y es privado. El archivo guarda su descripción.

## 4. Lo que sí entró de la conversación

Unos 24 MB que no estaban en git:

- el borrador por partes de la versión final del 2 de noviembre;
- los dos Word de cambios que se le enviaron al autor el 10 de noviembre, que comparan con otra versión que el Word de cambios del repositorio;
- el artículo tal como estaba antes de las cursivas;
- los guiones con que se comprobaron las citas y los patrones de redacción, con sus listas;
- las vistas de página de la auditoría;
- las páginas de Internet Archive de donde salen las imágenes 1 y 3, que son de dominio público.

## 5. Cómo se rehace y cómo se comprueba

```bash
python3 archivo_del_proyecto/herramientas/armar_archivo.py       # lo arma de nuevo desde git
python3 archivo_del_proyecto/herramientas/verificar_archivo.py   # lo comprueba y escribe verificacion.md
```

El verificador compara cada copia con el contenido de su ruta en su commit, revisa que el inventario ubique todo lo que hubo en la historia, que los enlaces funcionen y que nada cambió fuera de `archivo_del_proyecto/`. Si el proyecto cambia, se corre otra vez el primer guion. Las piezas de la conversación ya copiadas se conservan.

## 6. Lo que queda para el autor

Está en `archivo_del_proyecto/pendientes.md`. Lo principal:

- decidir si la rama de los registros de arquitectura se une, y entonces renumerar su `analisis/34`;
- decidir si se conservan las dos ramas de Codex, que ya entregaron su archivo;
- si guarda las imágenes de exploración hechas con IA o las cinco referencias de estilo del 30 de septiembre, decidir si pueden estar en un repositorio público antes de archivarlas.
