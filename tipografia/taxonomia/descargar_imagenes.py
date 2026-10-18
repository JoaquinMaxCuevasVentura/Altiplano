"""Baja las imágenes de dominio público de las referencias, para el atlas de la taxonomía (R-09).

Uso (desde la raíz del repositorio):
    pip install pillow
    python3 tipografia/taxonomia/descargar_imagenes.py [--solo hauy] [--rehacer]

Para cada referencia abre su página (IMAGENES, en taxonomia.py) y baja su imagen a
tipografia/taxonomia/imagenes/<clave>.jpg, con 1600 px como máximo. Anota de dónde
salió en imagenes/fuentes.json: la página, la imagen, la licencia y la fecha.

Cómo encuentra la imagen:
- si la referencia trae `imagen`, esa dirección;
- si trae `commons`, el archivo de Wikimedia Commons, con la licencia que dice Commons;
- en la Wellcome Collection, la página `pagina_libro` del libro, por su API (IIIF);
- si no, la imagen que la página declara como suya (og:image). En el Public Domain
  Image Archive se pide el original y no el recorte de 1200 × 630 para redes.

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
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from urllib.parse import urljoin

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import taxonomia as T  # noqa: E402

CARPETA = AQUI / "imagenes"
AGENTE = "ContenidaAtlas/1.0 (+https://github.com/JoaquinMaxCuevasVentura/Altiplano; investigación)"
MAXIMO = 1600

ETIQUETA = re.compile(r"<meta\s[^>]*?(?:property|name)\s*=\s*[\"'](?:og:image(?::secure_url)?|twitter:image(?::src)?)"
                      r"[\"'][^>]*>", re.I)
CONTENIDO = re.compile(r"content\s*=\s*[\"']([^\"']+)[\"']", re.I)
ENLACE = re.compile(r"<link\s[^>]*rel\s*=\s*[\"']image_src[\"'][^>]*href\s*=\s*[\"']([^\"']+)", re.I)


def pedir(url, acepta="text/html", intentos=4):
    """Pide una dirección; si el servidor corta o pide calma (429, 5xx), espera y vuelve a pedir."""
    pedido = urllib.request.Request(url, headers={"User-Agent": AGENTE, "Accept": f"{acepta},*/*;q=0.8"})
    for n in range(intentos):
        try:
            with urllib.request.urlopen(pedido, timeout=60) as r:
                return r.read(), r.geturl()
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504) or n == intentos - 1:
                raise
        except (urllib.error.URLError, ConnectionError, TimeoutError):
            if n == intentos - 1:
                raise
        time.sleep(2 ** (n + 1))


def imagen_de(pagina, base):
    """La imagen que la página declara como suya: og:image, twitter:image o image_src."""
    for etiqueta in ETIQUETA.finditer(pagina):
        c = CONTENIDO.search(etiqueta.group(0))
        if c:
            return urljoin(base, html.unescape(c.group(1)))
    m = ENLACE.search(pagina)
    return urljoin(base, html.unescape(m.group(1))) if m else None


def original(url):
    """El Public Domain Image Archive declara un recorte para redes; se pide la imagen entera."""
    partes = urllib.parse.urlsplit(url)
    if partes.netloc == "images.pdimagearchive.org":
        return urllib.parse.urlunsplit(partes._replace(query=f"width={MAXIMO}"))
    return url


def de_wellcome(pagina, indice):
    """La página `indice` de un libro de la Wellcome Collection, por su API y su servidor IIIF."""
    obra = pagina.rstrip("/").rsplit("/", 1)[-1]
    datos, _ = pedir(f"https://api.wellcomecollection.org/catalogue/v2/works/{obra}?include=items", "application/json")
    manifiesto = next(l["url"] for it in json.loads(datos)["items"] for l in it["locations"]
                      if l.get("url", "").startswith("https://iiif.wellcomecollection.org/presentation"))
    datos, _ = pedir(manifiesto, "application/json")
    lienzo = json.loads(datos)["sequences"][0]["canvases"][indice]
    servicio = lienzo["images"][0]["resource"]["service"]
    servicio = servicio if isinstance(servicio, dict) else servicio[0]
    return f"{servicio['@id']}/full/!{MAXIMO},{MAXIMO}/0/default.jpg"


def de_commons(archivo):
    """Un archivo de Wikimedia Commons: su dirección y la licencia que declara Commons."""
    q = urllib.parse.urlencode(dict(action="query", titles=archivo, prop="imageinfo", iiprop="url|extmetadata",
                                    iiurlwidth=MAXIMO, format="json"))
    datos, _ = pedir(f"https://commons.wikimedia.org/w/api.php?{q}", "application/json")
    info = next(iter(json.loads(datos)["query"]["pages"].values()))["imageinfo"][0]
    licencia = info.get("extmetadata", {}).get("LicenseShortName", {}).get("value", "")
    return info.get("thumburl") or info["url"], licencia


def guardar(datos, destino):
    from PIL import Image
    im = Image.open(io.BytesIO(datos)).convert("RGB")
    im.thumbnail((MAXIMO, MAXIMO))
    im.save(destino, "JPEG", quality=88)
    return im.size


def bajar(k, I):
    """Devuelve (dirección de la imagen, licencia, bytes)."""
    licencia = I["licencia"]
    if I.get("imagen"):
        url = I["imagen"]
    elif I.get("commons"):
        url, lic = de_commons(I["commons"])
        licencia = f"{lic}, según Wikimedia Commons" if lic else licencia
    elif "wellcomecollection.org/works/" in I["pagina"]:
        url = de_wellcome(I["pagina"], I.get("pagina_libro", 0))
    else:
        pagina, base = pedir(I["pagina"])
        url = imagen_de(pagina.decode("utf8", "replace"), base)
        if not url:
            raise ValueError("la página no declara una imagen")
        url = original(url)
    datos, _ = pedir(url, "image/*")
    return url, licencia, datos


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
            url, licencia, datos = bajar(k, I)
            ancho, alto = guardar(datos, destino)
        except Exception as e:  # noqa: BLE001 — se anota y se sigue con la siguiente
            fallas.append(k)
            print(f"  ! {k}: {e}")
            continue
        registro[k] = dict(pagina=I["pagina"], imagen=url, licencia=licencia,
                           fecha=datetime.date.today().isoformat(), px=[ancho, alto])
        bajadas += 1
        print(f"  {k}: {ancho} × {alto} px · {licencia}")
        time.sleep(0.5)            # sin apurar a los archivos
    ruta_registro.write_text(json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf8")
    print(f"{bajadas} bajadas; {len(fallas)} sin bajar{': ' + ', '.join(fallas) if fallas else ''}")
    if fallas:
        print("Si la red las bloquea (un 403), hay que permitir esos dominios. También se pueden poner a mano en "
              "imagenes/, con el nombre de su clave.")


if __name__ == "__main__":
    main()
