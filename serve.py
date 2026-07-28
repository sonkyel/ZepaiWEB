"""Servidor local para probar la web tal y como la sirve Vercel.

Vercel tiene "cleanUrls": true, asi que /consultoria-ia sirve
consultoria-ia.html. El servidor de Python no hace eso por su cuenta, y por
eso los enlaces de las paginas nuevas daban 404 en local.

Uso:
    python serve.py          -> http://localhost:8000
    python serve.py 8765     -> http://localhost:8765
"""
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class CleanUrlHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        local = super().translate_path(path)
        # Sin extension: el .html equivalente gana, incluso si existe un
        # directorio con ese nombre (/blog sirve blog.html, no el listado de
        # blog/). Asi se evita la redireccion 301 a /blog/, que chocaria con
        # trailingSlash:false y con el canonical.
        if not os.path.splitext(local)[1]:
            html = local.rstrip("/\\") + ".html"
            if os.path.isfile(html):
                return html
        return local

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("Sirviendo en http://localhost:%d  (Ctrl+C para parar)" % port)
    ThreadingHTTPServer(("", port), CleanUrlHandler).serve_forever()
