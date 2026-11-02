#!/usr/bin/env python3
"""Arma tipografia/archivo_del_proyecto/: el archivo del desarrollo de Contenida.

Saca de git cada versión anterior de cada archivo del proyecto y la deja en versiones/<línea>/<versión>/, con su
ruta original debajo de tipografia/ y las dependencias que necesita para abrirse. Suma lo que quedó registrado en
la conversación (escrituras, vistas de prueba, pruebas) y en línea (los artefactos de claude.ai). Escribe el
inventario, las fichas, la línea de tiempo, los pendientes y la guía. Los originales no se tocan.

Se corrió una vez, en la sesión donde se hizo el proyecto, desde la raíz del repositorio y en su rama:
    python3 armar_archivo.py --conversacion REGISTRO.jsonl --scratch CARPETA --artefactos CARPETA
La parte de git se puede rehacer en cualquier copia del repositorio; la de la conversación necesita su registro,
que no está en el repositorio. Para comprobar el archivo ya armado: verificar_archivo.py.
"""

import argparse
import base64
import csv
import datetime as dt
import functools
import hashlib
import html
import json
import posixpath
import re
import shutil
import struct
import subprocess
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

RAMA = "claude/fervent-lovelace-exgqzl"
BASE = "1128c3f"                      # el último commit del artículo antes de Contenida: la rama del proyecto sale de él
PROYECTO = "tipografia/"
ARCHIVO = "tipografia/archivo_del_proyecto"
UTC = dt.timezone.utc

LINEAS = {   # el orden es el del índice
    "documentos": ("Los documentos", "Los documentos 01 a 10, el README de tipografia/ e inventario.py: la obra, las tesis, el sistema, la anatomía, la gramática, el taller, lo digital, la ética, Posnansky, los nombres, el manuaje y las imágenes de dominio público."),
    "textos": ("Los textos de partida", "El poema, el pie de la lámina y el inventario de letras halladas y por reconstruir."),
    "esquemas": ("Los esquemas", "La caja, la pauta de calco, la ficha de hallazgo, la cadena de estados, los montajes y las plantillas imprimibles."),
    "simulacion": ("La simulación del taller", "La propuesta de la máquina: los testigos del pie, la gramática en Python y los estados simulados, con sus salidas."),
    "laminas": ("Las láminas de exposición", "Las láminas 4:3: sus fuentes HTML, las imágenes, las exportaciones en PNG y el PDF."),
    "aplicacion": ("La aplicación de las decisiones de la letra", "La gramática en el navegador: de la aplicación de cuatro vistas a la de los planos de detalle."),
    "informe": ("El informe de decisiones", "El informe en Word y PDF, con seis mapas, y su generador."),
    "digital": ("La póliza en OpenType", "Lo digital: el generador de la póliza."),
    "planos": ("Los planos de la anatomía base", "Once planos A3 con cotas, niveles, cortes y detalles, en SVG, PNG, DXF y PDF."),
    "taxonomia": ("La taxonomía de las referencias", "Las láminas de la taxonomía y el atlas de imágenes de dominio público."),
    "repujado": ("El ensayo del repujado", "La mesa del repujado: la placa de aluminio, el punzón y la mano simulada."),
    "editorial": ("El libro de Contenida", "El documento editorial único, compuesto con Vivliostyle: el libro para pantalla e imprenta y la cubierta."),
}

ESTADOS = ("versión anterior", "alternativa", "prueba o experimento", "versión vigente", "entregable aprobado",
           "material descartado", "estado sin confirmar")

# Por qué se retiró algo, cuando lo dice el mensaje del commit que lo retiró.
RETIROS = {
    "845851c": ("material descartado", "«Quita Are.na del proyecto Contenida. Borra 10_arena.md…» (mensaje del commit 845851c)."),
    "e5cca9f": ("material descartado", "«Se sacan los simuladores de los estados» (mensaje del commit e5cca9f)."),
    "bbeb653": ("material descartado", "«Fuera de la simulación: piel, caja, hectógrafo, azulejo y estrofa» (mensaje del commit bbeb653)."),
    "deb0435": ("material descartado", "«Saca un __pycache__ del repositorio y lo ignora» (mensaje del commit deb0435)."),
    "7f57d95": ("versión anterior", "El juego de láminas se rehízo: «Diecisiete láminas…» (mensaje del commit 7f57d95). No consta una correspondencia una a una con las nuevas."),
    "3f66520": ("estado sin confirmar", "«Piel, copia y azulejo quedan en pausa, con sus acciones escritas en 04» (mensaje del commit 3f66520). Si lo retirado es eso o algo más, el mensaje no lo precisa."),
}

GENERADORES = [   # (patrón de la ruta, generador); «deducido» cuando no lo dice el propio generador o su README
    (r"^tipografia/textos/inventario\.md$", "tipografia/inventario.py"),
    (r"^tipografia/esquemas/caja\.json$", "tipografia/inventario.py"),
    (r"^tipografia/esquemas/.+\.(svg|png|pdf)$", "tipografia/esquemas/generar_esquemas.py"),
    (r"^tipografia/simulacion/testigos/", "tipografia/simulacion/extraer_testigos.py, desde una foto del pie que no está en el repositorio"),
    (r"^tipografia/simulacion/salida/", "tipografia/simulacion/simular.py y sus módulos"),
    (r"^tipografia/laminas/(html|png)/|^tipografia/laminas/contenida_laminas\.pdf$", "tipografia/laminas/generar_laminas.py"),
    (r"^tipografia/laminas/img/", "tipografia/laminas/imagenes.py (deducido)"),
    (r"^tipografia/aplicacion/datos\.js$", "tipografia/aplicacion/exportar.py"),
    (r"^tipografia/informe/contenida_informe_de_decisiones\.docx$", "tipografia/informe/informe.js, llamado por armar.py"),
    (r"^tipografia/informe/contenida_informe_de_decisiones\.pdf$", "tipografia/informe/armar.py (LibreOffice, desde el .docx)"),
    (r"^tipografia/informe/paginas\.json$", "tipografia/informe/armar.py"),
    (r"^tipografia/informe/mapas/", "tipografia/informe/mapas.py (con mano.py y materia.py)"),
    (r"^tipografia/informe/img/aplicacion\.png$", "captura de tipografia/aplicacion/ en un navegador sin pantalla"),
    (r"^tipografia/planos/(svg|png|dxf)/|^tipografia/planos/contenida_planos\.pdf$", "tipografia/planos/generar_planos.py"),
    (r"^tipografia/taxonomia/(svg|png)/|^tipografia/taxonomia/contenida_taxonomia\.pdf$", "tipografia/taxonomia/generar_taxonomia.py"),
    (r"^tipografia/repujado/muestras/", "la mesa de tipografia/repujado/ (repujado.js y pulso.js) (deducido)"),
    (r"^tipografia/editorial/imagenes/placa_", "tipografia/editorial/placas_de_cerca.py"),
    (r"^tipografia/editorial/(contenida_.+\.pdf|imagenes\.md|muestras/)", "tipografia/editorial/armar.py (con libro.py, planas.py, cubierta.py y estilo.css)"),
]

COLUMNAS = ["id", "nombre", "descripcion", "categoria", "linea", "version_o_etapa", "estado", "formato", "copia",
            "ruta_original", "ruta_archivada", "rama", "commit", "fecha", "que_representa_la_fecha", "en_versiones",
            "relacion", "fuente_o_generador", "sha256", "bytes", "blob_git", "observaciones"]

QUE_FECHA = {
    "git": "fecha del commit (UTC) en que este contenido entra en git; no es la fecha de creación de la obra ni, necesariamente, la del archivo",
    "escritura": "momento (UTC) en que se escribió en la conversación",
    "imagen": "momento (UTC) en que la conversación vio la imagen",
    "scratch": "última modificación del archivo en el contenedor de la sesión (UTC)",
    "en_linea": "publicación de esa versión del artefacto (UTC), deducida de su identificador de versión",
}


# ---------------------------------------------------------------------------------------------------------------- git
def git(*args, binario=False):
    r = subprocess.run(["git", "-c", "core.quotepath=false", *args], capture_output=True, check=True)
    return r.stdout if binario else r.stdout.decode("utf8")


@functools.lru_cache(None)
def arbol(commit):
    d = {}
    for ent in git("ls-tree", "-r", "-z", commit, binario=True).decode("utf8").split("\0"):
        if ent:
            meta, ruta = ent.split("\t", 1)
            _, tipo, blob = meta.split()
            if tipo == "blob":
                d[ruta] = blob
    return d


@functools.lru_cache(None)
def contenido(blob):
    return git("cat-file", "blob", blob, binario=True)


def cambios(commit):
    partes = git("diff-tree", "-r", "-z", "--no-commit-id", "-M", "--root", commit, binario=True).decode("utf8").split("\0")
    res, i = [], 0
    while i < len(partes):
        meta = partes[i]
        i += 1
        if not meta.startswith(":"):
            continue
        _, _, ba, bb, est = meta[1:].split(" ")
        if est[0] in "RC":
            viejo, nuevo = partes[i], partes[i + 1]
            i += 2
        else:
            viejo = nuevo = partes[i]
            i += 1
        res.append({"est": est[0], "viejo": viejo, "nuevo": nuevo, "ba": ba, "bb": bb})
    return res


def commits():
    salida = git("log", "--reverse", "--format=%H%x1f%aI%x1f%s%x1f%b%x1e", f"{BASE}..{RAMA}")
    lista = []
    for reg in salida.split("\x1e"):
        reg = reg.strip("\n")
        if not reg:
            continue
        h, fecha, asunto, cuerpo = reg.split("\x1f")
        cuerpo = "\n".join(l for l in cuerpo.strip().splitlines()
                           if not l.startswith(("Co-Authored-By:", "Claude-Session:"))).strip()
        lista.append({"h": h, "c": h[:7], "fecha": dt.datetime.fromisoformat(fecha).astimezone(UTC),
                      "asunto": asunto, "cuerpo": cuerpo})
    return lista


# ---------------------------------------------------------------------------------------------------------------- utilidades
def sha256(b):
    return hashlib.sha256(b).hexdigest()


def blob_git(b):
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def slug(t, largo=40):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    palabras, out = re.findall(r"[a-z0-9]+", t), ""
    for p in palabras:
        if len(out) + len(p) + 1 > largo:
            break
        out = f"{out}-{p}" if out else p
    return out


def fecha_txt(f):
    return f.strftime("%Y-%m-%d %H:%M") + " UTC"


def linea_de(ruta):
    if not ruta.startswith(PROYECTO) or ruta.startswith(ARCHIVO + "/"):
        return None
    partes = ruta.split("/")
    return "documentos" if len(partes) == 2 else partes[1]


def bajo_tipografia(ruta):
    return ruta[len(PROYECTO):] if ruta.startswith(PROYECTO) else ruta


def formato(ruta):
    ext = posixpath.splitext(ruta)[1].lower().lstrip(".")
    return ext.upper() if ext else "—"


def categoria(ruta):
    n, ext = ruta.lower(), posixpath.splitext(ruta.lower())[1]
    base = posixpath.basename(n)
    if ext in (".woff2", ".ttf", ".otf"):
        return "recurso: fuente tipográfica"
    if base.startswith("license"):
        return "recurso: licencia"
    if base == "clipper.js":
        return "recurso: biblioteca de terceros"
    if base in ("package.json", "package-lock.json"):
        return "dependencias"
    if "/testigos/" in n:
        return "datos: recortes del pie"
    if ext in (".md", ".txt"):
        return "documento"
    if ext == ".py":
        return "generador o código"
    if ext == ".js":
        return "aplicación" if ("/aplicacion/" in n or "/repujado/" in n) and base not in ("exportar.py",) else "generador o código"
    if ext in (".html", ".htm"):
        return "fuente editable" if "/laminas/html/" in n else "aplicación"
    if ext == ".css":
        return "fuente editable"
    if ext in (".json", ".csv"):
        return "datos"
    if ext in (".pdf", ".docx", ".dxf", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"):
        return "resultado exportado"
    return "otro"


def generador(ruta):
    for patron, gen in GENERADORES:
        if re.search(patron, ruta):
            return gen
    if categoria(ruta) in ("documento",) and not ruta.endswith(("inventario.md",)):
        return "redactado (sin generador)"
    return ""


def descripcion(ruta, datos):
    base, ext = posixpath.basename(ruta), posixpath.splitext(ruta)[1].lower()
    texto = None
    if ext in (".md", ".py", ".js", ".css", ".html", ".htm", ".svg", ".txt"):
        try:
            texto = datos.decode("utf8")
        except UnicodeDecodeError:
            texto = None
    t = None
    if texto is not None:
        if ext == ".md":
            m = re.search(r"^#\s+(.+)$", texto, re.M)
            t = m and m.group(1)
        elif ext == ".py":
            m = re.search(r'^(?:#.*\n|\s*\n)*[rRuUbB]*("""|\'\'\')\s*(.+?)\s*(?:\n|\1)', texto)
            t = m and m.group(2)
        elif ext in (".js", ".css"):
            m = re.search(r"/\*+\s*(.+?)\s*(?:\n|\*/)", texto) or re.search(r"^//\s*(.+)$", texto, re.M)
            t = m and m.group(1)
        elif ext in (".html", ".htm", ".svg"):
            m = re.search(r"<title>(.*?)</title>", texto, re.S) or re.search(r"<h1[^>]*>(.*?)</h1>", texto, re.S)
            t = m and html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
        elif ext == ".txt":
            t = texto.strip().splitlines()[0] if texto.strip() else None
    if not t:
        m = re.match(r"(\d{3})\.png$", base)
        if "/testigos/" in ruta and m:
            t = f"Testigo {m.group(1)}: una letra del pie, recortada y enderezada"
        elif "/simulacion/salida/" in ruta:
            t = f"Salida de la simulación: {base}"
        elif "/laminas/png/" in ruta:
            t = f"Lámina exportada: {base}"
        elif "/laminas/img/" in ruta:
            t = f"Imagen para las láminas: {base}"
        elif ruta.endswith("contenida_informe_de_decisiones.docx"):
            t = "El informe de decisiones, en Word"
        elif ruta.endswith("contenida_informe_de_decisiones.pdf"):
            t = "El informe de decisiones, en PDF"
        elif "/informe/mapas/" in ruta:
            t = f"Mapa del informe: {base}"
        elif "/planos/" in ruta:
            t = f"Plano: {base}"
        elif "/taxonomia/" in ruta:
            t = f"Taxonomía: {base}"
        elif "/esquemas/" in ruta:
            t = f"Esquema: {base}"
        elif "/fuentes/" in ruta:
            t = f"Fuente tipográfica o su licencia: {base}"
        elif "/editorial/" in ruta:
            t = {"contenida_libro.pdf": "El libro, para pantalla", "contenida_libro_imprenta.pdf": "El libro, para la imprenta",
                 "contenida_cubierta_imprenta.pdf": "La cubierta, para la imprenta"}.get(base, f"Libro: {base}")
        elif "/repujado/muestras/" in ruta:
            t = f"Muestra de la mesa del repujado: {base}"
        else:
            t = base
    t = re.sub(r"\s*\(?[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}\)?", "", t)    # sin direcciones de correo
    t = re.sub(r"\s+", " ", t).strip()
    return t[:160]


def medidas_imagen(b):
    """Ancho y alto de un PNG o un JPEG, sin bibliotecas."""
    if b[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", b[16:24])
    if b[:2] == b"\xff\xd8":
        i = 2
        while i < len(b) - 9:
            if b[i] != 0xFF:
                i += 1
                continue
            m = b[i + 1]
            if m in (0xC0, 0xC1, 0xC2):
                h, w = struct.unpack(">HH", b[i + 5:i + 9])
                return w, h
            i += 2 + struct.unpack(">H", b[i + 2:i + 4])[0]
    return None


REF = re.compile(r"""(?:\bsrc|\bhref|xlink:href)\s*=\s*["']([^"']+)["']|url\(\s*["']?([^"')]+)["']?\s*\)""")


IMAGEN_MD = re.compile(r"""!\[[^\]]*\]\(\s*<?([^)\s>]+)|<img[^>]+src\s*=\s*["']([^"']+)["']""")


def referencias(texto, md=False):
    for m in (IMAGEN_MD if md else REF).finditer(texto):
        r = (m.group(1) or m.group(2) or "").strip()
        if not r or r.startswith(("http:", "https:", "data:", "mailto:", "//", "#", "javascript:", "about:", "blob:")):
            continue
        r = html.unescape(r.split("#")[0].split("?")[0])
        if r:
            yield r


# ---------------------------------------------------------------------------------------------------------------- el archivo
class Archivo:
    def __init__(self, raiz, destino):
        self.raiz, self.destino = raiz, destino
        self.filas = []
        self.versiones = []                 # por línea, en orden
        self.archivados = {}                # (ruta, blob) -> fila H
        self.vigentes = {}                  # ruta -> fila V
        self.por_contenido = defaultdict(list)   # sha256 -> filas copiadas (para los duplicados)
        self.notas = []

    # -- filas
    def fila(self, **k):
        f = {c: "" for c in COLUMNAS}
        f.update({c: ("" if v is None else v) for c, v in k.items()})
        self.filas.append(f)
        return f

    def copiar(self, datos, destino_rel):
        p = self.destino / destino_rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(datos)
        return str(Path(ARCHIVO) / destino_rel)

    # -- versiones de git
    def desde_git(self):
        self.cambios = {}
        self.commits = []
        for c in commits():                     # los commits que solo tocan este archivo no son historia del proyecto
            cs = cambios(c["h"])
            if any(not x["nuevo"].startswith(ARCHIVO + "/") for x in cs):
                self.cambios[c["h"]] = cs
                self.commits.append(c)
        self.cabeza = self.commits[-1]
        self.VIG = {r: b for r, b in arbol(self.cabeza["h"]).items() if linea_de(r)}
        self.indice = {c["c"]: i for i, c in enumerate(self.commits)}
        eventos = defaultdict(list)            # ruta -> [(i, est, blob o None, otra ruta)]
        primera = {}                           # (ruta, blob) -> commit donde aparece
        compartidos = []
        for i, c in enumerate(self.commits):
            por_linea = defaultdict(list)
            for x in self.cambios[c["h"]]:
                l = linea_de(x["nuevo"]) or linea_de(x["viejo"])
                if x["est"] == "R":
                    eventos[x["viejo"]].append((i, "R", None, x["nuevo"]))
                    eventos[x["nuevo"]].append((i, "A", x["bb"], x["viejo"]))
                elif x["est"] == "D":
                    eventos[x["viejo"]].append((i, "D", None, None))
                else:
                    eventos[x["nuevo"]].append((i, x["est"], x["bb"], None))
                if x["est"] != "D":
                    primera.setdefault((x["nuevo"], x["bb"]), c)
                if l:
                    por_linea[l].append(x)
                elif x["nuevo"] in ("README.md", ".gitignore") and x["est"] != "D":
                    compartidos.append((c, x))
            for l in sorted(por_linea, key=list(LINEAS).index):
                self.version_git(l, c, por_linea[l])
        self.eventos, self.primera = eventos, primera
        self.estados_historicos()
        self.vigentes_en_su_lugar()
        self.composicion()
        self.compartidos_con_el_articulo(compartidos)

    def version_git(self, l, c, xs):
        carpeta = f"{c['fecha']:%Y-%m-%d_%H%M}_{c['c']}_{slug(c['asunto'])}"
        v = {"linea": l, "carpeta": carpeta, "origen": "git", "commit": c, "fecha": c["fecha"], "asunto": c["asunto"],
             "cuerpo": c["cuerpo"], "aqui": [], "dependencias": [], "vigentes": [], "repetidos": [], "retirados": [],
             "renombrados": [], "anadidos": [], "modificados": [], "residuos": [], "rotos": []}
        for x in xs:
            if x["est"] == "D":
                v["retirados"].append(x["viejo"])
                continue
            if x["est"] == "R":
                v["renombrados"].append((x["viejo"], x["nuevo"]))
            elif x["est"] in "AC":
                v["anadidos"].append(x["nuevo"])
            else:
                v["modificados"].append(x["nuevo"])
            ruta, blob = x["nuevo"], x["bb"]
            if "/__pycache__/" in ruta or ruta.endswith(".pyc"):
                v["residuos"].append(ruta)
                self.fila(id="", nombre=posixpath.basename(ruta), descripcion="Caché de Python compilada, subida por error",
                          categoria="residuo técnico", linea=l, version_o_etapa=carpeta, estado="material descartado",
                          formato=formato(ruta), copia="no se copia", ruta_original=ruta, rama=RAMA, commit=c["c"],
                          fecha=fecha_txt(c["fecha"]), que_representa_la_fecha=QUE_FECHA["git"], blob_git=blob,
                          fuente_o_generador="Python, al importar exportar.py", relacion="se borró en deb0435",
                          observaciones="No es material del proyecto. Se recupera con: git show " + c["c"] + ":" + ruta)
                continue
            if self.VIG.get(ruta) == blob:
                v["vigentes"].append(ruta)
                continue
            if (ruta, blob) in self.archivados:
                v["repetidos"].append((ruta, self.archivados[(ruta, blob)]))
                continue
            datos = contenido(blob)
            dest = self.copiar(datos, f"versiones/{l}/{carpeta}/{bajo_tipografia(ruta)}")
            f = self.fila(id="", nombre=posixpath.basename(ruta), descripcion=descripcion(ruta, datos), categoria=categoria(ruta),
                          linea=l, version_o_etapa=carpeta, estado="", formato=formato(ruta), copia="copia exacta",
                          ruta_original=ruta, ruta_archivada=dest, rama=RAMA, commit=c["c"], fecha=fecha_txt(c["fecha"]),
                          que_representa_la_fecha=QUE_FECHA["git"], fuente_o_generador=generador(ruta), sha256=sha256(datos),
                          bytes=len(datos), blob_git=blob)
            f["_versiones"] = set()
            self.archivados[(ruta, blob)] = f
            v["aqui"].append(f)
        self.dependencias_de(v, arbol(c["h"]))
        self.versiones.append(v)

    def dependencias_de(self, v, arbol_ref, presentes=None):
        """Lo que piden los HTML, CSS y SVG de la carpeta (imágenes, hojas de estilo, letras, guiones) y las imágenes que
        muestran sus Markdown, copiado al lado. Los enlaces comunes de los Markdown no se copian: apuntan al proyecto de entonces."""
        presentes = presentes if presentes is not None else {f["ruta_original"]: f for f in v["aqui"]}
        cola = [r for r in presentes if posixpath.splitext(r)[1].lower() in (".html", ".htm", ".css", ".svg", ".md")]
        while cola:
            ruta = cola.pop()
            f = presentes[ruta]
            datos = (self.destino / Path(f["ruta_archivada"]).relative_to(ARCHIVO)).read_bytes()
            faltan, resueltos = [], set()
            for ref in referencias(datos.decode("utf8", "ignore"), md=ruta.lower().endswith(".md")):
                objetivo = posixpath.normpath(posixpath.join(posixpath.dirname(ruta), ref))
                if objetivo in presentes:
                    resueltos.add(posixpath.basename(objetivo))
                    continue
                if not objetivo.startswith(PROYECTO):
                    continue
                blob = arbol_ref.get(objetivo)
                if blob is None:
                    faltan.append(ref)
                    continue
                resueltos.add(posixpath.basename(objetivo))
                datos_d = contenido(blob)
                dest = self.copiar(datos_d, f"versiones/{v['linea']}/{v['carpeta']}/{bajo_tipografia(objetivo)}")
                d = self.fila(id="", nombre=posixpath.basename(objetivo), descripcion=descripcion(objetivo, datos_d),
                              categoria=categoria(objetivo), linea=linea_de(objetivo) or v["linea"], version_o_etapa=v["carpeta"],
                              estado="", formato=formato(objetivo), copia="copia funcional (dependencia)", ruta_original=objetivo,
                              ruta_archivada=dest, rama=RAMA, commit=v["commit"]["c"] if v.get("commit") else "",
                              fecha="", que_representa_la_fecha="", fuente_o_generador=generador(objetivo),
                              sha256=sha256(datos_d), bytes=len(datos_d), blob_git=blob)
                d["_original"] = (objetivo, blob)
                d["_requerida_por"] = ruta
                t = self.titular(objetivo, blob) if self.vigentes else None
                if t is not None:
                    d.update(estado=t["estado"], fecha=t["fecha"], que_representa_la_fecha=t["que_representa_la_fecha"])
                    d["_titular"] = t
                presentes[objetivo] = d
                v["dependencias"].append(d)
                if posixpath.splitext(objetivo)[1].lower() in (".html", ".htm", ".css", ".svg"):
                    cola.append(objetivo)
            v["rotos"] += [(ruta, ref) for ref in faltan if posixpath.basename(ref) not in resueltos]   # una ruta alternativa no es un enlace roto

    def estados_historicos(self):
        """Estado de cada versión anterior: si su ruta sigue, la reemplazó otra; si no, cómo salió."""
        for (ruta, blob), f in self.archivados.items():
            ev = self.eventos[ruta]
            i0 = self.indice[f["commit"]]
            despues = [e for e in ev if e[0] > i0]
            if ruta in self.VIG:
                f["estado"] = "versión anterior"
                sig = next((e for e in despues if e[1] in "AMT"), None)
                f["relacion"] = f"versión anterior de {ruta}" + (f"; la reemplaza el commit {self.commits[sig[0]]['c']}" if sig else "")
                continue
            sal = next((e for e in despues if e[1] in "RD"), None) or next((e for e in reversed(ev) if e[1] in "RD"), None)
            if sal and sal[1] == "R":
                f["estado"] = "versión anterior"
                f["relacion"] = f"renombrada a {sal[3]} en {self.commits[sal[0]]['c']}"
            elif sal:
                c = self.commits[sal[0]]["c"]
                estado, por_que = RETIROS.get(c, ("estado sin confirmar", f"Se retiró en {c}; el mensaje del commit no dice por qué."))
                sig = next((e for e in despues if e[1] in "AMT" and e[0] < sal[0]), None)
                f["estado"] = estado if not sig else "versión anterior"
                f["relacion"] = (f"la reemplaza el commit {self.commits[sig[0]]['c']}; " if sig else "") + f"la ruta se retiró en {c}"
                f["observaciones"] = por_que
            else:
                f["estado"] = "estado sin confirmar"
                f["observaciones"] = "No se encontró cómo salió esta ruta."

    def vigentes_en_su_lugar(self):
        for ruta, blob in sorted(self.VIG.items()):
            datos = contenido(blob)
            c = self.primera.get((ruta, blob))
            f = self.fila(id="", nombre=posixpath.basename(ruta), descripcion=descripcion(ruta, datos), categoria=categoria(ruta),
                          linea=linea_de(ruta), version_o_etapa=f"vigente ({self.cabeza['c']})", estado="versión vigente",
                          formato=formato(ruta), copia="en su lugar (no se copia)", ruta_original=ruta, ruta_archivada=ruta,
                          rama=RAMA, commit=c["c"] if c else "", fecha=fecha_txt(c["fecha"]) if c else "",
                          que_representa_la_fecha=QUE_FECHA["git"], fuente_o_generador=generador(ruta), sha256=sha256(datos),
                          bytes=len(datos), blob_git=blob,
                          observaciones="Estado actual de la rama: no consta una aprobación.")
            f["_versiones"] = set()
            self.vigentes[ruta] = f

    def titular(self, ruta, blob):
        if self.VIG.get(ruta) == blob:
            return self.vigentes[ruta]
        return self.archivados.get((ruta, blob))

    def composicion(self):
        for v in self.versiones:
            estado = {r: b for r, b in arbol(v["commit"]["h"]).items() if linea_de(r) == v["linea"]}
            cuenta = {"aqui": 0, "antes": 0, "vigente": 0, "otro": 0}
            ids_aqui = {id(f) for f in v["aqui"]}
            for r, b in estado.items():
                t = self.titular(r, b)
                if t is None:
                    cuenta["otro"] += 1
                    continue
                t["_versiones"].add(v["commit"]["c"])
                if id(t) in ids_aqui:
                    cuenta["aqui"] += 1
                elif t["estado"] == "versión vigente":
                    cuenta["vigente"] += 1
                else:
                    cuenta["antes"] += 1
            v["cuenta"], v["total"] = cuenta, len(estado)
        for v in self.versiones:
            for d in v["dependencias"]:
                t = self.titular(*d["_original"])
                d["estado"] = "versión vigente" if t and t["estado"] == "versión vigente" else (t["estado"] if t else "estado sin confirmar")
                d["_titular"] = t
                d["fecha"], d["que_representa_la_fecha"] = (t["fecha"], t["que_representa_la_fecha"]) if t else ("", "")

    def compartidos_con_el_articulo(self, compartidos):
        for c, x in compartidos:
            self.fila(id="", nombre=x["nuevo"], descripcion="Archivo de la raíz del repositorio, compartido con el artículo Altiplano",
                      categoria="compartido con otro proyecto", linea="(raíz del repositorio)", version_o_etapa=c["c"],
                      estado="versión vigente" if self.cabeza and arbol(self.cabeza["h"]).get(x["nuevo"]) == x["bb"] else "versión anterior",
                      formato=formato(x["nuevo"]), copia="no se copia", ruta_original=x["nuevo"], rama=RAMA, commit=c["c"],
                      fecha=fecha_txt(c["fecha"]), que_representa_la_fecha=QUE_FECHA["git"], blob_git=x["bb"],
                      relacion="cambió con el commit de Contenida " + c["c"] + ": " + c["asunto"],
                      observaciones="Mezcla los dos proyectos; no se copia para no mezclarlos. Se recupera con: git show "
                                    + c["c"] + ":" + x["nuevo"])

    # -- la conversación y lo que está en línea
    def leer_registro(self, ruta_registro):
        """Del registro de la conversación: las escrituras de archivos, las imágenes que se vieron y la página v4."""
        escrituras, imagenes, lecturas = [], [], {}
        self.v4, self.informados = None, {}
        for linea in open(ruta_registro, encoding="utf8"):
            e = json.loads(linea)
            c = (e.get("message") or {}).get("content")
            if not isinstance(c, list) or not e.get("timestamp"):
                continue
            ts = dt.datetime.fromisoformat(e["timestamp"].replace("Z", "+00:00"))
            for b in c:
                if b.get("type") == "tool_use" and b.get("name") == "Write":
                    escrituras.append({"ts": ts, "ruta": b["input"]["file_path"], "datos": b["input"]["content"].encode("utf8")})
                elif b.get("type") == "tool_use" and b.get("name") == "Read":
                    lecturas[b["id"]] = b["input"].get("file_path", "")
                elif b.get("type") == "tool_result":
                    cont = b.get("content")
                    if isinstance(cont, list):
                        for x in cont:
                            if x.get("type") == "image" and (x.get("source") or {}).get("type") == "base64":
                                imagenes.append({"ts": ts, "ruta": lecturas.get(b.get("tool_use_id"), ""),
                                                 "tipo": x["source"]["media_type"], "datos": base64.b64decode(x["source"]["data"])})
                    texto = cont if isinstance(cont, str) else "".join(x.get("text", "") for x in (cont or []) if x.get("type") == "text")
                    for m in re.finditer(r'File saved: "([^"]+)" \((\d+) bytes, "[^"]*", sha256 ([0-9a-f]{64})\)', texto or ""):
                        self.informados[m.group(1)] = m.group(3)
                    m = re.search(r'Files saved under "([^"]+)"', texto or "")
                    if m:
                        for x in re.finditer(r'- "([^"]+)" saved \((\d+) bytes, "[^"]*", sha256 ([0-9a-f]{64})', texto):
                            self.informados[f"{m.group(1)}/{x.group(1)}"] = x.group(3)
                    m = re.search(r"<cowritten-artifact-html>\n(.*?)\n</cowritten-artifact-html>", texto or "", re.S)
                    if m and "version 1792250851-c8e8" in texto:
                        self.v4 = {"ts": ts, "datos": m.group(1).encode("utf8")}
        return escrituras, imagenes

    def duplicado_de(self, datos):
        h = sha256(datos)
        for f in self.filas:
            if f.get("sha256") == h and f["copia"] in ("copia exacta", "en su lugar (no se copia)", "copia de la conversación",
                                                        "copia reducida (de la conversación)", "copia de la versión en línea"):
                return f
        return None

    def version_extra(self, linea, fecha, origen, nombre, estado, resumen, respaldo, deduccion):
        carpeta = f"{fecha:%Y-%m-%d_%H%M}_{origen}_{slug(nombre, 48)}"
        v = {"linea": linea, "carpeta": carpeta, "origen": origen, "fecha": fecha, "asunto": nombre, "estado": estado,
             "resumen": resumen, "respaldo": respaldo, "deduccion": deduccion, "aqui": [], "dependencias": [],
             "registrados": [], "rotos": []}
        self.versiones.append(v)
        return v

    def poner(self, v, datos, rel, *, ruta_original, descripcion_, categoria_, estado, copia, fecha, que_fecha, relacion="",
              generador_="", observaciones="", id_prefijo="C", fuente=None):
        if fuente is not None and str(fuente) in getattr(self, "informados", {}):
            observaciones = (observaciones + " " if observaciones else "") + f"SHA-256 informado por claude.ai al descargarla: {self.informados[str(fuente)]}."
        dup = self.duplicado_de(datos)
        comun = dict(id="", nombre=posixpath.basename(rel), descripcion=descripcion_, categoria=categoria_, linea=v["linea"],
                     version_o_etapa=v["carpeta"], estado=estado, formato=formato(rel), ruta_original=ruta_original,
                     rama="", commit="", fecha=fecha_txt(fecha), que_representa_la_fecha=que_fecha,
                     fuente_o_generador=generador_, sha256=sha256(datos), bytes=len(datos), blob_git=blob_git(datos))
        if dup is not None and dup["copia"] != "copia funcional (dependencia)":
            f = self.fila(**comun, copia="no se copia (duplicado exacto)", ruta_archivada=dup["ruta_archivada"],
                          relacion=(relacion + "; " if relacion else "") + "duplicado exacto de " + "@" + str(id(dup)),
                          observaciones=observaciones)
            f["_dup"] = dup
        else:
            dest = self.copiar(datos, f"versiones/{v['linea']}/{v['carpeta']}/{rel}")
            f = self.fila(**comun, copia=copia, ruta_archivada=dest, relacion=relacion, observaciones=observaciones)
        f["_prefijo"] = id_prefijo
        v["aqui"].append(f)
        return f

    def conversacion(self, registro, scratch, artefactos):
        escrituras, imagenes = self.leer_registro(registro)
        antes_02dcb14 = arbol(git("rev-parse", "02dcb14~1").strip())

        def escrita(sufijo, minuto):
            for w in escrituras:
                if w["ruta"].endswith(sufijo) and w["ts"].strftime("%Y-%m-%dT%H:%M") == minuto:
                    return w
            raise SystemExit(f"no está la escritura de {sufijo} a las {minuto}")

        def titular_git(ruta, commit):
            b = arbol(git("rev-parse", commit).strip()).get(ruta)
            return self.titular(ruta, b) if b else None

        # 1 · el libro: la primera escritura de sus archivos, antes de los arreglos que entraron en a7b4bb4
        v = self.version_extra("editorial", escrita("editorial/extraer_informe.js", "2026-10-19T00:36")["ts"], "conversacion",
                               "primera escritura del libro", "versión anterior",
                               "La primera escritura de siete archivos del libro, tal como quedaron en la conversación antes de los arreglos que se hicieron al probarlo. La versión que entró en git es la del commit a7b4bb4.",
                               "Las llamadas de escritura del registro de la conversación (19.10.2026) y el commit a7b4bb4, cuyo contenido es otro.",
                               "«Versión anterior»: estos archivos cambiaron antes del commit; ninguna de estas escrituras está en git.")
        presentes = {}
        for suf, minuto in [("editorial/extraer_informe.js", "2026-10-19T00:36"), ("editorial/estilo.css", "2026-10-19T00:49"),
                            ("editorial/armar.py", "2026-10-19T00:55"), ("editorial/planas.py", "2026-10-19T01:00"),
                            ("editorial/placas_de_cerca.py", "2026-10-19T01:07"), ("editorial/cubierta.py", "2026-10-19T01:19"),
                            ("editorial/README.md", "2026-10-19T09:25")]:
            w = escrita(suf, minuto)
            ruta = "tipografia/" + suf
            t = titular_git(ruta, "a7b4bb4")
            presentes[ruta] = self.poner(v, w["datos"], suf, ruta_original=ruta, descripcion_=descripcion(ruta, w["datos"]),
                       categoria_=categoria(ruta), estado="versión anterior", copia="copia de la conversación",
                       fecha=w["ts"], que_fecha=QUE_FECHA["escritura"], relacion=f"estado intermedio de {ruta}" + (f"; la versión del commit a7b4bb4 es @{id(t)}" if t else ""),
                       observaciones="Escrita entera en la conversación; después se corrigió con ediciones que no quedaron registradas una por una.")

        self.dependencias_de(v, arbol(git("rev-parse", "a7b4bb4").strip()), {r: f for r, f in presentes.items() if r.endswith(".md")})
        v["deduccion"] += " Las imágenes que muestra el README se copian del commit a7b4bb4, el estado más cercano en git."

        # 2 · el libro: lo que se vio al probarlo (vistas de páginas y del prototipo)
        def origen_editorial(r):
            for clave, sub in (("editorial/.cache/vistas/", "vistas_del_armado"), ("scratchpad/editorial/vistas/", "vistas_del_prototipo"),
                               ("scratchpad/editorial/prueba/", "prueba_del_prototipo"), ("tipografia/editorial/muestras/", "muestras")):
                if clave in r:
                    return sub
            return None
        imgs = [i for i in imagenes if origen_editorial(i["ruta"])]
        if imgs:
            v = self.version_extra("editorial", imgs[0]["ts"], "conversacion", "vistas de prueba del libro", "prueba o experimento",
                                   f"{len(imgs)} imágenes de páginas y del prototipo del libro, como las vio la conversación al probar el armado (19.10.2026). Muestran estados intermedios: algunos con los errores que después se arreglaron.",
                                   "Las lecturas de imágenes del registro de la conversación, con su hora; el resumen de la conversación anota los errores y sus arreglos.",
                                   "Son copias reducidas: la conversación guarda las imágenes al tamaño en que las vio, no los archivos originales, que se rehacían en cada prueba.")
            self.poner_imagenes(v, imgs, origen_editorial, "vista de prueba del libro")

        # 3 · el libro: el encargo para que otra IA diseñara el documento (en línea)
        enc = artefactos / "f93e8668-a923-4e41-a3f7-022bcee0a41a" / "index.html"
        fecha_enc = dt.datetime.fromtimestamp(1792366179, UTC)
        v = self.version_extra("editorial", fecha_enc, "en-linea", "encargo editorial para gpt astra 6", "alternativa",
                               "El encargo editorial publicado como artefacto: el prompt para que GPT Astra 6 leyera el proyecto y diseñara el documento editorial, con las cinco referencias visuales y los límites que no se negocian.",
                               "El pedido del prompt para «chat gpt Astra 6» y el pedido siguiente, «Sabes que realiza tu este diseño editorial…», que llevó al libro (resumen de la conversación); el artefacto «Encargo editorial de Contenida».",
                               "«Alternativa»: es otro camino para el mismo documento. No consta si se usó.")
        self.poner(v, enc.read_bytes(), "artefacto/index.html", ruta_original="https://claude.ai/artifact/Xn7KdZAVXaFVrrLdUGSbcm",
                   descripcion_="Encargo editorial de Contenida: el prompt para GPT Astra 6", categoria_="documento (página en línea)",
                   estado="alternativa", copia="copia de la versión en línea", fecha=fecha_enc, que_fecha=QUE_FECHA["en_linea"],
                   observaciones="Página servida por claude.ai (versión 1792366179-5292), con el envoltorio que agrega la plataforma. Su fuente, encargo/encargo_editorial.html, estaba fuera del repositorio y no se conserva.",
                   id_prefijo="L", fuente=enc)

        # 4 · la aplicación en línea, versión 4 (la de los deslizadores)
        if self.v4:
            fecha_v4 = dt.datetime.fromtimestamp(1792250851, UTC)
            v = self.version_extra("aplicacion", fecha_v4, "en-linea", "artefacto gramatica version 4", "versión anterior",
                                   "La página del artefacto «Gramática de Contenida» en su versión 4: la aplicación de las nueve decisiones con deslizadores, con las letras de Google Fonts y Clipper de jsDelivr. Al lado, los tres guiones que carga, para que abra.",
                                   "La lectura del artefacto en la conversación (30.10.2026), antes de publicar la versión 5; datos.js y gramatica.js se compararon entonces con los del repositorio y eran iguales.",
                                   "«Versión anterior»: la reemplazó la versión 5 el 30.10.2026. app.js se toma del commit 1eaf342 porque tiene el mismo tamaño que el de la versión 4 (21 438 bytes); no se comparó su contenido.")
            self.poner(v, self.v4["datos"], "artefacto/index.html", ruta_original="https://claude.ai/artifact/MD4hC81MMftYgHHB1RT9bL (versión 4)",
                       descripcion_="Gramática de Contenida, versión 4 en línea: la página", categoria_="aplicación (página en línea)",
                       estado="versión anterior", copia="copia de la versión en línea", fecha=fecha_v4, que_fecha=QUE_FECHA["en_linea"],
                       observaciones="Recuperada del registro de la conversación (lectura del 30.10.2026, 03:19 UTC); mide lo mismo que el archivo publicado (9319 bytes).",
                       id_prefijo="L")
            cabeza = arbol(self.cabeza["h"])
            for nombre, fuente, nota in (("datos.js", ("tipografia/aplicacion/datos.js", cabeza), "Igual al de la versión 4: se comparó el 30.10.2026."),
                                         ("gramatica.js", ("tipografia/aplicacion/gramatica.js", cabeza), "Igual al de la versión 4: se comparó el 30.10.2026."),
                                         ("app.js", ("tipografia/aplicacion/app.js", arbol(git("rev-parse", "1eaf342").strip())), "Probable: el app.js de la versión 4 mide 21 438 bytes, como este; no se comparó su contenido.")):
                b = fuente[1][fuente[0]]
                self.dependencia_extra(v, contenido(b), f"artefacto/{nombre}", fuente[0], b, nota)

        # 5 · la bandeja radial, descartada
        v = self.version_extra("aplicacion", escrita("aplicacion/index.html", "2026-10-30T02:37")["ts"], "conversacion",
                               "bandeja radial descartada", "material descartado",
                               "La primera respuesta al video de referencia: una «bandeja» radial con las decisiones como ejes alrededor del desagüe. Se escribió la página y su guion; no se probó.",
                               "El mensaje del pedido del 30.10.2026 a las 02:39 UTC, mientras se escribía: «Ojo no te pido copiar la interfaz, ves el ejemplo de como desarrollar interfaces AD hoc a cada proyecto y que no todos sean iguales». La respuesta registrada la descarta por copiar la estrella radial del video.",
                               "«Material descartado»: lo descarta el intercambio citado. Las dependencias se toman del estado de la rama en ese momento (a7b4bb4).")
        presentes = {}
        for suf, minuto in (("aplicacion/index.html", "2026-10-30T02:37"), ("aplicacion/app.js", "2026-10-30T02:40")):
            w = escrita(suf, minuto)
            presentes["tipografia/" + suf] = self.poner(v, w["datos"], suf, ruta_original="tipografia/" + suf,
                                                        descripcion_=descripcion(suf, w["datos"]), categoria_=categoria("tipografia/" + suf),
                                                        estado="material descartado", copia="copia de la conversación", fecha=w["ts"],
                                                        que_fecha=QUE_FECHA["escritura"], relacion="borrador descartado de tipografia/" + suf)
        self.dependencias_de(v, antes_02dcb14, presentes)

        # 6 · los planos de detalle: el primer borrador, sin probar
        v = self.version_extra("aplicacion", escrita("aplicacion/index.html", "2026-10-30T02:45")["ts"], "conversacion",
                               "planos de detalle primer borrador", "versión anterior",
                               "El primer borrador de la interfaz de los planos de detalle, antes de probarlo; la sección de los dibujos reescrita después de la primera prueba; y la primera escritura del README nuevo.",
                               "Las escrituras del registro de la conversación (30.10.2026) y el commit 02dcb14, que guarda la versión probada.",
                               "«Versión anterior»: la versión vigente salió de estos borradores después de las pruebas (02dcb14).")
        presentes = {}
        for suf, minuto in (("aplicacion/index.html", "2026-10-30T02:45"), ("aplicacion/app.js", "2026-10-30T02:48"),
                            ("aplicacion/README.md", "2026-10-30T03:12")):
            w = escrita(suf, minuto)
            presentes["tipografia/" + suf] = self.poner(v, w["datos"], suf, ruta_original="tipografia/" + suf,
                                                        descripcion_=descripcion(suf, w["datos"]), categoria_=categoria("tipografia/" + suf),
                                                        estado="versión anterior", copia="copia de la conversación", fecha=w["ts"],
                                                        que_fecha=QUE_FECHA["escritura"], relacion="estado intermedio de tipografia/" + suf)
        w = escrita("scratchpad/dibujos.js", "2026-10-30T03:00")
        self.poner(v, w["datos"], "trabajo/dibujos.js", ruta_original="(scratch de la sesión) dibujos.js",
                   descripcion_="Los siete dibujos reescritos, antes de empalmarlos en app.js", categoria_="aplicación (fragmento)",
                   estado="versión anterior", copia="copia de la conversación", fecha=w["ts"], que_fecha=QUE_FECHA["escritura"],
                   relacion="fragmento de tipografia/aplicacion/app.js")
        self.dependencias_de(v, antes_02dcb14, {k: f for k, f in presentes.items() if k.endswith("index.html") or k.endswith("app.js")})

        # 7 · las pruebas de la aplicación, del informe y del libro (30.10.2026)
        self.pruebas_del_30(scratch, imagenes)

        # 8 · la aplicación en línea, versión 5 (la vigente)
        g5 = artefactos / "a3a5f96c-3d69-49bf-95d2-508738cb92f7"
        fecha_v5 = dt.datetime.fromtimestamp(1793330424, UTC)
        v = self.version_extra("aplicacion", fecha_v5, "en-linea", "artefacto gramatica version 5", "versión vigente",
                               "La página del artefacto «Gramática de Contenida» en su versión 5, la de los planos de detalle, como la sirve claude.ai. Al lado, los tres guiones que carga (iguales a los de tipografia/aplicacion/).",
                               "La publicación registrada en la conversación (30.10.2026, 03:20 UTC) y la descarga de la versión servida (02.11.2026); su app.js es igual al del repositorio.",
                               "«Versión vigente» en línea: es la última publicada. No consta una aprobación.")
        self.poner(v, (g5 / "index.html").read_bytes(), "artefacto/index.html", ruta_original="https://claude.ai/artifact/MD4hC81MMftYgHHB1RT9bL (versión 5)",
                   descripcion_="Gramática de Contenida, versión 5 en línea: la página", categoria_="aplicación (página en línea)",
                   estado="versión vigente", copia="copia de la versión en línea", fecha=fecha_v5, que_fecha=QUE_FECHA["en_linea"],
                   observaciones="Página servida (versión 1793330424-c77f), con el envoltorio de la plataforma. Se armó desde tipografia/aplicacion/index.html: letras de Google Fonts y Clipper de jsDelivr.",
                   id_prefijo="L", fuente=g5 / "index.html")
        cabeza = arbol(self.cabeza["h"])
        for nombre in ("datos.js", "gramatica.js", "app.js"):
            r = "tipografia/aplicacion/" + nombre
            self.dependencia_extra(v, contenido(cabeza[r]), f"artefacto/{nombre}", r, cabeza[r], "Igual al publicado en la versión 5.")

        # 9 · el repujado en línea (y su duplicado, publicado por error)
        rep = artefactos / "50dedd80-74bd-4a12-a67f-012ea81e773d" / "index.html"
        dup = artefactos / "fb5c04c9-af76-48dd-bd7c-3216a11d35b5" / "index.html"
        fecha_r = dt.datetime.fromtimestamp(1792339544, UTC)
        v = self.version_extra("repujado", fecha_r, "en-linea", "artefacto el repujado de contenida", "versión vigente",
                               "La mesa del repujado como artefacto de una sola página, servida por claude.ai. Hay dos direcciones con la misma página: la buena y un duplicado publicado por error 23 segundos antes.",
                               "Las dos páginas descargadas (02.11.2026) son idénticas byte a byte; el resumen de la conversación anota: «Artifact published as a new URL by mistake: read and republished to AzCijUBf7Grujskuw7qPmE».",
                               "«Versión vigente» en línea para AzCijUBf7Grujskuw7qPmE. El duplicado se registra, no se copia dos veces.")
        f = self.poner(v, rep.read_bytes(), "artefacto/index.html", ruta_original="https://claude.ai/artifact/AzCijUBf7Grujskuw7qPmE",
                       descripcion_="El repujado de Contenida, en línea: la mesa", categoria_="aplicación (página en línea)",
                       estado="versión vigente", copia="copia de la versión en línea", fecha=fecha_r, que_fecha=QUE_FECHA["en_linea"],
                       observaciones="Página servida (versión 1792339544-dfa2), con el envoltorio de la plataforma. El repositorio guarda su fuente en tipografia/repujado/.",
                       id_prefijo="L", fuente=rep)
        datos_dup = dup.read_bytes()
        g = self.fila(id="", nombre="index.html", descripcion="El repujado de Contenida, duplicado publicado por error",
                      categoria="aplicación (página en línea)", linea="repujado", version_o_etapa=v["carpeta"],
                      estado="material descartado", formato="HTML", copia="no se copia (duplicado exacto)",
                      ruta_original="https://claude.ai/artifact/Y3FyvuU5q3hZjo9TW8qKor", ruta_archivada=f["ruta_archivada"],
                      fecha=fecha_txt(dt.datetime.fromtimestamp(1792339521, UTC)), que_representa_la_fecha=QUE_FECHA["en_linea"],
                      relacion=f"duplicado exacto de @{id(f)}", sha256=sha256(datos_dup), bytes=len(datos_dup), blob_git=blob_git(datos_dup),
                      observaciones="Sigue publicado: borrarlo quedó pendiente de que se pida." + (f" SHA-256 informado por claude.ai al descargarla: {self.informados[str(dup)]}." if str(dup) in self.informados else ""))
        g["_prefijo"], g["_dup"] = "L", f
        v["registrados"].append(g)

    def dependencia_extra(self, v, datos, rel, ruta_original, blob, nota):
        dest = self.copiar(datos, f"versiones/{v['linea']}/{v['carpeta']}/{rel}")
        t = self.titular(ruta_original, blob)
        d = self.fila(id="", nombre=posixpath.basename(rel), descripcion=descripcion(ruta_original, datos), categoria=categoria(ruta_original),
                      linea=v["linea"], version_o_etapa=v["carpeta"], estado=t["estado"] if t else "estado sin confirmar",
                      formato=formato(rel), copia="copia funcional (dependencia)", ruta_original=ruta_original, ruta_archivada=dest,
                      rama=RAMA, commit=t["commit"] if t else "", fecha=t["fecha"] if t else "", que_representa_la_fecha=t["que_representa_la_fecha"] if t else "",
                      fuente_o_generador=generador(ruta_original), sha256=sha256(datos), bytes=len(datos), blob_git=blob, observaciones=nota)
        d["_titular"], d["_requerida_por"] = t, rel
        v["dependencias"].append(d)

    def poner_imagenes(self, v, imgs, subcarpeta, que_es, linea=None):
        usados = set()
        for i in imgs:
            ext = {"image/png": ".png", "image/jpeg": ".jpg", "image/gif": ".gif", "image/webp": ".webp"}.get(i["tipo"], ".img")
            base = posixpath.splitext(posixpath.basename(i["ruta"]))[0]
            nombre = f"{i['ts']:%H%M%S}_{base}{ext}"
            n = 2
            while nombre in usados:
                nombre = f"{i['ts']:%H%M%S}_{base}_{n}{ext}"
                n += 1
            usados.add(nombre)
            wh = medidas_imagen(i["datos"])
            self.poner(v, i["datos"], f"{subcarpeta(i['ruta'])}/{nombre}",
                       ruta_original=i["ruta"].replace("/tmp/claude-0/-home-user-Altiplano/352f68a8-9ee1-54d4-afeb-470f1498d6cf/", "(sesión) ").replace("/home/user/Altiplano/", ""),
                       descripcion_=f"{que_es}: {posixpath.basename(i['ruta'])}", categoria_="prueba (imagen)", estado="prueba o experimento",
                       copia="copia reducida (de la conversación)", fecha=i["ts"], que_fecha=QUE_FECHA["imagen"],
                       observaciones=f"Copia que guardó la conversación ({wh[0]} × {wh[1]} px), no el archivo original." if wh else "Copia que guardó la conversación, no el archivo original.")

    def pruebas_del_30(self, scratch, imagenes):
        def mtime(p):
            return dt.datetime.fromtimestamp(p.stat().st_mtime, UTC)
        grupos = {"aplicacion": [], "informe": [], "editorial": []}
        for p in sorted((scratch / "capturas").glob("*.png")):
            n = p.name
            l = "informe" if n.startswith(("informe_", "hoja_informe", "figura_informe")) else "editorial" if n.startswith(("libro_", "hoja_libro")) else "aplicacion"
            grupos[l].append(p)
        herramientas = [scratch / n for n in ("probar.js", "arrastrar.js", "zoom.js", "hoja.js", "figura.js", "medir.js") if (scratch / n).exists()]
        ediciones = sorted((scratch / "ed").glob("*.py"))
        vistas = [i for i in imagenes if "/scratchpad/capturas/" in i["ruta"]]
        textos = {
            "aplicacion": ("pruebas de la aplicacion", "Las pruebas de la interfaz de los planos de detalle en un navegador sin pantalla: los guiones que la abren, la arrastran y la capturan, las capturas finales y las que vio la conversación en cada vuelta, con los errores que se corrigieron. También los guiones con que se hicieron las ediciones."),
            "informe": ("comprobaciones del informe", "Las páginas 28 y 29 del informe rehecho, para comprobar el §8.4 y su figura."),
            "editorial": ("comprobaciones del libro", "Las páginas 52 y 53 del libro rehecho (por folio), para comprobar el §8.4 y su figura."),
        }
        for l, ps in grupos.items():
            vl = [i for i in vistas if (("informe" if posixpath.basename(i["ruta"]).startswith(("informe_", "hoja_informe")) else "editorial" if posixpath.basename(i["ruta"]).startswith(("libro_", "hoja_libro")) else "aplicacion") == l)]
            if not ps and not vl:
                continue
            fecha = min([mtime(p) for p in ps] + [i["ts"] for i in vl] + ([mtime(h) for h in herramientas] if l == "aplicacion" else []))
            v = self.version_extra(l, fecha, "conversacion", textos[l][0], "prueba o experimento", textos[l][1],
                                   "Los archivos de la carpeta de trabajo de la sesión del 30.10.2026 y las lecturas de imágenes del registro de la conversación.",
                                   "«Prueba o experimento»: sirven para comprobar, no son entregables.")
            for p in ps:
                d = p.read_bytes()
                wh = medidas_imagen(d)
                self.poner(v, d, f"capturas_finales/{p.name}", ruta_original=f"(sesión) scratchpad/capturas/{p.name}",
                           descripcion_=f"Captura de prueba: {p.name}", categoria_="prueba (imagen)", estado="prueba o experimento",
                           copia="copia de la conversación", fecha=mtime(p), que_fecha=QUE_FECHA["scratch"],
                           observaciones=(f"{wh[0]} × {wh[1]} px. " if wh else "") + "Última versión del archivo: varias capturas se rehicieron con el mismo nombre.")
            if vl:
                self.poner_imagenes(v, vl, lambda r: "capturas_vistas_en_la_conversacion", "captura vista en la conversación")
            if l == "aplicacion":
                for h in herramientas:
                    d = h.read_bytes()
                    self.poner(v, d, f"herramientas_de_prueba/{h.name}", ruta_original=f"(sesión) scratchpad/{h.name}",
                               descripcion_=descripcion(h.name, d), categoria_="prueba (herramienta)", estado="prueba o experimento",
                               copia="copia de la conversación", fecha=mtime(h), que_fecha=QUE_FECHA["scratch"],
                               observaciones="Se corre con Node." if h.name == "medir.js" else "Se corre con Node y Playwright, con el Chromium de la sesión.")
                for h in ediciones:
                    d = h.read_bytes()
                    self.poner(v, d, f"ediciones/{h.name}", ruta_original=f"(sesión) scratchpad/ed/{h.name}",
                               descripcion_=descripcion(h.name, d) if h.name == "reemplazar.py" else f"Reemplazos aplicados con reemplazar.py: {h.name}",
                               categoria_="prueba (herramienta)", estado="prueba o experimento", copia="copia de la conversación",
                               fecha=mtime(h), que_fecha=QUE_FECHA["scratch"],
                               observaciones="Registro de las ediciones del 30.10.2026 (aplicación, README, informe, 03c y armado del libro).")

    # -- lo que no se archiva o no está
    def ausentes(self, video, frames):
        def n(**k):
            f = self.fila(id="", copia=k.pop("copia", "no se archiva"), **k)
            f["_prefijo"] = "N"
            return f
        if video and video.exists():
            d = video.read_bytes()
            n(nombre=video.name, descripcion="El reel de referencia para la interfaz de la aplicación (Ultravaria, de Aimeric)",
              categoria="referencia de terceros", linea="aplicacion", estado="no aplica: referencia de terceros", formato="MP4",
              ruta_original=f"(adjunto de la conversación) {video.name}", fecha="2026-10-30 02:29 UTC",
              que_representa_la_fecha="cuándo se adjuntó en la conversación", sha256=sha256(d), bytes=len(d), blob_git=blob_git(d),
              observaciones="No se sube: «se cita, no se sube». Se tomó el método, no la interfaz.")
        if frames and frames.exists():
            ps = sorted(frames.glob("*"))
            n(nombre=frames.name + "/", descripcion=f"{len(ps)} fotogramas y hojas de contacto sacados del reel, para analizarlo",
              categoria="referencia de terceros (derivado)", linea="aplicacion", estado="no aplica: referencia de terceros",
              formato="PNG", ruta_original="(sesión) scratchpad/video_ui/", fecha="2026-10-30", que_representa_la_fecha="día en que se sacaron",
              bytes=sum(p.stat().st_size for p in ps), observaciones="No se suben, como el video. La conversación vio 8 de estas imágenes; tampoco se copian.")
        filas = [
            ("Cinco imágenes de referencia editorial (segunda tanda)", "referencia de terceros", "editorial", "JPG",
             "(adjuntos de la conversación) 38.jpg a 42.jpg", "antes del 2026-10-19 00:32 UTC", "se adjuntaron con el pedido del libro; la hora exacta no está en este registro",
             "El libro con forma de guion, «PAST (in)tense / future (im)PERFECT», el catálogo de un festival de cine, un libro coreano sobre la vida en Japón y una doble página de «EUROPE ©2020» de Dora Lazarevic. No se suben (06, §6.4: las referencias se citan). La conversación las vio el 19.10 y guarda copias reducidas; tampoco se copian."),
            ("Cinco imágenes de referencia editorial (primera tanda)", "referencia de terceros", "editorial", "JPG",
             "(adjuntos de la conversación)", "anterior al 2026-10-19", "se adjuntaron con el pedido del prompt para GPT Astra 6; sin fecha en este registro",
             "El guion, un cuadernillo de HEAD Genève, las páginas de los noventa, el catálogo de cine y el libro coreano, según el encargo editorial. No están en este contenedor y no se suben (06, §6.4)."),
            ("El reel del repujado y su video", "referencia de terceros", "repujado", "MP4",
             "(adjunto de la conversación) y https://www.instagram.com/reel/DemRiTionHY/ · https://youtu.be/gFGqe2nQBH8", "anterior al 2026-10-19", "se compartió antes del 19.10; sin fecha en este registro",
             "La referencia para la simulación del repujado. No está en este contenedor y no se sube: «se cita, no se sube»."),
            ("La foto del pie de la lámina", "fuente del proyecto (no se sube)", "simulacion", "—",
             "(fuera del repositorio)", "", "",
             "De ella salen los testigos de simulacion/testigos/. «La foto no se sube al repositorio: solo letras sueltas» (extraer_testigos.py; 07_posnansky.md, §3)."),
            ("Las imágenes del atlas", "imágenes de dominio público (fuera del repositorio)", "taxonomia", "JPG/PNG",
             "tipografia/taxonomia/imagenes/ (ignorada por git)", "2026-10-18", "día en que se bajaron (commit 976fbf0)",
             "Veinticuatro imágenes de dominio público. «imagenes/ sigue fuera del repositorio (06, §6.4)». No están en este contenedor; se rehacen con taxonomia/descargar_imagenes.py."),
            ("Los dos zips de entregables (documentos e imágenes)", "resultado exportado", "(todas)", "ZIP",
             "(enviados en la conversación)", "anterior al 2026-10-19", "se enviaron antes del 19.10; sin fecha en este registro",
             "Se armaron con armar_entregables.sh y se enviaron en la conversación (uno de 32 MB). No están en este contenedor; su contenido sale del repositorio de entonces (commit sin confirmar)."),
            ("Herramientas de trabajo de contenedores anteriores", "herramientas", "(varias)", "SH/PY/HTML/MD",
             "armar_entregables.sh, artefacto/armar.py, prueba_esqueleto.html, encargo/prompt_astra.md, encargo/encargo_editorial.html, editorial/viv/", "anterior al 2026-10-19", "",
             "Se perdieron con sus contenedores. Del encargo queda la página publicada (en versiones/editorial/)."),
            ("El registro de la conversación del 29.09 al 18.10", "conversación", "(todas)", "—",
             "(contenedores anteriores)", "2026-09-29 a 2026-10-18", "lo que abarcaba",
             "No está en este contenedor. Quedan los commits, los documentos y el resumen con que sigue la conversación (19.10.2026), del que salen los pedidos sin fecha de la línea de tiempo."),
            ("Las versiones 1 a 3 del artefacto «Gramática de Contenida»", "aplicación (página en línea)", "aplicacion", "HTML",
             "https://claude.ai/artifact/MD4hC81MMftYgHHB1RT9bL", "", "",
             "No se pudieron leer: se archivan la versión 4 (del registro de la conversación) y la 5 (la vigente)."),
            ("La primera versión del artefacto «El repujado de Contenida»", "aplicación (página en línea)", "repujado", "HTML",
             "https://claude.ai/artifact/AzCijUBf7Grujskuw7qPmE", "", "",
             "El resumen de la conversación la nombra «v2»: la anterior no se pudo leer."),
            ("Los estados intermedios hechos con ediciones por guion", "registro de trabajo", "(varias)", "—",
             "(conversación)", "", "",
             "Muchos cambios se hicieron con guiones de Python o sed, no escribiendo el archivo entero: de esos queda el resultado (en git), no cada paso. Lo mismo con la edición de editorial/libro.py del 19.10 (su base es anterior a este registro)."),
            ("El armado intermedio del libro (.cache/)", "resultado intermedio", "editorial", "HTML/JSON/PNG",
             "tipografia/editorial/.cache/ (ignorada por git)", "", "",
             "libro.html, el texto del informe en JSON y las vistas de las páginas. Se rehace con armar.py: «Todo lo que se arma va a .cache/, que no entra en el repositorio» (README del libro)."),
            ("Las dependencias de Node del libro (node_modules/)", "dependencias", "editorial", "—",
             "tipografia/editorial/node_modules/ (ignorada por git)", "", "",
             "Vivliostyle CLI 11.3.3 y lo que necesita. Se reinstalan con «npm ci» desde package-lock.json, que es vigente."),
            ("Archivos generados e ignorados", "resultado intermedio", "(varias)", "JSON/FEA/PYC",
             "tipografia/informe/.titulos.json, tipografia/digital/poliza.fea, __pycache__/", "", "",
             "Los ignora .gitignore; se rehacen con sus generadores (informe/armar.py, digital/poliza.py)."),
            ("El entorno de la sesión", "herramientas", "(todas)", "—",
             "(sesión) venv, npm, Playwright, LibreOffice", "", "",
             "Las herramientas con que se armó, se probó y se rehízo todo: no son material del proyecto."),
            ("«Contenedor»: posible antecedente, de otra conversación", "aplicación (página en línea)", "(sin línea)", "HTML",
             "https://claude.ai/artifact/MYW9vtsGRxjnydSAwjKZNL", "2026-09-27", "última actualización según la lista de artefactos",
             "Se presenta como «Tipografía · prototipo 0.100 · 144 caracteres · 5 ejes» a partir de Contener una ruina. Es anterior a esta conversación, que empieza el 29.09: no se archiva hasta que confirmes si es parte del proyecto."),
            ("«Vasijas»: posible antecedente, de otra conversación", "aplicación (páginas en línea)", "(sin línea)", "HTML",
             "https://claude.ai/artifact/NyVpACsGDDzxdpvSnkMsYG", "2026-09-28", "última actualización según la lista de artefactos",
             "Se presenta como «Contener una ruina · tipografía · segundo intento» (seis páginas: agua, cadena, espalda, placa, ruina). Anterior a esta conversación: no se archiva hasta que lo confirmes."),
        ]
        REGLA, AUSENTE, REGENERA = "no se archiva", "ausente", "no se copia: se regenera"
        tipo = {   # nombre -> (estado, copia)
            "Cinco imágenes de referencia editorial (segunda tanda)": ("no aplica: referencia de terceros", REGLA),
            "Cinco imágenes de referencia editorial (primera tanda)": ("no aplica: referencia de terceros", REGLA),
            "El reel del repujado y su video": ("no aplica: referencia de terceros", REGLA),
            "La foto del pie de la lámina": ("no aplica: no se sube por decisión documentada", REGLA),
            "Las imágenes del atlas": ("no aplica: fuera del repositorio por regla (06, §6.4)", REGLA),
            "Los dos zips de entregables (documentos e imágenes)": ("estado sin confirmar", AUSENTE),
            "Herramientas de trabajo de contenedores anteriores": ("estado sin confirmar", AUSENTE),
            "El registro de la conversación del 29.09 al 18.10": ("estado sin confirmar", AUSENTE),
            "Las versiones 1 a 3 del artefacto «Gramática de Contenida»": ("versión anterior", AUSENTE),
            "La primera versión del artefacto «El repujado de Contenida»": ("versión anterior", AUSENTE),
            "Los estados intermedios hechos con ediciones por guion": ("versión anterior", AUSENTE),
            "El armado intermedio del libro (.cache/)": ("no aplica: se regenera", REGENERA),
            "Las dependencias de Node del libro (node_modules/)": ("no aplica: se regenera", REGENERA),
            "Archivos generados e ignorados": ("no aplica: se regenera", REGENERA),
            "El entorno de la sesión": ("no aplica: herramientas de la sesión", REGENERA),
            "«Contenedor»: posible antecedente, de otra conversación": ("estado sin confirmar", REGLA),
            "«Vasijas»: posible antecedente, de otra conversación": ("estado sin confirmar", REGLA),
        }
        for nombre, cat, linea, fmt, ruta, fecha, que, obs in filas:
            estado, copia = tipo[nombre]
            n(nombre=nombre, descripcion=nombre, categoria=cat, linea=linea, estado=estado, formato=fmt, copia=copia,
              ruta_original=ruta, fecha=fecha, que_representa_la_fecha=que, observaciones=obs)

    # -- números, relaciones y documentos
    def numerar(self):
        orden_l = list(LINEAS)
        def clave(f):
            return (orden_l.index(f["linea"]) if f["linea"] in orden_l else 99, f["fecha"], f["ruta_original"], f["version_o_etapa"])
        grupos = defaultdict(list)
        for f in self.filas:
            if f.get("_prefijo"):
                p = f["_prefijo"]
            elif f["copia"] == "en su lugar (no se copia)":
                p = "V"
            elif f["copia"] == "copia funcional (dependencia)":
                p = "D"
            elif f["copia"] == "copia exacta":
                p = "H"
            else:
                p = "N"
            grupos[p].append(f)
        for p in ("V", "H", "D", "C", "L", "N"):
            for i, f in enumerate(sorted(grupos[p], key=clave), 1):
                f["id"] = f"{p}-{i:04d}" if p in "VHD" else f"{p}-{i:03d}"
        por_objeto = {str(id(f)): f["id"] for f in self.filas}
        for f in self.filas:
            if f.get("_versiones"):
                f["en_versiones"] = " ".join(sorted(f["_versiones"], key=lambda c: self.indice.get(c, 0)))
            if f["copia"] == "copia exacta" and f["ruta_original"] in self.vigentes:
                f["relacion"] += f"; vigente: {self.vigentes[f['ruta_original']]['id']}"
            if f.get("_titular") is not None and f["copia"] == "copia funcional (dependencia)":
                f["relacion"] = f"copia funcional de {f['_titular']['id']}, que pide {f.get('_requerida_por', '')}"
            elif f["copia"] == "copia funcional (dependencia)" and f.get("_original"):
                t = self.titular(*f["_original"])
                f["relacion"] = (f"copia funcional de {t['id']}" if t else "copia funcional") + f", que pide {bajo_tipografia(f.get('_requerida_por', ''))}"
            f["relacion"] = re.sub(r"@(\d+)", lambda m: por_objeto.get(m.group(1), "?"), f["relacion"])
        self.filas.sort(key=lambda f: ("VHDCLN".index(f["id"][0]), f["id"]))

    def escribir_inventario(self):
        with open(self.destino / "inventario.csv", "w", newline="", encoding="utf-8-sig") as fh:
            w = csv.DictWriter(fh, fieldnames=COLUMNAS, extrasaction="ignore")
            w.writeheader()
            for f in self.filas:
                w.writerow({c: f[c] for c in COLUMNAS})

    # -- los documentos del archivo
    def enlace(self, desde, hacia):
        """Enlace relativo entre dos rutas del repositorio (desde: el documento; hacia: el destino)."""
        return posixpath.relpath(hacia, posixpath.dirname(desde))

    def ficha_de(self, v):
        return f"{ARCHIVO}/versiones/{v['linea']}/{v['carpeta']}/ficha.md"

    def vigente_de(self, l):
        return "tipografia" if l == "documentos" else f"tipografia/{l}"

    def escribir(self, rel, lineas):
        p = self.destino / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("\n".join(lineas).rstrip() + "\n", encoding="utf8")

    def lista(self, rutas, n=14):
        rutas = sorted(rutas)
        txt = ", ".join(f"`{bajo_tipografia(r)}`" for r in rutas[:n])
        return txt + (f" y {len(rutas) - n} más" if len(rutas) > n else "")

    def escribir_documentos(self):
        por_linea = defaultdict(list)
        for v in self.versiones:
            por_linea[v["linea"]].append(v)
        for l in por_linea:
            por_linea[l].sort(key=lambda v: (v["fecha"], v["carpeta"]))
        self.por_linea = por_linea
        self.ultima_git = {l: [v for v in vs if v["origen"] == "git"][-1] for l, vs in por_linea.items() if any(v["origen"] == "git" for v in vs)}
        for l, vs in por_linea.items():
            git_vs = [v for v in vs if v["origen"] == "git"]
            for i, v in enumerate(vs):
                if v["origen"] == "git":
                    j = git_vs.index(v)
                    self.ficha_git(v, git_vs[j - 1] if j else None, git_vs[j + 1] if j + 1 < len(git_vs) else None)
                else:
                    self.ficha_extra(v)
            self.readme_linea(l, vs)
        self.indice_versiones()
        self.linea_de_tiempo()
        self.pendientes()
        self.recursos_compartidos()
        self.readme()

    def ficha_git(self, v, previa, siguiente):
        c, l = v["commit"], v["linea"]
        titulo = LINEAS[l][0]
        doc = f"{ARCHIVO}/versiones/{l}/{v['carpeta']}/ficha.md"
        ultima = v is self.ultima_git[l]
        estado = "versión vigente" if ultima else "versión anterior"
        cu = v["cuenta"]
        L = [f"# {titulo} · {fecha_txt(v['fecha'])}", "",
             "| | |", "|---|---|",
             f"| Línea | [{titulo}]({self.enlace(doc, f'{ARCHIVO}/versiones/{l}/README.md')}) |",
             f"| Origen | commit `{c['c']}` de la rama `{RAMA}` |",
             f"| Fecha | {fecha_txt(v['fecha'])}: la del commit, no la de creación de lo que contiene |",
             f"| Estado de la versión | {estado} |",
             f"| Lo vigente | [`{self.vigente_de(l)}/`]({self.enlace(doc, self.vigente_de(l))}/) |"]
        if previa:
            otra = previa["carpeta"]
            L.append(f"| La versión anterior | [{otra}]({self.enlace(doc, f'{ARCHIVO}/versiones/{l}/{otra}/ficha.md')}) |")
        if siguiente:
            otra = siguiente["carpeta"]
            L.append(f"| La versión siguiente | [{otra}]({self.enlace(doc, f'{ARCHIVO}/versiones/{l}/{otra}/ficha.md')}) |")
        L += ["", "## Qué contiene esta carpeta", ""]
        if v["aqui"]:
            L.append(f"- **{len(v['aqui'])} archivos de esta versión que ya no son los vigentes,** con su ruta original debajo de `tipografia/`: "
                     + self.lista([f["ruta_original"] for f in v["aqui"]]) + ".")
        else:
            L.append("- **Ningún archivo propio:** todo lo que cambió en este commit sigue vigente, en su lugar." if ultima or v["vigentes"]
                     else "- **Ningún archivo propio.**")
        if v["dependencias"]:
            L.append(f"- **{len(v['dependencias'])} copias de dependencias**, lo que piden sus HTML, CSS o SVG, para que abran como entonces: "
                     + self.lista([d["ruta_original"] for d in v["dependencias"]], 8) + ".")
        if v["rotos"]:
            L.append(f"- **Referencias que no existían en ese commit:** " + ", ".join(f"`{r}` en `{bajo_tipografia(a)}`" for a, r in v["rotos"][:8]) + ".")
        L += ["", "## La versión completa", "",
              f"En este commit, la línea tenía {v['total']} archivos: {cu['aqui']} están en esta carpeta, {cu['antes']} en carpetas de versiones "
              f"anteriores y {cu['vigente']} siguen vigentes en su lugar. Para ver cuáles, filtra `inventario.csv` por la columna "
              f"`en_versiones` con `{c['c']}`.", "",
              "## Qué cambió respecto de la anterior", ""]
        for nombre, rutas in (("Añadidos", v["anadidos"]), ("Modificados", v["modificados"]), ("Retirados", v["retirados"])):
            if rutas:
                L.append(f"- **{nombre} ({len(rutas)}):** {self.lista(rutas)}.")
        for a, b in v["renombrados"][:10]:
            L.append(f"- **Renombrado:** `{bajo_tipografia(a)}` → `{bajo_tipografia(b)}`.")
        if len(v["renombrados"]) > 10:
            L.append(f"- Y {len(v['renombrados']) - 10} renombrados más.")
        if v["residuos"]:
            L.append(f"- **Residuo técnico (no se copia):** {self.lista(v['residuos'])}.")
        if v["retirados"] and c["c"] in RETIROS:
            L.append(f"- **Por qué se retiró:** {RETIROS[c['c']][1]}")
        cita = [f"> {c['asunto']}"] + ([">"] + [f"> {x}" if x else ">" for x in c["cuerpo"].splitlines()] if c["cuerpo"] else [])
        L += ["", "## Lo que lo respalda", "", f"El mensaje del commit `{c['c']}`:", ""] + cita
        readme = f"{self.vigente_de(l)}/README.md"
        cambiados = set(v["anadidos"]) | set(v["modificados"])
        if readme in cambiados:
            t = self.titular(readme, arbol(c["h"]).get(readme))
            if t:
                L += ["", f"Y el README de la línea en ese commit: [{t['id']}]({self.enlace(doc, t['ruta_archivada'])})."]
        L += ["", "## Lo que deduce el archivo", "",
              ("- «Versión vigente»: es la última versión de la línea en la rama. Que sea la más reciente no la vuelve aprobada; no consta una aprobación."
               if ultima else "- «Versión anterior»: la reemplazan las versiones siguientes de la línea. No consta que se haya aprobado.")]
        if v["dependencias"]:
            L.append("- Las dependencias son copias del estado de la rama en ese mismo commit; no cambian nada de lo que se archivó.")
        self.escribir(f"versiones/{l}/{v['carpeta']}/ficha.md", L)

    def ficha_extra(self, v):
        l = v["linea"]
        titulo = LINEAS[l][0]
        doc = f"{ARCHIVO}/versiones/{l}/{v['carpeta']}/ficha.md"
        origen = {"conversacion": "la conversación: su registro o la carpeta de trabajo de la sesión", "en-linea": "un artefacto publicado en claude.ai"}[v["origen"]]
        filas = v["aqui"] + v["registrados"]
        fecha_que = filas[0]["que_representa_la_fecha"] if filas else ""
        L = [f"# {titulo} · {fecha_txt(v['fecha'])} · {v['asunto']}", "",
             "| | |", "|---|---|",
             f"| Línea | [{titulo}]({self.enlace(doc, f'{ARCHIVO}/versiones/{l}/README.md')}) |",
             f"| Origen | {origen} |",
             f"| Fecha | {fecha_txt(v['fecha'])}: {fecha_que} |",
             f"| Estado | {v['estado']} |",
             f"| Lo vigente | [`{self.vigente_de(l)}/`]({self.enlace(doc, self.vigente_de(l))}/) |",
             "", "## Qué es", "", v["resumen"], "", "## Qué contiene esta carpeta", ""]
        for f in filas:
            if f["copia"].startswith("no se copia"):
                L.append(f"- `{f['id']}` · {f['descripcion']} · {f['copia']}: {f['relacion']}.")
            else:
                L.append(f"- [`{f['id']}`]({self.enlace(doc, f['ruta_archivada'])}) · {f['descripcion']} · {f['estado']}.")
        if v["dependencias"]:
            L.append(f"- Y {len(v['dependencias'])} copias de dependencias, para que abra: " + ", ".join(f"`{d['id']}`" for d in v["dependencias"]) + ".")
        L += ["", "## Lo que lo respalda", "", v["respaldo"], "", "## Lo que deduce el archivo", "", v["deduccion"]]
        self.escribir(f"versiones/{l}/{v['carpeta']}/ficha.md", L)

    def readme_linea(self, l, vs):
        titulo, desc = LINEAS[l]
        doc = f"{ARCHIVO}/versiones/{l}/README.md"
        n = {o: sum(1 for v in vs if v["origen"] == o) for o in ("git", "conversacion", "en-linea")}
        L = [f"# {titulo}", "", desc, "",
             f"- **Lo vigente:** [`{self.vigente_de(l)}/`]({self.enlace(doc, self.vigente_de(l))}/), el estado de la rama en `{self.cabeza['c']}`. No se copia aquí.",
             f"- **Versiones:** {n['git']} de git" + (f", {n['conversacion']} de la conversación" if n["conversacion"] else "")
             + (f" y {n['en-linea']} en línea" if n["en-linea"] else "") + ".",
             f"- **Volver:** [al índice del archivo]({self.enlace(doc, ARCHIVO + '/README.md')}).", "",
             "| Fecha (UTC) | Origen | Versión | Estado | Qué cambió o qué es |", "|---|---|---|---|---|"]
        for v in vs:
            if v["origen"] == "git":
                origen, estado, que = f"commit `{v['commit']['c']}`", ("versión vigente" if v is self.ultima_git[l] else "versión anterior"), v["asunto"]
            else:
                origen, estado, que = {"conversacion": "conversación", "en-linea": "en línea"}[v["origen"]], v["estado"], v["resumen"].split(". ")[0].rstrip(".") + "."
            L.append(f"| {fecha_txt(v['fecha'])[:-4]} | {origen} | [{v['carpeta']}]({v['carpeta']}/ficha.md) | {estado} | {que.replace('|', '/')} |")
        if l == "documentos":
            L += ["", "## Cada documento y sus versiones", "",
                  "Las versiones anteriores de cada documento, en orden; la última columna es la vigente.", "",
                  "| Documento | Versiones anteriores | Vigente |", "|---|---|---|"]
            hist = defaultdict(list)
            for f in self.filas:
                if f["linea"] == "documentos" and f["copia"] == "copia exacta":
                    hist[f["ruta_original"]].append(f)
            for r in sorted(set(hist) | {r for r in self.vigentes if linea_de(r) == "documentos"}):
                antes = " · ".join(f"[{f['commit']}]({self.enlace(doc, f['ruta_archivada'])})" for f in sorted(hist[r], key=lambda f: self.indice[f["commit"]]))
                vig = self.vigentes.get(r)
                L.append(f"| `{bajo_tipografia(r)}` | {antes or '—'} | " + (f"[{vig['id']}]({self.enlace(doc, r)})" if vig else "ya no está") + " |")
        self.escribir(f"versiones/{l}/README.md", L)

    def indice_versiones(self):
        doc = f"{ARCHIVO}/versiones/README.md"
        L = ["# Las versiones, por línea de trabajo", "",
             "Cada carpeta guarda una versión: lo que cambió en un commit, o lo que dejó la conversación o un artefacto en línea. "
             "Debajo de cada versión, los archivos conservan su ruta original desde `tipografia/`. Cada una tiene su `ficha.md`.", "",
             "| Línea | Versiones | Lo vigente |", "|---|---|---|"]
        for l in LINEAS:
            if l in self.por_linea:
                L.append(f"| [{LINEAS[l][0]}]({l}/README.md) | {len(self.por_linea[l])} | [`{self.vigente_de(l)}/`]({self.enlace(doc, self.vigente_de(l))}/) |")
        self.escribir("versiones/README.md", L)

    PEDIDOS_SIN_FECHA = [   # del resumen de la conversación (19.10.2026), en su orden; el commit al que llevan es deducción
        ("Pide correr descargar_imagenes.py para bajar las imágenes del atlas y rehacer la lámina: «Ya configuré el acceso a la red y guardé los cambios».", "976fbf0"),
        ("Comparte un reel de Instagram y un video de YouTube para simular el repujado sobre aluminio «realizando ingeniería inversa», y después adjunta el video.", "508401d"),
        ("Pregunta si la primera simulación era mejor y pide iterar lo mejor logrado.", None),
        ("«Igual para todas las simulaciones considero que se debería preveer que el pulso humano no es como el de una máquina».", "0cdccf1"),
        ("«Igual debería ser más sutil no tan evidente».", "0cdccf1"),
        ("«Bien ahora actualiza todos los documentos entregables que generamos hasta el momento».", "5b3708d"),
        ("Pide el prompt para que GPT Astra 6 arme un documento de alto diseño editorial, «estilo suizo», con cinco imágenes de referencia.", "en-linea_encargo"),
    ]
    PEDIDOS_FECHADOS = [
        ("2026-10-19T00:32", "antes de las 00:32 · ", "Pide hacer el diseño editorial: «Sabes que realiza tu este diseño editorial… Analiza las referencias para poder desarrollar un único documento editorial», con cinco referencias, y buscar una herramienta en GitHub."),
        ("2026-10-19T09:17", "", "«Intentar nuevamente / Continua con lo que estabas haciendo»."),
        ("2026-10-30T02:29", "", "Adjunta un reel y pide un control «como este, es decir también coherente con el proyecto» para la aplicación paramétrica."),
        ("2026-10-30T02:39", "", "«Ojo no te pido copiar la interfaz, ves el ejemplo de como desarrollar interfaces AD hoc a cada proyecto y que no todos sean iguales»."),
        ("2026-11-02T18:41", "", "Pide este archivo: organizar todo lo generado, con sus versiones e iteraciones."),
        ("2026-11-02T21:46", "", "«Continua», después de un reinicio de la sesión."),
    ]

    def linea_de_tiempo(self):
        doc = f"{ARCHIVO}/linea_de_tiempo.md"
        ev = []
        por_commit = defaultdict(list)
        for v in self.versiones:
            if v["origen"] == "git":
                por_commit[v["commit"]["c"]].append(v)
        for c in self.commits:
            enl = ", ".join(f"[{LINEAS[v['linea']][0].lower()}]({self.enlace(doc, self.ficha_de(v))})"
                            for v in por_commit[c["c"]])
            ev.append((c["fecha"], f"commit `{c['c']}` · {c['asunto']}" + (f" → {enl}" if enl else " (solo archivos compartidos con el artículo)")))
        for v in self.versiones:
            if v["origen"] != "git":
                origen = "conversación" if v["origen"] == "conversacion" else "en línea"
                ev.append((v["fecha"], f"{origen} · {v['asunto']} → [{LINEAS[v['linea']][0].lower()}]({self.enlace(doc, self.ficha_de(v))})"))
        for f, pre, t in self.PEDIDOS_FECHADOS:
            ev.append((dt.datetime.fromisoformat(f + ":00+00:00"), f"{pre}**pedido** · {t}"))
        ev.sort(key=lambda e: e[0])
        L = ["# Línea de tiempo", "",
             "Todo lo que se puede fechar, en orden. Las horas son UTC. Una fecha de commit dice cuándo entró algo en git, no cuándo se creó; "
             "las de la conversación, cuándo se escribió o se vio algo; las de los artefactos, cuándo se publicó esa versión. "
             "*Contenener una ruina*, la obra de Rebeca Paz Prada de la que sale el proyecto, es del 22 de agosto de 2026: ningún archivo tiene esa fecha.".replace("Contenener", "Contener"), "",
             f"[Volver al índice del archivo]({self.enlace(doc, ARCHIVO + '/README.md')}).", "",
             "## Antes del 19 de octubre: pedidos sin fecha", "",
             "La conversación de esas semanas no está en este contenedor. El resumen con que siguió anota estos pedidos, en este orden y sin fecha. "
             "El commit al que llevaron es una deducción del archivo, por el tema y el orden.", ""]
        for t, a in self.PEDIDOS_SIN_FECHA:
            if a and a.startswith("en-linea"):
                v = next(x for x in self.versiones if x["origen"] == "en-linea" and "encargo" in x["carpeta"])
                L.append(f"- {t} Lleva al [encargo editorial]({self.enlace(doc, self.ficha_de(v))}) (deducido).")
            elif a:
                c = next(x for x in self.commits if x["c"] == a)
                L.append(f"- {t} Lleva al commit `{a}` del {c['fecha']:%d.%m.%Y}, «{c['asunto']}» (deducido).")
            else:
                L.append(f"- {t}")
        dia = None
        L += ["", "## Día por día"]
        for f, t in ev:
            if f.date() != dia:
                dia = f.date()
                L += ["", f"### {dia:%Y-%m-%d}", ""]
            L.append(f"- **{f:%H:%M}** · {t}")
        self.escribir("linea_de_tiempo.md", L)

    def pendientes(self):
        doc = f"{ARCHIVO}/pendientes.md"
        ns = [f for f in self.filas if f["id"].startswith("N-")]
        reglas = [f for f in ns if f["copia"] == "no se archiva"]
        otros = [f for f in ns if f["copia"] != "no se archiva" and f["categoria"] not in ("compartido con otro proyecto", "residuo técnico")]
        compartidos = [f for f in self.filas if f["categoria"] == "compartido con otro proyecto"]
        dups = [f for f in self.filas if f["copia"] == "no se copia (duplicado exacto)"]
        L = ["# Pendientes, ausencias y dudas", "",
             f"Lo que falta en el archivo y por qué, lo que se registra sin copiarlo y lo que solo tú puedes confirmar. Cada fila tiene su número en `inventario.csv`. [Volver al índice]({self.enlace(doc, ARCHIVO + '/README.md')}).", "",
             "## Lo que no se archiva por decisión o por las reglas del proyecto", "",
             "| Id | Qué | Por qué no está aquí |", "|---|---|---|"]
        for f in reglas:
            L.append(f"| `{f['id']}` | {f['nombre']} | {f['observaciones']} |")
        L += ["", "## Lo que no está o no se pudo recuperar", "", "| Id | Qué | Qué pasó |", "|---|---|---|"]
        for f in otros:
            L.append(f"| `{f['id']}` | {f['nombre']} | {f['observaciones']} |")
        L += ["", "## Lo que se registra sin copiarlo", "",
              f"- **Los archivos de la raíz del repositorio** (`README.md` y `.gitignore`) cambiaron {len(compartidos)} veces con commits de *Contenida*, "
              "pero mezclan los dos proyectos: no se copian. Cada fila dice cómo recuperarlos con `git show`.",
              f"- **{len(dups)} duplicados exactos** de materiales que ya están archivados o vigentes: se anotan con el número del original. "
              + ", ".join(f"`{f['id']}` ({f['descripcion']})" for f in dups[:6]) + ("…" if len(dups) > 6 else "") + ".",
              "- **La caché de Python que se subió por error** el 30.09 y se borró en `deb0435`: se anota, no se copia.", "",
              "## Dudas que solo puedes resolver tú", "",
              "1. **«Contenedor» y «Vasijas».** Son dos artefactos de claude.ai del 27 y el 28 de septiembre, anteriores a esta conversación. "
              "Por su texto parecen el primer y el segundo intento de esta tipografía. ¿Son parte del proyecto? Si lo son, entran como antecedentes.",
              "2. **¿Hay algún entregable aprobado?** Ningún registro lo dice, así que nada figura como «entregable aprobado». Lo vigente es el estado actual de la rama.",
              "3. **¿Se usó el encargo para GPT Astra 6?** Figura como «alternativa» porque no consta.",
              "4. **¿Se borra el duplicado del artefacto del repujado** (`Y3FyvuU5q3hZjo9TW8qKor`)? Sigue publicado.",
              "5. **¿Cuándo se escribieron los textos de partida** (el poema, el pie de la lámina)? El archivo solo tiene la fecha del commit en que entraron.", "",
              "## Lo que el archivo deduce y conviene revisar", "",
              "- **El `app.js` de la versión 4 en línea** se toma del commit `1eaf342` porque mide lo mismo (21 438 bytes); no se comparó su contenido.",
              "- **Las fechas de las versiones en línea** salen de su identificador de versión, que es una marca de tiempo: con la versión 5 coincide con la publicación registrada (03:20 UTC del 30.10.2026).",
              "- **Los generadores marcados «deducido»** en el inventario no los nombra el propio generador ni su README.",
              "- **Lo que se retiró en `3f66520`** figura como «estado sin confirmar»: el commit dice que piel, copia y azulejo «quedan en pausa», no que se descarten.",
              "- **Los pedidos sin fecha** de la línea de tiempo se unen a un commit por su tema y su orden."]
        self.escribir("pendientes.md", L)

    def recursos_compartidos(self):
        doc = f"{ARCHIVO}/recursos_compartidos/README.md"
        grupos = [("Las letras", "tipografia/laminas/fuentes/", ["laminas/fuentes", "/fuentes/"]),
                  ("Los textos de partida", "tipografia/textos/", ["textos/", "poema.txt", "pie_de_lamina"]),
                  ("Los testigos del pie", "tipografia/simulacion/testigos/", ["testigos"]),
                  ("La gramática en JavaScript", "tipografia/aplicacion/", ["aplicacion/gramatica.js", "aplicacion/datos.js", "aplicacion/clipper.js"])]
        copias = defaultdict(list)
        for f in self.filas:
            if f["copia"] == "copia funcional (dependencia)" and f.get("_titular") is not None:
                copias[f["_titular"]["id"]].append(f)
            elif f["copia"] == "copia funcional (dependencia)" and f.get("_original"):
                t = self.titular(*f["_original"])
                if t:
                    copias[t["id"]].append(f)
        textos = {r: self.vigentes[r] for r in self.vigentes if posixpath.splitext(r)[1] in (".py", ".js", ".html", ".css", ".md")}
        L = ["# Recursos compartidos", "",
             "Lo que usan varias versiones y varias líneas a la vez. **No se copia aquí:** sigue en su lugar, vigente, y cada versión que lo necesita "
             "para abrir lleva su propia copia al lado (una «copia funcional», marcada en el inventario con el número del original). "
             "Moverlo a esta carpeta rompería las rutas con que lo llaman los archivos.", "",
             f"[Volver al índice]({self.enlace(doc, ARCHIVO + '/README.md')}).", ""]
        for titulo, carpeta, agujas in grupos:
            vig = [f for r, f in sorted(self.vigentes.items()) if r.startswith(carpeta)]
            if carpeta.endswith("aplicacion/"):
                vig = [f for f in vig if f["nombre"] in ("gramatica.js", "datos.js", "clipper.js")]
            usan = sorted({bajo_tipografia(r) for r, f in textos.items() if not r.startswith(carpeta)
                           and any(a in contenido(f["blob_git"]).decode("utf8", "ignore") for a in agujas)})
            L += [f"## {titulo}", "", f"En [`{carpeta}`]({self.enlace(doc, carpeta)}): {len(vig)} archivos vigentes.", ""]
            if usan:
                L.append("**Los nombran** (según su código o su texto): " + ", ".join(f"`{u}`" for u in usan[:16]) + (f" y {len(usan) - 16} más" if len(usan) > 16 else "") + ".")
                L.append("")
            L += ["| Id | Archivo | Desde el commit | Copias funcionales en versiones |", "|---|---|---|---|"]
            for f in vig[:40]:
                cs = copias.get(f["id"], [])
                L.append(f"| `{f['id']}` | `{bajo_tipografia(f['ruta_original'])}` | `{f['commit']}` | {len(cs)} |")
            if len(vig) > 40:
                L.append(f"| … | y {len(vig) - 40} más | | |")
            L.append("")
        self.escribir("recursos_compartidos/README.md", L)

    def readme(self):
        doc = f"{ARCHIVO}/README.md"
        cuenta = defaultdict(int)
        for f in self.filas:
            cuenta[f["id"][0]] += 1
        copiado = sum(int(f["bytes"] or 0) for f in self.filas if f["copia"] in
                      ("copia exacta", "copia funcional (dependencia)", "copia de la conversación", "copia reducida (de la conversación)", "copia de la versión en línea"))
        primero, ultimo = self.commits[0], self.cabeza
        L = ["# Archivo del proyecto *Contenida*", "",
             "Este archivo ordena lo que se produjo al desarrollar *Contenida*, la tipografía en homenaje a *Contener una ruina: acciones para "
             "desenterrar una voz*, de Rebeca Paz Prada. Reúne lo que quedó registrado en la rama del proyecto, en esta conversación y en los "
             "artefactos publicados en claude.ai. Sirve para ver qué se hizo, cómo cambió y recuperar cualquier versión anterior sin confundirla "
             "con la vigente.", "",
             "No es una versión nueva del proyecto ni una selección: guarda también las pruebas, los borradores y lo descartado. "
             "Los originales siguen en su lugar, sin cambios.", "",
             "## Qué abarca", "",
             f"- **Solo *Contenida*.** Es la carpeta `tipografia/` y sus {len(self.commits)} commits en la rama `{RAMA}`, del "
             f"{primero['fecha']:%d.%m} al {ultimo['fecha']:%d.%m.%Y} (de `{primero['c']}` a `{ultimo['c']}`). El repositorio guarda también "
             "el artículo *Altiplano* (la raíz, `articulo/` y `analisis/`, con su propia rama): es otro proyecto y queda fuera. Por eso este "
             "archivo está dentro de `tipografia/` y no en la raíz.",
             f"- **De git:** {cuenta['H']} versiones anteriores de archivos, copiadas tal cual, y los {cuenta['V']} archivos vigentes, "
             "registrados en su lugar.",
             f"- **De la conversación:** {cuenta['C']} piezas que no entraron en git como estaban: borradores, una propuesta descartada, "
             "pruebas y las imágenes de prueba que se vieron.",
             f"- **En línea:** {cuenta['L']} registros de los artefactos del proyecto en claude.ai, con sus copias.",
             f"- **Copias funcionales:** {cuenta['D']} dependencias copiadas al lado de las páginas y los SVG que las piden, para que abran.",
             f"- **Lo que falta:** {cuenta['N']} registros de lo que no se archiva o no está, con el motivo. Están en "
             f"[pendientes.md]({self.enlace(doc, ARCHIVO + '/pendientes.md')}).",
             f"- **Peso de lo copiado:** {copiado / 1e6:.0f} MB. Lo que viene de git no agranda el repositorio: git guarda una sola vez cada contenido.", "",
             "## Cómo está ordenado", "", "```",
             "archivo_del_proyecto/",
             "├── README.md               esta guía",
             "├── inventario.csv          un registro por material, con su procedencia",
             "├── linea_de_tiempo.md      todo lo que tiene fecha, en orden",
             "├── pendientes.md           lo que falta, lo que no se copia y las dudas",
             "├── verificacion.md         lo que se comprobó y cómo",
             "├── versiones/              las versiones, por línea de trabajo",
             "│   └── <línea>/",
             "│       ├── README.md       sus versiones, en orden",
             "│       └── AAAA-MM-DD_HHMM_<origen>_<nombre>/",
             "│           ├── ficha.md    qué es, qué cambió y qué lo respalda",
             "│           └── …           los archivos, con su ruta original desde tipografia/",
             "├── recursos_compartidos/   lo que usan varias versiones (sigue en su lugar)",
             "└── herramientas/           el guion que armó el archivo y el que lo verifica",
             "```", "",
             f"- [inventario.csv](inventario.csv) · [linea_de_tiempo.md](linea_de_tiempo.md) · [pendientes.md](pendientes.md) · "
             f"[verificacion.md](verificacion.md) · [versiones/](versiones/README.md) · [recursos_compartidos/](recursos_compartidos/README.md) · "
             f"[herramientas/](herramientas/)", "",
             "## Las líneas de trabajo", "",
             "| Línea | Versiones | Lo vigente, en su lugar |", "|---|---|---|"]
        for l in LINEAS:
            if l in self.por_linea:
                vs = self.por_linea[l]
                n = {o: sum(1 for v in vs if v["origen"] == o) for o in ("git", "conversacion", "en-linea")}
                det = f"{n['git']} de git" + (f", {n['conversacion']} de la conversación" if n["conversacion"] else "") + (f", {n['en-linea']} en línea" if n["en-linea"] else "")
                L.append(f"| [{LINEAS[l][0]}](versiones/{l}/README.md) | {det} | [`{self.vigente_de(l)}/`]({self.enlace(doc, self.vigente_de(l))}/) |")
        L += ["", "## Cómo se lee", "",
              "### Las carpetas de versión", "",
              "Se llaman `AAAA-MM-DD_HHMM_<origen>_<nombre>`: la fecha y la hora (UTC), el origen (el commit, `conversacion` o `en-linea`) y "
              "unas palabras del commit o de lo que es. No hay números de versión: el proyecto no los usó y el archivo no los inventa.", "",
              "Cada carpeta guarda **lo que en esa versión era distinto de lo vigente**: lo que cambió en ese commit y ya no está así. Lo que "
              "no cambió está en una carpeta anterior o sigue vigente en su lugar. La ficha dice cuántos archivos tenía la versión completa, y "
              "el inventario dice cuáles (columna `en_versiones`). Debajo de cada carpeta, los archivos conservan su ruta desde `tipografia/` "
              "para que sus enlaces funcionen. Por eso las páginas HTML y los SVG llevan al lado copias de lo que piden: imágenes, estilos, "
              "letras y guiones.", "",
              "### Los estados", "",
              "Cada material lleva uno, y solo cuando hay un registro que lo sostenga:", "",
              "- **Versión vigente:** el estado actual de la rama, o la última versión publicada en línea. Es lo más reciente, no lo aprobado.",
              "- **Versión anterior:** la reemplazó un commit posterior, o es un estado intermedio que dejó la conversación antes del commit.",
              "- **Alternativa:** otro camino para lo mismo. Es el caso del encargo editorial para otra IA.",
              "- **Prueba o experimento:** lo que sirvió para comprobar: guiones de prueba, capturas, vistas de páginas.",
              "- **Material descartado:** lo que un commit o un mensaje sacó del proyecto. Su ficha o su fila citan el registro.",
              "- **Estado sin confirmar:** lo que salió sin que el registro diga por qué, o lo que no se sabe si es del proyecto.",
              "- **Entregable aprobado:** ninguno, porque en los registros no consta una aprobación.", "",
              "Las referencias de terceros, como los videos y las imágenes de otros libros, no llevan estado: no son material del proyecto.", "",
              "### Las fechas", "",
              "Cada fecha dice qué representa, en la columna `que_representa_la_fecha`:", "",
              "- **La de un commit** es cuándo entró ese contenido en git. No es la fecha en que se creó la obra, ni necesariamente la del archivo.",
              "- **La de la conversación** es cuándo se escribió o se vio algo.",
              "- **La de un artefacto** es cuándo se publicó esa versión, deducida de su identificador.", "",
              "La obra de Rebeca Paz Prada es del 22 de agosto de 2026: ningún archivo del proyecto tiene esa fecha.", "",
              "### Los números del inventario", "",
              "| Prefijo | Qué es |", "|---|---|",
              "| `V-` | Vigente, en su lugar: no se copia |",
              "| `H-` | Versión anterior recuperada de git: copia exacta |",
              "| `D-` | Copia funcional de una dependencia: el original tiene su propio número |",
              "| `C-` | De la conversación |",
              "| `L-` | De un artefacto en línea |",
              "| `N-` | Lo que no se archiva o no está |", "",
              "### Las copias y los duplicados", "",
              "Todo se comparó por contenido, con SHA-256 y con el hash de git. Un contenido que ya está archivado o vigente no se copia otra "
              "vez: se anota como «duplicado exacto», con el número del original. Las copias funcionales son la única repetición, y se hacen "
              "para que una versión abra. No cuentan como duplicado otra exportación, otro formato o una copia reducida: un .docx y su PDF, una "
              "lámina en HTML y en PNG, una captura y la copia reducida que guardó la conversación.", "",
              "### Lo documentado y lo deducido", "",
              "Las fichas separan lo que respalda cada versión (el mensaje del commit, un mensaje del pedido, el README de esa versión) de lo "
              "que deduce el archivo, como el estado. Ninguna decisión se atribuye al autor sin un registro, y lo que es deducción se dice.", "",
              "## La versión vigente", "",
              f"Está en su lugar, en [`tipografia/`]({self.enlace(doc, 'tipografia')}/), y no se copia. El inventario la registra con su número "
              "`V-`, su hash y el commit en que entró cada archivo. En línea, lo vigente son los artefactos «Gramática de Contenida» (versión 5) "
              "y «El repujado de Contenida», copiados en sus líneas.", "",
              "## Cómo recuperar una versión", "",
              "- **Un archivo:** copia el de su carpeta de versión. Es idéntico al de git: tiene el mismo hash.",
              "- **Desde git, sin pasar por el archivo:** `git show <commit>:<ruta>`. Por ejemplo, "
              "`git show e8962b4:tipografia/aplicacion/app.js` da la aplicación de septiembre.",
              "- **El repositorio entero como estaba:** `git worktree add ../contenida_<commit> <commit>`. Sirve para rehacer los resultados "
              "con sus generadores, que leen de varias carpetas a la vez.", "",
              "## Verificación", "",
              "[verificacion.md](verificacion.md) dice qué se comprobó y con qué resultado. Para repetirlo, desde la raíz del repositorio:", "",
              "```bash", "python3 tipografia/archivo_del_proyecto/herramientas/verificar_archivo.py", "```", "",
              "El armado se puede leer en `herramientas/armar_archivo.py`. Su parte de git se puede rehacer en cualquier copia del "
              "repositorio; la de la conversación necesita su registro, que no está en el repositorio.", "",
              "## Asistencia de IA", "",
              "Este archivo lo armó Claude a pedido de quien lleva el proyecto. Ordena y registra; no decide. Lo que deduce, lo dice."]
        self.escribir("README.md", L)


def main():
    ap = argparse.ArgumentParser(description="Arma tipografia/archivo_del_proyecto/.")
    ap.add_argument("--conversacion", type=Path, help="el registro de la conversación (.jsonl)")
    ap.add_argument("--scratch", type=Path, help="la carpeta de trabajo de la sesión")
    ap.add_argument("--artefactos", type=Path, help="las páginas descargadas de los artefactos")
    ap.add_argument("--video", type=Path, help="el video adjunto (solo se registra)")
    args = ap.parse_args()
    raiz = Path(git("rev-parse", "--show-toplevel").strip())
    if Path.cwd() != raiz:
        sys.exit("Córrelo desde la raíz del repositorio.")
    destino = raiz / ARCHIVO
    if destino.exists():
        shutil.rmtree(destino)
    a = Archivo(raiz, destino)
    a.desde_git()
    if args.conversacion:
        a.conversacion(args.conversacion, args.scratch, args.artefactos)
    a.ausentes(args.video, args.scratch / "video_ui" if args.scratch else None)
    a.numerar()
    a.escribir_inventario()
    a.escribir_documentos()
    herr = destino / "herramientas"
    herr.mkdir(exist_ok=True)
    aqui = Path(__file__).resolve()
    shutil.copy2(aqui, herr / "armar_archivo.py")
    if aqui.with_name("verificar_archivo.py").exists():
        shutil.copy2(aqui.with_name("verificar_archivo.py"), herr / "verificar_archivo.py")
    cuenta = defaultdict(int)
    for f in a.filas:
        cuenta[f["id"][0]] += 1
    print("listo:", dict(cuenta), "| versiones:", len(a.versiones))


if __name__ == "__main__":
    main()
