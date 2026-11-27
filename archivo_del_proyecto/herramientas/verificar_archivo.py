#!/usr/bin/env python3
"""Verifica archivo_del_proyecto/ y escribe verificacion.md.

Comprueba que cada copia coincide con su origen, que el inventario ubica todo lo recuperado, que los enlaces de
los índices y las fichas funcionan y que los originales no cambiaron. Se corre desde la raíz del repositorio:
    python3 archivo_del_proyecto/herramientas/verificar_archivo.py
Sale con error si alguna comprobación falla.
"""

import csv
import datetime as dt
import hashlib
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import unquote

ARCHIVO = "archivo_del_proyecto"
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent))
import armar_archivo as A   # noqa: E402  (las mismas reglas con que se armó)


def git(*args, binario=False):
    r = subprocess.run(["git", "-c", "core.quotepath=false", *args], capture_output=True, check=True)
    return r.stdout if binario else r.stdout.decode("utf8")


def blob_git(b):
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def main():
    raiz = Path(git("rev-parse", "--show-toplevel").strip())
    arch = raiz / ARCHIVO
    filas = list(csv.DictReader(open(arch / "inventario.csv", encoding="utf-8-sig")))
    por_id = {f["id"]: f for f in filas}
    pruebas = []          # (qué, cuántos, fallos)

    def prueba(que, total, fallos):
        pruebas.append((que, total, fallos))

    # 1. identificadores únicos y estados permitidos
    repetidos = [i for i, n in Counter(f["id"] for f in filas).items() if n > 1]
    prueba("Los identificadores del inventario no se repiten", len(filas), repetidos)
    prueba("Cada estado es uno de los siete previstos, o está vacío", len(filas),
           [f["id"] for f in filas if f["estado"] and f["estado"] not in A.ESTADOS])

    # 2. cada copia existe y conserva su contenido
    copias = [f for f in filas if f["copia"].startswith("copia")]
    fallos = []
    for f in copias:
        p = raiz / f["ruta_archivada"]
        if not p.is_file():
            fallos.append(f"{f['id']}: falta {f['ruta_archivada']}")
            continue
        b = p.read_bytes()
        if hashlib.sha256(b).hexdigest() != f["sha256"] or blob_git(b) != f["blob_git"] or str(len(b)) != f["bytes"]:
            fallos.append(f"{f['id']}: el contenido no coincide con el inventario")
    prueba("Cada archivo copiado existe y su SHA-256, su tamaño y su identificador de git son los del inventario", len(copias), fallos)

    # 3. cada copia de git coincide con su procedencia: el contenido de esa ruta en ese commit
    de_git = [f for f in filas if f["id"][0] in "HDR" and f["commit"]]
    fallos = []
    for f in de_git:
        try:
            blob = git("rev-parse", f"{f['commit']}:{f['ruta_original']}").strip()
        except subprocess.CalledProcessError:
            fallos.append(f"{f['id']}: {f['commit']} no tiene {f['ruta_original']}")
            continue
        if blob != f["blob_git"]:
            fallos.append(f"{f['id']}: en {f['commit']} el contenido es otro")
    prueba("Cada registro sacado de git coincide con el contenido de su ruta en su commit", len(de_git), fallos)

    # 4. los vigentes: uno por archivo de la rama, y sin cambios
    cabeza = next(c for c in reversed(A.lista_commits("HEAD")) if any(A.linea_de(x["nuevo"]) for x in A.cambios(c["h"])))
    arbol = {r: b for r, b in A.arbol(cabeza["h"]).items() if A.linea_de(r)}
    vig = {f["ruta_original"]: f for f in filas if f["id"].startswith("V-")}
    fallos = [f"falta el registro de {r}" for r in arbol if r not in vig] + [f"sobra {r}" for r in vig if r not in arbol]
    for r, f in vig.items():
        p = raiz / r
        if r in arbol and (f["blob_git"] != arbol[r] or not p.is_file() or blob_git(p.read_bytes()) != arbol[r]):
            fallos.append(f"{f['id']}: {r} no coincide con el commit {cabeza['c']}")
    prueba(f"Cada archivo vigente de la rama (commit {cabeza['c']}) tiene su registro y está en su lugar sin cambios", len(arbol), fallos)

    # 5. toda la historia está ubicada: cada (ruta, contenido) de cada commit tiene registro
    ubicados = {(f["ruta_original"], f["blob_git"]) for f in filas if f["id"][0] in "VHR"}
    historia = set()
    for c in A.lista_commits("HEAD"):
        for x in A.cambios(c["h"]):
            if x["est"] != "D" and A.linea_de(x["nuevo"]):
                historia.add((x["nuevo"], x["bb"]))
    prueba("Cada contenido que tuvo cada ruta en la historia de la rama está en el inventario", len(historia),
           [f"{r} ({b[:7]})" for r, b in sorted(historia - ubicados)])

    # 6. los duplicados apuntan a un archivo con el mismo contenido
    dup = [f for f in filas if f["copia"].startswith("no se copia: duplicado")]
    fallos = []
    for f in dup:
        p = raiz / f["ruta_archivada"]
        if not p.is_file() or blob_git(p.read_bytes()) != f["blob_git"]:
            fallos.append(f"{f['id']}: {f['ruta_archivada']} no tiene el mismo contenido")
    prueba("Cada duplicado que no se copia apunta a un archivo con el mismo contenido", len(dup), fallos)

    # 7. no hay archivos sueltos en versiones/
    registrados = {f["ruta_archivada"] for f in copias}
    sueltos = [p.relative_to(raiz).as_posix() for p in (arch / "versiones").rglob("*")
               if p.is_file() and p.name not in ("ficha.md", "README.md") and p.relative_to(raiz).as_posix() not in registrados]
    # un README.md o una ficha.md que sí es copia de un archivo del proyecto
    en_disco = sum(1 for p in (arch / "versiones").rglob("*") if p.is_file())
    prueba("Cada archivo de versiones/ está en el inventario, o es una ficha o un índice", en_disco, sueltos)

    # 8. cada versión tiene su ficha
    carpetas = [p for p in (arch / "versiones").glob("*/*") if p.is_dir()]
    prueba("Cada carpeta de versión tiene su ficha", len(carpetas), [p.name for p in carpetas if not (p / "ficha.md").is_file()])
    etapas = {f["version_o_etapa"] for f in filas if f["id"][0] in "HDC" or (f["id"][0] == "R" and f["linea"] in ("registros", "tierra"))}
    prueba("Cada versión que nombra el inventario tiene su carpeta", len(etapas),
           sorted(e for e in etapas if not any(p.name == e for p in carpetas)))

    # 9. los enlaces de la guía, los índices y las fichas
    propios = [arch / n for n in ("README.md", "linea_de_tiempo.md", "pendientes.md", "recursos_compartidos/README.md", "versiones/README.md")]
    propios += list((arch / "versiones").glob("*/README.md")) + list((arch / "versiones").glob("*/*/ficha.md"))
    total, fallos = 0, []
    for md in propios:
        for m in re.finditer(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)", md.read_text("utf8")):
            destino = unquote(m.group(1).split("#")[0])
            if not destino or destino.startswith(("http:", "https:", "mailto:")):
                continue
            total += 1
            if not (md.parent / destino).exists() and (md.parent / destino).resolve() != (arch / "verificacion.md").resolve():
                fallos.append(f"{md.relative_to(arch)}: {destino}")
    prueba("Los enlaces de la guía, los índices y las fichas llevan a un archivo que existe", total, fallos)

    # 10. las imágenes que piden las páginas archivadas
    total, fallos, ya_rotas = 0, [], 0
    for f in copias:
        if f["id"][0] != "H":
            continue
        p = raiz / f["ruta_archivada"]
        for r in A.referencias(f["ruta_original"], p.read_bytes()):
            total += 1
            if not (p.parent / r).exists():
                if r in [x for x in A.referencias(f["ruta_original"], p.read_bytes())] and not _existia(f, r):
                    ya_rotas += 1
                else:
                    fallos.append(f"{f['id']}: {r}")
    prueba(f"Las imágenes que piden las páginas archivadas están a su lado ({ya_rotas} rutas ya no existían en su commit: pendientes.md)", total, fallos)

    # 11. los originales, intactos
    estado = [l for l in git("status", "--porcelain").splitlines() if not l[3:].strip('"').startswith(ARCHIVO + "/")]
    prueba("Fuera de archivo_del_proyecto/, la carpeta de trabajo no tiene cambios respecto de la rama", 1, estado)

    # 12. nada de lo que no debe estar
    prohibidos = []
    for p in arch.rglob("*"):
        if p.is_file() and p.suffix.lower() in (".md", ".py", ".json", ".csv", ".txt"):
            t = p.read_text("utf8", errors="ignore")
            if re.search(r"drive\.google\.com|usercontent\.google|hotmail\.com\b(?<!ieb160@hotmail\.com)", t):
                prohibidos.append(p.relative_to(arch).as_posix())
    prueba("Ningún texto del archivo trae el enlace de la carpeta privada del autor ni un correo suyo que no esté ya en el artículo", 1, prohibidos)

    # el informe
    cuenta = Counter(f["id"][0] for f in filas)
    peso = defaultdict(int)
    for f in copias:
        peso[f["id"][0]] += int(f["bytes"])
    mal = [p for p in pruebas if p[2]]
    L = ["# Verificación del archivo", "",
         f"Hecha el {dt.datetime.now(dt.timezone.utc):%d.%m.%Y} con `herramientas/verificar_archivo.py`, sobre el commit `{cabeza['c']}` de la rama del artículo. "
         "Se rehace con la misma orden, desde la raíz del repositorio.", "",
         f"**Resultado: {'todas las comprobaciones pasan' if not mal else str(len(mal)) + ' comprobaciones fallan'}.**", "",
         "| Qué se comprobó | Cuántos | Resultado |", "|---|---|---|"]
    for que, total, fallos in pruebas:
        L.append(f"| {que} | {total} | {'bien' if not fallos else 'FALLA: ' + '; '.join(map(str, fallos[:8])) + (' …' if len(fallos) > 8 else '')} |")
    L += ["", "## El inventario, en números", "", "| Prefijo | Registros | Copiados | Peso copiado |", "|---|---|---|---|"]
    for k in "VHDCRLN":
        n_copias = sum(1 for f in copias if f["id"][0] == k)
        L.append(f"| `{k}-` | {cuenta[k]} | {n_copias} | {peso[k] / 1e6:.1f} MB |".replace(".", ","))
    L += ["", "## Lo que esta verificación no cubre", "",
          "- **Las piezas de la conversación** (`C-`) se comprueban contra `herramientas/conversacion.json`, que guarda su tamaño y su SHA-256 del día en que se copiaron. "
          "Su origen era la carpeta de trabajo de la sesión, que no se conserva.",
          "- **Los canales de Are.na** (`L-`) y **la carpeta de fuentes del autor** no se abrieron: el archivo solo registra lo que dicen de ellos los documentos del proyecto.",
          "- **Que cada Word o PDF anterior se abra bien** no se probó uno por uno: son copias exactas de lo que estaba en git.",
          "- **Los enlaces dentro de los documentos archivados** que llevan a otros documentos (no a imágenes) apuntan a rutas del proyecto, y en una carpeta de versión pueden no resolverse. "
          "El documento vigente o la versión del mismo commit están en el inventario."]
    (arch / "verificacion.md").write_text("\n".join(L) + "\n", "utf8")
    for que, total, fallos in pruebas:
        print(("BIEN  " if not fallos else "FALLA ") + f"{que} [{total}]")
        for x in fallos[:15]:
            print("       ", x)
    sys.exit(1 if mal else 0)


def _existia(f, r):
    """¿Existía en su commit la ruta que pide la página?"""
    import posixpath
    dep = posixpath.normpath(posixpath.join(posixpath.dirname(f["ruta_original"]), r))
    if dep.startswith(".."):
        return False
    return subprocess.run(["git", "cat-file", "-e", f"{f['commit']}:{dep}"], capture_output=True).returncode == 0


if __name__ == "__main__":
    main()
