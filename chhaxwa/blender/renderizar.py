"""Renderiza las maquetas de forma de Chhaxwa en el estudio.

Necesita Blender como módulo de Python (bpy 5.0.1, para Python 3.11):
    python3 -m venv venv_bpy && venv_bpy/bin/pip install bpy==5.0.1
Se corre desde la raíz del repositorio:
    venv_bpy/bin/python chhaxwa/blender/renderizar.py 1A 2B        # algunas
    venv_bpy/bin/python chhaxwa/blender/renderizar.py todas         # las quince
    ... --rapido                                                   # 480 px y pocas muestras, para probar
    ... --medio                                                    # 640 px, para las hojas de contacto
    ... --salida CARPETA                                           # por omisión, chhaxwa/renders/

Cada imagen se llama render_forma_XX.jpg. Son renders de Blender, no fotos de maquetas: así hay que presentarlas.
"""

import math
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import bpy                       # noqa: E402
from mathutils import Vector     # noqa: E402

import comun as C                # noqa: E402
import formas as F               # noqa: E402


def encuadrar(objs, acimut=-35, elevacion=22, lente=55, aire=1.12):
    bpy.context.view_layer.update()
    pts = []
    for ob in objs:
        if ob.hide_render or ob.type != 'MESH':
            continue
        pts += [ob.matrix_world @ Vector(c) for c in ob.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    centro = (lo + hi) / 2
    radio = (hi - lo).length / 2
    fov = 2 * math.atan(18 / lente)
    dist = radio / math.sin(fov / 2) * aire
    return C.camara(centro, dist, acimut, elevacion, lente=lente)


def renderizar(clave, salida, rapido=False, semilla=1):
    t0 = time.time()
    C.escena_nueva()
    mats = C.Materiales()
    zc = C.estudio(mats)
    antes = set(bpy.data.objects)
    ctx = F.Ctx(mats, zc, semilla)
    res = F.FORMAS[clave](ctx)
    k, nombre = res[0], res[1]
    vista = dict(res[2]) if len(res) > 2 else {}
    nuevos = [o for o in bpy.data.objects if o not in antes]
    giro = vista.pop("girar", 0)
    if giro:                                         # se gira la maqueta sobre la mesa, como se haría con una real
        vacio = C.ligar(bpy.data.objects.new("giro", None))
        vacio.location = (0, 0, zc)
        bpy.context.view_layer.update()
        for ob in nuevos:
            ob.parent = vacio
            ob.matrix_parent_inverse = vacio.matrix_world.inverted()
        vacio.rotation_euler.z = math.radians(giro)
    encuadrar(nuevos, **vista)
    ancho, alto, muestras = {"rapido": (480, 600, 16), "medio": (640, 800, 28)}.get(rapido, (1000, 1250, 80))
    destino = Path(salida) / f"render_forma_{clave}.jpg"
    C.ajustes_render(ancho, alto, muestras, str(destino), exposicion=-1.5)
    print(f"{clave} · {nombre} · escala 1:{round(1 / k)} · {len(nuevos)} objetos · armada en {time.time() - t0:.0f} s")
    t1 = time.time()
    bpy.ops.render.render(write_still=True)
    print(f"{clave} renderizada en {time.time() - t1:.0f} s -> {destino}")


def main():
    args = [a for a in sys.argv[1:] if a != "--"]
    rapido = "rapido" if "--rapido" in args else ("medio" if "--medio" in args else None)
    salida = AQUI.parent / "renders"
    if "--salida" in args:
        salida = Path(args[args.index("--salida") + 1])
    exploracion = [c for c in F.FORMAS if c[0].isdigit()]
    elegidas = [c for c in F.FORMAS if c.startswith("E")]
    claves = ([a for a in args if a in F.FORMAS] or (exploracion if "exploracion" in args else [])
              + (elegidas if "elegidas" in args else []) or (list(F.FORMAS) if "todas" in args else []))
    if not claves:
        sys.exit("Indica qué formas: 1A, 1B, ... 5C, o «todas».")
    salida.mkdir(parents=True, exist_ok=True)
    for c in claves:
        renderizar(c, salida, rapido)


if __name__ == "__main__":
    main()
