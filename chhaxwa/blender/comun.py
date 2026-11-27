"""Biblioteca común de Chhaxwa para Blender (bpy 5.0).

Materiales procedurales, generadores de piedra, tierra, paja y madera, el estudio de fotografía de maquetas y el sol
de La Paz. La usan formas.py y renderizar.py. Todo está escrito con nodos y código: no hay texturas de terceros ni
imágenes hechas con IA.

Unidades: metros de la maqueta. Las maquetas de forma son a escala 1:20 (E = 0,05), así que 1 m real = 5 cm.
"""

import bmesh
import bpy
import datetime as dt
import math
import random
from mathutils import Vector, noise

E = 1 / 20                     # escala de las maquetas de forma

# ----------------------------------------------------------------------------------------------------------------
# El sol en La Paz (las mismas fórmulas de la NOAA que la tabla de la prueba 5)
# ----------------------------------------------------------------------------------------------------------------
LAT, LON, HUSO = -16.50, -68.15, -4


def sol(fecha, hora):
    """Altura y acimut del sol en grados. El acimut, desde el norte en el sentido del reloj."""
    n = fecha.timetuple().tm_yday
    g = 2 * math.pi / 365 * (n - 1 + (hora - 12) / 24)
    eot = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g) - 0.014615 * math.cos(2 * g)
                    - 0.040849 * math.sin(2 * g))
    d = (0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g) - 0.006758 * math.cos(2 * g)
         + 0.000907 * math.sin(2 * g) - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g))
    h = math.radians((hora * 60 + eot + 4 * LON - 60 * HUSO) / 4 - 180)
    f = math.radians(LAT)
    alt = math.asin(math.sin(f) * math.sin(d) + math.cos(f) * math.cos(d) * math.cos(h))
    az = math.degrees(math.atan2(math.sin(h), math.cos(h) * math.sin(f) - math.tan(d) * math.cos(f))) + 180
    return math.degrees(alt), az % 360


def vector_sol(fecha=dt.date(2026, 6, 21), hora=10.0):
    """Vector unitario hacia el sol, con +x al este, +y al norte y +z arriba."""
    alt, az = sol(fecha, hora)
    a, z = math.radians(alt), math.radians(az)
    return Vector((math.sin(z) * math.cos(a), math.cos(z) * math.cos(a), math.sin(a)))


# ----------------------------------------------------------------------------------------------------------------
# Escena
# ----------------------------------------------------------------------------------------------------------------

def escena_nueva():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = 'METRIC'
    return sc


def ligar(ob, coleccion=None):
    (coleccion or bpy.context.scene.collection).objects.link(ob)
    return ob


def objeto(nombre, malla, loc=(0, 0, 0), rot=(0, 0, 0), escala=(1, 1, 1)):
    ob = bpy.data.objects.new(nombre, malla)
    ob.location, ob.rotation_euler, ob.scale = loc, rot, escala
    return ligar(ob)


def malla_de_bm(bm, nombre, mat=None, suave=True):
    me = bpy.data.meshes.new(nombre)
    bm.to_mesh(me)
    bm.free()
    for f in me.polygons:
        f.use_smooth = suave
    if mat:
        me.materials.append(mat)
    return me


# ----------------------------------------------------------------------------------------------------------------
# Materiales procedurales
# ----------------------------------------------------------------------------------------------------------------

def _arbol(nombre):
    m = bpy.data.materials.new(nombre)
    m.use_nodes = True
    t = m.node_tree
    t.nodes.clear()
    return m, t.nodes, t.links


def _rampa(N, colores, posiciones=None):
    cr = N.new("ShaderNodeValToRGB")
    el = cr.color_ramp.elements
    posiciones = posiciones or [i / (len(colores) - 1) for i in range(len(colores))]
    while len(el) < len(colores):
        el.new(0.5)
    for e, c, p in zip(el, colores, posiciones):
        e.position, e.color = p, (*c, 1)
    return cr


def _ruido(N, L, vec, escala, detalle=6.0, rugosidad=0.5):
    n = N.new("ShaderNodeTexNoise")
    n.inputs["Scale"].default_value = escala
    n.inputs["Detail"].default_value = detalle
    n.inputs["Roughness"].default_value = rugosidad
    L.new(vec, n.inputs["Vector"])
    return n


def mat_piedra(nombre="piedra", claro=(0.30, 0.285, 0.26), oscuro=(0.085, 0.08, 0.075), escala_obj=1.0):
    """Piedra de campo del altiplano: gris pardo, con variación por piedra, poros, aristas y suciedad en las juntas."""
    m, N, L = _arbol(nombre)
    o = N.new("ShaderNodeOutputMaterial"); b = N.new("ShaderNodeBsdfPrincipled")
    tc = N.new("ShaderNodeTexCoord"); info = N.new("ShaderNodeObjectInfo")
    vec = N.new("ShaderNodeVectorMath"); vec.operation = 'SCALE'; vec.inputs["Scale"].default_value = escala_obj
    L.new(tc.outputs["Object"], vec.inputs[0])
    sum_ = N.new("ShaderNodeVectorMath"); sum_.operation = 'ADD'
    L.new(vec.outputs[0], sum_.inputs[0]); L.new(info.outputs["Random"], sum_.inputs[1])
    n1 = _ruido(N, L, sum_.outputs[0], 7.0, 12, 0.6)
    cr = _rampa(N, [oscuro, claro])
    L.new(n1.outputs["Fac"], cr.inputs["Fac"])
    var = _rampa(N, [(0.68, 0.66, 0.64), (1.18, 1.10, 1.0)])
    L.new(info.outputs["Random"], var.inputs["Fac"])
    mul = N.new("ShaderNodeMix"); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'; mul.inputs[0].default_value = 1
    L.new(cr.outputs["Color"], mul.inputs[6]); L.new(var.outputs["Color"], mul.inputs[7])
    ao = N.new("ShaderNodeAmbientOcclusion"); ao.inputs["Distance"].default_value = 0.004 if escala_obj > 5 else 0.04
    mz = N.new("ShaderNodeMix"); mz.data_type = 'RGBA'; mz.blend_type = 'MULTIPLY'
    inv = N.new("ShaderNodeMath"); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1.0
    L.new(ao.outputs["AO"], inv.inputs[1]); L.new(inv.outputs[0], mz.inputs[0])
    L.new(mul.outputs[2], mz.inputs[6]); mz.inputs[7].default_value = (0.35, 0.3, 0.25, 1)
    L.new(mz.outputs[2], b.inputs["Base Color"])
    rr = N.new("ShaderNodeMapRange"); rr.inputs["To Min"].default_value = 0.72; rr.inputs["To Max"].default_value = 0.95
    L.new(n1.outputs["Fac"], rr.inputs["Value"]); L.new(rr.outputs[0], b.inputs["Roughness"])
    n2 = _ruido(N, L, sum_.outputs[0], 90.0, 8, 0.7)
    v = N.new("ShaderNodeTexVoronoi"); v.feature = 'DISTANCE_TO_EDGE'; v.inputs["Scale"].default_value = 11
    L.new(sum_.outputs[0], v.inputs["Vector"])
    b1 = N.new("ShaderNodeBump"); b1.inputs["Strength"].default_value = 0.5
    b1.inputs["Distance"].default_value = 0.0004 if escala_obj > 5 else 0.004
    L.new(n2.outputs["Fac"], b1.inputs["Height"])
    cv = N.new("ShaderNodeMapRange"); cv.inputs["From Max"].default_value = 0.05
    L.new(v.outputs["Distance"], cv.inputs["Value"])
    b2 = N.new("ShaderNodeBump"); b2.inputs["Strength"].default_value = 0.3
    b2.inputs["Distance"].default_value = 0.0008 if escala_obj > 5 else 0.008
    L.new(cv.outputs[0], b2.inputs["Height"]); L.new(b1.outputs["Normal"], b2.inputs["Normal"])
    L.new(b2.outputs["Normal"], b.inputs["Normal"])
    L.new(b.outputs[0], o.inputs[0])
    return m


def mat_tierra(nombre="tierra", capas=True, escala_obj=1.0, claro=(0.36, 0.285, 0.20), oscuro=(0.19, 0.15, 0.105),
               paja=False):
    """Tierra apisonada o barro: granulada, con capas horizontales de apisonado y, si se pide, briznas de paja."""
    m, N, L = _arbol(nombre)
    o = N.new("ShaderNodeOutputMaterial"); b = N.new("ShaderNodeBsdfPrincipled")
    tc = N.new("ShaderNodeTexCoord")
    vec = N.new("ShaderNodeVectorMath"); vec.operation = 'SCALE'; vec.inputs["Scale"].default_value = escala_obj
    L.new(tc.outputs["Generated" if False else "Object"], vec.inputs[0])
    n1 = _ruido(N, L, vec.outputs[0], 4.0, 10, 0.6)
    cr = _rampa(N, [oscuro, claro])
    L.new(n1.outputs["Fac"], cr.inputs["Fac"])
    col = cr.outputs["Color"]
    alto = None
    if capas:                                   # capas de apisonado: bandas en z
        sep = N.new("ShaderNodeSeparateXYZ"); L.new(vec.outputs[0], sep.inputs[0])
        w = N.new("ShaderNodeTexWave"); w.wave_type = 'BANDS'; w.bands_direction = 'Z'
        w.inputs["Scale"].default_value = 7.0; w.inputs["Distortion"].default_value = 0.7
        w.inputs["Detail"].default_value = 3
        L.new(vec.outputs[0], w.inputs["Vector"])
        bnd = _rampa(N, [(0.72, 0.7, 0.68), (1.0, 1.0, 1.0), (1.1, 1.06, 1.0)], [0.0, 0.55, 1.0])
        L.new(w.outputs["Fac"], bnd.inputs["Fac"])
        mm = N.new("ShaderNodeMix"); mm.data_type = 'RGBA'; mm.blend_type = 'MULTIPLY'; mm.inputs[0].default_value = 1
        L.new(col, mm.inputs[6]); L.new(bnd.outputs["Color"], mm.inputs[7])
        col = mm.outputs[2]
        alto = w.outputs["Fac"]
    if paja:                                    # briznas de paja en el barro
        wv = N.new("ShaderNodeTexWave"); wv.wave_type = 'BANDS'; wv.inputs["Scale"].default_value = 60
        wv.inputs["Distortion"].default_value = 30; wv.inputs["Detail"].default_value = 2
        L.new(vec.outputs[0], wv.inputs["Vector"])
        ps = _rampa(N, [(0, 0, 0), (1, 1, 1)], [0.93, 0.97]); L.new(wv.outputs["Fac"], ps.inputs["Fac"])
        mp = N.new("ShaderNodeMix"); mp.data_type = 'RGBA'
        L.new(ps.outputs["Color"], mp.inputs[0]); L.new(col, mp.inputs[6]); mp.inputs[7].default_value = (0.62, 0.53, 0.33, 1)
        col = mp.outputs[2]
    L.new(col, b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.97
    v = N.new("ShaderNodeTexVoronoi"); v.inputs["Scale"].default_value = 140
    L.new(vec.outputs[0], v.inputs["Vector"])
    n2 = _ruido(N, L, vec.outputs[0], 40.0, 8, 0.7)
    mx = N.new("ShaderNodeMath"); mx.operation = 'ADD'
    L.new(v.outputs["Distance"], mx.inputs[0]); L.new(n2.outputs["Fac"], mx.inputs[1])
    bm = N.new("ShaderNodeBump"); bm.inputs["Strength"].default_value = 0.8
    bm.inputs["Distance"].default_value = 0.0006 if escala_obj > 5 else 0.006
    L.new(mx.outputs[0], bm.inputs["Height"])
    if alto is not None:
        b3 = N.new("ShaderNodeBump"); b3.inputs["Strength"].default_value = 0.25
        b3.inputs["Distance"].default_value = 0.0008 if escala_obj > 5 else 0.008
        L.new(alto, b3.inputs["Height"]); L.new(bm.outputs["Normal"], b3.inputs["Normal"])
        L.new(b3.outputs["Normal"], b.inputs["Normal"])
    else:
        L.new(bm.outputs["Normal"], b.inputs["Normal"])
    L.new(b.outputs[0], o.inputs[0])
    return m


def mat_barro_huella(nombre="barro_costal", escala_obj=1.0, paso=0.004):
    """Barro de la p'ira con la huella de un costal de lana: una trama cruzada en relieve (Šolc, 2011 [1975]: 105)."""
    m = mat_tierra(nombre, capas=False, escala_obj=escala_obj, claro=(0.36, 0.30, 0.22), oscuro=(0.2, 0.165, 0.12))
    N, L = m.node_tree.nodes, m.node_tree.links
    b = next(n for n in N if n.type == 'BSDF_PRINCIPLED')
    tc = N.new("ShaderNodeTexCoord")
    ondas = []
    for dirc in ('X', 'Y'):
        w = N.new("ShaderNodeTexWave"); w.wave_type = 'BANDS'; w.bands_direction = dirc
        w.inputs["Scale"].default_value = 1 / paso / 6.28 * 6.28 / 10
        w.inputs["Distortion"].default_value = 0.6; w.inputs["Detail"].default_value = 1
        L.new(tc.outputs["Object"], w.inputs["Vector"])
        ondas.append(w)
    mx = N.new("ShaderNodeMath"); mx.operation = 'MULTIPLY'
    L.new(ondas[0].outputs["Fac"], mx.inputs[0]); L.new(ondas[1].outputs["Fac"], mx.inputs[1])
    viejo = b.inputs["Normal"].links[0].from_node if b.inputs["Normal"].links else None
    bt = N.new("ShaderNodeBump"); bt.inputs["Strength"].default_value = 0.7; bt.inputs["Distance"].default_value = 0.0008
    L.new(mx.outputs[0], bt.inputs["Height"])
    if viejo:
        L.new(viejo.outputs["Normal"], bt.inputs["Normal"])
    L.new(bt.outputs["Normal"], b.inputs["Normal"])
    return m


def mat_paja(nombre="paja", seco=True):
    """Ichu seco: dorado gris en las puntas, más oscuro en la base; un poco translúcido."""
    m, N, L = _arbol(nombre)
    o = N.new("ShaderNodeOutputMaterial"); b = N.new("ShaderNodeBsdfPrincipled")
    uv = N.new("ShaderNodeUVMap"); sep = N.new("ShaderNodeSeparateXYZ"); L.new(uv.outputs[0], sep.inputs[0])
    cr = _rampa(N, [(0.13, 0.12, 0.07), (0.46, 0.39, 0.22), (0.66, 0.58, 0.40)], [0.0, 0.35, 1.0])
    L.new(sep.outputs["Y"], cr.inputs["Fac"])
    info = N.new("ShaderNodeObjectInfo"); attr = N.new("ShaderNodeAttribute"); attr.attribute_name = "azar"
    hsv = N.new("ShaderNodeHueSaturation")
    mr = N.new("ShaderNodeMapRange"); mr.inputs["To Min"].default_value = 0.72; mr.inputs["To Max"].default_value = 1.2
    L.new(attr.outputs["Fac"], mr.inputs["Value"])
    L.new(mr.outputs[0], hsv.inputs["Value"]); L.new(cr.outputs["Color"], hsv.inputs["Color"])
    L.new(hsv.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.55
    tr = N.new("ShaderNodeBsdfTranslucent"); L.new(hsv.outputs["Color"], tr.inputs["Color"])
    ms = N.new("ShaderNodeMixShader"); ms.inputs[0].default_value = 0.22
    L.new(b.outputs[0], ms.inputs[1]); L.new(tr.outputs[0], ms.inputs[2])
    L.new(ms.outputs[0], o.inputs[0])
    return m


def mat_madera(nombre="madera", tono=(0.42, 0.30, 0.18), vetas=True, escala_obj=1.0, rugosidad=0.6, contraste=0.28):
    """Madera: queñua de los palos o terciado de la mesa. Vetas con ondas deformadas."""
    m, N, L = _arbol(nombre)
    o = N.new("ShaderNodeOutputMaterial"); b = N.new("ShaderNodeBsdfPrincipled")
    tc = N.new("ShaderNodeTexCoord")
    vec = N.new("ShaderNodeVectorMath"); vec.operation = 'SCALE'; vec.inputs["Scale"].default_value = escala_obj
    L.new(tc.outputs["Object"], vec.inputs[0])
    w = N.new("ShaderNodeTexWave"); w.wave_type = 'BANDS'; w.bands_direction = 'X'
    w.inputs["Scale"].default_value = 3.0; w.inputs["Distortion"].default_value = 6; w.inputs["Detail"].default_value = 4
    L.new(vec.outputs[0], w.inputs["Vector"])
    osc = tuple(c * (1 - contraste) for c in tono)
    cr = _rampa(N, [osc, tono, tuple(min(1, c * (1 + contraste * 0.4)) for c in tono)], [0.0, 0.5, 1.0])
    L.new(w.outputs["Fac"], cr.inputs["Fac"])
    L.new(cr.outputs["Color"] if vetas else cr.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = rugosidad
    bm = N.new("ShaderNodeBump"); bm.inputs["Strength"].default_value = 0.15; bm.inputs["Distance"].default_value = 0.0005
    L.new(w.outputs["Fac"], bm.inputs["Height"]); L.new(bm.outputs["Normal"], b.inputs["Normal"])
    L.new(b.outputs[0], o.inputs[0])
    return m


def mat_liso(nombre, color, rugosidad=0.85):
    m, N, L = _arbol(nombre)
    o = N.new("ShaderNodeOutputMaterial"); b = N.new("ShaderNodeBsdfPrincipled")
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = rugosidad
    L.new(b.outputs[0], o.inputs[0])
    return m


class Materiales:
    def __init__(self):
        self.piedra = mat_piedra("piedra", escala_obj=12)
        self.piedra_fina = mat_piedra("piedra_menuda", claro=(0.34, 0.32, 0.29), oscuro=(0.12, 0.11, 0.1), escala_obj=18)
        self.tierra = mat_tierra("tierra_apisonada", capas=True, escala_obj=12)
        self.adobe = mat_tierra("adobe", capas=False, escala_obj=14, paja=True, claro=(0.40, 0.32, 0.22))
        self.champa = mat_tierra("champa", capas=False, escala_obj=14, claro=(0.26, 0.22, 0.15), oscuro=(0.11, 0.095, 0.07),
                                 paja=True)
        self.barro = mat_barro_huella("barro_costal", escala_obj=14)
        self.paja = mat_paja("ichu")
        self.palo = mat_madera("queñua", tono=(0.30, 0.20, 0.12), escala_obj=40, rugosidad=0.75)
        self.terciado = mat_madera("terciado", tono=(0.60, 0.50, 0.38), escala_obj=1.2, rugosidad=0.5, contraste=0.06)
        self.figura = mat_madera("figura", tono=(0.66, 0.55, 0.40), escala_obj=30, rugosidad=0.55)
        self.yeso = mat_liso("base_blanca", (0.80, 0.79, 0.77), 0.9)
        self.fondo = mat_liso("fondo", (0.82, 0.815, 0.80), 0.95)


# ----------------------------------------------------------------------------------------------------------------
# Generadores
# ----------------------------------------------------------------------------------------------------------------

def bm_piedra(dims, semilla, cortes=6, sub=2, rugosidad=1.0):
    """Piedra de campo: una caja cortada por planos al azar (caras de fractura), subdividida y rugosa."""
    r2 = random.Random(semilla)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * dims[0], v.co.y * dims[1], v.co.z * dims[2]))
    for _ in range(cortes):
        nrm = Vector((r2.uniform(-1, 1), r2.uniform(-1, 1), r2.uniform(-1, 1))).normalized()
        alcance = 0.5 * (abs(nrm.x) * dims[0] + abs(nrm.y) * dims[1] + abs(nrm.z) * dims[2])
        res = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], dist=1e-7,
                                     plane_co=nrm * alcance * r2.uniform(0.55, 0.85), plane_no=nrm, clear_outer=True)
        bordes = [e for e in res["geom_cut"] if isinstance(e, bmesh.types.BMEdge)]
        if bordes:
            bmesh.ops.holes_fill(bm, edges=bordes, sides=0)
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=sub, use_grid_fill=True)
    bm.normal_update()
    off = Vector((semilla * 1.31, semilla * 0.77, semilla * 0.33))
    m = min(dims)
    for v in bm.verts:
        d = noise.noise(v.co * (3.0 / m) + off) * 0.06 + noise.noise(v.co * (11.0 / m) + off) * 0.018
        v.co += v.normal * d * m * rugosidad
    return bm


class Pedrera:
    """Una biblioteca de piedras de tamaño unitario que se reutilizan como duplicados enlazados (instancias)."""

    def __init__(self, mat, n=36, semilla=1, cortes=(7, 11)):
        r = random.Random(semilla)
        self.mallas = []
        for i in range(n):
            dims = (1.0, r.uniform(0.6, 0.95), r.uniform(0.4, 0.75))
            bm = bm_piedra(dims, semilla * 1000 + i, cortes=r.randint(*cortes), sub=1, rugosidad=0.5)
            self.mallas.append((malla_de_bm(bm, f"piedra_{i}", mat, suave=False), dims))
        self.r = r

    def poner(self, centro, tam, rot=None, aplanar=1.0, nombre="piedra"):
        me, dims = self.r.choice(self.mallas)
        rot = rot if rot is not None else (self.r.uniform(-0.15, 0.15), self.r.uniform(-0.15, 0.15), self.r.uniform(0, 6.28))
        k = tam
        return objeto(nombre, me, centro, rot, (k, k, k * aplanar))


class Adobera:
    """Adobes hechos a mano: cajas de tamaño unitario con aristas gastadas y caras un poco irregulares, que se reutilizan
    como instancias, igual que las piedras de la Pedrera. poner() las escala a la medida real."""

    def __init__(self, mat, n=10, semilla=1, desorden=0.035):
        r = random.Random(semilla)
        self.mallas = []
        for i in range(n):
            bm = bmesh.new()
            bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=2, use_grid_fill=True)
            for v in bm.verts:
                v.co += Vector((r.uniform(-1, 1), r.uniform(-1, 1), r.uniform(-1, 1))) * desorden
            bmesh.ops.bevel(bm, geom=[e for e in bm.edges if not e.is_boundary], offset=0.06, segments=1,
                            affect='EDGES', clamp_overlap=True)
            self.mallas.append(malla_de_bm(bm, f"adobe_{i}", mat, suave=False))
        self.r = r

    def poner(self, centro, dims, giro=0.0, inclinar=0.01, nombre="adobe"):
        me = self.r.choice(self.mallas)
        rot = (self.r.uniform(-inclinar, inclinar), self.r.uniform(-inclinar, inclinar), giro + self.r.uniform(-0.02, 0.02))
        return objeto(nombre, me, centro, rot, dims)


def sigmoide(t):
    return 1 / (1 + math.exp(-t))


def monton(pedrera, centro, radio, alto, tam, r, hueco=None, z0=0.0):
    """Un montón de piedras sueltas: capas de piedras sobre la superficie de un cono (y un núcleo oscuro).
    hueco = (ángulo, ancho, alto) deja una boca."""
    cx, cy = centro[0], centro[1]
    capas = max(3, int(alto / (tam * 0.55)))
    puestas = 0
    for k in range(capas + 1):
        zk = alto * k / capas
        rk = radio * (1 - zk / alto)
        m = max(1, int(2 * math.pi * rk / (tam * 0.9)))
        fase = r.uniform(0, 6.28)
        for i in range(m):
            a = fase + 2 * math.pi * i / m + r.uniform(-0.1, 0.1)
            if hueco:
                da = (a - hueco[0] + math.pi) % (2 * math.pi) - math.pi
                if abs(da) < hueco[1] / 2 and zk < hueco[2]:
                    continue
            s = tam * r.uniform(0.7, 1.3) * (1 - 0.3 * zk / alto)
            pedrera.poner((cx + rk * math.cos(a), cy + rk * math.sin(a), z0 + zk + s * 0.2), s,
                          (r.uniform(-0.6, 0.6), r.uniform(-0.6, 0.6), r.uniform(0, 6.28)), aplanar=0.8)
            puestas += 1
    # núcleo para que no se vea a través
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=radio * 0.85, radius2=radio * 0.05, depth=alto * 0.9)
    for v in bm.verts:
        v.co.z += alto * 0.45
    ob = objeto("nucleo", malla_de_bm(bm, "nucleo", mat_liso("nucleo", (0.06, 0.055, 0.05))), (cx, cy, z0))
    if hueco:
        ob.hide_render = True
    return puestas


def hilada_recta(pedrera, p0, p1, z, alto, prof, r, lado_y=0.0, largo=(0.7, 1.5), exacto=False):
    """Una hilada de piedras de cara entre dos puntos (en planta), a la altura z.
    Con exacto, la hilada empieza y termina en los puntos dados, para no tapar vanos ni rendijas."""
    p0, p1 = Vector(p0), Vector(p1)
    d = (p1 - p0)
    L = d.length
    u = d.normalized()
    nrm = Vector((-u.y, u.x))
    t = 0.0 if exacto else -r.uniform(0, 0.4) * alto
    ang = math.atan2(u.y, u.x)
    while t < L:
        lx = alto * r.uniform(*largo)
        if exacto and L - t - lx < alto * largo[0] * 0.6:
            lx = L - t
        c = p0 + u * (t + lx / 2) + nrm * lado_y
        me, dims = r.choice(pedrera.mallas)
        objeto("piedra", me, (c.x, c.y, z + alto / 2 + r.uniform(-0.05, 0.05) * alto),
               (r.uniform(-0.06, 0.06), r.uniform(-0.06, 0.06), ang + r.uniform(-0.08, 0.08)),
               (lx * 0.96, prof / dims[1], alto / dims[2]))
        t += lx


def palo(a, b, r, mat, lados=8, nombre="palo"):
    a, b = Vector(a), Vector(b)
    d = b - a
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=lados, radius1=r, radius2=r * 0.85, depth=d.length)
    me = malla_de_bm(bm, nombre, mat)
    ob = objeto(nombre, me, (a + b) / 2)
    ob.rotation_mode = 'QUATERNION'
    ob.rotation_quaternion = d.to_track_quat('Z', 'Y')
    return ob


def caja(centro, dims, mat, nombre="caja", rot=(0, 0, 0), bisel=0.0):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * dims[0], v.co.y * dims[1], v.co.z * dims[2]))
    if bisel:
        bmesh.ops.bevel(bm, geom=bm.edges[:], offset=bisel, segments=2, affect='EDGES')
    return objeto(nombre, malla_de_bm(bm, nombre, mat, suave=False), centro, rot)


def tronco(centro, r_abajo, r_arriba, alto, mat, lados=4, abierto_arriba=False, espesor=0.0, nombre="tronco",
           ruido=0.0, semilla=0):
    """Tronco de cono o de pirámide (lados=4). Con espesor, es una cáscara hueca."""
    bm = bmesh.new()
    if lados == 4:
        bmesh.ops.create_cone(bm, cap_ends=not abierto_arriba, segments=4, radius1=r_abajo * math.sqrt(2),
                              radius2=r_arriba * math.sqrt(2), depth=alto)
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=__import__('mathutils').Matrix.Rotation(math.pi / 4, 3, 'Z'))
    else:
        bmesh.ops.create_cone(bm, cap_ends=not abierto_arriba, segments=lados, radius1=r_abajo, radius2=r_arriba, depth=alto)
    if abierto_arriba:
        arriba = [f for f in bm.faces if f.normal.z > 0.99]
        bmesh.ops.delete(bm, geom=arriba, context='FACES_ONLY')
    for v in bm.verts:
        v.co.z += alto / 2
    if ruido:
        bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=6, use_grid_fill=True)
        for v in bm.verts:
            v.co += Vector((noise.noise(v.co * 4 + Vector((semilla, 0, 0))), noise.noise(v.co * 4 + Vector((0, semilla, 0))), 0)) * ruido
    me = malla_de_bm(bm, nombre, mat, suave=lados > 6)
    ob = objeto(nombre, me, centro)
    if espesor:
        md = ob.modifiers.new("espesor", 'SOLIDIFY'); md.thickness = espesor
    return ob


def paja_sobre(objeto_base, mat, densidad=9000, largo=(0.02, 0.035), ancho=0.0007, semilla=1, abajo=Vector((0, 0, -1)),
               levantar=0.0015, capa=None):
    """Cubre las caras de un objeto con briznas de ichu que caen por la pendiente (techo de paja).
    Con capa (altura de cada hilada de paja, en metros de la maqueta), las briznas arrancan en líneas horizontales
    y se ven las capas que sobresalen una de otra, como en Enquelga (Šolc, 2011 [1975]: 109)."""
    r = random.Random(semilla)
    bpy.context.view_layer.update()
    me0 = objeto_base.data
    mw = objeto_base.matrix_world
    caras = [(f, f.area) for f in me0.polygons]
    total = sum(a for _, a in caras) * (objeto_base.scale.x * objeto_base.scale.y)
    n = int(densidad * total)
    pesos = [a for _, a in caras]
    verts, quads, uvs, azar = [], [], [], []
    acum = []
    s = 0
    for p in pesos:
        s += p
        acum.append(s)
    import bisect
    for _ in range(n):
        k = bisect.bisect(acum, r.uniform(0, s))
        f = caras[min(k, len(caras) - 1)][0]
        vs = [mw @ me0.vertices[i].co for i in f.vertices]
        a, b = r.random(), r.random()
        if a + b > 1:
            a, b = 1 - a, 1 - b
        p = vs[0] + (vs[1] - vs[0]) * a + (vs[-1] - vs[0]) * b
        nrm = (mw.to_3x3() @ f.normal).normalized()
        caida = (abajo - nrm * abajo.dot(nrm))
        if caida.length < 1e-4:
            caida = Vector((r.uniform(-1, 1), r.uniform(-1, 1), 0))
        caida.normalize()
        caida = (caida + Vector((r.uniform(-0.25, 0.25), r.uniform(-0.25, 0.25), r.uniform(-0.1, 0.1)))).normalized()
        lado = caida.cross(nrm).normalized()
        L = r.uniform(*largo)
        if capa and caida.z < -0.05:
            z_top = (math.floor(p.z / capa) + 1) * capa + r.uniform(-0.12, 0.12) * capa
            p = p + caida * ((p.z - z_top) / -caida.z)
            L = capa / -caida.z * r.uniform(1.25, 1.7)
        i0 = len(verts)
        seg = 3
        for j in range(seg + 1):
            t = j / seg
            q = p + nrm * (levantar + 0.002 * t * r.random()) + caida * L * t
            w = ancho * (1 - 0.7 * t)
            verts += [q - lado * w, q + lado * w]
            uvs += [(0, 0.25 + 0.75 * t), (1, 0.25 + 0.75 * t)]
            if j:
                c = i0 + 2 * (j - 1)
                quads.append((c, c + 1, c + 3, c + 2))
        azar.append(r.random())
    me = bpy.data.meshes.new("paja")
    me.from_pydata([tuple(v) for v in verts], [], quads)
    uvl = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        for li in poly.loop_indices:
            uvl.data[li].uv = uvs[me.loops[li].vertex_index]
    at = me.attributes.new("azar", 'FLOAT', 'FACE')
    for i, poly in enumerate(me.polygons):
        at.data[i].value = azar[i // 3]
    me.materials.append(mat)
    return objeto("paja", me)


def figura_madera(pos, mat, alto=1.65 * E, giro=0.0, pose="pie"):
    """La figura de madera que da la escala, como la de las maquetas de studio_cifuentes_ethz."""
    x, y, z = pos
    k = alto / 1.65
    partes = []
    if pose == "pie":
        partes = [((0, 0, 1.48), (0.2, 0.2, 0.26)), ((0, 0, 1.08), (0.38, 0.22, 0.52)),
                  ((-0.1, 0, 0.42), (0.14, 0.16, 0.8)), ((0.1, 0, 0.42), (0.14, 0.16, 0.8)),
                  ((-0.26, 0, 1.0), (0.1, 0.12, 0.62)), ((0.26, 0, 1.0), (0.1, 0.12, 0.62))]
    elif pose == "cuclillas":
        partes = [((0.05, 0, 0.9), (0.2, 0.2, 0.26)), ((-0.05, 0, 0.55), (0.36, 0.22, 0.5)),
                  ((0.08, -0.1, 0.32), (0.4, 0.14, 0.14)), ((0.08, 0.1, 0.32), (0.4, 0.14, 0.14)),
                  ((0.26, -0.1, 0.16), (0.12, 0.14, 0.32)), ((0.26, 0.1, 0.16), (0.12, 0.14, 0.32))]
    elif pose == "rodillas":
        partes = [((0.0, 0, 1.12), (0.2, 0.2, 0.26)), ((0.0, 0, 0.74), (0.36, 0.22, 0.52)),
                  ((0.0, -0.1, 0.25), (0.14, 0.14, 0.5)), ((0.0, 0.1, 0.25), (0.14, 0.14, 0.5)),
                  ((-0.22, -0.1, 0.05), (0.44, 0.13, 0.1)), ((-0.22, 0.1, 0.05), (0.44, 0.13, 0.1))]
    obs = []
    for (c, d) in partes:
        cx, cy = c[0] * math.cos(giro) - c[1] * math.sin(giro), c[0] * math.sin(giro) + c[1] * math.cos(giro)
        obs.append(caja((x + cx * k, y + cy * k, z + c[2] * k), (d[0] * k, d[1] * k, d[2] * k), mat, "figura",
                        rot=(0, 0, giro), bisel=0.004 * k))
    return obs


# ----------------------------------------------------------------------------------------------------------------
# El estudio: fondo curvo, mesa de terciado sobre caballetes, luz de ventana
# ----------------------------------------------------------------------------------------------------------------

def estudio(mats, tablero=(1.3, 0.85), alto_mesa=0.74, caballetes=True):
    """Devuelve la altura de la cubierta de la mesa. La maqueta se arma sobre z = esa altura."""
    # fondo curvo (ciclorama)
    bm = bmesh.new()
    perfil = []
    R = 0.9
    for i in range(13):
        a = math.pi / 2 * i / 12
        perfil.append((0, -R * math.cos(a) + R, R - R * math.sin(a)))
    pts = [(0, -6, 0)] + [(0, 2.2 + p[1], p[2]) for p in perfil] + [(0, 2.2 + R, 4.0)]
    vs_a = [bm.verts.new((-6, y, z)) for (_, y, z) in pts]
    vs_b = [bm.verts.new((6, y, z)) for (_, y, z) in pts]
    for i in range(len(pts) - 1):
        bm.faces.new((vs_a[i], vs_b[i], vs_b[i + 1], vs_a[i + 1]))
    objeto("fondo", malla_de_bm(bm, "fondo", mats.fondo))
    zc = alto_mesa
    caja((0, 0, zc - 0.012), (tablero[0], tablero[1], 0.024), mats.terciado, "tablero", bisel=0.002)
    if caballetes:
        for x in (-tablero[0] / 2 + 0.18, tablero[0] / 2 - 0.18):
            for sy in (-1, 1):
                palo((x - 0.1 * sy * 0, -0.3 * sy, 0), (x, -0.06 * sy, zc - 0.024), 0.018, mats.terciado, lados=4)
                palo((x, 0.3 * sy, 0), (x, 0.06 * sy, zc - 0.024), 0.018, mats.terciado, lados=4)
            caja((x, 0, zc - 0.05), (0.06, tablero[1] * 0.85, 0.05), mats.terciado, "travesano")
    # luz de ventana a la izquierda y un poco de relleno
    luz = bpy.data.lights.new("ventana", 'AREA'); luz.shape = 'RECTANGLE'; luz.size = 2.2; luz.size_y = 2.6
    luz.energy = 520
    ob = ligar(bpy.data.objects.new("ventana", luz)); ob.location = (-2.6, -0.6, 2.2)
    ob.rotation_euler = (Vector((0, 0.2, zc)) - ob.location).to_track_quat('-Z', 'Y').to_euler()
    luz2 = bpy.data.lights.new("rebote", 'AREA'); luz2.size = 3.0; luz2.energy = 90
    ob2 = ligar(bpy.data.objects.new("rebote", luz2)); ob2.location = (2.4, -2.2, 1.6)
    ob2.rotation_euler = (Vector((0, 0, zc)) - ob2.location).to_track_quat('-Z', 'Y').to_euler()
    w = bpy.data.worlds.new("estudio"); bpy.context.scene.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (0.9, 0.9, 0.92, 1); bg.inputs["Strength"].default_value = 0.18
    return zc


def camara(objetivo, distancia, acimut, elevacion, lente=50, apertura=None, nombre="camara"):
    cam = bpy.data.objects.new(nombre, bpy.data.cameras.new(nombre))
    ligar(cam)
    a, e = math.radians(acimut), math.radians(elevacion)
    t = Vector(objetivo)
    cam.location = t + Vector((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e))) * distancia
    cam.rotation_euler = (t - cam.location).to_track_quat('-Z', 'Y').to_euler()
    cam.data.lens = lente
    if apertura:
        cam.data.dof.use_dof = True
        cam.data.dof.focus_distance = (t - cam.location).length
        cam.data.dof.aperture_fstop = apertura
    bpy.context.scene.camera = cam
    return cam


def ajustes_render(ancho, alto, muestras, salida, exposicion=0.0):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.samples = muestras
    sc.cycles.use_denoising = True
    sc.cycles.denoiser = 'OPENIMAGEDENOISE'
    sc.cycles.max_bounces = 8
    sc.render.resolution_x, sc.render.resolution_y = ancho, alto
    sc.view_settings.view_transform = 'AgX'
    sc.view_settings.exposure = exposicion
    sc.render.filepath = salida
    sc.render.image_settings.file_format = 'JPEG'
    sc.render.image_settings.quality = 88
