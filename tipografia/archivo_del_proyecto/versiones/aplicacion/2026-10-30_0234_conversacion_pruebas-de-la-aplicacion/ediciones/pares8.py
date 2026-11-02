PARES = [
    ('''def chromium():
    for c in [os.environ.get("CHROMIUM"), "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"]:
        if c and Path(c).exists():
            return c
    return None''',
     '''def chromium():
    """El de la variable CHROMIUM o, si no, el de Playwright, sea cual sea su versión."""
    playwright = sorted(Path("/opt/pw-browsers").glob("chromium-*/chrome-linux*/chrome"), reverse=True)
    for c in [os.environ.get("CHROMIUM"), *map(str, playwright)]:
        if c and Path(c).exists():
            return c
    return None'''),
]
