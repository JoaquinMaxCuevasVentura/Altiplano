# El índice y las reglas del repositorio · 2026-11-28 01:20 UTC

**Dibuja las seis láminas de detalle de Chhaxwa en DXF y quita las figuras humanas**

| | |
|---|---|
| Línea | [El índice y las reglas del repositorio](../README.md) |
| Origen | commit `261e6d3` de la rama `claude/altiplano-botelho-article-jm2nlr` |
| Fecha | 2026-11-28 01:20 UTC: la del commit, no la de creación de lo que contiene |
| Estado de la versión | versión vigente |
| Lo vigente | [`README.md y AGENTS.md`](../../../../) |
| La versión anterior | [2026-11-27_2056_b7027f7_pone-la-casa-redonda-como-e3-y](../2026-11-27_2056_b7027f7_pone-la-casa-redonda-como-e3-y/ficha.md) |

## Qué contiene esta carpeta

- **2 que siguen vigentes en su lugar,** sin cambios desde este commit: [`AGENTS.md`](../../../../AGENTS.md), [`README.md`](../../../../README.md).

## La versión completa

En este commit, la línea tenía 2 archivos: 0 están en esta carpeta, 0 en carpetas de otras versiones y 2 siguen vigentes en su lugar. Para ver cuáles, filtra `inventario.csv` por la columna `en_versiones` con `261e6d3`. Para tenerla entera: `git worktree add ../altiplano_261e6d3 261e6d3`.

## Qué cambió respecto de la anterior

- **Modificados (2):** `AGENTS.md`, `README.md`.

## Lo que lo respalda

El mensaje del commit `261e6d3`:

> Dibuja las seis láminas de detalle de Chhaxwa en DXF y quita las figuras humanas
>
> Las láminas de detalle, a pedido del autor, que propuso QCAD para dibujarlas.
> QCAD no se puede instalar en este entorno, así que chhaxwa/detalles/dibujar_detalles.py
> las dibuja con ezdxf en DXF, que QCAD abre y edita. Son seis A3 a una sola escala
> (E1 a 1:25, las demás a 1:20), en metros reales, con una vista en grises de cada una
> y un PDF con las seis.
>
> A mitad del trabajo el autor pidió dos cosas:
> - quitar las figuras humanas, que se veían mal: FIGURAS = False en blender/comun.py
>   las apaga en todos los modelos, y los pies y textos que las nombraban se corrigen;
> - cuidar los grosores: las capas siguen la jerarquía del dibujo de arquitectura
>   (lo cortado a 0,50 mm con juntas de 0,18; el suelo a 0,70; lo visto en gris a 0,18;
>   los sombreados en gris a 0,09; cotas y guías a 0,13).
>
> Las láminas resolvieron cosas que los modelos dejaban abiertas, marcadas como
> decisiones del proyecto en exploraciones.md, y mostraron tres medidas mal escritas:
> los palos de E2 miden 1,4 m (no 1,7), la rendija de la clave de E5 es de 43 cm (no 30)
> y el paso de E3 deja 84 cm libres al centro. El modelo y el diagrama de E2 se ajustan
> para que el anillo cargue los pares. El documento suma las láminas como serie L1-L6.
>
> Los renders sin figuras, el PDF del documento y el archivo del proyecto van en los
> commits siguientes, cuando terminen de rehacerse las imágenes. Registro en analisis/43 §16.

El registro del proyecto que ese commit escribió o puso al día: [`analisis/43_chhaxwa.md`](../../../../analisis/43_chhaxwa.md).
