from pathlib import Path
p=Path('/tmp/dintel-claro/modelar.py')
src=p.read_text()
def replace(a,b):
    global src
    assert a in src, a[:90]
    src=src.replace(a,b,1)
replace('import math\n','import math\nimport random\n')
replace("scene = bpy.data.scenes.new('D · El claro de la piedra')","scene = bpy.data.scenes.new('D · El claro de la pirca')")
replace("scene['decision'] = 'Conservar un paso bajo, abrir la planta al final y dejar una piedra fuera del eje.'", """scene['decision'] = 'Paso estrecho y cubierto. Claro lateral rebajado. Dos caras de piedra y relleno visible al final.'
scene['fuentes'] = 'Cosecha de piedras, §7, Altiplano pp. 155–157 y 8. Figura 7. Análisis 11, B. Las referencias visuales orientan la representación material.'""")
replace("mapped = center + normal*(y-source_y)","""face_shift = .33*blendstep(5.60,6.30,x) if side == 'norte' else 0.
        mapped = center + normal*(y-source_y+face_shift)""")
replace('walls = [move_wall(\'sur\',.925), move_wall(\'norte\',3.565)]',"""walls = [move_wall('sur',.925), move_wall('norte',3.565)]
rng = random.Random(2241)

def additional_stones(name, rows, seed):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([entry[0] for entry in rows],[],[])
    for i,attr in ((1,'medidas'),(2,'giro')):
        layer = mesh.attributes.new(attr,'FLOAT_VECTOR','POINT')
        layer.data.foreach_set('vector',[v for entry in rows for v in entry[i]])
    mesh.update()
    obj = bpy.data.objects.new(name,mesh)
    scene.collection.objects.link(obj)
    mod = obj.modifiers.new('Montaje por Geometry Nodes','NODES')
    mod.node_group = walls[0].modifiers[0].node_group
    seed_socket = next(s for s in mod.node_group.interface.items_tree if s.name == 'Semilla')
    mod[seed_socket.identifier] = seed
    return obj

def shifted(x,y,z):
    center, tangent, normal = frame('norte',x)
    p = center+normal*y
    return (*p,z),math.atan2(tangent.y,tangent.x)

inner = []
heights = [0,.22,.438,.632,.84,1.047,1.206]
for layer,(low,high) in enumerate(zip(heights,heights[1:])):
    a = 5.58+rng.uniform(-.08,.09)
    end = 8.15-rng.uniform(-.015,.09)-.045*layer
    while a < end-.08:
        length = min(rng.uniform(.23,.43),end-a)
        x = a+length/2
        y = -.32*blendstep(5.32,6.20,x)+rng.uniform(-.022,.033)
        p, spin = shifted(x,y,(low+high)/2+rng.uniform(-.016,.016))
        inner.append((p,(length*1.04,rng.uniform(.33,.37),(high-low)*rng.uniform(1.01,1.15)),
                      (rng.uniform(-.09,.09),rng.uniform(-.06,.06),spin+rng.uniform(-.14,.14))))
        a += length
additional_stones('D · Pirca norte · cara interior escalonada',inner,1523)
core = []
for row in range(8):
    x = 6.15+rng.uniform(-.07,.04)
    tip = 8.53-.046*row+rng.uniform(-.06,.05)
    while x < tip:
        for lane in (-.11,.038,.15):
            p, spin = shifted(x+rng.uniform(-.077,.077),lane+rng.uniform(-.044,.033),
                              .056+row*.132+rng.uniform(-.022,.019))
            core.append((p,(rng.uniform(.14,.237),rng.uniform(.14,.22),rng.uniform(.13,.175)),
                         (rng.uniform(-.22,.22),rng.uniform(-.24,.24),spin+rng.uniform(-.50,.50))))
        x+=rng.uniform(.145,.188)
additional_stones('D · Piedra menuda · relleno de la pirca a la vista',core,6231)
""")
replace("""stone_x, stone_y = 6.91,3.28
line_a = Vector((5.81,1.02))
line_b = Vector((6.66,2.94))
line_delta = line_b-line_a
def ground_z(x,y):
    recessed = math.exp(-(((x-stone_x)/.78)**2+((y-stone_y)/.96)**2))
    point = Vector((x,y))
    s = min(1.,max(0.,(point-line_a).dot(line_delta)/line_delta.length_squared))
    foot = line_a+line_delta*s
    groove = -.027*math.exp(-((point-foot).length/.045)**2)*math.sin(math.pi*s)**.32
    return -.014-.143*recessed + .017*noise.noise(Vector((x*1.65,y*1.65,1.7))) + groove""",
"""def ground_z(x,y):
    recessed = math.exp(-(((x-7.18)/1.04)**2+((y-2.64)/.53)**2))
    return -.014-.128*recessed + .017*noise.noise(Vector((x*1.65,y*1.65,1.7)))""")
replace("'D · Suelo excavado y surco discontinuo'", "'D · Rebaje seco del claro'")
start=src.index("library = bpy.data.collections['Biblioteca · 12 formas de piedra']")
end=src.index("cloth = simple",start)
src=src[:start]+src[end:]
replace("hood['operacion'] = 'Cubrir el tramo estrecho y recortar el borde sobre el claro.'",
"""hood['operacion'] = 'El paño cubre el tramo del dintel. Se retira sobre el extremo de la pirca para hacer visible la sección.'""")
replace("center = centerline(side,x)\n        tube(f'D · Montante",
"""center, _, normal = frame(side,x)
        if side == 'norte':
            center += normal*(.33*blendstep(5.60,6.30,x))
        tube(f'D · Montante""")
replace("inside_camera = camera('D · Desde el umbral',(1.09,2.09,1.41),(7.62,2.97,.97),23)",
"""inside_camera = camera('D · Hacia el relleno expuesto',(10.60,.54,2.23),(7.50,3.68,.76),42)
camera('D · Desde el umbral',(1.09,2.09,1.41),(7.62,2.97,.97),23)""")
replace("'//D_El_claro_de_la_piedra.png'", "'//D_El_claro_de_la_pirca.png'")
replace("""notes.write(\"\"\"EL CLARO DE LA PIEDRA · Variante de El dintel de Jatun-Kolla

Maquetas de Joaquin Cuevas. El recinto curvo aporta la relación entre masa, pieza suelta y luz. Las maquetas de estratos y cavidades aportan la idea de un suelo rebajado y de un trazo ligero. El volumen con ranuras convierte la abertura en una operación del espacio. La membrana tensada aporta la relación de peso entre la piedra y una cubierta delgada.

Altiplano, edición de 1982, pp. 155–156. El retorno se cuenta como detenerse en el dintel, tocar el suelo y recomponer las pircas. En la variante D el trazado se abre al final. Una pirca curva delimita un claro de tierra rebajada. El borde recortado del paño deja a la piedra testigo fuera de la sombra. La pieza se coloca fuera del eje y se puede rodear.

El archivo contiene los estudios A, B, C y D. Las pircas y la grava de D se instancian con el grupo de Geometry Nodes del proyecto. Las costillas, los tensores y la membrana se pueden editar por separado. Las cámaras Maqueta abierta y Desde el umbral muestran dos lecturas de la misma geometría. La luminotecnia corresponde a una maqueta digital de estudio.
\"\"\")""",
"""notes.write(\"\"\"EL CLARO DE LA PIRCA · Variante de El dintel de Jatun-Kolla

FUENTE Y DECISIÓN

1. Dintel y pausa. Cosecha de piedras, sección 7. En Altiplano (edición de 1982, p. 155), la gente se detiene y se arrodilla al regresar. El proyecto interpreta esa pausa con un paso angosto y bajo que se abre a un lado. Curvatura, cotas y tela son decisiones de proyecto.

2. La pirca que se recompone. Altiplano, pp. 8 y 156, y el análisis 11, apartado B. La obra repone el lindero. El artículo lee las piedras menudas que sostienen el muro como figura de quienes quedan fuera del relato del retorno. El proyecto deja al descubierto la sección de una pirca de doble cara: las piedras grandes delimitan y el relleno pequeño permanece visible. La doble cara es una técnica tomada por el artículo para su analogía, no una descripción de las pircas de Jatun-Kolla en la novela.

3. El foso de la memoria. Altiplano, pp. 156–157, y la Figura 7. El artículo lee el contraste entre mirar el horizonte y el hambre que queda debajo. Un rebaje lateral, seco y somero, orienta aquí la mirada hacia el suelo y el relleno. El texto narra una imagen de la memoria. El corte del suelo es una traducción espacial.

LAS MAQUETAS DE REFERENCIA

El recinto curvo ayuda a ensayar la apertura en planta. Las cavidades y los cantos estratificados ayudan a dibujar una sección legible. Las ranuras y el borde recortado ayudan a dirigir la luz. La membrana aporta una forma ligera de representar el gesto de volver a cubrir. El remate descubierto deja ver la sección de la pirca.

El archivo contiene los estudios A, B, C y D, con la variante D activa. Las caras de la pirca, el relleno y la grava tienen objetos y grupos de Geometry Nodes editables. La membrana, las costillas y los tirantes quedan separados. Las cámaras Maqueta abierta, Hacia el relleno expuesto, Desde el umbral y Planta muestran el mismo modelo. La luminotecnia corresponde a una maqueta digital de estudio.
\"\"\")""")
replace("[(main_camera,'D_El_claro_de_la_piedra.png'),(inside_camera,'D_Desde_el_umbral.png')]",
        "[(main_camera,'D_El_claro_de_la_pirca.png'),(inside_camera,'D_Relleno_de_la_pirca.png')]")
Path('/tmp/dintel-claro/el_claro_fuentes.py').write_text(src)
