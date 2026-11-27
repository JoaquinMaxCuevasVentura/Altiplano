"""Prototipo: una pirca de piedra seca en la puna, con cielo físico y el sol del 21 de junio a las 10.

Fue la primera prueba del flujo de trabajo en Blender (investigacion_blender.md, §3). Se corre así:
    venv_bpy/bin/python chhaxwa/blender/prototipo_pirca_paisaje.py -- ANCHO ALTO MUESTRAS SALIDA.png EXPOSICION
La imagen de renders/ se hizo con 1280 800 64 y exposición -5. Es un render, no una foto."""
import bpy, bmesh, math, random, sys, time
from mathutils import Vector, noise, Matrix

args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
W, H, SPP = int(args[0]) if args else 480, int(args[1]) if len(args) > 1 else 300, int(args[2]) if len(args) > 2 else 32
SALIDA = args[3] if len(args) > 3 else "render_prototipo.png"
EXPO = float(args[4]) if len(args) > 4 else -3.0
t0 = time.time()
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
rng = random.Random(7)

# --- cielo y sol -------------------------------------------------------------------------------------------
ALT_SOL, AZ_SOL = 35.1, 44.3            # La Paz, 21 de junio, 10:00 (tabla de la prueba 5)
w = bpy.data.worlds.new("cielo"); sc.world = w
nt = w.node_tree; nt.nodes.clear()
sky = nt.nodes.new("ShaderNodeTexSky"); sky.sky_type = 'MULTIPLE_SCATTERING'
sky.sun_elevation = math.radians(ALT_SOL); sky.sun_rotation = math.radians(AZ_SOL)
sky.altitude = 3850.0                   # altura del altiplano en metros
sky.sun_disc = True
bg = nt.nodes.new("ShaderNodeBackground"); out = nt.nodes.new("ShaderNodeOutputWorld")
nt.links.new(sky.outputs[0], bg.inputs[0]); nt.links.new(bg.outputs[0], out.inputs[0])


def nodos(mat):
    mat.use_nodes = True
    t = mat.node_tree
    t.nodes.clear()
    return t, t.nodes, t.links


# --- materiales ---------------------------------------------------------------------------------------------
def mat_piedra():
    m = bpy.data.materials.new("piedra")
    t, N, L = nodos(m)
    o = N.new("ShaderNodeOutputMaterial"); b = N.new("ShaderNodeBsdfPrincipled")
    tc = N.new("ShaderNodeTexCoord")
    info = N.new("ShaderNodeObjectInfo")
    # color: andesita gris parda con manchas; variación por piedra
    n1 = N.new("ShaderNodeTexNoise"); n1.inputs["Scale"].default_value = 6.0; n1.inputs["Detail"].default_value = 10
    L.new(tc.outputs["Object"], n1.inputs["Vector"])
    cr = N.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].color = (0.085, 0.078, 0.07, 1); cr.color_ramp.elements[1].color = (0.30, 0.27, 0.235, 1)
    L.new(n1.outputs["Fac"], cr.inputs["Fac"])
    var = N.new("ShaderNodeValToRGB")
    var.color_ramp.elements[0].color = (0.62, 0.6, 0.58, 1); var.color_ramp.elements[1].color = (1.2, 1.1, 0.98, 1)
    L.new(info.outputs["Random"], var.inputs["Fac"])
    mul = N.new("ShaderNodeMix"); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'; mul.inputs[0].default_value = 1
    L.new(cr.outputs["Color"], mul.inputs[6]); L.new(var.outputs["Color"], mul.inputs[7])
    # líquenes crustosos en las caras de arriba
    geo = N.new("ShaderNodeNewGeometry")
    sep = N.new("ShaderNodeSeparateXYZ"); L.new(geo.outputs["Normal"], sep.inputs[0])
    n2 = N.new("ShaderNodeTexNoise"); n2.inputs["Scale"].default_value = 14; n2.inputs["Detail"].default_value = 4
    L.new(tc.outputs["Object"], n2.inputs["Vector"])
    mth = N.new("ShaderNodeMath"); mth.operation = 'MULTIPLY'
    L.new(n2.outputs["Fac"], mth.inputs[0]); L.new(sep.outputs["Z"], mth.inputs[1])
    lim = N.new("ShaderNodeValToRGB")
    lim.color_ramp.elements[0].position = 0.43; lim.color_ramp.elements[1].position = 0.47
    L.new(mth.outputs[0], lim.inputs["Fac"])
    liq = N.new("ShaderNodeMix"); liq.data_type = 'RGBA'
    L.new(lim.outputs["Color"], liq.inputs[0]); L.new(mul.outputs[2], liq.inputs[6])
    liq.inputs[7].default_value = (0.52, 0.48, 0.22, 1)
    # suciedad en las cavidades
    ao = N.new("ShaderNodeAmbientOcclusion"); ao.inputs["Distance"].default_value = 0.05
    sucio = N.new("ShaderNodeMix"); sucio.data_type = 'RGBA'; sucio.blend_type = 'MULTIPLY'
    inv = N.new("ShaderNodeMath"); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1.0
    L.new(ao.outputs["AO"], inv.inputs[1])
    L.new(inv.outputs[0], sucio.inputs[0]); L.new(liq.outputs[2], sucio.inputs[6])
    sucio.inputs[7].default_value = (0.45, 0.38, 0.3, 1)
    L.new(sucio.outputs[2], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.88
    # relieve fino: grano y fisuras
    v = N.new("ShaderNodeTexVoronoi"); v.feature = 'DISTANCE_TO_EDGE'; v.inputs["Scale"].default_value = 9
    L.new(tc.outputs["Object"], v.inputs["Vector"])
    n3 = N.new("ShaderNodeTexNoise"); n3.inputs["Scale"].default_value = 140; n3.inputs["Detail"].default_value = 6
    L.new(tc.outputs["Object"], n3.inputs["Vector"])
    bm1 = N.new("ShaderNodeBump"); bm1.inputs["Strength"].default_value = 0.55; bm1.inputs["Distance"].default_value = 0.004
    L.new(n3.outputs["Fac"], bm1.inputs["Height"])
    cv = N.new("ShaderNodeMapRange"); cv.inputs["From Max"].default_value = 0.04
    L.new(v.outputs["Distance"], cv.inputs["Value"])
    bm2 = N.new("ShaderNodeBump"); bm2.inputs["Strength"].default_value = 0.25; bm2.inputs["Distance"].default_value = 0.01
    L.new(cv.outputs[0], bm2.inputs["Height"]); L.new(bm1.outputs["Normal"], bm2.inputs["Normal"])
    L.new(bm2.outputs["Normal"], b.inputs["Normal"])
    L.new(b.outputs[0], o.inputs[0])
    return m


def mat_suelo():
    m = bpy.data.materials.new("suelo")
    t, N, L = nodos(m)
    o = N.new("ShaderNodeOutputMaterial"); b = N.new("ShaderNodeBsdfPrincipled")
    tc = N.new("ShaderNodeTexCoord")
    n1 = N.new("ShaderNodeTexNoise"); n1.inputs["Scale"].default_value = 0.35; n1.inputs["Detail"].default_value = 10
    L.new(tc.outputs["Object"], n1.inputs["Vector"])
    cr = N.new("ShaderNodeValToRGB")
    e = cr.color_ramp.elements
    e[0].color = (0.085, 0.07, 0.055, 1); e[1].color = (0.20, 0.165, 0.12, 1)
    L.new(n1.outputs["Fac"], cr.inputs["Fac"])
    v = N.new("ShaderNodeTexVoronoi"); v.inputs["Scale"].default_value = 60; v.inputs["Randomness"].default_value = 1
    L.new(tc.outputs["Object"], v.inputs["Vector"])
    gr = N.new("ShaderNodeValToRGB")
    gr.color_ramp.elements[0].position = 0.0; gr.color_ramp.elements[1].position = 0.18
    L.new(v.outputs["Distance"], gr.inputs["Fac"])
    mix = N.new("ShaderNodeMix"); mix.data_type = 'RGBA'
    L.new(gr.outputs["Color"], mix.inputs[0])
    mix.inputs[6].default_value = (0.24, 0.225, 0.2, 1)       # granos de grava
    L.new(cr.outputs["Color"], mix.inputs[7])
    L.new(mix.outputs[2], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.95
    bm = N.new("ShaderNodeBump"); bm.inputs["Strength"].default_value = 0.6; bm.inputs["Distance"].default_value = 0.01
    inv = N.new("ShaderNodeMath"); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1
    L.new(gr.outputs["Color"], inv.inputs[1])
    L.new(inv.outputs[0], bm.inputs["Height"])
    L.new(bm.outputs["Normal"], b.inputs["Normal"])
    L.new(b.outputs[0], o.inputs[0])
    return m


def mat_ichu():
    m = bpy.data.materials.new("ichu")
    t, N, L = nodos(m)
    o = N.new("ShaderNodeOutputMaterial"); b = N.new("ShaderNodeBsdfPrincipled")
    uv = N.new("ShaderNodeUVMap"); sep = N.new("ShaderNodeSeparateXYZ")
    L.new(uv.outputs[0], sep.inputs[0])
    cr = N.new("ShaderNodeValToRGB")
    e = cr.color_ramp.elements
    e[0].position = 0.0; e[0].color = (0.16, 0.17, 0.08, 1)
    e[1].position = 0.35; e[1].color = (0.50, 0.42, 0.22, 1)
    e3 = e.new(1.0); e3.color = (0.70, 0.62, 0.42, 1)
    L.new(sep.outputs["Y"], cr.inputs["Fac"])
    info = N.new("ShaderNodeObjectInfo")
    hsv = N.new("ShaderNodeHueSaturation")
    mr = N.new("ShaderNodeMapRange"); mr.inputs["To Min"].default_value = 0.8; mr.inputs["To Max"].default_value = 1.15
    L.new(info.outputs["Random"], mr.inputs["Value"])
    L.new(mr.outputs[0], hsv.inputs["Value"]); L.new(cr.outputs["Color"], hsv.inputs["Color"])
    L.new(hsv.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.6
    b.inputs["Subsurface Weight"].default_value = 0.0
    b.inputs["Transmission Weight"].default_value = 0.0
    tr = N.new("ShaderNodeBsdfTranslucent"); L.new(hsv.outputs["Color"], tr.inputs["Color"])
    ms = N.new("ShaderNodeMixShader"); ms.inputs[0].default_value = 0.25
    L.new(b.outputs[0], ms.inputs[1]); L.new(tr.outputs[0], ms.inputs[2])
    L.new(ms.outputs[0], o.inputs[0])
    return m


def mat_lejos():
    """Cerros: el suelo, mezclado con el color del cielo según la distancia (perspectiva aérea)."""
    m = bpy.data.materials.new("lejos")
    t, N, L = nodos(m)
    o = N.new("ShaderNodeOutputMaterial"); b = N.new("ShaderNodeBsdfPrincipled")
    tc = N.new("ShaderNodeTexCoord")
    n1 = N.new("ShaderNodeTexNoise"); n1.inputs["Scale"].default_value = 0.004; n1.inputs["Detail"].default_value = 12
    L.new(tc.outputs["Object"], n1.inputs["Vector"])
    cr = N.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].color = (0.07, 0.065, 0.05, 1); cr.color_ramp.elements[1].color = (0.19, 0.16, 0.11, 1)
    L.new(n1.outputs["Fac"], cr.inputs["Fac"])
    L.new(cr.outputs["Color"], b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 1.0
    cam = N.new("ShaderNodeCameraData")
    mr = N.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = 300; mr.inputs["From Max"].default_value = 9000
    mr.inputs["To Max"].default_value = 0.55
    L.new(cam.outputs["View Distance"], mr.inputs["Value"])
    em = N.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (0.42, 0.55, 0.78, 1)
    em.inputs["Strength"].default_value = 3.0
    ms = N.new("ShaderNodeMixShader")
    L.new(mr.outputs[0], ms.inputs[0]); L.new(b.outputs[0], ms.inputs[1]); L.new(em.outputs[0], ms.inputs[2])
    L.new(ms.outputs[0], o.inputs[0])
    return m


M_PIEDRA, M_SUELO, M_ICHU = mat_piedra(), mat_suelo(), mat_ichu()


# --- piedras ------------------------------------------------------------------------------------------------
def malla_piedra(dims, semilla, cortes=6, sub=3, rugosidad=1.0):
    """Piedra de campo: una caja cortada por planos al azar (caras de fractura), subdividida y rugosa."""
    r2 = random.Random(semilla)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * dims[0], v.co.y * dims[1], v.co.z * dims[2]))
    for _ in range(cortes):
        nrm = Vector((r2.uniform(-1, 1), r2.uniform(-1, 1), r2.uniform(-1, 1))).normalized()
        alcance = 0.5 * (abs(nrm.x) * dims[0] + abs(nrm.y) * dims[1] + abs(nrm.z) * dims[2])
        co = nrm * alcance * r2.uniform(0.55, 0.85)
        geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
        res = bmesh.ops.bisect_plane(bm, geom=geom, dist=1e-5, plane_co=co, plane_no=nrm, clear_outer=True)
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
    me = bpy.data.meshes.new("piedra")
    bm.to_mesh(me); bm.free()
    for f in me.polygons:
        f.use_smooth = True
    me.materials.append(M_PIEDRA)
    return me


def poner(me, loc, rot=(0, 0, 0), nombre="o"):
    ob = bpy.data.objects.new(nombre, me)
    ob.location = loc; ob.rotation_euler = rot
    sc.collection.objects.link(ob)
    return ob


# la pirca: 5 m a lo largo de x, 0,6 m de ancho abajo y 0,5 arriba, 1,2 m de alto
LARGO, ALTO, BASE, CIMA = 5.0, 1.2, 0.6, 0.5
n = 0
z = 0.0
fila = 0
while z < ALTO - 0.06:
    hz_base = rng.uniform(0.15, 0.28) * (1.25 if fila == 0 else 1.0)
    tal = (BASE - CIMA) / 2 * (z + hz_base / 2) / ALTO
    for lado in (-1, 1):
        x = -rng.uniform(0, 0.25)
        while x < LARGO:
            lx = rng.uniform(0.16, 0.55)
            hz = hz_base * rng.uniform(0.75, 1.1)
            prof = rng.uniform(0.2, 0.32)
            y = lado * (BASE / 2 - tal - prof / 2 + 0.015)
            n += 1
            me = malla_piedra((lx * 0.96, prof, hz), n, cortes=rng.randint(4, 8))
            poner(me, (x + lx / 2, y + rng.uniform(-0.02, 0.02), z + hz / 2 + rng.uniform(-0.01, 0.01)),
                  (rng.uniform(-0.07, 0.07), rng.uniform(-0.08, 0.08), rng.uniform(-0.09, 0.09)))
            if rng.random() < 0.55:                    # cuña (ch'äta) en la junta
                s = rng.uniform(0.04, 0.08)
                n += 1
                me = malla_piedra((s * 1.3, s, s * 0.55), n, cortes=4, sub=2)
                poner(me, (x + lx + rng.uniform(-0.02, 0.02), y + lado * 0.06, z + rng.uniform(0.02, hz)),
                      (rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5), rng.uniform(0, 3)))
            x += lx
    for _ in range(int(LARGO / 0.12)):                 # relleno de piedra menuda
        s = rng.uniform(0.04, 0.09)
        n += 1
        me = malla_piedra((s, s * 0.9, s * 0.8), n, cortes=4, sub=2)
        poner(me, (rng.uniform(0, LARGO), rng.uniform(-0.09, 0.09), z + rng.uniform(0.03, hz_base - 0.03)))
    z += hz_base
    fila += 1
x = 0.0                                                # remate de piedras planas
while x < LARGO:
    lx = rng.uniform(0.25, 0.45)
    n += 1
    me = malla_piedra((lx, CIMA + rng.uniform(0.0, 0.12), rng.uniform(0.1, 0.17)), n, cortes=6)
    poner(me, (x + lx / 2, rng.uniform(-0.03, 0.03), z + 0.06), (rng.uniform(-0.08, 0.08), 0, rng.uniform(-0.1, 0.1)))
    x += lx
print("piedras de la pirca:", n)

# piedrecilla menuda regada al pie de la pirca
for i in range(260):
    s = rng.uniform(0.02, 0.09)
    n += 1
    me = malla_piedra((s, s * rng.uniform(0.6, 1), s * 0.6), n, cortes=5, sub=1)
    a = rng.uniform(-1.2, LARGO + 1.5)
    yy = rng.choice((-1, 1)) * (BASE / 2 + abs(rng.gauss(0, 0.6)))
    poner(me, (a, yy, s * 0.15), (0, 0, rng.uniform(0, 6.28)))

# --- suelo y cerros ------------------------------------------------------------------------------------------
bm = bmesh.new()
bmesh.ops.create_grid(bm, x_segments=160, y_segments=160, size=40)
for v in bm.verts:
    d = Vector((v.co.x, v.co.y, 0)).length
    v.co.z = noise.noise(v.co * 0.08) * 0.35 + noise.noise(v.co * 0.6) * 0.04 - (0.05 if d < 4 else 0)
    if d < 4:
        v.co.z *= (d / 4) ** 2
me = bpy.data.meshes.new("suelo"); bm.to_mesh(me); bm.free()
for f in me.polygons:
    f.use_smooth = True
me.materials.append(M_SUELO)
poner(me, (2.5, 0, -0.02), nombre="suelo")

bm = bmesh.new()
bmesh.ops.create_grid(bm, x_segments=260, y_segments=260, size=40000)
for v in bm.verts:
    d = v.co.length
    f = max(0.0, (d - 3000) / 9000)
    h = noise.ridged_multi_fractal(v.co * 0.00011, 0.9, 2.1, 7, 1.0, 2.0) * 700 * min(1.0, f) ** 0.8
    v.co.z = max(h, 0) - 3
me = bpy.data.meshes.new("cerros"); bm.to_mesh(me); bm.free()
for f in me.polygons:
    f.use_smooth = True
me.materials.append(mat_lejos())
poner(me, (0, 0, 0), nombre="cerros")


# --- ichu -----------------------------------------------------------------------------------------------------
def malla_mata(semilla, hojas=140):
    r2 = random.Random(semilla)
    verts, caras, uvs = [], [], []
    for h in range(hojas):
        ang = r2.uniform(0, 2 * math.pi)
        incl = abs(r2.gauss(0, 0.45)) + 0.05
        largo = r2.uniform(0.35, 0.85)
        base = Vector((math.cos(ang) * r2.uniform(0, 0.09), math.sin(ang) * r2.uniform(0, 0.09), 0))
        dirh = Vector((math.cos(ang), math.sin(ang), 0))
        perp = Vector((-math.sin(ang), math.cos(ang), 0))
        seg = 7
        i0 = len(verts)
        for k in range(seg + 1):
            t = k / seg
            caida = t * t * largo * (0.15 + incl * 0.6)
            p = base + dirh * math.sin(incl) * largo * t * 1.1 + Vector((0, 0, math.cos(incl) * largo * t - caida))
            p.z = max(p.z, 0.005)
            w = 0.0022 * (1 - t) + 0.0004
            verts += [p - perp * w, p + perp * w]
            uvs += [(0, t), (1, t)]
            if k:
                a = i0 + 2 * (k - 1)
                caras.append((a, a + 1, a + 3, a + 2))
    me = bpy.data.meshes.new("mata")
    me.from_pydata([tuple(v) for v in verts], [], caras)
    uvl = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        for li in poly.loop_indices:
            vi = me.loops[li].vertex_index
            uvl.data[li].uv = uvs[vi]
    me.materials.append(M_ICHU)
    return me


matas = [malla_mata(s) for s in range(6)]
cuantas = 0
for i in range(2600):
    x, y = rng.uniform(-8, 20), rng.uniform(-14, 18)
    if -0.9 < y < 0.9 and -0.6 < x < LARGO + 0.6:
        continue
    if noise.noise(Vector((x * 0.25, y * 0.25, 0))) < -0.3:
        continue
    ob = poner(rng.choice(matas), (x, y, 0.0), (0, 0, rng.uniform(0, 6.28)), nombre="mata")
    k = rng.uniform(0.8, 1.6); ob.scale = (k, k, k * rng.uniform(0.8, 1.2))
    cuantas += 1
print("matas de ichu:", cuantas)

# --- cámara y render -----------------------------------------------------------------------------------------
cam = bpy.data.objects.new("camara", bpy.data.cameras.new("camara"))
sc.collection.objects.link(cam); sc.camera = cam
cam.data.lens = 35
cam.location = (-2.2, 4.6, 1.55)
d = Vector((2.6, 0.0, 0.55)) - cam.location
cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
sc.render.engine = 'CYCLES'
sc.cycles.device = 'CPU'
sc.cycles.samples = SPP
sc.cycles.use_denoising = True
sc.cycles.denoiser = 'OPENIMAGEDENOISE'
sc.cycles.max_bounces = 6
sc.render.resolution_x, sc.render.resolution_y = W, H
sc.view_settings.view_transform = 'AgX'
sc.view_settings.exposure = EXPO
sc.render.filepath = SALIDA
sc.render.image_settings.file_format = 'PNG'
print("escena armada en %.1f s" % (time.time() - t0))
t1 = time.time()
bpy.ops.render.render(write_still=True)
print("render en %.1f s" % (time.time() - t1))
