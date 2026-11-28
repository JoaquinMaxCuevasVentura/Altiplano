"""La bóveda de E5 en Geometry Nodes, armada desde código.

Arma un grupo de nodos, «Bóveda de E5», cuyos controles son los parámetros del piloto: el arranque, el alto de la hilada,
el vuelo inicial y el final para la bóveda de hiladas voladas, y la flecha y el espesor para la bóveda verdadera, que
se elige con un interruptor. En Blender se abre e5_parametrica.blend, se elige uno de los cuatro objetos y se mueven
los controles en el panel del modificador: la bóveda cambia al momento. Las reglas no están en los nodos; se revisan
con boveda_e5.py.

El guion comprueba que los nodos dan la misma geometría que el cálculo de Python (el número de hiladas y la altura de la
clave), guarda el .blend y hace una imagen de los cuatro objetos, e5_nodos.jpg. Es un render de Blender, no una foto.
Se corre desde la raíz:
    venv_bpy/bin/python chhaxwa/parametrico/boveda_e5_nodos.py      (bpy 5.0.1, Python 3.11)
"""

import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import bpy                                   # noqa: E402

import boveda_e5 as B                        # noqa: E402
import boveda_e5_verdadera as V              # noqa: E402

CONTROLES = [   # (nombre, tipo, valor, mínimo, máximo)
    ("Bóveda verdadera", "NodeSocketBool", False, None, None),
    ("Ancho", "NodeSocketFloat", B.WI, 2.0, 5.0),
    ("Largo", "NodeSocketFloat", B.LI, 1.0, 10.0),
    ("Alto del bloque", "NodeSocketFloat", B.HW, 1.0, 4.0),
    ("Muro", "NodeSocketFloat", B.CARA, 0.1, 1.0),
    ("Arranque", "NodeSocketFloat", 0.35, 0.0, 1.5),
    ("Alto de hilada", "NodeSocketFloat", B.HH, 0.05, 0.3),
    ("Vuelo inicial", "NodeSocketFloat", 0.11, 0.02, 0.3),
    ("Vuelo final", "NodeSocketFloat", 0.13, 0.02, 0.3),
    ("Cierre", "NodeSocketFloat", B.R_CIERRE, 0.05, 0.5),
    ("Cola", "NodeSocketFloat", B.COLA, 0.1, 0.8),
    ("Flecha", "NodeSocketFloat", B.WI / 2, 0.3, 3.0),
    ("Espesor", "NodeSocketFloat", 0.20, 0.05, 0.5),
]


def material(nombre, color):
    m = bpy.data.materials.new(nombre)
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.9
    return m


def arbol(mats):
    ng = bpy.data.node_groups.new("Bóveda de E5", "GeometryNodeTree")
    for nombre, tipo, valor, lo, hi in CONTROLES:
        s = ng.interface.new_socket(nombre, in_out="INPUT", socket_type=tipo)
        s.default_value = valor
        if lo is not None:
            s.min_value, s.max_value = lo, hi
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    N, Ln = ng.nodes, ng.links
    gi, go = N.new("NodeGroupInput"), N.new("NodeGroupOutput")
    E = {nombre: gi.outputs[nombre] for nombre, *_ in CONTROLES}

    def conectar(dst, src):
        if isinstance(src, (int, float)):
            dst.default_value = src
        else:
            Ln.new(src, dst)

    def m(op, a, b=None, c=None):
        n = N.new("ShaderNodeMath")
        n.operation = op
        for k, x in enumerate((a, b, c)):
            if x is not None:
                conectar(n.inputs[k], x)
        return n.outputs[0]

    def xyz(x, y, z):
        n = N.new("ShaderNodeCombineXYZ")
        for k, v in enumerate((x, y, z)):
            conectar(n.inputs[k], v)
        return n.outputs[0]

    def cubo(sx, sy, sz):
        n = N.new("GeometryNodeMeshCube")
        conectar(n.inputs["Size"], xyz(sx, sy, sz))
        return n.outputs["Mesh"]

    def juntar(*geos):
        n = N.new("GeometryNodeJoinGeometry")
        for g in reversed(geos):
            Ln.new(g, n.inputs["Geometry"])
        return n.outputs["Geometry"]

    def con_material(geo, mat):
        n = N.new("GeometryNodeSetMaterial")
        Ln.new(geo, n.inputs["Geometry"])
        n.inputs["Material"].default_value = mat
        return n.outputs["Geometry"]

    def espejar(geo):
        """La otra mitad: media vuelta sobre el eje vertical (la bóveda es simétrica a lo largo), sin dar vuelta las normales."""
        n = N.new("GeometryNodeTransform")
        Ln.new(geo, n.inputs["Geometry"])
        n.inputs["Rotation"].default_value = (0.0, 0.0, math.pi)
        return juntar(geo, n.outputs["Geometry"])

    R = m("MULTIPLY", E["Ancho"], 0.5)
    # --- la bóveda de hiladas voladas: la cuenta de cupula_perfil, hilada por hilada ------------------------------------
    b = m("DIVIDE", E["Vuelo inicial"], E["Alto de hilada"])
    a2H = m("MULTIPLY", m("SUBTRACT", m("DIVIDE", E["Vuelo final"], E["Alto de hilada"]), b), 0.5)
    Hh = m("DIVIDE", m("SUBTRACT", R, E["Cierre"]), m("ADD", b, a2H))
    a2 = m("DIVIDE", a2H, Hh)
    n_hil = m("ADD", m("CEIL", m("SUBTRACT", m("DIVIDE", Hh, E["Alto de hilada"]), 0.5001)), 1.0)   # como en boveda_e5.py
    linea = N.new("GeometryNodeMeshLine")
    linea.inputs["Count"].default_value = 60
    idx = N.new("GeometryNodeInputIndex").outputs[0]
    h = m("MULTIPLY", idx, E["Alto de hilada"])
    r = m("MAXIMUM", E["Cierre"], m("SUBTRACT", m("SUBTRACT", R, m("MULTIPLY", b, h)), m("MULTIPLY", a2, m("MULTIPLY", h, h))))
    pos = xyz(m("ADD", r, m("MULTIPLY", E["Cola"], 0.5)), 0.0,
              m("ADD", m("ADD", E["Arranque"], h), m("MULTIPLY", E["Alto de hilada"], 0.5)))
    sp = N.new("GeometryNodeSetPosition")
    Ln.new(linea.outputs["Mesh"], sp.inputs["Geometry"])
    Ln.new(pos, sp.inputs["Position"])
    cmp = N.new("FunctionNodeCompare")
    cmp.data_type, cmp.operation = "FLOAT", "GREATER_EQUAL"
    Ln.new(idx, cmp.inputs[0])
    Ln.new(n_hil, cmp.inputs[1])
    borrar = N.new("GeometryNodeDeleteGeometry")
    borrar.domain = "POINT"
    Ln.new(sp.outputs["Geometry"], borrar.inputs["Geometry"])
    Ln.new(cmp.outputs["Result"], borrar.inputs["Selection"])
    inst = N.new("GeometryNodeInstanceOnPoints")
    Ln.new(borrar.outputs["Geometry"], inst.inputs["Points"])
    Ln.new(cubo(E["Cola"], E["Largo"], m("SUBTRACT", E["Alto de hilada"], 0.01)), inst.inputs["Instance"])
    real = N.new("GeometryNodeRealizeInstances")
    Ln.new(inst.outputs["Instances"], real.inputs["Geometry"])
    z_clave = m("ADD", E["Arranque"], m("MULTIPLY", n_hil, E["Alto de hilada"]))
    lajas = N.new("GeometryNodeTransform")
    Ln.new(cubo(B.LAJA_ANCHO, E["Largo"], B.LAJA), lajas.inputs["Geometry"])
    Ln.new(xyz(0.0, 0.0, m("ADD", z_clave, B.LAJA / 2)), lajas.inputs["Translation"])
    volada = juntar(con_material(espejar(real.outputs["Geometry"]), mats["adobe"]),
                    con_material(lajas.outputs["Geometry"], mats["laja"]))
    # --- la bóveda verdadera: un arco de círculo con su flecha (de medio punto si la flecha es el medio ancho) ---------
    f = E["Flecha"]
    Rarc = m("DIVIDE", m("ADD", m("MULTIPLY", R, R), m("MULTIPLY", f, f)), m("MULTIPLY", f, 2.0))
    al = m("ARCSINE", m("MINIMUM", m("DIVIDE", R, Rarc), 1.0))
    arco = N.new("GeometryNodeCurveArc")
    arco.mode = "RADIUS"
    arco.inputs["Resolution"].default_value = 96
    Ln.new(m("ADD", Rarc, m("MULTIPLY", E["Espesor"], 0.5)), arco.inputs["Radius"])
    Ln.new(m("SUBTRACT", math.pi / 2, al), arco.inputs["Start Angle"])
    Ln.new(m("MULTIPLY", al, 2.0), arco.inputs["Sweep Angle"])
    # las dovelas: un punto cada 11 cm por el arco y en cada uno un adobe con la junta hacia el centro
    puntos = N.new("GeometryNodeCurveToPoints")
    puntos.mode = "LENGTH"
    puntos.inputs["Length"].default_value = 0.11
    Ln.new(arco.outputs["Curve"], puntos.inputs["Curve"])
    sep = N.new("ShaderNodeSeparateXYZ")
    Ln.new(N.new("GeometryNodeInputPosition").outputs[0], sep.inputs[0])
    phi = m("ARCTAN2", sep.outputs["Y"], sep.outputs["X"])
    n_arcos = m("CEIL", m("DIVIDE", E["Largo"], 0.40))
    paso = m("DIVIDE", E["Largo"], n_arcos)
    dovelas = N.new("GeometryNodeInstanceOnPoints")
    Ln.new(puntos.outputs["Points"], dovelas.inputs["Points"])
    Ln.new(cubo(E["Espesor"], 0.10, m("SUBTRACT", paso, 0.01)), dovelas.inputs["Instance"])
    Ln.new(xyz(0.0, 0.0, phi), dovelas.inputs["Rotation"])
    un_arco = N.new("GeometryNodeRealizeInstances")
    Ln.new(dovelas.outputs["Instances"], un_arco.inputs["Geometry"])
    # los arcos, uno detrás de otro a lo largo de la bóveda
    fila = N.new("GeometryNodeMeshLine")
    Ln.new(n_arcos, fila.inputs["Count"])
    Ln.new(xyz(0.0, 0.0, m("ADD", m("MULTIPLY", E["Largo"], -0.5), m("MULTIPLY", paso, 0.5))), fila.inputs["Start Location"])
    Ln.new(xyz(0.0, 0.0, paso), fila.inputs["Offset"])
    arcos = N.new("GeometryNodeInstanceOnPoints")
    Ln.new(fila.outputs["Mesh"], arcos.inputs["Points"])
    Ln.new(un_arco.outputs["Geometry"], arcos.inputs["Instance"])
    # trabado: un arco de cada dos gira media dovela, para que las juntas no corran a lo largo
    impar = m("MODULO", N.new("GeometryNodeInputIndex").outputs[0], 2.0)
    medio = m("DIVIDE", 0.055, m("ADD", Rarc, m("MULTIPLY", E["Espesor"], 0.5)))
    Ln.new(xyz(0.0, 0.0, m("MULTIPLY", impar, medio)), arcos.inputs["Rotation"])
    malla = N.new("GeometryNodeRealizeInstances")
    Ln.new(arcos.outputs["Instances"], malla.inputs["Geometry"])
    girar = N.new("GeometryNodeTransform")
    Ln.new(malla.outputs["Geometry"], girar.inputs["Geometry"])
    girar.inputs["Rotation"].default_value = (math.pi / 2, 0.0, 0.0)
    subir = N.new("GeometryNodeTransform")
    Ln.new(girar.outputs["Geometry"], subir.inputs["Geometry"])
    Ln.new(xyz(0.0, 0.0, m("SUBTRACT", m("ADD", E["Arranque"], f), Rarc)), subir.inputs["Translation"])
    verdadera = con_material(subir.outputs["Geometry"], mats["adobe"])
    sw = N.new("GeometryNodeSwitch")
    sw.input_type = "GEOMETRY"
    Ln.new(E["Bóveda verdadera"], sw.inputs["Switch"])
    Ln.new(volada, sw.inputs["False"])
    Ln.new(verdadera, sw.inputs["True"])
    # --- los muros: la cara de adentro hasta el arranque y la pirca de afuera, sin talud -----------------------------
    cara = N.new("GeometryNodeTransform")
    Ln.new(cubo(E["Muro"], E["Largo"], E["Arranque"]), cara.inputs["Geometry"])
    Ln.new(xyz(m("ADD", R, m("MULTIPLY", E["Muro"], 0.5)), 0.0, m("MULTIPLY", E["Arranque"], 0.5)), cara.inputs["Translation"])
    pirca = N.new("GeometryNodeTransform")
    Ln.new(cubo(E["Muro"], E["Largo"], E["Alto del bloque"]), pirca.inputs["Geometry"])
    Ln.new(xyz(m("ADD", R, m("SUBTRACT", B.E0, m("MULTIPLY", E["Muro"], 0.5))), 0.0, m("MULTIPLY", E["Alto del bloque"], 0.5)),
           pirca.inputs["Translation"])
    muros = con_material(espejar(juntar(cara.outputs["Geometry"], pirca.outputs["Geometry"])), mats["piedra"])
    Ln.new(juntar(sw.outputs["Output"], muros), go.inputs["Geometry"])
    return ng


def objeto(ng, nombre, valores, x):
    me = bpy.data.meshes.new(nombre)
    ob = bpy.data.objects.new(nombre, me)
    bpy.context.scene.collection.objects.link(ob)
    md = ob.modifiers.new("Bóveda", "NODES")
    md.node_group = ng
    ids = {it.name: it.identifier for it in ng.interface.items_tree if it.item_type == "SOCKET" and it.in_out == "INPUT"}
    for k, v in valores.items():
        md[ids[k]] = v
    ob.location.x = x
    return ob


def medir(ob):
    """Los vértices del objeto y lo más alto de la bóveda (sin los muros, que están más allá de 1,6 m del eje)."""
    dg = bpy.context.evaluated_depsgraph_get()
    ev = ob.evaluated_get(dg)
    me = ev.to_mesh()
    zs = [v.co.z for v in me.vertices if abs(v.co.x) < 1.0]
    ys = [v.co.y for v in me.vertices]
    n = len(me.vertices)
    ev.to_mesh_clear()
    return n, max(zs), max(ys) - min(ys)


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    mats = {"adobe": material("adobe", (0.62, 0.50, 0.39)), "laja": material("laja", (0.38, 0.38, 0.37)),
            "piedra": material("piedra", (0.55, 0.54, 0.52))}
    ng = arbol(mats)
    vs = B.barrer()
    actual = B.buscar(vs, *B.ACTUAL)
    quince = B.mejor(vs, 2)
    casos = [("E5, la actual", dict(Arranque=actual["arranque"], **{"Vuelo inicial": actual["vuelo_inicial"],
                                                                     "Vuelo final": actual["vuelo_final"]}), actual),
             ("Hiladas voladas, si el adobe vuela 15 cm", dict(Arranque=quince["arranque"], **{
                 "Vuelo inicial": quince["vuelo_inicial"], "Vuelo final": quince["vuelo_final"]}), quince),
             ("De medio punto, dovelas de canto", {"Bóveda verdadera": True, "Arranque": 0.15, "Flecha": B.WI / 2,
                                                   "Espesor": 0.20}, None),
             ("Rebajada, dovelas de canto", {"Bóveda verdadera": True, "Arranque": 0.80, "Flecha": 1.00, "Espesor": 0.20}, None)]
    obs = []
    for k, (nombre, valores, ref) in enumerate(casos):
        ob = objeto(ng, nombre, valores, k * 7.0)
        obs.append(ob)
        nv, zmax, largo = medir(ob)
        assert abs(largo - B.LI) < 0.02, (nombre, largo)
        if ref is not None:                                    # las hiladas y la clave, contra el cálculo de Python
            n_nodos = (nv // 8 - 1 - 4) // 2
            assert n_nodos == ref["hiladas"], (nombre, n_nodos, ref["hiladas"])
            assert abs(zmax - ref["techo"]) < 1e-4, (nombre, zmax, ref["techo"])
        else:
            P = V.intrados("medio punto" if valores["Flecha"] >= B.WI / 2 else "rebajada", valores["Arranque"], valores["Flecha"])
            techo = P[0][1] + valores["Espesor"]
            assert abs(zmax - techo) < 0.02, (nombre, zmax, techo)
        print(f"{nombre}: {nv} vértices, lo más alto a {zmax:.3f} m (coincide con el cálculo)")
    # una cámara, una luz y el render de los cuatro
    cam = bpy.data.objects.new("cámara", bpy.data.cameras.new("cámara"))
    bpy.context.scene.collection.objects.link(cam)
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = 29.5
    cam.location = (10.5 + 18 * math.sin(math.radians(-22)), -18 * math.cos(math.radians(-22)), 7.2)
    cam.rotation_euler = (math.radians(70), 0.0, math.radians(-22))
    bpy.context.scene.camera = cam
    sol = bpy.data.objects.new("sol", bpy.data.lights.new("sol", "SUN"))
    sol.data.energy = 3.0
    sol.rotation_euler = (math.radians(50), 0.0, math.radians(-40))
    bpy.context.scene.collection.objects.link(sol)
    mundo = bpy.data.worlds.new("mundo")
    mundo.use_nodes = True
    mundo.node_tree.nodes["Background"].inputs["Color"].default_value = (0.92, 0.91, 0.89, 1.0)
    mundo.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.9
    bpy.context.scene.world = mundo
    suelo = bpy.data.objects.new("suelo", bpy.data.meshes.new("suelo"))
    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=30)
    bm.to_mesh(suelo.data)
    suelo.location = (10.5, 0, 0)
    suelo.data.materials.append(material("suelo", (0.80, 0.79, 0.76)))
    bpy.context.scene.collection.objects.link(suelo)
    esc = bpy.context.scene
    esc.render.engine = "CYCLES"
    esc.cycles.device = "CPU"
    esc.cycles.samples = 48
    esc.render.resolution_x, esc.render.resolution_y = 2400, 820
    esc.view_settings.view_transform = "AgX"
    esc.render.image_settings.file_format = "JPEG"
    esc.render.image_settings.quality = 88
    esc.render.filepath = str(AQUI / "e5_nodos.jpg")
    bpy.context.preferences.filepaths.save_version = 0           # sin la copia de respaldo .blend1
    bpy.ops.wm.save_as_mainfile(filepath=str(AQUI / "e5_parametrica.blend"), compress=True)
    if "--sin-render" not in sys.argv:
        bpy.ops.render.render(write_still=True)
    print("listo")


if __name__ == "__main__":
    main()
