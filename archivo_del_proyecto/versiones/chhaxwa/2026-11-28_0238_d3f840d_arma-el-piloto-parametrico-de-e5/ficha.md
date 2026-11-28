# Chhaxwa. Cinco pruebas de construcción · 2026-11-28 02:38 UTC

**Arma el piloto paramétrico de E5 y compara las hiladas voladas con la bóveda verdadera**

| | |
|---|---|
| Línea | [Chhaxwa. Cinco pruebas de construcción](../README.md) |
| Origen | commit `d3f840d` de la rama `claude/altiplano-botelho-article-jm2nlr` |
| Fecha | 2026-11-28 02:38 UTC: la del commit, no la de creación de lo que contiene |
| Estado de la versión | versión anterior |
| Lo vigente | [`chhaxwa/`](../../../../chhaxwa/) |
| La versión anterior | [2026-11-28_0152_badd9c7_rehace-sin-figuras-humanas-los](../2026-11-28_0152_badd9c7_rehace-sin-figuras-humanas-los/ficha.md) |
| La versión siguiente | [2026-11-28_0300_216bcd0_anota-que-e5-sigue-volando](../2026-11-28_0300_216bcd0_anota-que-e5-sigue-volando/ficha.md) |

## Qué contiene esta carpeta

- **6 archivos de esta versión que ya no son los vigentes,** con su ruta original: [`chhaxwa/LEEME.md`](chhaxwa/LEEME.md), [`chhaxwa/detalles/dibujar_detalles.py`](chhaxwa/detalles/dibujar_detalles.py), [`chhaxwa/documento/chhaxwa.pdf`](chhaxwa/documento/chhaxwa.pdf), [`chhaxwa/documento/chhaxwa.typ`](chhaxwa/documento/chhaxwa.typ), [`chhaxwa/exploraciones.md`](chhaxwa/exploraciones.md), [`chhaxwa/parametrico/LEEME.md`](chhaxwa/parametrico/LEEME.md).
- **14 que siguen vigentes en su lugar,** sin cambios desde este commit: [`chhaxwa/parametrico/boveda_e5.py`](../../../../chhaxwa/parametrico/boveda_e5.py), [`chhaxwa/parametrico/boveda_e5_nodos.py`](../../../../chhaxwa/parametrico/boveda_e5_nodos.py), [`chhaxwa/parametrico/boveda_e5_verdadera.py`](../../../../chhaxwa/parametrico/boveda_e5_verdadera.py), [`chhaxwa/parametrico/e5_campo.png`](../../../../chhaxwa/parametrico/e5_campo.png), [`chhaxwa/parametrico/e5_elegidas.dxf`](../../../../chhaxwa/parametrico/e5_elegidas.dxf), [`chhaxwa/parametrico/e5_elegidas.png`](../../../../chhaxwa/parametrico/e5_elegidas.png), [`chhaxwa/parametrico/e5_matriz.dxf`](../../../../chhaxwa/parametrico/e5_matriz.dxf), [`chhaxwa/parametrico/e5_matriz.png`](../../../../chhaxwa/parametrico/e5_matriz.png), [`chhaxwa/parametrico/e5_nodos.jpg`](../../../../chhaxwa/parametrico/e5_nodos.jpg), [`chhaxwa/parametrico/e5_parametrica.blend`](../../../../chhaxwa/parametrico/e5_parametrica.blend), [`chhaxwa/parametrico/e5_variantes.csv`](../../../../chhaxwa/parametrico/e5_variantes.csv), [`chhaxwa/parametrico/e5_variantes_verdaderas.csv`](../../../../chhaxwa/parametrico/e5_variantes_verdaderas.csv), [`chhaxwa/parametrico/e5_verdaderas.dxf`](../../../../chhaxwa/parametrico/e5_verdaderas.dxf), [`chhaxwa/parametrico/e5_verdaderas.png`](../../../../chhaxwa/parametrico/e5_verdaderas.png).

## La versión completa

En este commit, la línea tenía 111 archivos: 6 están en esta carpeta, 20 en carpetas de otras versiones y 85 siguen vigentes en su lugar. Para ver cuáles, filtra `inventario.csv` por la columna `en_versiones` con `d3f840d`. Para tenerla entera: `git worktree add ../altiplano_d3f840d d3f840d`.

## Qué cambió respecto de la anterior

- **Añadidos (15):** `chhaxwa/parametrico/LEEME.md`, `chhaxwa/parametrico/boveda_e5.py`, `chhaxwa/parametrico/boveda_e5_nodos.py`, `chhaxwa/parametrico/boveda_e5_verdadera.py`, `chhaxwa/parametrico/e5_campo.png`, `chhaxwa/parametrico/e5_elegidas.dxf`, `chhaxwa/parametrico/e5_elegidas.png`, `chhaxwa/parametrico/e5_matriz.dxf`, `chhaxwa/parametrico/e5_matriz.png`, `chhaxwa/parametrico/e5_nodos.jpg`, `chhaxwa/parametrico/e5_parametrica.blend`, `chhaxwa/parametrico/e5_variantes.csv`, `chhaxwa/parametrico/e5_variantes_verdaderas.csv`, `chhaxwa/parametrico/e5_verdaderas.dxf`, `chhaxwa/parametrico/e5_verdaderas.png`.
- **Modificados (5):** `chhaxwa/LEEME.md`, `chhaxwa/detalles/dibujar_detalles.py`, `chhaxwa/documento/chhaxwa.pdf`, `chhaxwa/documento/chhaxwa.typ`, `chhaxwa/exploraciones.md`.

## Lo que lo respalda

El mensaje del commit `d3f840d`:

> Arma el piloto paramétrico de E5 y compara las hiladas voladas con la bóveda verdadera
>
> A pedido del autor, la bóveda de E5 se vuelve una función de sus reglas de
> construcción, en chhaxwa/parametrico/:
>
> - boveda_e5.py barre 825 variantes de hiladas voladas (arranque, vuelo de la
>   primera y de la última hilada) y revisa tres reglas: la clave bajo 2 m (p. 30),
>   el relleno sobre las colas con 30 cm de parapeto y una rendija que cierre una
>   laja. Como el vuelo del adobe lo mide la prueba 3, prueba tres escenarios: 12 cm,
>   un tercio (13,3 cm) y 15 cm. Con un tercio, la mejor es la E5 actual; con 15 cm,
>   la bóveda arranca a 60 cm y gasta 112 adobes menos.
> - boveda_e5_verdadera.py responde a la pregunta del autor por una bóveda
>   convencional y a su foto de un arco de adobe de dovelas: 258 bóvedas de medio
>   punto, catenarias y rebajadas, con anillos de 10, 20 o 40 cm, que se sostienen si
>   su línea de presiones cabe en el anillo y la resultante cae en la base del muro.
>   Cumplen 145; con dovelas de canto dejan de 0,93 a 1,20 m de pie, contra 0,43.
>   Cuenta plana con pesos supuestos.
> - boveda_e5_nodos.py arma la misma bóveda en Geometry Nodes, con controles y un
>   interruptor, comprueba que da lo mismo que el cálculo y guarda el .blend y un
>   render. Las hiladas usan ahora la misma regla de empate en los dos lados.
>
> Salen un gráfico, tres láminas en DXF (P2 a P4) y el render, que entran al
> documento como serie P (34 páginas). dibujar_detalles.py acepta carpeta,
> materiales y pie de cajetín, sin cambiar las láminas de detalle. E5 sigue con
> hiladas voladas hasta que el autor decida. Registro en analisis/43 §17.

El registro del proyecto que ese commit escribió o puso al día: [`analisis/43_chhaxwa.md`](../../../../analisis/43_chhaxwa.md).
