# La gramática en el navegador

Una página para intervenir la gramática paramétrica de Contenida (`../03c_gramatica.md`) y ver sus efectos. Cuando mueves un parámetro, los 55 signos se vuelven a armar. Cada signo puede pasar por los seis estados simulados.

Como el resto de la simulación, es la propuesta de la máquina: **no entra en la caja ni en la fuente.**

## Dónde se abre

- **En línea:** el artefacto de Claude [«Gramática de Contenida»](https://claude.ai/artifact/MD4hC81MMftYgHHB1RT9bL) (privado; se comparte desde su menú). Guarda versiones de los parámetros, y Claude puede leerlas para correr la simulación en Python.
- **En tu computadora:** sirve esta carpeta y abre la página. Necesita conexión para la biblioteca de polígonos (clipper-lib, de cdn.jsdelivr.net) y las fuentes. Sin el artefacto no hay versiones guardadas: se usa el JSON.

  ```bash
  cd tipografia/aplicacion && python3 -m http.server 8000
  # y abre http://localhost:8000
  ```

## Qué tiene

| Vista | Qué muestra |
|---|---|
| **Caja** | La caja de 8 × 7 con los 55 cuerpos base: en tinta lo hallado, en violeta lo reconstruido. Opcionalmente, las líneas de la piscina y el testigo del pie |
| **Signo** | Un signo con sus partes: el testigo, el cuerpo, los ejes con sus nodos, los alivios, las gotas y los asientos. También la receta, de dónde sale en el pie y sus medidas en milímetros. Se copia o se descarga en SVG |
| **Texto** | Un verso, o cualquier texto, compuesto celda por celda en caja baja. Lo que no está en la caja sale como celda vacía. *Sobre la piscina*, las juntas de los azulejos de 150 mm cortan las letras |
| **Estados** | Los seis simuladores sobre un signo: calco, placa (reverso y anverso), cinta (puesta y arrancada), frotado (se frota hasta que no se lee: el peso en frotadas), agua (quieta y tocada) y voz (ondas de Faraday con una sílaba del verso) |

**La ficha de parámetros** trae la altura de x (ascendente sobre x: 1,52 en el sustituto, 1,71 en la foto) y los 20 parámetros de `gramatica.py`. Cada uno lleva su valor en píxeles, milímetros y canales, qué controla, de dónde sale y cómo volver al valor de la obra.

## De la página a la simulación

1. Ajusta los parámetros.
2. Guarda una versión, o copia o descarga `parametros.json`. Solo cuentan los ajustados: el resto sigue saliendo del pie.
3. Corre:

   ```bash
   python3 tipografia/simulacion/gramatica.py --parametros parametros.json
   python3 tipografia/simulacion/simular.py --parametros parametros.json
   ```

`simular.py` escribe siempre en `simulacion/salida/` y en `informe.md`: con `--parametros`, las láminas y el informe pasan a ser los de esa versión, y el informe lo dice al principio. Para volver a la propuesta de la obra, se corre de nuevo sin `--parametros`.

La gramática de la página es la de `gramatica.py`, portada a JavaScript. Repite el azar de Python: los mismos quiebres de los fustes y los mismos desvíos de las comillas. Con los mismos ajustes, los 55 cuerpos de la página y los de Python coinciden hasta el píxel del borde.

Los simuladores de la página son los modelos de `desenterrar.py`, `contener.py`, `gramatica.py` (`encintar`) y `devolver.py`, con otro azar: la misma receta, otra mano. Sus números no reemplazan a los de `informe.md`.

## Archivos

| Archivo | Qué es |
|---|---|
| `index.html` | La página. Lo que va entre `<!-- contenido -->` y `<!-- /contenido -->` es lo que se publica como artefacto |
| `app.js` | La ficha, las cuatro vistas y las versiones |
| `gramatica.js` | La gramática: achatar el pie, medirlo, el esqueleto, los parámetros, el taller, las 55 recetas y el cuerpo (con clipper-lib) |
| `simuladores.js` | Calco, placa, cinta, frotado, agua y voz |
| `datos.js` | Generado: los 30 testigos ya escalados al azulejo, sus medidas, la razón de la foto, la caja, las recetas, los parámetros con su procedencia, el poema y el azar de cada receta |
| `exportar.py` | Regenera `datos.js`. Con `--prueba RUTA` escribe también los cuerpos de Python, para comparar |

Si cambia el pie o la gramática en Python:

```bash
python3 tipografia/aplicacion/exportar.py
```

Hecho con asistencia de IA.
