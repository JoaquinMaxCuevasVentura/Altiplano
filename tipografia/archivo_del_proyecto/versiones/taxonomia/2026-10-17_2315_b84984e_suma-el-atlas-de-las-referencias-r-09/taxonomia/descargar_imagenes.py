"""Baja las imágenes de dominio público de las referencias, para el atlas de la taxonomía (R-09).

Uso (desde la raíz del repositorio):
    pip install pillow
    python3 tipografia/taxonomia/descargar_imagenes.py [--solo hauy] [--rehacer]

Para cada referencia abre su página (IMAGENES, en taxonomia.py), toma la imagen
que la página declara como suya (og:image) y la guarda en
tipografia/taxonomia/imagenes/<clave>.jpg, con 1600 px como máximo. Anota de
dónde salió en imagenes/fuentes.json: la página, la imagen, la licencia y la fecha.

La carpeta imagenes/ no entra en el repositorio (06, §6.4): lo ajeno se cita y no
se sube. Las fotos de hoy (el Smithsonian, Perkins, el museo de la APH, The Paris
Review) no se bajan. Una imagen también se puede poner a mano, con el nombre de
su clave: imagenes/hauy.jpg.

Después: python3 tipografia/taxonomia/generar_taxonomia.py
"""

import argparse
import datetime
import html
import io
import json
import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urljoin

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import taxonomia as T  # noqa: E402

CARPETA = AQUI / "imagenes"
AGENTE = "Mozilla/5.0 (compatible; Contenida, atlas de referencias de dominio publico)"
MAXIMO = 1600

ETIQUETA = re.compile(r"<meta\s[^>]*?(?:property|name)\s*=\s*[\"'](?:og:image(?::secure_url)?|twitter:image(?::src)?)"
                      r"[\"'][^>]*>", re.I)
CONTENIDO = re.compile(r"content\s*=\s*[\"']([^\"']+)[\"']", re.I)
ENLACE = re.compile(r"<link\s[^>]*rel\s*=\s*[\"']image_src[\"'][^>]*href\s*=\s*[\"']([^\"']+)", re.I)


def pedir(url, acepta="text/html"):
    pedido = urllib.request.Request(url, headers={"User-Agent": AGENTE, "Accept": f"{acepta},*/*;q=0.8"})
    with urllib.request.urlopen(pedido, timeout=40) as r:
        return r.read(), r.geturl()


def imagen_de(pagina, base):
    """La imagen que la página declara como suya: og:image, twitter:image o image_src."""
    for etiqueta in ETIQUETA.finditer(pagina):
        c = CONTENIDO.search(etiqueta.group(0))
        if c:
            return urljoin(base, html.unescape(c.group(1)))
    m = ENLACE.search(pagina)
    return urljoin(base, html.unescape(m.group(1))) if m else None


def guardar(datos, destino):
    from PIL import Image
    im = Image.open(io.BytesIO(datos)).convert("RGB")
    im.thumbnail((MAXIMO, MAXIMO))
    im.save(destino, "JPEG", quality=88)
    return im.size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--solo", help="solo esta referencia (su clave: hauy, chladni…)")
    ap.add_argument("--rehacer", action="store_true", help="vuelve a bajar las que ya están")
    args = ap.parse_args()
    CARPETA.mkdir(exist_ok=True)
    ruta_registro = CARPETA / "fuentes.json"
    registro = json.loads(ruta_registro.read_text(encoding="utf8")) if ruta_registro.exists() else {}
    bajadas, fallas = 0, []
    for k, I in T.IMAGENES.items():
        if args.solo and k != args.solo:
            continue
        destino = CARPETA / f"{k}.jpg"
        if not I.get("descarga", True):
            print(f"  {k}: no se baja ({I['licencia']})")
            continue
        if destino.exists() and not args.rehacer:
            print(f"  {k}: ya está")
            continue
        try:
            pagina, base = pedir(I["pagina"])
            url = imagen_de(pagina.decode("utf8", "replace"), base)
            if not url:
                raise ValueError("la página no declara una imagen")
            datos, _ = pedir(url, "image/*")
            ancho, alto = guardar(datos, destino)
        except Exception as e:  # noqa: BLE001 — se anota y se sigue con la siguiente
            fallas.append(k)
            print(f"  ! {k}: {e}")
            continue
        registro[k] = dict(pagina=I["pagina"], imagen=url, licencia=I["licencia"],
                           fecha=datetime.date.today().isoformat(), px=[ancho, alto])
        bajadas += 1
        print(f"  {k}: {ancho} × {alto} px · {I['licencia']}")
    ruta_registro.write_text(json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf8")
    print(f"{bajadas} bajadas; {len(fallas)} sin bajar{': ' + ', '.join(fallas) if fallas else ''}")
    if fallas:
        print("Si la red las bloquea (un 403), hay que permitir esos dominios. También se pueden poner a mano en "
              "imagenes/, con el nombre de su clave.")


if __name__ == "__main__":
    main()
