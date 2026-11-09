# Verificación del archivo

Se corrió el 2026-11-09 22:57 UTC sobre el commit `a3036cf` (con lo que hubiera sin commit), con `herramientas/verificar_archivo.py` y el registro de la conversación.

**Resultado: todo correcto.**

| Comprobación | Resultado | Detalle |
|---|---|---|
| Números únicos en el inventario | correcto | 1834 filas |
| Las copias están y tienen el contenido del inventario | correcto | 1147 archivos: SHA-256, tamaño y hash de git |
| Cada copia de git es la de su ruta en su commit | correcto | 1629 archivos: git cat-file <commit>:<ruta> da el mismo blob |
| Lo vigente está en su lugar, sin cambios | correcto | 642 archivos iguales a a3036cf |
| Lo que está en línea es lo que sirvió claude.ai | correcto | 3 de 4 con el SHA-256 informado al descargarlas; la página v4 sale del registro de la conversación (L-001); de las últimas publicaciones se guarda la fuente que se publicó, sin el envoltorio de la plataforma (L-003, L-006) |
| Lo de la conversación es lo que quedó en su registro | correcto | 85 copias encontradas en el registro |
| Los originales siguen intactos | correcto | fuera de tipografia/archivo_del_proyecto/, nada difiere de a3036cf |
| Todo lo del archivo está en el inventario | correcto | 1147 copias registradas |
| Los enlaces internos funcionan | correcto | 1041 enlaces de los documentos del archivo y 233 imágenes que muestran los Markdown archivados. Además, 9 enlaces comunes de documentos archivados apuntan al proyecto de entonces, fuera de su carpeta: se abren con git (ver README). |
| Lo ausente y las dudas están en pendientes.md | correcto | 35 registros N- |
| Las relaciones nombran filas que existen | correcto |  |
| Sin direcciones de correo ni colas de commit en lo que escribe el archivo | correcto | 136 documentos del archivo y 61 copias de la conversación y en línea |

[Volver al índice](README.md).
