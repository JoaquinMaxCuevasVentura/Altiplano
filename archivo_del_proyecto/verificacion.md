# Verificación del archivo

Hecha el 15.11.2026 con `herramientas/verificar_archivo.py`, sobre el commit `3d57d31` de la rama del artículo. Se rehace con la misma orden, desde la raíz del repositorio.

**Resultado: todas las comprobaciones pasan.**

| Qué se comprobó | Cuántos | Resultado |
|---|---|---|
| Los identificadores del inventario no se repiten | 1259 | bien |
| Cada estado es uno de los siete previstos, o está vacío | 1259 | bien |
| Cada archivo copiado existe y su SHA-256, su tamaño y su identificador de git son los del inventario | 824 | bien |
| Cada registro sacado de git coincide con el contenido de su ruta en su commit | 915 | bien |
| Cada archivo vigente de la rama (commit 3d57d31) tiene su registro y está en su lugar sin cambios | 207 | bien |
| Cada contenido que tuvo cada ruta en la historia de la rama está en el inventario | 637 | bien |
| Cada duplicado que no se copia apunta a un archivo con el mismo contenido | 26 | bien |
| Cada archivo de versiones/ está en el inventario, o es una ficha o un índice | 1035 | bien |
| Cada carpeta de versión tiene su ficha | 200 | bien |
| Cada versión que nombra el inventario tiene su carpeta | 66 | bien |
| Los enlaces de la guía, los índices y las fichas llevan a un archivo que existe | 2722 | bien |
| Las imágenes que piden las páginas archivadas están a su lado (6 rutas ya no existían en su commit: pendientes.md) | 310 | bien |
| Fuera de archivo_del_proyecto/, la carpeta de trabajo no tiene cambios respecto de la rama | 1 | bien |
| Ningún texto del archivo trae el enlace de la carpeta privada del autor ni un correo suyo que no esté ya en el artículo | 1 | bien |

## El inventario, en números

| Prefijo | Registros | Copiados | Peso copiado |
|---|---|---|---|
| `V-` | 207 | 0 | 0,0 MB |
| `H-` | 430 | 416 | 175,7 MB |
| `D-` | 304 | 304 | 74,8 MB |
| `C-` | 114 | 104 | 24,4 MB |
| `R-` | 181 | 0 | 0,0 MB |
| `L-` | 11 | 0 | 0,0 MB |
| `N-` | 12 | 0 | 0,0 MB |

## Lo que esta verificación no cubre

- **Las piezas de la conversación** (`C-`) se comprueban contra `herramientas/conversacion.json`, que guarda su tamaño y su SHA-256 del día en que se copiaron. Su origen era la carpeta de trabajo de la sesión, que no se conserva.
- **Los canales de Are.na** (`L-`) y **la carpeta de fuentes del autor** no se abrieron: el archivo solo registra lo que dicen de ellos los documentos del proyecto.
- **Que cada Word o PDF anterior se abra bien** no se probó uno por uno: son copias exactas de lo que estaba en git.
- **Los enlaces dentro de los documentos archivados** que llevan a otros documentos (no a imágenes) apuntan a rutas del proyecto, y en una carpeta de versión pueden no resolverse. El documento vigente o la versión del mismo commit están en el inventario.
