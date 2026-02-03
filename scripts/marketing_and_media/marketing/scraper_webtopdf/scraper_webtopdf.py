#!/usr/bin/env python3
"""
Script para generar documentos PDF estilo Word desde contenido de páginas web.
Extrae contenido principal y aplica formato profesional optimizado para SEO.
"""

import argparse
import sys
import subprocess
import platform
import tempfile
import base64
from pathlib import Path
from urllib.parse import urlparse, urljoin


def install_dependencies():
    """
    Instala automáticamente las dependencias necesarias.
    """
    required_packages = {
        'requests': 'requests>=2.31.0',
        'bs4': 'beautifulsoup4>=4.12.0',
        'weasyprint': 'weasyprint>=60.0',
        'lxml': 'lxml>=4.9.0',
        'readability': 'readability-lxml>=0.8.1'
    }

    packages_to_install = []

    for module_name, package_spec in required_packages.items():
        try:
            __import__(module_name)
        except ImportError:
            packages_to_install.append(package_spec)

    if packages_to_install:
        print("Instalando dependencias necesarias...")
        print(f"Paquetes a instalar: {', '.join(packages_to_install)}")

        try:
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install'] + packages_to_install,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE
            )
            print("Dependencias instaladas exitosamente.\n")
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar dependencias: {e}")
            sys.exit(1)


def show_gtk_installation_help():
    """
    Muestra instrucciones para instalar GTK en Windows.
    """
    print("\n" + "="*70)
    print("ERROR: WeasyPrint requiere GTK para funcionar en Windows")
    print("="*70)
    print("\nPara solucionar este problema:")
    print("\n1. Descarga e instala GTK3 Runtime para Windows desde:")
    print("   https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases")
    print("\n2. Descarga el archivo: gtk3-runtime-x.x.x-x-x-x-ts-win64.exe")
    print("   (donde x.x.x son números de versión)")
    print("\n3. Ejecuta el instalador y sigue las instrucciones")
    print("\n4. Reinicia tu terminal/PowerShell")
    print("\n5. Vuelve a ejecutar este script")
    print("\n" + "="*70)
    print("\nAlternativamente, puedes usar este script en Linux o macOS")
    print("donde WeasyPrint funciona sin configuración adicional.")
    print("="*70 + "\n")


# Instalar dependencias al inicio
install_dependencies()

# Importar módulos después de asegurar que están instalados
try:
    import requests
    from bs4 import BeautifulSoup
    from readability import Document
except ImportError as e:
    print(f"Error crítico al importar módulos: {e}")
    sys.exit(1)

# Intentar importar WeasyPrint con manejo especial de errores para Windows
try:
    from weasyprint import HTML
except OSError as e:
    if platform.system() == 'Windows' and 'libgobject' in str(e):
        show_gtk_installation_help()
        sys.exit(1)
    else:
        print(f"Error al cargar WeasyPrint: {e}")
        sys.exit(1)
except ImportError as e:
    print(f"Error crítico al importar WeasyPrint: {e}")
    sys.exit(1)


# Plantilla CSS estilo documento Word profesional
WORD_STYLE_CSS = """
@page {
    size: A4;
    margin: 2.5cm;
}

body {
    font-family: Calibri, 'Segoe UI', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.5;
    color: #000000;
    text-align: justify;
    margin: 0;
    padding: 0;
}

h1, h2, h3, h4, h5, h6 {
    font-family: Cambria, Georgia, 'Times New Roman', serif;
    font-weight: bold;
    margin-top: 1.2em;
    margin-bottom: 0.6em;
    page-break-after: avoid;
}

h1 {
    font-size: 14pt;
    color: #000000;
    margin-top: 0;
    margin-bottom: 1em;
}

h2 {
    font-size: 13pt;
    color: #2E75B5;
    margin-top: 1.5em;
}

h3 {
    font-size: 11pt;
    color: #2E75B5;
}

h4 {
    font-size: 11pt;
    color: #000000;
}

h5, h6 {
    font-size: 10pt;
    color: #000000;
}

p {
    margin-top: 0;
    margin-bottom: 0.8em;
    orphans: 3;
    widows: 3;
}

a {
    color: #0563C1;
    text-decoration: underline;
}

a:hover {
    color: #0563C1;
}

img {
    max-width: 80%;
    height: auto;
    display: block;
    margin: 1.5em auto;
    page-break-inside: avoid;
}

ul, ol {
    margin-top: 0.5em;
    margin-bottom: 0.8em;
    padding-left: 1.5em;
}

li {
    margin-bottom: 0.3em;
}

blockquote {
    margin: 1em 2em;
    padding-left: 1em;
    border-left: 3px solid #2E75B5;
    font-style: italic;
    color: #333333;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}

table, th, td {
    border: 1px solid #CCCCCC;
}

th, td {
    padding: 0.5em;
    text-align: left;
}

th {
    background-color: #F2F2F2;
    font-weight: bold;
}

code {
    font-family: 'Courier New', Consolas, monospace;
    background-color: #F5F5F5;
    padding: 0.1em 0.3em;
    border-radius: 3px;
    font-size: 10pt;
}

pre {
    font-family: 'Courier New', Consolas, monospace;
    background-color: #F5F5F5;
    padding: 1em;
    border-radius: 3px;
    overflow-x: auto;
    font-size: 9pt;
    line-height: 1.4;
}

strong, b {
    font-weight: bold;
}

em, i {
    font-style: italic;
}
"""


class WebToPDF:
    """Clase para convertir páginas web a PDF con formato estilo Word"""

    def __init__(self, url, output_path=None):
        """
        Inicializa el conversor.

        Args:
            url (str): URL de la página web
            output_path (str): Ruta del archivo PDF de salida
        """
        self.url = url

        # Generar nombre de archivo si no se proporciona
        if output_path:
            self.output_path = Path(output_path)
        else:
            # Usar el dominio y path como nombre
            parsed = urlparse(url)
            filename = f"{parsed.netloc}_{parsed.path.replace('/', '_')}.pdf"
            filename = filename.replace('__', '_').strip('_')
            if not filename.endswith('.pdf'):
                filename += '.pdf'
            self.output_path = Path(filename)

    def fetch_content(self):
        """
        Obtiene el contenido HTML de la URL.

        Returns:
            str: Contenido HTML
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise Exception(f"Error al obtener la página: {e}")

    def download_image(self, img_url):
        """
        Descarga una imagen y la convierte a base64.

        Args:
            img_url (str): URL de la imagen

        Returns:
            str: Imagen en formato data URI base64
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(img_url, headers=headers, timeout=10)
            response.raise_for_status()

            # Detectar tipo de contenido
            content_type = response.headers.get('content-type', 'image/jpeg')

            # Convertir a base64
            img_base64 = base64.b64encode(response.content).decode('utf-8')
            return f"data:{content_type};base64,{img_base64}"
        except Exception as e:
            print(f"  ! Error descargando imagen {img_url}: {e}")
            return None

    def extract_main_content(self, html_content):
        """
        Extrae el contenido principal del artículo usando Readability.

        Args:
            html_content (str): Contenido HTML original

        Returns:
            tuple: (título, contenido HTML)
        """
        # PRIMERO extraer las imágenes del HTML original ANTES de procesarlo
        original_soup = BeautifulSoup(html_content, 'html.parser')
        original_images = []

        # Buscar en el artículo/main/contenido principal
        main_content = (original_soup.find('article') or
                       original_soup.find('main') or
                       original_soup.find(class_=['entry-content', 'post-content', 'article-content']) or
                       original_soup)

        # Buscar TODAS las imágenes
        for img in main_content.find_all('img'):
            # Buscar en TODOS los posibles atributos de lazy loading
            src = (img.get('nitro-lazy-src') or  # Nitro CDN primero!
                   img.get('data-nitro-lazy-src') or
                   img.get('data-src') or
                   img.get('data-lazy-src') or
                   img.get('data-original') or
                   img.get('data-lazy') or
                   img.get('src') or
                   '')

            # Si src está vacío, buscar en srcset o nitro-lazy-srcset
            if not src or src.startswith('data:image/svg'):
                srcset = img.get('nitro-lazy-srcset') or img.get('data-srcset') or img.get('srcset') or ''
                if srcset:
                    # Tomar la primera URL del srcset (la más pequeña generalmente)
                    first_src = srcset.split(',')[0].strip().split()[0]
                    if first_src and not first_src.startswith('data:'):
                        src = first_src

            # Solo agregar si es una URL válida
            if src and not src.startswith('data:') and src != '' and 'http' in src:
                full_url = urljoin(self.url, src)
                alt = img.get('alt', '')
                original_images.append({'url': full_url, 'alt': alt})
                print(f"  + Imagen detectada: {alt[:50]}")

        print(f"  Total imágenes encontradas en HTML original: {len(original_images)}")

        # Usar Readability para extraer el contenido
        doc = Document(html_content)
        title = doc.title()
        content = doc.summary()

        # Limpiar y mejorar el HTML extraído
        soup = BeautifulSoup(content, 'html.parser')

        # Eliminar elementos no deseados
        for tag in soup.find_all(['script', 'style', 'iframe', 'nav', 'footer', 'aside']):
            tag.decompose()

        # Descargar y reemplazar imágenes con data URIs
        img_tags = soup.find_all('img')
        print(f"  Imágenes en contenido extraído: {len(img_tags)}")

        if img_tags and original_images:
            print("  Descargando imágenes...")
            for idx, img in enumerate(img_tags):
                if idx < len(original_images):
                    img_data = original_images[idx]
                    print(f"    Descargando: {img_data['url']}")

                    # Descargar y convertir a base64
                    data_uri = self.download_image(img_data['url'])
                    if data_uri:
                        img['src'] = data_uri
                        img['alt'] = img_data['alt']
                        img.attrs = {'src': data_uri, 'alt': img_data['alt']}
                        print(f"    OK - Imagen {idx + 1} embebida")
                    else:
                        print(f"    ERROR - No se pudo descargar imagen {idx + 1}")

        # Limpiar atributos de otros elementos
        for tag in soup.find_all(True):
            if tag.name == 'a' and tag.has_attr('href'):
                href = urljoin(self.url, tag['href'])
                tag.attrs = {'href': href}
            elif tag.name != 'img':
                tag.attrs = {}

        return title, str(soup)

    def create_html_document(self, title, content):
        """
        Crea el documento HTML completo con estilos CSS.

        Args:
            title (str): Título del documento
            content (str): Contenido HTML del artículo

        Returns:
            str: Documento HTML completo
        """
        html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
    {WORD_STYLE_CSS}
    </style>
</head>
<body>
    <h1>{title}</h1>
    {content}
</body>
</html>
"""
        return html_template

    def generate_pdf(self):
        """
        Genera el archivo PDF desde la URL.

        Returns:
            Path: Ruta del archivo PDF generado
        """
        print(f"Obteniendo contenido de: {self.url}")
        html_content = self.fetch_content()

        print("Extrayendo contenido principal del artículo...")
        title, main_content = self.extract_main_content(html_content)

        print("Aplicando formato estilo Word profesional...")
        final_html = self.create_html_document(title, main_content)

        print(f"Generando PDF: {self.output_path}")

        try:
            # Convertir HTML a PDF usando WeasyPrint
            HTML(string=final_html, base_url=self.url).write_pdf(
                target=str(self.output_path)
            )
            print(f"PDF generado exitosamente: {self.output_path.absolute()}")
            return self.output_path
        except Exception as e:
            raise Exception(f"Error al generar PDF: {e}")


def main():
    """Función principal del script"""
    parser = argparse.ArgumentParser(
        description='Genera un documento PDF estilo Word desde el contenido de una página web',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python web_to_pdf.py https://example.com
  python web_to_pdf.py https://example.com -o mi-documento.pdf
  python web_to_pdf.py https://octonove.com/posicionar-en-google/ -o seo-guide.pdf

El PDF generado incluirá:
  - Contenido principal del artículo (sin menús, sidebar, footer)
  - Formato estilo documento Word profesional
  - Enlaces clickeables preservados
  - Estilos: H1 Cambria 14pt, H2 Cambria 13pt azul, H3 Cambria 11pt azul
  - Párrafos: Calibri 11pt, justificado
  - Imágenes centradas
        """
    )

    parser.add_argument(
        'url',
        help='URL de la página web a convertir'
    )

    parser.add_argument(
        '-o', '--output',
        help='Ruta del archivo PDF de salida (opcional)',
        default=None
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Mostrar información detallada'
    )

    args = parser.parse_args()

    # Validar URL
    if not args.url.startswith(('http://', 'https://')):
        print("Error: La URL debe comenzar con http:// o https://")
        sys.exit(1)

    try:
        converter = WebToPDF(
            url=args.url,
            output_path=args.output
        )

        converter.generate_pdf()

    except KeyboardInterrupt:
        print("\n\nProceso interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
