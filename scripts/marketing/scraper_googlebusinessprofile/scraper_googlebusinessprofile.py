"""
Script para extraer información de Google Business Profile usando web scraping
"""

from playwright.sync_api import sync_playwright
import json
import time


def extract_gmb_data(url, timeout=30000):
    """
    Extrae datos de un perfil de Google Business Profile

    Args:
        url: URL del perfil de Google Business
        timeout: Tiempo máximo de espera en milisegundos

    Returns:
        dict: Diccionario con la información del negocio
    """
    data = {
        'url': url,
        'nombre': None,
        'categoria': None,
        'calificacion': None,
        'total_resenas': None,
        'direccion': None,
        'telefono': None,
        'sitio_web': None,
        'horarios': {},
        'descripcion': None,
        'atributos': [],
        'coordenadas': None
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            print(f"Accediendo a: {url}")
            page.goto(url, wait_until='networkidle', timeout=timeout)
            time.sleep(3)  # Espera adicional para carga dinámica

            # Nombre del negocio
            try:
                nombre = page.locator('h1.DUwDvf').first
                if nombre.is_visible():
                    data['nombre'] = nombre.inner_text()
            except:
                pass

            # Categoría
            try:
                categoria = page.locator('button.DkEaL').first
                if categoria.is_visible():
                    data['categoria'] = categoria.inner_text()
            except:
                pass

            # Calificación y reseñas
            try:
                rating_element = page.locator('div.F7nice span[aria-hidden="true"]').first
                if rating_element.is_visible():
                    data['calificacion'] = rating_element.inner_text()

                reviews_element = page.locator('div.F7nice span[aria-label*="reseña"]').first
                if reviews_element.is_visible():
                    reviews_text = reviews_element.get_attribute('aria-label')
                    data['total_resenas'] = reviews_text
            except:
                pass

            # Información de contacto (dirección, teléfono, web)
            try:
                buttons = page.locator('button[data-item-id*="address"], button[data-item-id*="phone"], button[data-item-id*="authority"]').all()

                for button in buttons:
                    aria_label = button.get_attribute('aria-label') or ''

                    if 'Dirección' in aria_label or 'Address' in aria_label:
                        data['direccion'] = button.locator('div.Io6YTe').inner_text()
                    elif 'Teléfono' in aria_label or 'Phone' in aria_label:
                        data['telefono'] = button.locator('div.Io6YTe').inner_text()
                    elif 'Sitio' in aria_label or 'Website' in aria_label:
                        data['sitio_web'] = button.locator('div.Io6YTe').inner_text()
            except Exception as e:
                print(f"Error extrayendo contacto: {e}")

            # Horarios
            try:
                # Click en el botón de horarios si existe
                horarios_button = page.locator('button[data-item-id*="oh"], button[aria-label*="Horario"]').first
                if horarios_button.is_visible():
                    horarios_button.click()
                    time.sleep(1)

                    # Extraer horarios
                    dias = page.locator('table.eK4R0e tr').all()
                    for dia in dias:
                        try:
                            nombre_dia = dia.locator('td:first-child').inner_text()
                            horario_dia = dia.locator('td:last-child').inner_text()
                            data['horarios'][nombre_dia] = horario_dia
                        except:
                            pass
            except:
                pass

            # Descripción (si está disponible)
            try:
                descripcion = page.locator('div.WeS02d.fontBodyMedium').first
                if descripcion.is_visible():
                    data['descripcion'] = descripcion.inner_text()
            except:
                pass

            # Atributos (accesibilidad, servicios, etc)
            try:
                atributos = page.locator('div.iP2t7d.fontBodyMedium').all()
                for atributo in atributos:
                    try:
                        texto = atributo.inner_text()
                        if texto:
                            data['atributos'].append(texto)
                    except:
                        pass
            except:
                pass

            # Extraer coordenadas de la URL
            try:
                current_url = page.url
                if '@' in current_url:
                    coords_part = current_url.split('@')[1].split('/')[0]
                    coords = coords_part.split(',')[:2]
                    data['coordenadas'] = {
                        'latitud': coords[0],
                        'longitud': coords[1]
                    }
            except:
                pass

            print("✓ Extracción completada")

        except Exception as e:
            print(f"Error durante la extracción: {e}")

        finally:
            browser.close()

    return data


def save_to_json(data, filename='business_data.json'):
    """Guarda los datos en un archivo JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✓ Datos guardados en {filename}")


def print_business_info(data):
    """Imprime la información del negocio de forma legible"""
    print("\n" + "="*60)
    print("INFORMACIÓN DEL NEGOCIO")
    print("="*60)

    if data['nombre']:
        print(f"\n📍 Nombre: {data['nombre']}")
    if data['categoria']:
        print(f"🏷️  Categoría: {data['categoria']}")
    if data['calificacion']:
        print(f"⭐ Calificación: {data['calificacion']}")
    if data['total_resenas']:
        print(f"💬 Reseñas: {data['total_resenas']}")
    if data['direccion']:
        print(f"📫 Dirección: {data['direccion']}")
    if data['telefono']:
        print(f"📞 Teléfono: {data['telefono']}")
    if data['sitio_web']:
        print(f"🌐 Sitio web: {data['sitio_web']}")

    if data['horarios']:
        print(f"\n🕐 Horarios:")
        for dia, horario in data['horarios'].items():
            print(f"   {dia}: {horario}")

    if data['descripcion']:
        print(f"\n📝 Descripción: {data['descripcion']}")

    if data['atributos']:
        print(f"\n✨ Atributos:")
        for attr in data['atributos']:
            print(f"   • {attr}")

    if data['coordenadas']:
        print(f"\n🗺️  Coordenadas: {data['coordenadas']['latitud']}, {data['coordenadas']['longitud']}")

    print("\n" + "="*60)


if __name__ == "__main__":
    # URL de ejemplo
    url = "https://maps.app.goo.gl/uaqvw7LUiGAft3qQ7"

    print("Iniciando extracción de datos de Google Business Profile...")

    # Extraer datos
    business_data = extract_gmb_data(url)

    # Mostrar información
    print_business_info(business_data)

    # Guardar en JSON
    save_to_json(business_data)
