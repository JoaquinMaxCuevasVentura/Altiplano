# El índice y las reglas del repositorio · 2026-11-28 02:38 UTC

**Arma el piloto paramétrico de E5 y compara las hiladas voladas con la bóveda verdadera**

| | |
|---|---|
| Línea | [El índice y las reglas del repositorio](../README.md) |
| Origen | commit `d3f840d` de la rama `claude/altiplano-botelho-article-jm2nlr` |
| Fecha | 2026-11-28 02:38 UTC: la del commit, no la de creación de lo que contiene |
| Estado de la versión | versión anterior |
| Lo vigente | [`README.md y AGENTS.md`](../../../../) |
| La versión anterior | [2026-11-28_0120_261e6d3_dibuja-las-seis-laminas-de](../2026-11-28_0120_261e6d3_dibuja-las-seis-laminas-de/ficha.md) |
| La versión siguiente | [2026-11-28_1415_a0af7fe_lleva-el-piloto-parametrico-a-e1](../2026-11-28_1415_a0af7fe_lleva-el-piloto-parametrico-a-e1/ficha.md) |

## Qué contiene esta carpeta

- **2 archivos de esta versión que ya no son los vigentes,** con su ruta original: [`AGENTS.md`](AGENTS.md), [`README.md`](README.md).

## La versión completa

En este commit, la línea tenía 2 archivos: 2 están en esta carpeta, 0 en carpetas de otras versiones y 0 siguen vigentes en su lugar. Para ver cuáles, filtra `inventario.csv` por la columna `en_versiones` con `d3f840d`. Para tenerla entera: `git worktree add ../altiplano_d3f840d d3f840d`.

## Qué cambió respecto de la anterior

- **Modificados (2):** `AGENTS.md`, `README.md`.

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
