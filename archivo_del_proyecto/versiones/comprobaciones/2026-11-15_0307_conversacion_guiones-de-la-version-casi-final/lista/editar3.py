"""Incorpora al artículo a Suárez Jordán (1990) y Yampara Blanco (2019): sección 3, conclusiones y bibliografía.
Uso: python3 editar3.py articulo.md"""
import sys
from pathlib import Path
p = Path(sys.argv[1]); s = p.read_text('utf8')
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70])
    s = s.replace(a, b)

# 1. La planta tipo de Suárez Jordán, después de Churata
rep("suele quedar fuera, junto a las parcelas (Churata, 2017: 123). Para Alexander, por último,",
    "suele quedar fuera, junto a las parcelas (Churata, 2017: 123). También la dibujó en planta la arquitecta Marina Suárez Jordán, "
    "que estudió la vivienda aymara del altiplano boliviano. Su casa rural tipo se compone de «volúmenes aislados alrededor de un espacio abierto», "
    "que son cuartos sueltos y sin «subdivisiones internas», y el mayor es la *ach'a uta* o casa grande, donde «se concentran las actividades domésticas» "
    "y que suele ser «la habitación de los padres» (Suárez Jordán, 1990: 130). La falta de cuartos que anota el narrador es, en este tipo de casa, "
    "su manera de tenerlos, porque las habitaciones son «partes separadas que conforman la unidad» (ibid.: 131). Suárez Jordán advertía que el resto de los "
    "bolivianos veía esa arquitectura «únicamente como síntomas del subdesarrollo» (ibid.: 128). Para Alexander, por último,")

# 2. Yampara Blanco, después del párrafo del fuego
rep("saca a la *chujlla* de la historia.\n",
    "saca a la *chujlla* de la historia.\n\n"
    "Hay estudios hechos desde más cerca. La arquitecta Pacha Yapucha Yampara Blanco midió quince casas del *ayllu* Jach'a Chambi, al sur del departamento de La Paz, "
    "en un trabajo que se hizo en aymara, «recuperando las palabras y los significados originales» (Yampara Blanco, 2019: 10). Allí la casa se llama *uta* y es doble, "
    "con una casa redonda y otra cuadrada que el patio articula. En la redonda, el fogón de arcilla que se enciende en la época de lluvia y de frío es "
    "«el punto de reunión donde se comparte en familia», y de noche la familia duerme ordenada por edades, «estando los padres en el centro». La cuadrada sirve sobre todo de "
    "«despensa y depósito de herramientas agrícolas, materiales de trabajo, alimentos y semillas» (ibid.: 13). El estudio es de 2019 y de otra comarca del altiplano, "
    "pero son usos que la novela reúne también en la *chujlla* de los Huanca, con sus braseros en medio y sus herramientas colgadas de las vigas. "
    "Yampara Blanco recoge, además, que en el quicio de la puerta se enterraba la placenta del recién nacido, «para que los hijos no se marcharan lejos de la casa» (ibid.). "
    "La novela no cuenta nada parecido, aunque deja a Paulo en ese lugar, el portal de su *chujlla*, cuando los hijos se van. Para esta autora la *uta* es "
    "«el nido de la red de familias» de los *ayllus* (ibid.: 12), y hoy muchas de esas casas «se encuentran abandonadas, deshabitadas y en proceso de desaparición» (ibid.: 9).\n")

# 3. El primer límite de las conclusiones
rep("«hace tiempo, hemos añorado por escribir» (Choque Canqui, 1978 [1974]: s. p.). Churata,",
    "«hace tiempo, hemos añorado por escribir» (Choque Canqui, 1978 [1974]: s. p.). Los estudios de Suárez Jordán (1990) y de Yampara Blanco (2019), "
    "que aquí sirven solo para la casa de los Huanca, son parte de esas fuentes. Churata,")

# 4. Bibliografía
rep("The Voidz (2018). *Virtue* [álbum].",
    "Suárez Jordán, Marina (1990). «Permanencia y cambio: el caso de la vivienda aymara en centros poblados del altiplano boliviano». "
    "*Ciudad y Territorio*, 85: 127-135. https://recyt.fecyt.es/index.php/CyTET/article/view/83696.\n\n"
    "The Voidz (2018). *Virtue* [álbum].")
rep("Zavaleta Mercado, René (1986).",
    "Yampara Blanco, Pacha Yapucha (2019). «La arquitectura de los pueblos milenarios del altiplano: una configuración femenina y masculina, Jaqi Andino». "
    "*Revista Nodo*, 14(27): 8-23. https://doi.org/10.54104/nodo.v14n27.170.\n\n"
    "Zavaleta Mercado, René (1986).")
p.write_text(s, 'utf8')
