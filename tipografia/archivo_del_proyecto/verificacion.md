# Verificación del archivo

Se corrió el 2026-11-12 17:21 UTC sobre el commit `8d8fc7b` (con lo que hubiera sin commit), con `herramientas/verificar_archivo.py` y el registro de la conversación.

**Resultado: todo correcto.**

| Comprobación | Resultado | Detalle |
|---|---|---|
| Números únicos en el inventario | correcto | 2010 filas |
| Las copias están y tienen el contenido del inventario | correcto | 1318 archivos: SHA-256, tamaño y hash de git |
| Cada copia de git es la de su ruta en su commit | correcto | 1802 archivos: git cat-file <commit>:<ruta> da el mismo blob |
| Lo vigente está en su lugar, sin cambios | correcto | 646 archivos iguales a 8d8fc7b |
| Lo que está en línea es lo que sirvió claude.ai | correcto | 3 de 4 con el SHA-256 informado al descargarlas; la página v4 sale del registro de la conversación (L-001); de las últimas publicaciones se guarda la fuente que se publicó, sin el envoltorio de la plataforma (L-003, L-004, L-007, L-008) |
| Lo de la conversación es lo que quedó en su registro | correcto | 85 copias encontradas en el registro |
| Los originales siguen intactos | correcto | fuera de tipografia/archivo_del_proyecto/, nada difiere de 8d8fc7b |
| Todo lo del archivo está en el inventario | correcto | 1318 copias registradas |
| Los enlaces internos funcionan | correcto | 1122 enlaces de los documentos del archivo y 258 imágenes que muestran los Markdown archivados. Además, 15 enlaces comunes de documentos archivados apuntan al proyecto de entonces, fuera de su carpeta: se abren con git (ver README). |
| Lo ausente y las dudas están en pendientes.md | correcto | 35 registros N- |
| Las relaciones nombran filas que existen | correcto |  |
| Sin direcciones de correo ni colas de commit en lo que escribe el archivo | correcto | 148 documentos del archivo y 61 copias de la conversación y en línea |

[Volver al índice](README.md).
