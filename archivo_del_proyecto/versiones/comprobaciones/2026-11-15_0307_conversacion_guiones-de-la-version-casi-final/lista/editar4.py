"""Pasada de pulido para la versión casi final: quita los patrones de redacción que quedaban, sin tocar citas ni páginas.
Uso: python3 editar4.py articulo.md"""
import sys
from pathlib import Path
p = Path(sys.argv[1]); s = p.read_text('utf8')
n = 0
def rep(a, b):
    global s, n
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b); n += 1

# --- Abstract: dos puntos que «revelan»
rep("Our interest lies in what the novel records without its narrator noticing: the material way in which land is lost.",
    "Our interest lies in something the novel records without its narrator noticing, namely the material way in which land is lost.")

# --- §1
rep("En Jatun-Kolla la piedra todavía no es una ruina; es una posesión presente.",
    "En Jatun-Kolla la piedra sigue siendo una posesión presente y todavía no ha pasado a ruina.")

# --- §2
rep("Inventar, en ese sentido, quiere decir hacer, y no mentir.",
    "En ese sentido, inventar una palabra es hacerla, que es cosa distinta de mentir.")
rep("porque no aportan datos nuevos sobre la novela, aunque obligan a decidir lo que el texto deja abierto.",
    "porque no aportan datos nuevos sobre la novela, aunque piden decisiones que el texto no toma.")
rep("propone para explorar la imagen arquitectónica, que son la observación, la disección, el ensamblaje y la inmersión.",
    "propone para explorar la imagen arquitectónica: observación, disección, ensamblaje e inmersión.")
rep("las ordena según cuatro funciones constructivas, que son el apoyo, el vano, la masa y el límite (Cuadro 1).",
    "las ordena según cuatro funciones constructivas, el apoyo, el vano, la masa y el límite (Cuadro 1).")
rep("Fuão pone además una condición, que adoptamos.", "Fuão pone una condición, que adoptamos.")

# --- §3
rep("El narrador, por su parte, declara cerrada el alma de los comunarios,",
    "El narrador, en cambio, declara cerrada el alma de los comunarios,")
# el párrafo de los cuartos se parte en dos: las miradas de fuera y las de quienes conocían esas casas
rep(" Churata, que sí conocía esas casas, describió en 1939",
    " Para Alexander, además, todos los patrones de una casa caben superpuestos «en una simple cabaña de una sola habitación» (Alexander et al., 1977: xliii).\n\n"
    "Churata, que sí conocía esas casas, describió en 1939")
rep(" Para Alexander, por último, todos los patrones de una casa caben superpuestos «en una simple cabaña de una sola habitación» (Alexander et al., 1977: xliii). Leídas con estos autores,",
    " Leídas con estos autores,")
rep("Hay estudios hechos desde más cerca. La arquitecta Pacha Yapucha Yampara Blanco midió quince viviendas",
    "Más cerca todavía trabajó la arquitecta Pacha Yapucha Yampara Blanco, que midió quince viviendas")
rep("al sur del departamento de La Paz, en un trabajo que se hizo en aymara,", "al sur del departamento de La Paz, en un estudio hecho en aymara,")
rep("La hoja junta dos vistas, el cerro en corte, escalonado con capas de empaste, y el catastro en planta, rayado con un punzón sobre la cera.",
    "La hoja junta dos vistas, el cerro en corte, escalonado con capas de empaste, y el catastro, que es el plano de las parcelas, rayado en planta con un punzón sobre la cera.")

# --- §4
rep("Umacachi, la aldea, está hecha de ocupaciones sucesivas, que son un tambo incaico, una iglesia y un fuerte coloniales y, ya con la República,",
    "Umacachi, la aldea, está hecha de ocupaciones sucesivas. Hubo allí un tambo incaico, después una iglesia y un fuerte coloniales y, ya con la República,")
rep("El despojo, por otro lado, no tiene un solo villano.", "El despojo no tiene un solo villano.")
rep("Umacachi lo desmiente, porque es una aldea,", "Umacachi no encaja en esa explicación, porque es una aldea,")
rep("Entonces llega la letra: «Todos los animales de carneo que existen dentro del radio urbano serán requisados [...] (Fdo.) Dr. Margarito Mendoza» (ibid.: 96). La firma es la del lobo. El radio urbano",
    "Entonces llega la letra, con la firma del lobo: «Todos los animales de carneo que existen dentro del radio urbano serán requisados [...] (Fdo.) Dr. Margarito Mendoza» (ibid.: 96). El radio urbano")

# --- §7
rep("Los comunarios miran atrás, aunque lo hacen para saltar el foso y no para caminar, como quiere el lema, y por eso recuerdan las cosechas y no el hambre.",
    "Los comunarios miran atrás, pero saltándose el foso, y por eso recuerdan las cosechas y callan el hambre.")
rep("Todo recipiente, sin embargo, elige qué guarda, y el narrador cierra con héroes: los derrotados vuelven a ser",
    "Todo recipiente, sin embargo, elige qué guarda, y el narrador cierra con héroes, porque los derrotados vuelven a ser")

# --- §8
rep("vuelve paisaje una posesión que la novela, sin que él lo advierta, deja escrita en la piedra,",
    "vuelve paisaje una posesión que la novela, a pesar suyo, deja escrita en la piedra,")
rep("Los pasteles obligan a decidir lo que el texto deja abierto (desde dónde se mira, a qué escala, qué queda dentro y qué fuera),",
    "Para hacer un pastel hay que resolver lo que el texto no dice (desde dónde se mira, a qué escala, qué queda dentro y qué fuera),")
p.write_text(s, 'utf8'); print(n, 'cambios')
