#!/usr/bin/env python3
"""Verifica tipografia/archivo_del_proyecto/: cada copia es lo que dice el inventario y los originales siguen intactos.

Uso, desde la raíz del repositorio:
    python3 tipografia/archivo_del_proyecto/herramientas/verificar_archivo.py [--conversacion REGISTRO.jsonl]
Con el registro de la conversación, comprueba también que lo que se copió de ella sea lo que quedó escrito ahí.
Escribe archivo_del_proyecto/verificacion.md y sale con código 1 si algo falla.
"""

import argparse
import base64
import csv
import datetime as dt
import hashlib
import json
import posixpath
import re
import subprocess
import sys
from pathlib import Path

ARCHIVO = "tipografia/archivo_del_proyecto"
ANTES = "02dcb14"             # el último commit del proyecto antes del archivo: fuera del archivo, nada cambia respecto de él
COPIAS = ("copia exacta", "copia funcional (dependencia)", "copia de la conversación", "copia reducida (de la conversación)",
          "copia de la versión en línea")
DOCUMENTOS = re.compile(r"^(README\.md|inventario\.csv|pendientes\.md|linea_de_tiempo\.md|verificacion\.md|herramientas/[^/]+\.py|"
                        r"recursos_compartidos/README\.md|versiones/README\.md|versiones/[^/]+/README\.md|versiones/[^/]+/[^/]+/ficha\.md)$")
CORREO = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}")      # ninguna dirección en lo que escribe el archivo
COLAS = re.compile(r"^(Co-Authored-By|Claude-Session):", re.M)            # las colas de los commits no se copian en las fichas


def git(*a, entrada=None):
    return subprocess.run(["git", "-c", "core.quotepath=false", *a], capture_output=True, text=True, input=entrada).stdout


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def blob_git(b):
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def main():
    ap = argparse.ArgumentParser(description="Verifica el archivo del proyecto.")
    ap.add_argument("--conversacion", type=Path)
    args = ap.parse_args()
    raiz = Path(git("rev-parse", "--show-toplevel").strip())
    base = raiz / ARCHIVO
    filas = list(csv.DictReader(open(base / "inventario.csv", encoding="utf-8-sig")))
    por_id = {f["id"]: f for f in filas}
    r = []      # (comprobación, correcto, detalle)

    ids = [f["id"] for f in filas]
    repetidos = sorted({i for i in ids if ids.count(i) > 1})
    r.append(("Números únicos en el inventario", not repetidos, f"{len(filas)} filas" + (f"; repetidos: {repetidos[:5]}" if repetidos else "")))

    # las copias: están, y su contenido es el del inventario
    malas, n = [], 0
    for f in filas:
        if f["copia"] in COPIAS:
            n += 1
            p = raiz / f["ruta_archivada"]
            if not p.is_file():
                malas.append(f"{f['id']}: no está")
                continue
            d = p.read_bytes()
            if sha256(d) != f["sha256"] or str(len(d)) != f["bytes"] or (f["blob_git"] and blob_git(d) != f["blob_git"]):
                malas.append(f"{f['id']}: su contenido no es el del inventario")
    r.append(("Las copias están y tienen el contenido del inventario", not malas, f"{n} archivos: SHA-256, tamaño y hash de git" + (f"; fallan: {malas[:5]}" if malas else "")))

    # las copias de git: el contenido es el de su ruta en su commit
    pedidos = [(f, f"{f['commit']}:{f['ruta_original']}") for f in filas if f["copia"] in ("copia exacta", "copia funcional (dependencia)", "en su lugar (no se copia)")
               and f["commit"] and f["ruta_original"].startswith("tipografia/")]
    salida = git("cat-file", "--batch-check", entrada="\n".join(p for _, p in pedidos) + "\n").splitlines()
    malas = []
    for (f, p), linea in zip(pedidos, salida):
        blob = linea.split()[0] if linea and "missing" not in linea else None
        if blob != f["blob_git"]:
            malas.append(f"{f['id']} ({p})")
    r.append(("Cada copia de git es la de su ruta en su commit", not malas, f"{len(pedidos)} archivos: git cat-file <commit>:<ruta> da el mismo blob" + (f"; fallan: {malas[:5]}" if malas else "")))

    # lo vigente: en su lugar e igual a la cabeza de la rama antes del archivo
    vig = [f for f in filas if f["copia"] == "en su lugar (no se copia)"]
    antes = dict(l.split("\t", 1)[::-1] for l in git("ls-tree", "-r", ANTES, "--format=%(objectname)\t%(path)").splitlines())
    malas = [f["id"] for f in vig if antes.get(f["ruta_original"]) != f["blob_git"] or not (raiz / f["ruta_original"]).is_file()
             or blob_git((raiz / f["ruta_original"]).read_bytes()) != f["blob_git"]]
    faltan = sorted(r_ for r_ in antes if r_.startswith("tipografia/") and not r_.startswith(ARCHIVO + "/")
                    and r_ not in {f["ruta_original"] for f in vig})
    r.append(("Lo vigente está en su lugar, sin cambios", not malas and not faltan,
              f"{len(vig)} archivos iguales a {ANTES}" + (f"; distintos: {malas[:5]}" if malas else "") + (f"; sin registro: {faltan[:5]}" if faltan else "")))

    # lo que está en línea: el contenido es el que informó claude.ai
    en_linea = [f for f in filas if f["copia"] == "copia de la versión en línea"]
    malas, sin = [], []
    for f in en_linea:
        m = re.search(r"SHA-256 informado por claude\.ai al descargarla: ([0-9a-f]{64})", f["observaciones"])
        if not m:
            sin.append(f["id"])
        elif m.group(1) != f["sha256"]:
            malas.append(f["id"])
    r.append(("Lo que está en línea es lo que sirvió claude.ai", not malas,
              f"{len(en_linea) - len(sin)} de {len(en_linea)} con el SHA-256 informado al descargarlas" + (f"; la página v4 sale del registro de la conversación ({', '.join(sin)})" if sin else "") + (f"; fallan: {malas}" if malas else "")))

    # lo que viene de la conversación
    conv = [f for f in filas if f["copia"] == "copia reducida (de la conversación)"
            or (f["copia"] == "copia de la conversación" and not f["ruta_original"].startswith("(sesión) scratchpad/"))]
    if args.conversacion and args.conversacion.exists():
        escritos = set()
        for l in open(args.conversacion, encoding="utf8"):
            e = json.loads(l)
            c = (e.get("message") or {}).get("content")
            if not isinstance(c, list):
                continue
            for b in c:
                if b.get("type") == "tool_use" and b.get("name") == "Write":
                    escritos.add(sha256(b["input"]["content"].encode("utf8")))
                if b.get("type") == "tool_result" and isinstance(b.get("content"), list):
                    for x in b["content"]:
                        if x.get("type") == "image" and (x.get("source") or {}).get("type") == "base64":
                            escritos.add(sha256(base64.b64decode(x["source"]["data"])))
        malas = [f["id"] for f in conv if f["sha256"] not in escritos]
        r.append(("Lo de la conversación es lo que quedó en su registro", not malas, f"{len(conv)} copias encontradas en el registro" + (f"; no están: {malas[:5]}" if malas else "")))
    else:
        r.append(("Lo de la conversación es lo que quedó en su registro", True, f"no se comprobó ahora: hace falta el registro (--conversacion); {len(conv)} copias"))

    # los originales: fuera del archivo, nada cambió
    cambios = [l for l in git("diff", "--name-only", ANTES, "--", ".", f":(exclude){ARCHIVO}").splitlines() if l]
    sueltos = [l[3:] for l in git("status", "--porcelain", "--", ".", f":(exclude){ARCHIVO}").splitlines() if l]
    r.append(("Los originales siguen intactos", not cambios and not sueltos,
              f"fuera de {ARCHIVO}/, nada difiere de {ANTES}" + (f"; cambiados: {cambios[:5]}" if cambios else "") + (f"; sueltos: {sueltos[:5]}" if sueltos else "")))

    # todo lo que hay en el archivo está en el inventario, o es un documento del archivo
    registrados = {f["ruta_archivada"] for f in filas if f["copia"] in COPIAS}
    extra = []
    for p in sorted(base.rglob("*")):
        if p.is_file():
            rel = p.relative_to(raiz).as_posix()
            if rel not in registrados and not DOCUMENTOS.match(p.relative_to(base).as_posix()):
                extra.append(rel)
    r.append(("Todo lo del archivo está en el inventario", not extra, f"{len(registrados)} copias registradas" + (f"; sin registro: {extra[:5]}" if extra else "")))

    # los enlaces: los de los documentos del archivo, todos; de los Markdown archivados, las imágenes que muestran
    (base / "verificacion.md").write_text("# Verificación del archivo\n\nEn curso.\n", encoding="utf8")
    rotos, n, imagenes, info = [], 0, 0, 0
    for doc in sorted(base.rglob("*.md")):
        rel = doc.relative_to(base).as_posix()
        propio = bool(DOCUMENTOS.match(rel))
        texto = doc.read_text(encoding="utf8", errors="ignore")
        for m in re.finditer(r"(!?)\[[^\]]*\]\(\s*<?([^)\s>]+)", texto):
            destino = m.group(2).split("#")[0]
            if not destino or re.match(r"^[a-z]+:", destino):
                continue
            existe = (doc.parent / destino).resolve().exists()
            if propio:
                n += 1
                if not existe:
                    rotos.append(f"{rel} → {destino}")
            elif m.group(1):
                imagenes += 1
                if not existe:
                    rotos.append(f"{rel} → {destino}")
            elif not existe:
                info += 1
    r.append(("Los enlaces internos funcionan", not rotos,
              f"{n} enlaces de los documentos del archivo y {imagenes} imágenes que muestran los Markdown archivados"
              + (f"; rotos: {rotos[:5]}" if rotos else "")
              + f". Además, {info} enlaces comunes de documentos archivados apuntan al proyecto de entonces, fuera de su carpeta: se abren con git (ver README)."))

    # las ausencias y las relaciones
    pend = (base / "pendientes.md").read_text(encoding="utf8")
    sin = [f["id"] for f in filas if f["id"].startswith("N-") and f["categoria"] not in ("compartido con otro proyecto", "residuo técnico") and f["id"] not in pend]
    r.append(("Lo ausente y las dudas están en pendientes.md", not sin, f"{sum(1 for f in filas if f['id'].startswith('N-'))} registros N-" + (f"; falta: {sin}" if sin else "")))
    malas = sorted({i for f in filas for i in re.findall(r"\b[VHDCLN]-\d{3,4}\b", f["relacion"]) if i not in por_id})
    r.append(("Las relaciones nombran filas que existen", not malas, "" if not malas else f"no existen: {malas[:5]}"))

    # nada que no deba estar en lo que escribe el archivo: direcciones de correo, las colas de los commits
    malas = []
    escritos = [base / f["ruta_archivada"][len(ARCHIVO) + 1:] for f in filas
                if f["copia"] in ("copia de la conversación", "copia de la versión en línea")]
    propios = [p for p in base.rglob("*") if p.is_file() and DOCUMENTOS.match(p.relative_to(base).as_posix())
               and not p.relative_to(base).as_posix().startswith("herramientas/")]
    for p in propios + escritos:
        if p.suffix.lower() in (".md", ".csv", ".html", ".js", ".py", ".css", ".txt"):
            t = p.read_text(encoding="utf8", errors="ignore")
            if CORREO.search(t) or (p in propios and COLAS.search(t)):
                malas.append(p.relative_to(base).as_posix())
    r.append(("Sin direcciones de correo ni colas de commit en lo que escribe el archivo", not malas,
              f"{len(propios)} documentos del archivo y {len(escritos)} copias de la conversación y en línea" + (f"; aparecen en: {malas[:5]}" if malas else "")))

    ok = all(x[1] for x in r)
    cabeza = git("rev-parse", "--short", "HEAD").strip()
    L = ["# Verificación del archivo", "",
         f"Se corrió el {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC sobre el commit `{cabeza}` (con lo que hubiera sin commit), "
         "con `herramientas/verificar_archivo.py`" + (" y el registro de la conversación." if args.conversacion else "."), "",
         f"**Resultado: {'todo correcto' if ok else 'hay fallas'}.**", "",
         "| Comprobación | Resultado | Detalle |", "|---|---|---|"]
    for nombre, bien, det in r:
        L.append(f"| {nombre} | {'correcto' if bien else 'FALLA'} | {det} |")
    L += ["", "[Volver al índice](README.md)."]
    (base / "verificacion.md").write_text("\n".join(L) + "\n", encoding="utf8")
    for nombre, bien, det in r:
        print(("ok    " if bien else "FALLA ") + nombre + ": " + det)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
