# Figuras del artículo

El artículo todavía no lleva figuras: la exploración gráfica está en curso. Cuando termines dos o tres pasteles **con su registro escrito**, guárdalos aquí como `figura_1.jpg`, `figura_2.jpg`… (de 2.000 a 3.000 px de lado mayor).

Para insertar cada uno en `../articulo_altiplano.md`, junto al párrafo «Para el dibujo, el pasaje ofrece…» de su escena:

```markdown
::: {custom-style="Figura"}
![](figuras/figura_1.jpg){width=14cm}
:::

::: {custom-style="Pie de figura"}
**Figura 1.** Título de trabajo. Nombre, pastel al óleo sobre papel, 29,7 × 42 cm, 2026. Escena: … Operación: … Imagen especulativa: … Fuente: elaboración propia.
:::
```

Usa `{height=18cm}` en las figuras verticales. Menciona cada figura en el texto y regenera el Word con `python3 articulo/generar_docx.py`.

Instrucciones completas, modelo de pie y registro: `../../analisis/05_guia_de_dibujo.md`, §§5.4, 5.7 y 5.8.
