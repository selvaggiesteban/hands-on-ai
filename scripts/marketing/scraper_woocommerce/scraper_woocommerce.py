#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Web Scraping para WooCommerce - Amarantus Floristas
Extrae productos desde la tienda online y genera CSV compatible con WooCommerce
"""

import sys
import subprocess
import importlib.util
from datetime import datetime
import os

# Lista de dependencias requeridas
REQUIRED_PACKAGES = {
    'requests': 'requests',
    'bs4': 'beautifulsoup4',
    'lxml': 'lxml',
    'pandas': 'pandas',
    'PIL': 'Pillow',
    'slugify': 'python-slugify',
    'tqdm': 'tqdm'
}

def check_and_install_dependencies():
    """Verifica e instala las dependencias necesarias"""
    print("=" * 60)
    print("VERIFICANDO DEPENDENCIAS")
    print("=" * 60)

    missing_packages = []

    for module_name, package_name in REQUIRED_PACKAGES.items():
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            missing_packages.append(package_name)
            print(f"✗ {package_name} no encontrado")
        else:
            print(f"✓ {package_name} instalado")

    if missing_packages:
        print(f"\n{len(missing_packages)} paquete(s) faltante(s). Instalando...")
        for package in missing_packages:
            print(f"\nInstalando {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✓ {package} instalado correctamente")
            except subprocess.CalledProcessError as e:
                print(f"✗ Error instalando {package}: {e}")
                sys.exit(1)
        print("\n✓ Todas las dependencias instaladas correctamente")
        print("Reiniciando script...\n")
        # Reiniciar el script después de instalar dependencias
        os.execv(sys.executable, [sys.executable] + sys.argv)
    else:
        print("\n✓ Todas las dependencias están instaladas\n")

# Verificar e instalar dependencias
check_and_install_dependencies()

# Ahora importar las bibliotecas
import requests
from bs4 import BeautifulSoup
import pandas as pd
from PIL import Image
from io import BytesIO
from slugify import slugify
from tqdm import tqdm
import time
import re

# Configuración
BASE_URL = "https://amarantusfloristas.es"
SHOP_URL = f"{BASE_URL}/tienda/"
IMAGE_BASE_URL = "https://amarantus.esloogan.online/wp-content/uploads/2025/10/"
CSV_INPUT = "wc-product-export-27-10-2025-1761567643591.csv"
IMAGES_DIR = "./images"
RATE_LIMIT = 12  # Segundos entre requests

# Crear directorio de imágenes si no existe
os.makedirs(IMAGES_DIR, exist_ok=True)

class WooCommerceScraperAmarantus:
    """Scraper para tienda WooCommerce de Amarantus Floristas"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.products_data = []
        self.csv_headers = []

    def log(self, message, level="INFO"):
        """Función de logging"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")

    def read_csv_structure(self):
        """Lee la estructura del CSV original"""
        self.log("Leyendo estructura del CSV original...")
        try:
            df = pd.read_csv(CSV_INPUT, nrows=0, encoding='utf-8-sig')
            self.csv_headers = df.columns.tolist()
            self.log(f"CSV con {len(self.csv_headers)} columnas detectadas")
            return True
        except FileNotFoundError:
            self.log(f"ERROR: No se encontró el archivo {CSV_INPUT}", "ERROR")
            return False
        except Exception as e:
            self.log(f"ERROR leyendo CSV: {e}", "ERROR")
            return False

    def get_product_urls(self):
        """Extrae URLs de todos los productos desde las páginas de la tienda"""
        self.log("Extrayendo URLs de productos...")
        product_urls = []

        # Páginas 1-4 de la tienda
        pages = [SHOP_URL] + [f"{SHOP_URL}page/{i}/" for i in range(2, 5)]

        for page_url in tqdm(pages, desc="Scrapeando páginas"):
            try:
                response = self.session.get(page_url, timeout=30)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'lxml')

                # Buscar enlaces a productos
                products = soup.select('a[href*="/producto/"]')

                for product in products:
                    url = product.get('href')
                    if url and '/producto/' in url and url not in product_urls:
                        # Asegurar URL completa
                        if not url.startswith('http'):
                            url = BASE_URL + url
                        product_urls.append(url)

                time.sleep(RATE_LIMIT)

            except Exception as e:
                self.log(f"Error scrapeando {page_url}: {e}", "ERROR")

        # Eliminar duplicados y ordenar
        product_urls = sorted(list(set(product_urls)))
        self.log(f"✓ {len(product_urls)} productos encontrados")
        return product_urls

    def extract_product_data(self, product_url):
        """Extrae todos los datos de un producto individual"""
        try:
            response = self.session.get(product_url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')

            product_data = {}

            # ID del producto (desde URL o data attributes)
            product_id = self.extract_product_id(soup, product_url)
            product_data['ID'] = product_id

            # Tipo de producto
            product_data['Tipo'] = 'simple'

            # SKU
            sku_element = soup.find('span', class_='sku')
            product_data['SKU'] = sku_element.text.strip() if sku_element else ''

            # GTIN, UPC, EAN o ISBN
            product_data['GTIN, UPC, EAN o ISBN'] = ''

            # Nombre del producto
            title = soup.find('h1', class_='product_title')
            if not title:
                title = soup.find('h1')
            product_data['Nombre'] = title.text.strip() if title else ''

            # Publicado
            product_data['Publicado'] = 1

            # Destacado
            product_data['¿Está destacado?'] = 0

            # Visibilidad
            product_data['Visibilidad en el catálogo'] = 'visible'

            # Descripción corta
            short_desc = soup.find('div', class_='woocommerce-product-details__short-description')
            if not short_desc:
                short_desc = soup.find('div', class_='product-short-description')
            product_data['Descripción corta'] = short_desc.text.strip() if short_desc else ''

            # Descripción completa
            full_desc = soup.find('div', {'id': 'tab-description'})
            if not full_desc:
                full_desc = soup.find('div', class_='woocommerce-Tabs-panel--description')
            if not full_desc:
                full_desc = soup.find('div', {'id': 'description'})
            product_data['Descripción'] = full_desc.text.strip() if full_desc else ''

            # Fechas de precio rebajado
            product_data['Día en que empieza el precio rebajado'] = ''
            product_data['Día en que termina el precio rebajado'] = ''

            # Impuestos
            product_data['Estado del impuesto'] = 'taxable'
            product_data['Clase de impuesto'] = ''

            # Stock
            stock_status = soup.find('p', class_='stock')
            in_stock = stock_status and 'in-stock' in stock_status.get('class', [])
            product_data['¿Existencias?'] = 1 if in_stock else 0
            product_data['Inventario'] = ''
            product_data['Cantidad de bajo inventario'] = ''
            product_data['¿Permitir reservas de productos agotados?'] = 0

            # Vendido individualmente
            product_data['¿Vendido individualmente?'] = 0

            # Dimensiones y peso
            product_data['Peso (lbs)'] = ''
            product_data['Longitud (in)'] = ''
            product_data['Anchura (in)'] = ''
            product_data['Altura (in)'] = ''

            # Valoraciones
            product_data['¿Permitir valoraciones de clientes?'] = 1

            # Nota de compra
            product_data['Nota de compra'] = ''

            # Precios
            price_data = self.extract_prices(soup)
            product_data['Precio rebajado'] = price_data['sale_price']
            product_data['Precio normal'] = price_data['regular_price']

            # Categorías
            categories = self.extract_categories(soup)
            product_data['Categorías'] = ', '.join(categories)

            # Etiquetas
            tags = self.extract_tags(soup)
            product_data['Etiquetas'] = ', '.join(tags)

            # Clase de envío
            product_data['Clase de envío'] = ''

            # Imágenes
            images = self.extract_and_download_images(soup, product_data['Nombre'], product_id)
            product_data['Imágenes'] = ', '.join(images)

            # Descargas
            product_data['Límite de descargas'] = ''
            product_data['Días de caducidad de la descarga'] = ''

            # Producto superior
            product_data['Superior'] = ''

            # Productos agrupados
            product_data['Productos agrupados'] = ''

            # Ventas
            product_data['Ventas dirigidas'] = ''
            product_data['Ventas cruzadas'] = ''

            # URL externa
            product_data['URL externa'] = ''
            product_data['Texto del botón'] = ''

            # Posición
            product_data['Posición'] = 0

            # Marcas
            product_data['Marcas'] = ''

            # Meta AIOSEO
            product_data['Meta: _aioseo_og_title'] = ''
            product_data['Meta: _aioseo_og_description'] = ''
            product_data['Meta: _aioseo_og_article_section'] = ''
            product_data['Meta: _aioseo_twitter_title'] = ''
            product_data['Meta: _aioseo_twitter_description'] = ''

            return product_data

        except Exception as e:
            self.log(f"Error extrayendo datos de {product_url}: {e}", "ERROR")
            return None

    def extract_product_id(self, soup, url):
        """Extrae el ID del producto"""
        # Intentar desde el artículo
        article = soup.find('article')
        if article and article.get('id'):
            match = re.search(r'post-(\d+)', article.get('id'))
            if match:
                return match.group(1)

        # Intentar desde botón add-to-cart
        add_to_cart = soup.find('button', {'name': 'add-to-cart'})
        if add_to_cart and add_to_cart.get('value'):
            return add_to_cart.get('value')

        # Último recurso: desde URL
        match = re.search(r'/producto/([^/]+)/', url)
        if match:
            return slugify(match.group(1))

        return ''

    def extract_prices(self, soup):
        """Extrae precios del producto"""
        prices = {'regular_price': '', 'sale_price': ''}

        # Buscar precio
        price_elem = soup.find('p', class_='price')
        if price_elem:
            # Precio rebajado
            sale_price = price_elem.find('ins')
            if sale_price:
                price_text = sale_price.get_text(strip=True)
                prices['sale_price'] = re.sub(r'[^\d.,]', '', price_text)

                # Precio regular
                regular_price = price_elem.find('del')
                if regular_price:
                    price_text = regular_price.get_text(strip=True)
                    prices['regular_price'] = re.sub(r'[^\d.,]', '', price_text)
            else:
                # Solo precio regular
                price_text = price_elem.get_text(strip=True)
                prices['regular_price'] = re.sub(r'[^\d.,]', '', price_text)

        return prices

    def extract_categories(self, soup):
        """Extrae categorías del producto"""
        categories = []

        # Buscar en breadcrumbs
        breadcrumb = soup.find('nav', class_='woocommerce-breadcrumb')
        if breadcrumb:
            links = breadcrumb.find_all('a')
            for link in links:
                text = link.text.strip()
                if text and text.lower() not in ['inicio', 'home', 'tienda', 'shop']:
                    categories.append(text)

        # Buscar en categorías de producto
        cat_links = soup.find_all('a', {'rel': 'tag'})
        for link in cat_links:
            if '/categoria-producto/' in link.get('href', ''):
                categories.append(link.text.strip())

        return list(set(categories))

    def extract_tags(self, soup):
        """Extrae etiquetas del producto"""
        tags = []

        tag_links = soup.find_all('a', {'rel': 'tag'})
        for link in tag_links:
            if '/etiqueta-producto/' in link.get('href', ''):
                tags.append(link.text.strip())

        return tags

    def extract_and_download_images(self, soup, product_name, product_id):
        """Extrae URLs de imágenes, las descarga y genera URLs optimizadas para SEO"""
        image_urls = []
        final_urls = []

        # Buscar galería de imágenes
        gallery = soup.find('div', class_='woocommerce-product-gallery')
        if gallery:
            images = gallery.find_all('img')
            for img in images:
                src = img.get('src') or img.get('data-src') or img.get('data-large_image')
                if src and src not in image_urls:
                    image_urls.append(src)

        # Si no hay galería, buscar imagen principal
        if not image_urls:
            main_img = soup.find('img', class_='wp-post-image')
            if main_img:
                src = main_img.get('src') or main_img.get('data-src')
                if src:
                    image_urls.append(src)

        # Descargar y renombrar imágenes
        for idx, img_url in enumerate(image_urls, start=1):
            try:
                # Generar nombre SEO
                slug = slugify(product_name)
                extension = img_url.split('.')[-1].split('?')[0]
                if extension not in ['jpg', 'jpeg', 'png', 'webp', 'gif']:
                    extension = 'webp'

                if len(image_urls) > 1:
                    filename = f"{slug}-amarantus-floristas-{idx}.{extension}"
                else:
                    filename = f"{slug}-amarantus-floristas.{extension}"

                filepath = os.path.join(IMAGES_DIR, filename)

                # Descargar imagen
                response = self.session.get(img_url, timeout=30)
                response.raise_for_status()

                # Guardar imagen
                with open(filepath, 'wb') as f:
                    f.write(response.content)

                # Generar URL final
                final_url = IMAGE_BASE_URL + filename
                final_urls.append(final_url)

            except Exception as e:
                self.log(f"Error descargando imagen {img_url}: {e}", "WARNING")

        return final_urls

    def scrape_all_products(self):
        """Scrapea todos los productos de la tienda"""
        self.log("=" * 60)
        self.log("INICIANDO SCRAPING DE PRODUCTOS")
        self.log("=" * 60)

        # Obtener URLs de productos
        product_urls = self.get_product_urls()

        if not product_urls:
            self.log("No se encontraron productos para scrapear", "ERROR")
            return False

        # Scrapear cada producto
        self.log(f"\nScrapeando {len(product_urls)} productos...")

        for url in tqdm(product_urls, desc="Procesando productos"):
            product_data = self.extract_product_data(url)
            if product_data:
                self.products_data.append(product_data)
            time.sleep(RATE_LIMIT)

        self.log(f"\n✓ {len(self.products_data)} productos extraídos correctamente")
        return True

    def generate_csv(self):
        """Genera el CSV con la estructura idéntica al original"""
        self.log("=" * 60)
        self.log("GENERANDO CSV")
        self.log("=" * 60)

        if not self.products_data:
            self.log("No hay datos para exportar", "ERROR")
            return False

        # Crear DataFrame con los datos
        df = pd.DataFrame(self.products_data)

        # Asegurar que todas las columnas del CSV original estén presentes
        for col in self.csv_headers:
            if col not in df.columns:
                df[col] = ''

        # Ordenar columnas según el CSV original
        df = df[self.csv_headers]

        # Generar nombre de archivo
        timestamp = datetime.now().strftime("%d-%m-%Y-%H%M%S")
        output_file = f"wc-product-export-complete-{timestamp}.csv"

        # Guardar CSV con encoding UTF-8 con BOM (igual que el original)
        df.to_csv(output_file, index=False, encoding='utf-8-sig')

        self.log(f"✓ CSV generado: {output_file}")
        self.log(f"✓ Total de productos: {len(df)}")
        self.log(f"✓ Imágenes descargadas en: {IMAGES_DIR}/")

        return True

    def run(self):
        """Ejecuta el proceso completo de scraping"""
        print("\n" + "=" * 60)
        print("SCRAPER WOOCOMMERCE - AMARANTUS FLORISTAS")
        print("=" * 60 + "\n")

        # Leer estructura CSV
        if not self.read_csv_structure():
            return False

        # Scrapear productos
        if not self.scrape_all_products():
            return False

        # Generar CSV
        if not self.generate_csv():
            return False

        print("\n" + "=" * 60)
        print("✓ PROCESO COMPLETADO EXITOSAMENTE")
        print("=" * 60 + "\n")

        return True

if __name__ == "__main__":
    scraper = WooCommerceScraperAmarantus()
    success = scraper.run()
    sys.exit(0 if success else 1)
