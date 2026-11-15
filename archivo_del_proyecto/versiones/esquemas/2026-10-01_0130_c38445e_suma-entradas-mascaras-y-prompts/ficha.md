# Los esquemas, las notaciones y las guías · 2026-10-01 01:30 UTC

**Suma entradas, máscaras y prompts para mejorar las figuras 7 y 8**

| | |
|---|---|
| Línea | [Los esquemas, las notaciones y las guías](../README.md) |
| Origen | commit `c38445e` de la rama `claude/altiplano-botelho-article-jm2nlr` |
| Fecha | 2026-10-01 01:30 UTC: la del commit, no la de creación de lo que contiene |
| Estado de la versión | versión anterior |
| Lo vigente | [`analisis/esquemas/`](../../../../analisis/esquemas/) |
| La versión anterior | [2026-10-01_0033_b557ff6_rehace-las-figuras-7-y-8-como](../2026-10-01_0033_b557ff6_rehace-las-figuras-7-y-8-como/ficha.md) |
| La versión siguiente | [2026-10-01_0445_ea19cd0_rehace-las-figuras-1-a-6-como](../2026-10-01_0445_ea19cd0_rehace-las-figuras-1-a-6-como/ficha.md) |

## Qué contiene esta carpeta

- **1 archivo de esta versión que ya no es el vigente,** con su ruta original: [`analisis/esquemas/diagramas/generar_diagramas.js`](analisis/esquemas/diagramas/generar_diagramas.js).
- **15 que siguen vigentes en su lugar,** sin cambios desde este commit: [`analisis/esquemas/guias/entrada_fig7_memoria_retorno.png`](../../../../analisis/esquemas/guias/entrada_fig7_memoria_retorno.png), [`analisis/esquemas/guias/entrada_fig7_memoria_retorno.svg`](../../../../analisis/esquemas/guias/entrada_fig7_memoria_retorno.svg), [`analisis/esquemas/guias/entrada_fig8_tres_montones.png`](../../../../analisis/esquemas/guias/entrada_fig8_tres_montones.png), [`analisis/esquemas/guias/entrada_fig8_tres_montones.svg`](../../../../analisis/esquemas/guias/entrada_fig8_tres_montones.svg), [`analisis/esquemas/guias/generar_guias.py`](../../../../analisis/esquemas/guias/generar_guias.py), [`analisis/esquemas/guias/mascara_fig7_atalaya.png`](../../../../analisis/esquemas/guias/mascara_fig7_atalaya.png), [`analisis/esquemas/guias/mascara_fig7_foso.png`](../../../../analisis/esquemas/guias/mascara_fig7_foso.png), [`analisis/esquemas/guias/mascara_fig7_horizonte.png`](../../../../analisis/esquemas/guias/mascara_fig7_horizonte.png), [`analisis/esquemas/guias/mascara_fig7_muralla.png`](../../../../analisis/esquemas/guias/mascara_fig7_muralla.png), [`analisis/esquemas/guias/mascara_fig7_rotulos.png`](../../../../analisis/esquemas/guias/mascara_fig7_rotulos.png), [`analisis/esquemas/guias/mascara_fig8_castillete.png`](../../../../analisis/esquemas/guias/mascara_fig8_castillete.png), [`analisis/esquemas/guias/mascara_fig8_montones.png`](../../../../analisis/esquemas/guias/mascara_fig8_montones.png), [`analisis/esquemas/guias/mascara_fig8_rotulos.png`](../../../../analisis/esquemas/guias/mascara_fig8_rotulos.png), [`analisis/esquemas/guias/zonas_fig7.png`](../../../../analisis/esquemas/guias/zonas_fig7.png), [`analisis/esquemas/guias/zonas_fig8.png`](../../../../analisis/esquemas/guias/zonas_fig8.png).

## La versión completa

En este commit, la línea tenía 50 archivos: 1 están en esta carpeta, 0 en carpetas de otras versiones y 49 siguen vigentes en su lugar. Para ver cuáles, filtra `inventario.csv` por la columna `en_versiones` con `c38445e`. Para tenerla entera: `git worktree add ../altiplano_c38445e c38445e`.

## Qué cambió respecto de la anterior

- **Añadidos (14):** `analisis/esquemas/guias/entrada_fig7_memoria_retorno.png`, `analisis/esquemas/guias/entrada_fig7_memoria_retorno.svg`, `analisis/esquemas/guias/entrada_fig8_tres_montones.png`, `analisis/esquemas/guias/entrada_fig8_tres_montones.svg`, `analisis/esquemas/guias/mascara_fig7_atalaya.png`, `analisis/esquemas/guias/mascara_fig7_foso.png`, `analisis/esquemas/guias/mascara_fig7_horizonte.png`, `analisis/esquemas/guias/mascara_fig7_muralla.png`, `analisis/esquemas/guias/mascara_fig7_rotulos.png`, `analisis/esquemas/guias/mascara_fig8_castillete.png`, `analisis/esquemas/guias/mascara_fig8_montones.png`, `analisis/esquemas/guias/mascara_fig8_rotulos.png`, `analisis/esquemas/guias/zonas_fig7.png`, `analisis/esquemas/guias/zonas_fig8.png`.
- **Modificados (2):** `analisis/esquemas/diagramas/generar_diagramas.js`, `analisis/esquemas/guias/generar_guias.py`.

## Lo que lo respalda

El mensaje del commit `c38445e`:

> Suma entradas, máscaras y prompts para mejorar las figuras 7 y 8
>
> - generar_diagramas.js escribe también cada notación con sus rótulos en
>   los tamaños de GPT Image 2 (entrada_*); las figuras y las guías no
>   cambian.
> - generar_guias.py las pasa a PNG y hace las máscaras: una que conserva
>   los rótulos (diferencia entre entrada y guía) y una por zona (muralla,
>   foso, horizonte, atalaya; montones, castillete), más un mapa de zonas.
> - analisis/22: bloque de mejora, tres maneras (toda la hoja, todo menos
>   los rótulos, zona por zona), cuatro variantes, qué mirar y cuidados.
> - 21, README y LEEME al día.

El registro del proyecto que ese commit escribió o puso al día: [`analisis/21_diagramas_como_notaciones.md`](../../../../analisis/21_diagramas_como_notaciones.md), [`analisis/22_prompts_para_mejorar_las_notaciones.md`](../../../../analisis/22_prompts_para_mejorar_las_notaciones.md).
